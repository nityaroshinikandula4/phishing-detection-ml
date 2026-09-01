from __future__ import annotations

import csv
from pathlib import Path

import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from app.features import analyze_url

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "sample_urls.csv"
OUTPUT = ROOT / "models" / "url_model.joblib"


def row_features(url: str) -> dict[str, float]:
    signals, metrics = analyze_url(url)
    features = dict(metrics)
    for signal in signals:
        features[f"signal_{signal.key}"] = 1.0
    return features


def main() -> None:
    rows: list[dict[str, str]] = []
    with DATASET.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    x = [row_features(row["url"]) for row in rows]
    y = [int(row["label"]) for row in rows]
    model = Pipeline([
        ("vectorizer", DictVectorizer(sparse=True)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])
    model.fit(x, y)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, OUTPUT)
    print(f"Saved demonstration model to {OUTPUT}")
    print("This tiny dataset validates the pipeline only; it is not suitable for security decisions.")


if __name__ == "__main__":
    main()
