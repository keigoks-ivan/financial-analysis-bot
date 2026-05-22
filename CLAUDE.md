# Repo-wide instructions

## Decision-time critic：思考產業 thesis 動部位前必先 spawn

當用戶討論以下任一情境，**必須先 spawn `industry-thesis-critic` sub-agent** 對相關 ID 跑冷讀，再給投資建議。這是 Boris verify-app pattern 在投資決策的翻譯 — 寫 ID 的 agent 與驗 thesis 的 agent 不同。

**觸發情境**（任一即觸發）：
- 「考慮加倉 / 減倉 / 新進 / 退出 X 產業 theme」
- 「{theme} thesis 還活著嗎」
- 「該不該對 {industry} 增加 / 降低曝險」
- 「{ID 主題} 現在還能 act 嗎」
- 用戶提及具體 ID 主題並表達決策意圖（不是純資訊查詢）

**Spawn 方式**：
```
Agent({
  description: "Cold review {theme} thesis",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "You are operating as the industry-thesis-critic sub-agent. Read spec at /Users/ivanchang/.claude/agents/industry-thesis-critic.md. ID: {path}. Intent: {user 意圖}. Save report to docs/id/_critic_{Theme}_{YYYYMMDD}.md."
})
```

**不觸發**（僅資訊查詢）：
- 「ID_X 寫了什麼」/「{theme} 是什麼」/「介紹一下 {industry}」 — 純解釋型問題，直接回答即可
- 寫稿過程中（that's a separate write-time critic, P2 未實作）

**例外**：用戶明確說「不用跑 critic」/「我自己看就好」可跳過。

## Site composition：4 repos 共同產生 docs/

公開站 `https://research.investmquest.com/` 由 4 個 repo 共同生成 `docs/` 內容。任何「整站樣板/頁首/頁尾」這類任務，第一步要先判斷該頁路徑屬於哪個 repo，再去對應 repo 改 generator template。

**速查**：
- `qgm/`、`qgm-tw/` → minervini-quality-backtest
- `briefing/YYYY-*`、`weekly/`、可能 `earnings/` 流程 → morning-briefing
- `backtest/`、可能 `six-state/` 報告檔 → v7-backtest
- 其餘（首頁、`earnings/`、`research/`、`pm/`、`dd/`、`id/`、`markets.html`、`sectors.html`、`screener*.html`、`how-to.html`、`briefing/index.html`、`six-state/index.html`）→ 本 repo

不確定時：`git -C <repo> log --oneline -- docs/<path>` 看哪個 repo 有歷史。改外部 repo 是新的 commit/push 範圍，**動手前先跟用戶確認**。

詳細 4-repo 表格 + 每個 repo 的 generator/workflow/commit author：見 `.claude/notes/site-composition.md`。

## Workflow: 每次 DD / DCA 必同步 research 頁（DD 組合快照）

任何 DD（`docs/dd/`）或 DCA（`docs/dca/`）的新增、修改、補 patch 後，**commit 前必跑** `python scripts/update_dd_index.py`，以同時更新：
- `docs/research/index.html` 主表（dd-tbody-v12 整段重生 from dd-meta JSON）
- DD 組合快照（DD_AUTO_STATS：訊號分布、最新 8 筆、PEG 便宜 top 5、5Y P/E 分位、2Y upside、X cohort 拆分、DCA Verdict 分布、護城河面板）
- 同跑 `DD_STALE_FRESH` / `PM_LAST_RUN` / `PM_HOLDINGS` / `PM_ACTIONS` 五段標記注入
- **自動觸發** `scripts/build_dd_screener.py`（rebuild `docs/dd-screener/latest.json`），讓 `/research/` 與 `/dd-screener/` 兩個頁面 universe 永遠一致。yfinance 失敗時 screener rebuild 會 warn 但不 abort research sync；要離線跑加 `--skip-dd-screener`。

把 `docs/research/index.html`、`docs/dd-screener/latest.json`、DD/DCA 新檔**併入同一 commit**，避免任一頁面滯後於底層報告。stock-analyst skill §2164 與 deep-conviction-analyst skill §68 已內建此步，但**手動 patch / 補 metadata / 改 DCA Verdict** 這類 skill-外路徑也必須遵守此規則。

