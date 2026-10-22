#!/usr/bin/env python3
"""
選股席位變化通知（零 LLM，只比對名單，不做判斷）。

只在兩種情況發信：
  1. 三套席位有股票進席或出席
       美股看板 5 席     docs/engine/arena.json            core_seats
       台股 5 席         docs/cockpit-tw/data/seats_tw.json core_seats
       精選榜十倍組 10 席 docs/picks/tenbagger.json         seats.roster
  2. 每套「排隊前 5 名」的成員有進出（只比成員，名次對調不報）
       美股看板  arena.json buyable_seats，依 pool_rank 由小到大取前 5
       台股      seats_tw.json buyable 前 5（檔內已是排序）
       十倍組    tenbagger.json buyable 扣掉已在席者，取前 5
     三個定義跟 docs/cockpit/index.html、docs/cockpit-tw/index.html 的 renderRoster()
     「排隊（下次有空席先補）」完全一致。

池子進出、階段、品質閘翻轉都不報。

狀態檔 docs/engine/roster_notify_state.json（schema "roster-v1"）：
  {"schema": "roster-v1", "as_of": "YYYY-MM-DD",
   "segments": {"us": {"seats": [{"t": 代號, "n": 名稱}], "queue": [...]}, "tw": ..., "tb": ...}}
換版後第一次跑（狀態檔不存在、或不是這個 schema）只建基準，不發通知。
某一套的資料檔缺失或格式不符：那一套沿用舊狀態、不比較、不報；其他套照常。

輸出（有變化才寫，沒變化會刪掉舊檔）：
  roster_alert.txt          純文字內文（email 備援與 Discord 共用）
  roster_alert_subject.txt  標題（資料日）
  roster_alert_mail.html    email 版型（scripts/mail_html.py）

--dry-run：印出會寄的內容，不寫任何檔。永遠 exit 0，不能讓 workflow 失敗。

Usage: python3 scripts/check_seat_roster_alerts.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mail_html import esc, frame, note, section  # noqa: E402 — 共用 email 版型

ROOT = Path(__file__).resolve().parent.parent
ARENA_JSON = ROOT / "docs" / "engine" / "arena.json"
TW_JSON = ROOT / "docs" / "cockpit-tw" / "data" / "seats_tw.json"
TB_JSON = ROOT / "docs" / "picks" / "tenbagger.json"
STATE_JSON = ROOT / "docs" / "engine" / "roster_notify_state.json"
ALERT_TXT = ROOT / "roster_alert.txt"
SUBJECT_TXT = ROOT / "roster_alert_subject.txt"
MAIL_HTML = ROOT / "roster_alert_mail.html"  # 純本地 workspace 產物，gitignored

SCHEMA = "roster-v1"
QUEUE_N = 5
SITE = "https://research.investmquest.com"
LINKS = (("美股看板與總覽", f"{SITE}/cockpit/"), ("台股席位", f"{SITE}/cockpit-tw/"),
         ("精選榜十倍組", f"{SITE}/cockpit/#picks"))
SEGMENTS = (("us", "美股看板"), ("tw", "台股"), ("tb", "精選榜十倍組"))


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _entry(row: dict) -> dict | None:
    t = row.get("ticker") if isinstance(row, dict) else None
    if not t:
        return None
    return {"t": t, "n": row.get("name") or ""}


def _entries(rows) -> list[dict]:
    return [e for e in (_entry(r) for r in rows) if e]


def _rank_key(row: dict):
    pr = row.get("pool_rank") if isinstance(row, dict) else None
    return pr if isinstance(pr, (int, float)) else float("inf")


def load_segments() -> tuple[dict, str | None]:
    """回傳 ({"us"|"tw"|"tb": {"seats": [...], "queue": [...]}}, 資料日)。
    資料檔缺失或欄位不是 list 的那一套不會出現在結果裡。資料日取各套可得日期的最大值。"""
    out: dict[str, dict] = {}
    dates: list[str] = []

    arena = _load_json(ARENA_JSON)
    if isinstance(arena, dict) and isinstance(arena.get("core_seats"), list) \
            and isinstance(arena.get("buyable_seats"), list):
        # sorted 是穩定排序：pool_rank 缺值的維持檔內順序排在後面
        bq = sorted(arena["buyable_seats"], key=_rank_key)
        out["us"] = {"seats": _entries(arena["core_seats"]), "queue": _entries(bq)[:QUEUE_N]}
        d = str(arena.get("run_timestamp") or "")[:10]
        if d:
            dates.append(d)

    tw = _load_json(TW_JSON)
    if isinstance(tw, dict) and isinstance(tw.get("core_seats"), list) \
            and isinstance(tw.get("buyable"), list):
        out["tw"] = {"seats": _entries(tw["core_seats"]), "queue": _entries(tw["buyable"])[:QUEUE_N]}
        if tw.get("as_of"):
            dates.append(str(tw["as_of"])[:10])

    tb = _load_json(TB_JSON)
    seats = (tb or {}).get("seats") if isinstance(tb, dict) else None
    if isinstance(seats, dict) and isinstance(seats.get("roster"), list) \
            and isinstance(tb.get("buyable"), list):
        roster = _entries(seats["roster"])
        seated = {e["t"] for e in roster}
        queue = [e for e in _entries(tb["buyable"]) if e["t"] not in seated]
        out["tb"] = {"seats": roster, "queue": queue[:QUEUE_N]}
        if tb.get("as_of"):
            dates.append(str(tb["as_of"])[:10])

    return out, (max(dates) if dates else None)


def _label(ticker: str, names: dict) -> str:
    """台股 2330.TW → 「2330 台積電」；其他（美股）有名稱才附。"""
    name = names.get(ticker) or ""
    code = ticker[:-3] if ticker.endswith(".TW") else ticker
    return f"{code} {name}" if name else code


def diff_segment(prev: dict, cur: dict) -> dict:
    """prev/cur 都是 {"seats": [...], "queue": [...]}；只比成員。"""
    names = {e["t"]: e["n"] for part in (prev, cur) for k in ("seats", "queue") for e in part[k]}
    ps, cs = [e["t"] for e in prev["seats"]], [e["t"] for e in cur["seats"]]
    pq, cq = [e["t"] for e in prev["queue"]], [e["t"] for e in cur["queue"]]
    seat_in = [t for t in cs if t not in ps]
    seat_out = [t for t in ps if t not in cs]
    q_in = [t for t in cq if t not in pq]
    q_out = [t for t in pq if t not in cq]
    return {"seat_in": seat_in, "seat_out": seat_out, "q_in": q_in, "q_out": q_out,
            "seated_now": set(cs), "seated_before": set(ps), "names": names}


def _describe(d: dict) -> str | None:
    """一套的白話一行；沒變化回 None。"""
    nm = d["names"]
    parts = []
    if d["seat_in"]:
        parts.append("進席 " + "、".join(_label(t, nm) for t in d["seat_in"]))
    if d["seat_out"]:
        parts.append("出席 " + "、".join(_label(t, nm) for t in d["seat_out"]))
    qi = [_label(t, nm) + ("（剛出席）" if t in d["seat_out"] else "") for t in d["q_in"]]
    qo = [_label(t, nm) + ("（改進席）" if t in d["seat_in"] else "") for t in d["q_out"]]
    if qi or qo:
        q = []
        if qi:
            q.append("新進 " + "、".join(qi))
        if qo:
            q.append("掉出 " + "、".join(qo))
        parts.append("排隊前 5 " + "，".join(q))
    return "；".join(parts) if parts else None


def compute(state, segments: dict, as_of: str | None) -> dict:
    """純函式：給舊狀態與今天的各套名單，回傳事件行與新狀態。"""
    baseline = not (isinstance(state, dict) and state.get("schema") == SCHEMA
                    and isinstance(state.get("segments"), dict))
    prev_segs = {} if baseline else state["segments"]
    new_segs: dict[str, dict] = {}
    lines: list[tuple[str, str]] = []  # (套名, 白話一行)

    for key, label in SEGMENTS:
        cur = segments.get(key)
        prev = prev_segs.get(key)
        if cur is None:
            # 今天這套資料缺：沿用舊狀態，不比較
            if isinstance(prev, dict):
                new_segs[key] = prev
            continue
        new_segs[key] = cur
        if baseline or not isinstance(prev, dict) or "seats" not in prev or "queue" not in prev:
            continue  # 首跑或這套第一次出現：只建基準
        text = _describe(diff_segment(prev, cur))
        if text:
            lines.append((label, text))

    new_state = {"schema": SCHEMA, "as_of": as_of or (state or {}).get("as_of") or "", "segments": new_segs}
    return {"baseline": baseline, "lines": lines, "new_state": new_state}


def build_subject(as_of: str) -> str:
    return f"🧭 選股席位變化 {as_of}"


def build_body(lines: list[tuple[str, str]]) -> str:
    out = [f"{label}：{text}" for label, text in lines]
    out += [""] + [f"{name}：{url}" for name, url in LINKS]
    return "\n".join(out) + "\n"


def build_mail_html(as_of: str, lines: list[tuple[str, str]]) -> str:
    body = ""
    for label, text in lines:
        items = "".join(f'<li style="margin:0 0 6px;">{esc(p)}</li>' for p in text.split("；"))
        body += section("ROSTER", label,
                        f'<ul style="margin:0;padding-left:18px;font-size:13.5px;line-height:1.65;'
                        f'color:#333333;">{items}</ul>')
    body += note("排隊前 5 只比成員，名次對調不報。" + " ".join(
        f'<a href="{esc(url)}">{esc(name)}</a>' for name, url in LINKS))
    return frame(title="選股席位變化", date=as_of, body_html=body,
                 button_label="前往選股主控台 →", button_url=LINKS[0][1], accent="navy",
                 disclaimer="本信為機械化名單異動通知，非投資判斷或買賣建議。")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="印出內容，不寫任何檔")
    args = parser.parse_args(argv)

    segments, as_of = load_segments()
    state = _load_json(STATE_JSON)
    if not segments:
        print("roster_alerts: 三套資料檔都讀不到，略過（狀態檔未動）")
        return 0
    result = compute(state, segments, as_of)
    lines = result["lines"]
    tag = "[dry-run] " if args.dry_run else ""

    if result["baseline"]:
        print(f"{tag}roster_alerts: 沒有 {SCHEMA} 狀態檔，只建基準、不發通知（資料日 {as_of}）")
    elif lines:
        print(f"{tag}roster_alerts: {len(lines)} 套有變化（資料日 {as_of}）")
    else:
        print(f"{tag}roster_alerts: 無變化（資料日 {as_of}）")

    if lines:
        subject, body = build_subject(as_of), build_body(lines)
        if args.dry_run:
            print(f"{tag}---- 標題 ----\n{subject}\n{tag}---- 內文 ----\n{body}", end="")
        else:
            ALERT_TXT.write_text(body, encoding="utf-8")
            SUBJECT_TXT.write_text(subject, encoding="utf-8")
            MAIL_HTML.write_text(build_mail_html(as_of, lines), encoding="utf-8")
    elif not args.dry_run:
        for p in (ALERT_TXT, SUBJECT_TXT, MAIL_HTML):
            if p.exists():
                p.unlink()

    if args.dry_run:
        print(f"{tag}狀態檔未寫入")
    else:
        STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
        STATE_JSON.write_text(json.dumps(result["new_state"], ensure_ascii=False, indent=1),
                              encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 — 通知器不可擋排程，任何未預期錯誤照樣 exit 0
        print(f"roster_alerts: unexpected error, skipping ({exc!r})")
        sys.exit(0)
