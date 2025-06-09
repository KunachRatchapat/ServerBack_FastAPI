from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

#load .env file
load_dotenv() 

#Read .env file
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT","5432")

# เชื่อมไปยัง Postgres ที่รันใน Docker
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

#create DB
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    from db.model import Vegetable, Users , Favorite , Fruit
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
