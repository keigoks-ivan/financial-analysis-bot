# 實單主系統改規則 ＋ 實單頁重做（2026-09-15 持有人拍板）

持有人 2026-09-15 決定三件事，本檔是規格與分工。兩階段執行，第一階段推上線後才做第二階段。

1. 實單主系統的股票腿改成「cap 1.5 ＋ 日線均線確認（1% 遲滯）」。
2. 實單頁加一個「F70 均線版」區塊（股票腿 70% ＋ TLT／GLD／DBC 30%）。
3. 實單頁整頁重做，圖表改成 TradingView 那種樣式。

## 0. 為什麼現在改（決策紀錄）

- 持有人自陳：實單上線後，跌中還開槓桿的日子曾想手動減碼。會被干預的規則，回測數字不算數。把「不在跌中借錢」寫進規則，比事後偷偷減碼誠實。
- 回測（v7 `results/vol_targeting/w52_adaptive_ma_confirm_lag20_buf1.json`，斜率 lag 20、價格條件 1% 遲滯，含執行層 A2）：美股年化 14.1% → 13.9%，最大回撤 −23.7% → −23.0%，跌中持有超過 100% 的天數 591 → 369。台股年化 23.3% → 22.7%，回撤不變，跌中槓桿天數 339 → 170。
- 同日另外測過的階梯上限、分數乘法、100% 以下退場，全部比簡單版差，不採用（`run_w52_adaptive_ma_ladder.py`）。
- F70 組合換腿：年化 13.3% → 12.9%，回撤 −15.6% → −15.2%（`run_f70_ma.py`）。組合層面兩版幾乎相同。
- 我（協調者）當時建議等 10 月回顧點再換。持有人看完階梯版與 F70 數字後決定現在換。這是持有人的決定，照做，但流程要完整：帳本登記、舊規則轉影子、kill condition 預註冊。

## 1. 規則定義（凍結，改動＝改規則）

每腿每日：

- W52 週線閘門：不變。
- 自適應套袖：`raw = σ_t / RV20`，`σ_t` ＝ RV20 的 rolling(756, min_periods=252) 中位數，不變。
- **均線確認（新）**：五條件——收 > MA60、收 > MA120、收 > MA200、MA120 > 20 日前、MA200 > 20 日前。三個價格條件各加 1% 遲滯：目前為關，收 > MA 才轉開；目前為開，收 < MA×0.99 才轉關；中間沿用前一日。斜率條件不加遲滯。五條全開 → `cap_eff = 1.5`，否則 `cap_eff = 1.0`。MA 未暖機視為不全開。
- 套袖權重：`w = min(cap_eff, raw)`。
- 執行層 A2：20pp 門檻、10% 取整、clamp 75pp，不變。
- 成本、t+1、台股現金 1%：不變。

向量化定義逐位元對齊 `scripts/update_long_track_w52_adaptive_ma_confirm.py` 的 `_hyst` 與 `_ma_conditions`。

## 2. 第一階段：改規則（engine）

負責檔案（fab）：

| 動作 | 檔案 |
|---|---|
| 改 | `scripts/update_long_track_w52_adaptive.py`（實單主系統） |
| 改 | `docs/long-track-w52-adaptive/state.json`（只由腳本寫，人工不動） |
| 新 | `scripts/update_long_track_w52_adaptive_noma.py`（舊規則影子，由 ma_confirm 腳本改名改造） |
| 退役 | `scripts/update_long_track_w52_adaptive_ma_confirm.py`、`docs/long-track-w52-adaptive/ma-confirm.html`、`ma_confirm_state.json` |
| 改 | `.github/workflows/update_long_track_w52_adaptive.yml` |
| 改 | `scripts/build_long_track_index.py` ＋重建 `docs/long-track/index.html` |
| 改 | `scripts/build_live_scoreboard.py`（PREREG amendments 加一條說明，SPRT 參數不動） |
| 改 | `knowledge/rule_ledger.md`（實單主系統規則鏈那一列加修訂與 kill condition） |
| 改 | `tools/tradingview/w52_adaptive_vt.pine`（只改 tooltip 文字：實單已含均線層） |
| 複製 | v7 `src/vol_target_backtest/` 對應副本 |

### 2.1 實單主系統腳本的改法

