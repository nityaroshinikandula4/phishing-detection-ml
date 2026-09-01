from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_requires_input() -> None:
    response = client.post("/api/analyze", json={"url": "", "email_text": ""})
    assert response.status_code == 422


def test_analyze_returns_explanations() -> None:
    response = client.post(
        "/api/analyze",
        json={"url": "http://secure-account-verify.example.test/login", "email_text": "Verify your password immediately"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["score"] > 0
    assert payload["signals"]
    assert "does not open" in payload["disclaimer"]
