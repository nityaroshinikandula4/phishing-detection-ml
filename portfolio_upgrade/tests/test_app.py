from fastapi.testclient import TestClient

from portfolio_upgrade.app import app

client = TestClient(app)


def test_health() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_requires_url_or_message() -> None:
    response = client.post('/api/analyze', json={'url': '', 'email_text': ''})
    assert response.status_code == 422


def test_suspicious_input_returns_explanation() -> None:
    response = client.post(
        '/api/analyze',
        json={
            'url': 'http://192.0.2.40/verify-password',
            'email_text': 'URGENT: verify your account and enter your credentials immediately',
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload['score'] >= 65
    assert payload['label'] == 'high risk'
    assert payload['signals']
    assert 'Decision-support' in payload['disclaimer']
