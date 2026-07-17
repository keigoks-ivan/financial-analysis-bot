#!/usr/bin/env python3
"""
rule_audit.py — rule_ledger 判斷類規則的預審計 joiner（2026-10 校準要直接貼的素材）。

把 rule_ledger.md 的審計方法（「grep 報告中的規則觸發標記 × settlement forward
return」）機械化成可重跑的 joiner：對每條「判斷類規則」偵測它在 DD 報告中的**觸發**，
接上 settlement.json 的 forward return，讓校準時能一眼看到「規則觸發的那批裁決，後來
報酬如何」——KEEP / TIGHTEN|LOOSEN / KILL 的證據。

覆蓋分三級（誠實優先，寧可標 manual 也不弱 pattern 亂命中——誤 join 比漏 join 毒）：
  - mechanical：dd-meta 結構化欄位的確定性判定（零誤判，如估值燈基線 / Hard Veto）。
  - partial：dd-meta 欄位代理（只抓得到規則的可觀測分支）或本文 fired-state regex
            （抽樣驗過），命中為真觸發子集，非全集。
  - manual：觸發標記不在 DD 掃描範圍（ID/macro/detective/GRP/supply-chain/synthesis
           等其他檔族或引擎碼），或屬 always-on 鷹架（每份報告都在、無法辨別是否 fired）
           → 交人判，本 joiner 不臆測。

輸出 knowledge/rule_audit.json（衍生物，gitignore，本地重算）。
  --report  印 markdown 審計預覽表（每規則一行：觸發數 / 成熟樣本 / mean to_date / 備註空白留人判）。

staleness：比照 q.py——decisions.jsonl / settlement.json 過期就先 subprocess 重跑
build_knowledge.py / settle_outcomes.py，再讀。不改動 settlement 的任何結算邏輯。
"""
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

KDIR = Path(__file__).resolve().parent
ROOT = KDIR.parent
DD_DIR = ROOT / "docs" / "dd"
LEDGER = KDIR / "rule_ledger.md"
DECISIONS = KDIR / "decisions.jsonl"
SETTLE = KDIR / "settlement.json"
CACHE_DIR = ROOT / "data" / "weekly_cache"
BUILD = KDIR / "build_knowledge.py"
SETTLE_BUILD = KDIR / "settle_outcomes.py"
OUT = KDIR / "rule_audit.json"

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL
)
MATURE_DAYS = 28  # README 讀數紀律：聚合只取結算齡 ≥ 28 天樣本


# ── staleness gate（比照 q.py，衍生物過期先 rebuild）───────────────────────────
def _ensure_derivatives():
    if not DECISIONS.exists():
        subprocess.run([sys.executable, str(BUILD)], check=True)
    try:
        stale = not SETTLE.exists()
        if not stale:
            t = SETTLE.stat().st_mtime
            if DECISIONS.exists() and t < DECISIONS.stat().st_mtime:
                stale = True
            elif CACHE_DIR.exists():
                with os.scandir(CACHE_DIR) as it:
                    stale = any(
                        e.stat().st_mtime > t for e in it if e.name.endswith(".json")
                    )
        if stale:
            subprocess.run([sys.executable, str(SETTLE_BUILD)], check=True)
    except Exception as e:  # cache 缺漏等，降級為無結算（不擋審計）
        print(f"（結算重算跳過：{e}）", file=sys.stderr)


def _load_settlement():
    if not SETTLE.exists():
        return {}, None
    data = json.loads(SETTLE.read_text(encoding="utf-8"))
    return {r["id"]: r for r in data.get("rows", [])}, data.get("as_of")


def _dd_meta(text):
    m = DD_META_RE.search(text)
    if not m:
        return None
    try:
        return json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        return None


def _load_dd_corpus():
    """回傳 [(decision_id, meta, body)] for 每份 v13/v14 DD（有 dd-meta 者）。
    decision_id = f'{ticker}-{date_no_dash}'，與 build_knowledge.py:157 / decisions.jsonl
    的 id 建構完全一致（同一 ticker+date 空間，故不需檔名還原 → 免踩 2308TW/2308/2345.TW
    三種檔名慣例）。"""
    corpus = []
    if not DD_DIR.exists():
        return corpus
    for path in sorted(DD_DIR.glob("DD_*.html")):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        meta = _dd_meta(text)
        if not meta or not str(meta.get("schema", "")).startswith(("v13", "v14")):
            continue
        tk, d = meta.get("ticker"), meta.get("date")
        if not (tk and d):
            continue
        did = f"{tk}-{d.replace('-', '')}"
        corpus.append((did, meta, text, path.name))
    return corpus


