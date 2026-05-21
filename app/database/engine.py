from sqlmodel import Session, create_engine

from app.config import settings

connect_args = {"check_same_thread": False} if settings.is_sqlite else {}
engine = create_engine(settings.database_url, connect_args=connect_args or None)


def get_session():
    with Session(engine) as session:
        yield session
