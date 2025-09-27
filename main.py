from fastapi import FastAPI
from db.database import create_db_and_tables
from routers import users, vegetable,favorite,fruit,search,admin, prediction

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
    
app.include_router(vegetable.router)
app.include_router(favorite.router)
app.include_router(fruit.router)
app.include_router(search.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(prediction.router)




