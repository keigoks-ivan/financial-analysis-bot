#!/usr/bin/env python3
"""check_moat_review.py {TICKER} — 護城河三題檔的機械把關閘（照
.claude/skills/moat-review/SKILL.md v2.0 第 4 步「把關」）。

驗 docs/stock-dash/data/moat/{T}.json 的 current（moat-v3 schema）：
  0. schema=="moat-v3"；status∈{初出,已重出}
  1. current.one_liner_zh 非空
  2. current.questions 恰 3 題，每題四樣東西齊（q_zh／why_zh／evidence／lean／
     lean_reason_zh／watch）
  3. 每條 evidence 要有 text_zh，且 date 非空或 text_zh 含「未能確認」
  4. lean ∈ {撐住,鬆動,不明}
  5. 每題 watch ≥1 條，且每條有 desc_zh，並且 metric_key 非空或 manual=True
     （事件型條件標「需人工」）
  6. 禁止買賣指令字眼（買進／賣出／加碼／減碼／建議持有）——只查本系統／模型
     自己撰寫的欄位（one_liner_zh／vs_prior_zh／每題 q_zh／why_zh／
     lean_reason_zh／evidence[].text_zh／watch[].desc_zh），不查 legacy_scores
     ／rivals（引用來源，不是本系統判斷）
  7. 正文不可出現「DD」字樣，也不可出現 current.rivals 清單裡任一個對手
     ticker——SKILL 明講「正文不列對手名字」，只放收合區
  8. 全形標點（中文字後面接半形 , . : 視為缺失，僅警告不擋）
  9. 追蹤條件機械規則（v2.1，watch_rule_errors）：metric_key 要在清單裡、綁欄位就要
     有數字門檻、單季／財測口徑不能綁近四季或年度共識欄位、分項營收不能綁總營收、
     門檻不能只寫「顯著」「大幅」這類字

回非零＝不能上頁（頁面應該顯示上一版）。純 stdlib，不用網路。

Usage:
    python3 scripts/check_moat_review.py NVDA
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOAT_DIR = ROOT / "docs" / "stock-dash" / "data" / "moat"

BANNED_PHRASES = ["買進", "賣出", "加碼", "減碼", "建議持有", "建議買進", "建議賣出"]
VALID_STATUS = {"初出", "已重出"}
VALID_LEAN = {"撐住", "鬆動", "不明"}

HALFWIDTH_PUNCT_RE = re.compile(r'[一-鿿][,.:](?!\d)')

# 可追蹤的機械欄位與口徑（SKILL v2.1）。出題 prompt 從這裡列給 sonnet，build_stock_dash.py
# 的 METRIC_KEY_RESOLVERS 要有同一組 key。口徑寫清楚，是為了擋「拿單季財測門檻去追近四季累計」。
KNOWN_METRIC_KEYS = {
    "roic_ltm_pct": "ROIC，近四季",
    "roic_3y_avg_pct": "ROIC，三年平均",
    "roic_5y_avg_pct": "ROIC，五年平均",
    "gm_ltm_pct": "毛利率，近四季累計（不是單季）",
    "gm_fy1_pct": "毛利率，今年度市場共識（年度）",
    "gm_fy2_pct": "毛利率，明年度市場共識（年度）",
    "incremental_roic_pct": "增量 ROIC",
    "rev_yoy_fq0_pct": "總營收年增，最新一季（不是分項營收）",
    "rev_yoy_fq1_pct": "總營收年增，上一季（不是分項營收）",
    "eps_fy_next_revision_pct": "明年度 EPS 預估，近一個月修正幅度",
    "eps_rev_3m_pct": "EPS 預估，近三個月修正幅度",
    "pe_ntm_x": "本益比，未來 12 個月",
}
# 條件文字提到這些字，代表門檻是單季／財測口徑，不能綁近四季或年度共識欄位
_QUARTERLY_WORDS = re.compile(r"單季|季度|本季|當季|指引|財測|非\s*GAAP|non-?GAAP", re.I)
# 沒有數字又用這些字，代表門檻不可核對
_VAGUE_WORDS = re.compile(r"顯著|明顯|大幅|明確(上升|下滑|增加|減少)|持續(上升|下滑|增加|減少)")


def watch_rule_errors(questions):
    """追蹤條件的機械規則（SKILL v2.1）。出題後、送 opus 前先跑一次，最後把關再跑一次。
    適用 sonnet 原始輸出（manual 條件 metric_key 是空字串）與落檔後的文件（None）。"""
    errs = []
    for i, q in enumerate(questions or [], 1):
        for j, w in enumerate((q or {}).get("watch") or [], 1):
            tag = f"第{i}題第{j}條追蹤條件"
            key = (w.get("metric_key") or "").strip()
            desc, thr = w.get("desc_zh") or "", w.get("threshold") or ""
            text = f"{desc} {thr}"
            has_digit = bool(re.search(r"\d", thr))
            if key:
                if key not in KNOWN_METRIC_KEYS:
                    errs.append(f"{tag}：metric_key「{key}」不在可追蹤欄位清單裡，改用清單裡的欄位，或留空並標需人工")
                    continue
                if not has_digit:
                    errs.append(f"{tag}：綁了 {key} 但門檻沒有數字（「{thr}」），程式無法判斷是否觸及")
                if _QUARTERLY_WORDS.search(text) and not key.startswith("rev_yoy_fq") and not key.startswith("eps_"):
                    errs.append(f"{tag}：條件是單季／財測口徑，但 {key} 是「{KNOWN_METRIC_KEYS[key]}」，口徑對不上；改成需人工，或換口徑相同的欄位")
                if key.startswith("rev_yoy_fq") and re.search(r"資料中心|分項|事業部|網路業務", text):
                    errs.append(f"{tag}：條件講的是分項營收，但 {key} 是總營收，口徑對不上；改成需人工")
            # 「連2季明顯低於」這種寫法，數字只是期數，比較本身還是模糊的；出現模糊字就擋
            if _VAGUE_WORDS.search(thr):
                errs.append(f"{tag}：門檻「{thr}」用了「顯著／明顯／大幅」這類字，改成具體數字（例如低於幾%）或具體事件")
    return errs


def _nonempty(v):
    return bool(v.strip()) if isinstance(v, str) else bool(v)


def check(ticker):
    errors, warnings = [], []
    moat_path = MOAT_DIR / f"{ticker}.json"
    if not moat_path.exists():
        return [f"找不到 {moat_path}"], []
    try:
        doc = json.loads(moat_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"moat/{ticker}.json 不是合法 JSON：{e}"], []

    if doc.get("schema") != "moat-v3":
        errors.append(f"schema 應為 moat-v3，實際是 {doc.get('schema')!r}")
    current = doc.get("current")
    if not current:
        return errors + ["缺少 current 區塊"], warnings

    status = current.get("status")
    if status not in VALID_STATUS:
        errors.append(f"status={status!r} 不屬於 初出／已重出 之一")

    if not _nonempty(current.get("one_liner_zh")):
        errors.append("current.one_liner_zh 是空的")

    rivals = [str(r) for r in (current.get("rivals") or [])]

    # 所有本系統／模型自己撰寫的中文欄位（禁語＋DD／對手名字＋全形標點都查這組）
    prose_fields = {}
    if _nonempty(current.get("one_liner_zh")):
        prose_fields["one_liner_zh"] = current["one_liner_zh"]
    if _nonempty(current.get("vs_prior_zh")):
        prose_fields["vs_prior_zh"] = current["vs_prior_zh"]

    questions = current.get("questions") or []
    if len(questions) != 3:
        errors.append(f"questions 應恰 3 題，實際 {len(questions)} 題")

    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            errors.append(f"questions[{i}] 不是物件")
            continue
        tag = f"questions[{i}]"
        for k in ("q_zh", "why_zh", "lean_reason_zh"):
            if not _nonempty(q.get(k)):
                errors.append(f"{tag} 缺 {k}")
            else:
                prose_fields[f"{tag}.{k}"] = q[k]

        lean = q.get("lean")
        if lean not in VALID_LEAN:
            errors.append(f"{tag}.lean={lean!r} 不屬於 撐住／鬆動／不明 之一")

        evidence = q.get("evidence") or []
        if not evidence:
            errors.append(f"{tag}.evidence 是空的（至少要 1 條）")
        for j, e in enumerate(evidence):
            if not isinstance(e, dict):
                errors.append(f"{tag}.evidence[{j}] 不是物件")
                continue
            text = e.get("text_zh")
            if not _nonempty(text):
                errors.append(f"{tag}.evidence[{j}] 缺 text_zh")
                continue
            prose_fields[f"{tag}.evidence[{j}].text_zh"] = text
            date = e.get("date")
            if not _nonempty(date) and "未能確認" not in text:
                errors.append(f"{tag}.evidence[{j}] 沒有日期，且未寫「未能確認」")

        watch = q.get("watch") or []
        if not watch:
            errors.append(f"{tag}.watch 是空的（至少要 1 條）")
        for j, w in enumerate(watch):
            if not isinstance(w, dict):
                errors.append(f"{tag}.watch[{j}] 不是物件")
                continue
            if not _nonempty(w.get("desc_zh")):
                errors.append(f"{tag}.watch[{j}] 缺 desc_zh")
            else:
                prose_fields[f"{tag}.watch[{j}].desc_zh"] = w["desc_zh"]
            if not (_nonempty(w.get("metric_key")) or w.get("manual") is True):
                errors.append(f"{tag}.watch[{j}] 沒有 metric_key 也沒標 manual（需人工）")
    errors.extend(watch_rule_errors(questions))

    # 正文不可出現「DD」字樣或對手 ticker
    for name, text in prose_fields.items():
        if not text:
            continue
        if "DD" in text:
            errors.append(f"{name} 出現「DD」字樣，正文不可提及研究來源")
        for rv in rivals:
            if rv and rv in text:
                errors.append(f"{name} 出現對手代號「{rv}」，正文不可列對手名字")

    # 禁買賣指令字眼
    full_text = "\n".join(t for t in prose_fields.values() if t)
    for phrase in BANNED_PHRASES:
        if phrase in full_text:
            errors.append(f"出現禁用買賣指令字眼：「{phrase}」")

    # 全形標點（僅警告）
    for name, text in prose_fields.items():
        if text and HALFWIDTH_PUNCT_RE.search(text):
            hits = HALFWIDTH_PUNCT_RE.findall(text)
            warnings.append(f"{name} 疑似有半形標點接在中文字後面（應用全形，，。：）：{hits[:3]}")

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print("usage: python3 scripts/check_moat_review.py TICKER", file=sys.stderr)
        sys.exit(2)
    ticker = sys.argv[1].upper().strip()
    errors, warnings = check(ticker)
    for w in warnings:
        print(f"⚠️  {w}")
    if errors:
        for e in errors:
            print(f"❌ {e}")
        print(f"check_moat_review {ticker}：{len(errors)} 個錯誤，不能上頁（頁面應顯示上一版）。")
        sys.exit(1)
    print(f"✅ check_moat_review {ticker}：通過（{len(warnings)} 個警告）。")


if __name__ == "__main__":
    main()
