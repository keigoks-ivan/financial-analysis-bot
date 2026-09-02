#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""market_read_summary.py — 把 `docs/market/data/read.json`（或失敗時的
`docs/market/data/read_status.json`）收斂成一封純文字 email 摘要。

供 `.github/workflows/market-read-notify.yml` 消費：本檔第一行印主旨，
第二行空白，之後印信文；`dawidd6/action-send-mail@v3` 直接把這兩段塞進
subject／body。設計稿：
`notes/site-internal/root/_market_read_design_20260903.md` §5.5。

判斷邏輯：先看 `--status-file`（預設 `docs/market/data/read_status.json`）；
若存在且 status=="failed"，印失敗摘要（不讀 read.json）。否則讀
`--file`（預設 `docs/market/data/read.json`）印成功摘要。任何檔案缺失／
欄位缺失一律降級印「（無資料）」等說明字串，絕不 crash；exit code 恆為 0
（email 一定要寄得出去，摘要腳本本身不應該擋 workflow）。

用法
----
  python scripts/market_read_summary.py
  python scripts/market_read_summary.py --file docs/market/data/read.json \\
      --status-file docs/market/data/read_status.json \\
      --state docs/market/data/state.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = ROOT / "docs" / "market" / "data" / "read.json"
DEFAULT_STATUS_FILE = ROOT / "docs" / "market" / "data" / "read_status.json"
DEFAULT_STATE_FILE = ROOT / "docs" / "market" / "data" / "state.json"
PAGE_URL = "https://research.investmquest.com/market/"


