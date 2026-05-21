from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.core.security import hash_password
from app.database.engine import get_session
from app.main import app
from db.models.user_model import Users

TEST_DB_URL = "sqlite:///./test.db"
_test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})


def override_get_session() -> Generator[Session, None, None]:
    with Session(_test_engine) as session:
        yield session


@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(_test_engine)
    yield
    SQLModel.metadata.drop_all(_test_engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def db() -> Generator[Session, None, None]:
    with Session(_test_engine) as session:
        yield session


@pytest.fixture
def admin_token(client: TestClient) -> str:
    with Session(_test_engine) as db:
        user = Users(
            email="admin@test.com",
            password=hash_password("admin123"),
            username="admin",
            surname="Admin",
            role="admin",
            is_verified=True,
        )
        db.add(user)
        db.commit()
    r = client.post("/api/v1/auth/login", json={"email": "admin@test.com", "password": "admin123"})
    return r.json()["result"]["access_token"]


@pytest.fixture
def user_token(client: TestClient) -> str:
    with Session(_test_engine) as db:
        user = Users(
            email="user@test.com",
            password=hash_password("user123"),
            username="user",
            surname="User",
            role="user",
            is_verified=True,
        )
        db.add(user)
        db.commit()
    r = client.post("/api/v1/auth/login", json={"email": "user@test.com", "password": "user123"})
    return r.json()["result"]["access_token"]


@pytest.fixture
def admin_headers(admin_token: str) -> dict:
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def user_headers(user_token: str) -> dict:
    return {"Authorization": f"Bearer {user_token}"}
