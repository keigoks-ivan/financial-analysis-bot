#!/usr/bin/env python3
"""Build the site-wide search index + homepage 最新發布 strip.

Walks every report corpus under docs/, extracts a compact entry per report
({u:url, t:title, k:type, s:[tickers/keywords], d:YYYY-MM-DD}) and emits
docs/assets/search-index.json (short keys, sorted, zero-churn write).

This script is ALSO the single owner of the homepage 最新發布 strip: it
re-injects the 8 newest dated entries between the
<!-- LATEST_FEED_START --> / <!-- LATEST_FEED_END --> markers in
docs/index.html, so the strip stays fresh when the chain re-runs.

build_rss.py imports collect_inventory() from here — one inventory, two
consumers. No git side effects.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# ── type labels (short, used as filter-chip keys on /search.html) ──
T_DD = "個股DD"
T_ID = "產業ID"
T_MACRO = "總經"
T_MS = "對比"
T_SYN = "期望綜合"
T_DS = "產業DS·legacy"
T_DCA = "決策DCA·legacy"
T_EARN = "財報"
T_CROWD = "擁擠交易"
T_ROT = "產業輪動"
T_SC = "供應鏈"

MAX_TITLE = 96  # trim long titles to keep index compact


def _read(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def _meta(text: str, mid: str):
    m = re.search(r'id="%s"[^>]*>(.*?)</script>' % re.escape(mid), text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def _title_tag(text: str) -> str:
    m = re.search(r"<title>([^<]*)</title>", text)
    return m.group(1).strip() if m else ""


def _fdate(yyyymmdd: str) -> str:
    return f"{yyyymmdd[0:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}"


def _trim(s: str) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    return s[: MAX_TITLE - 1] + "…" if len(s) > MAX_TITLE else s


def _uniq(seq):
    seen, out = set(), []
    for x in seq:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def collect_inventory() -> list[dict]:
    """Return list of entries: {u,t,k,s,d}. s = ticker/keyword list."""
    ent: list[dict] = []

    # ── 個股 DD ──
    for f in glob.glob(os.path.join(DOCS, "dd", "DD_*.html")):
        base = os.path.basename(f)
        m = re.match(r"^DD_(.+)_(\d{8})\.html$", base)
        if not m:
            continue
        ticker, ymd = m.group(1), m.group(2)
        meta = _meta(_read(f), "dd-meta") or {}
        verdict = meta.get("dca_verdict") or meta.get("verdict") or meta.get("signal") or ""
        role = meta.get("dca_role") or ""
        title = f"{ticker} 個股 DD"
        if verdict:
            title += f"｜{verdict}"
        if role:
            title += f"｜{role}"
        ent.append({"u": f"/dd/{base}", "t": _trim(title), "k": T_DD,
                    "s": [ticker], "d": _fdate(ymd)})

    # ── 產業 ID（無 id-meta 者跳過）──
    for f in glob.glob(os.path.join(DOCS, "id", "ID_*.html")):
        base = os.path.basename(f)
        text = _read(f)
        meta = _meta(text, "id-meta")
        if not meta:
            continue
        theme = meta.get("theme") or _title_tag(text)
        date = meta.get("publish_date") or ""
        if not date:
            dm = re.search(r"_(\d{8})", base)
            date = _fdate(dm.group(1)) if dm else ""
        tickers = [rt.get("ticker") for rt in meta.get("related_tickers", [])
                   if isinstance(rt, dict) and rt.get("ticker")]
        ent.append({"u": f"/id/{base}", "t": _trim(f"{theme} 產業 ID"), "k": T_ID,
                    "s": _uniq(tickers)[:12], "d": date})

    # ── 總經 MACRO ──
    for f in glob.glob(os.path.join(DOCS, "macro", "MACRO_*.html")):
        base = os.path.basename(f)
        meta = _meta(_read(f), "macro-meta") or {}
        m = re.match(r"^MACRO_(.+)_(\d{8})\.html$", base)
        slug = meta.get("slug") or (m.group(1) if m else "")
        date = meta.get("date") or (_fdate(m.group(2)) if m else "")
        topic = meta.get("topic") or slug
        ent.append({"u": f"/macro/{base}", "t": _trim(f"{topic} 總經報告"), "k": T_MACRO,
                    "s": [slug] if slug else [], "d": date})

    # ── 多股對比 MS ──
    for f in glob.glob(os.path.join(DOCS, "comparisons", "MS_*.html")):
        base = os.path.basename(f)
        m = re.match(r"^MS_(.+)_(\d{8})\.html$", base)
        if not m:
            continue
        mid, ymd = m.group(1), m.group(2)
        parts = re.split(r"vs|_", mid)
        parts = [p for p in parts if p]
        ent.append({"u": f"/comparisons/{base}",
                    "t": _trim(" vs ".join(parts) + " 多股對比"), "k": T_MS,
                    "s": _uniq(parts)[:6], "d": _fdate(ymd)})

    # ── 期望落差綜合研判 ──
    for f in glob.glob(os.path.join(DOCS, "research", "synthesis", "*.html")):
        base = os.path.basename(f)
        if base == "index.html":
            continue
        m = re.match(r"^(.+)_(\d{8})\.html$", base)
        if not m:
            continue
        ticker, ymd = m.group(1), m.group(2)
        ent.append({"u": f"/research/synthesis/{base}",
                    "t": _trim(f"{ticker} 趨勢 × 期望落差綜合研判"), "k": T_SYN,
                    "s": [ticker], "d": _fdate(ymd)})

    # ── 產業 DS（legacy）──
    for f in glob.glob(os.path.join(DOCS, "ds", "DS_*.html")):
        base = os.path.basename(f)
        m = re.match(r"^DS_(.+)_(\d{8})\.html$", base)
        if not m:
            continue
        slug, ymd = m.group(1), m.group(2)
        ent.append({"u": f"/ds/{base}", "t": _trim(f"{slug} 產業敘述 DS"), "k": T_DS,
                    "s": [slug], "d": _fdate(ymd)})

    # ── 決策 DCA（legacy）──
    for f in glob.glob(os.path.join(DOCS, "dca", "DCA_*.html")):
        base = os.path.basename(f)
        m = re.match(r"^DCA_(.+)_(\d{8})\.html$", base)
        if not m:
            continue
        ticker, ymd = m.group(1), m.group(2)
        ent.append({"u": f"/dca/{base}", "t": _trim(f"{ticker} 決策 DCA"), "k": T_DCA,
                    "s": [ticker], "d": _fdate(ymd)})

    # ── 財報（日報 + 統整）──
    for f in (glob.glob(os.path.join(DOCS, "earnings", "earnings_*.html"))
              + glob.glob(os.path.join(DOCS, "earnings", "synthesis_*.html"))):
        base = os.path.basename(f)
        m = re.match(r"^(earnings|synthesis)_(\d{4}-\d{2}-\d{2})\.html$", base)
        if not m:
            continue
        date = m.group(2)
        title = _title_tag(_read(f)) or f"財報 {date}"
        title = re.sub(r"\s*[—·|]\s*InvestMQuest.*$", "", title)
        ent.append({"u": f"/earnings/{base}", "t": _trim(title), "k": T_EARN,
                    "s": [], "d": date})

    # ── 擁擠交易監測 ──
    for f in glob.glob(os.path.join(DOCS, "crowding", "CROWDING_*.html")):
        base = os.path.basename(f)
        m = re.match(r"^CROWDING_(\d{8})\.html$", base)
        if not m:
            continue
        title = _title_tag(_read(f)) or "跨資產擁擠交易監測"
        title = re.sub(r"\s*·\s*InvestMQuest.*$", "", title)
        ent.append({"u": f"/crowding/{base}", "t": _trim(title), "k": T_CROWD,
                    "s": [], "d": _fdate(m.group(1))})

    # ── 產業輪動監測 ──
    for f in glob.glob(os.path.join(DOCS, "rotation", "ROTATION_*.html")):
        base = os.path.basename(f)
        m = re.match(r"^ROTATION_(\d{8})\.html$", base)
        if not m:
            continue
        title = _title_tag(_read(f)) or "產業輪動監測"
        title = re.sub(r"\s*·\s*InvestMQuest.*$", "", title)
        ent.append({"u": f"/rotation/{base}", "t": _trim(title), "k": T_ROT,
                    "s": [], "d": _fdate(m.group(1))})

    # ── 供應鏈地圖（依 manifest active topics；無日期）──
    tp = os.path.join(DOCS, "supply-chain", "data", "topics.json")
    if os.path.exists(tp):
        for t in json.load(open(tp, encoding="utf-8")).get("topics", []):
            if not t.get("active"):
                continue
            tid = t.get("id")
            page = os.path.join(DOCS, "supply-chain", f"{tid}.html")
            if not tid or not os.path.exists(page):
                continue
            ent.append({"u": f"/supply-chain/{tid}.html",
                        "t": _trim(t.get("title") or tid), "k": T_SC,
                        "s": _uniq([tid, t.get("tab")]), "d": ""})

    # newest first; undated sink to bottom; url tiebreak for stable order
    ent.sort(key=lambda e: (e["d"], e["u"]), reverse=True)
    return ent


# ── zero-churn helpers ──

def _write_if_changed(path: str, content: str) -> bool:
    old = None
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            old = fh.read()
    if old == content:
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return True


def _esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def build_homepage_strip(entries: list[dict]) -> str:
    dated = [e for e in entries if e["d"]][:8]
    rows = []
    for e in dated:
        label = str(e["t"]).split()[0] if e["t"] else e["k"]
        rows.append(
            '        <a class="lf-chip" href="%s" title="%s">'
            '<span class="lf-badge">%s</span>%s'
            '<span class="lf-d">%s</span></a>'
            % (_esc(e["u"]), _esc(e["t"]), _esc(e["k"]), _esc(label), _esc(e["d"]))
        )
    items = "\n".join(rows)
    return (
        "<!-- LATEST_FEED_START -->\n"
        '<section class="latest-feed">\n'
        '  <div class="container">\n'
        '    <div class="lf-head">\n'
        "      <h2>最近發布</h2>\n"
        '      <form class="lf-search" action="/search.html" method="get" role="search">\n'
        '        <input type="search" name="q" placeholder="搜尋代碼、公司或主題 —— NVDA、玻璃基板…" aria-label="全站搜尋" autocomplete="off">\n'
        "      </form>\n"
        "    </div>\n"
        '    <div class="lf-strip">\n'
        f"{items}\n"
        '        <a class="lf-more" href="/t/">全部 &rarr;</a>\n'
        "    </div>\n"
        '    <div class="lf-links">\n'
        '      <a href="/search.html">全站搜尋</a><span class="lf-sep">·</span>'
        '<a href="/t/">個股總覽 /t/</a><span class="lf-sep">·</span>'
        '<a href="/track-record/">裁決實績</a><span class="lf-sep">·</span>'
        '<a href="/data.html">公開資料</a><span class="lf-sep">·</span>'
        '<a href="/rss.xml">RSS</a>\n'
        "    </div>\n"
        "  </div>\n"
        "</section>\n"
        "<!-- LATEST_FEED_END -->"
    )


def reinject_homepage(entries: list[dict]) -> str:
    path = os.path.join(DOCS, "index.html")
    text = _read(path)
    strip = build_homepage_strip(entries)
    pat = re.compile(r"<!-- LATEST_FEED_START -->.*?<!-- LATEST_FEED_END -->", re.S)
    if not pat.search(text):
        return "no-markers"
    new = pat.sub(lambda _m: strip, text)
    return "updated" if _write_if_changed(path, new) else "unchanged"


def main() -> None:
    entries = collect_inventory()
    payload = json.dumps({"v": 1, "entries": entries},
                         ensure_ascii=False, separators=(",", ":"))
    out = os.path.join(DOCS, "assets", "search-index.json")
    changed = _write_if_changed(out, payload)

    by_type: dict[str, int] = {}
    for e in entries:
        by_type[e["k"]] = by_type.get(e["k"], 0) + 1
    print(f"search-index: {len(entries)} entries, {len(payload)} bytes "
          f"({len(payload)/1024:.1f} KB) — {'written' if changed else 'zero-churn'}")
    for k, v in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {k:14s} {v}")

    hp = reinject_homepage(entries)
    print(f"homepage 最新發布 strip: {hp}")


if __name__ == "__main__":
    main()
