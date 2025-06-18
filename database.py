from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_DATABASE = "mysql+pymysql://root:root@localhost:3306/1000farms"
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)
Base = declarative_base()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()