# 研究區整併：7 頁 → 2 console（2026-08-20）

狀態：**第一、二階段皆已執行**。任務裁決「把導覽列『研究』群的 7 頁收斂成兩個主控台」，第一階段建主控台＋轉址（本輪未改 `scripts/site_nav.py` 的 MENU／nav 結構）；第二階段（2026-08-20 同日）執行 nav 標籤瘦身，`scripts/site_nav.py` 的 MENU["research"] 由 7 項收斂為 3 項，並同步至外部三 repo 的 nav literal copy。詳見§7。
前身：`_consolidation_stock_console_20260710.md`（選股主控台 4→1 的同一手法，本次沿用其 iframe＋nav-less 片段＋redirect stub 三件套）。

---

## 1. 每頁職能 × 數據源 × builder 盤點

| 頁面 | 職能（獨有內容） | 數據源 | 產生器 |
|---|---|---|---|
| `/t/index.html` | 個股總覽：252 檔 ticker 目錄，per-ticker 聚合（DD／ID／供應鏈／對比／期望落差） | 全站 dd-meta／id-meta／supply-chain data／comparisons／synthesis 掃描 | `build_ticker_hubs.py`（每次全量重建 `docs/t/`） |
| `/research/index.html` | DD 清單：652 份報告主表（訊號／護城河／估值篩選＋搜尋）＋ Weekly Review 標記區 | dd-meta JSON | `update_dd_index.py`（原地 regex 改寫，marker 驅動） |
| `/comparisons/index.html` | 多股對比：11 份報告 listing | 無（skill-appended，multi-stock-comparator-v1） | **無**（純手寫/skill append） |
| `/research/synthesis/index.html` | 期望落差綜合研判：6 份報告 listing | 無（skill-appended，expectations-synthesis） | **無**（純手寫/skill append） |
| `/id/index.html` | 產業 ID：59 檔已收錄產業深度報告目錄＋分類彙總＋Tier Matrix 健康度卡片 | id-meta JSON（隱藏 injection zone 供 `build_id_category_pages.py` 消費） | 無 producer builder；`refresh_id_staleness.py`／`check_tier_matrix.py` 做小範圍 marker 注入 |
| `/id/tier_matrix.html` | 全覆蓋 conviction 底圖（慢層手評 Tier＋快層 live 數據） | dd-screener `latest.json`（前端 fetch） | **無**（純手寫，快層 JS 現抓） |
| `/supply-chain/index.html` | 供應鏈地圖總目錄：44 個子產業主題 + 全站稀缺瓶頸排名（TIERS_AUTO 區塊） | `data/dd_links.json`＋策展稀缺分級清單 | `build_supply_chain_tiers.py`（原地 marker 替換） |

## 2. 重複內容矩陣（結論）

| 職能 | /t/（原個股總覽） | /research/ | /comparisons/ | /research/synthesis/ | /id/ | /supply-chain/ |
|---|---|---|---|---|---|---|
| 個股研究入口 | ● 唯一（ticker 聚合視角） | ● 唯一（報告類型視角，同數據不同切法） | | | | |
| 多檔橫向對比 | | | ● 唯一 | | | |
| 期望落差研判 | | | | ● 唯一 | | |
| 產業深度報告 | | | | | ● 唯一 | |
| 供應鏈節點圖 | | | | | | ● 唯一 |

**結論**：與選股主控台整併不同，這 7 頁**沒有內容重複**——每頁都是獨有職能，DD/多股對比/期望落差三者只是「同一份個股研究地圖」的三種切法（ticker 為單位思考時，這三者理應同框），供應鏈與 ID 則是「產業視角」的兩種鏡頭（表格 dashboard vs 節點圖）本就設計為並存（見 supply-chain/index.html 自身文案「位於 /id/ 之外的另一種產業視角」）。所以本次整併**不是砍重複**，而是**收斂入口表面**：把「個股研究」三頁摺進 `/t/`（它本來就是唯一的 ticker 聚合入口，天然適合當殼），把「供應鏈地圖」摺進 `/id/` 當一個分頁（產業視角就近取用），並把 ID 頁面footer 裡原本埋很深的「待研究子題」拉成獨立分頁，提升可見度。`/id/tier_matrix.html` 因自身已是獨立且高頻引用的判斷底圖（全站多處連結指向它），維持完全獨立不折疊。

