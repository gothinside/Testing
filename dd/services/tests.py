import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..database import Base
from ..crud import create_service, get_services, update_service, delete_service
from ..schemas import ServiceCreate, ServiceUpdate
from ..models import Service

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_create_service(client, db_session):
    response = client.post("/services/", json={"name": "Test Service", "description": "Test Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Service"
    assert data["description"] == "Test Description"

def test_read_services(client, db_session):
    response = client.get("/services/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_update_service(client, db_session):
    service_id = db_session.query(Service).first().service_id
    response = client.patch(f"/services/{service_id}", json={"name": "Updated Service"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Service"

def test_delete_service(client, db_session):
    service_id = db_session.query(Service).first().service_id
    response = client.delete(f"/services/{service_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Service deleted successfully"
