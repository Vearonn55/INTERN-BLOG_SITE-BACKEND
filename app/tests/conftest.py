# app/tests/conftest.py

import pytest
from app import create_app
from app.engine import engine
from sqlmodel import SQLModel, Session
from app.models.user import User


@pytest.fixture(scope="session")
def app():
    app = create_app()
    yield app


@pytest.fixture(scope="function")
def session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    res = client.post("/api/login", json={
        "email": "admin@example.com",
        "password": "securepass"
    })
    assert res.status_code == 200
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
