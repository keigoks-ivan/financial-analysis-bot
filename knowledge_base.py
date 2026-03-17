"""
knowledge_base.py — 知識庫管理

負責：
  1. 維護公司 (companies.json) 與產業 (industries.json) JSON 索引
  2. 每次 10-K 分析後，從 Claude 輸出中提取並更新護城河五維度評分
  3. 追蹤護城河歷史趨勢（年度對比）

目錄結構：
  knowledge_base/
    companies.json      — { ticker: { name, industry, reports:[...] } }
    industries.json     — { industry_name: { tickers:[...], summary:{} } }
    moat_scores.json    — { ticker: { "2024": { brand_power:7, ... } } }
"""

import os
import re
import json
import datetime
from pathlib import Path

# ── 路徑常數 ─────────────────────────────────────────────────────────────────
KB_DIR          = Path("knowledge_base")
COMPANIES_FILE  = KB_DIR / "companies.json"
INDUSTRIES_FILE = KB_DIR / "industries.json"
MOAT_FILE       = KB_DIR / "moat_scores.json"

# ── 護城河五維度 ─────────────────────────────────────────────────────────────
MOAT_DIMENSIONS = [
    "brand_power",       # 品牌力
    "switching_costs",   # 轉換成本
    "network_effects",   # 網絡效應
    "cost_advantage",    # 成本優勢
    "regulatory_moat",   # 監管護城河
]

# Claude 輸出中搜尋評分的正則（支援「維度名稱：X/10」或「X/10」形式）
_SCORE_PATTERNS = {
    "brand_power":    r"(?:品牌力|brand)[^0-9]*?(\d(?:\.\d)?)\s*/\s*10",
    "switching_costs": r"(?:轉換成本|switching)[^0-9]*?(\d(?:\.\d)?)\s*/\s*10",
    "network_effects": r"(?:網絡效應|network)[^0-9]*?(\d(?:\.\d)?)\s*/\s*10",
    "cost_advantage":  r"(?:成本優勢|cost advantage)[^0-9]*?(\d(?:\.\d)?)\s*/\s*10",
    "regulatory_moat": r"(?:監管護城河|regulatory)[^0-9]*?(\d(?:\.\d)?)\s*/\s*10",
}

# 護城河等級（8 維度分析中第三維度的滿分為 10，此處五維度也用 10 分）
MOAT_WIDE_THRESHOLD   = 7.0
MOAT_NARROW_THRESHOLD = 5.0


