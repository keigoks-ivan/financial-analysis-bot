# 系統群整併第一批：/long-track/ 升級系統主控台 + 570 頁 nav 欠帳補齊（2026-08-23）

狀態：**Phase 0（外部樹 nav 欠帳）與 Phase 1（系統主控台）皆已執行**。本批任務明確限定「只做這兩個階段，不改 `scripts/site_nav.py` 的 MENU 結構」——nav 群瘦身（`system` 8 項→4 項）與偵探移群留待下一批，見§7。
前身：`_consolidation_stock_console_20260710.md`（選股主控台 4→1）、`_consolidation_research_20260820.md`（研究區 7→2）——本次沿用同一套 iframe＋nav-less 片段＋redirect stub 三件套。

---

## Phase 0：570 個外部樹頁面的 nav 欠帳

### 0.1 根因

`scripts/site_nav.py` 的 `EXTERNAL_TREES = {"qgm","qgm-tw","briefing","weekly","backtest"}` 是**刻意的永久設計**（避免本 repo 的全站掃描與外部 repo 自己的 cron 重生互相覆蓋），不是 bug——這一點與任務原始猜測（「這些樹頁沒被涵蓋，可能要納入注入範圍」）方向不同，實查後判定不應改動 `EXTERNAL_TREES` 本身。

真正的欠帳來源是：三個外部 repo（v7-backtest／morning-briefing／minervini-quality-backtest）各自手動同步的 nav literal 副本（`site_nav_snippet.py`／`briefing/site_nav_snippet.py`／`live/site_nav_block.py`）**落後 canonical 1-2 批**——2026-08-20 同日稍早的「選股入口整頓第二批」（`pick` 群摺成單一連結、`system` 群加入 `det` 市場偵探）從未同步到三個外部 repo，v7-backtest 自己的 docstring 甚至明文記載這是「既有落後、非本次改動範圍」。既然外部 repo 的 nav 副本是舊的，它們下次重生 570 頁時只會覆蓋回舊版——單純對 `docs/` 掃一次治標不治本。

### 0.2 處置（先修源頭、再一次性補歷史欠帳）

1. **修源頭**：對照 canonical `full_nav_block()` 輸出，用程式化比對（byte-identical 驗證，非人工目測）修正三個外部 repo 的 nav literal：
   - v7-backtest `site_nav_snippet.py`（`MENU["pick"]`／`MENU["market"]`／`MENU["system"]` 三段＋`build_nav()` 的 pick 群渲染）
   - morning-briefing `briefing/site_nav_snippet.py`（`NAV_BLOCK_BRIEF`／`NAV_BLOCK_WEEK`／`NAV_BLOCK_EARN` 三個字面區塊）
   - minervini-quality-backtest `live/site_nav_block.py`（`NAV_BLOCKS["us"]`／`["tw"]` 兩個字面區塊）
   三者皆以 Python 直接呼叫 canonical `site_nav.full_nav_block(group, item)` 重新生成後比對，確認與各自實際使用的 `(group, item)` 組合輸出 **byte-identical**（`True`/`True`）。
2. **一次性補歷史欠帳**：寫一支不進 repo 的 throwaway script（重用 `site_nav.py` 自身的 `STRIP_PATTERNS`／`full_nav_block`／`active_for`／`BODY_RE`／`SKIP_FILES` 邏輯，唯一差異是**不**套用 `EXTERNAL_TREES` 早退），對 5 棵樹（`backtest`／`qgm`／`qgm-tw`／`briefing`／`weekly`）跑一次全掃。第一次執行：`skip 1 / updated 569`；第二次執行（驗冪等）：`skip 1 / unchanged 569`。唯一的 `skip` 是 `backtest/six_state/status/index.html`（本就在 `SKIP_FILES`，刻意無頭）。`site_nav.py` 主注入器的 `EXTERNAL_TREES` 早退邏輯本身**完全未動**，`--check` 模式仍回報 `skip-external 570`。

