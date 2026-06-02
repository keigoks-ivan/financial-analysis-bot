#!/usr/bin/env python3
"""Aggregate the 💎 satellite / 🐘 elephant / 🔒 uninvestable tiers across ALL
supply-chain topic maps into a single cross-map synthesis block on the hub page
docs/supply-chain/index.html.

Mirrors the per-page logic in assets/engine.js (isGolden + node_role), but
deduped across every map and keyed by normalized ticker. Output is injected
between the <!-- TIERS_AUTO_START --> / <!-- TIERS_AUTO_END --> markers, so the
hub page stays a static file (no client-side fetch storm over 26 JSONs).

Re-run whenever a map's tiers change:
    python3 scripts/build_supply_chain_tiers.py
"""
from __future__ import annotations

import glob
import html
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SC = ROOT / "docs" / "supply-chain"
DATA = SC / "data"
INDEX = SC / "index.html"
SKIP = {"topics.json", "dd_links.json"}

# Collapse overlapping topics into real process-domains, so cross-map "breadth"
# is not inflated by how densely a niche happens to be mapped.
DOMAIN = {
    "advanced": "前段/微影", "fe-equipment": "前段/微影", "metrology": "前段/微影",
    "hbm": "記憶體", "memory": "記憶體",
    "cowos": "封裝/載板", "substrate": "封裝/載板", "plp": "封裝/載板",
    "material": "封裝/載板", "ai-pcb": "封裝/載板",
    "asic": "晶片設計/IP", "icdesign": "晶片設計/IP",
    "cpo": "光通訊", "siph": "光通訊",
    "dc-networking": "資料中心硬體", "server": "資料中心硬體",
    "neocloud": "雲端/GPU", "power": "電源散熱", "passive": "被動元件",
    "defense": "軍工", "nuclear": "核能", "robot": "機器人",
    "leosat": "太空", "spacedc": "太空", "fusion": "核融合", "quantum": "量子",
}

FLAG = {
    "TW": "🇹🇼", "US": "🇺🇸", "JP": "🇯🇵", "KR": "🇰🇷", "CN": "🇨🇳", "NL": "🇳🇱",
    "DE": "🇩🇪", "EU": "🇪🇺", "IL": "🇮🇱", "HK": "🇭🇰", "SG": "🇸🇬", "CH": "🇨🇭",
    "UK": "🇬🇧", "FR": "🇫🇷", "AT": "🇦🇹", "DK": "🇩🇰", "SE": "🇸🇪", "GLOBAL": "🌐",
}

TICKER_SUFFIX = re.compile(r"\.(TWO|TW|T|KS|HK|DE|SW|PA|L|AX|SI|KQ|SS)$", re.I)


def norm_key(c: dict) -> str:
    t = (c.get("ticker") or "").strip()
    if t and t != "—":
        return TICKER_SUFFIX.sub("", t)
    return "NM:" + c.get("name", "?").split("(")[0].strip()


def is_golden(node: dict, c: dict) -> bool:
    # 💎 Top Pick must be investable — a no-ticker private name (e.g. SpaceX
    # pre-IPO) can never be a satellite, even if core_business+tight.
    tk = (c.get("ticker") or "").strip()
    return bool(node.get("single")) and c.get("core_business") is True \
        and c.get("supply_chain_lock") == "tight" and tk not in ("", "—")


def tier_of(node: dict, c: dict) -> str | None:
    if is_golden(node, c):
        return "satellite"
    nr = c.get("node_role")
    if nr in ("elephant", "uninvestable"):
        return nr
    return None


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def collect():
    dd_links = {}
    p = DATA / "dd_links.json"
    if p.exists():
        try:
            dd_links = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            dd_links = {}

    tiers = {"satellite": {}, "elephant": {}, "uninvestable": {}}
    for f in sorted(glob.glob(str(DATA / "*.json"))):
        if Path(f).name in SKIP:
            continue
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        tid = d.get("id", Path(f).stem)
        dom = DOMAIN.get(tid, tid)
        for n in d.get("nodes", []):
            if not n.get("single"):
                continue
            for c in n.get("companies", []):
                t = tier_of(n, c)
                if not t:
                    continue
                k = norm_key(c)
                e = tiers[t].setdefault(k, {
                    "name": c.get("name", "?"), "ticker": c.get("ticker", ""),
                    "country": c.get("country", ""), "topics": {}, "domains": set(),
                    "evidence": "",
                })
                e["domains"].add(dom)
                # keep the strongest-looking share/single snippet as evidence
                share = (c.get("share") or "").strip()
                e["topics"][tid] = share
                if not e["evidence"]:
                    e["evidence"] = (n.get("single") or share or "")[:120]
    return tiers, dd_links


