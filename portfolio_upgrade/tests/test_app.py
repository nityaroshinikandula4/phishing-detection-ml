from fastapi.testclient import TestClient
from portfolio_upgrade.app import app

client=TestClient(app)

def test_health():
    assert client.get('/health').json()=={'status':'ok'}

def test_requires_input():
    assert client.post('/api/analyze',json={'url':'','email_text':''}).status_code==422

def test_explainable_high_risk_result():
    response=client.post('/api/analyze',json={'url':'http://192.0.2.4/verify-password','email_text':'URGENT: verify your account and enter credentials immediately'})
    assert response.status_code==200
    result=response.json()
    assert result['score']>=65
    assert result['signals']