## Workflow: push earnings / 發布財報

當用戶說「push earnings」/「發布財報」/「發佈財報」/「發布新財報」/「更新 earnings index」時，自動觸發 `push-earnings` skill（`.claude/skills/push-earnings/`），照其 9 個 steps 執行。

## Workflow: 30 天財報統整 (earnings synthesis)

當用戶說「跑最近財報的統整」/「earnings 統整」/「30 天財報統整」/「月度財報統整」/「財報季統整」/「過去 30 天財報重點」/「earnings synthesis」/「earnings monthly recap」/「earnings 30-day recap」/「monthly earnings rollup」時，自動觸發 `earnings-synthesis` skill（`.claude/skills/earnings-synthesis/`）。

**定位**：消費端 skill — 假設 `docs/earnings/earnings_YYYY-MM-DD.html` 30 天日報已存在。重點是把 vertical 日報串成 horizontal sector-level 敘事 + investment implication，不重做 per-company 分析。

**輸出**：
- HTML：`docs/earnings/synthesis_YYYY-MM-DD.html`（同階層；prefix `synthesis_` 不與日報 regex 衝突，push-earnings 不會誤抓）
- 索引：`docs/earnings/index.html` 在 hero 之後 / 日報列表之前插入 `<section id="monthly-synthesis">` highlight card（CSS 已預備在 index.html `.synthesis-tag` / `.synthesis-list` 規則）

**素材結構**：本地日報的 §2/§3/§4/§5 + lede + report-meta（複用 push-earnings 的 parsing 邏輯）+ **缺失交易日 web fill-gap**（mkt cap ≥ $50B 的當日 earnings，light WebFetch 取 EPS/rev/guidance/reaction）+ 中量 WebSearch / WebFetch（3-5 輪/主題）做趨勢深掘。Ticker → 子產業 mapping 走 `docs/id/ID_*.html` id-meta `related_tickers[]` 為主、`docs/dd/dd-meta` industry 補強、inline 硬表 fallback。本地深度料 vs web 補料在報告中**明確分色標示（`.source-local` 藍 vs `.source-webfill` 橘）+ 信心度註腳**，§6 add/cut/hold 建議只用本地深度料當主錨。

**Critic**：無強制 gate（v1 政策同 push-earnings）。用戶可在發布後手動跑 `id-review --mode synthesis`（未來 Phase 2 才有此 mode；現階段用一般 cold-review）。

**git flow**：commit 訊息格式 `Add earnings synthesis: window YYYY-MM-DD → YYYY-MM-DD`，直接 push main。

## Workflow: DCA 深度定見分析

當用戶說「幫我跑 {ticker} dca」/「{ticker} 定見」/「{ticker} dca」/「conviction analysis {ticker}」/「最終判斷 {ticker}」時，自動觸發 `deep-conviction-analyst` skill（`.claude/skills/deep-conviction-analyst/`）。

**定位**：DD 之上的「投資決策層」 — Phase A 三軸獨立搜尋（護城河 / 產業趨勢 / 業務財務） + Phase B 矛盾辨識與強制裁決 + Phase C PM 決策框架（§2 thesis、§7 倉位+opportunity cost、§5 single-thing、§6 pre-mortem）。

**輸出**：
- HTML：`docs/dca/DCA_{TICKER}_{YYYYMMDD}.html`（不放 `docs/dd/`，避免被 `validate_dd_meta.py` 鎖規則）
- 索引：`docs/dca/INDEX.md`（skill 自動 append）
- Research 頁同步：跑 `python scripts/update_dd_index.py` 後，「定見」欄會自動連到該 ticker 最新的 DCA 報告

## Workflow: 產業 DS（敘述型產業研究）

當用戶說「{主題} ds」/「ds {主題}」/「{產業} 敘述報告」/「分析 {產業} 的供需循環」/「{產業} 歷史與未來」/「discourse {industry}」時，自動觸發 `industry-ds` skill（`.claude/skills/industry-ds/`）。

