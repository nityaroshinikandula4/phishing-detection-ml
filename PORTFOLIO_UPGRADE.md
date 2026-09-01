# Sentinel — Recruiter-Facing Project Overview

Sentinel is an explainable phishing-risk reference application designed to show an end-to-end security workflow rather than only a model notebook. It combines a FastAPI service, URL and email feature extraction, transparent risk reasons, a responsive browser dashboard, and a Manifest V3 extension prototype.

## Engineering highlights

- Validated REST request and response contracts
- Lexical URL signals such as raw-IP hosts, suspicious subdomain depth, look-alike patterns, and credential-oriented paths
- Email signals for urgency, credential requests, embedded forms, and suspicious links
- Human-readable risk reasons and recommended actions
- Optional Scikit-learn training workflow with a clearly labeled demonstration dataset
- Browser-extension flow that evaluates the active tab against a locally controlled API
- Automated feature and API tests in the complete project package

## Architecture

```text
Dashboard / browser extension
             |
             v
       FastAPI endpoint
             |
             v
 URL + email feature extraction
             |
      +------+------+
      |             |
      v             v
Explainable      Optional trained
baseline score   classifier
      |             |
      +------+------+
             v
 Score + label + reasons + actions
```

## Responsible use

This repository is a portfolio reference implementation, not a replacement for a managed email-security platform or a production threat-intelligence program. The detector can produce false positives and false negatives. A production version would need current licensed datasets, calibration, drift monitoring, reputation feeds, privacy controls, authentication, rate limits, observability, and an analyst feedback loop.

## Recommended repository topics

`python` · `fastapi` · `machine-learning` · `phishing-detection` · `cybersecurity` · `browser-extension` · `explainable-ai`