### 0.3 下次外部 cron 重生會不會蓋回舊版？

**不會**——三個外部 repo 的 nav 副本已與 canonical byte-identical，下次各自 cron 重生時自然產出當前版本，570 頁不會再退回舊 nav。**但這個保證的前提是三個外部 repo的本地 commit 要真的 push 上去**，見下方治理備註。

### 0.4 治理備註（需人工確認）

三個外部 repo的 nav 同步 commit 目前皆為**本地 commit、尚未 push**（v7-backtest `4b7d302`、morning-briefing `7db8c9a`、minervini-quality-backtest `907a08e`）——本 repo 的 `.claude/notes/site-composition.md` 明文規定「改外部 repo 是新的 commit/push 範圍，動手前先跟用戶確認（不在預設 git push 授權範圍內）」，故三個 commit 停在本地等待人工確認後再 push。**在這三個 commit push 之前，Phase 0.3 的「不會蓋回」保證尚未完全生效**——若這三個外部 repo 在 push 前先跑了一次自己的 cron，仍會用舊 nav 副本重生涉及的頁面（不影響本次已補的 570 頁本身，但會讓外部 repo 產生新的落後頁）。

Phase 0 commit：`aa8b41d8f`（本地）→ worktree cherry-pick 後最終 SHA `7b1fae2fb`（已在 `origin/main`）。

---

## Phase 1：/long-track/ 升級系統主控台

### 1.1 每頁職能 × 數據源 × builder 盤點

| 頁面 | 職能 | 數據源 | 產生器 | 觸發頻率 |
|---|---|---|---|---|
| `/long-track/index.html` | 家族地圖：實單主系統／影子對照／前瞻 OOS 候選／已退役凍結對照 四分類卡片 | 靜態內容（手寫 `GROUPS`） | `build_long_track_index.py` | 手動（系統狀態變動時） |
| `/long-track-w52-adaptive/index.html` | 實單主系統儀表板：兩市場四腿訊號／執行層／曝險時間軸／回測縮圖 | yfinance 即時抓取＋`state.json` 歷史 | `update_long_track_w52_adaptive.py` | GitHub Actions cron，每交易日 × 2（台/美收盤後） |
| `/pm/index.html` | 持倉週掃：MONITOR_*.md 週掃報告渲染＋歷史列表 | `docs/pm/MONITOR_*.md`（position-thesis-monitor agent 產出） | `build_pm_index.py` | 手動／cron 觸發 |
| `/track-record/index.html` | 裁決實績：全站 DD 裁決回顧性前瞻報酬統計 | `docs/dd/DD_*.html` dd-meta＋週線價格快取 | `build_track_record.py` | 手動（鏈於 `update_dd_index.py` 之後） |

### 1.2 重複內容矩陣

四頁彼此**無內容重複**——與研究區整併同理，這是「同一個追蹤家族」的四種切法（總覽是地圖、實單主系統是即時儀表板、持倉週掃是持倉健檢、裁決實績是回顧統計），不是砍重複，是收斂入口表面。

### 1.3 最終架構：`/long-track/` 四分頁（deep-link hash 錨點）

| 分頁 | 錨點 | 內容 | 實作 |
|---|---|---|---|
| 總覽 | `#overview` | 原家族地圖（四分類卡片） | inline，client 內容**原封不動** |
| 實單主系統 | `#live` | W52 × 自適應波動率 cap 1.5 儀表板 | iframe → `/long-track-w52-adaptive/_body.html` |
| 持倉週掃 | `#positions` | 最新＋歷史 MONITOR 週掃報告 | iframe → `/pm/_body.html` |
| 裁決實績 | `#record` | 全站 DD 裁決回顧統計 | iframe → `/track-record/_body.html` |

**為何 iframe 而非 client re-render**：與前兩次整併同理——三個來源頁各自有獨立且複雜的資料管線（yfinance 即時抓取＋cron／markdown 渲染／dd-meta 掃描＋價格快取），同源 iframe 做到零重寫、零漂移，builder 只改輸出目標。

