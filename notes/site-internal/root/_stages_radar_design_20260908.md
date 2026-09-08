# 個股階段雷達（Stages）設計稿 — 2026-09-08

> 持有人拍板：把 RS+VCP screener 與轉強觀察接成同一條生命週期，不合成分數。規劃＝orchestrator（本檔），實作＝sonnet。前置：`screener.py` 三個 commit（下載韌性／VCP 閘加分／rs_ibd 平行欄）已落地。

## 0. 定位與治理

- 發現層描述器，與 `/screener.html`、`/rs-turn/` 同家族；**不是收斂面**：不跨階段總排名、不做 RS×VCP 加權、不進 picks／GRP／dd-screener／cockpit 名單。站內接線只有純連結。
- 描述器紀律：禁擇時結論、禁買賣指令語。階段是「現在在哪一段」，轉場基率是「過去 250 日內這一段的名字後來去了哪」。
- 參數集中 `PARAMS`＋`DEFINITION_VERSION="v1"`，history 逐日帶版號；不登記 rule_ledger（描述器參數）。
- legacy `rs_score` 家族（SOP 漏斗等消費者）**完全不動**；本頁只讀新欄位或自算。

## 1. 檔案落點

| 用途 | 路徑 |
|---|---|
| 共用價格核心（下載＋同 run 快取） | `scripts/tech_core.py` |
| 階段分類建置 | `scripts/build_stages.py` |
| 頁面 | `docs/stages/index.html` |
| 當日資料 | `docs/stages/data/latest.json` |
| 階段歷史（250 日整段重算） | `docs/stages/data/history.json` |
| 同 run 快取（gitignore） | `data/tech_core/cache/`（加進 `.gitignore`） |
| 排程 | `daily-us-close.yml` 在 `[rs-turn]` 之後加 `[stages]` step，PATHS 加 `docs/stages/data/` |

## 2. 共用價格核心 `tech_core.py`

- `download_prices(tickers, period="15mo", auto_adjust=<caller 指定>) -> DataFrame`（`group_by="ticker"` 形狀，與 `yf.download` 相同）：內部批 100＋4 次退避＋抖動（沿用 screener.py commit 1 的實作，把那段搬進來，screener.py 改 import；行為不變）。
- **同 run 快取**：以 `(ticker, auto_adjust)` 為鍵存 `data/tech_core/cache/{YYYY-MM-DD}_{adj|raw}.pkl`（pickle 的 per-ticker DataFrame dict）。呼叫時只下載快取缺的 ticker，再合併回傳。日期用 UTC 今日；CI 每次 runner 全新所以不會跨日汙染；本機舊快取由日期檔名自然失效（保留最近 2 天，其餘刪）。
- 消費者：`screener.py::fetch_all_data`（520 檔，band 早段）、`build_rs_turn.py`（約 1,400 檔，band 尾段，只補下載差集）、`build_stages.py`（零下載，全讀快取；快取缺就自己下載）。
- 驗收：`screener.py` 改接後 rs_score／rs_trend／combined 與改前同日輸出逐檔 diff＝0（下載資料相同的前提下）。

## 3. 階段定義（`build_stages.py`，全向量化，母體＝rs-turn 母體約 1,400 檔）

指標（寬表，日 t）：`C`、`E21`、`SMA50/150/200`、`rs21/rs63`（同 rs-turn）、`rs_ibd_pct`（IBD 加權報酬 `2·r63+r126+r189+r252` 當日全母體百分位，`rank(axis=1, pct=True)`）、`dist_52w_high`（vs 252 日最高收盤）、`low_52w_ratio = C / 252 日最低收盤`、`atr10/atr60` 比率（用 High/Low/Close）、`vol10/vol50` 比率、`RSI14`、`rs_line_high`（C/SPY 是否在 252 日高的 0.5% 內）。

