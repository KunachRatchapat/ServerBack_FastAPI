from fastapi import FastAPI
from db.database import create_db_and_tables
from routers import vegetable,favorite

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
    
app.include_router(vegetable.router)
app.include_router(favorite.router , prefix="/favorite")