- 加 `_hyst`、`_ma_conditions`、`MA_BUF = 0.01`、`MA_LAG = 20`、`RULE_TAG = "w52a_ma_h1"`。
- `_sleeve_from` 回傳多 `ma5_on`、`cap_eff`；`sleeve_state` 與 `_daily_record` 每腿多存 `ma5_on`、`cap_eff`、`ma_cond`（五個布林）、`rule`。
- **歷史不重算**：`state.json` 的 `history_us`／`history_tw` 既有紀錄一筆不動（2026-07-18 切換時的同一條紀律）。2026-09-15 起新紀錄帶 `rule: "w52a_ma_h1"`，舊紀錄沒有這個欄位就視為舊規則。`band_exec_replay` 照舊從全 history 重放，現持自然接續。
- `docstring`、頁首規則說明、email 內文與 `build_mail_html` 都要提到均線層與 `cap_eff`。email 主旨不變。
- 「可行動變化」的定義不變（閘門翻轉或執行層變動 ≥10pp）。`detect_changes` 多報一種：任一腿 `cap_eff` 翻轉，但這種只寫進 email 內文的說明，不單獨觸發 email。
- 回測常數：`BT_US`／`BT_TW`／`LEV` 加一列「W52×自適應×均線確認＋執行層（本頁追蹤，2026-09-15 起）」，數字轉錄自 `w52_adaptive_ma_confirm_lag20_buf1.json`，舊列保留當對照並改標「舊實單規則（2026-07-18～2026-09-14）」。
- `FREEZE_DATE` 保留，另加 `RULE_REVISION_DATE = "2026-09-15"`。

### 2.2 舊規則影子

- 把 `update_long_track_w52_adaptive_ma_confirm.py` 改名為 `update_long_track_w52_adaptive_noma.py`，均線層拿掉（`cap_eff` 恆 1.5），輸出 `noma.html`／`noma_state.json`，docstring 寫清楚：這是 2026-07-18～2026-09-14 的實單規則，2026-09-15 起降為影子，供均線層 kill condition 對帳。
- 歷史：從主系統 `state.json` 複製 `history_us`／`history_tw` 當起始（那本來就是舊規則的紀錄），之後每日追加。
- `ma-confirm.html` 改成 redirect stub → `/long-track/#live`。`ma_confirm_state.json` 刪除。CI 的 step 與 `git add` 對應更新。
- `build_long_track_index.py`：「影子對照」組加「舊實單規則 cap 1.5 無均線層」；「前瞻候選」組刪掉 ma-confirm 那一筆；實單主系統卡片文字改成含均線層、2026-09-15 修訂。

### 2.3 帳本（rule_ledger.md）

在「實單主系統規則鏈」那一列加修訂紀錄，內容照 §0 與 §1，kill condition 預註冊如下，不得改：

- (d) 均線層 kill：自 2026-09-15 起前瞻 250 個交易日，若實單（含均線層）年化落後舊規則影子超過 3 個百分點，且「跌中持有超過 100% 的天數」沒有少於舊規則影子的一半 → 均線層撤回，實單復歸舊規則。
- (e) 抖動 kill：任一腿 60 個交易日內 `cap_eff` 翻轉 ≥ 6 次 → 遲滯參數送 10 月回顧點檢討；連兩季 → 均線層撤回。
- 檢查點：2026-10 回顧點與其後每季，與既有 (a)(b)(c) 一起看。

### 2.4 驗證（第一階段交付前）

1. 主系統腳本本機跑成功兩次，`history` 長度不變（冪等）；舊紀錄逐筆與改前的 `state.json` 相同（用 git 的上一版比對）。
2. 今日新紀錄的 `sleeve`：`ma5_on` 為真時等於 `min(1.5, raw)`，為假時等於 `min(1.0, raw)`；與退役前 `ma_confirm_state.json` 今日那筆逐腿相同。
3. 舊規則影子今日 `sleeve` 等於改前主系統會算出的值（用 git 上一版腳本跑一次對照）。
4. `ast.parse` 兩支腳本；yml 用 yaml 載入；`build_long_track_index.py` 重建成功。
5. `_body.html` 生成後用瀏覽器或 python 檢查沒有 `None%`、`{{`。
6. 兩 repo 副本逐位元相同。

## 3. 第二階段：頁面重做（含 F70 均線版）

### 3.1 版面（由上到下）

1. **今天結論條**：兩市場並排。每市場一個大數字（現持曝險 %）、目標 %、閘門狀態、均線 x/5、`cap_eff`、下一個會動的價位（例如「QQQ 跌破 705 上限降回 1.0」）。一眼看完。
2. **主圖（TradingView 樣式）**：每市場一張，用 Lightweight Charts（TradingView 開源圖表庫，`https://unpkg.com/lightweight-charts@5/dist/lightweight-charts.standalone.production.js`，非 Artifact 不受 CSP 限制）。三個 pane 垂直排：
   - pane 1：兩腿價格（線圖，各自正規化為 100）＋ 各腿 W52 線；閘門出場區底色淡紅；`cap_eff` 被壓到 1.0 的區間底色淡紫。
   - pane 2：現持曝險（階梯線，粗）＋ 每日理論目標（細線）；100% 與 150% 水平參考線；2026-09-15 規則修訂處一條垂直標記。
   - pane 3：RV20 與 σ_t 兩線（每腿各一組顏色）。
   - 十字線、hover 圖例（日期、各數值）、時間軸可拖可縮、預設顯示近一年、按鈕切 1Y／3Y／5Y。深淺色跟站台變數。
   - 資料：`history` 的 1260 筆（已含 rv20／sigma_t／raw_ratio／final_pct／executed_pct），價格線要在生成時把每腿近 1260 日收盤（正規化）與 W52 一起嵌進 JSON。