Trend Template（五條，同 screener.py commit 2）：`C>SMA150>SMA200`、`SMA200 > SMA200.shift(21)`、`SMA50>SMA150`、`C ≥ 1.30×52w低`、`C ≥ 0.75×52w高`；`tt_pass_count` 0–5。

**階段（互斥，依此優先序判定，第一個成立者為準）**：

| 代碼 | 名稱 | 條件 |
|---|---|---|
| S4 | 領先 | `tt_pass_count==5` 且 `rs_ibd_pct ≥ 80` 且 `dist_52w_high ≥ −8%` |
| S3 | 收縮完成 | `tt_pass_count==5` 且 `dist_52w_high ≥ −8%` 且 `atr10/atr60 < 0.7` 且 `vol10/vol50 < 0.9`（VCP 向量化代理；完整 calc_vcp 閘只在 screener 頁） |
| S1 | 轉強 | rs-turn v2 六條件（import `build_rs_turn.PARAMS` 與同一套算式，勿複製數字） |
| S2 | 築底 | `C > SMA50` 且 `tt_pass_count ≥ 3` 且 `−25% ≤ dist_52w_high < −8%` |
| S0 | 弱勢 | `C < SMA50` 且 `C < SMA200` 且 `rs63 < 0` |
| S9 | 過渡 | 其餘 |

旗標（不是階段，可疊加）：`extended`＝`C/E21−1 > 15%` 或 `RSI14 > 80`；`rs_line_high`。流動性門檻同 rs-turn（ADV ≥ $20M、價 ≥ $5），不過者 S9 且不進表。

## 4. 歷史與轉場

- 對最近 250 個交易日整段重算（同 rs-turn 做法），`history.json`：
  ```json
  {"schema":"stages-history-v1","definition_version":"v1","updated":"…",
   "dates":["2025-09-05",…],
   "counts":{"S0":[…],"S1":[…],"S2":[…],"S3":[…],"S4":[…],"S9":[…]},  // 與 dates 等長
   "qqq":[…],
   "stages":{"SMCI":"9990011112223…"}   // 每檔一字串，每字元＝該日階段碼（0-4,9），與 dates 對齊
  }
  ```
  合併規則：窗口內整列覆蓋、窗口外舊資料保留；每檔字串長度必須等於 dates 長度。
- **每檔轉場欄**（寫進 latest.json rows）：`stage_since`（本段起始日）、`days_in_stage`、`prev_stage`、`prev_stage_ended`（幾天前）、`path`（最近三段代碼串，例如 `0→1→2`）。
- **轉場基率表**（latest.json `transitions`，由 history 回算）：對窗口內每一次「進入 S1」事件（前一日非 S1、且進入日距今 ≥ 60 日），統計 60 個交易日內是否曾到達 S3、S4、S0；輸出 `{"from":"S1","n":…, "to_S3_pct":…, "to_S4_pct":…, "to_S0_pct":…, "still_S1_or_S2_pct":…}`；同樣算 S2→S3／S4、S3→S4／S0。n < 20 的列標「樣本不足」。

## 5. `latest.json`

```json
{"schema":"stages-v1","definition_version":"v1","as_of":"…","run_timestamp":"…","benchmark":"QQQ",
 "params":{…},"universe":{"total":…, "eligible":…},
 "counts_today":{"S0":…,"S1":…,"S2":…,"S3":…,"S4":…,"S9":…},
 "transitions":[…],
 "rows":[{"ticker":"SMCI","stage":"S1","stage_name":"轉強","days_in_stage":10,"stage_since":"…",
          "prev_stage":"S0","prev_stage_ended":10,"path":"0→1",
          "rs_ibd_pct":72.3,"rs21":…,"rs63":…,"dist_52w_high_pct":…,"tt_pass_count":3,
          "atr_ratio":…,"vol_ratio":…,"extended":false,"rs_line_high":false,"adv20_usd":…,"price":…,
          "hub":"/t/SMCI.html"|null}]}
```
rows 只收 S1–S4（S0／S9 只進 counts）；每個階段內以 `days_in_stage` 升冪（最新進入者在前）排序，**不跨階段排名**。

