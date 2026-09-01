from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .features import analyze_message, analyze_url
from .schemas import AnalyzeRequest, AnalyzeResponse, SignalResponse
from .scoring import combine_signals, recommended_actions

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Sentinel Phishing Analysis API",
    version="1.0.0",
    description="Explainable URL and email risk signals for a portfolio reference implementation.",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "sentinel"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    if not payload.url and not payload.email_text:
        raise HTTPException(status_code=422, detail="Provide a URL, an email message, or both.")

    url_signals, url_metrics = analyze_url(payload.url)
    message_signals, message_metrics = analyze_message(payload.email_text)
    score, label, signals = combine_signals(url_signals, message_signals)

    metrics = {f"url_{key}": value for key, value in url_metrics.items()}
    metrics.update({f"message_{key}": value for key, value in message_metrics.items()})
    return AnalyzeResponse(
        score=score,
        label=label,
        signals=[SignalResponse(**signal.__dict__) for signal in signals],
        actions=recommended_actions(label),
        metrics=metrics,
        disclaimer=(
            "Educational baseline only. A low score never guarantees safety, and this service does not open, "
            "resolve, or fetch submitted URLs."
        ),
    )


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