# ── 觸發偵測器（detector）─────────────────────────────────────────────────────
# 每個 detector: fn(meta, body) -> bool。設計原則見檔頭。命中皆抽樣驗過（見 __doc__）。
def _d_hard_veto(m, b):
    # §14 row 1-3 Hard Veto：X 訊號 or moat↓+≤B → 迴避。取「迴避 且 (X | moat↓)」為
    # 確定性可觀測分支（矛盾未解分支無結構化欄位，故整體標 mechanical 但屬 veto 已 fired）。
    return m.get("dca_verdict") == "迴避" and (
        m.get("signal") == "X"
        or (m.get("moat_trend") == "↓" and m.get("signal") in ("B", "C", "X"))
    )


def _d_val_baseline(m, b):
    # §14 row 8 估值燈基線：val ∈ {🟠,🔴} 且裁決落 觀望（估值紀律實際 bind 的樣本）。
    return m.get("val") in ("🟠", "🔴") and m.get("dca_verdict") == "觀望"


def _d_soft_veto(m, b):
    # §14 row 6/7 Soft Veto 可觀測分支：C 訊號 or runway🔴 且 ≥觀望。
    # 7a「估值依賴」分支非結構化欄位 → partial（命中為子集）。
    return m.get("dca_verdict") in ("觀望", "迴避") and (
        m.get("signal") == "C" or m.get("runway_post_y5") == "🔴"
    )


def _d_cyclical_gate(m, b):
    # row 8b 循環衛星五閘 / QC-42：cycle_position 有值 ＝ 循環鏡頭實際 engage。
    # partial：engage ≠「五閘擋下」，只標記循環軌被評估的樣本。
    return bool(m.get("cycle_position"))


def _d_qc42_antimomentum(m, b):
    # QC-42 反動能硬閘：晚循環最相關（禁 blow-off 新建）。partial 子集。
    return m.get("cycle_position") == "晚循環"


# 本文 fired-state regex（排除「不觸發／不滿足／失效」的否定敘事）
_RE_BLIND1_FIRED = re.compile(r"盲點 ?1[^。<]{0,60}?救[起滿]")
_RE_BLIND3_FIRED = re.compile(r"盲點 ?3 上修救援[：:][^。]{0,80}?(?<!不)觸發")
# QC-50 fired = 「採納…錯過成本反向 critic…升級」（EAT 型真升級）；排除「§14 未升級」
# 「對…critic 的正面回應」等否定/中性敘事（抽樣驗過：2454 的「未升級」不誤中）。
_RE_QC50_FIRED = re.compile(r"採納[^。]{0,20}錯過成本反向 ?critic[^。]{0,40}升級")


def _d_blind1(m, b):
    return bool(_RE_BLIND1_FIRED.search(b))


def _d_blind3(m, b):
    return bool(_RE_BLIND3_FIRED.search(b))


def _d_qc50(m, b):
    return bool(_RE_QC50_FIRED.search(b))