**Surface 帳**：對外入口 4 → **1**（`/long-track/`）。`/long-track-w52-adaptive/`、`/pm/`、`/track-record/` 三個舊 URL → 輕量 redirect stub（meta refresh + canonical + noindex → 對應 tab 錨點），比照 `/picks/`／`/research/` stub 模式。`/long-track-w52-adaptive/leverage.html`、`/long-track-w52-adaptive/tw-semivol.html` **不在本批整併範圍內**，維持獨立完整頁、照常掛站 nav。

### 1.4 三處自主判斷（偏離任務字面描述，需回報）

1. **`<base target="_parent">`**：任務原描述要求片段用 `<base target="_parent">＋noindex`。實查全站既有 6 個 nav-less 片段（`research/_body.html`／`comparisons/_body.html`／`dd-screener/_pipeline_body.html`／`supply-chain/_body.html`／`picks/_embed.html`／`engine/_index_body.html`）**沒有一個用 `<base target="_parent">`**——一律只是 noindex + nav-less 的完整標準頁。改採實際站內慣例（不加 `<base>` 標籤），與既有 6 個片段一致。
2. **`flags.json`／`holdings.json` client fetch 風險**：任務原描述要求驗證這兩份 JSON 在 iframe 內的 fetch 路徑是否仍解析正確。實查 `build_pm_index.py` 與現行 `docs/pm/index.html`，**這兩份 JSON 完全沒有被任何 client-side JS fetch**——它們只在 MONITOR_*.md 的文字內容中被提及（如「flags.json 記載的 -16.6%」），由 markdown 渲染器轉成純文字段落，不是被瀏覽器讀取的資料源。故此風險點實際不存在，iframe 化對持倉週掃分頁沒有資料路徑影響。同理 `track-record` 頁把統計資料以 `<script id="track-record-data" type="application/json">` 內嵌方式輸出（非外部 fetch），iframe 化亦無影響。
3. **CSS token 體系**：`build_ticker_hubs.py` 的 `CONSOLE_CSS` 用 `/assets/imq-base.css` 的 token（`--line`／`--paper`／`--sec`／`--gold-deep` 等），但 `/long-track/` 自身從未載入該檔、用的是自成一格的 token（`--brand:#1a56db`／`--bg:#f9fafb`／`--muted` 等）。若直接照搬 `CONSOLE_CSS` 會出現未定義變數。改為**用 `/long-track/` 既有 token 名重寫 tabbar 樣式**（`.console-tab-btn.active{color:var(--brand);border-bottom-color:var(--brand)}` 等），視覺語言與本頁既有卡片配色一致，未載入 `imq-base.css`。

### 1.5 每個 builder 的處置

