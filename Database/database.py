from typing import Union
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI , Request 
from pydantic import BaseModel


    
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


#Request Variable
SessionDep = Annotated[Session, Depends(get_session)] 

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    


