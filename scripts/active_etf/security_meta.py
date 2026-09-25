#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""個股靜態基本資料(已發行股數 + 產業別)快取,供擁擠度(M2,股數÷已發行股數)
與風格偏好(M4,產業權重、市值分位)兩個分析模組共用。來源:證交所 OpenAPI
t187ap03_L(上市)+ 櫃買中心 OpenAPI mopsfin_t187ap03_O(上櫃)——與
scripts/build_price_momentum_tw.py 的 universe 抓法同一組端點,但目的不同:
P10-TW 只要「名冊」(公司名+產業別+上市日)用來篩選投資池,這裡額外要「已發行
股數」(t187ap03_L 的『已發行普通股數或TDR原股發行股數』欄、TPEx 的
『IssueShares』欄),且不套用 P10-TW 的創新板/上市未滿週年過濾——主動式 ETF
可能持有任何一檔,過濾掉會讓那些股票的擁擠度/產業分類直接缺值。

產業別代碼→中文名稱重用 build_price_momentum_tw.SECTOR_MAP(同一套證交所/櫃買
產業別代碼體系),不重寫這張表。

儲存:data/active_etf/security_meta.json,單一 dict {ticker(.TW/.TWO):
{name, shares_outstanding, industry_code, industry_name, market, as_of}}。
產業別、股本這類資料變動慢,FULL(週六)模式才重抓,PRICE 模式直接讀既有快取。
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import build_price_momentum_tw as bpm  # noqa: E402 — 只借用 SECTOR_MAP

META_PATH = REPO_ROOT / "data" / "active_etf" / "security_meta.json"

TWSE_URL = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
TPEX_URL = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def _to_int(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def fetch_twse_meta():
    resp = requests.get(TWSE_URL, headers={"User-Agent": UA}, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    out = {}
    for row in data:
        code = str(row.get("公司代號", "")).strip()
        if not (len(code) == 4 and code.isdigit()):
            continue
        ind_code = str(row.get("產業別", "")).strip()
        out[code + ".TW"] = {
            "name": str(row.get("公司簡稱", "")).strip(),
            "shares_outstanding": _to_int(row.get("已發行普通股數或TDR原股發行股數")),
            "industry_code": ind_code,
            "industry_name": bpm.SECTOR_MAP.get(ind_code, "未分類"),
            "market": "TWSE",
        }
    return out


def fetch_tpex_meta():
    resp = requests.get(TPEX_URL, headers={"User-Agent": UA}, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    out = {}
    for row in data:
        code = str(row.get("SecuritiesCompanyCode", "")).strip()
        if not (len(code) == 4 and code.isdigit()):
            continue
        ind_code = str(row.get("SecuritiesIndustryCode", "")).strip()
        out[code + ".TWO"] = {
            "name": str(row.get("CompanyAbbreviation", "")).strip(),
            "shares_outstanding": _to_int(row.get("IssueShares")),
            "industry_code": ind_code,
            "industry_name": bpm.SECTOR_MAP.get(ind_code, "未分類"),
            "market": "TPEx",
        }
    return out


def build_security_meta():
    """回傳 (meta_dict, errors)——單一交易所端點失敗不讓另一邊也失敗;兩邊都
    失敗且既有快取也沒有時,呼叫端會退回使用空 dict(該次建置的產業/擁擠度分析
    整批標記覆蓋率 0,不中斷整個 build)。"""
    meta, errors = {}, []
    today = datetime.date.today().isoformat()
    try:
        twse = fetch_twse_meta()
        for k, v in twse.items():
            v["as_of"] = today
        meta.update(twse)
    except Exception as e:  # noqa: BLE001
        errors.append("TWSE t187ap03_L: {}".format(e))
    try:
        tpex = fetch_tpex_meta()
        for k, v in tpex.items():
            v["as_of"] = today
        meta.update(tpex)
    except Exception as e:  # noqa: BLE001
        errors.append("TPEx mopsfin_t187ap03_O: {}".format(e))
    return meta, errors


def load_security_meta():
    if not META_PATH.exists():
        return {}
    try:
        return json.loads(META_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_security_meta(meta):
    META_PATH.parent.mkdir(parents=True, exist_ok=True)
    META_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def update_security_meta(mode):
    """mode="full":重抓兩個交易所端點並整檔覆寫(單邊失敗時保留該邊舊快取,
    只覆蓋抓成功的一邊,見下)。mode="price":直接讀既有快取,不打 API。"""
    if mode != "full":
        return load_security_meta(), []
    fresh, errors = build_security_meta()
    if not fresh:
        return load_security_meta(), errors
    existing = load_security_meta()
    # 只覆蓋這次真的抓到的 market(TWSE/TPEx 分開判斷),另一邊若這次失敗就保留
    # 既有快取裡那個 market 的舊資料,不因單邊 API 掛掉而整批清空。
    fresh_markets = {v["market"] for v in fresh.values()}
    merged = {k: v for k, v in existing.items() if v.get("market") not in fresh_markets}
    merged.update(fresh)
    save_security_meta(merged)
    return merged, errors


if __name__ == "__main__":
    m, errs = update_security_meta("full")
    print("security_meta: {} tickers ({} TWSE, {} TPEx), errors={}".format(
        len(m), sum(1 for v in m.values() if v.get("market") == "TWSE"),
        sum(1 for v in m.values() if v.get("market") == "TPEx"), errs))