| builder | 舊輸出 | 新處置 |
|---|---|---|
| `build_long_track_index.py` | `docs/long-track/index.html`（單分頁家族地圖，含 nav） | 改為 4 分頁主控台殼：`render_overview_body()` 拆出原家族地圖邏輯做 Tab 1 內嵌本體；`render()` 改組出 tabbar + 3 個 iframe panel（`/long-track-w52-adaptive/_body.html`／`/pm/_body.html`／`/track-record/_body.html`）+ `NAV_BLOCK`（`full_nav_block("system","lthub")`，未改 MENU）。 |
| `update_long_track_w52_adaptive.py` | 原地寫 `docs/long-track-w52-adaptive/index.html`（`{NAV_BLOCK}` 直接烘焙進 f-string 模板） | `OUTPUT` 改指 `_body.html`；`NAV_BLOCK` 改為空字串（模板其餘 ~1300 行完全不動，只有這兩個常數變了）。`index.html` 改為一次性寫入的 redirect stub，此後不再被本 script 覆寫。**`leverage.html`／`tw-semivol.html` 走完全獨立的另兩支 script（各自 `NAV_BLOCK`／`OUTPUT` 常數不受影響），已逐一確認零耦合。** |
| `.github/workflows/update_long_track_w52_adaptive.yml` | `git add` 明列 `docs/long-track-w52-adaptive/index.html` | 改列 `docs/long-track-w52-adaptive/_body.html`；其餘 5 個 `git add` 目標（`state.json`／`leverage.html`／`leverage_state.json`／`tw-semivol.html`／`tw_semivol_state.json`）不變。 |
| `build_pm_index.py` | 原地寫 `docs/pm/index.html`（nav 靠 `site_nav.py` 外部掃描注入，builder 本身不烘焙 nav） | `OUT` 改指 `_body.html`；內容渲染邏輯完全不變。`docs/pm/index.html` 改為一次性寫入的 redirect stub。 |
| `build_track_record.py` | 原地寫 `docs/track-record/index.html`（`extract_canonical()` 從 `docs/mental-models/index.html` 逐字抓 `nav_style`／`nav_header`／`nav_script` 烘焙進模板——第三種、與前兩者都不同的 nav 機制） | `OUT_HTML` 改指 `_body.html`；`render_html()` 內組裝模板時**不再插入** `nav_style`／`nav_header`／`nav_script`（`extract_canonical()` 仍抓這三段但標記未使用，`fonts_tokens`／`footer` 照常使用）。鏈於 `update_dd_index.py` 之後的呼叫關係不變（該檔只是呼叫本 script，路徑無關）。 |

**資料 JSON（`state.json`／`holdings.json`／`flags.json`／`track-record/data/latest.json`）一律照舊產出**，各分頁資料層無斷更。

### 1.6 nav 與站內引用

- **nav（本批）**：零改動 `MENU`／`PREFIX_ACTIVE`（依任務要求）。`PREFIX_ACTIVE` 現有的 `("long-track-w52-adaptive/", ("system","voltrack"))`／`("pm/", ("system","pm"))`／`("track-record/", ("system","tr"))`／`("long-track/", ("system","lthub"))` 四條前綴映射在 stub 化後仍然正確——stub／片段檔名雖變了，但目錄前綴不變，高亮邏輯不受影響。
- **`SKIP_FILES` 新增 6 筆**：3 個 redirect stub（`long-track-w52-adaptive/index.html`、`pm/index.html`、`track-record/index.html`）＋ 3 個 nav-less iframe 片段（`long-track-w52-adaptive/_body.html`、`pm/_body.html`、`track-record/_body.html`）。`docs/long-track/index.html` 本身**未列入 SKIP_FILES**，維持正常 nav 注入（與 `/cockpit/`／`/t/`／`/id/` 先例一致）。`leverage.html`／`tw-semivol.html` 不受影響，繼續正常掛 nav。
- **驗證**：`python3 scripts/site_nav.py` 全站掃描跑兩次——第一次 `updated 6 / skip 30`（skip 較之前 +6，即本批新增的 6 筆 `SKIP_FILES`）；第二次 `updated 0 / unchanged 1701 / skip 30`，確認冪等、且無 nav 被灌入任一新 stub／片段。

### 1.7 執行記錄與驗證結果

1. **本地驗證**（`python3 -m http.server` 起本機伺服器）：`/long-track/` 主殼 HTTP 200；三個 iframe 片段（`_body.html`）各自 HTTP 200；三個舊 URL（`/long-track-w52-adaptive/`／`/pm/`／`/track-record/`）皆回應 `<meta http-equiv="refresh" content="0; url=/long-track/#live|#positions|#record">`，目標錨點正確對應。
2. **實跑三個 builder＋主 shell**：`build_long_track_index.py`（19,630 bytes）、`build_pm_index.py`（36,240 bytes）、`build_track_record.py`（含一次 yfinance 抓取，`ABB` 因下市查無資料屬既有已知缺口、非本次引入）、`update_long_track_w52_adaptive.py`（實跑抓取四腿即時訊號，`_body.html` 261,807 bytes，`state.json` 依既有冪等 merge-by-date 邏輯更新，無 actionable change 故未產生 `lt_w52a_alert.txt`）。
3. **`python3 scripts/qc.py --all`**：0 errors、3553 warnings（全部為既有、與本批無關的檔案——`docs/long-track/`／`docs/long-track-w52-adaptive/`／`docs/pm/`／`docs/track-record/` 四個目錄下逐一確認**零筆**警告）。
4. Phase 1 commit：見主報告（獨立於 Phase 0 commit）。

