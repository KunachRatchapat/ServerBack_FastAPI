import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(DATABASE_URL)


# ฟังก์ชันสร้างตาราง
def create_db_and_tables():
    
    from db.models import vegetable_model, user_model, favorite_model, fruit_model
    SQLModel.metadata.create_all(bind=engine) 


# ฟังก์ชัน Session
def get_session():
    with Session(engine) as session: 
        yield session