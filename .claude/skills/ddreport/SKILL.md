---
name: ddreport
version: v2.2
released: 2026-09-03
description: "單一指令跑完整條 DD→sync→commit pipeline。收到一個或多個 ticker 後，依序觸發 stock-analyst（現 v15.2，一號到底的單一報告；報告端 schema 仍 v15.0：商業本質優先章序，writer 只產 BODY 檔、`render_dd.py` 組裝＋四支驗證）→ 寫稿後獨立 critic（opus，讀 `dd_sections.py text` 全文）→ patch agent（sonnet，乾淨 context，`extract`/`replace` 修 🔴🟡）→ 需要時 critic re-gate → patch 第二輪 → python scripts/update_dd_index.py（同步 research 頁 + dd-screener + picks）→ size-budget gate（schema v15 新檔 70KB 下界·115KB 上界警告，`dd_sections.py bytes` 分章 WARN）→ commit & push main。DCA 已併入單一 DD 報告，不再有獨立 deep-conviction-analyst 步驟（單一報告即含決策層）。可選自動偵測同產業 peer 一起跑。本 skill 是 thin orchestrator，不重做分析邏輯（那是 stock-analyst 的職責），只把固定鏈固化成一鍵。觸發：用戶說『跑 {ticker} ddreport』、『{ticker} 全套』、『{ticker} 走完整流程』、『ddreport {ticker}』、『/ddreport {ticker}』。若用戶只要單檔報告不要 commit，直接走 stock-analyst。"
---

# DD Report Pipeline（thin orchestrator，v2.2 — 單檔 DD）

把這條每次都重複的鏈固化成一鍵，並把 writer→critic→patch 鏈、size-floor 與 sync 步驟內建，避免漏跑：

```
stock-analyst writer（sonnet，BODY 檔一次 Write→render_dd→四支驗證） → 獨立 critic（opus，讀 text 全文） → patch agent（sonnet，乾淨 context，extract/replace） → [需要時 critic re-gate → patch 第二輪] → update_dd_index.py → size gate（70KB 下界／目標 75-105KB，dd_sections.py bytes） → commit/push
```

**本 skill 不做分析** — 所有研究、決策層、品質規則都在 `stock-analyst`（現 v15.2，版號一號到底；報告端 dd-meta `schema` 仍 `v15.0`）裡。這裡只負責「順序、同步、閘門、提交」。**不再有獨立 DCA 步驟**：單一報告 `docs/dd/DD_*.html` 已內含 Part II 決策層（§11-§14）與統一裁決，不再產 `docs/dca/DCA_*.html`。

## Steps

1. **解析 ticker(s)**。模糊或不確定的 ticker **先問用戶**，不要瞎猜（memory `feedback_dca_session_pitfalls`）。
   - 開始前先 `git log --oneline -5` + `git status`，確認沒有並行 session 的背景動作 / orphan 檔（parallel-session git hygiene）。

2. **（可選）peer 自動偵測**。用戶給單一 ticker 且語氣是「這個 theme / 這群」時，可從 `docs/dd/` 同產業、或 `docs/id/ID_*.html` 的 `related_tickers[]` 帶出 1–3 檔 peer 一起跑（如 KLAC → ASML / LRCX）。**會擴張範圍時先跟用戶確認要不要連 peer**。

3. **決策意圖 → 先跑 critic**。若用戶語氣是「要不要加倉 / 新進 / 退出某 theme」這種**決策**（不是純研究），先按 repo 頂部「Decision-time critic」規則 spawn `industry-thesis-critic`，再產報告。純資訊查詢不觸發。

