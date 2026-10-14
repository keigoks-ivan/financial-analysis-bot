#!/usr/bin/env python3
"""id2 run.py — 產業深度報告（ID）管線原型，仿 scripts/dd2。

    python3.12 scripts/id2/run.py {Theme} [--date YYYYMMDD] [--until STAGE] [--resume] [--refresh]
                                  [--dry-run] [--publish]

段：plan → evidence → judge → gate → prose → check → (publish)
LLM 只在 evidence（sonnet，每軸一通，平行，各自獨立 session）、judge（opus，單輪無工具，同 prompt 平行三次，sd_verdict／clock_phase 取多數，2:1 加交界標記）、
gate（sonnet，單輪無工具；紅燈一通 patch map 再閘一次）、prose（sonnet，前後半平行，只有 Write）。
其餘零 LLM。預設（含 --dry-run）只寫 .id_build/runs/{Theme}_{date}/，不碰 docs/；--publish 才發布。
設計：notes/site-internal/id/_id2_design_20261013.md。dd2 與 dd_headless 一字不改，只 import。
"""
import argparse
import copy
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SCRIPTS = ROOT / "scripts"
for p in (str(SCRIPTS), str(SCRIPTS / "dd2")):
    if p not in sys.path:
        sys.path.insert(0, p)

import dd_headless  # noqa: E402
import spawn as sp  # noqa: E402  dd2/spawn.py

SKILL_DIR = ROOT / ".claude" / "skills" / "industry-analyst"
BUILD = ROOT / ".id_build"
STAGES = ["plan", "evidence", "judge", "gate", "prose", "check", "publish"]
SKILL_VERSION = "v4.1"  # id2 產物；id-meta 三處同值

AXES = ["A", "B", "C", "D", "E"]
# 證據軸快取期限（天）：歷史慢、價格與庫存快
AXIS_TTL = {"A": 180, "B": 30, "C": 30, "D": 14, "E": 30}
EVID_MAX_TURNS = 32
EVID_MAX_SEARCH, EVID_MAX_FETCH = 16, 8
JUDGE_THINKING_CAP = 32_000
JUDGE_RUNS = 3  # 2026-10-14 持有人拍板：判斷跑三次取多數（穩定度測試 clock_phase II／III／III）
PHASE_ORDER = {"I": 1, "II": 2, "III": 3, "IV": 4}
SD_ORDER = {"shortage": 1, "balanced": 2, "surplus": 3, "split": 4}
BOUNDARY_ZH = {"I": "第一", "II": "第二", "III": "第三", "IV": "第四",
               "shortage": "短缺", "balanced": "平衡", "surplus": "過剩", "split": "分裂"}
GATE_MODEL, JUDGE_MODEL, PROSE_MODEL = "sonnet", "opus", "sonnet"
SECTION_ZH = {"thesis": "核心判斷", "debates": "市場哪裡看錯", "mechanics": "機制與供需", "valuation": "現在貴不貴",
              "risks": "我怎麼知道我錯了", "stocks": "誰受影響", "appendix": "背景與歷史", "base_rate": "核心判斷"}


