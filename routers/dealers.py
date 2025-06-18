from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from database import get_db
from datetime import datetime, date
import models 
from models import DealerProduct

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dealers/new", response_class=HTMLResponse)
async def show_add_form(request: Request):
    return templates.TemplateResponse("dealer_detail.html", {"request": request, "dealer": None})



@router.get("/dealers/{dealer_id}", response_class=HTMLResponse)
async def dealer_detail(request: Request, dealer_id: int, db: Session = Depends(get_db)):
    dealer = db.query(models.Dealer).filter(models.Dealer.dealer_id == dealer_id).first()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    dealer_products = db.query(DealerProduct).filter(DealerProduct.dealer_id == dealer_id).all()
    other_dealers = db.query(models.Dealer).filter(models.Dealer.dealer_id != dealer_id).all()

    return templates.TemplateResponse("dealer_detail.html", {
        "request": request,
        "dealer": dealer,
        "dealer_products": dealer_products,
        "current_date": date.today().isoformat(),
        "other_dealers": other_dealers
    })

@router.post("/dealers/save")
async def save_dealer_changes(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    dealer_id = int(form.get("dealer_id"))  # if you're using a hidden field
    dealer = db.query(models.Dealer).filter_by(dealer_id=dealer_id).first()

    if dealer:
        dealer.State = form.get("State")
        dealer.CONTACT_NO = form.get("CONTACT_NO")
        dealer.District = form.get("District")
        # ... other fields if you allow them to be edited

        db.commit()
        return RedirectResponse(url=f"/dealers/{dealer_id}", status_code=302)
    else:
        raise HTTPException(status_code=404, detail="Dealer not found")







@router.get("/dealers/{dealer_id}/products", response_class=HTMLResponse)
async def dealer_products(request: Request, dealer_id: int, db: Session = Depends(get_db)):
    dealer = db.query(models.Dealer).filter(models.Dealer.dealer_id == dealer_id).first()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    dealer_products = db.query(DealerProduct).filter(DealerProduct.dealer_id == dealer_id).all()

    return templates.TemplateResponse("dealer_products.html", {
        "request": request,
        "dealer": dealer,
        "dealer_products": dealer_products
    })

@router.post("/dealers/{dealer_id}/buy")
async def buy_product(
    dealer_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    
    # Get common fields
    sale_to = form_data.get("sale_to", "")  # Added strip() to clean input
    date_str = form_data.get("date_str", "").strip()
    
    # Parse date
    try:
        transfer_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Get sender info
    sender = db.query(models.Dealer).filter(models.Dealer.dealer_id == dealer_id).first()
    if not sender:
        raise HTTPException(status_code=404, detail="Sender dealer not found")

    sender_name = sender.NAME_OF_THE_FIRM
    receiver_name = sale_to

    # If sale to "Farmer", no dealer_id; else fetch receiver dealer_id
    receiver_id = None
    if receiver_name != "Farmer":
        receiver = db.query(models.Dealer).filter(
            func.lower(models.Dealer.NAME_OF_THE_FIRM) == func.lower(receiver_name)
        ).first()
        if not receiver:
            raise HTTPException(status_code=404, detail="Receiver dealer not found.")
        receiver_id = receiver.dealer_id

    # Process each product
    products_data = []
    for key, value in form_data.items():
        if key.startswith("products["):
            # Extract index and field name (e.g., "products[0][product_id]" -> 0, "product_id")
            parts = key.split("[")
            idx = parts[1].split("]")[0]
            field = parts[2].rstrip("]")
            
            # Ensure we have an entry for this product
            while len(products_data) <= int(idx):
                products_data.append({})
            
            products_data[int(idx)][field] = value

    # Validate we have at least one product
    if not products_data:
        raise HTTPException(status_code=400, detail="No products specified for transfer")

    # Process each product transfer
    for product in products_data:
        product_id = product.get("product_id")
        quantity = product.get("quantity")
        
        if not product_id or not quantity:
            continue  # Skip invalid entries
            
        try:
            quantity = int(quantity)
            product_id = int(product_id)
        except ValueError:
            continue  # Skip invalid entries

        # Get sender's product
        sender_dp = db.query(DealerProduct).filter(
            DealerProduct.id == product_id,
            DealerProduct.dealer_id == dealer_id
        ).first()
        
        if not sender_dp:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found for this dealer.")

        if sender_dp.quantity < quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient quantity to transfer for product ID {product_id}.")
        
        product_obj = db.query(models.Product).filter(models.Product.id == sender_dp.product_id).first()
        if not product_obj:
            raise HTTPException(status_code=404, detail=f"Product details not found for ID {sender_dp.product_id}.")

        product_name = product_obj.Product  # Assuming the column name is `Product`

        # Deduct from sender
        sender_dp.quantity -= quantity

        # Check if receiver already has this product
        existing_dp = None
        if receiver_id:
            existing_dp = db.query(DealerProduct).filter(
                DealerProduct.dealer_id == receiver_id,
                DealerProduct.product_id == sender_dp.product_id,
                DealerProduct.sender_id == sender.dealer_id
            ).first()

        if existing_dp:
            # Update quantity and date
            existing_dp.quantity += quantity
            existing_dp.date = transfer_date
            existing_dp.sale_from = sender_name
            existing_dp.sale_to = receiver_name
            existing_dp.Product_name = product_name
        else:
            # Create new dealer product entry for receiver
            new_dp = DealerProduct(
                dealer_id=receiver_id,
                sender_id = sender.dealer_id,
                product_id=sender_dp.product_id,
                Product_name=product_name,
                quantity=quantity,
                date=transfer_date,
                sale_from=sender_name,
                sale_to=receiver_name
            )
            db.add(new_dp)
        transaction = models.Transactions(
            dealer_id=sender.dealer_id,
            product_id=sender_dp.product_id,
            Product_name=product_name,
            quantity=quantity,
            date=transfer_date,
            sale_from=sender_name,
            sale_to=receiver_name
        )
        db.add(transaction)
    db.commit()
    return RedirectResponse(url=f"/dealers/{dealer_id}", status_code=303)