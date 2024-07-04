from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from mysql import connector
from sqlalchemy import Column, Integer, String

##################################################################################
            # for database connection with mysql database 
            # install: pip install pymysql and pip install mysql-connector-python
##################################################################################

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/maitri_email"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
