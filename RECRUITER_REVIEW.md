# Recruiter Review Guide

This branch presents the phishing-detection project as an explainable security reference application.

## Fast review

1. Read `portfolio_upgrade/README.md`.
2. Inspect `portfolio_upgrade/app.py` for typed API validation and transparent scoring.
3. Open `/portfolio` after running the app to review the responsive interface.
4. Run `pytest -q portfolio_upgrade/tests`.

## Evidence demonstrated

- Python API development
- Input validation and structured responses
- Security-aware design that does not fetch submitted URLs
- Explainable rules instead of opaque claims
- Responsive UI and automated tests

## Honest boundary

The implementation is a portfolio reference build, not a production phishing-classification service.