---

## 附：留待下一批的項目（本批明確排除，Phase 2 執行時已完成 1／2，見下）

1. ~~**nav 標籤瘦身**：`MENU["system"]` 由現行 8 項...收斂為 4 項~~ → 已於 Phase 2 完成，見 §7。
2. ~~**市場偵探移群**：`det`（市場偵探）...移至 `market` 群~~ → 已於 Phase 2 完成，見 §7。
3. **`how-to.html` 改寫**：涉及站內導覽說明文字更新，需同步反映 `/long-track/` 四分頁化與 nav 瘦身後的群組結構——**Phase 2 仍不動 how-to.html**，是下一批（最後一批）任務。
4. ~~**三個外部 repo 的 nav 同步 commit push**~~ → 已於 Phase 2 執行，見 §7（原 Phase 0.4 遺留的 3 個本地 commit 因與 Phase 2 的 `system` 群改動疊加，改為一次性重新同步後 push，而非分兩輪推）。

---

## Phase 2：系統群 nav 瘦身（2026-08-23，緊接 Phase 0/1 之後執行）

### 7.1 範圍

`scripts/site_nav.py`：

- `MENU["system"]` 8 項→4 項：`det`／`tr`／`pm`／`voltrack` 四個 item 鍵移除；倖存的 `lthub` 項標籤由「追蹤總覽」改「系統主控台」（URL 不變，`/long-track/`）；`bt`／`tools`／`data` 三項不變。**不新增 `det` 回市場群選單**（維持不轉址、直達頁的判定，比照 crowding/regime/rotation）。
- `PREFIX_ACTIVE` 改點：
  - `track-record/`、`pm/`、`long-track-w52-adaptive/`、`long-track-qs-vt/`、`long-track-adaptive-vt/`、`long-track-tw-vt/` 六條前綴統一改掛 `("system", "lthub")`（原本分別掛 `tr`／`pm`／`voltrack`）。
  - `detective/` 改掛 `("market", "intel")`（原 `("system","det")`）——選擇 intel 而非純群層高亮（`("market", None)`），理由：`/detective/` 是 `/intel/` 「變化」分頁的同源完整互動頁，與 crowding/regime/rotation 三頁「歸市場群某具體 item」的判定一致，不是泛用市場頁。
  - 清 dangling keys：`("pick","dds")`／`mom5`／`qus`／`qtw`／`scr` 五個 2026-08-20 選股群收斂時已從 `MENU["pick"]` 移除、但 `PREFIX_ACTIVE` 漏改的殘留 item 鍵，統一改 `("pick", None)`（`dd-screener/`、`engine/`、`research/momentum-5/`、`qgm/`、`qgm-tw/`、`screeners.html`、`screener.html`、`screener-tw.html`、`screener-jp.html`、`screener-my.html` 十條前綴）。
- 內部 generator 同步：7 支 `scripts/update_long_track_*_vt*.py`（`adaptive_vt`／`qs_vt_adaptive`／`qs_vt`／`w52_adaptive_leverage`／`w52_adaptive_tw_semivol`／`tw_vt`／`tw_vt_adaptive`）原本硬編 `full_nav_block("system", "voltrack")`，`voltrack` 鍵移除後若不改會靜默退化成「群高亮但無 item 高亮」（與 dangling keys 同一類問題），已同步改 `full_nav_block("system", "lthub")`。經盤點確認 `/detective/`／`/pm/`／`/track-record/` 三頁的 builder（`build_detective.py`／`build_pm_flags.py`／`build_track_record.py` 等）皆不自行呼叫 `full_nav_block`，nav 完全依賴 `site_nav.py` 全站掃描 + `PREFIX_ACTIVE`，故上述 `PREFIX_ACTIVE` 改點已自動覆蓋，無需額外改 builder。
- `build_nav()` 本身**不變**——`system` 群瘦身後仍是 4 項，維持下拉形態，不觸發選股群式的單項 flat-link 特例（那個特例只在群縮到剛好 1 項時才轉換）。
- 檔頭 change log 補記 2026-08-23 條目。