def row_html(e: dict, dd_links: dict) -> str:
    flag = FLAG.get(e["country"], "")
    tk = e["ticker"] if e["ticker"] and e["ticker"] != "—" else ""
    tk_html = f'<span class="tk">{esc(tk)}</span>' if tk else ""
    dd = dd_links.get(tk) if tk else None
    dd_btn = (f' <a href="{esc(dd)}" class="dd-link" target="_blank" rel="noopener" '
              f'title="開啟 DD 報告">DD ↗</a>') if dd else ""
    ndom = len(e["domains"])
    dom_badge = (f'<span class="gold-node-chip">跨 {ndom} 域</span>' if ndom >= 2 else "")
    topic_chips = "".join(
        f'<span class="gold-node-chip">{esc(t)}</span>' for t in sorted(e["topics"])
    )
    ev = esc(e["evidence"])
    return (f'<tr><td><span class="gold-co"><span class="co-flag">{flag}</span>'
            f'<strong>{esc(e["name"])}</strong>{tk_html}</span>{dd_btn}{dom_badge}</td>'
            f'<td>{topic_chips}</td>'
            f'<td><span class="gold-single">⚑ {ev}</span></td></tr>')


def table_html(entries: dict, cls: str, dd_links: dict, head0: str) -> str:
    # sort by distinct real-domains desc (breadth, de-biased), then #topics, then key
    rows = sorted(entries.values(),
                  key=lambda e: (-len(e["domains"]), -len(e["topics"]), e["name"]))
    body = "".join(row_html(e, dd_links) for e in rows)
    return (f'<div class="gold-table-wrap"><table class="gold-table {cls}">'
            f'<thead><tr><th>{head0}</th><th>出現產業</th><th>鎖喉證據</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


def build_block(tiers: dict, dd_links: dict) -> str:
    sat, ele, uni = tiers["satellite"], tiers["elephant"], tiers["uninvestable"]
    h = []
    h.append(f'<h3><span class="ico">💎</span>Satellite Top Picks · {len(sat)} 檔</h3>')
    h.append('<p class="lede">全站去重後、鎖喉<strong>推得動該股 EPS</strong> 的純玩家。'
             '依「跨真實製程域」數排序（非出現次數 — 避免某利基被多張圖重複覆蓋而虛胖）；'
             '<em>次數多 ≠ 更不可或缺</em>，廣度只是加分，深度（自身壟斷強度）才是主軸。</p>')
    h.append(table_html(sat, "", dd_links, "公司"))
    h.append(f'<h3 class="tier-ele"><span class="ico">🐘</span>Elephant · {len(ele)} 個 — '
             '最不可或缺，但鎖喉被稀釋</h3>')
    h.append('<p class="lede">它<strong>就是</strong>鎖喉本身（壟斷／近獨佔），但身處大型多角化集團，'
             '單一節點推不動 EPS。<strong>用 core-holding 框架評</strong>，不是 single-point satellite。</p>')
    h.append(table_html(ele, "tier-ele-tbl", dd_links, "公司"))
    h.append(f'<h3 class="tier-uni"><span class="ico">🔒</span>不可投資的鎖喉 · {len(uni)} 個</h3>')
    h.append('<p class="lede">結構上唯一 / sole-source，但<strong>買不到純曝險</strong> — '
             '未上市，或已是某上市母體的次組件。要曝險請透過母體 / 客戶。</p>')
    h.append(table_html(uni, "tier-uni-tbl", dd_links, "節點供應商"))
    h.append('<p class="gold-foot">由 <code>scripts/build_supply_chain_tiers.py</code> 掃描全部 '
             '<code>docs/supply-chain/data/*.json</code> 聚合。判準：💎 <code>core_business</code>×'
             '<code>supply_chain_lock:"tight"</code>｜🐘 <code>node_role:"elephant"</code>｜'
             '🔒 <code>node_role:"uninvestable"</code>。</p>')
    return "\n".join(h)


def main() -> int:
    tiers, dd_links = collect()
    block = build_block(tiers, dd_links)
    txt = INDEX.read_text(encoding="utf-8")
    pat = re.compile(r"(<!-- TIERS_AUTO_START -->).*?(<!-- TIERS_AUTO_END -->)", re.S)
    if not pat.search(txt):
        print("ERROR: markers not found in index.html")
        return 1
    new = pat.sub(lambda m: f"{m.group(1)}\n{block}\n{m.group(2)}", txt)
    INDEX.write_text(new, encoding="utf-8")
    print(f"injected: 💎 {len(tiers['satellite'])} / 🐘 {len(tiers['elephant'])} / "
          f"🔒 {len(tiers['uninvestable'])} into {INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