# ── 規則 → 覆蓋規格（sig 子字串匹配 ledger 第一欄）────────────────────────────
# detector 存在 = mechanical/partial；否則 manual + 明確理由（觸發標記不在 DD 掃描範圍）。
# 每條 spec: (sig, coverage, detector_or_None, note)
SPECS = [
    ("Hard Veto", "mechanical", _d_hard_veto,
     "迴避 且 (signal=X ∨ moat↓+≤B)；矛盾未解分支無欄位、以裁決結果為錨"),
    ("row 6/7/7a Soft Veto", "partial", _d_soft_veto,
     "C 訊號 ∨ runway🔴 且 ≥觀望；估值依賴(7a)分支無結構化欄位，命中為子集"),
    ("row 8 估值燈基線", "mechanical", _d_val_baseline,
     "val∈{🟠,🔴} 且裁決=觀望（估值紀律實際 bind 的樣本）"),
    ("估值燈盲點 1 救援", "partial", _d_blind1,
     "本文 fired-state regex（排除失效/不觸發敘事）；救援極少 fire"),
    ("估值燈盲點 3 上修救援", "partial", _d_blind3,
     "本文 fired-state regex（排除不觸發/不滿足）；救援極少 fire"),
    ("row 8a", "manual", None,
     "26 週漲幅位置閘的 fired-state 無乾淨結構化欄位（pct_5y 是 5Y 分位非 26W）→ 交人判"),
    ("row 8b 循環衛星五閘", "partial", _d_cyclical_gate,
     "cycle_position 有值＝循環鏡頭 engage；≠「五閘擋下」，標記受評樣本"),
    ("反偏差防線", "manual", None,
     "機率地板每份都套、是否 bind 不可觀測 → 交人判"),
    ("QC-48 爆發候選冷讀", "manual", None,
     "corpus 內 QC-48 全為『不觸發/非強制觸發』（downgrade-only 從未 fire），無正例可校準"
     " fired-regex、否定敘事又會誤中 → 交人判（0-fire 本身即審計訊號：kill 條件『兩輪 0 觸發』）"),
    ("QC-49 裁決 hysteresis", "manual", None,
     "90 天翻面 fired-state 敘事幾乎全為「非翻面/方向一致」否定式，正向 fire 難乾淨辨別 → 交人判"),
    ("QC-50 錯過成本反向 critic", "partial", _d_qc50,
     "本文 fired regex：反向 critic 實際促成升級/改判進場"),
    ("QC-51 同形狀 peer", "manual", None,
     "跨報告 peer 一致性對帳非單檔 fired，DD 掃描抓不到跨檔事件 → 交人判"),
    ("QC-42 反動能硬閘", "partial", _d_qc42_antimomentum,
     "cycle_position=晚循環（反動能最相關分支）；partial 子集"),
    ("GRP R 閘", "manual", None,
     "觸發在 scripts/engine/grp.py，不在 DD → GRP 季檢 owner 對帳"),
    ("GRP G 閘", "manual", None,
     "觸發在 scripts/engine/grp.py，不在 DD → GRP 季檢 owner 對帳"),
    ("GRP P 閘", "manual", None,
     "觸發在 scripts/engine/grp.py，不在 DD → GRP 季檢 owner 對帳"),
    ("ID conviction pill", "manual", None,
     "觸發標記在 docs/id/ID_*.html（industry-analyst），非 DD → ID 校準輪對帳"),
    ("ID QC-6", "manual", None,
     "ID 來源占比在 id-meta / ID 報告，非 DD → ID 校準輪"),
    ("ID sd_verdict", "manual", None,
     "ID 裁決欄在 id-meta，非 DD → ID 校準輪"),
    ("ID priced_in", "manual", None,
     "ID priced_in 欄在 id-meta，非 DD → ID 校準輪"),
    ("QC-52 DD↔ID 對帳", "manual", None,
     "fired=DD/ID 分歧事件，需跨檔比對 sd_verdict，非單檔可判 → 交人判"),
    ("v14.9 判斷反萃取三件套", "manual", None,
     "§12.4b/§13b'/§11 為 always-on 鷹架，每份都在、是否改變裁決不可從 HTML 辨別 → 交人判"),
    ("QC-53 DD 情境判斷手冊", "manual", None,
     "情境手冊為觸發索引式鷹架，逐條 fired 不落 HTML → 交人逐條審"),
    ("ID 情境判斷手冊", "manual", None,
     "industry-analyst 手冊，觸發在 ID 寫稿流程非 DD → ID 校準輪"),
    ("id-review V2-12", "manual", None,
     "id-review critic 的 finding 記在 notes/site-internal/id/，非 DD → critic 記錄對帳"),
    ("對比判斷手冊", "manual", None,
     "multi-stock-comparator 手冊，觸發在 docs/comparisons/ → 對比校準"),
    ("供應鏈瓶頸兩層制", "manual", None,
     "觸發在 docs/supply-chain/ sidecar 與 hub，非 DD → 供應鏈複審"),
    ("macro §0 stance", "manual", None,
     "觸發在 docs/macro/MACRO_*.html，非 DD → macro 校準輪"),
    ("macro-analyst skill 本體", "manual", None,
     "tool-level 使用 kill（90 天引用），非單檔 fired → 引用實績對帳"),
    ("宏觀投資時鐘機械層", "manual", None,
     "觸發在 build_macro_clock.py / regime 頁，非 DD → 時鐘季檢"),
    ("synthesis 退出分軌", "manual", None,
     "觸發在 docs/research/synthesis/，非 DD → synthesis 校準帳本"),
    ("priced_in=high 上行閘", "manual", None,
     "expectations-synthesis Step 4，觸發在 synthesis 報告非 DD → synthesis 校準"),
    ("賣方料等級聲明", "manual", None,
     "synthesis §6 權重欄，觸發在 synthesis 報告非 DD → synthesis 校準"),
    ("衛星席時機路由", "manual", None,
     "觸發在 /cockpit/ 陣容表與 cyclical-track，非 DD → 衛星席季檢"),
    ("正不對稱三級標記", "manual", None,
     "build_dd_screener.py 現價驅動注入 /research/＋/dd-screener/，非 DD 本文 → screener 對帳"),
    ("R1", "manual", None, "detective_rules.py 複合規則，觸發在 docs/detective/ → detective 審計"),
    ("R2", "manual", None, "detective_rules.py 複合規則，觸發在 docs/detective/ → detective 審計"),
    ("R3", "manual", None, "detective_rules.py 複合規則，觸發在 docs/detective/ → detective 審計"),
    ("R4", "manual", None, "detective_rules.py 複合規則，觸發在 docs/detective/ → detective 審計"),
    ("R5", "manual", None, "detective_rules.py 複合規則，觸發在 docs/detective/ → detective 審計"),
    ("R6", "manual", None, "detective_rules.py 複合規則，觸發在 docs/detective/ → detective 審計"),
    ("R7", "manual", None, "detective_rules.py 複合規則，觸發在 docs/detective/ → detective 審計"),
    ("R8", "manual", None, "detective_rules.py 複合規則，觸發在 docs/detective/ → detective 審計"),
    ("R9", "manual", None, "detective_rules.py 複合規則，觸發在 docs/detective/ → detective 審計"),
]