## 3. 最終架構

### 3.1 `/t/` 升級為**個股研究主控台**，四分頁（deep-link hash 錨點）

| 分頁 | 錨點 | 內容 | 實作 |
|---|---|---|---|
| 總覽 | `#overview` | 原 252 檔 ticker 可篩選網格（filter input＋卡片） | client JS **原封不動**，inline（非 iframe） |
| DD 清單 | `#dd` | 652 份 DD 報告主表全內容 | iframe → `/research/_body.html` |
| 多股對比 | `#compare` | 11 份對比報告 listing | iframe → `/comparisons/_body.html` |
| 期望落差 | `#synthesis` | 6 份期望落差研判 listing | iframe → `/research/synthesis/_body.html` |

### 3.2 `/id/` 升級為**產業研究主控台**，三分頁

| 分頁 | 錨點 | 內容 | 實作 |
|---|---|---|---|
| ID 報告 | `#reports` | 原 59 檔產業 ID 目錄／分類彙總／Tier Matrix 健康度卡片（含隱藏 injection zone，`build_id_category_pages.py` 消費源，逐字保留） | client 原內容，inline |
| 供應鏈地圖 | `#supplychain` | 44 主題目錄＋全站稀缺瓶頸排名 | iframe → `/supply-chain/_body.html`（`/supply-chain/index.html` 本身**維持完全獨立、可直接到達**，因 44 張子地圖仍需獨立連結） |
| 待研究 backlog | `#backlog` | 各分類「建議補建」清單，即時聚合視圖 | **client-side JS 於載入時從隱藏 injection zone 逐分類搬入**（非靜態複製，見§4 說明） |

**為何 iframe 而非 client re-render**：與選股主控台先例同理——`/research/index.html` 是 marker 驅動的 652 列表格（`update_dd_index.py` 逐次全量重建 `dd-tbody-v12`），`/supply-chain/index.html` 有策展稀缺分級 + DD 連結解析。同源 iframe 做到零重寫、零漂移，builder 只改輸出目標。

**Surface 帳**：對外入口 7 → **2**（`/t/`、`/id/`）。`/research/index.html`、`/comparisons/index.html`、`/research/synthesis/index.html` 三個舊 URL → 輕量 redirect stub（meta refresh + canonical + noindex → 對應 tab 錨點），比照 `/picks/` stub 模式。`/id/tier_matrix.html`、`/supply-chain/index.html` 維持獨立明細頁，不折疊、不轉址。

## 4. 「待研究 backlog」的實作偏離說明（自主判斷，需回報）

任務原描述「待研究子題目前埋在 `docs/id/index.html` 的頁面 footer」——**與實際不符**。實查發現：這份內容其實是 15 個（14 個分類 + 1 個重複的 `cat-consumer`）獨立的 `<details class="suggest">` 區塊，逐分類分散嵌在一個 `display:none` 的 `#industry-analyst-injection-zone` 巨型隱藏區塊裡（`build_id_category_pages.py` 依賴這個 zone 逐字節做為單一資料源，去生成 15 個 `cat-{mega}.html` 分類頁），**不是**頁尾的單一列表。

若照字面「移到獨立分頁」去搬移/複製這些內容，會製造第二份資料源，未來新增 ID 時容易漂移。改採：**「待研究 backlog」分頁的 mount 點在頁面載入、使用者切到該分頁時，用 client-side JS 從隱藏 injection zone 動態讀取＋clone 每個分類的 `<details class="suggest">` 內容**，逐分類分組呈現。Injection zone 本身完全未動一個字元，`build_id_category_pages.py` 的產線不受影響；backlog 分頁與資料源之間零漂移風險。

## 5. 每個 builder 的處置

