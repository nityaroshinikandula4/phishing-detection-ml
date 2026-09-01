# Security Policy

## Project scope

Sentinel is an educational and portfolio reference implementation. It is not a managed security product and must not be treated as the sole control for deciding whether a message, URL, or attachment is safe.

## Reporting a vulnerability

Please avoid opening a public issue containing exploit details, credentials, private messages, or malicious payloads. Send a concise report to `nityaroshinikandula412@gmail.com` with:

- affected component and version or commit
- steps to reproduce using non-sensitive test data
- expected and observed behavior
- potential impact
- suggested mitigation, when available

## Safe testing

- Use reserved or controlled domains and synthetic email content.
- Do not submit credentials or confidential messages to an untrusted deployment.
- Do not use this project to scan systems without authorization.
- Keep dependencies current and review automated security alerts before deployment.

## Production expectations

A public deployment should add authentication, authorization, TLS, managed secrets, request-size limits, rate limiting, audit logging, dependency scanning, observability, retention controls, and an incident-response process.