def _match_spec(rule_name):
    for sig, cov, det, note in SPECS:
        if sig in rule_name:
            return sig, cov, det, note
    return None, "manual", None, "未匹配任何 detector 規格 → 預設交人判（新規則？補 SPECS）"


# ── 解析 rule_ledger.md 第一張表 ──────────────────────────────────────────────
def parse_ledger():
    """抽第一張表（| 規則 | 生日 | … |）全部資料列。容忍 <br>/粗體/長文。"""
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    rules, in_tbl, seen_header = [], False, False
    for ln in lines:
        s = ln.strip()
        if s.startswith("|") and "規則" in s and "生日" in s:
            in_tbl, seen_header = True, True
            continue
        if in_tbl:
            if not s.startswith("|"):
                break  # 第一張表結束（遇空行/散文）
            if set(s) <= set("|-: "):
                continue  # 分隔列
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) < 2:
                continue
            name = re.sub(r"<[^>]+>", "", cells[0])  # 去 <br>/<strong>
            name = re.sub(r"\*\*", "", name).strip()
            rules.append({"name": name, "birth": cells[1] if len(cells) > 1 else ""})
    if not seen_header:
        raise SystemExit("rule_ledger.md 第一張表頭未找到（格式變了？）")
    return rules


# ── join ─────────────────────────────────────────────────────────────────────
def _returns(srow):
    if not srow:
        return None
    return {
        "h30": srow.get("h30"),
        "h91": srow.get("h91"),
        "h182": srow.get("h182"),
        "h365": srow.get("h365"),
        "to_date_pct": srow.get("to_date_pct"),
        "days": srow.get("days"),
    }