## 6. 頁面 `docs/stages/index.html`

殼照 `docs/rs-turn/index.html`（同一家族），內嵌 SVG 折線同 rs-turn。

1. 標題「個股階段雷達（美股）」＋一句話：「同一檔股票通常會走過弱勢→轉強→築底→收縮完成→領先。這頁把美股約 1,400 檔每天各放進一段，看名單，也看每一段有幾檔。名單只回答『看誰』。」
2. **階段家數圖**：S1、S3、S4 三條線（可勾選 S0／S2），右軸 QQQ。白話：「轉強家數從低檔翻上、領先家數在掉，描述的是輪動早期；領先很多、轉強很少，描述的是後期。它描述現況，不預測轉折。」
3. **轉場基率表**：來源段、樣本數、60 日內到收縮完成％、到領先％、跌回弱勢％。白話註：「這是過去 250 個交易日回算，不是預測。」
4. **四個分頁**：轉強（S1）／築底（S2）／收縮完成（S3）／領先（S4）。表格欄：代號（hub 連結）｜在此階段天數｜來路（前一段＋幾天前，例「弱勢 → 10 天前」）｜RS 12 個月百分位｜距 52 週高｜Trend Template 過幾條｜ATR 比率｜量比｜旗標（延伸／RS 線新高）｜日均成交金額。
5. **階段定義說明**（六段白話＋數字），**緊接其後放一個「哪一段最有用」區塊**（持有人 2026-09-08 指定文案，照下面的意思寫、可微調語氣但四點與結語都要在，讀者導向、不出現「你的系統」這類內部指涉）：
   - 標題：「哪一段最有用，看你在問什麼」
   - **對「先決定值不值得擁有、再談進場」的長抱型組合，最有價值的正向碼是「轉強」。** 名字本來就在想擁有的名單上，剩下的問題只有「回檔是不是結束了」，轉強回答的正是這個。收縮完成與領先來得更晚，位置更差；領先幾乎等於市場已經定價。
   - **最有價值的警訊碼是「弱勢」。** 手上的核心持股掉進弱勢，是最便宜的論點複查觸發器，可以直接接到既有的證偽條件與持倉週掃，不用另建監測。
   - **對純技術交易者，最有價值的是「收縮完成」。** 它是最緊、最可證偽的狀態：關鍵價位明確、停損位置明確、幾週內就知道對錯，Minervini 的優勢全在這一段。但對以擁有為先的組合，它是次要的。
   - **真正的價值在轉場，不在單一階段。** 走完「弱勢→轉強→築底」這條路的名字，比任何一個靜態階段都有資訊，所以轉場基率表放在名單前面。
   - 結語（可證偽）：「這頁有沒有用，看兩個數字：轉強名單在 60 個交易日內走到收縮完成或領先的比例，應明顯高於全母體；跌回弱勢的比例，應明顯低於弱勢名單的續弱率。若沒有這個差距，轉強就只是雜訊。」——這兩個數字直接從上方轉場基率表讀，頁面要把對應的兩格用小字標出來。
   然後是「怎麼算」折疊區、提醒（同 rs-turn 段）。
6. 互連：本頁連 `/rs-turn/`（轉強細節）與 `/screener.html`（VCP 細節）；`/rs-turn/` 與 `/screener.html` 各加一句「看這檔在生命週期哪一段 → 個股階段雷達」連回。

文案鐵律同 `_plainlang_styleguide.md`；全形標點；禁流程劇場。

## 7. 接線

