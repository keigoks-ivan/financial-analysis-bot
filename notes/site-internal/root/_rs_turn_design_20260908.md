# 轉強觀察（RS Turn）設計稿 — 2026-09-08

> 持有人需求：在站上做一個「剛從弱轉強」的美股技術面觀察名單（不是創新高／貼高的強勢股），加上一條**每天符合條件的家數**日線當寬度指標。規劃＝orchestrator（本檔），實作＝sonnet。

## 0. 定位與治理（先讀，這段決定了什麼能做、什麼不能做）

- **層級＝發現層技術雷達＋寬度描述器**，與 `scripts/screener.py`（RS+VCP）並列，是同一個「純技術結構雷達」家族的第二支鏡頭：RS+VCP 看「已經領先且波動收縮」，本頁看「曾經回檔、相對強度剛翻上來」。兩者刻意不合併。
- **不是收斂面**（2026-07-07 拍板不得再蓋新收斂面）：輸出**不進** picks／GRP 席位／三軌／dd-screener／cockpit 任何名單，不被任何 build 腳本 import。唯一的站內接線是兩個純連結：`docs/cockpit/index.html` 想法四路「品質路」欄加一行連結、`docs/screeners.html` 加一張卡片。
- **描述器紀律**：頁面文案只描述「今天有幾檔、誰在名單上、為什麼入選」，**禁擇時結論、禁買賣指令語**（比照 crowding／monitor 家族）。寬度線只說「家數從低檔翻上來代表一批股票同時轉強」這類機制陳述，不說「該進場」。
- **參數凍結**：所有門檻集中在 `PARAMS` 字典＋`DEFINITION_VERSION = "v1"`，寫進每份 JSON。門檻是描述器參數不是裁決閘，**不登記 rule_ledger**；但上線後不得靜默調參——調參要升版號，history 逐列帶版號。
- **市場範圍**：只做美股（S&P 500 ∪ Nasdaq-100 ∪ Russell 1000），與 2026-09-02「先只做美股」拍板一致。

## 1. 檔案落點

| 用途 | 路徑 |
|---|---|
| 建置腳本（零 LLM、pandas 向量化） | `scripts/build_rs_turn.py` |
| 母體快取（月更，commit） | `data/rs_turn/universe.json` |
| 頁面 | `docs/rs-turn/index.html` |
| 當日名單＋指標 | `docs/rs-turn/data/latest.json` |
| 寬度日線歷史（append／覆寫合併） | `docs/rs-turn/data/history.json` |
| 排程 | `.github/workflows/daily-us-close.yml` 新增一個 step（**不**開新 workflow，見 §7） |

不動任何既有 script 的邏輯；`site_nav.py`／`daily-us-close.yml`／`screeners.html`／`cockpit/index.html` 只做「加一行」級的接線。

## 2. 母體（universe）

**基底直接重用 `data/engine/universe.json`**（972 檔，`scripts/engine/build_universe.py` 月更：S&P 500 ∪ Nasdaq-100 ∪ S&P 400 ＋ DD 池美股；已 commit、有 fail-safe），**不要再寫第四支 S&P／NDX 爬蟲**。讀法：`[r["ticker"] for r in json["tickers"]]`。

