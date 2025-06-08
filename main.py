from fastapi import FastAPI
from db.database import create_db_and_tables
from routers import vegetable

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Router สำหรับ Vegetable
app.include_router(vegetable.router)
