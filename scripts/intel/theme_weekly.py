#!/usr/bin/env python3
"""scripts/intel/theme_weekly.py — Phase 2 Task D：產業主題週摘要。

每週一次（掛在既有週報分支日，見 .github/workflows/intel-2-daily.yml 的
`IS_SUNDAY` 判斷——UTC 週日 22:30 收工 = 台北時間週一 06:30，本來就是既有
週更分支日，不需要另外挑日子），把過去 7 天各主題（scripts/intel/themes.yml）
的卡片標題＋summary_zh 收斂丟給 sonnet 一次呼叫，寫出
docs/intel/data/theme_weekly.json（schema intel-theme-weekly-v1），給
render.py 的「產業」分頁（build_themes_body）在每個主題列下方掛一段週更綜述。

單一 sonnet 呼叫、單一 ledger bucket（"theme_weekly"，見 llm.py
DAILY_CARD_CAPS），跟每日 classify/summarize/deepread 的額度互不影響。

失敗策略：任何一步失敗（讀檔／CLI／解析）都不得讓這支腳本回非 0——這是
「加值」步驟不是關鍵路徑，chain 的其餘段落（intel_run／render）不因這裡
失敗而受影響。唯一例外是寫檔的 OSError，一樣吞掉只印警告。

CLI:
    python3 scripts/intel/theme_weekly.py --date 2026-08-20
    python3 scripts/intel/theme_weekly.py --date 2026-08-20 --dry-run   # 不呼叫 LLM，只印統計
    python3 scripts/intel/theme_weekly.py --date 2026-08-20 --out /tmp/x.json --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from common import DATA_DIR, load_json, load_themes, read_prompt
from llm import Ledger, run_claude

MAX_ITEMS_PER_THEME = 15
LOOKBACK_DAYS = 7
THEME_WEEKLY_SCHEMA = "intel-theme-weekly-v1"


def _today_tpe() -> str:
    return datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")


def _assign_theme(card: dict, themes: list) -> str | None:
    """跟 render.py::assign_theme 同一套邏輯（render.py 刻意不 import
    common.py，故無法共用函式；這裡另帶一份等價實作，兩邊都讀
    themes.yml 的 keywords，行為保證一致）。card.theme 有填（haiku 分類階段
    挑的）就直接用；沒有就退回關鍵字 fallback。"""
    theme = card.get("theme")
    if theme:
        return theme
    hay = (card.get("title") or "").lower()
    tags_themes = " ".join((card.get("tags") or {}).get("themes") or []).lower()
    hay = f"{hay} {tags_themes}"
    for t in themes:
        for kw in t.get("keywords") or []:
            if kw and kw.lower() in hay:
                return t["key"]
    return None


def _date_range(end_date: str, days: int) -> list[str]:
    try:
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return [end_date]
    return [(end - timedelta(days=i)).isoformat() for i in range(days)]


def collect_theme_cards(date: str, themes: list, days: int = LOOKBACK_DAYS) -> dict:
    """回傳 {theme_key: [{"title":…, "summary_zh":…}, …]}（依重要度排序、每
    主題上限 MAX_ITEMS_PER_THEME 則）。只收有 summary_zh 的卡片（title-only
    的 passthrough 卡片對週摘要沒有實質內容可用，略過）；跨日用卡片 id 去重
    （id 本身已含日期／來源雜湊，理論上不會跨日撞號，仍防禦性去重一次）。"""
    by_theme: dict[str, list] = {}
    seen_ids: set = set()
    for d in _date_range(date, days):
        payload = load_json(DATA_DIR / f"{d}.json")
        if not payload:
            continue
        for c in payload.get("cards") or []:
            cid = c.get("id")
            if cid and cid in seen_ids:
                continue
            summary = (c.get("summary_zh") or "").strip()
            if not summary:
                continue
            key = _assign_theme(c, themes)
            if not key:
                continue
            if cid:
                seen_ids.add(cid)
            by_theme.setdefault(key, []).append({
                "title": c.get("title") or "",
                "summary_zh": summary,
                "_importance": c.get("importance", 1),
            })

    out = {}
    for key, items in by_theme.items():
        items.sort(key=lambda x: -x["_importance"])
        trimmed = [{"title": it["title"], "summary_zh": it["summary_zh"]} for it in items[:MAX_ITEMS_PER_THEME]]
        out[key] = trimmed
    return out


_TAG_RE = re.compile(r"<[^>]*>")


def _clean_text(s: str) -> str:
    """防禦性清理：theme_weekly.md 明確要求純文字輸出，但 LLM 偶爾還是會漏
    夾標籤——這裡去掉任何殘留的角括號標籤，並收斂多餘空白，不假設輸出乾淨。"""
    s = _TAG_RE.sub("", s or "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def build_weekly(date: str, themes_payload: dict) -> dict | None:
    """呼叫 sonnet 一次，回傳 {"schema":…, "week_of":…, "themes":{key:text}}
    或 None（LLM 不可用／被額度擋／解析失敗——呼叫端保留舊檔案不覆蓋）。"""
    if not themes_payload:
        return None
    ledger = Ledger()
    system = read_prompt("theme_weekly.md")
    user = json.dumps({"themes": themes_payload}, ensure_ascii=False)
    parsed, usage = run_claude(
        system=system,
        user=user,
        model="sonnet",
        label="theme_weekly",
        ledger=ledger,
        card_count=len(themes_payload),
        ledger_key="theme_weekly",
    )
    if not parsed or not isinstance(parsed, dict):
        print(f"[intel/theme_weekly] LLM call produced no usable result: {usage}", file=sys.stderr)
        return None
    raw_themes = parsed.get("themes")
    if not isinstance(raw_themes, dict):
        return None
    valid_keys = set(themes_payload.keys())
    out_themes = {}
    for k, v in raw_themes.items():
        if k not in valid_keys or not isinstance(v, str):
            continue
        cleaned = _clean_text(v)
        if cleaned:
            out_themes[k] = cleaned
    if not out_themes:
        return None
    return {"schema": THEME_WEEKLY_SCHEMA, "week_of": date, "themes": out_themes}


def write_weekly(out_path: Path, result: dict) -> None:
    """zero-churn 寫入（比照 render.py::update_theme_history／
    write_status_snapshot 慣例）：序列化內容不變就不重寫、不帶
    generated_at。"""
    content = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
    try:
        if out_path.exists() and out_path.read_text(encoding="utf-8") == content:
            print(f"[intel/theme_weekly] {out_path} unchanged, skip write")
            return
    except OSError:
        pass
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"[intel/theme_weekly] wrote {out_path}")
    except OSError as e:
        print(f"[intel/theme_weekly] WARNING: could not write {out_path}: {e!r}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="YYYY-MM-DD, default = today TPE")
    ap.add_argument("--days", type=int, default=LOOKBACK_DAYS, help="lookback window (default 7)")
    ap.add_argument("--out", default=None, help="override output path (default docs/intel/data/theme_weekly.json)")
    ap.add_argument(
        "--dry-run", action="store_true",
        help="collect + print per-theme card counts, skip the LLM call and the write — "
             "for local testing without spending sonnet tokens.",
    )
    args = ap.parse_args()

    date = args.date or _today_tpe()
    out_path = Path(args.out) if args.out else (DATA_DIR / "theme_weekly.json")

    try:
        themes = load_themes()
        if not themes:
            print("[intel/theme_weekly] themes.yml empty/unreadable — nothing to do.", file=sys.stderr)
            return 0
        themes_payload = collect_theme_cards(date, themes, days=args.days)
    except Exception as e:  # noqa: BLE001 — 加值步驟，任何例外都不可讓 chain 變紅
        print(f"[intel/theme_weekly] ERROR collecting cards: {e!r} — skipping this week.", file=sys.stderr)
        return 0

    counts = {k: len(v) for k, v in sorted(themes_payload.items())}
    print(f"[intel/theme_weekly] date={date} days={args.days} themes_with_cards={len(themes_payload)} "
          f"counts={counts}")

    if args.dry_run:
        print("[intel/theme_weekly] --dry-run: skipping LLM call and write.")
        return 0

    if not themes_payload:
        print("[intel/theme_weekly] no theme has any card in the lookback window — nothing to write.")
        return 0

    try:
        result = build_weekly(date, themes_payload)
    except Exception as e:  # noqa: BLE001
        print(f"[intel/theme_weekly] ERROR calling LLM: {e!r} — keeping existing theme_weekly.json.", file=sys.stderr)
        return 0

    if result is None:
        print("[intel/theme_weekly] no usable LLM result — keeping existing theme_weekly.json.")
        return 0

    write_weekly(out_path, result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