**再聯集 Russell 1000（改用市值代理源，2026-09-08 校正）**——原帖名單裡 CRCL／BLSH／NBIS／GLXY／IREN／ALM／SNDK 這類新上市或未進 S&P 指數的名字，只有 R1000 收得到，正是這頁想抓的族群，所以不能省。Wikipedia 的 `Russell_1000_Index` 頁面實測已無成分股表格（只剩摘要／報酬率表），是死源；改用 Nasdaq 官方篩選器抓全美股名單、取市值前 1,300 檔當代理——R1000 本身定義就是「市值前約 1,000 大美股，每年 6 月重組」，但 Nasdaq 名單含 ADR 與非美國籍註冊公司這些 Russell 本身排除的名字，同樣取前 1,000 檔時市值門檻會落在約 $8B，明顯高於 R1000 實際門檻（約 $4-5B），故拉高到前 1,300 檔校正這個落差（PARAMS["r1000_proxy_n"]，2026-09-08 二次校正）。用同一把尺（市值排序）現抓一份是合理替代，不保證與官方成分股逐檔一致：
1. `GET https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=5000&offset=0&download=true`（headers：`User-Agent: Mozilla/5.0 (Macintosh)`、`Accept: application/json`；逾時 30 秒，失敗重試一次、隔 10 秒），取 `data.rows[]`（`symbol`／`name`／`marketCap` 等）。symbol 需符合 `^[A-Z]{1,5}$`（濾掉單位／權證／特別股／股類代碼帶 `^` `/` `.` 的列）；name 不得含 Warrant／Warrants／` Unit`／Units／Preferred／Depositary Shares／Depositary Receipt／` ETF`／Fund／Notes（保留 Trust，REIT 需要）；`marketCap` 需能轉成正浮點數。依市值降冪排序取前 1,300 檔，來源標記 `nasdaq-screener-top1300`。
2. 失敗改試 iShares IWB holdings CSV（`https://www.ishares.com/us/products/239707/ishares-russell-1000-etf/1467271812596.ajax?fileType=csv&fileName=IWB_holdings&dataType=fund`，跳過前置說明列、只取 `Asset Class == Equity`；本機測試會被導向 HTML 攔截頁，留作 GitHub Actions runner 上的第二層備援）。
3. 寫 `data/rs_turn/universe.json`：`{"fetched_at","n","sources":{"engine":972,"r1000":1300,"union":...},"r1000_source","r1000_tickers","tickers":[...]}`。Ticker 正規化：股類代碼帶點的美股（`BRK.B`／`BF.B`／`MOG.A`，樣式 `^[A-Z]+\.[A-Z]$`）→ `.`→`-`（engine 母體讀入時同步套用，修正先前 `BRK.B` 這類代碼因未轉換被 yfinance 判定不存在的問題）；其餘帶點／怪異後綴的代碼維持排除，不做轉換猜測。
4. **快取規則**：`fetched_at` 30 天內 → 不上網直接用；R1000 兩個來源都失敗 → 用舊快取的 R1000 部分；舊快取也沒有 → 只用 engine 母體並 `::warning::`。聯集 < 700 檔視為異常 abort（exit 0＋warning，不寫任何輸出）。

（註：engine 母體 v1.1 刻意排除 S&P 600 小型股；R1000 下緣市值約 $2B、不含真正小型股，與該決定不衝突。日均成交金額 ≥ $2,000 萬的流動性條件另外把尾端濾掉。）

## 3. 價格資料

- `yfinance` 日線，`period="2y"`、`interval="1d"`、`auto_adjust=True`，每批 100 檔一次 `yf.download(..., group_by="ticker", threads=True)`。**下載韌性直接照抄 `scripts/build_momentum5.py` docstring「DOWNLOAD RESILIENCE (2026-09-08 fix)」那套**：批 100、每批最多 4 次、指數退避約 20／60／150 秒＋抖動、覆蓋率地板、失敗 fail-safe exit 0 不碰輸出。同一個 band 已經有 screener.py 的 510 檔一次性下載，再加 1,000 檔就是 429 高風險區，所以本步驟**放在 band 最後一步**（monitor 之後），與 screener 的爆量隔開最遠。
- 為什麼不做持久化價格快取：本頁寬度線是「整段窗口重算」不是 append（§5），某天 429 跳過，隔天重算自然補回，不需要快取來保今天；1,000 檔 × 2 年日線 JSON 每日 commit 約 8MB，不值得。
- 額外抓基準 `QQQ`（本頁相對強度基準照原帖用 QQQ，與 screener.py 的 SPY 不同，寫進 `PARAMS["benchmark"]`）。
- 取 `Close`（已調整）、`Volume`。整理成寬表 `closes: DataFrame[date × ticker]`。
- **覆蓋率閘**：有 ≥ 260 根 K 的 ticker 佔母體 < 85% → abort（exit 0＋`::warning::`，不寫 latest／不動 history）。部分缺檔正常，寫進 `coverage` 欄。

## 4. 每檔指標（as of 日 t，全部用調整後收盤價）

符號：`C` 收盤、`E21`／`E50`＝21／50 日 EMA（指數移動平均，`ewm(span=n, adjust=False)`）、`Q` QQQ 收盤。

