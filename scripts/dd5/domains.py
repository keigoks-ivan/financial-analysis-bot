#!/usr/bin/env python3
"""dd5 引用來源網域清單（source_domains.json）的讀取與比對。lint 與精簡版提示詞共用，清單只維護一處。"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

PATH = Path(__file__).resolve().parent / "source_domains.json"
RE_LINK = re.compile(r"\[([^\]\n]*)\]\((https?://[^)\s]+)\)")


def load():
    return json.loads(PATH.read_text(encoding="utf-8"))


def low_quality():
    return list(load().get("low_quality", []))


def match(url, entries):
    """url 命中 entries 裡哪一條就回傳該條，沒命中回傳 None。條目 'host' 或 'host/path前綴'；host 含子網域。"""
    u = urlparse(url)
    host = (u.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = u.path or "/"
    for e in entries:
        e_host, _, e_path = e.lower().partition("/")
        if host == e_host or host.endswith("." + e_host):
            if not e_path or path.lower().lstrip("/").startswith(e_path):
                return e
    return None


def prompt_line():
    lq = low_quality()
    return "以下網域是整理站或低品質來源，不要引用（搜到也不要放進報告連結）：" + "、".join(lq) + "。" if lq else ""