### 7.2 全站 re-inject 驗證（idempotency）

`python3 scripts/site_nav.py`：
- 第一次：`updated 1701 / skip 30 / skip-external 570 / no-body 8`
- 第二次：`unchanged 1701 / skip 30 / skip-external 570 / no-body 8`（冪等確認；`no-body` 8 筆與本批無關——皆為既有 HTML 結構缺失的 DD 報告，非本批引入，且與下方「6 個 DD-gate 髒檔」中的 5 筆不完全重疊）。

1701 全數變動：因為 `MENU["system"]` 內容變動會反映在**每一頁**渲染出的完整 nav header（下拉選單內容），不限於系統群自身頁面，與 Phase 1 全站 1701 頁基準一致。

外部五樹（`backtest`／`qgm`／`qgm-tw`／`briefing`／`weekly`）沿用 Phase 0.2 的 throwaway sweep script 邏輯（不套用 `EXTERNAL_TREES` 早退）同步跑過，結果與 canonical `docs/` 一致（byte-identical 抽查）。

### 7.3 已知不動的 6 個 DD-gate 髒檔

工作區中以下 6 個檔案在本批之前即為髒檔（DD math pre-commit gate 因內容問題擋下、與本次 nav 改動無關），本批全程不碰、不納入 commit：

```
docs/dd/DD_UBER_20260808.html
docs/dd/DD_TSM_20260806.html
docs/dd/DD_SNDK_20260806.html
docs/dd/DD_LLY_20260806.html
docs/dd/DD_KLIC_20260806.html
docs/earnings/synthesis_2026-08-20.html
```

判定依據：這 6 檔的 `git diff --stat` 變動行數（33／33／33／33／33／14）明顯高於同批其餘 nav-only 頁面的基準值（6 行）——多出的行數是先前既有、與本批無關的內容差異，本批的 nav re-inject 疊加在其上但未刻意處理。commit 時用 `--only` 明列檔案，天然排除這 6 個。

### 7.4 三個外部 repo 的 commit / push

延續 Phase 0.4 的治理備註：v7-backtest（`4b7d302`）／morning-briefing（`7db8c9a`）／minervini-quality-backtest（`907a08e`）三個本地 commit 因與本階段 `system` 群改動有邏輯疊加（尤其 v7-backtest 的 `MENU["system"]` 字面副本），改為**先完成本 canonical repo 的 Phase 2 改動，再一次性重新同步三個外部 repo 到最終狀態後 push**，而非分兩輪各推一次（原字面任務指令是「先 push 待推 commit、再做瘦身」兩步驟，此處為主動排序調整，屬本批第二個需回報的自主判斷——見主報告）。三個 repo 最終 commit hash 與 push 結果見主報告。

### 7.5 Commit 與 push 結果

Phase 2 commit（獨立於 Phase 0／Phase 1 commit，`--only` 明列 `scripts/site_nav.py`＋7 支 `update_long_track_*_vt*.py`＋1704 個檔案〔1701 nav-only 頁面＋本設計文件＋2 支 generator 腳本已含在 1701 之外〕，明確排除上方 6 個 DD-gate 髒檔）：