def load_json(path: Path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def fmt_pct(x):
    if not isinstance(x, (int, float)):
        return "—"
    return f"{x * 100:.0f}%" if abs(x) <= 1 else f"{x:.1f}%"


def fmt_pct1(x):
    if not isinstance(x, (int, float)):
        return "—"
    return f"{x * 100:.1f}%" if abs(x) <= 1 else f"{x:.1f}%"


# ═══════════════════════════════════════════════════════════════════════════
# 失敗摘要
# ═══════════════════════════════════════════════════════════════════════════

def build_failure(status: dict):
    as_of = status.get("as_of", "?")
    stage = status.get("stage", "?")
    reasons = status.get("reasons") or []

    subject = f"市況判讀失敗 {as_of}｜{stage}"

    lines = []
    lines.append(f"本次市況判讀在「{stage}」關卡失敗，read.json 未變更、判讀未落帳。")
    lines.append("")
    if reasons:
        lines.append("失敗原因：")
        for r in reasons:
            lines.append(f"　－{r}")
    else:
        lines.append("失敗原因：（未提供）")
    lines.append("")
    lines.append("routine 明天會依觸發條件自動重試，或手動跑 market-read skill 補上。")
    lines.append("")
    lines.append(f"連結：{PAGE_URL}")
    body = "\n".join(lines)
    return subject, body


# ═══════════════════════════════════════════════════════════════════════════
# 成功摘要
# ═══════════════════════════════════════════════════════════════════════════

def build_horizons_lines(horizons):
    lines = []
    if not isinstance(horizons, list):
        return ["　（無三框架資料）"]
    for h in horizons:
        label = h.get("label", h.get("key", "?"))
        p_up = fmt_pct(h.get("p_up"))
        p_clim_up = fmt_pct1(h.get("p_clim_up"))
        parts = [f"收高機率 {p_up}（基準 {p_clim_up}）"]
        p_dd = h.get("p_dd10") if h.get("p_dd10") is not None else h.get("p_dd20")
        if p_dd is not None:
            dd_label = "回撤 10%" if h.get("p_dd10") is not None else "回撤 20%"
            p_clim_dd = fmt_pct1(h.get("p_clim_dd"))
            parts.append(f"{dd_label} 機率 {fmt_pct(p_dd)}（基準 {p_clim_dd}）")
        lines.append(f"　－{label}：{'；'.join(parts)}")
    return lines or ["　（無三框架資料）"]


def build_forces_lines(forces):
    if not isinstance(forces, list) or not forces:
        return ["　（無三股力量資料）"]
    return [f"　－{f.get('title', '?')}" for f in forces]


def lookup_quote_value(state_data, ref, field="num"):
    if not isinstance(state_data, dict):
        return None
    quotes = ((state_data.get("evidence") or {}).get("quotes") or {})
    q = quotes.get(ref)
    if not isinstance(q, dict):
        return None
    return q.get(field)


def compute_distance_pct(current, threshold, op):
    if not isinstance(current, (int, float)) or not isinstance(threshold, (int, float)) or threshold == 0:
        return None
    if op in (">", ">="):
        return round((threshold - current) / abs(threshold) * 100, 1)
    return round((current - threshold) / abs(threshold) * 100, 1)


def build_falsifiers_lines(falsifiers, state_data):
    if not isinstance(falsifiers, list) or not falsifiers:
        return ["　（無證偽表資料）"]
    lines = []
    for f in falsifiers[:5]:
        label = f.get("label", "?")
        ref = f.get("ref")
        field = f.get("field", "num")
        threshold = f.get("threshold")
        unit = f.get("unit", "")
        op = f.get("op", "")
        current = lookup_quote_value(state_data, ref, field)
        if current is None:
            cur_str = "現值—"
        else:
            cur_str = f"現值 {current}{unit}"
        dist = compute_distance_pct(current, threshold, op)
        dist_str = f"，距離 {dist}%" if dist is not None else ""
        lines.append(f"　－[{f.get('direction', '?')}] {label}：{cur_str} → 門檻 {threshold}{unit}{dist_str}")
    return lines


def build_deviations_summary(deviations):
    if not isinstance(deviations, list) or not deviations:
        return "　（本次判讀與帳簿表格無申報分歧）"
    biggest = max(deviations, key=lambda d: abs((d.get("my_p") or 0) - (d.get("table_p") or 0)))
    diff = abs((biggest.get("my_p") or 0) - (biggest.get("table_p") or 0))
    return (f"　共 {len(deviations)} 條分歧；最大一條：{biggest.get('claim', '?')}"
            f"（表格 p={biggest.get('table_p')}，判讀 p={biggest.get('my_p')}，差 {diff:.2f}）")


def build_review_summary(review):
    if not isinstance(review, dict) or not review:
        return "　（本次判讀尚未經自動化冷讀 gate，或為 manual 模式產出）"
    model = review.get("model", "?")
    rnd = review.get("round", "?")
    verdict = review.get("verdict", "?")
    findings = review.get("findings") or []
    n_yellow = sum(1 for f in findings if isinstance(f, dict) and f.get("severity") == "🟡")
    return f"　冷讀模型 {model}／第 {rnd} 輪／verdict={verdict}／剩餘 🟡 {n_yellow} 條"


def build_success(data: dict, state_data):
    as_of = data.get("as_of", "?")
    thesis = data.get("thesis_zh", "") or ""
    subject = f"市況判讀 {as_of}｜{thesis[:28]}…"

    lines = []
    lines.append("【主張】")
    lines.append(thesis or "（無）")
    lines.append("")
    lines.append("【路徑】")
    lines.append(data.get("path_zh") or "（無）")
    lines.append("")
    lines.append("【三個時間框架】")
    lines.extend(build_horizons_lines(data.get("horizons")))
    lines.append("")
    lines.append("【三股力量】")
    lines.extend(build_forces_lines(data.get("forces")))
    lines.append("")
    lines.append("【證偽表（前 5 條）】")
    lines.extend(build_falsifiers_lines(data.get("falsifiers"), state_data))
    lines.append("")
    lines.append("【與帳簿表格的分歧】")
    lines.append(build_deviations_summary(data.get("deviations_from_tables")))
    lines.append("")
    lines.append("【冷讀結果】")
    lines.append(build_review_summary(data.get("review")))
    lines.append("")
    claim_ids = data.get("claim_ids") or []
    lines.append(f"【落帳編號】{claim_ids if claim_ids else '（無）'}")
    lines.append("")
    lines.append(f"連結：{PAGE_URL}")
    body = "\n".join(lines)
    return subject, body


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=str(DEFAULT_FILE), help="read.json 路徑（預設 %(default)s）")
    ap.add_argument("--status-file", default=str(DEFAULT_STATUS_FILE), help="read_status.json 路徑（預設 %(default)s）")
    ap.add_argument("--state", default=str(DEFAULT_STATE_FILE), help="state.json 路徑（供證偽表現值查詢，預設 %(default)s）")
    args = ap.parse_args()

    try:
        status_data = load_json(Path(args.status_file))
        if isinstance(status_data, dict) and status_data.get("status") == "failed":
            subject, body = build_failure(status_data)
        else:
            read_data = load_json(Path(args.file))
            if not isinstance(read_data, dict):
                subject = "市況判讀摘要產生失敗｜read.json 不可讀"
                body = f"找不到或無法解析 {args.file}，且 {args.status_file} 未標記失敗狀態。\n\n連結：{PAGE_URL}"
            else:
                state_data = load_json(Path(args.state))
                subject, body = build_success(read_data, state_data)
    except Exception as e:  # noqa: BLE001 — 摘要腳本絕不能讓 workflow 因未預期例外而卡住
        subject = "市況判讀摘要產生時發生未預期錯誤"
        body = f"market_read_summary.py 拋出例外：{e!r}\n\n連結：{PAGE_URL}"

    print(subject)
    print()
    print(body)
    sys.exit(0)


if __name__ == "__main__":
    main()
