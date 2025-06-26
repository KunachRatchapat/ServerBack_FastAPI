from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# โหลด .env
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


DATABASE_URL = (   f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
                    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
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