4. **跑 DD——writer → critic → patch 鏈**（模型：writer／patch agent＝`sonnet`；critic＝`opus`，**writer↔critic 永不同模型**；2026-08-06 起試行至 2026-10 校準，orchestrator 本身維持 opus；理由與 kill condition 見 repo CLAUDE.md「DD 層 writer↔critic 對調」）：
   - **4.1 Writer**：對每個 ticker 觸發 `stock-analyst`（spawn 模型＝`sonnet`）。writer 只產出 `.dd_build/DD_{T}_{D}.body.html` 一次 Write（裝不下最多分 2 次 `cat` 合併），再自行跑 `python3 scripts/render_dd.py` 組裝＋四支驗證（`verify_dd_math.py`／`validate_dd_meta.py --report`／`qc.py`／`python3 scripts/dd_sections.py bytes`），任一 FAIL 或 bytes WARN 用 `dd_sections.py extract`/`replace` 修段，驗證輪次 ≤3、禁 Edit、禁 Read 自己輸出的 HTML。產出單一 `docs/dd/DD_{TICKER}_{YYYYMMDD}.html`，schema v15.0，含 dd-meta 決策層欄位（`dca_verdict`/`dca_role`/`moat_trend`/`runway_post_y5`/`ev5y_pct`）+ 統一裁決 `id="decision"` 錨點（§13）。writer 最終回報含 INDEX.md ready-to-paste 行與 `bytes` 表原文，**不 spawn critic、不 commit**。
   - **4.2 Critic**：orchestrator 依 QC-41／QC-48／QC-50／row 8b 觸發規則（合併載具規則不變）spawn 獨立 `opus` critic，輸入＝`python3 scripts/dd_sections.py text FILE` 全文（前份 DD 亦同法讀 `text`），輸出存 `notes/site-internal/dd/_critic_{T}_{D}.md`，檔頭固定 FINDINGS 表＋GATE 行（PASS／PASS-with-fixes／FAIL；格式見 stock-analyst `references/critic-gates.md` §4.2）。
   - **4.3 Patch agent**：spawn 乾淨 context 的 `sonnet` patch agent，輸入 critic md 路徑＋DD 路徑＋要處理的 finding 編號（預設全部 🔴＋🟡）。用 `dd_sections.py extract` 取受影響段落、在 context 內改寫、`dd_sections.py replace` 寫回，連動欄位（dd-meta／dashboard）同法同步；跑四支驗證＋`leaks`；回報每條 finding 的處置（已修／不採納＋理由）與改動段落 bytes 前後。
   - **4.4 需要時 re-gate**：patch 後若 GATE 非 PASS，SendMessage 同一 critic agent（讀 `text` 全文重驗）→ 需要時 patch 第二輪（沿用同一 patch agent，SendMessage）。
   - **4.5 INDEX.md 登錄**：用 writer 最終回報中 ready-to-paste 的那一行登錄 `docs/dd/INDEX.md`（並行模式例外時直接沿用該行不 Edit 檔案，見 stock-analyst `references/html-output.md`）。

5. **同步**：`python scripts/update_dd_index.py`（重生 research 主表 + DD 組合快照 + 自動連鎖 `build_dd_screener.py` rebuild `docs/dd-screener/latest.json` + `build_picks.py` 更新 `docs/picks/candidates.json`；報告由 script 直接讀 dd-meta dca 欄位，「定見」欄連 `/dd/DD_X.html#decision`）。離線 / yfinance 掛掉時加 `--skip-dd-screener`（會 warn 但不 abort）。

6. **Size-budget gate（pre-commit hook 也會擋，但這裡先自驗）**：新報告須 **≥ 70KB 且目標落在 75–105KB 帶內（含 §8.5 附文獻 ≤115KB）**（gate 對 `"schema":"v15` 檔生效；下界擋 commit、上界只警告；Part I 基本面 ≥60%、估值＋附A ~7%）。跑 `python3 scripts/dd_sections.py bytes FILE`，把分章 WARN（若有）併入本步驟回報。**未達下界不是去灌水**，而是回去把缺的量化模組補實（五個深度模組 + 四個決策模組的 sourced 數字、非段落注水）。**超過上界不是去刪模組**，而是套三條省法（不印程序性自檢／表只留承重列／同一數字只出現一次）——見 CLAUDE.md「Report 篇幅預算」與 stock-analyst QC-38。真要放行 lean-but-complete 報告才 `--no-verify`。

7. **commit & push**：把 `docs/dd/DD_*`、`docs/research/_body.html`（2026-08-20 起 `/research/index.html` 已改為轉址 stub → `/t/#dd`，實際 DD 表格內容在 `_body.html`）、`docs/dd-screener/latest.json`、`docs/picks/candidates.json`、critic 報告 `notes/site-internal/dd/_critic_{T}_{D}.md` **併入同一 commit**（避免任一頁面滯後）。push 前重查 research / screener 沒被並行 session 覆蓋。commit message 沿用既有風格（如 `Add {TICKER} DD (統一裁決 ...); resync research+screener`）。

## 邊界

- 只要單檔報告（不 commit）→ 直接走 `stock-analyst`；多檔橫向對比 → 走 `multi-stock-comparator-v1`。本 skill 專門用於「同一 ticker 走完整 DD 報告 + 同步 + 提交」。
- **DCA 已退役**（併入單一 DD）；`deep-conviction-analyst` 是 deprecation stub，dca/定見 觸發語改觸發 `stock-analyst`。
- 不新增任何 validator / build script；step 5 的 `update_dd_index.py` 與 pre-commit hook 已涵蓋所有 plumbing。
- **白話呈現條款（2026-09-01 持有人拍板，全站適用，極簡版）**：本 skill 是 thin orchestrator，不自產報告文案——讀者可見文字的白話呈現責任在 `stock-analyst`（QC-54）；本 skill 產出中若出現顯示 label（如 commit 訊息、terminal 摘要），遵守 `notes/site-internal/root/_plainlang_styleguide.md` 對照表白話主名。