| builder | 舊輸出 | 新處置 |
|---|---|---|
| `build_ticker_hubs.py` | `docs/t/index.html`（單分頁 filterable grid，含 nav） | 改為 4 分頁主控台殼：`render_overview_body()` 拆出原 grid 邏輯做 Tab 1 內嵌本體；`render_index()` 改組出 tabbar + 3 個 iframe panel（`/research/_body.html`／`/comparisons/_body.html`／`/research/synthesis/_body.html`）+ `page_head()` 提供全站 nav。252 檔 per-ticker 頁（`docs/t/{TICKER}.html`）不動。 |
| `update_dd_index.py` | 原地改寫 `docs/research/index.html`（`dd-tbody-v12`／`meta-refresh`／`WR_*`／`PM_*` marker） | `INDEX_HTML` 常數改指向 `docs/research/_body.html`；同一組 marker 驅動邏輯**完全不變**，只是換寫入檔案。`docs/research/index.html` 改為靜態 redirect stub，此後不再被此 builder 碰。 |
| `build_supply_chain_tiers.py` | 原地改寫 `docs/supply-chain/index.html`（`TIERS_AUTO_START/END` marker） | 新增 `BODY = SC / "_body.html"` 常數；`main()` 收工前對 `INDEX` 與 `BODY`（若存在）做**同一次** marker 替換，兩檔的稀缺排名區塊保證同步、不漂移。`INDEX`（`docs/supply-chain/index.html`）維持獨立完整頁不變。 |
| `.claude/skills/multi-stock-comparator-v1/SKILL.md` | 指示 skill 把新報告卡片 append 進 `docs/comparisons/index.html` | 改為 append 進 `docs/comparisons/_body.html`；`docs/comparisons/index.html` 是靜態 stub，之後不再被此 skill 動。 |
| `.claude/skills/expectations-synthesis/SKILL.md` | 指示 skill 把新報告卡片 append 進 `docs/research/synthesis/index.html` | 改為 append 進 `docs/research/synthesis/_body.html`。 |
| `scripts/publish_dd.sh` | `git add docs/dd/ docs/research/index.html` | 改 `git add docs/dd/ docs/research/_body.html`。 |
| `.claude/skills/ddreport/SKILL.md`（步驟 7 commit 清單） | 提及 `docs/research/index.html` 為 commit 目標 | 改註記 `docs/research/_body.html` 為實際內容檔，並說明 index.html 現為轉址 stub。 |
| `docs/id/index.html` | 手寫頁（無 producer builder；`refresh_id_staleness.py`／`check_tier_matrix.py` 做局部 marker 注入） | 手改插入 tabbar/JS，**逐字保留**隱藏 injection zone（`build_id_category_pages.py` 消費源）與 `STALE_PILL:*` marker span（`refresh_id_staleness.py` 注入點）；`check_tier_matrix.py` 原本要找的注入錨點（`統計卡片`／`stats-row`）目前在頁面中已不存在（2026-06-22 已停用該卡片、屬既有現象，非本次造成），不受影響。 |

**資料 JSON／dd-meta／id-meta 一律照舊產出**，各分頁 client fetch 邏輯無斷更。

## 6. nav 與站內引用

