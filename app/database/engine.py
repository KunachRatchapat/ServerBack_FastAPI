from sqlalchemy import text
from sqlmodel import Session, create_engine

from app.config import settings

if settings.is_sqlite:
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.database_url)

_db_display_url = settings.database_url
if settings.DB_PASSWORD:
    _db_display_url = _db_display_url.replace(settings.DB_PASSWORD, "****")
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print(f"[DB] Connected: {_db_display_url}")
except Exception as e:
    print(f"[DB] Connection FAILED: {e}")
    print(f"[DB] URL: {_db_display_url}")


def get_session():
    with Session(engine) as session:
        yield session