**定位**：與 `industry-analyst`（產業 ID）並列的姊妹 skill — ID 給 PM 表格 dashboard 快速決策、DS 給供需循環敘事深度準備。同 theme 可並存（DS `ds-meta.related_ids[]` 指向同主題 ID，§0 顯示 cross-link callout）。

**章節骨架（不可動）**：§0 TL;DR → §1 歷史 → §2 現供 → §3 未供 → §4 現需 → §5 未需（含 TAM） → §6 短中長期推估 → §7 投資時鐘 → §8 Non-Consensus → §9 Kill Scenario → §10 Catalyst → §11 關聯個股。

**硬性比例**：文字 ≥ 80%、表格 ≤ 20%（與 ID 的 ≥ 70% 表格反過來）。表格上限 4 張，每張 ≤ 8 行。

**輸出**：
- HTML：`docs/ds/DS_{Theme}_{YYYYMMDD}.html`
- 索引：`docs/ds/INDEX.md` + `docs/ds/index.html`（skill 插入卡片到 subgroup-anchor 之後）
- 分類頁：跑 `python3 scripts/build_ds_category_pages.py` 重新生成 15 個 `docs/ds/cat-{mega}.html`
- 上站路徑：`https://research.investmquest.com/ds/`（與 `/id/` 並列）

**Plumbing**：
- `scripts/validate_ds_meta.py`：驗 `<script id="ds-meta">` 欄位（pre-commit hook 會跑）
- `scripts/build_ds_category_pages.py`：mirror `build_id_category_pages.py`，從 `docs/ds/index.html` 產 cat-*.html
- `scripts/init_ds_index.py`：一次性 bootstrap（從 `docs/id/index.html` 轉換出 `docs/ds/index.html`）
- Taxonomy：完全共用 ID（`docs/id/taxonomy.md` 是單一資料源；`validate_ds_meta.py` import `validate_id_meta.TAXONOMY`）

**Critic gate**：Step 8.7 強制 spawn `id-review` skill `--mode ds`（reuse 既有 id-review，加 6 條 DS-specific 檢查：表格比 / history-future causality / 供需平衡 / §6 三情境 / §10 雙路徑 / §11 一致性）。Critic report 放 `docs/ds/_critic_{Theme}_{YYYYMMDD}.md`。

## Workflow: 多股對比（multi-stock comparator）

當用戶說「比較 {T1} {T2} 用 DCA」/「比較 {T1} {T2} {T3} 看 DD」/「多檔比較」/「同類對比」/「該選哪一家」/「DCA 對比分析」時，自動觸發 `multi-stock-comparator-v1` skill（`.claude/skills/multi-stock-comparator-v1/`）。

**定位**：消費端 skill — 假設目標 ticker 的 DCA / DD 已存在（`docs/dca/` / `docs/dd/`），不自動觸發 `stock-analyst` 或 `deep-conviction-analyst`。對 2-5 檔執行四層時間框架（<12M / 2-3Y / 3-5Y / 5-10Y）橫向打分，每層獨立排序 + 判斷邏輯，最後給推薦標的 + 不選其他檔的具體理由。

**輸出**：
- HTML：`docs/comparisons/MS_{T1}vs{T2}_{YYYYMMDD}.html`（4 檔以上用底線連接：`MS_T1_T2_T3_T4_YYYYMMDD.html`）
- 索引：`docs/comparisons/index.html`（skill 在 `<ul class="reports">` 最上方 insert `<li>` 卡片；首份報告產出後自動移除 `.empty-state` div）
- 上站路徑：`https://research.investmquest.com/comparisons/`

**股價來源**：固定走 `WebSearch`（`scripts/fetch_prices.py` 是 weekly GitHub Actions batch，不收 ticker 參數，無法 ad-hoc）。報告日 >3 天時重抓現價並重算 Fwd PE / PEG（v1.3 無痕呈現規則）。

**Plumbing**：無 pre-commit validator（與 DCA 同政策）；無 build script（listing 是 skill-appended，類似 `push-earnings` 模式）；目前無 `push-comparisons` skill，git flow 是手動 `add / commit / push`。

## Git pre-commit hook

Repo 有 dd/id meta validator pre-commit hook。新 clone 啟用方式與 bypass 細節：見 `scripts/README.md`。
