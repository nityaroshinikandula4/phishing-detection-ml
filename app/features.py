from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass
from urllib.parse import urlparse

URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "ow.ly", "is.gd", "buff.ly", "rebrand.ly"
}
URGENCY_TERMS = {
    "urgent", "immediately", "final warning", "act now", "suspended", "expires today",
    "within 24 hours", "verify now", "limited time"
}
CREDENTIAL_TERMS = {
    "password", "passcode", "login", "sign in", "verify your account", "security question",
    "one-time code", "otp", "credential"
}
PAYMENT_TERMS = {
    "wire transfer", "gift card", "bank account", "payment failed", "invoice attached",
    "refund", "cryptocurrency", "wallet"
}


@dataclass(frozen=True)
class Signal:
    key: str
    label: str
    weight: int
    detail: str


def normalize_url(raw_url: str) -> str:
    value = raw_url.strip()
    if value and "://" not in value:
        value = f"https://{value}"
    return value


def _is_ip(hostname: str) -> bool:
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def analyze_url(raw_url: str) -> tuple[list[Signal], dict[str, float]]:
    normalized = normalize_url(raw_url)
    if not normalized:
        return [], {}

    parsed = urlparse(normalized)
    hostname = (parsed.hostname or "").lower().rstrip(".")
    path_and_query = f"{parsed.path}?{parsed.query}" if parsed.query else parsed.path
    labels = [part for part in hostname.split(".") if part]

    metrics: dict[str, float] = {
        "url_length": float(len(normalized)),
        "hostname_length": float(len(hostname)),
        "subdomain_depth": float(max(0, len(labels) - 2)),
        "digit_ratio": sum(ch.isdigit() for ch in normalized) / max(1, len(normalized)),
        "hyphen_count": float(hostname.count("-")),
        "path_depth": float(len([segment for segment in parsed.path.split("/") if segment])),
    }

    signals: list[Signal] = []
    if _is_ip(hostname):
        signals.append(Signal("ip_host", "Raw IP address used as host", 22, "Legitimate services usually present a recognizable domain name."))
    if parsed.scheme.lower() != "https":
        signals.append(Signal("not_https", "Connection is not HTTPS", 12, "Transport security is absent or unclear."))
    if "@" in normalized:
        signals.append(Signal("at_symbol", "URL contains an @ symbol", 16, "Text before @ can visually distract from the actual destination."))
    if hostname.startswith("xn--") or ".xn--" in hostname:
        signals.append(Signal("punycode", "Internationalized hostname encoding detected", 12, "Punycode can be legitimate, but it merits careful visual review."))
    if hostname in URL_SHORTENERS:
        signals.append(Signal("shortener", "Link-shortening service hides the destination", 14, "Resolve shortened links using a trusted preview tool before visiting."))
    if metrics["subdomain_depth"] >= 3:
        signals.append(Signal("deep_subdomain", "Unusually deep subdomain structure", 12, "Attackers may place a trusted brand name in an unrelated subdomain."))
    if len(normalized) >= 100:
        signals.append(Signal("long_url", "Very long URL", 8, "Long paths and query strings can conceal the meaningful destination."))
    if hostname.count("-") >= 3:
        signals.append(Signal("hyphenated_host", "Heavily hyphenated hostname", 9, "Multiple separators can imitate familiar naming patterns."))
    if re.search(r"(?:login|verify|secure|account|update|signin)", hostname) and len(labels) > 2:
        signals.append(Signal("lookalike_host", "Account-related language in a nested hostname", 17, "Confirm the registrable domain rather than trusting a familiar word."))
    if re.search(r"\.(?:exe|scr|js|zip)(?:$|[?#])", path_and_query, flags=re.IGNORECASE):
        signals.append(Signal("risky_download", "Potential executable or archive download", 18, "Unexpected downloads should be verified through a trusted channel."))
    return signals, metrics


def analyze_message(text: str) -> tuple[list[Signal], dict[str, float]]:
    value = text.strip().lower()
    if not value:
        return [], {}

    urgency_hits = sorted(term for term in URGENCY_TERMS if term in value)
    credential_hits = sorted(term for term in CREDENTIAL_TERMS if term in value)
    payment_hits = sorted(term for term in PAYMENT_TERMS if term in value)
    links = re.findall(r"https?://[^\s<>'\"]+", value)
    exclamation_count = value.count("!")

    signals: list[Signal] = []
    if urgency_hits:
        signals.append(Signal("urgency", "Urgency or pressure language detected", min(20, 8 + 3 * len(urgency_hits)), f"Matched: {', '.join(urgency_hits[:4])}."))
    if credential_hits:
        signals.append(Signal("credentials", "Credential request detected", min(24, 12 + 3 * len(credential_hits)), f"Matched: {', '.join(credential_hits[:4])}."))
    if payment_hits:
        signals.append(Signal("payment", "Payment or transfer language detected", min(20, 10 + 3 * len(payment_hits)), f"Matched: {', '.join(payment_hits[:4])}."))
    if re.search(r"<form\b|<input\b", value):
        signals.append(Signal("embedded_form", "Embedded form markup detected", 16, "Credential forms inside unexpected messages are high-risk."))
    if exclamation_count >= 4:
        signals.append(Signal("excess_punctuation", "Excessive exclamation marks", 5, "High-pressure punctuation can reinforce social-engineering language."))
    if len(links) >= 3:
        signals.append(Signal("many_links", "Message contains several links", 6, "Review each destination and avoid opening links from untrusted messages."))

    metrics = {
        "character_count": float(len(text)),
        "urgency_hits": float(len(urgency_hits)),
        "credential_hits": float(len(credential_hits)),
        "payment_hits": float(len(payment_hits)),
        "link_count": float(len(links)),
    }
    return signals, metrics
