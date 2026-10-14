from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app


client = TestClient(app)


def teardown_function() -> None:
    get_settings.cache_clear()


def test_health_returns_service_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "clauseiq-api",
        "version": "0.1.0",
        "environment": "development",
    }


def test_health_uses_environment_version(monkeypatch) -> None:
    monkeypatch.setenv("APP_VERSION", "0.1.0-test")
    get_settings.cache_clear()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["version"] == "0.1.0-test"


def test_unknown_route_returns_not_found() -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404