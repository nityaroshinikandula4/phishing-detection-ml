from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl, field_validator


class AnalyzeRequest(BaseModel):
    url: str = Field(default="", max_length=2048)
    email_text: str = Field(default="", max_length=20000)

    @field_validator("url", "email_text")
    @classmethod
    def strip_values(cls, value: str) -> str:
        return value.strip()


class SignalResponse(BaseModel):
    key: str
    label: str
    weight: int
    detail: str


class AnalyzeResponse(BaseModel):
    score: int = Field(ge=0, le=100)
    label: str
    signals: list[SignalResponse]
    actions: list[str]
    metrics: dict[str, float]
    disclaimer: str
