import os

# Set before importing the app. Real env values are overwritten on purpose, so
# tests can never reach the real database, LiveScore or Firebase.
# load_dotenv() does not override variables that are already set.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["LIVESCORE_API_KEY"] = "test"
os.environ["LIVESCORE_API_SECRET"] = "test"
os.environ["FIREBASE_CREDENTIALS_PATH"] = "does-not-exist.json"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.services.auth import get_current_user

TEST_USER = {"uid": "test-user", "email": "test@example.com"}


@pytest.fixture
def db():
    # Fresh in-memory SQLite database per test. StaticPool keeps one shared
    # connection, otherwise each connection would get its own empty database.
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture
def client(db):
    # Unauthenticated client. Routes get the test database instead of the real one.
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def auth_client(client):
    # Same client, but every request is treated as coming from TEST_USER.
    app.dependency_overrides[get_current_user] = lambda: TEST_USER
    return client
