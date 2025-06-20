from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from database import SessionLocal, engine, get_db

# Initialize app first
app = FastAPI()

# Database setup
models.Base.metadata.create_all(bind=engine)

# Templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Import routers BEFORE routes to avoid circular imports
from routers.dealers import router as dealers_router
from routers.product import router as product_router
from routers.add_new_dealers import router as add_new_dealers_router

app.include_router(dealers_router)
app.include_router(product_router)
app.include_router(add_new_dealers_router)



# Root route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Direct dealer routes (consider moving to routers/dealers.py)
@app.get("/dealers", response_class=HTMLResponse)
def read_dealers(request: Request, page: int = 1, db: Session = Depends(get_db)):
    per_page = 10
    offset = (page - 1) * per_page

    total = db.query(func.count(models.Dealer.dealer_id)).scalar()
    dealers = db.query(models.Dealer).offset(offset).limit(per_page).all()
    
    total_pages = (total + per_page - 1) // per_page

    return templates.TemplateResponse("dealers.html", {
        "request": request,
        "dealers": dealers,
        "page": page,
        "total_pages": total_pages
    })

# Search route
@app.get("/search")
def list_dealers(request: Request, q: str = "", page: int = 1, db: Session = Depends(get_db)):
    page_size = 10
    query = db.query(models.Dealer)

    if q:
        q_like = f"%{q}%"
        query = query.filter(
            (models.Dealer.NAME_OF_THE_FIRM.ilike(q_like)) |
            (models.Dealer.CONTACT_NO.ilike(q_like)) |
            (models.Dealer.State.ilike(q_like)) |
            (models.Dealer.NAME_OF_THE_PROPRIETOR.ilike(q_like))
        )

    total = query.count()
    dealers = query.offset((page - 1) * page_size).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size

    return templates.TemplateResponse("dealers.html", {
        "request": request,
        "dealers": dealers,
        "q": q,
        "page": page,
        "total_pages": total_pages,
    })






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