| 欄位 | 定義 |
|---|---|
| `rs21` | `((C_t/C_{t-21} − 1) − (Q_t/Q_{t-21} − 1)) × 100`，單位 pt |
| `rs63` | 同上換 63 日 |
| `rs_accel` | `rs21 − rs63`（pt）——原帖的「RS +41.2pt」就是這個差 |
| `dist_high_pct` | `(C_t / max(C_{t-251..t}) − 1) × 100`，負值；頁面顯示「距 52 週高 33%」＝其絕對值 |
| `pullback_pct` | `(min(C_{t-62..t}) / max(C_{t-251..t}) − 1) × 100`，負值＝近一季最深回檔 |
| `above_e21` | `C_t > E21_t` |
| `e21_up` | `E21_t > E21_{t-5}` |
| `reclaimed_e21` | `above_e21` 且 `t-10..t-1` 之間至少一天 `C < E21` |
| `crossed_e50` | `C_t > E50_t` 且 `t-10..t-1` 之間至少一天 `C < E50` |
| `near_e50` | `abs(C_t/E50_t − 1) ≤ 0.03` |
| `higher_low` | `min(C_{t-9..t}) > min(C_{t-29..t-10})` |
| `range_pos` | `(C_t − min63) / (max63 − min63)`，63 日區間位置 0–1 |
| `adv20_usd` | `mean(C × Volume, 20)` |

**六條件（全部成立才入榜）**，門檻集中在 `PARAMS`：

1. RS 加速：`rs21 > 0` 且 `rs_accel ≥ 10`
2. 曾明顯回檔：`pullback_pct ≤ −15`
3. 均線結構轉佳：`above_e21` 且（`reclaimed_e21` 或 `e21_up`）
4. 價格結構改善：`higher_low` 或 `range_pos ≥ 0.7`
5. 還沒貼高：`dist_high_pct ≤ −8`
6. 流動性：`adv20_usd ≥ 2e7` 且 `C_t ≥ 5`

**狀態標籤**：`rs_accel ≥ 20` 且 `e21_up` → 「偏加速中」；否則「逐漸轉強」。

**入選原因 tags（頁面「為什麼入選」欄，依序最多 4 個，用「；」接）**：
- `pullback_pct ≤ −25` → 「深回檔後相對強度急拉」，否則 「回檔後相對強度改善」
- `reclaimed_e21` → 「剛站回 21 日線」；否則 `e21_up` → 「21 日線拐頭向上」
- `crossed_e50` → 「剛穿 50 日線」；否則 `near_e50` → 「貼近 50 日線」
- `higher_low` → 「低點抬高」；否則 `range_pos ≥ 0.7` → 「靠近整理區上沿」

**排序**：`rs_accel` 由大到小；`latest.json` 寫全部通過者，頁面預設顯示前 30、可展開全部。

**連續在榜天數**：從 `history.json` 各日 `members` 回推（含今日），今天首次出現 → `days_on_list = 1` 並標 🆕。

## 5. 寬度指標（家數日線）

- 對最近 **250 個交易日**每一天 t，用同一套向量化計算算出：
  - `n_full`：六條件全過的家數（主線）
  - `n_soft`：`rs_accel > 0` 且 `above_e21` 的家數（較寬鬆的「轉強苗頭」副線）
  - `n_eligible`：該日資料足夠（≥ 252 根）且流動性過關的家數（分母）
  - `pct_full = n_full / n_eligible × 100`
  - `qqq`：QQQ 收盤（頁面副軸疊圖）
  - `members`：當日 `n_full` 的 ticker 陣列（供連續在榜天數、新進／掉榜、日後回測命中率用）
- **每次執行整段重算**（不是只 append 今天）：`history.json` 合併規則＝重算窗口內的日期整列覆蓋、窗口外的舊列保留；每個日期在 `version_by_date` 記 `DEFINITION_VERSION`。定義升版時窗口內自動重寫，窗口外舊版日期頁面標灰。
- 2y 資料扣掉 252 日 lookback 剛好約 250 日可算；資料不足的早期日期不寫。

## 6. JSON schema

`docs/rs-turn/data/latest.json`
```json
{
  "schema": "rs-turn-v1",
  "definition_version": "v1",
  "as_of": "2026-09-04",
  "run_timestamp": "2026-09-05T22:10:00+00:00",
  "benchmark": "QQQ",
  "params": {"rs_accel_min": 10, "rs21_min": 0, "pullback_min_pct": -15, "dist_high_max_pct": -8, "range_pos_min": 0.7, "adv_min_usd": 20000000, "price_min": 5, "accel_label_min": 20},
  "universe": {"total": 1010, "covered": 985, "eligible": 940, "sources": {"engine": 972, "r1000": 1005, "union": 1080}},
  "breadth_today": {"n_full": 15, "n_soft": 212, "n_eligible": 940, "pct_full": 1.6, "n_full_ma20": 9.4, "n_full_pctile_250d": 78},
  "changes": {"new": ["SMCI"], "dropped": ["XYZ"]},
  "rows": [
    {"rank": 1, "ticker": "SMCI", "status": "偏加速中", "tags": ["深回檔後相對強度急拉", "21 日線拐頭向上"],
     "rs_accel": 41.2, "rs21": 28.0, "rs63": -13.2, "dist_high_pct": -33.1, "pullback_pct": -41.0,
     "range_pos": 0.82, "adv20_usd": 2.1e9, "price": 45.2, "days_on_list": 1, "is_new": true, "hub": "/t/SMCI.html"}
  ]
}
```
`hub` 只在 `docs/t/{TICKER}.html` 存在時填，否則 `null`。

