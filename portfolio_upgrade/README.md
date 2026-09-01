# Sentinel Portfolio Reference App

This folder contains a complete, reviewable phishing-risk demonstration prepared for Nitya Roshini Kandula's portfolio.

## What it demonstrates

- FastAPI request validation and typed responses
- Explainable URL and email heuristics
- A responsive, accessibility-aware web interface
- No server-side URL fetching, which avoids turning the demo into an SSRF surface
- Automated API tests
- Explicit limitations and production hardening notes

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn httpx pytest
uvicorn portfolio_upgrade.app:app --reload
```

Open `http://127.0.0.1:8000/portfolio`.

## Test

```bash
pytest -q portfolio_upgrade/tests
```

## Security boundary

This is an educational decision-support demo. A low risk score does not prove a link or message is safe. A production system would require current reputation data, model evaluation, drift monitoring, rate limiting, privacy controls, observability, and independent security review.
