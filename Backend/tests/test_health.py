from fastapi.testclient import TestClient

from Backend.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ok"
    assert body["app"] == "FixProof AI"
    assert body["version"] == "1.0.0"


def test_unknown_route_returns_404():
    response = client.get("/route-that-does-not-exist")

    assert response.status_code == 404
