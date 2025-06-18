from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from sqlalchemy import func
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter(prefix="/products", tags=["products"])
templates = Jinja2Templates(directory="templates")

# HTML Routes
@router.get("/", response_class=HTMLResponse)
async def list_products(request: Request, page: int = 1, db: Session = Depends(get_db)):
    per_page = 10
    offset = (page - 1) * per_page

    total = db.query(func.count(models.Product.id)).scalar()
    products = db.query(models.Product).offset(offset).limit(per_page).all()
    
    total_pages = (total + per_page - 1) // per_page

    return templates.TemplateResponse("products.html", {
        "request": request,
        "products": products,
        "page": page,
        "total_pages": total_pages
    })

@router.get("/new", response_class=HTMLResponse)
async def new_product_form(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})

@router.post("/", response_class=RedirectResponse)
async def create_product_from_form(
    request: Request,
    Product: str = Form(...),
    HSN_CODE: str = Form(...),
    MRP: float = Form(...),
    db: Session = Depends(get_db)
):
    new_product = models.Product(
        Product=Product,
        HSN_CODE=HSN_CODE,
        MRP=MRP
    )
    db.add(new_product)
    db.commit()
    return RedirectResponse(url="/products", status_code=303)

@router.get("/search", response_class=HTMLResponse)
async def search_products(
    request: Request, 
    q: str = "", 
    page: int = 1, 
    db: Session = Depends(get_db)
):
    page_size = 10
    query = db.query(models.Product)

    if q:
        q_like = f"%{q}%"
        query = query.filter(
            (models.Product.Product.ilike(q_like)) |
            (models.Product.HSN_CODE.ilike(q_like))
        )

    total = query.count()
    products = query.offset((page - 1) * page_size).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size

    return templates.TemplateResponse("products.html", {
        "request": request,
        "products": products,
        "q": q,
        "page": page,
        "total_pages": total_pages,
    })

# API Routes
@router.post("/api/")
async def create_product_api(
    product: schemas.ProductCreate, 
    db: Session = Depends(get_db)
):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/api/{product_id}")
async def get_product_api(
    product_id: int, 
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product