- financial-analysis-bot 本地 commit `2a8774934` → worktree cherry-pick 後最終 SHA `ddfcc6c08`（已在 `origin/main`）。
- v7-backtest：origin 落後多批（研究群/選股群/intel Phase C/系統群），改用整檔覆蓋方式同步（避免與 origin 上其他 session 的並行 nav 提交衝突），commit `ff4d438`（已在 `origin/main`）。
- morning-briefing：本地兩個 commit（`7db8c9a` 選股入口整頓第二批 catch-up ＋ `7d96798` 系統群瘦身 phase 2）→ worktree cherry-pick 後最終 SHA `d39cc7c`（已在 `origin/main`）。
- minervini-quality-backtest：無分歧、可快轉，本地 commit `45afcd1` 直接 `git push` 成功（已在 `origin/main`）。

四個 repo 的 nav 副本現皆與 canonical 同步（v7-backtest 的 `full_nav_block("system","bt")`、morning-briefing 的 `brief`/`week`/`earn`、minervini-quality-backtest 的 `us`/`tw` 皆已程式化驗證 byte-identical）。

---

## Phase 3（最後一批）：`how-to.html` 整篇重寫 + `data.html` 補端點（2026-08-23）

**本批完結整個系統區＋指南改版系列。** Phase 0/1/2 處理了 nav 結構與系統主控台落地，本批把站內兩份「說明文件」——使用指南與公開資料端點文件——追上前三個 Phase 的落地結果，是這個系列設計文件的最後一條記錄。

### 8.1 觸發原因

`docs/how-to.html` 的內容早於 Phase 0-2：晨檢段落還在教 `/monitor/`／`/detective/`（未提 `/intel/`），決策鏈段落連到已變成 redirect stub 的 `/research/`／`/pm/`／`/track-record/`，速查表沿用舊四分組（市場層／選股與個股層／行為與實績層／工具與資料層），與 nav 實際的四分組（市場／選股／研究／系統）不同構；`.snapshot` 範例區塊硬編 2026-07-17／18 的截圖數字，每次改版就過期一次。`docs/data.html` 只文件化 8 組端點，停在 intel 世代之前——`/intel/`、`/detective/`、`/monitor/` 長歷史序列、`/pm/`、`/long-track-w52-adaptive/` 家族六個實際存在的端點完全沒有 schema 文件。

### 8.2 `how-to.html` 改動範圍

六段骨架（晨檢／週日定位／一筆真決策完整鏈／平時自動化／站的邊界／速查表）**維持不變**，只換每段的落地動線：

- **§1 晨檢**：首頁四磚點進去的細節頁從 `/monitor/`＋`/detective/` 改為 `/intel/gauges.html`（儀表）＋`/intel/change.html`（變化）；`/detective/` 降級為「從 /intel/change.html 點進去看」的一句話帶過。移除硬編 2026-07-17／18／2025-11-24 三個快照範例的具體數字，改寫成「威脅指針 vs 壓力分數同向／分歧怎麼判斷」的不綁日期教學框架（`.snapshot` 視覺區塊保留，內容改為方法論而非數字）。
- **§3 決策鏈**：`/flow/` 七步敘事結構原樣保留，連結逐一更新——③深度研究改連 `/t/`（個股研究總覽頁，一頁收斂 DD＋所屬 ID＋供應鏈＋對比）與 `/id/`；④裁決三錨、⑦出場歸帳的帳本連結改 `/long-track/#record`；⑥自動監控的持倉週掃連結改 `/long-track/#positions`。
- **§4 自動化**：`/cockpit/` 補上四分頁名稱（總覽・天氣陣容／席位排序／流程板機／精選榜），`/data.html` 範例端點加入 `intel/data/status_snapshot.json`。
- **§5 邊界**：帳本連結同步改 `/long-track/#record`。
- **速查表**：整表重建為五組——市場（11 列，含新增 `/intel/`、`/briefing/`）／選股（3 列：`/cockpit/`／`/dd-screener/`／`/picks/`）／研究（4 列：`/t/`／`/id/`／Tier Matrix／`/supply-chain/`）／系統（4 列：`/long-track/`／`/backtest/`／`/tools/`／`/data.html`）／頂層獨立頁（3 列：`/mental-models/`／`/flow/`／`/search.html`）——與 nav 四分組同構。欄位從三欄（頁面／用途／使用頻率）擴為四欄（入口／用途／更新頻率／使用時機）；主控台類入口在「入口」欄直接列分頁 hash 直達連結（如 `/cockpit/#seats`、`/t/#dd`、`/long-track/#live`）。`/learn/`（36 課分析框架課程）不在 nav 內、不進速查表，改在 hero lede 補一句話保留可發現性，避免速查表跟 nav 分組脫鉤又要為它開特例。