`docs/rs-turn/data/history.json`（`series` 形狀對齊 `docs/monitor/data/score_history.json`／`internals_history.json` 的 `[[date, value], ...]`，讓 monitor 頁的 SVG 折線程式碼可以直接搬）
```json
{"schema": "rs-turn-history-v1", "benchmark": "QQQ", "updated": "2026-09-04", "definition_version": "v1",
 "series": {"n_full": [["2025-09-05", 4]], "n_soft": [["2025-09-05", 150]], "n_eligible": [["2025-09-05", 930]],
            "pct_full": [["2025-09-05", 0.4]], "qqq": [["2025-09-05", 480.1]]},
 "version_by_date": {"2025-09-05": "v1"},
 "members": {"2025-09-05": ["A", "B"]}}
```

## 7. 排程接線

`daily-us-close.yml`（時段帶 A，2026-07-18 起所有美股收盤後 job 都收在這裡，**不開新 workflow**）：
- 加一個 step：
  ```yaml
  - name: "[rs-turn] Build turning-strong screener + breadth"
    continue-on-error: true
    run: python scripts/build_rs_turn.py || echo "::warning::rs-turn build failed; band unaffected"
  ```
  **位置：band 的最後一個 build 步驟（`[monitor] Build home pulse` 之後、`Commit and push` 之前）**，理由見 §3。`continue-on-error` 寫法照檔內其他步驟。
- `PATHS` 迴圈加 `docs/rs-turn/data/` 與 `data/rs_turn/universe.json`。
- 依賴：band 已裝 `yfinance pandas numpy requests lxml`，不需加。
- 檔頭「整合對照表」註解加一行本步驟。

## 8. 頁面規格（`docs/rs-turn/index.html`）

**殼**：靜態 HTML＋內嵌 JS `fetch('./data/latest.json')`／`fetch('./data/history.json')`；任一 404 或 parse 失敗 → 該區塊顯示「資料尚未產出」不整頁壞。沿用站內共用 CSS 變數（`--ink`／`--sec`／`--muted`／`--card`／`--paper`／`--line`／`--pos`／`--neg`／`--warn`）；**頁殼照 `docs/screeners.html`（現行 cream／navy 版，`<link rel="stylesheet" href="/assets/imq-base.css">`），不要照 `docs/screener.html`（舊藍版）**；圖表**不用外部 chart 函式庫**，照 `docs/monitor/index.html` 的 `score_history` 區塊（`renderScoreChart`＋crosshair＋tooltip＋touch）搬內嵌 SVG 折線做法。nav 由 `scripts/site_nav.py` 注入（見 §9）。

**文案鐵律**（`notes/site-internal/root/_plainlang_styleguide.md` 三條鐵律＋全形標點＋禁流程劇場）：白話為主、術語括號註解且第一次出現要寫（例：「21 日 EMA（指數移動平均，近期價格權重較高的均線）」）；不渲染 QC 代號、版本沿革、內部 agent 名稱；全形標點。

**區塊順序**：

1. **標題與一句話定位**：「轉強觀察（美股）」。副標：「不是追已經飆到高點的股票，是找剛從弱轉強的：先明顯回檔過，最近一個月相對 QQQ 的強度明顯改善，均線和價格結構開始抬升，離 52 週高還有一段距離。名單只回答『看誰』，不回答『買不買』。」
2. **寬度：每天有幾檔在轉強**：四個小格（今日家數／20 日均／250 日分位／佔母體％）＋SVG 折線：主線 `n_full`（實線）、副線 `n_soft`（淡色，可勾選隱藏）、右軸 QQQ（灰細線）。下方一段白話：「這條線算的是每天有幾檔符合全部條件。家數從低檔翻上來，代表回檔後有一批股票同時轉強；家數已經很高，代表轉強變得普遍，不再是早期。它描述現況，不預測轉折時點。」定義版本不同的舊列以淡色標示並註明「舊定義」。
3. **今日名單**：表格欄位＝排名｜代號（有 `hub` 就連 `/t/{T}.html`）｜狀態｜為什麼入選｜RS 加速（pt）｜近 21 日 RS｜近 63 日 RS｜距 52 週高｜回檔深度｜在榜天數（🆕）｜日均成交金額。預設前 30，「展開全部」按鈕。表頭 `title` 可疊加進階說明，但白話必須肉眼可見（欄名本身就是白話）。
4. **今日變化**：新進榜／掉榜兩列 ticker。
5. **條件說明**：六條件逐條白話＋數字（例：「①相對強度在加速：近 21 日相對 QQQ 的報酬，比近 63 日的高出 10 個百分點以上，而且近 21 日本身要贏 QQQ」）。附「怎麼算」折疊區放公式與母體來源、as-of、覆蓋率。
6. **提醒**（照原帖精神）：「這是技術面觀察清單，不是買進建議，也不是說現在就要追。轉強不等於一定續漲，假突破、二次回測失敗都很常見。進場前要自己看風險、部位與出場規則。」