3. **每腿卡片**：一列四張（QQQ、SMH、0050、2330），每張只放：閘門、收／W52 距離、均線五燈、`cap_eff`、raw、套袖、目標 pp、現持 pp。不放八週表。八週閘門軌跡收進 `<details>`。
4. **F70 均線版**（標「紙上候選・尚非實單」，因為 TLT／GLD／DBC 三腿仍是紙上）：一張表，帳戶層權重＝股票腿現持 × 70% ＋ 每腿 D1X 部位 × 30% × 1/3。D1X 部位讀 `docs/long-track/f70_signal_state.json` 最新一筆（顯示 as-of 日期；CI 裡 F70 alert 在主系統之後跑，資料可能晚一天，頁面要註明）。列：QQQ、SMH、TLT、GLD、DBC、現金、合計曝險。旁邊一句「月底再平衡回 70／30」與下一個月底日期。
5. **最近一年執行層事件表**：保留，瘦身成日期、腿、舊→新、原因四欄。
6. **回測與統計**：全部收進一個 `<details>`（回測堆疊表、逐年、分期、曝險分布、利差敏感度、壓力統計）。預設收起。
7. **規則說明**：一個 `<details>`，§1 的文字白話版，含 2026-09-15 修訂紀錄與 kill condition。

### 3.2 技術限制

- 仍是 `_body.html` nav-less 片段，被 `/long-track/index.html` 以 iframe 嵌入，父頁用 `scrollHeight` 撐高度。Lightweight Charts 要在 iframe 內用固定像素高度（每 pane 指定高度），不能依賴視窗高度。時間軸互動在 iframe 內要能拖。
- 文字照 `~/.claude/skills/zh-analyst-prose/SKILL.md`：結論先行、不用比喻、一段一個論點、術語第一次出現白話解釋。
- 不改任何規則邏輯。第二階段只動 `generate_html`／`market_html`／`market_js`／`_market_data` 這些呈現函式與 CSS。動到規則函式視為錯誤。
- 舊規則影子 `noma.html` 與 cap 1.0 影子 `leverage.html` 不重做，維持原樣。

### 3.3 驗證

1. 本機生成後用 Chrome 開 `docs/long-track/index.html#live`，截圖確認三個 pane 顯示、hover 有數值、切 1Y／3Y／5Y 正常、iframe 高度撐開沒被截。
2. 手機寬度（400px）不橫向捲動。
3. F70 表的合計＝各列加總；D1X 三腿部位與 `f70_signal_state.json` 最新一筆一致。
4. 生成兩次內容相同（除 generated_at）。

## 4. 連結（持有人 2026-09-15 補：「連結都要設好，所有的」）

兩階段都適用。交付前要跑一次連結稽核：把 `_body.html`、`noma.html`、`leverage.html`、`tw-semivol.html`、`ma-confirm.html`（stub）、`docs/long-track/index.html` 裡所有 `href` 抓出來，站內路徑逐一確認檔案存在（`docs/` 下對應路徑），站外只確認格式。任何指到已退役檔或不存在檔的連結都算錯。

必須存在且正確的連結：

- 實單頁 → 舊規則影子 `noma.html`、cap 1.0 影子 `leverage.html`、台股 B-ii 影子 `tw-semivol.html`、主控台 `/long-track/`、記分板 `/long-track/#scoreboard`、證據總覽 `/backtest/live_system_evidence/`、F70 研究頁 `/backtest/f_comfort/`。
- F70 均線版區塊 → `/backtest/f_comfort/`、記分板 S-F70。
- 主控台卡片 → 實單頁 `/long-track-w52-adaptive/`（redirect 到 `#live`）、各影子頁、退役卡。
- 三個影子頁與 stub → 回實單 `/long-track/#live`。
- `ma-confirm.html` stub → `/long-track/#live`（meta refresh ＋ 一行文字連結）。
- 規則說明 `<details>` 內 → 帳本不公開，不放連結；回測 JSON 在 v7 不公開，不放連結，只寫檔名。
