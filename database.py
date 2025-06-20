from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_HOST = os.getenv("mysql.railway.internal")
DB_PORT = os.getenv("3306")
DB_NAME = os.getenv("railway")
DB_USER = os.getenv("root")
DB_PASS = os.getenv("jxVjzFSyzajoGSTzaFPibAiLibMmOETE")


URL_DATABASE =  f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)
Base = declarative_base()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