- `daily-us-close.yml`：`[stages]` step 緊接 `[rs-turn]` 之後（讀快取零下載），`continue-on-error`；PATHS 加 `docs/stages/data/`；檔頭對照表加一行。
- `.gitignore` 加 `data/tech_core/cache/`。
- `site_nav.py` PREFIX_ACTIVE `("stages/", ("pick", None))`；`screeners.html` 第六卡；cockpit 想法四路一行；`index.html` 選股卡（count +1）＋資料時效清單一條（`/stages/data/latest.json`，`as_of`）；`flow/index.html` 品質路、`how-to.html` 表格各一行；`data.html` 兩條端點。
- qc.py 全部觸及檔 0 錯；死連結 0。
- PATHS 另加 `docs/stages/data/lamp.json`（在 `docs/stages/data/` 內已涵蓋）。

## 7b. 席位榜「時機燈」欄（2026-09-08 持有人拍板：加燈、不進分數、不動排序）

- **資料**：`build_stages.py` 另寫 `docs/stages/data/lamp.json`：`{"as_of":"…","definition_version":"v1","lamp":{"NVDA":"S4","VRT":"S1",…}}`（全母體，含 S0／S9）。
- **建置期渲染**：`scripts/engine/build_arena.py` 的 `render_board_html`（HTML 看板）與 `render_board_text`（board.txt）在既有 R／P 燈號欄旁加一欄「時機」，值＝讀 `lamp.json` 的階段碼轉白話短標（弱勢／轉強／築底／收縮完成／領先／過渡；母體外顯示「—」）。HTML 版每個時機 cell 加 `data-lamp-ticker="{ticker}"` 屬性。**只加欄，不改 own_score、pass、遲滯、席位任何邏輯。** 因為 engine 是週更，這裡的值是建置當時的。
- **每日刷新**：`docs/cockpit/index.html` 與 `docs/engine/arena.html` 兩個真頁面（不是 innerHTML 片段）各加一段小 JS：載入看板片段後 `fetch('/stages/data/lamp.json')`，依 `data-lamp-ticker` 覆寫 cell 文字與 as-of 註記；404 時保留建置期值。
- **文案**：欄頭「時機」＋小字白話「這檔現在在生命週期哪一段，只是燈號，不影響排序」。階段短標配色沿用站上 token：領先／收縮完成＝pos、轉強＝accent、築底＝sec、弱勢＝neg、過渡＝muted。
- **驗收**：build_arena 本機重跑後 board.txt 與 HTML 看板 diff 只多一欄；own_score 排序前後逐檔相同；cockpit 頁 jsdom 載入 lamp.json 後 cell 被覆寫；lamp.json 缺檔不報錯。
- **注意**：`build_arena.py` 屬 weekly-engine 管線（`.github/workflows/weekly-engine.yml`），改完要用 `/tmp/ddvenv/bin/python scripts/engine/build_arena.py` 實跑一次驗證，但**不要**把重跑產生的 arena.json／scoreboard 等資料檔一起 commit（只 commit 程式碼與看板片段若有必要）；若重跑會改動 arena.json 快照，改用 `git add -p` 或只 add 程式碼檔。

## 8. 驗收

1. `tech_core` 接上後：先跑 `screener.py --quick`，再跑 `build_rs_turn.py`，確認第二支只下載差集（log 顯示快取命中數）；`build_stages.py` 零下載。
2. `screener.py` 接 tech_core 前後 rs_score／rs_trend／combined 逐檔 diff＝0。
3. 抽查 3 檔手算階段判定（一檔 S1、一檔 S4、一檔 S0）與 JSON 一致；`stages` 字串長度＝dates 長度。
4. 轉場基率表至少 S1 列 n ≥ 20（250 日窗口應足夠）；兩次重跑冪等。
5. 頁面四分頁、圖、表在 jsdom 無錯；latest 或 history 缺檔各自優雅降級。

## 9. 禁區

不動 `rs_score` 家族算式；不改 `calc_vcp`；不新開 workflow；不用 `git add -A`／stash／rebase；不在頁面渲染內部治理字眼。
