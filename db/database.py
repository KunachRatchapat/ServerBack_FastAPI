from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = ""
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    from db.model import Vegetable, Users , Favorite , Fruit
    SQLModel.metadata.create_all(engine)
    
    
def get_session():
    with Session(engine) as session:
        yield session