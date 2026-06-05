"""tests/test_app.py — Automated tests run by the CI pipeline."""
import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """Root should return 200 with service name."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["service"] == "cicd-demo"
    assert "python" in data


def test_health_endpoint(client):
    """Health check must return 200 and status=healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_add_two_numbers(client):
    """POST /add should correctly add a and b."""
    response = client.post(
        "/add",
        json={"a": 3, "b": 4},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.get_json()["result"] == 7


def test_add_missing_fields(client):
    """POST /add with missing fields should return 400."""
    response = client.post("/add", json={"a": 5}, content_type="application/json")
    assert response.status_code == 400


def test_add_floats(client):
    """POST /add should also work with floats."""
    response = client.post(
        "/add",
        json={"a": 1.5, "b": 2.5},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.get_json()["result"] == pytest.approx(4.0)
