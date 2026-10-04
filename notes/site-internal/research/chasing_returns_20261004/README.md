# 追漲四問：歷史回測（2026-10-04）

追逐過去的高報酬有沒有用？這個資料夾是完整的回測程式、結果與兩份報告頁，資料截至 2026 年 9 月。網站版在 https://research.investmquest.com/backtest/chasing_returns/ ，由 `scripts/build_chasing_returns.py` 把這裡的兩個 HTML 包進網站外框後寫到 `docs/backtest/chasing_returns/`。

## 四個問題

1. 美國股市在最近幾年創下高報酬後的表現如何？
2. 在一段長時期創下高報酬或低報酬後才開始長期投資美股（5 到 20 年），績效會不會比較好？
3. 每年將投資轉換為近年來標普指數績效最佳的類股，是否會比大盤整體的平均表現更佳？
4. 近幾年績效最佳的避險基金策略，績效是否優於當年度所有策略的平均？

之後又追加七個追問：漲幅來源、結構性估值、漲勢寬度、領先類股何時結束、「熱＋貴」訊號太早的代價、樣本外檢驗、台股是否適用。

## 報告

| 檔案 | 內容 | 網站 |
|---|---|---|
| `chasing.html` | 主報告：四題，每題 6–9 個面向，分時期比較 | `/backtest/chasing_returns/` |
| `followups.html` | 續篇：七個追問 | `/backtest/chasing_returns/followups.html` |

兩個 HTML 是 Artifact 頁面的原始檔（沒有 `<html>`／`<head>` 外框），直接用瀏覽器開也能看。

## 主要結論

| 題目 | 結論 | 證據強度 |
|---|---|---|
| 1 高報酬之後 | 一年大漲沒有影響；連續 3–5 年高報酬之後，之後 1–5 年平均偏低、回撤風險上升。CAPE 快速上升或漲勢很窄時最明顯 | 全期間顯著；前後兩段同方向，後半段幅度較小 |
| 2 長期起點 | 冷起點長期較好（美國兩段、16 國中 15 國同方向），但持有 20 年在美國歷史上都沒有實質虧損 | 弱：考慮重疊窗口後只算邊緣顯著；台股看不到 |
| 3 追最強類股 | 每年換「去年冠軍大類股」沒有優勢；每月更新的細產業動能長期有效，但 2010 年後變弱 | 產業動能樣本外最穩健 |
| 4 追最強避險策略 | 追去年或近 3 年最佳策略都落後所有策略平均，2008 年後更差 | 兩套獨立指數一致 |

關於 2026 年 9 月的位置：美國估值、盈餘相對 10 年平均、漲勢集中度都在歷史前 20%，經利率或時代調整後的估值較溫和；台股近 3 年年化 43%，是 1990 年以來最高。歷史上這類訊號出現後通常還有一段漲幅。這些結果是歷史基準的描述，不是擇時訊號。

## 重跑

```bash
pip install pandas numpy scipy xlrd openpyxl
bash run_all.sh        # 約 2 分鐘，需要網路
```

`run_all.sh` 會先跑 `fetch_data.py` 下載所有公開資料，再依序重建結果 JSON 與兩份報告。重建後要更新網站版，在 repo 根目錄跑 `python3 scripts/build_chasing_returns.py`。2026-10-04 在乾淨資料夾重跑過一次：兩份 HTML 與原版逐位元相同，數值只有 Yahoo 調整價造成的百萬分之一級差異。Shiller、Ken French 與 Yahoo 的資料每月更新，日後重跑的數字會略有不同；報告中「現在」的文字是手寫的，日後重跑不會自動更新。

## 檔案

| 階段 | 檔案 |
|---|---|
| 共用 | `base.py`（美股月資料、Shiller）、`ind.py`（Ken French 產業）、`charts.py`（SVG 圖表）、`f6lib.py`（樣本外與重抽統計） |
| 資料 | `fetch_data.py`、`build_mkt.py`（1871–2026 美股月報酬與通膨） |
| 第一版 | `q12.py`、`q2.py`、`q3.py`、`q4.py`＋`q4_variants.py`、`build_page.py`、`build_q4.py` |
| 主報告（多面向） | `q1_deep.py`、`q2_deep.py`、`q2_intl.py`、`q12_extra.py`、`q3_deep.py`、`q3_cal.py`、`q4_deep.py`、`q4_cs.py` → `frags_v2.py` → `page_v2.py` |
| 續篇 | `f1.py`＋`f1_e10.py`（漲幅來源）、`f2.py`（結構性估值）、`f3.py`＋`f3_rsp.py`（寬度）、`f4.py`＋`f4b.py`（產業估值）、`f5.py`（太早的代價）、`f6.py`＋`f6b.py`＋`f6c.py`（樣本外）、`tw_*.py`（台股）→ `frags_f.py`＋`frags_tw.py` → `page_f.py` |
| 結果 | 根目錄的 `*.json`（每支腳本的輸出） |
| 頁面樣式 | `v2_css.txt`、`v2_head.txt`、`v2_script.txt` |

## 資料來源

已提交進 repo：

- `tw/`：臺灣加權指數（年資料 1967–2025、月資料 1990–2026）、報酬指數（2003–2026）、28 個類股指數年底值（2009–2025）。證交所網站擋掉程式下載，這些數字是透過網頁讀取工具轉錄，並與 Yahoo、臺灣指數公司交叉核對；1967–1989 年取自 Wikipedia，未經證交所核對。細節見 `tw/SOURCES_TW.md`。

執行時下載、不提交：

- Shiller 資料（shillerdata.com）：S&P 綜合指數、股息、盈餘、CPI、CAPE、超額 CAPE 殖利率、公債報酬
- Ken French Data Library：市場因子、10／12／17／30／49 產業組合
- FRED：CPIAUCNS（2025 年 10 月因美國政府停擺未公布，`build_mkt.py` 以對數內插補值）
- Jordà-Schularick-Taylor Macrohistory Database R6：16 國股票報酬
- Yahoo Finance：SPY、SPDR 類股 ETF、RSP
- EDHEC-Risk Alternative Indexes（EDHEC 課程公開資料集的 GitHub 鏡像，1997–2018）
- Credit Suisse Hedge Fund Index 各策略（公開 GitHub 專案中的 Bloomberg 匯出檔，1994–2022，二手資料，未與官方表格核對）

避險基金資料的取得過程與限制見 `sources/`。HFRX 指數有不得轉載的條款，沒有使用。

## 限制

- 月度觀察點彼此高度重疊，表中的月數遠大於獨立樣本；條件成立的獨立段數多在 4–18 段之間。
- 美股 1926 年後用 CRSP 全市場報酬，長期年化與 S&P 500 很接近，個別年份可能相差數個百分點。
- 台股全部是價格指數，不含股息（每年約 3.7%）；找不到可用的台灣 CPI，第 2 題用名目報酬。
- 所有回測未計交易成本與稅。
