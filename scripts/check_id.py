#!/usr/bin/env python3
"""check_id.py — industry-analyst v4 機械 pre-publish gate（單一 script 版）。

把 .claude/skills/industry-analyst/pre_publish_check.md 的 16 道人工 gate 中
能用程式驗的部分收斂成一支 stdlib-only script。相容 v4（八段機器錨點 +
kill-table / data-field 燈號 / data-window / src-table）與 v3.0 舊標記
（.debate-card / .judgment-card / .evidence-fold / .src-list .tier）。

只用 Python 標準庫，相容 Python 3.9（禁 match、禁 `X | Y` 型別、禁 f-string
內同種引號巢狀）。

Usage:
  python3 scripts/check_id.py <html> [--t1-floor N] [--report out.md]
                               [--excerpt out.md] [--json]

Exit 0 = 無 FAIL；有任一 FAIL exit 1。
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ANCHORS = ["summary", "thesis", "debates", "mechanics", "valuation",
           "risks", "stocks", "appendix"]

PASS, WARN, FAIL, SKIP = "PASS", "WARN", "FAIL", "SKIP"

FOLD_RE = re.compile(
    r'<details\b[^>]*\bclass="[^"]*\bevidence-fold\b[^"]*"[^>]*>.*?</details>',
    re.DOTALL)
SRC_TABLE_RE = re.compile(
    r'<table\b[^>]*\bclass="[^"]*\bsrc-table\b[^"]*"[^>]*>.*?</table>',
    re.DOTALL)
KILL_TABLE_RE = re.compile(
    r'<table\b[^>]*\bclass="[^"]*\bkill-table\b[^"]*"[^>]*>.*?</table>',
    re.DOTALL)
DEBATE_CARD_RE = re.compile(r'class="[^"]*\bdebate-card\b[^"]*"')
JUDGMENT_CARD_RE = re.compile(r'class="[^"]*\bjudgment-card\b[^"]*"')
EXTERNAL_THREAT_RE = re.compile(r'data-debate="external-threat"')
TABLE_RE = re.compile(r'<table\b[^>]*>.*?</table>', re.DOTALL)
TABLE_CAP = 12  # v4：必交物 D2/D4/D5/D8/D9/D11/D12 合計需 ~11 張分析表；來源總表不計

TR_RE = re.compile(r'<tr\b[^>]*>.*?</tr>', re.DOTALL)
TD_RE = re.compile(r'<t[hd]\b[^>]*>(.*?)</t[hd]>', re.DOTALL)
TBODY_RE = re.compile(r'<tbody\b[^>]*>(.*?)</tbody>', re.DOTALL)
THEAD_RE = re.compile(r'<thead\b[^>]*>(.*?)</thead>', re.DOTALL)
SPAN_TIER_RE = re.compile(
    r'<span class="tier">\[(T3\.5-zh|T1-zh|T2-zh|T3-zh|T3-[ABC]|T1|T2|T4)\]</span>')
TIER_TOKEN_RE = re.compile(r'T3\.5-zh|T1-zh|T2-zh|T3-zh|T3-[ABC]|T1|T2|T4')

LEAK_PATTERNS = [
    r'\[F:', r'\[I:', r'\[X:', r'\[A:', r'\[T[1-4]', r'NC#', r'AT_RISK',
    r'INTACT', r'QC-', r'Gate ', r'skill_version', r'sub_group[:：]',
    r'Method[:：]', r'本版補齊', r'呈現版',
]

QUANT_PAT = re.compile(
    r'\$\s?\d|\d+(\.\d+)?\s?%|\d+\s?(GW|TW|MW|B|T)\b|\d+(\.\d+)?\s?(倍|x|×)|'
    r'\d+(\.\d+)?\s?(GB|TB|MAU|DAU|億|萬|nm)')
YEAR_PAT = re.compile(r'\b(19|20)\d{2}\b')

FIELD_NAMES = ["sd_verdict", "clock_phase", "conviction", "priced_in",
               "demand_5y_multiple"]
LIGHT_TAG_RE = re.compile(
    r'<[a-zA-Z][^>]*\bdata-field="(' + '|'.join(FIELD_NAMES) + r')"[^>]*>')
DATA_VALUE_RE = re.compile(r'data-value="([^"]*)"')
DATA_WINDOW_RE = re.compile(
    r'<span\b[^>]*\bclass="[^"]*\bdata-window\b[^"]*"[^>]*>')
DATA_ASOF_RE = re.compile(r'data-asof="([^"]*)"')

WEIGHT_HEADER_RE = re.compile(r'權重')
NUM_RE = re.compile(r'-?\d+(?:\.\d+)?')


# --------------------------------------------------------------------------
# generic helpers
# --------------------------------------------------------------------------

def strip_noise(html):
    """Remove <script>, <style>, HTML comments — not part of 可見文字。"""
    out = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    out = re.sub(r'<style\b[^>]*>.*?</style>', '', out, flags=re.DOTALL)
    out = re.sub(r'<!--.*?-->', '', out, flags=re.DOTALL)
    return out


def strip_tags(text):
    return re.sub(r'<[^>]+>', '', text)


def visible_chars(text):
    """去 tag 後、去空白後的可見字元數（沿用全站既有 gate 慣例）。"""
    return re.sub(r'\s+', '', strip_tags(text))


def exclude_spans(text, *regexes):
    """從 text 移除所有 regex 命中的區塊（用於「主閱讀線＝不含折疊」）。"""
    spans = []
    for rgx in regexes:
        for m in rgx.finditer(text):
            spans.append((m.start(), m.end()))
    if not spans:
        return text
    spans.sort()
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    out = []
    prev = 0
    for s, e in merged:
        out.append(text[prev:s])
        prev = e
    out.append(text[prev:])
    return ''.join(out)


def get_segments(clean_html):
    """回傳 (positions dict, ordered_found list, segments dict)。"""
    positions = {}
    for a in ANCHORS:
        m = re.search(r'id="%s"' % re.escape(a), clean_html)
        if m:
            positions[a] = m.start()
    ordered = sorted(positions.items(), key=lambda kv: kv[1])
    segments = {}
    for i, (a, p) in enumerate(ordered):
        end = ordered[i + 1][1] if i + 1 < len(ordered) else len(clean_html)
        segments[a] = clean_html[p:end]
    return positions, ordered, segments


def table_rows(table_html):
    """資料列數（優先取 tbody；否則整表 tr 數扣掉 thead tr 數，至少 0）。"""
    tb = TBODY_RE.search(table_html)
    if tb:
        return len(TR_RE.findall(tb.group(1)))
    th = THEAD_RE.search(table_html)
    thead_rows = len(TR_RE.findall(th.group(1))) if th else 1
    total = len(TR_RE.findall(table_html))
    return max(0, total - thead_rows)


def find_owning_segment(pos, ordered):
    """給一個位移，回傳它落在哪個已找到的 anchor 段（用於分派表格）。"""
    owner = None
    for a, p in ordered:
        if p <= pos:
            owner = a
        else:
            break
    return owner


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def check_filename(html_path):
    base = os.path.basename(html_path)
    m = re.match(r'^ID_(.+)_(\d{8})\.html$', base)
    note = []
    status = PASS
    if not m:
        status = FAIL
        note.append("檔名不符 ID_{Theme}_{YYYYMMDD}.html：%s" % base)
    else:
        date_str = m.group(2)
        try:
            datetime.datetime.strptime(date_str, "%Y%m%d")
        except ValueError:
            status = FAIL
            note.append("日期非法：%s" % date_str)
    full_sibling = os.path.join(os.path.dirname(os.path.abspath(html_path)),
                                 base.replace(".html", "_full.html"))
    if os.path.exists(full_sibling):
        status = FAIL
        note.append("同目錄存在禁產的 _full.html：%s" % full_sibling)
    return {"check": "1. 檔名格式", "status": status, "value": base,
            "note": "；".join(note) if note else "OK"}


def check_id_meta_validate(html_path):
    validator = os.path.join(ROOT, "scripts", "validate_id_meta.py")
    try:
        proc = subprocess.run(
            [sys.executable, validator, html_path],
            capture_output=True, text=True, timeout=60)
    except Exception as e:
        return {"check": "2. id-meta 驗證", "status": FAIL,
                "value": "subprocess error", "note": str(e)}
    status = PASS if proc.returncode == 0 else FAIL
    out = (proc.stdout + proc.stderr).strip()
    note = "exit 0" if status == PASS else out[-500:]
    return {"check": "2. id-meta 驗證", "status": status,
            "value": "exit %d" % proc.returncode, "note": note}


def check_anchors(positions, ordered):
    missing = [a for a in ANCHORS if a not in positions]
    if missing:
        return {"check": "3. 八段錨點", "status": FAIL,
                "value": "%d/8" % (8 - len(missing)),
                "note": "缺：%s" % ", ".join(missing)}
    in_order = [p for _, p in ordered]
    is_sorted = all(in_order[i] < in_order[i + 1]
                     for i in range(len(in_order) - 1))
    # ordered 已按位置排序；比對其 anchor 名稱順序是否等於 canonical 順序
    canonical_order = [a for a, _ in ordered]
    if canonical_order != ANCHORS or not is_sorted:
        return {"check": "3. 八段錨點", "status": FAIL, "value": "8/8",
                "note": "順序錯誤，實際順序：%s" % ", ".join(canonical_order)}
    return {"check": "3. 八段錨點", "status": PASS, "value": "8/8", "note": "OK"}


def check_tables(clean_html, ordered):
    # 來源總表（.src-table）是來源清單不是分析表，不計入上限
    tables = [(m.start(), m.group(0)) for m in TABLE_RE.finditer(clean_html)
              if 'src-table' not in m.group(0)[:200]]
    count = len(tables)
    over = []
    for pos, t in tables:
        owner = find_owning_segment(pos, ordered)
        cap = 16 if owner == "stocks" else 8
        rows = table_rows(t)
        if rows > cap:
            over.append("%s 段表格 %d 列 > cap %d" % (owner or "?", rows, cap))
    status = PASS
    notes = []
    if count > TABLE_CAP:
        status = FAIL
        notes.append("表格總數 %d > %d（不含來源總表）" % (count, TABLE_CAP))
    if over:
        if status != FAIL:
            status = WARN
        notes.append("；".join(over))
    return {"check": "4. 表格數與列數", "status": status,
            "value": "%d 張表" % count,
            "note": "；".join(notes) if notes else "OK"}


def check_debates(segments):
    body = segments.get("debates", "")
    cards = len(DEBATE_CARD_RE.findall(body))
    ext = len(EXTERNAL_THREAT_RE.findall(body))
    status = PASS
    notes = []
    if not (3 <= cards <= 5):
        status = FAIL
        notes.append("debate-card %d 張，需 3–5" % cards)
    if ext < 1:
        status = FAIL
        notes.append("external-threat 卡 %d 張，需 ≥1" % ext)
    return {"check": "5. 分歧卡", "status": status,
            "value": "%d 張（威脅 %d）" % (cards, ext),
            "note": "；".join(notes) if notes else "OK"}


def check_judgment_card(clean_html):
    n = len(JUDGMENT_CARD_RE.findall(clean_html))
    status = PASS if n == 1 else FAIL
    return {"check": "6. PM 行動框", "status": status, "value": str(n),
            "note": "OK" if status == PASS else "需恰 1 個（v3.0 可能落在 thesis 段一併照數）"}


KILL_COLS = ["指標", "現值", "熊線", "來源/頻率", "領先幾季", "可否操縱", "破線後姿態"]


def check_kill_table(clean_html, segments, meta):
    is_v4 = bool(KILL_TABLE_RE.search(clean_html))
    table_html = None
    mode = None
    if is_v4:
        m = KILL_TABLE_RE.search(clean_html)
        table_html = m.group(0)
        mode = "v4"
    else:
        risks = segments.get("risks", "")
        m = TABLE_RE.search(risks)
        if m:
            table_html = m.group(0)
            mode = "v3.0（risks 段第一張表）"

    if table_html is None:
        return {"check": "7. kill 表", "status": FAIL, "value": "0 列",
                "note": "找不到 kill 表（v4 需 class=kill-table；v3.0 需 risks 段內至少一張表）"}

    rows_html = []
    tb = TBODY_RE.search(table_html)
    body_html = tb.group(1) if tb else table_html
    for trm in TR_RE.finditer(body_html):
        rows_html.append(trm.group(0))
    n_rows = len(rows_html)

    status = PASS
    notes = []
    if n_rows < 3:
        status = FAIL
        notes.append("資料列 %d < 3" % n_rows)

    if mode == "v4":
        empty_rows = []
        for i, tr in enumerate(rows_html):
            cells = [strip_tags(c).strip() for c in TD_RE.findall(tr)]
            val = cells[1] if len(cells) > 1 else ""
            if not val or val == "—":
                empty_rows.append(i + 1)
        if empty_rows:
            status = FAIL
            notes.append("第 %s 列現值欄空白或僅「—」" %
                          ", ".join(str(x) for x in empty_rows))

    km = meta.get("kill_metrics")
    km = km if isinstance(km, list) else []
    if len(km) != n_rows:
        status = FAIL
        notes.append("id-meta kill_metrics %d 條 != 表 %d 列" % (len(km), n_rows))

    table_plain = re.sub(r'\s+', '', strip_tags(table_html))
    unmatched = []
    for k in km:
        metric = k.get("metric", "") if isinstance(k, dict) else ""
        prefix = re.sub(r'\s+', '', str(metric))[:6]
        if prefix and prefix not in table_plain:
            unmatched.append(metric)
    if unmatched:
        if status not in (FAIL,):
            status = WARN
        notes.append("metric 對不上表列前 6 字：%s" % "；".join(unmatched))

    return {"check": "7. kill 表", "status": status,
            "value": "%d 列 / %s / kill_metrics %d 條" % (n_rows, mode, len(km)),
            "note": "；".join(notes) if notes else "OK"}


def _norm(v):
    return str(v).strip() if v is not None else ""


def check_lights(clean_html, meta):
    hits = {}
    for tm in LIGHT_TAG_RE.finditer(clean_html):
        tag = tm.group(0)
        field = tm.group(1)
        vm = DATA_VALUE_RE.search(tag)
        hits[field] = vm.group(1) if vm else ""
    if not hits:
        return {"check": "8. 燈號五格", "status": SKIP, "value": "0/5",
                "note": "v3.0 無 data-field 標記，SKIP"}
    mismatches = []
    for field, val in hits.items():
        meta_val = meta.get(field)
        if field == "demand_5y_multiple":
            nums = NUM_RE.findall(val)
            ok = False
            if nums and isinstance(meta_val, (int, float)):
                try:
                    ok = abs(float(nums[0]) - float(meta_val)) < 0.05 * max(1.0, abs(float(meta_val))) + 0.05
                except ValueError:
                    ok = False
            if not ok:
                mismatches.append("%s: data-value=%r vs id-meta=%r" % (field, val, meta_val))
        else:
            if _norm(val) != _norm(meta_val):
                mismatches.append("%s: data-value=%r vs id-meta=%r" % (field, val, meta_val))
    status = FAIL if mismatches else PASS
    return {"check": "8. 燈號五格", "status": status,
            "value": "%d/5 標記" % len(hits),
            "note": "；".join(mismatches) if mismatches else "OK"}


def check_data_window(clean_html):
    m = DATA_WINDOW_RE.search(clean_html)
    if not m:
        return {"check": "9. 資料窗", "status": SKIP, "value": "無標記",
                "note": "v3.0 無 data-window 標記，SKIP"}
    tag = m.group(0)
    am = DATA_ASOF_RE.search(tag)
    if not am:
        return {"check": "9. 資料窗", "status": FAIL, "value": "缺 data-asof",
                "note": "data-window 存在但無 data-asof 屬性"}
    asof = am.group(1)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', asof):
        return {"check": "9. 資料窗", "status": FAIL, "value": asof,
                "note": "日期格式非 YYYY-MM-DD"}
    try:
        datetime.datetime.strptime(asof, "%Y-%m-%d")
    except ValueError:
        return {"check": "9. 資料窗", "status": FAIL, "value": asof,
                "note": "非合法日期"}
    return {"check": "9. 資料窗", "status": PASS, "value": asof, "note": "OK"}


def check_t1_ratio(clean_html, meta, t1_floor_override):
    if t1_floor_override is not None:
        floor = t1_floor_override
    else:
        mega = meta.get("mega")
        floor = 45 if mega in ("macro", "cloud", "space") else 60

    src_tables = SRC_TABLE_RE.findall(clean_html)
    tiers = []
    if src_tables:
        for st in src_tables:
            for trm in TR_RE.finditer(st):
                cells = TD_RE.findall(trm.group(0))
                if len(cells) >= 3:
                    cell_text = strip_tags(cells[2])
                    tm = TIER_TOKEN_RE.search(cell_text)
                    if tm:
                        tiers.append(tm.group(0))
    else:
        tiers = SPAN_TIER_RE.findall(clean_html)

    total = len(tiers)
    t1 = sum(1 for t in tiers if t in ("T1", "T1-zh"))
    ratio = (t1 / total * 100) if total else 0.0

    if total == 0:
        return {"check": "10. T1 占比", "status": FAIL, "value": "0 條來源",
                "note": "無任何來源條目"}
    status = PASS if ratio >= floor else FAIL
    return {"check": "10. T1 占比", "status": status,
            "value": "%.1f%%（floor %d%%，共 %d 條）" % (ratio, floor, total),
            "note": "OK" if status == PASS else "低於 floor"}


def check_derive_lines(segments):
    fail_secs = []
    warn_secs = []
    counts = {}
    for name in ("mechanics", "valuation", "risks", "stocks"):
        body = segments.get(name, "")
        n = len(re.findall(r'推導[：:]', body))
        counts[name] = n
        if name in ("mechanics", "valuation") and n < 2:
            fail_secs.append("%s(%d<2)" % (name, n))
        if name in ("risks", "stocks") and n < 1:
            warn_secs.append("%s(%d<1)" % (name, n))
    status = PASS
    notes = []
    if fail_secs:
        status = FAIL
        notes.append("推導行不足（FAIL）：%s" % ", ".join(fail_secs))
    if warn_secs:
        if status != FAIL:
            status = WARN
        notes.append("推導行不足（WARN）：%s" % ", ".join(warn_secs))
    value = ", ".join("%s=%d" % (k, v) for k, v in counts.items())
    return {"check": "11. 推導行", "status": status, "value": value,
            "note": "；".join(notes) if notes else "OK"}


def check_appendix_history(segments):
    body = segments.get("appendix", "")
    if not body:
        return {"check": "12. 附錄歷史錨點", "status": WARN, "value": "0 段",
                "note": "appendix 段不存在，無法檢查"}
    # 排除表格與 aside（來源表通常不是 <p>，這裡先把 table/aside 挖掉再抓 <p>）
    scrub = re.sub(r'<table\b[^>]*>.*?</table>', '', body, flags=re.DOTALL)
    scrub = re.sub(r'<aside\b[^>]*>.*?</aside>', '', scrub, flags=re.DOTALL)
    paras = re.findall(r'<p\b([^>]*)>(.*?)</p>', scrub, re.DOTALL)
    year_paras = []
    for attrs, inner in paras:
        if 'lede' in attrs:
            continue
        txt = strip_tags(inner)
        if YEAR_PAT.search(txt):
            year_paras.append(txt)
    qualifying = [t for t in year_paras if QUANT_PAT.search(t)]
    status = PASS if len(qualifying) >= 2 else WARN
    return {"check": "12. 附錄歷史錨點", "status": status,
            "value": "%d/%d 段含年份+量化" % (len(qualifying), len(year_paras)),
            "note": "OK" if status == PASS else "含年份段落中同時含量化錨點的 < 2 段"}


def check_scenario_weights(clean_html):
    tables = TABLE_RE.findall(clean_html)
    # 只認表頭（thead 或第一列）含「權重」的表
    candidates = []
    for t in tables:
        head_m = THEAD_RE.search(t)
        head_text = head_m.group(1) if head_m else (TR_RE.findall(t)[0] if TR_RE.findall(t) else "")
        if WEIGHT_HEADER_RE.search(head_text):
            candidates.append((t, head_text))
    if not candidates:
        return {"check": "13. 情境權重", "status": SKIP, "value": "無權重欄",
                "note": "SKIP（無表格含「權重」欄）"}
    problems = []
    for idx, (t, head_text) in enumerate(candidates):
        header_cells = [strip_tags(c).strip() for c in TD_RE.findall(head_text)]
        col_idx = None
        for i, c in enumerate(header_cells):
            if "權重" in c:
                col_idx = i
                break
        if col_idx is None:
            continue
        tb = TBODY_RE.search(t)
        body_html = tb.group(1) if tb else t
        vals = []
        for trm in TR_RE.finditer(body_html):
            cells = [strip_tags(c).strip() for c in TD_RE.findall(trm.group(0))]
            if col_idx < len(cells):
                nums = NUM_RE.findall(cells[col_idx])
                if nums:
                    v = float(nums[0])
                    if 0 < v <= 1:
                        v *= 100
                    vals.append(v)
        if not vals:
            continue
        total = sum(vals)
        not_mult5 = [v for v in vals if abs(v - round(v / 5) * 5) > 1e-6]
        if abs(total - 100) > 1 or not_mult5:
            problems.append("表%d：總和%.1f（need 100±1），非5倍數：%s" %
                             (idx + 1, total, not_mult5 if not_mult5 else "無"))
    status = FAIL if problems else PASS
    return {"check": "13. 情境權重", "status": status,
            "value": "%d 張含權重欄的表" % len(candidates),
            "note": "；".join(problems) if problems else "OK"}


def check_leaks(clean_html):
    main_text = exclude_spans(clean_html, FOLD_RE, SRC_TABLE_RE)
    hits = []
    for pat in LEAK_PATTERNS:
        for m in re.finditer(pat, main_text):
            start = max(0, m.start() - 15)
            snippet = main_text[start:m.start() + 15]
            snippet = re.sub(r'\s+', ' ', strip_tags(snippet)).strip()
            hits.append((pat, snippet))
    status = FAIL if hits else PASS
    shown = hits[:10]
    note = "OK" if not hits else ("；".join(
        "%s: %s" % (p, s[:30]) for p, s in shown))
    return {"check": "14. 流程劇場外漏", "status": status,
            "value": "%d 處" % len(hits), "note": note}


def build_main_reading_by_segment(segments):
    result = {}
    for name in ANCHORS:
        body = segments.get(name, "")
        main = exclude_spans(body, FOLD_RE, SRC_TABLE_RE)
        result[name] = visible_chars(main)
    return result


def check_length(html_path, clean_html, main_reading):
    total_chars = sum(len(v) for v in main_reading.values())
    byte_size = os.path.getsize(html_path)
    css_external = bool(re.search(r'<link[^>]*id-v4\.css[^>]*>', clean_html))
    threshold = 55000 if css_external else 70000

    notes = []
    status = PASS
    if not (11000 <= total_chars <= 14000):
        status = WARN
        notes.append("主閱讀線可見字 %d 不在 11,000–14,000" % total_chars)
    if byte_size > threshold:
        status = WARN
        notes.append("HTML %d bytes > 上限 %d（%s）" %
                      (byte_size, threshold,
                       "外掛 CSS" if css_external else "inline CSS"))
    return {"check": "15. 篇幅", "status": status,
            "value": "%d 可見字 / %d bytes" % (total_chars, byte_size),
            "note": "；".join(notes) if notes else "OK"}


def print_section_breakdown(segments, clean_html, ordered, main_reading):
    tables_by_seg = {}
    for m in TABLE_RE.finditer(clean_html):
        owner = find_owning_segment(m.start(), ordered)
        tables_by_seg[owner] = tables_by_seg.get(owner, 0) + 1
    print()
    print("段落統計：")
    print("| 段 | 位元組 | 可見字（主閱讀線） | 表格數 |")
    print("|---|---:|---:|---:|")
    for name in ANCHORS:
        body = segments.get(name, "")
        print("| %s | %d | %d | %d |" %
              (name, len(body.encode("utf-8")), len(main_reading.get(name, "")),
               tables_by_seg.get(name, 0)))


EXSRC_RE = re.compile(r'<p\b[^>]*\bclass="[^"]*\bexhibit-source\b[^"]*"[^>]*>.*?</p>', re.S | re.I)


def check_dup_scan(main_reading, segments):
    """重複掃描：主閱讀線再剔除 exhibit-source 樣板行（「資料來源：…整理」屬合法重複，非復述）。"""
    WINDOW = 12
    shingle_locations = {}
    total_windows = 0
    dup_text = {}
    for name in ANCHORS:
        body = segments.get(name, "")
        if not body:
            continue
        stripped = exclude_spans(body, FOLD_RE, SRC_TABLE_RE, EXSRC_RE)
        dup_text[name] = visible_chars(stripped)
    main_reading = dup_text
    for name, text in main_reading.items():
        n = len(text)
        if n < WINDOW:
            continue
        for i in range(n - WINDOW + 1):
            s = text[i:i + WINDOW]
            shingle_locations.setdefault(s, []).append((name, i))
            total_windows += 1

    dup_instances = 0
    dup_groups = []
    for s, locs in shingle_locations.items():
        segs = set(n for n, _ in locs)
        if len(locs) >= 2 and len(segs) >= 2:
            dup_instances += len(locs)
            dup_groups.append((s, locs))

    ratio = (dup_instances / total_windows * 100) if total_windows else 0.0
    status = WARN if ratio > 8.0 else PASS
    notes = []
    dup_groups.sort(key=lambda g: len(g[1]), reverse=True)
    for s, locs in dup_groups[:5]:
        seg0, off0 = locs[0]
        src = main_reading[seg0]
        snippet = src[off0:off0 + 24]
        seg_names = sorted(set(n for n, _ in locs))
        notes.append("「%s」x%d @ %s" % (snippet, len(locs), ", ".join(seg_names)))
    return {"check": "16. 重複掃描", "status": status,
            "value": "%.1f%%（%d/%d windows）" % (ratio, dup_instances, total_windows),
            "note": "；".join(notes) if notes else "OK"}


def check_qc(html_path):
    qc_script = os.path.join(ROOT, "scripts", "qc.py")
    try:
        proc = subprocess.run(
            [sys.executable, qc_script, html_path],
            capture_output=True, text=True, timeout=120)
    except Exception as e:
        return {"check": "17. 全形標點(qc.py)", "status": WARN,
                "value": "subprocess error", "note": str(e)}
    status = PASS if proc.returncode == 0 else WARN
    out = (proc.stdout + proc.stderr).strip()
    return {"check": "17. 全形標點(qc.py)", "status": status,
            "value": "exit %d" % proc.returncode,
            "note": "OK" if status == PASS else out[-500:]}


# --------------------------------------------------------------------------
# excerpt
# --------------------------------------------------------------------------

def html_fragment_to_text(fragment):
    frag = exclude_spans(fragment, FOLD_RE, SRC_TABLE_RE)

    def table_repl(m):
        t = m.group(0)
        lines = []
        for trm in TR_RE.finditer(t):
            cells = TD_RE.findall(trm.group(0))
            cell_text = [re.sub(r'\s+', ' ', strip_tags(c)).strip() for c in cells]
            lines.append(" | ".join(cell_text))
        return "\n" + "\n".join(lines) + "\n"

    frag = TABLE_RE.sub(table_repl, frag)

    def make_head_repl(level):
        hashes = "#" * level

        def _r(m):
            text = re.sub(r'\s+', ' ', strip_tags(m.group(1))).strip()
            return "\n\n" + hashes + " " + text + "\n"
        return _r

    for lvl, tag in ((1, "h1"), (2, "h2"), (3, "h3"), (4, "h4")):
        frag = re.sub(r'<%s\b[^>]*>(.*?)</%s>' % (tag, tag),
                       make_head_repl(lvl), frag, flags=re.DOTALL)

    frag = re.sub(r'</(p|li|div|section|header|blockquote|tr)>', '\n', frag)
    frag = re.sub(r'<br\s*/?>', '\n', frag)
    frag = strip_tags(frag)
    frag = re.sub(r'[ \t]+', ' ', frag)
    frag = re.sub(r'\n{3,}', '\n\n', frag)
    return frag.strip()


def build_excerpt(segments, meta_raw):
    parts = []
    for name in ("summary", "thesis", "debates"):
        body = segments.get(name, "")
        if body:
            parts.append("## [%s]\n\n%s" % (name, html_fragment_to_text(body)))

    mech = segments.get("mechanics", "")
    if mech:
        h3s = list(re.finditer(r'<h3\b[^>]*>(.*?)</h3>', mech, re.DOTALL))
        verdict_start = None
        for hm in h3s:
            if "裁決" in strip_tags(hm.group(1)):
                verdict_start = hm.start()
                break
        if verdict_start is not None:
            mech_excerpt = mech[verdict_start:]
        else:
            mech_excerpt = mech[int(len(mech) * 0.6):]
        parts.append("## [mechanics 裁決小節]\n\n%s" % html_fragment_to_text(mech_excerpt))

    for name in ("valuation", "risks", "stocks"):
        body = segments.get(name, "")
        if body:
            parts.append("## [%s]\n\n%s" % (name, html_fragment_to_text(body)))

    if meta_raw:
        parts.append("## [id-meta]\n\n```json\n%s\n```" % meta_raw)

    return "\n\n".join(parts)


# --------------------------------------------------------------------------
# report rendering
# --------------------------------------------------------------------------

def render_markdown_table(rows):
    lines = ["| 檢查項 | 結果 | 數值 | 說明 |", "|---|---|---|---|"]
    for r in rows:
        note = r["note"].replace("\n", " ").replace("|", "\\|")
        value = str(r["value"]).replace("\n", " ").replace("|", "\\|")
        lines.append("| %s | %s | %s | %s |" % (r["check"], r["status"], value, note))
    return "\n".join(lines)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", help="path to ID_{Theme}_{YYYYMMDD}.html")
    ap.add_argument("--t1-floor", type=int, default=None)
    ap.add_argument("--report", default=None, help="write markdown table to this path")
    ap.add_argument("--excerpt", default=None, help="write critic excerpt to this path")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.html):
        print("ERROR: file not found: %s" % args.html, file=sys.stderr)
        sys.exit(2)

    raw_html = open(args.html, encoding="utf-8", errors="ignore").read()
    clean_html = strip_noise(raw_html)

    meta_raw = ""
    meta = {}
    mm = re.search(r'<script\s+id="id-meta"[^>]*>(.*?)</script>', raw_html, re.DOTALL)
    if mm:
        meta_raw = mm.group(1).strip()
        try:
            meta = json.loads(meta_raw)
        except json.JSONDecodeError:
            meta = {}

    positions, ordered, segments = get_segments(clean_html)
    main_reading = build_main_reading_by_segment(segments)

    rows = []
    rows.append(check_filename(args.html))
    rows.append(check_id_meta_validate(args.html))
    rows.append(check_anchors(positions, ordered))
    rows.append(check_tables(clean_html, ordered))
    rows.append(check_debates(segments))
    rows.append(check_judgment_card(clean_html))
    rows.append(check_kill_table(clean_html, segments, meta))
    rows.append(check_lights(clean_html, meta))
    rows.append(check_data_window(clean_html))
    rows.append(check_t1_ratio(clean_html, meta, args.t1_floor))
    rows.append(check_derive_lines(segments))
    rows.append(check_appendix_history(segments))
    rows.append(check_scenario_weights(clean_html))
    rows.append(check_leaks(clean_html))
    rows.append(check_length(args.html, clean_html, main_reading))
    rows.append(check_dup_scan(main_reading, segments))
    rows.append(check_qc(args.html))

    if args.excerpt:
        excerpt_text = build_excerpt(segments, meta_raw)
        with open(args.excerpt, "w", encoding="utf-8") as f:
            f.write(excerpt_text)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write("# check_id.py 報告 — %s\n\n" % os.path.basename(args.html))
            f.write(render_markdown_table(rows))
            f.write("\n")

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(render_markdown_table(rows))
        print_section_breakdown(segments, clean_html, ordered, main_reading)

    any_fail = any(r["status"] == FAIL for r in rows)
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
