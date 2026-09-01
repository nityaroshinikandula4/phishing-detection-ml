# Portfolio Architecture Notes

## Request path

1. A user submits a URL and optional email text from the dashboard or browser-extension popup.
2. FastAPI validates the payload and normalizes the URL without opening or fetching the submitted destination.
3. Feature extractors produce reviewable lexical and content signals.
4. The baseline scorer combines those signals into a bounded risk score and severity label.
5. When a trained model artifact is available, the service can include model probability while retaining explicit reasons.
6. The API returns a compact result containing the score, label, detected reasons, and practical next steps.

## Design decisions

### Explainability before model complexity

A recruiter or reviewer can understand why a result changed because every major signal is surfaced. This also creates a useful baseline against which a future classifier can be evaluated.

### No automatic URL retrieval

The analysis path does not visit the submitted site. That reduces accidental exposure to malicious content and keeps the demo deterministic.

### Thin interface, clear service boundary

The browser UI and extension call the same API contract. Feature logic remains testable outside the HTTP layer.

### Explicit project status

The included data and model workflow demonstrate engineering structure. They do not claim production detection accuracy.

## Production hardening backlog

- Managed identity and role-aware administrative endpoints
- Per-client rate limiting and abuse controls
- Domain reputation, certificate, and registration-age enrichment
- Dataset provenance and reproducible evaluation reports
- Probability calibration and threshold governance
- Drift, latency, error-rate, and false-positive monitoring
- Retention controls for submitted email content
- Signed extension distribution and a documented privacy policy