改寫前後行數：299 → 302 行（六段骨架份量持平，未灌水）。

### 8.3 `data.html` 新增端點

先逐一 `ls`／`python3 -c "json.load"` 驗證檔案存在與 schema 結構，確認 9 個候選路徑全部存在後才動筆（無一為假設）：

| 端點 | 路徑 | 來源 workflow |
|---|---|---|
| 跨資產壓力分數・長歷史 | `/monitor/data/score_history.json` | `monitor-daily` 跑 `build_monitor_score.py`（另於 `intel-2-daily` 鏈重算） |
| 偵測警報網 | `/detective/data/latest.json` | `intel-2-daily` 主跑 ＋ `detective-daily` 備援跑 `build_detective.py` |
| 情報監視器・現況彙整 | `/intel/data/status_snapshot.json` | `intel-2-daily` 跑 `scripts/intel/render.py` |
| 裁決實績 | `/track-record/data/latest.json` | 事件驅動，`update_dd_index.py` 連鎖 `build_track_record.py` |
| 持倉監控旗標 | `/pm/flags.json` | `intel-2-daily` 主跑 ＋ `detective-daily` 備援跑 `build_pm_flags.py` |
| 實單持倉組合 | `/pm/holdings.json` | `weekly-engine` 跑 `build_holdings.py` |
| W52 自適應引擎狀態（主系統／槓桿／台股半年化波動三檔） | `/long-track-w52-adaptive/{state,leverage_state,tw_semivol_state}.json` | `update_long_track_w52_adaptive` 依序跑三支 `.py` |

既有 8 組端點順手校正兩處過期敘述：DD Screener 段落「共同資料源」把已變 redirect stub 的 `/research/` 改為 `/t/`；monitor 段落補一句指向新增的 score_history 小節。TOC 從 8 個錨點擴為 15 個。改動後 394 → 575 行（純新增 6 個端點區塊，無刪減）。

### 8.4 驗證

- 自寫 `check_links.py`（掃 `how-to.html` 全部站內 `href` 對 `docs/` 檔案系統，轉址 stub 視為通過）：60 個唯一 href，51 內部＋3 外部（跳過）＋6 純錨點（跳過），**0 個失敗**；同法掃 `data.html`：45 個唯一 href，**0 個失敗**。
- `python3 scripts/site_nav.py`：`unchanged 1701`（無 `updated`）——確認本批兩檔案的 nav header 在 Phase 2 已是最終狀態，本批只動 body 內容，未觸發任何 nav 重寫。
- `python3 scripts/qc.py docs/how-to.html docs/data.html`：**0 errors, 0 warnings**。
- `git status`：僅 `docs/how-to.html`／`docs/data.html` 變動；既有 6 個 DD-gate 髒檔（`DD_UBER_20260808`／`DD_TSM_20260806`／`DD_SNDK_20260806`／`DD_LLY_20260806`／`DD_KLIC_20260806`／`earnings/synthesis_2026-08-20`）延續 Phase 2 判定，全程未觸碰。

### 8.5 Commit 與 push 結果

本批不涉外部 repo（`how-to.html`／`data.html` 為 canonical-only 頁，三個外部 repo 皆無同名檔案）。commit hash 與 push 結果見主報告。

**至此，整個系統區＋指南改版系列（Phase 0 外部樹欠帳 → Phase 1 系統主控台 → Phase 2 nav 瘦身 → Phase 3 指南與資料文件）全部完結，本設計文件不再新增條目。**
