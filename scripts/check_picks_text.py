#!/usr/bin/env python3
"""「本站挑選」文字的機械檢查（skill `picks-monthly`；登記程式 picks_register.py 也會呼叫）。

  python3 scripts/check_picks_text.py --kind active-etf|etf-dash --text FILE --evidence FILE [--mode register|review]
      [--base-rate FILE]

--text 的格式
  register（預設）：{"paragraphs": [{"lead": "", "text": ""} x 4], "frozen_note": ""}
                    （若另有 "title"、"sub"，只查數字與禁用詞，不查長度）
  review：{"text": "月評本文", "status_line": "一行摘要（可省略）"}；也接受純文字檔

--evidence 是模型唯一可引用的數字來源（picks_candidates.py --brief 的輸出，月評另附追蹤 JSON 摘要）。

檢查項目
  1. 數字：文字裡每個阿拉伯數字（含小數、含 +/−）都要在證據檔出現。
     小數照文字的顯示位數四捨五入比對（與 check_horizon_memo.py 相同）；整數要完全相同。
     符號：文字寫 − 必須對到證據裡的負值，寫 + 必須對到非負值，沒寫符號則不分。
     豁免：2022～2027 的整數年份、「22 檔」「21 檔」「126」、數字後接年／月／日／天／個月的時間標籤、
     YYYY-MM-DD 日期、基金代號（00981A、2558.T、0050.TW、W52 這類）、0 開頭的 4 位以上代號（0050）。
  2. 長度：register 每段（lead＋text）≤ 160 字、每句 ≤ 60 字、固定 4 段、frozen_note 非空；
     review 全文 ≤ 220 字、2～4 句。
  3. 禁用詞：「——」、比喻詞清單、「本頁不對」「值得點出」「真正該」、買賣指令用語；
     「；」每段最多 1 個（review 全文最多 1 個）。
  4. 「不是 A，是 B」句型全文最多 1 次。
  5. 基率引用（register 模式且給了 --base-rate，picks_base_rate.py 的輸出；skill picks-monthly v1.3）：
     基率檔的 brief 併進證據；第二段（攻方理由）的 lead＋text 至少要出現一條規則的「條件內勝率」或
     「條件內平均超額」（照顯示位數比對，符號要對）。三條都是「無基率」時，第二段要寫出「無基率」。
     沒給 --base-rate 不查這一條（舊登記、active-etf 照舊）。

輸出 PASS 或 FAIL＋逐條原因；FAIL 時 exit code 為 1。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

KINDS = ("active-etf", "etf-dash")
MODES = ("register", "review")

PARA_MAX = 160
SENT_MAX = 60
REVIEW_MAX = 220
REVIEW_SENT = (2, 4)
N_PARAS = 4

METAPHORS = ["吹出", "煞車", "天花板", "柱子", "震央", "癒合", "扛", "甩開", "雪崩", "閘門", "藥方",
             "天平", "鏡像", "同一張牌"]
SELF_TALK = ["本頁不對", "值得點出", "真正該"]
TRADE_WORDS = ["買進", "買入", "賣出", "加碼", "減碼", "建倉", "清倉", "停損", "停利", "目標價",
               "應該買", "應該賣", "建議買", "建議賣"]
DASH = "——"

MINUS = "-−–－"
PLUS = "+＋"

# 先剔除、不當成數字的片段（代號、日期、固定詞）
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_CODE_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9])\d{4,6}[A-Z](?![A-Za-z0-9])"),            # 00981A
    re.compile(r"(?<![A-Za-z0-9])\d{4,5}\.[A-Z]{1,2}(?![A-Za-z0-9])"),     # 2558.T、0050.TW
    re.compile(r"(?<![A-Za-z0-9])[A-Z]+\d+[A-Z]*(?![A-Za-z0-9])"),         # W52、A2
    re.compile(r"(?<![\d.])0\d{3,}(?![\d.])"),        # 0050
]
_FIXED = re.compile(r"(?<!\d)(?:22|21)\s*檔|(?<![\d.])126(?![\d.])|兩檔各半")
_YEAR_OK = {str(y) for y in range(2022, 2028)}
_TIME_UNIT = re.compile(r"\s*(?:年|月|日|天|個月|個交易日|週|周)")

_NUM = re.compile(r"(?<![A-Za-z0-9_.])([+\-−–－＋])?(\d+(?:,\d{3})*(?:\.\d+)?)")
_NOT_A_B = re.compile(r"不是[^。！？\n]{1,30}?[，,]\s*(?:而)?是")
_SENT_SPLIT = re.compile(r"[。！？!?\n]+")


def _to_float(s: str) -> float:
    return float(s.replace(",", ""))


def evidence_numbers(evidence: str) -> list[tuple[float, bool]]:
    """證據檔裡的 (絕對值, 是否負值) 清單。先去掉 ISO 日期，避免 2026-10-28 的 -10 被當負數。"""
    ev = _ISO_DATE.sub(" ", evidence)
    out: list[tuple[float, bool]] = []
    for m in _NUM.finditer(ev):
        out.append((_to_float(m.group(2)), (m.group(1) or "") in tuple(MINUS)))
    return out


def text_numbers(text: str) -> list[tuple[str, str, str]]:
    """文字裡要檢查的數字：(原樣字串, 符號, 數字本體)。已剔除豁免項目。"""
    t = _ISO_DATE.sub(" ", text)
    t = _FIXED.sub(" ", t)
    for p in _CODE_PATTERNS:
        t = p.sub(" ", t)
    out = []
    for m in _NUM.finditer(t):
        sign, body = m.group(1) or "", m.group(2)
        if "." not in body and "," not in body and not sign:
            if body in _YEAR_OK:
                continue
            if _TIME_UNIT.match(t, m.end()):
                continue
        out.append((sign + body, sign, body))
    return out


def _number_found(sign: str, body: str, ev: list[tuple[float, bool]]) -> bool:
    v = _to_float(body)
    dec = len(body.split(".")[1]) if "." in body else None
    for k, neg in ev:
        if sign and sign in MINUS and not neg:
            continue
        if sign and sign in PLUS and neg:
            continue
        if dec is None:
            if abs(k - v) < 1e-9:
                return True
        elif abs(round(k, dec) - v) < 1e-9:
            return True
    return False


def check_numbers(name: str, text: str, ev: list[tuple[float, bool]]) -> list[str]:
    errs = []
    seen = set()
    for raw, sign, body in text_numbers(text):
        if raw in seen:
            continue
        seen.add(raw)
        if not _number_found(sign, body, ev):
            errs.append(f"{name} 的數字 {raw} 在證據包裡找不到")
    return errs


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]


def check_words(name: str, text: str, semicolon_max: int | None = 1) -> list[str]:
    errs = []
    if DASH in text:
        errs.append(f"{name} 出現「——」")
    for w in METAPHORS:
        if w in text:
            errs.append(f"{name} 出現比喻詞「{w}」")
    for w in SELF_TALK:
        if w in text:
            errs.append(f"{name} 出現自我說明用語「{w}」")
    for w in TRADE_WORDS:
        if w in text:
            errs.append(f"{name} 出現買賣用語「{w}」")
    n = text.count("；")
    if semicolon_max is not None and n > semicolon_max:
        errs.append(f"{name} 的「；」有 {n} 個，上限 {semicolon_max}")
    return errs


def _paragraph_str(p: dict) -> str:
    return (p.get("lead") or "") + (p.get("text") or "")


def check_register(obj: dict, ev: list[tuple[float, bool]]) -> list[str]:
    errs: list[str] = []
    paras = obj.get("paragraphs")
    if not isinstance(paras, list) or len(paras) != N_PARAS:
        errs.append(f"paragraphs 要剛好 {N_PARAS} 段，現在 {len(paras) if isinstance(paras, list) else '沒有'}")
        paras = paras if isinstance(paras, list) else []
    all_text: list[str] = []
    for i, p in enumerate(paras, 1):
        name = f"第 {i} 段"
        if not isinstance(p, dict) or not (p.get("text") or "").strip():
            errs.append(f"{name} 空白")
            continue
        s = _paragraph_str(p)
        all_text.append(s)
        if len(s) > PARA_MAX:
            errs.append(f"{name} 超過 {PARA_MAX} 字（{len(s)}）")
        for j, sent in enumerate(split_sentences(s), 1):
            if len(sent) > SENT_MAX:
                errs.append(f"{name} 第 {j} 句超過 {SENT_MAX} 字（{len(sent)}）：{sent[:20]}…")
        errs += check_words(name, s)
        errs += check_numbers(name, s, ev)
    note = obj.get("frozen_note")
    if not (note or "").strip():
        errs.append("frozen_note 空白")
    else:
        all_text.append(note)
        for j, sent in enumerate(split_sentences(note), 1):
            if len(sent) > SENT_MAX:
                errs.append(f"frozen_note 第 {j} 句超過 {SENT_MAX} 字（{len(sent)}）")
        errs += check_words("frozen_note", note)
        errs += check_numbers("frozen_note", note, ev)
    for key in ("title", "sub"):
        if obj.get(key):
            all_text.append(obj[key])
            errs += check_words(key, obj[key], semicolon_max=None)
            errs += check_numbers(key, obj[key], ev)
    errs += check_not_a_b("\n".join(all_text))
    return errs


def check_review(obj: dict, ev: list[tuple[float, bool]]) -> list[str]:
    errs: list[str] = []
    text = (obj.get("text") or "").strip()
    if not text:
        return ["text 空白"]
    if len(text) > REVIEW_MAX:
        errs.append(f"月評超過 {REVIEW_MAX} 字（{len(text)}）")
    n = len(split_sentences(text))
    if not REVIEW_SENT[0] <= n <= REVIEW_SENT[1]:
        errs.append(f"月評要 {REVIEW_SENT[0]}～{REVIEW_SENT[1]} 句，現在 {n} 句")
    errs += check_words("月評", text)
    errs += check_numbers("月評", text, ev)
    parts = [text]
    sl = (obj.get("status_line") or "").strip()
    if sl:
        parts.append(sl)
        errs += check_words("status_line", sl)
        errs += check_numbers("status_line", sl, ev)
    errs += check_not_a_b("\n".join(parts))
    return errs


def base_rate_cites(br: dict) -> list[tuple[float, bool]]:
    """基率檔裡可以拿來當「引用」的數字：每條有基率的規則的條件內勝率與條件內平均超額。
    判定「無基率」的規則（樣本不足時也有數字）不算。"""
    out: list[tuple[float, bool]] = []
    for r in br.get("rules") or []:
        if r.get("verdict") == "無基率":
            continue
        for k in ("hit_cond_pct", "excess_cond_pct"):
            v = r.get(k)
            if isinstance(v, (int, float)):
                out.append((abs(float(v)), float(v) < 0))
    return out


def check_base_rate_citation(obj: dict, br: dict) -> list[str]:
    paras = obj.get("paragraphs")
    if not isinstance(paras, list) or len(paras) < 2 or not isinstance(paras[1], dict):
        return ["有基率檔但沒有第二段，無法檢查基率引用"]
    s = _paragraph_str(paras[1])
    cites = base_rate_cites(br)
    if not cites:
        return [] if "無基率" in s else ["三條規則都沒有基率，第二段要寫出「無基率」"]
    if any(_number_found(sign, body, cites) for _, sign, body in text_numbers(s)):
        return []
    return ["第二段沒有引用任何一條規則的歷史勝率或平均超額（基率檔的條件內勝率或條件內平均超額）"]


def check_not_a_b(text: str) -> list[str]:
    n = len(_NOT_A_B.findall(text))
    return [f"「不是 A，是 B」句型出現 {n} 次，全文上限 1 次"] if n > 1 else []


def load_text(path: Path, mode: str) -> dict:
    raw = path.read_text(encoding="utf-8")
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        if mode == "review":
            return {"text": raw}
        raise
    if isinstance(obj, str):
        return {"text": obj}
    if not isinstance(obj, dict):
        raise ValueError("text 檔要是 JSON 物件")
    return obj


def check(kind: str, obj: dict, evidence: str, mode: str = "register", base_rate: dict | None = None) -> list[str]:
    """回傳錯誤清單；空清單＝PASS。base_rate＝picks_base_rate.py 的輸出（只在 register 模式用）。"""
    if mode == "review":
        return check_review(obj, evidence_numbers(evidence))
    if base_rate:
        evidence = evidence + "\n" + (base_rate.get("brief") or "")
    errs = check_register(obj, evidence_numbers(evidence))
    if base_rate:
        errs += check_base_rate_citation(obj, base_rate)
    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kind", required=True, choices=KINDS)
    ap.add_argument("--text", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--mode", default="register", choices=MODES)
    ap.add_argument("--base-rate", default=None, help="picks_base_rate.py 的輸出 JSON（register 模式查第二段引用）")
    a = ap.parse_args(argv)
    try:
        obj = load_text(Path(a.text), a.mode)
        evidence = Path(a.evidence).read_text(encoding="utf-8")
        base_rate = json.loads(Path(a.base_rate).read_text(encoding="utf-8")) if a.base_rate else None
    except Exception as e:  # noqa: BLE001
        print(f"FAIL 讀不到輸入：{e}")
        return 1
    errs = check(a.kind, obj, evidence, a.mode, base_rate)
    if errs:
        print(f"FAIL {a.kind} {a.mode}")
        for e in errs:
            print(" -", e)
        return 1
    print(f"PASS {a.kind} {a.mode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
