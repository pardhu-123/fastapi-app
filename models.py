from sqlalchemy import Column, String,Integer,Float, ForeignKey, Enum, TIMESTAMP,Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base

class Dealer(Base):
    __tablename__ = "dealers"

    dealer_id = Column(Integer, primary_key=True, index=True)
    NAME_OF_THE_FIRM = Column(String(255))
    NAME_OF_THE_PROPRIETOR = Column(String(255))
    ADDRESS = Column(String(255))
    DIVISION = Column(String(100))
    CONTACT_NO = Column(String(50))
    FIRM_TYPE = Column(String(100))
    GST_NO = Column(String(100))
    PESTISIDE_LICENSE = Column(String(100))
    SEEDS_LICENSE = Column(String(100))
    FERTILIZERS_LICENSE = Column(String(100))
    BANK_NAME = Column(String(100))
    BANK_ACCOUNT_NO = Column(String(100))
    IFSC_CODE = Column(String(50))
    CHEQUE_NO = Column(String(100))
    PAN_CARD_NO = Column(String(100))
    AADHAR_CARD_NO = Column(String(100))
    EMAIL = Column(String(255))
    Building_No_Flat_No = Column(String(100))
    Name_Of_Premises_Building = Column(String(255))
    Road_Street = Column(String(255))
    Nearby_Landmark = Column(String(255))
    Locality_Sub_Locality = Column(String(255))
    City_Town_Village = Column(String(100))
    District = Column(String(100))
    Floor_No = Column(String(50))
    State = Column(String(100))
    PIN_Code = Column(String(20))
    Dates = Column(String(30))
    dealer_products = relationship("DealerProduct", back_populates="dealer")
    transactions = relationship("Transactions", back_populates="dealer")



class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Product = Column(String(255), nullable=False)
    HSN_code = Column(String(100), nullable=False)
    MRP = Column(Float, nullable=False)
    dealer_products = relationship("DealerProduct", back_populates="product")
    transactions = relationship("Transactions", back_populates="product")


class DealerProduct(Base):
    __tablename__ = "dealer_products"
    id = Column(Integer, primary_key=True, index=True)
    dealer_id = Column(Integer, ForeignKey("dealers.dealer_id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    Product_name = Column(String, nullable = True)
    date = Column(Date)
    sender_id = Column(Integer)

    sale_from = Column(String, nullable=True)  # Name of sender
    sale_to = Column(String, nullable=True)    # Name of receiver

    dealer = relationship("Dealer", back_populates="dealer_products")  # ✅ fixed
    product = relationship("Product", back_populates="dealer_products")

class Transactions(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    dealer_id = Column(Integer, ForeignKey("dealers.dealer_id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    Product_name = Column(String, nullable = True)
    date = Column(Date)
    sale_from = Column(String, nullable=True)  # Name of sender
    sale_to = Column(String, nullable=True)    # Name of receiver
    dealer = relationship("Dealer", back_populates="transactions")  # ✅ fixed
    product = relationship("Product", back_populates="transactions")