## 9. 站內接線與檢查清單

- `scripts/site_nav.py`：`PREFIX_ACTIVE` 加 `("rs-turn/", ("pick", None))`（歸選股群高亮、不佔頂層下拉席位，與 screener 家族同待遇）；新頁跑一次 site_nav 注入 nav（先看該腳本的單檔／check 模式怎麼用，不要全站重跑造成無關 diff——若全站重跑無 diff 就沒關係）。
- `docs/screeners.html`：四張卡片後加第五張卡片「轉強觀察（美股）」，一句話：「曾經回檔、相對強度剛翻上來的名單，附每天符合家數的寬度線」。
- `docs/cockpit/index.html` 品質路欄：`RS+VCP Screener` 那行之後加 `<a class="disc-link" href="/rs-turn/">轉強觀察<small>回檔後相對強度剛翻上來</small></a>`。
- `docs/data.html`：公開資料端點表加 `/rs-turn/data/latest.json` 與 `/rs-turn/data/history.json` 兩條（照既有 `.dt-ep-head`／`.dt-path`／`.dt-purpose`／`.dt-note` 區塊格式）。
- `python3 scripts/qc.py`（changed-files 模式）必須 exit 0；**新檔每一行都算新增行，全形標點與死連結一條都不能漏**（中文字後接半形 `,` `.` `:` 即錯；JS 字串因在 `<script>` 內豁免）。
- pre-commit hook：`docs/.nojekyll` 不動；新目錄不落任何 fixture。
- 既有閘掃描面自檢（CLAUDE.md 2026-09-07 條）：本頁不是 DD 產物，`verify_dd_math`／dd size floor／meta validator 皆不適用；`qc.py` changed-files 模式會掃到新 HTML——這是唯一相關的閘，必須通過。

## 10. 驗收（sonnet 交付前自己做完，結果寫進回報）

1. 本機用 `/tmp/ddvenv/bin/python`（py3.12＋yfinance 1.7＋pandas 3.0）跑 `scripts/build_rs_turn.py` 一次成功，回報：母體大小、覆蓋率、`n_full`／`n_soft`、前 15 檔 ticker 與 `rs_accel`。
2. **抽查 3 檔手算**：任選榜上 3 檔，用 `closes` 直接算 `rs21`／`rs63`／`dist_high_pct`，與 JSON 相符（容差 0.1）。
3. `history.json` 有約 250 列、日期單調遞增、無重複；重跑一次第二次輸出與第一次逐列相同（冪等）。
4. 用 `python3 -m http.server` 開 `docs/` 看 `/rs-turn/` 頁：圖有畫、表有列、刻意把 `history.json` 改名後頁面只有寬度區顯示「資料尚未產出」。
5. `python3 scripts/qc.py` exit 0。
6. `git status` 只出現：`scripts/build_rs_turn.py`、`docs/rs-turn/`、`data/rs_turn/universe.json`、`daily-us-close.yml`、`site_nav.py`、`screeners.html`、`cockpit/index.html`、以及 site_nav 注入產生的 nav diff（若有）。**不 commit、不 push**，停在這裡回報。

## 11. 禁區

- 不改 `scripts/screener.py`、`build_prices_cache.py` 或任何既有 build 腳本邏輯。
- 不新開 workflow 檔。
- 不把本頁輸出接進任何名單型頁面（picks／engine／dd-screener／intel／market）。
- 不用 `git add -A`；不 stash；不 rebase（並行 session 規範）。
- 不在頁面渲染內部治理字眼（QC、skill、agent 名）。
