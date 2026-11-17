import os
os.environ["DATABASE_URL"] = "sqlite://"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_chat_returns_reply_and_persists():
    response = client.post("/api/chat", json={"message": "Where can I get help?"})
    assert response.status_code == 200
    body = response.json()
    assert body["conversation_id"] > 0
    assert body["reply"]
    assert body["mode"] in {"demo", "openai", "unavailable"}

def test_chat_rejects_blank_message():
    response = client.post("/api/chat", json={"message": "   "})
    assert response.status_code == 422
