#!/usr/bin/env python3
"""Shared helpers for the Jev evidence layer (scripts/jev/, data/jev/).

Stdlib only, matching the rest of scripts/jev/ (probe.py). Nothing here
touches stock-dash, moat_pipeline.py, or any file outside scripts/jev/ and
data/jev/.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

JEV_DIR = Path(__file__).resolve().parent
ROOT = JEV_DIR.parent.parent
DATA_DIR = ROOT / "data" / "jev"

# EDGAR requires a descriptive contact per its fair-access policy; also sent
# to Google News / the newsroom RSS as a polite, identifiable UA.
USER_AGENT = "financial-analysis-bot research keigoks@gmail.com"
HTTP_TIMEOUT = 15
HTTP_RETRIES = 2

# Rough, conservative estimate (~4 chars/token for English text). Jev does
# not expose a tokenizer to callers; this is only used to decide when to
# split a request across multiple calls, never for billing.
CHARS_PER_TOKEN = 4


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def today_str():
    return datetime.now(timezone.utc).date().isoformat()


def load_json(path, default=None):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(value, ensure_ascii=False, indent=1, sort_keys=False) + "\n"
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=str(path.parent), delete=False) as f:
        f.write(body)
        tmp = f.name
    os.replace(tmp, path)


def append_jsonl(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def sha_id(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def get_api_key():
    key = os.environ.get("TYPESAFE_API_KEY")
    if key:
        return key
    kf = Path.home() / ".config" / "typesafe" / "api_key"
    return kf.read_text().strip() if kf.exists() else None


_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def strip_html(text):
    """Strip tags, unescape entities, collapse whitespace. Used on
    yfinance's HTML `description` and RSS `description` fields."""
    if not text:
        return ""
    text = _TAG_RE.sub(" ", text)
    text = html.unescape(text)
    return _WS_RE.sub(" ", text).strip()


def normalize_headline(headline):
    text = (headline or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return _WS_RE.sub(" ", text).strip()


def rfc822_to_iso(value):
    if not value:
        return ""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError):
        return value


def http_get(url, headers=None, allowed_hosts=None, timeout=HTTP_TIMEOUT, retries=HTTP_RETRIES):
    """GET with a descriptive User-Agent, timeout, and a couple of retries.
    Raises on failure; callers decide whether a failing source aborts the
    whole run (it should not — see fetch_evidence.collect_raw)."""
    host = urllib.parse.urlparse(url).hostname
    if allowed_hosts and host not in allowed_hosts:
        raise ValueError(f"host not in allowlist: {host}")
    req_headers = {"User-Agent": USER_AGENT}
    req_headers.update(headers or {})
    req = urllib.request.Request(url, headers=req_headers)
    last_err = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", errors="replace")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
            last_err = exc
            if attempt < retries:
                time.sleep(min(2 ** attempt, 4))
    raise last_err


_CJK_RE = re.compile(r"[一-鿿㐀-䶿豈-﫿]")


def has_cjk(value):
    """True if any CJK character appears anywhere in a JSON-serializable
    value. Used by tests to assert nothing Chinese is ever sent to Jev."""
    return bool(_CJK_RE.search(json.dumps(value, ensure_ascii=False)))


def estimate_tokens(obj):
    return len(json.dumps(obj, ensure_ascii=False)) // CHARS_PER_TOKEN


def chunk_indices_by_budget(costs, budget_tokens):
    """Greedily pack item indices [0, len(costs)) into chunks whose summed
    cost stays under budget_tokens. A single item whose own cost already
    exceeds the budget still gets its own (over-budget) chunk — there is
    nothing smaller to fall back to, so the caller sends it anyway and
    Jev's own 422 is the backstop.

    Pure function so it is directly unit-testable without a real request.
    """
    chunks, current, total = [], [], 0
    for i, c in enumerate(costs):
        if current and total + c > budget_tokens:
            chunks.append(current)
            current, total = [], 0
        current.append(i)
        total += c
    if current:
        chunks.append(current)
    return chunks
