from __future__ import annotations

from collections import OrderedDict

from .features import Signal


def combine_signals(url_signals: list[Signal], message_signals: list[Signal]) -> tuple[int, str, list[Signal]]:
    unique: OrderedDict[str, Signal] = OrderedDict()
    for signal in [*url_signals, *message_signals]:
        current = unique.get(signal.key)
        if current is None or signal.weight > current.weight:
            unique[signal.key] = signal

    signals = sorted(unique.values(), key=lambda item: item.weight, reverse=True)
    raw_score = sum(item.weight for item in signals)
    # A saturating curve prevents an arbitrary number of weak signals from exceeding 100 too quickly.
    score = round(100 * (1 - (0.985 ** raw_score))) if raw_score else 0
    score = max(0, min(100, score))

    if score >= 70:
        label = "high"
    elif score >= 40:
        label = "medium"
    elif score >= 15:
        label = "low"
    else:
        label = "minimal"
    return score, label, signals


def recommended_actions(label: str) -> list[str]:
    actions = [
        "Verify the sender and destination through a separate trusted channel.",
        "Inspect the registrable domain before opening the link.",
    ]
    if label in {"medium", "high"}:
        actions.extend([
            "Do not enter credentials or payment information from this message.",
            "Report the message to the relevant security or support team.",
        ])
    if label == "high":
        actions.append("Quarantine the message or close the page until it has been reviewed.")
    return actions
