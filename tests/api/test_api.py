from fastapi.testclient import TestClient
from app import app
client = TestClient(app=app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 404
    