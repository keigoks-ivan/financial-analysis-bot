"""讀 catalog：catalog/<區>.json，加上它 "parts" 列出的分檔 catalog/<區>_<分檔>.json。

分檔用在一區底下有好幾個國家的情況（東南亞）：每國一個檔，各自有 group（國名）與自己的大類。
分檔的大類依 parts 順序接在主檔大類後面，大類沒寫 group 就用分檔的 group；todo、unavailable 也併進來。
"""
from __future__ import annotations

import json
from pathlib import Path

CATALOG_DIR = Path(__file__).resolve().parent / "catalog"


def load_catalog(country, catalog_dir=None):
    d = Path(catalog_dir or CATALOG_DIR)
    p = d / (country + ".json")
    if not p.exists():
        return None
    cat = json.loads(p.read_text(encoding="utf-8"))
    for part in cat.get("parts", []):
        pp = d / f"{country}_{part}.json"
        if not pp.exists():
            continue
        sub = json.loads(pp.read_text(encoding="utf-8"))
        for k in sub.get("categories", []):
            k.setdefault("group", sub["group"])
            k["part"] = part
            cat["categories"].append(k)
        for key in ("todo", "unavailable"):
            for rec in sub.get(key, []):
                cat.setdefault(key, []).append(dict(rec, part=part))
    return cat
