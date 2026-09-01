from app.features import analyze_message, analyze_url
from app.scoring import combine_signals


def test_ip_and_http_are_explained() -> None:
    signals, metrics = analyze_url("http://192.0.2.50/login")
    keys = {signal.key for signal in signals}
    assert {"ip_host", "not_https"}.issubset(keys)
    assert metrics["url_length"] > 0


def test_message_credential_and_urgency_signals() -> None:
    signals, _ = analyze_message("URGENT: verify your password immediately")
    keys = {signal.key for signal in signals}
    assert "urgency" in keys
    assert "credentials" in keys


def test_score_is_bounded() -> None:
    url_signals, _ = analyze_url("http://192.0.2.1/login?x=" + "a" * 200)
    message_signals, _ = analyze_message("URGENT password wire transfer! ! ! !")
    score, label, signals = combine_signals(url_signals, message_signals)
    assert 0 <= score <= 100
    assert label in {"minimal", "low", "medium", "high"}
    assert signals