# ------------------------------------------------------------------ 小工具
def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def jload(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def jdump(p, obj):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(p) + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(p)


def render(tmpl_path, mapping):
    """單次掃描替換 {{KEY}}；值裡出現的 {{…}} 不再展開。"""
    text = Path(tmpl_path).read_text(encoding="utf-8")
    return re.sub(r"\{\{([A-Z0-9_]+)\}\}", lambda m: str(mapping.get(m.group(1), m.group(0))), text)


def run(cmd, cwd=ROOT):
    r = subprocess.run([str(c) for c in cmd], cwd=str(cwd), capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def usage(label, r, extra=None):
    rec = {"id": label, "ok": r.get("ok"), "num_turns": r.get("num_turns"), "output_tokens": r.get("output_tokens"),
           "cache_read": r.get("cache_read"), "cache_creation": r.get("cache_creation"),
           "cost_usd": r.get("cost_usd"), "duration_ms": r.get("duration_ms"),
           "thinking_tokens": r.get("thinking_tokens")}
    if extra:
        rec.update(extra)
    return rec


def enrich(r, out_json):
    """spawn_many 的結果補 thinking token（讀落地的 raw JSON）。"""
    r = dict(r or {"ok": False})
    try:
        mu = jload(out_json).get("modelUsage") or {}
        r["thinking_tokens"] = sum((v.get("thinkingTokens") or 0) for v in mu.values() if isinstance(v, dict))
    except Exception:
        pass
    return r


class Ctx:
    def __init__(self, a):
        self.theme = a.theme
        self.date = a.date or dt.date.today().strftime("%Y%m%d")
        self.iso = "{0}-{1}-{2}".format(self.date[:4], self.date[4:6], self.date[6:])
        self.a = a
        self.dir = BUILD / "runs" / "{0}_{1}".format(self.theme, self.date)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.mpath = self.dir / "manifest.json"
        self.m = jload(self.mpath) if self.mpath.exists() else {"theme": self.theme, "date": self.date,
                                                                 "pipeline": "id2", "stages": {}, "created": now()}

    def save(self):
        jdump(self.mpath, self.m)

    def begin(self, name):
        self.m["stages"][name] = {"state": "RUNNING", "started": now(), "agent_usage": []}
        self.save()
        return self.m["stages"][name]

    def end(self, name, ok, note=""):
        st = self.m["stages"][name]
        st["state"] = "PASS" if ok else "FAIL"
        st["ended"] = now()
        if note:
            st["note"] = note[-1500:]
        self.save()
        print("[{0}] {1} {2}".format(name, st["state"], note.splitlines()[-1] if note else ""))
        return ok

    def passed(self, name):
        return self.m["stages"].get(name, {}).get("state") == "PASS"


# ------------------------------------------------------------------ plan（零 LLM）
META_RE = re.compile(r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>', re.S)


def find_prior(theme):
    files = [f for f in glob.glob(str(ROOT / "docs" / "id" / "ID_{0}_*.html".format(theme)))
             if not f.endswith("_full.html")]
    files.sort(key=lambda f: re.search(r"_(\d{8})", f).group(1) if re.search(r"_(\d{8})", f) else "")
    return Path(files[-1]) if files else None


def prior_brief(prior):
    """只讀 id-meta＋kill 表＋分歧卡標題（防錨定）。回 (meta, markdown)。"""
    if not prior:
        return {}, "（無前版）"
    html = prior.read_text(encoding="utf-8")
    m = META_RE.search(html)
    meta = json.loads(m.group(1)) if m else {}
    lines = ["前版：{0}（skill {1}，發布 {2}）".format(prior.name, meta.get("skill_version"), meta.get("publish_date"))]
    for k in ("oneliner", "now_state", "future_state", "action", "sd_verdict", "clock_phase", "conviction",
              "priced_in", "demand_5y_multiple", "tam_usd_2030", "cagr_pct_5y", "mega", "sub_group"):
        if meta.get(k) is not None:
            lines.append("- {0}：{1}".format(k, meta[k]))
    lines.append("- 關聯個股：" + "、".join("{0}{1}".format(t.get("ticker"), t.get("depth", "")) for t in meta.get("related_tickers", [])))
    lines.append("\n前版 kill 指標：")
    for k in meta.get("kill_metrics", []):
        lines.append("- {0}｜{1}｜{2}".format(k.get("metric"), k.get("bear_threshold"), k.get("window")))
    titles = re.findall(r'class="dt"[^>]*>(?:<span class="dn">[^<]*</span>)?([^<]+)<', html)
    if titles:
        lines.append("\n前版分歧卡標題：" + "；".join(t.strip() for t in titles))
    return meta, "\n".join(lines)


def find_sisters(theme, prior_meta, tickers, date_iso):
    """同 mega/sub_group 或相關個股重疊 ≥2 的其他主題，每主題取最新一份 v4 以上 ID（掃 id-meta，不只信前版 sister_ids）。
    只回 sd_verdict／clock_phase／日期／數值欄／kill 表。"""
    latest = {}
    for f in glob.glob(str(ROOT / "docs" / "id" / "ID_*.html")):
        n = Path(f).name
        mm = re.fullmatch(r"ID_(.+)_(\d{8})(?:_full)?\.html", n)
        if not mm or n.endswith("_full.html") or mm.group(1) == theme:
            continue
        if mm.group(2) > date_iso.replace("-", ""):
            continue
        if mm.group(1) not in latest or mm.group(2) > latest[mm.group(1)][0]:
            latest[mm.group(1)] = (mm.group(2), f)
    mine = set(tickers)
    out = []
    for slug, (d, f) in latest.items():
        m = META_RE.search(Path(f).read_text(encoding="utf-8"))
        if not m:
            continue
        try:
            meta = json.loads(m.group(1))
        except Exception:
            continue
        if not meta.get("sd_verdict"):
            continue
        other = {x.get("ticker") for x in meta.get("related_tickers", []) if x.get("depth") in ("🔴", "🟡")}
        same = prior_meta.get("mega") and (meta.get("mega"), meta.get("sub_group")) == (prior_meta.get("mega"), prior_meta.get("sub_group"))
        ov = len(mine & other)
        if not (same or ov >= 2):
            continue
        out.append({"file": Path(f).name, "slug": slug, "date": d, "sd_verdict": meta.get("sd_verdict"), "clock_phase": meta.get("clock_phase"),
                    "conviction": meta.get("conviction"), "demand_5y_multiple": meta.get("demand_5y_multiple"),
                    "tam_usd_2030": meta.get("tam_usd_2030"), "overlap": ov, "same_group": bool(same),
                    "kill_metrics": [k.get("metric") + "｜" + str(k.get("bear_threshold")) for k in meta.get("kill_metrics", [])]})
    out.sort(key=lambda x: (not x["same_group"], -x["overlap"], x["date"]), reverse=False)
    return out[:8]


def sisters_block(prior_meta, sisters):
    lines = ["前版自己：sd_verdict={0} clock_phase={1} conviction={2} demand_5y_multiple={3} tam_usd_2030={4}".format(
        prior_meta.get("sd_verdict"), prior_meta.get("clock_phase"), prior_meta.get("conviction"), prior_meta.get("demand_5y_multiple"), prior_meta.get("tam_usd_2030"))]
    for s in sisters:
        lines.append("- {0}（{1}）：sd_verdict={2} clock_phase={3} conviction={4} demand_5y_multiple={5} tam_usd_2030={6}｜{7}｜kill：{8}".format(
            s["file"], s["date"], s["sd_verdict"], s["clock_phase"], s["conviction"], s["demand_5y_multiple"], s["tam_usd_2030"],
            "同 mega/sub_group" if s["same_group"] else "相關個股重疊 {0}".format(s["overlap"]), "；".join(s["kill_metrics"][:4])))
    return "\n".join(lines)


def weekly_return(ticker, today):
    f = ROOT / "data" / "weekly_cache" / "{0}.json".format(ticker)
    if not f.exists():
        return None
    bars = jload(f).get("weekly_bars") or []
    if len(bars) < 28:
        return None
    last, old = bars[-1], bars[-27]
    age = (today - dt.date.fromisoformat(last["week_end"])).days
    return {"close": last["close"], "as_of": last["week_end"], "ret26w_pct": round((last["close"] / old["close"] - 1) * 100, 1),
            "base_date": old["week_end"], "age_days": age}


def priced_inputs(tickers, today):
    """價格→26 週漲幅（weekly_cache）；Fwd P/E FY2 與 5Y 分位（dd-screener latest.json）。附來源、as-of、異常旗。"""
    sc = jload(ROOT / "docs" / "dd-screener" / "latest.json")
    rows = {r["ticker"]: r for r in sc.get("stocks", [])}
    out = []
    for t in tickers:
        rec = {"ticker": t, "flags": []}
        w = weekly_return(t, today)
        if w:
            rec.update(w)
            rec["ret_source"] = "data/weekly_cache/{0}.json（週線收盤，auto_adjust）".format(t)
            if abs(w["ret26w_pct"]) > 150:
                rec["flags"].append("26 週漲跌幅 >150%，確認資料")
            if w["age_days"] > 21:
                rec["flags"].append("週線已 {0} 天未更新".format(w["age_days"]))
        else:
            rec["flags"].append("無本地週線")
        r = rows.get(t)
        if r:
            rec["fpe_fy2"] = r.get("fpe_fy2")
            rec["pct_5y"] = r.get("pct_5y")
            rec["val_source"] = "docs/dd-screener/latest.json（as_of {0}）".format(sc.get("as_of"))
            if r.get("fpe_fy2") is None:
                rec["flags"].append("無 Fwd P/E")
            elif r["fpe_fy2"] <= 0 or r["fpe_fy2"] > 100:
                rec["flags"].append("Fwd P/E {0} 為離群值，不當估值錨".format(r["fpe_fy2"]))
            if r.get("pct_5y") is None:
                rec["flags"].append("無 5Y 分位")
        else:
            rec["flags"].append("不在 dd-screener 母體")
        out.append(rec)
    return out


def priced_block(items):
    lines = []
    for r in items:
        s = "- {0}：".format(r["ticker"])
        if "ret26w_pct" in r:
            s += "26 週 {0:+.1f}%（收盤 {1}，截至 {2}）；".format(r["ret26w_pct"], r["close"], r["as_of"])
        s += "Fwd P/E(FY2) {0}；5Y 分位 {1}".format(r.get("fpe_fy2", "無"), r.get("pct_5y", "無"))
        if r["flags"]:
            s += "　⚠ " + "；".join(r["flags"])
        lines.append(s)
    lines.append("來源：週線 data/weekly_cache、倍數 docs/dd-screener/latest.json。標 ⚠ 的數字不得當承重證據。")
    return "\n".join(lines)


CELL_RE = re.compile(r"^- \('(\w+)', '(\w+)'\)：n=(\d+)(?: ⚠n<10)?｜超額中位 ([+-][\d.]+)%｜勝率 (\d+)/(\d+)", re.M)
VERD_RE = re.compile(r"^- (\w+)：n=(\d+)(?: ⚠n<10)?｜超額中位 ([+-][\d.]+)%｜勝率 (\d+)/(\d+)", re.M)


def base_rate(prior_meta, today_iso):
    """id_autopsy（h91 成熟樣本）→ sd_verdict 與 sd_verdict×clock_phase 命中率。當日快取。"""
    cache = BUILD / "base_rate_{0}.json".format(today_iso)
    if cache.exists():
        data = jload(cache)
    else:
        rc, out = run(["python3.12", ROOT / "knowledge" / "id_autopsy.py"])
        if rc != 0:
            return {"error": out[-300:]}, "（id_autopsy 失敗：{0}）".format(out[-200:])
        m = re.search(r"### sd_verdict × clock_phase（h91）\n(.*?)\n\n", out, re.S)
        v = re.search(r"### sd_verdict（h91）\n(.*?)\n\n", out, re.S)
        data = {"cells": [{"verdict": a, "phase": b, "n": int(n), "median_excess_pct": float(e), "wins": int(w), "of": int(o)}
                          for a, b, n, e, w, o in CELL_RE.findall(m.group(1))] if m else [],
                "verdicts": [{"verdict": a, "n": int(n), "median_excess_pct": float(e), "wins": int(w), "of": int(o)}
                             for a, n, e, w, o in VERD_RE.findall(v.group(1))] if v else [],
                "source": "knowledge/id_autopsy.py，91 天成熟樣本，對基準超額；樣本含 2026-06-21 大批 backfill，非完全獨立"}
        jdump(cache, data)
    pv, pp = prior_meta.get("sd_verdict"), prior_meta.get("clock_phase")
    lines = ["來源：" + data["source"], "各格（sd_verdict × clock_phase）："]
    for c in data["cells"]:
        mark = "　←前版所在格" if (c["verdict"], c["phase"]) == (pv, pp) else ""
        thin = "（n<10，樣本薄）" if c["n"] < 10 else ""
        lines.append("- {0} × {1}：n={2}，超額中位 {3:+.1f}%，勝率 {4}/{5}{6}{7}".format(
            c["verdict"], c["phase"], c["n"], c["median_excess_pct"], c["wins"], c["of"], thin, mark))
    lines.append("規則：若你的裁決落在 shortage × Phase II（或前版在該格），base_rate.required 必須為 true：原文引用該格命中率，"
                 "並用證據包內的具體差異說明這次為何不同；說不出就降級（下調 conviction／改 sd_verdict 或 clock_phase，action=downgraded）。"
                 "其他格 required=false、action=not_applicable。\n若你的裁決格與前版不同：base_rate.differences 須說明換格由哪些證據支持（閘會並排兩格基準率並要求表態），不得因為新格歷史數字較好看而換。")
    return data, "\n".join(lines)


def do_plan(c):
    st = c.begin("plan")
    prior = find_prior(c.theme)
    meta, brief = prior_brief(prior)
    tick = [t["ticker"] for t in meta.get("related_tickers", []) if t.get("depth") in ("🔴", "🟡")][:12]
    pin = priced_inputs(tick, dt.date.fromisoformat(c.iso))
    br, brtext = base_rate(meta, c.iso)
    tax = (ROOT / "docs" / "id" / "taxonomy.md").read_text(encoding="utf-8")
    mm = re.search(r"\|\s*{0}\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|".format(re.escape(c.theme)), tax)
    mega = meta.get("mega") or (mm.group(1) if mm else "")
    sub = meta.get("sub_group") or (mm.group(2) if mm else "")
    sis = find_sisters(c.theme, dict(meta, mega=meta.get("mega") or mega, sub_group=meta.get("sub_group") or sub), tick, c.iso)
    (c.dir / "sisters_block.md").write_text(sisters_block(meta, sis), encoding="utf-8")
    plan = {"theme": c.theme, "sisters_latest": sis, "date": c.iso, "prior_file": prior.name if prior else None, "prior_meta": meta,
            "mega": mega, "sub_group": sub, "tickers": tick, "priced": pin, "base_rate": br,
            "sisters": meta.get("sister_ids", [])}
    jdump(c.dir / "plan.json", plan)
    (c.dir / "prior_brief.md").write_text(brief, encoding="utf-8")
    (c.dir / "priced_block.md").write_text(priced_block(pin), encoding="utf-8")
    (c.dir / "base_rate_block.md").write_text(brtext, encoding="utf-8")
    note = "prior={0} mega={1}.{2} tickers={3} flagged={4}".format(plan["prior_file"], mega, sub, len(tick),
                                                                   sum(1 for r in pin if r["flags"]))
    return c.end("plan", bool(mega and sub), note if mega and sub else "分類缺失：請在 taxonomy.md 登記主題")


# ------------------------------------------------------------------ evidence
def axis_blocks():
    text = (SKILL_DIR / "references" / "research-queries.md").read_text(encoding="utf-8")
    parts = re.split(r"^## (?=Axis [A-E] )", text, flags=re.M)
    blocks = {}
    for p in parts[1:]:
        blocks[p[5]] = "## " + p.split("\n## 回傳格式")[0].strip()
    return blocks


AXIS_EXTRA = {
    "D": "本軸額外要求：①前版 kill 指標逐個查最新現值；②至少找 1 個市場撮合價（現貨價、運價、指數等）並給最新值；③資本週期三指標（capex／折舊、ROIC vs WACC、lead time）至少各嘗試一次；④各核心個股的 Fwd P/E 歷史帶（若查得到一手或可靠來源）。",
    "E": "本軸額外要求：五條機械查詢不得因「顯然無關」跳過；查無實質威脅時也要在 findings 寫一條「已掃描，無一階威脅」並列出所搜詞，不要留白。",
    "B": "本軸額外要求：對關鍵玩家直讀 IR 簡報／10-K／20-F；玩家矩陣數字須有年度或四季加總，禁 Q×4。",
}


def do_evidence(c):
    st = c.begin("evidence")
    plan = jload(c.dir / "plan.json")
    blocks = axis_blocks()
    prior_kills = "\n".join("- " + k.get("metric", "") for k in plan["prior_meta"].get("kill_metrics", [])) or "（無）"
    fdir = BUILD / "facts" / c.theme
    (c.dir / "evidence").mkdir(exist_ok=True)
    (c.dir / "prompts").mkdir(exist_ok=True)
    (c.dir / "agents").mkdir(exist_ok=True)
    specs, reused = [], []
    for ax in AXES:
        part = c.dir / "evidence" / "{0}.json".format(ax)
        cached = fdir / "{0}.json".format(ax)
        if c.a.resume and part.exists():
            reused.append(ax)
            continue
        if not c.a.refresh and cached.exists():
            age = (time.time() - cached.stat().st_mtime) / 86400
            if age <= AXIS_TTL[ax]:
                part.write_text(cached.read_text(encoding="utf-8"), encoding="utf-8")
                reused.append(ax + "(cache {0:.0f}d)".format(age))
                continue
        if part.exists():
            part.unlink()
        pp = c.dir / "prompts" / "evidence_{0}.md".format(ax)
        pp.write_text(render(HERE / "prompts" / "evidence.md.tmpl", {
            "THEME": c.theme, "TODAY": c.iso, "AXIS": ax, "AXIS_BLOCK": blocks[ax], "TICKERS": "、".join(plan["tickers"]),
            "PRIOR_DATE": plan["prior_meta"].get("publish_date", "無"), "PRIOR_KILLS": prior_kills,
            "AXIS_EXTRA": AXIS_EXTRA.get(ax, ""), "MAX_SEARCH": EVID_MAX_SEARCH, "MAX_FETCH": EVID_MAX_FETCH,
            "PART_PATH": str(part)}), encoding="utf-8")
        specs.append({"id": "ev_" + ax, "model": "sonnet", "prompt": str(pp), "out": str(c.dir / "agents" / "ev_{0}.json".format(ax)),
                      "tools": ["WebSearch", "WebFetch", "Write"], "max_turns": EVID_MAX_TURNS, "run_dir": str(c.dir)})
    st["reused"] = reused
    c.save()
    if specs:
        for s, r in zip(specs, dd_headless.spawn_many(specs, max_parallel=5)):
            st["agent_usage"].append(usage(s["id"], enrich(r, s["out"])))
        c.save()
    # 驗收、編號
    merged, dropped, missing = [], 0, []
    for ax in AXES:
        part = c.dir / "evidence" / "{0}.json".format(ax)
        if not part.exists():
            missing.append(ax)
            continue
        try:
            obj = jload(part)
        except Exception:
            obj, _ = sp.strip_json(part.read_text(encoding="utf-8"))
        if not isinstance(obj, dict):
            missing.append(ax)
            continue
        i = 0
        for f in obj.get("findings", []):
            if not (f.get("claim") and re.fullmatch(r"\d{4}(-\d{2}){0,2}", str(f.get("as_of") or "")) and (f.get("url") or f.get("source"))):
                dropped += 1
                continue
            i += 1
            f["id"] = "{0}{1}".format(ax, i)
            f["axis"] = ax
            merged.append(f)
        fdir.mkdir(parents=True, exist_ok=True)
        (fdir / "{0}.json".format(ax)).write_text(part.read_text(encoding="utf-8"), encoding="utf-8")
        for nf in obj.get("not_found", []):
            merged.append({"id": "NF-" + ax, "axis": ax, "claim": "查不到：" + str(nf), "tier": "-", "as_of": "-", "url": None, "not_found": True})
    jdump(c.dir / "evidence.json", merged)
    real = [f for f in merged if not f.get("not_found")]
    t1 = sum(1 for f in real if str(f.get("tier", "")).startswith("T1"))
    st["findings"], st["dropped_undated"], st["t1_share_pct"] = len(real), dropped, round(100 * t1 / max(1, len(real)))
    ok = not missing and len(real) >= 25 and any(f["axis"] == "E" for f in real)
    if ok:
        merged = t1_supplement(c, plan, merged, st)
        real = [f for f in merged if not f.get("not_found") and not f.get("superseded_by")]
        t1 = sum(1 for f in real if str(f.get("tier", "")).startswith("T1"))
        st["findings"], st["t1_share_pct"] = len(real), round(100 * t1 / max(1, len(real)))
        jdump(c.dir / "evidence.json", merged)
    return c.end("evidence", ok, "findings={0} dropped={1} T1={2}% missing_axes={3}".format(len(real), dropped, st["t1_share_pct"], missing))


def t1_floor(mega):
    return 45 if mega in ("macro", "cloud", "space") else 60


def t1_share(ev):
    real = [f for f in ev if not f.get("not_found") and not f.get("superseded_by")]
    return 100 * sum(1 for f in real if str(f.get("tier", "")).startswith("T1")) / max(1, len(real))


def t1_supplement(c, plan, ev, st):
    """T1 占比低於 floor 時補一輪（上限一輪）：只針對 T2/T3 背書的承重數字找一手來源。
    成功的條目以新 id（S1…）加入，原條目標 superseded_by（不再給 judge 看）。"""
    floor = t1_floor(plan["mega"])
    before = t1_share(ev)
    st["t1_before_pct"], st["t1_floor_pct"] = round(before, 1), floor
    if before >= floor:
        st["t1_after_pct"], st["supplement"] = round(before, 1), "skipped（已達 floor）"
        return ev
    # 承重＝有數值的非 T1 條目，A 軸（歷史）優先序最低
    order = {"B": 0, "C": 1, "D": 2, "E": 3, "A": 4}
    cand = sorted([f for f in ev if not f.get("not_found") and not str(f.get("tier", "")).startswith("T1") and f.get("value")],
                  key=lambda f: order.get(f["axis"], 9))[:30]
    targets = "\n".join("[{0}] {1}｜{2}｜現有來源 {3}·{4}｜{5}".format(f["id"], f["claim"], f.get("value"), f.get("source"), f.get("tier"), f.get("as_of")) for f in cand)
    part = c.dir / "evidence" / "supplement.json"
    if part.exists():
        part.unlink()
    pp = c.dir / "prompts" / "supplement.md"
    pp.write_text(render(HERE / "prompts" / "supplement.md.tmpl", {
        "THEME": c.theme, "TODAY": c.iso, "TARGETS": targets, "MAX_SEARCH": 14, "MAX_FETCH": 10, "PART_PATH": str(part)}), encoding="utf-8")
    spec = {"id": "ev_supp", "model": "sonnet", "prompt": str(pp), "out": str(c.dir / "agents" / "ev_supp.json"),
            "tools": ["WebSearch", "WebFetch", "Write"], "max_turns": 28, "run_dir": str(c.dir)}
    r = enrich(dd_headless.spawn_many([spec], max_parallel=1)[0], spec["out"])
    st["agent_usage"].append(usage("ev_supp", r))
    n_up = 0
    if part.exists():
        try:
            obj = jload(part)
        except Exception:
            obj, _ = sp.strip_json(part.read_text(encoding="utf-8"))
        by_id = {f["id"]: f for f in ev}
        for u in (obj or {}).get("upgrades", []) if isinstance(obj, dict) else []:
            o = by_id.get(u.get("replaces"))
            if not (o and str(u.get("tier", "")).startswith("T1") and u.get("url") and
                    re.fullmatch(r"\d{4}(-\d{2}){0,2}", str(u.get("as_of") or "")) and u.get("claim")):
                continue
            n_up += 1
            nid = "S{0}".format(n_up)
            u2 = dict(u, id=nid, axis=o["axis"])
            o["superseded_by"] = nid
            ev.append(u2)
    after = t1_share(ev)
    st["t1_after_pct"], st["supplement"] = round(after, 1), "候選 {0} 條，升級 {1} 條".format(len(cand), n_up)
    print("[evidence] T1 補抓：{0:.1f}% → {1:.1f}%（floor {2}%）".format(before, after, floor))
    return ev


def evidence_text(ev, with_url=False):
    lines = []
    for f in ev:
        if f.get("superseded_by"):
            continue
        if f.get("not_found"):
            lines.append("[{0}] {1}".format(f["id"], f["claim"]))
            continue
        s = "[{0}] {1}｜{2}｜{3}·{4}｜{5}".format(f["id"], f["claim"], f.get("value") or "-", f.get("source") or "-", f.get("tier"), f.get("as_of"))
        if f.get("note"):
            s += "｜註：" + f["note"]
        lines.append(s)
    return "\n".join(lines)


# ------------------------------------------------------------------ judge / gate
def collect_cites(obj, path="", out=None):
    """依文件順序收集 cite／evidence_cite 內的證據編號。"""
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("cite", "evidence_cite") and isinstance(v, list):
                for x in v:
                    out.append((str(x), path.split(".")[0] or k))
            else:
                collect_cites(v, (path + "." + k) if path else k, out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            collect_cites(v, "{0}[{1}]".format(path, i), out)
    return out


def get_path(obj, path):
    cur = obj
    for tok in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        cur = cur[int(tok[1:-1])] if tok.startswith("[") else cur[tok]
    return cur


def set_path(obj, path, value):
    toks = re.findall(r"[^.\[\]]+|\[\d+\]", path)
    cur = obj
    for tok in toks[:-1]:
        cur = cur[int(tok[1:-1])] if tok.startswith("[") else cur[tok]
    last = toks[-1]
    if last.startswith("["):
        cur[int(last[1:-1])] = value
    else:
        cur[last] = value


def stub_validate(j, c):
    """用只含 id-meta 的 stub HTML 跑 validate_id_meta.py（最早的機械閘）。"""
    (c.dir / "stub").mkdir(exist_ok=True)
    stub = c.dir / "stub" / "ID_{0}_{1}.html".format(c.theme, c.date)  # 檔名不是 ID_*.html 會被 validator 當非 ID 跳過
    # 沒有 id-skill-version meta 會被 validator 當非 ID 跳過（2026-10-14 前此閘實際上從未生效）
    stub.write_text('<html><head><meta name="id-skill-version" content="{0}">'
                    '<script id="id-meta" type="application/json">{1}</script></head><body></body></html>'.format(
                        SKILL_VERSION, json.dumps(j.get("id_meta", {}), ensure_ascii=False)), encoding="utf-8")
    rc, out = run(["python3.12", SCRIPTS / "validate_id_meta.py", stub])
    return rc == 0, out[-600:]


def mech_checks(j, ev, plan, c):
    """零 LLM 機械檢查。回 [(severity, id, msg)]。"""
    f = []
    ids = {e["id"] for e in ev if not e.get("not_found")}
    meta = j.get("id_meta", {})
    ok, out = stub_validate(j, c)
    if not ok:
        f.append(("red", "meta", "id-meta 未過 validate_id_meta：" + out.strip().splitlines()[-1] if out.strip() else "validate fail"))
    for cid, sec in collect_cites(j):
        if cid not in ids:
            f.append(("red", "cite", "{0} 段引用不存在的證據編號 {1}".format(sec, cid)))
    deb = j.get("debates", [])
    if not 3 <= len(deb) <= 5:
        f.append(("red", "D7", "分歧卡 {0} 張，需 3–5".format(len(deb))))
    if not any(d.get("external_threat") for d in deb):
        f.append(("red", "D7", "缺替代威脅卡"))
    kt = j.get("risks", {}).get("kill_table", [])
    if len(kt) < 3:
        f.append(("red", "D9", "kill 表 {0} 條，需 ≥3".format(len(kt))))
    if not any(k.get("market_traded") for k in kt):
        f.append(("red", "D9", "kill 表無市場撮合價"))
    if len(kt) != len(meta.get("kill_metrics", [])):
        f.append(("red", "D9", "kill 表 {0} 條與 id_meta.kill_metrics {1} 條不同步".format(len(kt), len(meta.get("kill_metrics", [])))))
    if len(j.get("risks", {}).get("catalysts", [])) < 5:
        f.append(("red", "D10", "催化劑 <5"))
    tam = j.get("mechanics", {}).get("demand", {}).get("tam", {}).get("rows", [])
    try:
        if sum(float(r["weight"]) for r in tam) != 100:
            f.append(("red", "D4", "TAM 三情境權重加總不是 100"))
    except Exception:
        f.append(("red", "D4", "TAM 權重缺或非數字"))
    cc = j.get("mechanics", {}).get("verdict", {}).get("capital_cycle", [])
    if len(cc) < 2:
        f.append(("red", "D2", "資本週期指標 <2"))
    if len(j.get("mechanics", {}).get("verdict", {}).get("gate_sufficient", [])) < 2:
        f.append(("red", "D3", "換相充分條件需兩個獨立訊號"))
    br = j.get("base_rate", {})
    hot = (meta.get("sd_verdict"), meta.get("clock_phase")) == ("shortage", "II")
    prior_hot = (plan["prior_meta"].get("sd_verdict"), plan["prior_meta"].get("clock_phase")) == ("shortage", "II")
    if hot or prior_hot:
        if not br.get("required"):
            f.append(("red", "base_rate", "shortage×Phase II（本次或前版）但 base_rate.required 不是 true"))
        elif br.get("action") == "kept" and not [d for d in br.get("differences", []) if d.get("evidence_cite")]:
            f.append(("red", "base_rate", "維持 shortage×II 但沒有附證據的差異點"))
        elif br.get("action") not in ("kept", "downgraded"):
            f.append(("red", "base_rate", "base_rate.action 需為 kept 或 downgraded"))
    # J2：姊妹報告方向衝突須在頁面調和；sister_ids 須指向最新版
    sis = plan.get("sisters_latest", [])
    rec = {str(x.get("id")): x for x in j.get("thesis", {}).get("sister_reconcile", []) or []}
    for s in sis:
        if s["same_group"] and (s["sd_verdict"], s["clock_phase"]) != (meta.get("sd_verdict"), meta.get("clock_phase")):
            r_ = rec.get(s["file"]) or rec.get(s["slug"])
            if not r_ or not r_.get("reason"):
                f.append(("red", "J2", "與姊妹報告 {0}（{1}／{2}）方向不同，但 thesis.sister_reconcile 沒有調和說明".format(s["file"], s["sd_verdict"], s["clock_phase"])))
    newest = {s["slug"]: s["file"] for s in sis}
    for sid in meta.get("sister_ids", []):
        mm = re.fullmatch(r"ID_(.+)_\d{8}\.html", str(sid))
        if mm and mm.group(1) in newest and newest[mm.group(1)] != sid:
            f.append(("red", "J2", "sister_ids 的 {0} 不是最新版 {1}".format(sid, newest[mm.group(1)])))
    pr = {r["ticker"]: r for r in plan["priced"]}
    for row in j.get("valuation", {}).get("priced_rows", []):
        if row.get("ticker") not in pr:
            f.append(("yellow", "D8", "priced_rows 含程式輸入以外的 {0}".format(row.get("ticker"))))
    if not j.get("valuation", {}).get("priced_rows"):
        f.append(("red", "D8", "priced_rows 為空＝D8 未交"))
    # T1 占比（被引用的來源）
    cited = {x for x, _ in collect_cites(j)}
    tiers = [e.get("tier", "") for e in ev if e["id"] in cited]
    floor = 45 if meta.get("mega") in ("macro", "cloud", "space") else 60
    if tiers and 100 * sum(1 for t in tiers if t.startswith("T1")) / len(tiers) < floor:
        f.append(("red", "T1", "被引用來源 T1 占比 {0:.0f}% 低於 {1}%：承重數字改引證據包內的 T1 條目；沒有 T1 可引就是證據不足，須退回採集".format(
            100 * sum(1 for t in tiers if t.startswith("T1")) / len(tiers), floor)))
    for rt in meta.get("related_tickers", []):
        if rt.get("depth") == "🔴" and (rt.get("purity_pct") is None or not rt.get("mcap_bucket")):
            f.append(("red", "D11", "{0} 為 🔴 但缺 purity_pct 或 mcap_bucket".format(rt.get("ticker"))))
    try:
        if sum(float(h["weight"]) for h in j.get("mechanics", {}).get("verdict", {}).get("horizons", [])) != 100:
            f.append(("red", "D4", "三視野權重（每窗一個數字）加總不是 100"))
    except Exception:
        f.append(("red", "D4", "三視野權重缺或非數字"))
    if len(j.get("valuation", {}).get("derivations", [])) < 2 or not j.get("risks", {}).get("derivation"):
        f.append(("red", "derive", "推導行不足：valuation.derivations 需 ≥2、risks.derivation 需 1"))
    # 多數決：patch 只能在三次判斷出現過的值或前版值（閘判換格證據不足時改回）之間選
    vp = c.dir / "votes.json"
    if vp.exists():
        for fld, vals in (jload(vp).get("runs") or {}).items():
            if meta.get(fld) not in vals and meta.get(fld) != plan["prior_meta"].get(fld):
                f.append(("red", "votes", "{0}={1} 不在三次判斷的結果 {2} 內，也不是前版值".format(fld, meta.get(fld), vals)))
    return f


def normalize_votes(c, j):
    """patch 之後依票數重設 *_boundary／*_gate_reverted（程式擁有，不交給 patch）。
    值在票內：2:1 標交界；值不在票內（閘判換格證據不足、改回前版）：記下三次的票，頁面寫「維持原判」。"""
    vp = c.dir / "votes.json"
    if not vp.exists():
        return
    meta = j.get("id_meta", {})
    for fld, vals in (jload(vp).get("runs") or {}).items():
        meta.pop(fld + "_boundary", None)
        meta.pop(fld + "_gate_reverted", None)
        if meta.get(fld) in vals:
            b = boundary_value(fld, vals)
            if b:
                meta[fld + "_boundary"] = b
        else:
            meta[fld + "_gate_reverted"] = "/".join(vals)


def boundary_notes(meta):
    """id_meta 的 *_boundary／*_gate_reverted → 頁面要寫的白話（例「第二／第三階段交界」）。"""
    out = {}
    for fld, unit, suffix in (("clock_phase", "階段", "階段交界"), ("sd_verdict", "", "交界")):
        b = meta.get(fld + "_boundary")
        if b:
            out[fld] = "／".join(BOUNDARY_ZH.get(x, x) for x in b.split("/")) + suffix
        r = meta.get(fld + "_gate_reverted")
        if r:
            vals = r.split("/")
            top = Counter(vals).most_common(1)[0][0]
            out[fld] = "三次判斷{0}判{1}{2}，換格證據不足，維持原判{3}{2}".format(
                "皆" if len(set(vals)) == 1 else "多數", BOUNDARY_ZH.get(top, top), unit,
                BOUNDARY_ZH.get(meta.get(fld), meta.get(fld)))
    return out


def grid_block(plan, j):
    """裁決格與前版不同時，並排兩格基準率；相同回 None。"""
    pm = plan["prior_meta"]
    pcell = (pm.get("sd_verdict"), pm.get("clock_phase"))
    ncell = (j.get("id_meta", {}).get("sd_verdict"), j.get("id_meta", {}).get("clock_phase"))
    if not pm or pcell == ncell:
        return None
    cells = {(x["verdict"], x["phase"]): x for x in plan["base_rate"].get("cells", [])}

    def fmt(cell):
        x = cells.get(cell)
        if not x:
            return "{0} × {1}：無樣本".format(*cell)
        return "{0} × {1}：n={2}，勝率 {3}/{4}，超額中位 {5:+.1f}%{6}".format(
            cell[0], cell[1], x["n"], x["wins"], x["of"], x["median_excess_pct"], "（n<10，樣本薄）" if x["n"] < 10 else "")
    return "前版格　{0}\n本次格　{1}".format(fmt(pcell), fmt(ncell))


def judge_prompt(c, plan, ev):
    schema = render(HERE / "prompts" / "schema.txt", {"TODAY_ISO": c.iso, "MEGA": plan["mega"], "SUB_GROUP": plan["sub_group"]})
    return render(HERE / "prompts" / "judge.md.tmpl", {
        "THEME": c.theme, "TODAY": c.iso,
        "BASE_RATE_BLOCK": (c.dir / "base_rate_block.md").read_text(encoding="utf-8"),
        "PRICED_BLOCK": (c.dir / "priced_block.md").read_text(encoding="utf-8"),
        "PRIOR_BRIEF": (c.dir / "prior_brief.md").read_text(encoding="utf-8"),
        "PLAYBOOK": (SKILL_DIR / "references" / "judgment-playbook.md").read_text(encoding="utf-8"),
        "SISTERS_BLOCK": (c.dir / "sisters_block.md").read_text(encoding="utf-8"),
        "EVIDENCE": evidence_text(ev), "MEGA": plan["mega"], "SUB_GROUP": plan["sub_group"],
        "TICKERS": "、".join(plan["tickers"]), "SISTERS": "、".join(plan["sisters"]) or "無", "SCHEMA": schema})


def parse_json_result(r):
    if r.get("structured_output"):
        return r["structured_output"], None
    return sp.strip_json(r.get("result_text"))


def boundary_value(field, vals):
    """2:1 時回「多數值/少數值」依自然順序排（例 II/III）；3:0 回 None。"""
    order = PHASE_ORDER if field == "clock_phase" else SD_ORDER
    uniq = sorted(set(vals), key=lambda v: order.get(v, 9))
    return "/".join(uniq) if len(uniq) == 2 else None


def do_judge(c):
    """同 prompt 平行跑 JUDGE_RUNS 次，sd_verdict 與 clock_phase 各取多數；2:1 在 id_meta 加 *_boundary 標記。
    代表判斷＝第一個與兩個多數值都相符的跑次（三取二時必存在）。1:1:1 無多數，停下交人。"""
    st = c.begin("judge")
    plan, ev = jload(c.dir / "plan.json"), jload(c.dir / "evidence.json")
    pp = c.dir / "prompts" / "judge.md"
    pp.write_text(judge_prompt(c, plan, ev), encoding="utf-8")
    ks = list(range(1, JUDGE_RUNS + 1))
    if not c.a.resume:
        for k in ks:
            (c.dir / "judgment_{0}.json".format(k)).unlink(missing_ok=True)
    todo = [k for k in ks if not (c.dir / "judgment_{0}.json".format(k)).exists()]
    st["reused"] = [k for k in ks if k not in todo]

    def one(k):
        return k, sp.oneshot_stream(pp, JUDGE_MODEL, c.dir / "agents" / "judge_{0}.json".format(k), c.dir)

    env_key = sp._MAX_THINKING_TOKENS_ENV  # 平行時由這裡統一設，不讓各執行緒互相還原
    prev = os.environ.get(env_key)
    os.environ[env_key] = str(JUDGE_THINKING_CAP)
    try:
        with ThreadPoolExecutor(max_workers=JUDGE_RUNS) as pool:
            results = list(pool.map(one, todo))
    finally:
        if prev is None:
            os.environ.pop(env_key, None)
        else:
            os.environ[env_key] = prev
    bad = []
    for k, r in results:
        st["agent_usage"].append(usage("judge_{0}".format(k), r))
        obj, err = parse_json_result(r)
        if not isinstance(obj, dict):
            bad.append("judge_{0}：{1}｜{2}".format(k, err, (r.get("stderr_tail") or "")[-150:]))
            continue
        for rt in obj.get("id_meta", {}).get("related_tickers", []):
            for kk in [kk for kk, v in rt.items() if v is None]:
                del rt[kk]  # null 的選填欄（如 🟡 的 purity_pct）會被 validator 當型別錯
        jdump(c.dir / "judgment_{0}.json".format(k), obj)
    c.save()
    if bad:
        return c.end("judge", False, "判斷輸出無法解析（--resume 只重跑失敗的那幾次）：" + "；".join(bad))
    runs = [(k, jload(c.dir / "judgment_{0}.json".format(k))) for k in ks]
    votes = {f: [j.get("id_meta", {}).get(f) for _, j in runs] for f in ("sd_verdict", "clock_phase")}
    major = {}
    for f, vals in votes.items():
        v, n = Counter(vals).most_common(1)[0]
        if n * 2 <= len(vals):
            jdump(c.dir / "votes.json", {"runs": votes, "majority": None})
            return c.end("judge", False, "{0} 三次各異 {1}，無多數，停下交人".format(f, vals))
        major[f] = v
    k0, obj = next((k, j) for k, j in runs if all(j.get("id_meta", {}).get(f) == major[f] for f in major))
    for f, vals in votes.items():
        b = boundary_value(f, vals)
        if b:
            obj["id_meta"][f + "_boundary"] = b
    jdump(c.dir / "votes.json", {"runs": votes, "conviction": [j.get("id_meta", {}).get("conviction") for _, j in runs],
                                 "majority": major, "chosen": k0})
    st["votes"], st["chosen"] = votes, k0
    jdump(c.dir / "judgment.json", obj)
    return c.end("judge", True, "三次 sd={0} phase={1}；取第 {2} 次（sd={3} phase={4}{5}）".format(
        votes["sd_verdict"], votes["clock_phase"], k0, major["sd_verdict"], major["clock_phase"],
        "".join("，{0}={1}".format(f + "_boundary", obj["id_meta"][f + "_boundary"]) for f in votes if obj["id_meta"].get(f + "_boundary"))))


def gate_once(c, plan, ev, j, idx, st):
    mech = mech_checks(j, ev, plan, c)
    mtext = "\n".join("- [{0}] {1}：{2}".format(s, i, m) for s, i, m in mech) or "（機械檢查全過）"
    if boundary_notes(j.get("id_meta", {})):
        mtext += ("\n\n註：id_meta 的 *_boundary 欄是程式依三次獨立判斷 2:1 加的交界標記；*_gate_reverted 欄表示三次判斷的票、"
                  "閘判換格證據不足而改回前版值。兩者都由程式維護，不是錯誤，不要求刪除或改寫。")
    gb = grid_block(plan, j)
    if gb:
        mtext += ("\n\n# 裁決格切換（前版與本次不同格，基準率並排）\n" + gb +
                  "\n你必須在輸出 JSON 另加 \"grid_switch\":{\"justified\":true|false,\"reason\":\"…\"}：換格是否由證據包內的基本面證據支持，"
                  "而不是因為新格的歷史數字比較好看或樣本太薄無從反駁。沒有證據支持＝justified:false。")
    pp = c.dir / "prompts" / "gate_{0}.md".format(idx)
    pp.write_text(render(HERE / "prompts" / "gate.md.tmpl", {
        "MECH": mtext, "PRICED_BLOCK": (c.dir / "priced_block.md").read_text(encoding="utf-8"),
        "BASE_RATE_BLOCK": (c.dir / "base_rate_block.md").read_text(encoding="utf-8"),
        "SISTERS_BLOCK": (c.dir / "sisters_block.md").read_text(encoding="utf-8"),
        "EVIDENCE": evidence_text(ev), "JUDGMENT": json.dumps(j, ensure_ascii=False)}), encoding="utf-8")
    r = sp.oneshot_stream(pp, GATE_MODEL, c.dir / "agents" / "gate_{0}.json".format(idx), c.dir)
    st["agent_usage"].append(usage("gate_{0}".format(idx), r))
    obj, err = parse_json_result(r)
    findings = []
    if isinstance(obj, dict):
        findings = [dict(f) for f in obj.get("findings", [])]
    else:
        findings = [{"id": "gate", "severity": "red", "path": "", "issue": "閘輸出無法解析：{0}".format(err), "fix": "重跑"}]
    for s, i, m in mech:
        findings.append({"id": i, "severity": s, "path": "", "issue": m, "fix": "（機械檢查）"})
    if gb:
        gs = obj.get("grid_switch") if isinstance(obj, dict) else None
        st.setdefault("grid_switch", []).append({"grids": gb, "verdict": gs})
        if not isinstance(gs, dict) or gs.get("justified") is not True:
            findings.append({"id": "grid", "severity": "red", "path": "base_rate", "issue": "裁決格切換未獲證據支持或閘未表態：" + str((gs or {}).get("reason", ""))[:200],
                             "fix": "以證據包內的基本面證據重新論證換格；沒有就改回前版格或降低 conviction"})
    jdump(c.dir / "gate_{0}.json".format(idx), {"findings": findings, "verified": (obj or {}).get("verified_numbers") if isinstance(obj, dict) else None})
    return findings


def do_gate(c):
    st = c.begin("gate")
    plan, ev, j = jload(c.dir / "plan.json"), jload(c.dir / "evidence.json"), jload(c.dir / "judgment.json")
    f1 = gate_once(c, plan, ev, j, 1, st)
    red = [f for f in f1 if f["severity"] == "red"]
    st["round1"] = {"red": len(red), "yellow": len(f1) - len(red)}
    final = f1
    if red:
        pp = c.dir / "prompts" / "patch.md"
        pp.write_text(render(HERE / "prompts" / "patch.md.tmpl", {
            "FINDINGS": "\n".join("- [{0}] {1}｜{2}｜建議：{3}".format(f["id"], f.get("path"), f["issue"], f.get("fix")) for f in red),
            "BASE_RATE_BLOCK": (c.dir / "base_rate_block.md").read_text(encoding="utf-8"),
            "PRICED_BLOCK": (c.dir / "priced_block.md").read_text(encoding="utf-8"),
            "EVIDENCE": evidence_text(ev), "JUDGMENT": json.dumps(j, ensure_ascii=False)}), encoding="utf-8")
        r = sp.oneshot_stream(pp, JUDGE_MODEL, c.dir / "agents" / "patch_1.json", c.dir, thinking_cap=JUDGE_THINKING_CAP)
        st["agent_usage"].append(usage("patch_1", r))
        obj, err = parse_json_result(r)
        applied, failed = 0, []
        for p in (obj or {}).get("patches", []) if isinstance(obj, dict) else []:
            try:
                set_path(j, p["path"], p["value"])
                applied += 1
            except Exception as e:
                failed.append("{0}:{1}".format(p.get("path"), e))
        st["patches_applied"], st["patches_failed"] = applied, failed
        normalize_votes(c, j)
        jdump(c.dir / "judgment.json", j)
        final = gate_once(c, plan, ev, j, 2, st)
    red2 = [f for f in final if f["severity"] == "red"]
    st["final"] = {"red": len(red2), "yellow": len(final) - len(red2)}
    note = "紅 {0} 黃 {1}".format(len(red2), len(final) - len(red2))
    if red2:
        note += "｜仍紅，停下交人：" + "；".join("[{0}] {1}".format(f["id"], f["issue"][:60]) for f in red2[:5])
    return c.end("gate", not red2, note)


# ------------------------------------------------------------------ prose
def prose_view(j, ev):
    """cite → cite_nums；回 (view, sources_table)。"""
    by_id = {e["id"]: e for e in ev}
    order, first_sec = [], {}
    for cid, sec in collect_cites(j):
        if cid in by_id and cid not in first_sec:
            first_sec[cid] = SECTION_ZH.get(sec, sec)
            order.append(cid)
    num = {cid: i + 1 for i, cid in enumerate(order)}
    view = copy.deepcopy(j)

    def conv(o):
        if isinstance(o, dict):
            for k in list(o.keys()):
                if k in ("cite", "evidence_cite") and isinstance(o[k], list):
                    o["cite_nums"] = sorted({num[x] for x in map(str, o.pop(k)) if x in num})
                else:
                    conv(o[k])
        elif isinstance(o, list):
            for v in o:
                conv(v)
    conv(view)
    table = [{"n": num[cid], "section": first_sec[cid], "tier": by_id[cid].get("tier"),
              "title": (by_id[cid].get("source") or by_id[cid].get("url") or "")[:80],
              "url": by_id[cid].get("url"), "as_of": by_id[cid].get("as_of")} for cid in order]
    view["sources_table"] = table
    bn = boundary_notes(j.get("id_meta", {}))
    if bn:
        view["boundary_notes"] = bn
    view["data_window"] = j.get("id_meta", {}).get("publish_date")
    view["n_tickers"] = len(j.get("id_meta", {}).get("related_tickers", []))
    return view, table


def template_parts():
    t = (SKILL_DIR / "templates" / "report_template.md").read_text(encoding="utf-8")
    skel = t.split("```html", 1)[1].split("\n```\n", 1)[0]
    i_a = skel.index("<!-- PAGE 1")
    i_b = skel.index("<!-- 4 · 現在貴不貴")
    i_end = skel.index("</div><!-- /report-sheet -->")
    rules = "## Key Debates 硬規則" + t.split("## Key Debates 硬規則", 1)[1].split("## 站內 nav 注入區塊照抄規則", 1)[0]
    rules += "## 其他硬規則" + t.split("## 其他硬規則", 1)[1]
    rules = re.sub(r"- \*\*篇幅\*\*：.*", "- 篇幅：不設字數目標，HTML ≤55KB 為上界警告。", rules)
    return skel[i_a:i_b], skel[i_b:i_end], rules


def do_prose(c):
    st = c.begin("prose")
    ev, j = jload(c.dir / "evidence.json"), jload(c.dir / "judgment.json")
    view, table = prose_view(j, ev)
    jdump(c.dir / "prose_view.json", view)
    skel_a, skel_b, rules = template_parts()
    zh = (Path.home() / ".claude" / "skills" / "zh-analyst-prose" / "SKILL.md").read_text(encoding="utf-8")
    zh = zh.split("---", 2)[-1]
    halves = {
        "A": ("第一頁決策卡（summary）、導覽列、核心判斷（thesis）、市場哪裡看錯（debates）、機制與供需（mechanics，含 3.1–3.4）。"
              "從 `<header id=\"summary\"` 起寫到 mechanics 的 `</section>`；導覽列 `<nav class=\"toc-bar\">` 放在 header 之後。", skel_a),
        "B": ("現在貴不貴（valuation）、我怎麼知道我錯了（risks）、誰受影響（stocks）、附錄（appendix，含來源總表 src-table，列由 JSON 的 sources_table 逐列渲染）、"
              "結尾 pull-quote、「刻意不做的三件事」、Disclosures、colophon（版本號 {0}）、back-top。從 `<section id=\"valuation\"` 起寫到檔尾。".format(SKILL_VERSION), skel_b)}
    specs = []
    for k, (desc, skel) in halves.items():
        out = c.dir / "prose_{0}.html".format(k)
        if out.exists():
            out.unlink()
        pp = c.dir / "prompts" / "prose_{0}.md".format(k)
        pp.write_text(render(HERE / "prompts" / "prose.md.tmpl", {
            "HALF_DESC": desc, "OUT_PATH": str(out), "ZH_STYLE": zh, "SRC_NOTE": "共 {0} 筆來源，列於 sources_table。".format(len(table)),
            "SKELETON": skel, "RULES": rules, "JUDGMENT": json.dumps(view, ensure_ascii=False)}), encoding="utf-8")
        specs.append({"id": "prose_" + k, "model": PROSE_MODEL, "prompt": str(pp), "out": str(c.dir / "agents" / "prose_{0}.json".format(k)),
                      "tools": ["Write"], "max_turns": 4, "run_dir": str(c.dir)})
    for s, r in zip(specs, dd_headless.spawn_many(specs, max_parallel=2)):
        st["agent_usage"].append(usage(s["id"], enrich(r, s["out"])))
    miss = [k for k in halves if not (c.dir / "prose_{0}.html".format(k)).exists()]
    return c.end("prose", not miss, "缺 " + ",".join(miss) if miss else "兩半皆交")


def assemble(c, j):
    from site_nav import full_nav_block
    meta = j["id_meta"]
    ttl = j.get("title", {})
    a = (c.dir / "prose_A.html").read_text(encoding="utf-8")
    b = (c.dir / "prose_B.html").read_text(encoding="utf-8")
    head = ('<!DOCTYPE html>\n<html lang="zh-Hant">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<meta name="robots" content="noindex,nofollow">\n'
            '<meta name="color-scheme" content="only light">\n<title>{t} — {g} | InvestMQuest</title>\n'
            '<meta name="id-skill-version" content="{v}">\n<meta name="id-theme" content="{th}">\n<meta name="id-publish-date" content="{d}">\n'
            '<meta name="id-pipeline" content="id2">\n<script id="id-meta" type="application/json">\n{m}\n</script>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Noto+Serif+TC:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">\n'
            '<link rel="stylesheet" href="../assets/id-v4.css">\n</head>\n<body id="top">\n').format(
        t=meta.get("theme"), g=ttl.get("tagline", ""), v=meta["skill_version"], th=meta.get("theme"), d=meta["publish_date"],
        m=json.dumps(meta, ensure_ascii=False, indent=2))
    html = (head + full_nav_block("research", "id") + '\n<div class="report-sheet">\n' + a + "\n" + b +
            '\n</div><!-- /report-sheet -->\n\n<a class="back-top" href="#top">↑ TOP</a>\n\n</body>\n</html>\n')
    out = c.dir / "ID_{0}_{1}.html".format(c.theme, c.date)
    out.write_text(html, encoding="utf-8")
    return out


NUM_RE = re.compile(r"\d[\d,]*\.?\d*")


def number_audit(html_path, j):
    """表格與正文的數字若不在判斷 JSON 全文裡，列為疑似新增（警告，不擋）。"""
    corpus = json.dumps(j, ensure_ascii=False)
    corpus_nums = {n.rstrip(".").replace(",", "") for n in NUM_RE.findall(corpus)}
    body = re.sub(r"<script.*?</script>|<style.*?</style>|<header class=\"imq-nav-root\".*?</header>", "", html_path.read_text(encoding="utf-8"), flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    text = re.sub(r"［#[\d, ]+］", " ", text)
    extra = sorted({n.rstrip(".").replace(",", "") for n in NUM_RE.findall(text)
                    if len(n.rstrip(".").replace(",", "")) >= 2} - corpus_nums)
    return [n for n in extra if not re.fullmatch(r"20\d\d|\d{1,2}", n)]


def do_check(c):
    st = c.begin("check")
    j = jload(c.dir / "judgment.json")
    out = assemble(c, j)
    rep, exc = c.dir / "check_report.md", c.dir / "check_excerpt.md"
    rc1, o1 = run(["python3.12", SCRIPTS / "check_id.py", out, "--report", rep, "--excerpt", exc])
    rc2, o2 = run(["python3.12", SCRIPTS / "validate_id_meta.py", out])
    extra = number_audit(out, j)
    kb = out.stat().st_size / 1024
    html = out.read_text(encoding="utf-8")
    miss_b = [t for t in boundary_notes(j.get("id_meta", {})).values() if t not in html]
    st.update({"check_id_rc": rc1, "validate_rc": rc2, "html_kb": round(kb, 1), "numbers_not_in_judgment": extra[:40],
               "numbers_not_in_judgment_n": len(extra), "boundary_missing": miss_b})
    (c.dir / "check_stdout.txt").write_text(o1 + "\n---\n" + o2, encoding="utf-8")
    return c.end("check", rc1 == 0 and rc2 == 0 and not miss_b, "check_id rc={0} validate rc={1} {2:.0f}KB 疑似新增數字 {3} 個{4}".format(
        rc1, rc2, kb, len(extra), "｜頁面缺交界字樣：" + "、".join(miss_b) if miss_b else ""))


# ------------------------------------------------------------------ publish（只在 --publish；本階段未實跑）
def do_publish(c):
    st = c.begin("publish")
    j = jload(c.dir / "judgment.json")
    src = c.dir / "ID_{0}_{1}.html".format(c.theme, c.date)
    dst = ROOT / "docs" / "id" / src.name
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    m = j["id_meta"]
    row = "| {d} | {t} 🆕 id2 {v} | {n} | {r}🔴 / {y}🟡 / {g}🟢 | Phase {p} | — | tech:{d} 🟢 ｜ market:{d} 🟢 ｜ judgment:{d} 🟢 | {f} | id2 管線 |\n".format(
        d=c.iso, t=m.get("theme"), v=SKILL_VERSION, n=len(m.get("related_tickers", [])),
        r=sum(1 for t in m["related_tickers"] if t.get("depth") == "🔴"), y=sum(1 for t in m["related_tickers"] if t.get("depth") == "🟡"),
        g=sum(1 for t in m["related_tickers"] if t.get("depth") == "🟢"), p=m.get("clock_phase"), f=dst.name)
    with open(ROOT / "docs" / "id" / "INDEX.md", "a", encoding="utf-8") as fh:
        fh.write(row)
    log = []
    for cmd in (["build_id_category_pages.py"], ["id_dd_mapping.py"], ["retrofit_dd_id_banner.py"],
                ["check_tier_matrix.py", "--inject-html"], ["inject_report_primer.py", "--family", "id"], ["qc.py"]):
        if (SCRIPTS / cmd[0]).exists():
            rc, o = run(["python3.12", SCRIPTS / cmd[0]] + cmd[1:])
            log.append("{0}: rc={1}".format(cmd[0], rc))
    log.append("TODO 手動：docs/id/index.html 插卡片（找 subgroup-anchor）；id2 尚未自動化")
    return c.end("publish", True, "\n".join(log))


# ------------------------------------------------------------------ main
def report(c):
    tot_cost = tot_out = 0
    print("\n== id2 {0} {1} ==".format(c.theme, c.date))
    for name in STAGES:
        st = c.m["stages"].get(name)
        if not st:
            continue
        cost = sum((u.get("cost_usd") or 0) for u in st["agent_usage"])
        outt = sum((u.get("output_tokens") or 0) for u in st["agent_usage"])
        cr = sum((u.get("cache_read") or 0) for u in st["agent_usage"])
        ms = max([(u.get("duration_ms") or 0) for u in st["agent_usage"]] or [0])
        tot_cost += cost
        tot_out += outt
        print("{0:9s} {1:5s} agents={2} cost=${3:.2f} out={4:,} cache_read={5:,} 最長單通={6:.1f}分".format(
            name, st["state"], len(st["agent_usage"]), cost, outt, cr, ms / 60000))
    print("合計 cost=${0:.2f} output_tokens={1:,}".format(tot_cost, tot_out))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("theme")
    ap.add_argument("--date")
    ap.add_argument("--until", choices=STAGES)
    ap.add_argument("--resume", action="store_true", help="跳過已 PASS 的段；evidence 沿用 run dir 內已交的軸")
    ap.add_argument("--refresh", action="store_true", help="忽略跨 run 證據快取")
    ap.add_argument("--dry-run", action="store_true", help="預設即 dry run：只寫 .id_build/，與不帶旗標相同")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--ignore-gate-red", action="store_true", help="僅供除錯：gate 已 FAIL 時不重閘、繼續 prose／check；產物不得發布")
    a = ap.parse_args(argv)
    c = Ctx(a)
    fns = {"plan": do_plan, "evidence": do_evidence, "judge": do_judge, "gate": do_gate, "prose": do_prose, "check": do_check}
    last = a.until or ("publish" if a.publish else "check")
    if a.publish and a.ignore_gate_red:
        sys.exit("--publish 與 --ignore-gate-red 不可併用")
    for name in STAGES:
        if name == "publish" and not a.publish:
            break
        if a.ignore_gate_red and name == "gate" and c.m["stages"].get("gate", {}).get("state") == "FAIL":
            c.m["gate_red_ignored"] = True
            c.save()
            print("[gate] 仍紅但 --ignore-gate-red：繼續（除錯用，產物不得發布）")
        elif a.resume and c.passed(name):
            print("[{0}] 已 PASS，跳過".format(name))
        elif not fns.get(name, do_publish)(c):
            report(c)
            return 1
        if name == last:
            break
    report(c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
