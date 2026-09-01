from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import ipaddress
import re
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, model_validator

BASE_DIR = Path(__file__).resolve().parent
SUSPICIOUS_TERMS = {"login", "verify", "password", "account", "secure", "wallet", "invoice", "payment", "update", "unlock", "confirm"}
URGENCY_TERMS = ("act now", "immediately", "within 24 hours", "urgent", "final warning", "suspended")
CREDENTIAL_TERMS = ("confirm your password", "verify your account", "enter your credentials", "sign in to continue")


@dataclass(frozen=True)
class Signal:
    label: str
    weight: int
    evidence: str


class AnalyzeRequest(BaseModel):
    url: str = Field(default="", max_length=2048)
    email_text: str = Field(default="", max_length=20_000)

    @model_validator(mode="after")
    def require_input(self) -> "AnalyzeRequest":
        if not self.url.strip() and not self.email_text.strip():
            raise ValueError("Provide a URL, message, or both.")
        return self


app = FastAPI(title="Sentinel Portfolio API", version="1.0.0")


def analyze_url(raw: str) -> list[Signal]:
    if not raw.strip():
        return []
    submitted = raw.strip()
    parsed = urlparse(submitted if "://" in submitted else f"https://{submitted}")
    host = (parsed.hostname or "").lower()
    combined = parsed.geturl().lower()
    signals: list[Signal] = []
    if not host:
        return [Signal("Invalid URL structure", 100, "No valid hostname was found.")]
    try:
        ipaddress.ip_address(host)
        signals.append(Signal("IP address used as host", 30, host))
    except ValueError:
        pass
    if parsed.scheme == "http":
        signals.append(Signal("Unencrypted HTTP", 18, "The destination does not request HTTPS."))
    if "@" in submitted:
        signals.append(Signal("@ character in URL", 24, "Text before @ can obscure the destination."))
    if host.startswith("xn--") or ".xn--" in host:
        signals.append(Signal("Punycode hostname", 22, "Internationalized encoding can be used for lookalikes."))
    if len(host.split(".")) > 4:
        signals.append(Signal("Many subdomains", 16, host))
    words = sorted(term for term in SUSPICIOUS_TERMS if term in combined)
    if words:
        signals.append(Signal("Credential or payment wording", min(28, 10 + 4 * len(words)), ", ".join(words[:5])))
    if len(submitted) > 120:
        signals.append(Signal("Unusually long URL", 14, f"{len(submitted)} characters"))
    return signals


def analyze_email(text: str) -> list[Signal]:
    lowered = text.lower()
    signals: list[Signal] = []
    urgency = [term for term in URGENCY_TERMS if term in lowered]
    credentials = [term for term in CREDENTIAL_TERMS if term in lowered]
    if urgency:
        signals.append(Signal("Urgency or threat language", min(26, 12 + 5 * len(urgency)), ", ".join(urgency[:3])))
    if credentials:
        signals.append(Signal("Credential request", min(30, 18 + 4 * len(credentials)), ", ".join(credentials[:3])))
    if re.search(r"\b(gift card|wire transfer|crypto|bitcoin|routing number)\b", lowered):
        signals.append(Signal("High-risk payment request", 28, "Irreversible-payment wording detected."))
    return signals


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest) -> dict[str, object]:
    signals = analyze_url(request.url) + analyze_email(request.email_text)
    score = max(0, min(100, sum(signal.weight for signal in signals)))
    label = "high risk" if score >= 65 else "review" if score >= 30 else "low risk"
    recommendation = {
        "high risk": "Do not enter credentials. Verify the sender or domain through a trusted channel.",
        "review": "Pause and verify the destination independently before continuing.",
        "low risk": "No major heuristic indicators were found; continue with normal caution.",
    }[label]
    return {
        "score": score,
        "label": label,
        "signals": [asdict(signal) for signal in signals],
        "recommendation": recommendation,
        "disclaimer": "Decision-support demo; a low score does not prove safety.",
    }


@app.get("/portfolio", include_in_schema=False)
def portfolio() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")