def audit():
    rules = parse_ledger()
    corpus = _load_dd_corpus()
    settle_map, settle_as_of = _load_settlement()

    out_rules = []
    for r in rules:
        name = r["name"]
        sig, cov, det, note = _match_spec(name)
        hits = []
        if det is not None:
            for did, meta, body, fname in corpus:
                try:
                    fired = det(meta, body)
                except Exception:
                    fired = False
                if fired:
                    srow = settle_map.get(did)
                    hits.append({
                        "decision_id": did,
                        "ticker": meta.get("ticker"),
                        "date": meta.get("date"),
                        "verdict": meta.get("dca_verdict"),
                        "grade": meta.get("signal"),
                        "report": fname,
                        "returns": _returns(srow),
                    })
        settled = [h for h in hits if h["returns"] and h["returns"]["to_date_pct"] is not None]
        matured = [h for h in settled if (h["returns"]["days"] or 0) >= MATURE_DAYS]
        # mean to_date 取全部已結算命中（to_date 對所有齡都有定義）；成熟數(≥28天)另列為
        # 信任指標。corpus 年輕時 matured 可能為 0，但仍給得出方向性均值供人判。
        td = [h["returns"]["to_date_pct"] for h in settled]
        td_mat = [h["returns"]["to_date_pct"] for h in matured]
        h91_mat = sum(1 for h in hits if h["returns"] and h["returns"]["h91"] is not None)
        immature = None
        if hits and not matured:
            immature = f"{len(settled)}/{len(hits)} 已結算但全部齡 < {MATURE_DAYS} 天，量級待成熟（方向可讀）"
        elif hits and len(matured) < len(settled):
            immature = f"{len(matured)}/{len(settled)} 已結算命中成熟（≥{MATURE_DAYS} 天）"
        out_rules.append({
            "rule": name,
            "birth": r["birth"],
            "coverage": cov,
            "sig": sig,
            "detector_note": note,
            "trigger_count": len(hits),
            "settled_count": len(settled),
            "matured_count": len(matured),
            "h91_matured": h91_mat,
            "mean_to_date_pct": round(sum(td) / len(td), 2) if td else None,
            "mean_to_date_matured_pct": round(sum(td_mat) / len(td_mat), 2) if td_mat else None,
            "immature_note": immature,
            "hits": hits,
        })
    return {
        "schema": "rule-audit-v1",
        "as_of": date.today().isoformat(),
        "settlement_as_of": settle_as_of,
        "dd_corpus_n": len(corpus),
        "coverage_summary": _cov_summary(out_rules),
        "mature_days": MATURE_DAYS,
        "note": "audit 欄留空給人判；mechanical/partial 命中為觸發子集（見 detector_note），"
                "manual=觸發標記不在 DD 掃描範圍。量級慎讀（各視窗不等長、corpus 年輕）。",
        "rules": out_rules,
    }


def _cov_summary(rows):
    c = {"mechanical": 0, "partial": 0, "manual": 0}
    for r in rows:
        c[r["coverage"]] = c.get(r["coverage"], 0) + 1
    return c


# ── report（markdown 審計預覽）────────────────────────────────────────────────
def print_report(data):
    cs = data["coverage_summary"]
    print(f"# rule_audit 預審計預覽（as_of {data['as_of']}）\n")
    print(f"- DD corpus（v13/v14 有 dd-meta）：{data['dd_corpus_n']} 份　"
          f"settlement as_of：{data['settlement_as_of']}")
    print(f"- 覆蓋：mechanical {cs['mechanical']}　partial {cs['partial']}　"
          f"manual {cs['manual']}（共 {sum(cs.values())} 條判斷類規則）")
    print(f"- 成熟樣本 = 結算齡 ≥ {data['mature_days']} 天；mean to_date 取全部已結算命中"
          f"（v13/v14 決策層 2026-06-22 才起跑，成熟數常為 0 屬正常，方向可讀量級慎讀）\n")
    print("| 規則 | 覆蓋 | 觸發數 | 已結算 | 成熟數 | h91到期 | mean to_date% | 2026-10 審計 |")
    print("|---|---|---|---|---|---|---|---|")
    for r in sorted(data["rules"], key=lambda x: (-x["trigger_count"], x["coverage"])):
        nm = r["rule"]
        nm = (nm[:34] + "…") if len(nm) > 35 else nm
        mtd = "—" if r["mean_to_date_pct"] is None else f"{r['mean_to_date_pct']:+.1f}"
        tc = r["trigger_count"] if r["coverage"] != "manual" else "—(手判)"
        sc = r["settled_count"] if r["coverage"] != "manual" else "—"
        print(f"| {nm} | {r['coverage']} | {tc} | {sc} | {r['matured_count']} | "
              f"{r['h91_matured']} | {mtd} | |")
    print("\n> manual 規則觸發標記不在 DD 掃描範圍（見 rule_audit.json detector_note），"
          "由對應檔族/引擎 owner 於各自校準輪對帳。")


def main():
    _ensure_derivatives()
    data = audit()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    cs = data["coverage_summary"]
    print(f"rule_audit.json：{sum(cs.values())} 條規則（mechanical {cs['mechanical']} / "
          f"partial {cs['partial']} / manual {cs['manual']}），"
          f"DD corpus {data['dd_corpus_n']} 份，settlement as_of {data['settlement_as_of']}")
    if "--report" in sys.argv:
        print()
        print_report(data)


if __name__ == "__main__":
    main()