class KnowledgeBase:
    """
    公司與產業知識庫，提供 CRUD + 護城河評分管理。
    所有資料持久化為 JSON 檔案，供 web_generator 讀取。
    """

    def __init__(self) -> None:
        KB_DIR.mkdir(parents=True, exist_ok=True)
        self._companies  = self._load(COMPANIES_FILE, default={})
        self._industries = self._load(INDUSTRIES_FILE, default={})
        self._moat       = self._load(MOAT_FILE, default={})

    # ── 低層 I/O ─────────────────────────────────────────────────────────────

    @staticmethod
    def _load(path: Path, default) -> dict:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return default

    @staticmethod
    def _save(path: Path, data: dict) -> None:
        KB_DIR.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _flush(self) -> None:
        """將三個 JSON 全部寫回磁碟。"""
        self._save(COMPANIES_FILE, self._companies)
        self._save(INDUSTRIES_FILE, self._industries)
        self._save(MOAT_FILE, self._moat)

    # ── 公司索引 ─────────────────────────────────────────────────────────────

    def upsert_company(
        self,
        ticker: str,
        name: str = "",
        industry: str = "",
    ) -> None:
        """新增或更新公司基本資料。"""
        ticker = ticker.upper()
        if ticker not in self._companies:
            self._companies[ticker] = {
                "name":     name or ticker,
                "industry": industry,
                "reports":  [],
            }
        else:
            if name:
                self._companies[ticker]["name"] = name
            if industry:
                self._companies[ticker]["industry"] = industry

        # 同步更新產業索引
        if industry:
            self._add_company_to_industry(ticker, industry)

        self._save(COMPANIES_FILE, self._companies)

    def add_report(
        self,
        ticker: str,
        form: str,
        date: str,
        analysis: str,
    ) -> None:
        """
        新增一筆申報分析記錄至公司歷史列表。
        同一天同一 form 只保留最新一筆（覆蓋）。
        """
        ticker = ticker.upper()
        self.upsert_company(ticker)

        reports = self._companies[ticker]["reports"]
        # 去重
        reports = [
            r for r in reports
            if not (r["date"] == date and r["form"] == form)
        ]
        reports.insert(0, {
            "form":     form,
            "date":     date,
            "analysis": analysis,
        })
        # 最多保留 50 筆歷史
        self._companies[ticker]["reports"] = reports[:50]
        self._save(COMPANIES_FILE, self._companies)

    # ── 產業索引 ─────────────────────────────────────────────────────────────

    def _add_company_to_industry(self, ticker: str, industry: str) -> None:
        if industry not in self._industries:
            self._industries[industry] = {"tickers": [], "summaries": {}}
        tickers = self._industries[industry]["tickers"]
        if ticker not in tickers:
            tickers.append(ticker)
        self._save(INDUSTRIES_FILE, self._industries)

    def update_industry_summary(self, synthesis: str, date: str) -> None:
        """
        儲存每日整合報告摘要（前 500 字）至各產業的 summaries 字典。
        這裡以「GLOBAL」鍵儲存全市場整合，
        後續可依需求拆分到各產業。
        """
        snippet = synthesis[:500].replace("\n", " ")
        for industry in self._industries:
            if "summaries" not in self._industries[industry]:
                self._industries[industry]["summaries"] = {}
            self._industries[industry]["summaries"][date] = snippet
        self._save(INDUSTRIES_FILE, self._industries)

    # ── 護城河評分 ───────────────────────────────────────────────────────────

    def extract_moat_scores(self, analysis_text: str, ticker: str) -> dict:
        """
        從 Claude 10-K 分析輸出中，用正則表達式提取五維度護城河評分。
        若無法提取某維度，預設為 5.0（中性）。
        回傳 { "brand_power": 7.5, "switching_costs": 8.0, ... }
        """
        scores = {}
        text   = analysis_text.lower()

        for dim, pattern in _SCORE_PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # 取最後一個匹配（通常是明確的維度評分，非行文中的隨機數字）
                val = float(matches[-1])
                scores[dim] = min(10.0, max(0.0, val))
            else:
                scores[dim] = 5.0   # 無法識別時給中性分

        # 嘗試抓取「護城河總評分：X/10」
        total_match = re.search(
            r"護城河總評分[^0-9]*?(\d(?:\.\d)?)\s*/\s*10",
            analysis_text,
            re.IGNORECASE,
        )
        if total_match:
            total_score = float(total_match.group(1))
            # 若各維度均為中性 5.0，用總分等比縮放
            if all(v == 5.0 for v in scores.values()):
                factor = total_score / 5.0
                scores = {k: min(10.0, v * factor) for k, v in scores.items()}

        print(
            f"  [{ticker}] 護城河評分: "
            + ", ".join(f"{k}={v:.1f}" for k, v in scores.items())
        )
        return scores

    def update_moat_scores(
        self, ticker: str, scores: dict, year: str
    ) -> None:
        """
        更新指定公司、年份的護城河評分。
        若該年度已有資料則覆蓋。
        """
        ticker = ticker.upper()
        if ticker not in self._moat:
            self._moat[ticker] = {}

        self._moat[ticker][year] = {
            dim: scores.get(dim, 5.0) for dim in MOAT_DIMENSIONS
        }
        self._save(MOAT_FILE, self._moat)
        print(f"  [{ticker}] 護城河評分已更新（{year}年）")

    def get_moat_history(self, ticker: str) -> dict:
        """
        取得某公司歷年護城河評分。
        回傳 { "2022": {"brand_power": 7, ...}, "2023": {...}, ... }
        """
        return self._moat.get(ticker.upper(), {})

    def get_moat_level(self, ticker: str) -> str:
        """
        根據最新年度護城河均分，回傳等級字串：
          "Wide Moat" / "Narrow Moat" / "No Moat" / "Unknown"
        """
        history = self.get_moat_history(ticker)
        if not history:
            return "Unknown"

        latest_year = sorted(history.keys())[-1]
        sc  = history[latest_year]
        avg = sum(sc.values()) / len(sc) if sc else 0.0

        if avg >= MOAT_WIDE_THRESHOLD:
            return "Wide Moat"
        if avg >= MOAT_NARROW_THRESHOLD:
            return "Narrow Moat"
        return "No Moat"

    def get_moat_trend(self, ticker: str) -> list[dict]:
        """
        回傳護城河平均分的年度趨勢列表，供圖表渲染使用。
        格式：[{"year": "2022", "avg": 6.8}, {"year": "2023", "avg": 7.1}, ...]
        """
        history = self.get_moat_history(ticker)
        trend   = []
        for year in sorted(history.keys()):
            sc  = history[year]
            avg = sum(sc.values()) / len(sc) if sc else 0.0
            trend.append({"year": year, "avg": round(avg, 2)})
        return trend

    # ── 彙整查詢 ─────────────────────────────────────────────────────────────

    def get_industry_moat_comparison(self, industry: str) -> list[dict]:
        """
        取得某產業所有公司的最新護城河評分，
        回傳按均分降冪排序的列表。
        """
        ind_data = self._industries.get(industry, {})
        tickers  = ind_data.get("tickers", [])

        results = []
        for ticker in tickers:
            history = self.get_moat_history(ticker)
            if not history:
                continue
            latest_yr = sorted(history.keys())[-1]
            sc        = history[latest_yr]
            avg       = sum(sc.values()) / len(sc) if sc else 0.0
            results.append({
                "ticker":      ticker,
                "company_name": self._companies.get(ticker, {}).get("name", ticker),
                "moat_scores": sc,
                "avg_moat":    round(avg, 2),
                "moat_level":  self.get_moat_level(ticker),
            })

        results.sort(key=lambda r: r["avg_moat"], reverse=True)
        return results

    def get_all_companies(self) -> dict:
        """回傳完整 companies 字典。"""
        return self._companies

    def get_all_industries(self) -> list[str]:
        """回傳所有產業名稱列表。"""
        return list(self._industries.keys())

    def print_summary(self) -> None:
        """在 console 輸出知識庫統計摘要。"""
        print("\n── Knowledge Base 摘要 ──")
        print(f"  公司數：{len(self._companies)}")
        print(f"  產業數：{len(self._industries)}")
        scored = sum(1 for t in self._companies if t in self._moat)
        print(f"  有護城河評分：{scored} 家")

        if self._moat:
            print("\n  最新護城河評分：")
            for ticker, yearly in sorted(self._moat.items()):
                if not yearly:
                    continue
                yr  = sorted(yearly.keys())[-1]
                sc  = yearly[yr]
                avg = sum(sc.values()) / len(sc) if sc else 0
                lvl = self.get_moat_level(ticker)
                print(f"    {ticker:8s} {yr}  均分={avg:.1f}  {lvl}")
        print("─" * 30)


# ── 快速 CLI 測試 ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    kb = KnowledgeBase()
    kb.print_summary()