- **nav（第一階段）**：零改動（第一階段不動 `scripts/site_nav.py` 的 MENU/nav 結構，僅擴充 `SKIP_FILES`）。
- **nav（第二階段，2026-08-20 同日執行，見§7.1）**：`MENU["research"]` 由 7 項收斂為 3 項——「個股研究」(`thub`, `/t/`)／「產業研究」(`id`, `/id/`)／「Tier Matrix」(`tier`, `/id/tier_matrix.html`)，維持下拉形態不降頂層直連。`PREFIX_ACTIVE` 同步調整：移除選單的 4 個舊 item（`dd`/`sc`/`cmp`/`syn`）不再對應下拉條目，其實體頁面映射改點到吸收方——`docs/dd/`／`docs/dca/`／`docs/report/`／`docs/research/`（含 stub）／`docs/comparisons/`（含 stub）／`docs/research/synthesis/`（含 stub）改指 `("research","thub")`；`docs/supply-chain/`（獨立頁＋子地圖）改指 `("research","id")`。效果：這些頁面瀏覽時「研究」下拉的對應項與群同時高亮（不只群高亮）。全站 `python3 scripts/site_nav.py` re-inject 兩次驗證冪等（第一次 1701 updated，第二次 0 updated／1701 unchanged）；stub／nav-less 片段（`SKIP_FILES` 內）確認未被灌入 nav。
- **`site_nav.py` SKIP_FILES**（第一階段）：新增 7 檔——3 個 redirect stub（`research/index.html`、`comparisons/index.html`、`research/synthesis/index.html`）＋ 4 個 nav-less iframe 片段（`research/_body.html`、`comparisons/_body.html`、`research/synthesis/_body.html`、`supply-chain/_body.html`）。`docs/t/index.html`、`docs/id/index.html` 本身**未列入 SKIP_FILES**，維持正常 nav 注入（與 `/cockpit/` 先例一致）。第二階段未再變更 `SKIP_FILES`。
- **外部三 repo 同步（第二階段）**：`v7-backtest`（`site_nav_snippet.py`，commit `ee7d07b`）、`morning-briefing`（`briefing/site_nav_snippet.py`，commit `4abb44b`）、`minervini-quality-backtest`（`live/site_nav_block.py`，commit `2eb6c70`）三份 nav literal 的研究下拉皆已同步改為 3 項。**發現**：v7-backtest 的 `pick` 群（選股）尚未同步 2026-08-20 稍早的選股主控台單一入口收斂（仍列 6 項含已退役的 DD Screener/QGM/Momentum-5/RS+VCP Screener），已於該 repo commit 的 docstring change log 中註記為既有落後、非本次改動範圍；`market` 群已由另一並行 session 同日同步 intel 2.0 Phase C，cherry-pick 時與本次 research 群變更在 docstring 區段自動合併衝突，已手動解決（MENU dict 本身無衝突，僅 changelog 文字衝突）。
- `docs/id/tier_matrix.html` 的「三頁分工」段落原文把 `/picks/` 描述成獨立頁——但該 URL 已於 2026-07-10 選股主控台整併中改為轉址 stub → `/cockpit/#picks`。本輪同步修正為「選股主控台 · 精選榜」，並把「先在本頁定位…再去 picks 看它今天能不能 act」改成「…再去精選榜看」。
- `docs/id/index.html` 兩處硬編「Tier Matrix v2.1」版本號字樣改為「Tier Matrix」（不再帶版號），避免每次 Tier Matrix 改版都要回頭改這裡的文案；同段落新增一條文字連結指向本頁「供應鏈地圖」分頁（`#supplychain`）。

## 7. 第二階段執行記錄（2026-08-20 同日）

1. **nav 標籤瘦身 — 已執行**。研究下拉由 7 項（個股總覽／個股 DD／產業深度 ID／Tier Matrix／供應鏈地圖／多股對比／期望落差綜合研判）收斂為 3 項——**個股研究 `/t/`**／**產業研究 `/id/`**／**Tier Matrix**（`/id/tier_matrix.html` 因高頻獨立引用維持單獨入口；`/supply-chain/` 未獲獨立下拉項，因其主入口已可從 `/id/` 分頁到達，44 張子地圖仍可直接連結，只是不再佔頂層下拉席位）。`scripts/site_nav.py` 的 `MENU["research"]`／`PREFIX_ACTIVE`（見§6）已改，全站 `python3 scripts/site_nav.py` re-inject 完成並驗證冪等。主 repo commit：`171b7079d`（本地 commit `3a247e38a` 因 origin 分歧、經 worktree cherry-pick 重寫 SHA 後推送，內容相同）。外部三 repo nav literal 同步 commit：v7-backtest `ee7d07b`、morning-briefing `4abb44b`、minervini-quality-backtest `2eb6c70`（皆已 push）。另有 9 個檔案（5 份 `docs/dd/` DD 報告＋`docs/long-track-w52-adaptive/` 3 個 HTML＋3 個 state JSON）因另一 session 正在編輯中而排除於本次 commit：HTML 部分 nav 已個別復原（套用 nav 瘦身前的 site_nav.py 版本重新產生完整 nav block，同時把它們一併補齊到與全站其他頁一致的最新市場／選股群，只有研究群刻意維持瘦身前的 7 項），內容編輯完全未動；JSON 3 檔從未被 nav 注入器碰過，原樣不動。
2. **`/id/` 待研究 backlog 分頁的 JS 動態搬運**是否要改為 build-time 靜態生成（例如由一支新 builder 在每次跑 `refresh_id_staleness.py` 時順便重繪 backlog 靜態片段）——目前 client-side 即時讀取已能保證零漂移，暫無明顯必要性，但若日後分類數量成長導致載入延遲明顯，可重新評估。
3. **`docs/comparisons/index.html`／`docs/research/synthesis/index.html` 過去無 producer builder**（純 skill-append 手工維護）——`_body.html` 化之後仍是同樣的手工維護模式，只是換了檔名；若未來要幫這兩頁做自動化 index 重建（例如掃描目錄自動產生 listing），屬另一輪任務，本次不做。
