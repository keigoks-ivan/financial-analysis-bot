---
name: ddreport
version: v2.1
released: 2026-06-22
description: "單一指令跑完整條 DD→sync→commit pipeline。收到一個或多個 ticker 後，依序觸發 stock-analyst（現 v14.11，一號到底的單一報告：基本面 Part I + 決策層 Part II，統一裁決進場/觀望/迴避）→ python scripts/update_dd_index.py（同步 research 頁 + dd-screener + picks）→ size-floor gate（schema v13/v14 新檔 110KB）→ commit & push main。DCA 已併入單一 DD 報告，不再有獨立 deep-conviction-analyst 步驟（單一報告即含決策層）。可選自動偵測同產業 peer 一起跑。本 skill 是 thin orchestrator，不重做分析邏輯（那是 stock-analyst 的職責），只把固定鏈固化成一鍵。觸發：用戶說『跑 {ticker} ddreport』、『{ticker} 全套』、『{ticker} 走完整流程』、『ddreport {ticker}』、『/ddreport {ticker}』。若用戶只要單檔報告不要 commit，直接走 stock-analyst。"
---

# DD Report Pipeline（thin orchestrator，v2.1 — 單檔 DD）

把這條每次都重複的鏈固化成一鍵，並把 size-floor 與 sync 步驟內建，避免漏跑：

```
stock-analyst (v14.x DD，含決策層) → update_dd_index.py → size gate (110KB) → commit/push
```

**本 skill 不做分析** — 所有研究、決策層、品質規則都在 `stock-analyst`（現 v14.11，版號一號到底）裡。這裡只負責「順序、同步、閘門、提交」。**不再有獨立 DCA 步驟**：單一報告 `docs/dd/DD_*.html` 已內含 Part II 決策層（§12-§15）與統一裁決，不再產 `docs/dca/DCA_*.html`。

## Steps

1. **解析 ticker(s)**。模糊或不確定的 ticker **先問用戶**，不要瞎猜（memory `feedback_dca_session_pitfalls`）。
   - 開始前先 `git log --oneline -5` + `git status`，確認沒有並行 session 的背景動作 / orphan 檔（parallel-session git hygiene）。

2. **（可選）peer 自動偵測**。用戶給單一 ticker 且語氣是「這個 theme / 這群」時，可從 `docs/dd/` 同產業、或 `docs/id/ID_*.html` 的 `related_tickers[]` 帶出 1–3 檔 peer 一起跑（如 KLAC → ASML / LRCX）。**會擴張範圍時先跟用戶確認要不要連 peer**。

3. **決策意圖 → 先跑 critic**。若用戶語氣是「要不要加倉 / 新進 / 退出某 theme」這種**決策**（不是純研究），先按 repo 頂部「Decision-time critic」規則 spawn `industry-thesis-critic`，再產報告。純資訊查詢不觸發。

4. **跑 DD**：對每個 ticker 觸發 `stock-analyst`（現 v14.11；產出單一 `docs/dd/DD_{TICKER}_{YYYYMMDD}.html`，schema v14.x，含 dd-meta 決策層欄位 dca_verdict/dca_role/moat_trend/runway_post_y5/ev5y_pct + §14 `id="decision"` 錨點）。報告即含 Part II 決策層，**不需再跑獨立 DCA**。

5. **同步**：`python scripts/update_dd_index.py`（重生 research 主表 + DD 組合快照 + 自動連鎖 `build_dd_screener.py` rebuild `docs/dd-screener/latest.json` + `build_picks.py` 更新 `docs/picks/candidates.json`；報告由 script 直接讀 dd-meta dca 欄位，「定見」欄連 `/dd/DD_X.html#decision`）。離線 / yfinance 掛掉時加 `--skip-dd-screener`（會 warn 但不 abort）。

6. **Size-floor gate（pre-commit hook 也會擋，但這裡先自驗）**：新報告須 ≥ 110KB（gate 對 `"schema":"v1[34]` 檔生效；目標 ~110–125KB，Part I 基本面 ≥60%）。**未達不是去灌水**，而是回去把缺的量化模組補實（五個 v12.6 深度模組 + 四個決策模組的 sourced 數字、非段落注水；見 CLAUDE.md「Report 篇幅 floor」）。真要放行 lean-but-complete 報告才 `--no-verify`。

7. **commit & push**：把 `docs/dd/DD_*`、`docs/research/index.html`、`docs/dd-screener/latest.json`、`docs/picks/candidates.json` **併入同一 commit**（避免任一頁面滯後）。push 前重查 research / screener 沒被並行 session 覆蓋。commit message 沿用既有風格（如 `Add {TICKER} DD (統一裁決 ...); resync research+screener`）。

## 邊界

- 只要單檔報告（不 commit）→ 直接走 `stock-analyst`；多檔橫向對比 → 走 `multi-stock-comparator-v1`。本 skill 專門用於「同一 ticker 走完整 DD 報告 + 同步 + 提交」。
- **DCA 已退役**（併入單一 DD）；`deep-conviction-analyst` 是 deprecation stub，dca/定見 觸發語改觸發 `stock-analyst`。
- 不新增任何 validator / build script；step 5 的 `update_dd_index.py` 與 pre-commit hook 已涵蓋所有 plumbing。
