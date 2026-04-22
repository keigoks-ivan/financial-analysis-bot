#!/usr/bin/env python3
"""
id_dd_mapping.py — 建 ticker ↔ ID 對應表

讀 docs/id/INDEX.md 每行的「備注」欄，抽出「涵蓋 TICKER1 / TICKER2 / ...」清單，
與 docs/dd/INDEX.md 的 v11+ DD 對照。

輸出 portfolio/id_dd_map.json：
{
  "ticker_to_ids": {"NVDA": ["ID_AIAcceleratorDemand_20260419.html", ...], ...},
  "id_to_tickers": {"ID_AIAcceleratorDemand_20260419.html": ["NVDA","AVGO",...], ...},
  "dd_tickers_without_id": ["TICKER1", ...],
  "id_tickers_without_dd": ["TICKER1", ...]
}
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ID_INDEX = REPO / "docs" / "id" / "INDEX.md"
DD_INDEX = REPO / "docs" / "dd" / "INDEX.md"
OUT = REPO / "portfolio" / "id_dd_map.json"


# 常見 ticker 格式：1-5 個大寫字母，或 4 位數（台股），可帶 .TW/.T/.AS/.KS/.PA/.DE
TICKER_RE = re.compile(r"\b([A-Z]{1,5}(?:\.(?:TW|TWO|T|AS|KS|PA|DE))?|\d{4,6}(?:\.(?:TW|T|KS))?)\b")

# 白名單：常見會誤判的字
BLACKLIST = {
    "AI","ID","DD","PM","DC","HVM","ETF","GSU","LPT","LIDE","PSU","AP","AS","THE","AND","OR","FY","FX","EV","EBITDA","PE","PEG","ROE","ROIC","WACC","CAGR","EPS",
    "VS","ET","US","EU","JP","KR","CN","TW","TAM","SAM","ARR","LTV","CAC","COGS","SAAS","LLM","API","GPU","CPU","FPGA","AMD","ARM","ASIC","ML","NLP","SDK",
    "MGX","SST","CDU","DTC","CPO","HBM","GAAP","NON","IPO","IP","GM","COO","CEO","CFO","CTO","R","D","UALINK","UA","PCIE","NVLINK","CXL","CHIPS","IRA","CSR","MW","GW","KW","HZ","V","AH","SHARE","YOY","QOQ","UP","DOWN","KHZ","MHZ","GHZ","THZ","NM","MM","CM","TTM","NTM","YTD","QTD","TB","GB","PB","GT","H2","H1","Q1","Q2","Q3","Q4","FY1","FY2","FY3",
    "M","B","T","K","W","N","S","E",
    "BY","ON","TO","OF","IN","FOR","WITH","FROM","THIS","THAT","IS","BE","NOT","NEW","OLD","ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE","TEN",
}


def extract_tickers_from_note(note: str) -> set[str]:
    """從 ID INDEX 備注欄抽 ticker。"""
    tickers = set()
    # 先找「涵蓋 X / Y / Z」或「；X / Y / Z」段
    for m in TICKER_RE.finditer(note):
        t = m.group(1)
        if t in BLACKLIST:
            continue
        # 台股純數字補 .TW
        if re.fullmatch(r"\d{4,5}", t):
            t = t + ".TW"
        tickers.add(t)
    return tickers


def parse_id_index():
    """回傳 {id_file: {"topic":..., "tickers":{...}, "date":...}}"""
    result = {}
    for line in ID_INDEX.read_text().splitlines():
        if not line.startswith("| 2026") and not line.startswith("| 2027"):
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 10:
            continue
        date, topic = cols[1], cols[2]
        # 最後一個有意義欄前是檔名
        id_file = cols[8]
        note = cols[9]
        tickers = extract_tickers_from_note(note)
        result[id_file] = {"date": date, "topic": topic, "tickers": sorted(tickers)}
    return result


def parse_dd_index():
    """回傳 v11+ DD 的 ticker set (去重後)"""
    tickers = set()
    for line in DD_INDEX.read_text().splitlines():
        if not re.search(r"\| v1[12]\.", line):
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 8:
            continue
        t = cols[2]
        if re.fullmatch(r"\d{4,5}", t):
            t = t + ".TW"
        tickers.add(t)
    return tickers


def main():
    id_data = parse_id_index()
    dd_tickers = parse_dd_index()

    ticker_to_ids = {}
    id_to_tickers = {fn: data["tickers"] for fn, data in id_data.items()}

    for fn, data in id_data.items():
        for t in data["tickers"]:
            ticker_to_ids.setdefault(t, []).append(fn)

    id_ticker_set = set()
    for ts in id_to_tickers.values():
        id_ticker_set.update(ts)

    dd_tickers_without_id = sorted(dd_tickers - id_ticker_set)
    id_tickers_without_dd = sorted(id_ticker_set - dd_tickers)

    out_data = {
        "id_count": len(id_data),
        "dd_ticker_count": len(dd_tickers),
        "id_ticker_count": len(id_ticker_set),
        "overlapping_count": len(dd_tickers & id_ticker_set),
        "ticker_to_ids": {t: ticker_to_ids.get(t, []) for t in sorted(ticker_to_ids)},
        "id_to_tickers": id_to_tickers,
        "dd_tickers_without_id": dd_tickers_without_id,
        "id_tickers_without_dd": id_tickers_without_dd,
        "id_meta": {fn: {"date": d["date"], "topic": d["topic"]} for fn, d in id_data.items()},
    }
    OUT.write_text(json.dumps(out_data, ensure_ascii=False, indent=2))
    print(f"Wrote {OUT}")
    print(f"IDs: {out_data['id_count']}")
    print(f"DD tickers (v11+): {out_data['dd_ticker_count']}")
    print(f"ID tickers: {out_data['id_ticker_count']}")
    print(f"Overlap: {out_data['overlapping_count']}")
    print(f"DD without ID: {len(dd_tickers_without_id)}")
    print(f"ID without DD: {len(id_tickers_without_dd)}")


if __name__ == "__main__":
    main()
