# routers/add_new_dealers.py

from fastapi import APIRouter, Form, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from database import get_db
import models

router = APIRouter()

@router.post("/dealers/save")
def save_dealer(
    NAME_OF_THE_FIRM: str = Form(...),
    NAME_OF_THE_PROPRIETOR: str = Form(...),
    ADDRESS: str = Form(...),
    DIVISION: str = Form(...),
    CONTACT_NO: str = Form(...),
    FIRM_TYPE: str = Form(...),
    GST_NO: str = Form(...),
    PESTISIDE_LICENSE: str = Form(...),
    SEEDS_LICENSE: str = Form(...),
    FERTILIZERS_LICENSE: str = Form(...),
    BANK_NAME: str = Form(...),
    BANK_ACCOUNT_NO: str = Form(...),
    IFSC_CODE: str = Form(...),
    CHEQUE_NO: str = Form(...),
    PAN_CARD_NO: str = Form(...),
    AADHAR_CARD_NO: str = Form(...),
    EMAIL: str = Form(...),
    City_Town_Village: str = Form(...),
    Floor_No: str = Form(...),
    District: str = Form(...),
    State: str = Form(...),
    PIN_Code: str = Form(...),
    Dates: str = Form(...),
    db: Session = Depends(get_db),
):
    dealer = models.Dealer(
        NAME_OF_THE_FIRM=NAME_OF_THE_FIRM,
        NAME_OF_THE_PROPRIETOR=NAME_OF_THE_PROPRIETOR,
        ADDRESS=ADDRESS,
        DIVISION=DIVISION,
        CONTACT_NO=CONTACT_NO,
        FIRM_TYPE=FIRM_TYPE,
        GST_NO=GST_NO,
        PESTISIDE_LICENSE=PESTISIDE_LICENSE,
        SEEDS_LICENSE=SEEDS_LICENSE,
        FERTILIZERS_LICENSE=FERTILIZERS_LICENSE,
        BANK_NAME=BANK_NAME,
        BANK_ACCOUNT_NO=BANK_ACCOUNT_NO,
        IFSC_CODE=IFSC_CODE,
        CHEQUE_NO=CHEQUE_NO,
        PAN_CARD_NO=PAN_CARD_NO,
        AADHAR_CARD_NO=AADHAR_CARD_NO,
        EMAIL=EMAIL,
        City_Town_Village=City_Town_Village,
        Floor_No=Floor_No,
        District=District,
        State=State,
        PIN_Code=PIN_Code,
        Dates=Dates
    )
    db.add(dealer)
    db.commit()
    db.refresh(dealer)
    return RedirectResponse(url="/", status_code=303)
