"""email 摘要（market_read_summary.py）開頭換成 home_card 四層：結論、證據、動能、儀表。"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location("market_read_summary", ROOT / "scripts" / "market_read_summary.py")
summary = importlib.util.module_from_spec(spec)
sys.modules["market_read_summary"] = summary
spec.loader.exec_module(summary)


def _card():
    item = lambda label, tk, change=None: {"label": label, "ticker": tk, "streak_days": 3, "change": change}
    return {
        "schema": "market-home-card-v1", "headline": "測試結論一句。", "headline_source": "thesis_zh",
        "read_as_of": "2026-10-26", "read_expired": False, "data_as_of": "2026-10-27",
        "groups": [{"claim": "信用利差續寬", "source": "forces", "lines": [
            {"ref": "monitor:hy_oas", "label": "高收益債利差", "value_text": "3.38%",
             "position_text": "高於近一年 99% 的交易日", "as_of": "2026-10-23", "read_value_text": "3.30%"}]}],
        "momentum": {"as_of": "2026-10-26", "note": "動能說明一行。", "cells": {
            "strong_up": {"title": "強且變強", "items": [item("大宗", "DBC", {"text": "x", "status": "near"})]},
            "strong_down": {"title": "強但轉弱", "items": [item("標普500", "SPY", {"text": "y", "status": "confirmed"})]},
            "weak_up": {"title": "弱但轉強", "items": []},
            "weak_down": {"title": "弱且變弱", "items": [item("黃金", "GLD")]}}},
        "gauges": {"now": [{"key": "stress", "name": "跨資產壓力", "value_text": "66.8", "label": "緊張", "note": "壓力說明。"}],
                   "next_month": [{"key": "vol_up_21d", "name": "一個月內波動變大的機率", "value_text": "65%",
                                   "label": "高於平常", "note": "波動說明。"}]},
    }


READ = {"mode": "commentary", "as_of": "2026-10-27", "thesis_zh": "舊主張。", "path_zh": "舊路徑。",
        "horizons": [], "forces": [], "falsifiers": []}


def test_html_has_four_layers_and_drops_one_minute():
    html = summary.build_html_success(READ, {"home_card": _card()})
    for needle in ("測試結論一句。", "資料 10-27 · 判讀 10-26", "信用利差續寬", "高收益債利差", "判讀時 3.30%",
                   "資產動能", "強且變強", "大宗 DBC（未站穩）", "標普500 SPY（已確認）", "黃金 GLD", "動能說明一行。",
                   "動能到 10-26", "現在", "接下來一個月", "跨資產壓力", "波動說明。"):
        assert needle in html, needle
    assert "一分鐘版" not in html


def test_text_has_four_layers():
    subject, body = summary.build_success(READ, {"home_card": _card()})
    for needle in ("【結論】", "【證據】", "【資產動能】（動能到 10-26）", "【儀表・現在】", "【儀表・接下來一個月】",
                   "強但轉弱：標普500 SPY（已確認）", "弱但轉強：—"):
        assert needle in body, needle
    assert "【主張】" not in body


def test_missing_home_card_falls_back_to_one_minute_summary():
    html = summary.build_html_success(READ, {})
    assert "一分鐘版" in html and "資產動能" not in html
    _, body = summary.build_success(READ, None)
    assert "【主張】" in body and "【結論】" not in body
