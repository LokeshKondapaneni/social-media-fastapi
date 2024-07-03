from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg

SQLALCHEMY_DB_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

# Connecting to Postgres DB for raw SQL commands
"""
try:
    conn = psycopg.connect(dbname="fastapi", host= 'localhost', user='postgres',
                           password='What123@', port=5432)
    cursor = conn.cursor()
    print("Connection to DB successfull")
except Exception as error:
    print('Connection failed- ', error)
"""