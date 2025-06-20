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

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables correctly
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# SQLAlchemy database URL
URL_DATABASE = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine

engine = create_engine(URL_DATABASE)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

for db in get_db():
    print("✅ Connected to Railway DB!")

