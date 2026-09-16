# P10 台股版（P10-TW）設計稿 — 2026-09-16

目的：把 `/research/price-momentum/`（美股 P10 雙線純價格動能 paper track）複製一份到台股，路徑 `/research/price-momentum-tw/`。規則、門檻、程式路徑盡量與美股版逐字相同，只換三樣東西：股票名單、基準、資料來源。這樣兩個市場的差異才能歸因到市場本身。

## 一、不變的部分（與美股版逐字相同）

- 雙線 L12（12-1 動能）與 L6（6-1 動能），唯一差異是回看窗口。
- 常數全部照抄：`MIN_CLOSES=253`、`MA_WINDOW=200`、`FAR_IDX_L12=-253`、`FAR_IDX_L6=-127`、近端 `-22`、`HEAT_RET12=2.5`、`TOP_BUY=10`、`TOP_HOLD=40`、`N_SEATS=10`、`TURNOVER_WINDOW=12`、`TURNOVER_KILL_PCT=300`。
- 資格：該線 ret > 0，且收盤 > 200 日均線。沒有任何基本面條件。
- 月度換倉、top-40 緩衝、等權重置、現金席位、換手統計、同日重跑冪等、`eligible` 旗標揭露、fail-safe exit 0、GitHub Actions `::warning::`、分批下載＋重試：全部沿用。
- 台股一年約 245 個交易日，253 筆收盤約等於 12.4 個月。刻意不改常數，頁面揭露這一點即可。

## 二、換掉的三樣東西

### 1. 股票名單：上市加上櫃普通股，取流動性前 300 名

- 來源：上市走證交所 OpenAPI `https://openapi.twse.com.tw/v1/opendata/t187ap03_L`（上市公司基本資料，不變）；上櫃走櫃買中心 OpenAPI `https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O`（上櫃公司基本資料，891 筆，英文欄位：`SecuritiesCompanyCode`/`CompanyAbbreviation`/`SecuritiesIndustryCode`/`DateOfListing`，`DateOfListing` 格式與證交所同為 YYYYMMDD，已實測確認）。QGM 台股版每天在 GitHub Actions 用同一支上市 API，可用。
- 篩選：兩邊都只保留代號為 4 位數字者（排除 ETF、權證、特別股）。金融股保留。P10 是純價格序列，美股版也沒排金融股。
- 流動性閘：對合併後（上市 ∪ 上櫃）通過 253 筆收盤門檻的名字，算最近 120 個交易日「收盤 × 成交股數」的中位數，取前 300 名為本週 universe。這是用價量資料機械決定的，等同美股版用「S&P 500 成分」當大型股代理。掉出前 300 名的持股視為不合格，下次月度換倉賣出，與美股版指數剔除的處理一致。
- 每檔記 `name`（公司簡稱）與 `sector`（產業別代碼轉中文，上市上櫃共用同一張對照表，兩交易所的產業別編碼體系相同，對照表寫死在 script 裡）。
- 創新板不納入（公司簡稱「-創」結尾，上市上櫃同一條規則；上櫃目前查無此類名字）。上市或上櫃日期距執行日不足 365 天者不納入，上市用「上市日期」、上櫃用「DateOfListing」算。這兩條是 2026-09-16 第一天修正：首次 inception 後發現 7610 聯友金屬-創（2025-09-09 上市，但 yfinance 有 852 筆興櫃時期價格）排兩線第一，同日撤回重建，當時未發生任何換倉。
- yfinance 代碼：上市 `{code}.TW`；上櫃 `{code}.TWO`（已實測抓得到）。同一代號若兩邊都出現（理論上不會），上市優先。
- **2026-09-16 同日第二次修正**：名單由「僅上市」擴為「上市 ∪ 上櫃」——原設計上櫃不納入，本次撤回重建改為納入，同樣在任何換倉前完成，未發生任何換倉。理由：P10 是市場純價格動能的機械測試，沒有理由只涵蓋半個市場。基準仍為 0050（只含上市股），與名單母體不完全對齊，屬已知取捨，頁面明講。

### 2. 基準：0050.TW

- 用元大台灣 50 ETF 的還原收盤，對應美股版的 SPY。加權指數 `^TWII` 不含股利，會讓基準變好打，所以不用。
- 頁面揭露：0050 約五成到六成是台積電，基準本身高度集中。

### 3. Kill conditions

- kill ①（24 個月 NAV 落後 0050 且最大回撤更深）：沿用，逐線獨立。
- kill ②（對 Momentum-5 shadow line C）：台股沒有對照線，寫明「不適用」。
- kill ③（換手 > 300%）：沿用。
- 正式評估點：inception 日起 24 個月。

## 三、檔案清單

| 檔案 | 動作 |
|---|---|
| `scripts/build_price_momentum_tw.py` | 新增。以 `build_price_momentum.py` 為底複製，只改第二節那三樣。 |
| `docs/research/price-momentum-tw/track.json` | 由 script 產生。本機先跑一次做 inception。 |
| `docs/research/price-momentum-tw/index.html` | 新增。以美股版 `index.html` 為底複製，改文案與欄位名。 |
| `.github/workflows/weekly-price-momentum-tw.yml` | 新增。每週六 01:08 UTC（台北 09:08），比美股 workflow 晚一小時，避免同一個 job 連發大批下載觸發 Yahoo 429。commit/push 段照抄美股 workflow。 |
| `scripts/site_nav.py` | `PREFIX_ACTIVE` 加一行 `("research/price-momentum-tw/", ("pick", None))`。 |
| `docs/index.html` | 選股欄加一個 li；新鮮度監視器加一條 `P10 台股`。 |
| `docs/cockpit/index.html` | 對照組區加一個 disc-link。 |
| `docs/research/price-momentum/index.html` | 副標尾端加一句連到台股版。 |

## 四、track.json 欄位差異

- `schema`: `price-momentum-tw-v1`
- `benchmark`: `0050.TW`
- `bench_close_inception` 取代 `spy_close_inception`
- `nav_series` 每列：`date, nav_L12, nav_L6, nav_bench, bench_close`
- `coverage` 多記 `listed_raw`（API 原始筆數）、`price_sufficient_all`（全部通過 253 筆者）、`universe`（流動性前 300）
- holdings 每筆多 `name`
- `prereg` 全文改寫成台股版，多一節 `market_adaptation` 說明三樣差異

## 五、fail-safe 門檻

- API 回傳 4 位數代碼少於 700 筆 → 中止。
- 通過 253 筆收盤者少於 250 檔 → 中止（流動性前 300 名補不滿也算）。
- 0050.TW 序列空 → 重試，用盡後中止。

## 六、頁面文案要點

- 標題：`P10 台股 · 雙線純價格動能 Paper Track`。
- 副標第一句講清楚：這是美股 P10 的台股鏡像，規則相同，只換名單與基準。
- 持股表顯示 `代號 簡稱`。
- 揭露三件事：0050 集中度、253 筆約 12.4 個月、上櫃不納入。
- 文字照 `~/.claude/skills/zh-analyst-prose/SKILL.md` 寫。
