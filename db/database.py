from typing import Union, Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends
from contextlib import contextmanager
from datetime import datetime

# Create FastAPI instance
app = FastAPI()

# Variable database
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Sen to SQLite
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Func CreateTable
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# ฟังก์ชัน get_session สำหรับ dependency injection
def get_session():
    with Session(engine) as session:
        yield session

# ใช้ Annotated สำหรับ dependency
SessionDep = Annotated[Session, Depends(get_session)]

#Create Table at Rundev
@app.on_event("startup")
def on_startup():
    create_db_and_tables()



