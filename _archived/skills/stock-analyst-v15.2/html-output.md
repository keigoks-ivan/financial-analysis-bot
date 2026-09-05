# stock-analyst v15.2 — html-output.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-07 v14.7 結構拆分，內容自 v14.6 原文搬移、語意零變更；2026-09-03 v15.2 改為 BODY 契約＋模板抽離，見 `references/changelog.md`）。必讀時點見 SKILL.md 條件載入路由表。修改規則請同步 SKILL.md stub 與 references/changelog.md。

## 【HTML 輸出協議】

**writer 唯一產出是 BODY 檔，不直接 Write 最終 HTML**。完成所有章節後，用 Write 產出 BODY（不得省略或延後、不得摘要化任何章節），再交給 `render_dd.py` 組裝成完整報告。

### BODY 檔格式（writer 唯一產出）

路徑：`.dd_build/DD_{TICKER}_{YYYYMMDD}.body.html`（`.dd_build/` 已在 `.gitignore`，不會被 commit）。內容依序：

1. `<script id="dd-meta" type="application/json">{…}</script>`（schema v15.0，見下方 dd-meta 段）
2. `<!-- TITLE: DD {公司名}（{TICKER}）— {YYYY-MM-DD}（統一裁決：{裁決}） -->`
3. `<!-- SOURCES: {頁尾「資料來源：」句的內容} -->`
4. dashboard 區：`<div class="topbar">…</div>`、`<div class="wrap">`、`<h1>`、頂部標註 `<p class="note">`、`<div class="status-bar">…</div>`、`<p class="thesis">`、`<div class="hypothesis-box">…</div>`、讀法 `<p class="note">`（模板見下方【頁首結論儀表板】）
5. `<section id="s1">`…`<section id="s14">`（含條件性 `s85`；§13 為 `<section id="decision">`）
6. `<details id="appA">`／`<details id="appB">`（B 僅循環 archetype 才寫）
7. `<section id="revlog">`、`<section id="sources">`（選填）

**預設分兩次 Write**（單則輸出過長會撞輸出上限而整段作廢）：`.body.part1.html`＝dd-meta＋TITLE／SOURCES 註解＋dashboard＋`s1`–`s7`；`.body.part2.html`＝`s8`（含 `s85`）–`s14`＋`appA`／`appB`＋`revlog`／`sources`；`cat part1 part2 > .dd_build/DD_{T}_{D}.body.html` 合併。短報告可單次 Write；**part 檔可小幅 Edit（局部修字／數字，非整段重寫；Edit 後重新 `cat` 合併）**；分三次以上＝篇幅已失控，先套分章節省法再 render。

### render 與四支驗證

```
python3 scripts/render_dd.py .dd_build/DD_{T}_{D}.body.html -o docs/dd/DD_{T}_{D}.html
```
render_dd 負責組裝 `<head>`（charset／robots noindex,nofollow／viewport／`dd-schema-version`／`<title>`／dd-meta／內嵌 `scripts/dd_template/dd.css`）、自動生成 `<nav class="dd-toc">`（依實際存在的 section／details id 產生 pill 連結，writer 不手寫 toc）、頁尾來源句（取 SOURCES 註解）、列印按鈕，並依序 post-process 注入站內 nav／導讀 primer／livebar。

render 完成後**跑四支驗證**：`verify_dd_math.py FILE`、`validate_dd_meta.py --report`、`qc.py FILE`、`python3 scripts/dd_sections.py bytes FILE`。任一 FAIL 或 bytes 出現 WARN：
1. `python3 scripts/dd_sections.py extract FILE ID` 取該段原文
2. 在 context 內重寫該段，寫暫存檔
3. `python3 scripts/dd_sections.py replace FILE ID NEWFILE` 就地覆寫
4. 重跑四支驗證

**驗證輪次 ≤3**；**禁止 Read 整份輸出 HTML、禁止 Read 自己的 BODY 檔、`docs/dd/` 產物禁止 Edit（只准 `extract`/`replace`）**。確認 `id="decision"` 錨點存在；確認 dca_verdict 三處（頁首 status-bar／§13／dd-meta）一致。

### 視覺規格

**樣式全部由 `scripts/dd_template/dd.css` 內嵌，writer 不寫 `<style>`、不寫行內 padding／border-radius／font-size 等 CSS 細節**，只在 BODY 內容中挑用既有 class 與語意色。

**色碼語意表（精簡版，供挑 class／挑顏色）**：

| 用途 | class | 顏色語意 |
|---|---|---|
| 頁首固定列 | `.topbar` | 深底白字 |
| 一行 grid 儀表板 | `.status-bar`（`.sb-cell` `.lab` `.val`） | 淺灰底＋左右 4px accent 藍線 |
| thesis 大字 | `.thesis` | 淺藍底 #EFF6FF |
| 儀表板要點清單 | `.hypothesis-box` | 淺藍底＋左 4px 藍線 |
| §2 核心假設 | `.sec-assume` | 淺藍底 #EFF6FF |
| 價值陷阱警示 | `.sec-trap` | 橘紅底 #FFF0E6 |
| §11 矛盾 | `.sec-contra` | 淺橘底 #FFF7ED |
| §12b Pre-mortem | `.sec-premortem` | 淺紅底 #FEF2F2 |
| §10.5/10.6 情境樹 | `.sec-irr` | 淺藍學習感 #F0F9FF |
| §13 決策晶片 | `.chip` ＋ 行內 `style="background:{色}"` | 進場 #166534／觀望 #92400E／迴避 #991B1B |
| §12c Max DD 大數字 | `.maxdd-num` | 依範圍下界行內色：≥−30 綠／−30~−50 amber／<−50 紅 |
| §12c color bar | `.bar` | 綠→amber→紅固定三段（0~−30／−30~−50／<−50） |
| 狀態小標記 | `.g`（綠 Beat/符合）／`.y`（黃 中性）／`.r`（紅 Miss/不符合）／`.b`（藍） | — |
| 折疊區 | `<details>`／`<details id="appA">`／`<details id="appB">`／`<details class="audit">` | 白底卡片 |

**§13 裁決晶片色碼**（規格不變）：進場 背景 #F0FDF4／左線 #166534；觀望 背景 #FEF9C3／左線 #92400E；迴避 背景 #FFF1F2／左線 #991B1B；晶片副標籤 13px #475569 斜體（`.chip-sub`）。

整體風格：金融研究報告質感，無圓角過度裝飾，線條簡潔，留白充足。**禁止**漸層背景、過重陰影、非專業裝飾。

### 章節顯示順序（HTML 呈現）

| 顯示位置 | 章節 | 說明 |
|:---|:---|:---|
| 0（最頂部） | 頁首結論儀表板 | Status Bar + thesis + 統一裁決（模板見下方） |
| 1 | §1 投資結論詳述 | trap 四問 + 監測指標見 §13 表；先生意後價格 |
| 2 | §2 投資論點錨定 | 開頭 ≤1KB 序章引子（第一性原理×逆向）+ §2.F Single Thing |
| 3 | §3 產業格局 | 含利潤池位置、§3.F 逐段 TAM/SAM |
| 4 | §4 商業模式解剖＋核心門檻檢核（Munger） | |
| 5 | §5 護城河（報告核心） | 含權威 moat_trend、§5.F 對手 P&L、**§5.R 報酬持續期檢核** |
| 6 | §6 長期成長性 | 含 §6.A'' Y5 後跑道、§6.I 分部前瞻、增量 ROIC×再投資率 |
| 7 | §7 財務品質監測 | 含 §7.E DuPont+營運資金 |
| 8 | §8 即時財報情報 | |
| 8.5 | §8.5 隨附研究文獻 read-through | **條件性**:僅當有隨附外部文件才渲染 |
| 9 | §9 治理與資本配置 | 含 §9.D 10Y track、§9.E FCF 去向 |
| 10 | §10 估值與報酬（短章 ≤5KB） | 10.1/10.2/10.4 擇一呈現 + 10.5/10.6/10.7 |
| 11 | §11 矛盾辨識與強制裁決 | 渲染散文＋`<ul>`；逐 row 檢核與版本對帳進 `<details>`（見 references/decision-layer.md） |
| 12 | §12 Pre-mortem 與 Max DD | 渲染散文＋`<ul>`；Max DD 大數字＋色條保留 |
| 13 | **§13 決策（`<section id="decision">`）** | **統一裁決唯一居所;research 頁定見欄連此錨點**；末段接 E12 監測與觸發器表 |
| 14 | §14 複審觸發與保質期 | |
| 附錄 A | 擇時（降級） | `<details id="appA">` 整段折疊（列印時展開）——Pure MA / R:R / 估值燈 / 週線六態 / 大盤豁免 / 長期持有信心推導，**含原頁首儀表板移除的基本面評級細項（品質分／估值燈／Pure MA／陷阱定性）** |
| 附錄 B | 循環交易讀數（條件性） | `<details id="appB">`，**僅 QC-43 判定循環子型才渲染（archetype 驅動）**;按子型選位置錶（商品/capex/需求量三選一）+ 循環位置 5 檔 + 交易姿態 + 反動能硬閘（含閘 5 倍數）;明標投機;**v14.5:循環位置（cycle_position/cycle_verdict）落 dd-meta 並經 row 8b 接 §13;trade_stance 仍僅進 HTML**;成長股省略 |

### 功能規格

- 頁首固定：標的代碼 ｜ 資料抓取時間 ｜ 最新股價 ｜ DD Schema v15.0（writer 於 topbar 內填寫）
- **版本一號到底（v14.0 起）**:frontmatter `version`、dd-meta `schema`、`<meta dd-schema-version>`、頁首字串、INDEX.md Schema 欄**全部一致（目前 = `v15.0`）**。skill 版號（v15.2）**不外流到報告**——報告端 schema 維持 `v15.0`，只有 writer 契約與流程層變動。**下游相容**:validator（`^v1[2345]\.\d+$`）、pre-commit、`aggregate_dca_stats` / `update_dd_index` / `dd_screener_dd_loader` 等九站已放寬接受 v13.x ∪ v14.x ∪ v15.x，既有報告照常運作，不需回溯重跑。
- **`<head>` 由 render_dd 組裝，writer 不寫 `<head>`**：writer 只需在 BODY 提供 `dd-meta` script（含 `schema`）與 `<!-- TITLE: … -->` 註解；render_dd 據此產出 `<meta charset>`／`<meta name="robots" content="noindex,nofollow">`／`<meta name="dd-schema-version" content="v15.0">`／`<title>`。
- **`<section id="decision">` 錨點**:§13 決策章節的 `<section>` 必須帶 `id="decision"`。research 頁「定見」欄 link 到 `/dd/DD_{ticker}_{date}.html#decision`，漏寫錨點 → 定見連結跳到頁首而非裁決。
- **目錄導覽列**:由 `render_dd.py` 自動生成 `<nav class="dd-toc">`（依 BODY 內實際存在的 section／details id 產生 pill 連結，對照表見腳本契約），writer 不手寫 toc、不得省略任何一個 section 的 id。@media print 時 `.dd-toc` 隱藏。
- 右下角固定「列印為 PDF」按鈕，@media print CSS——皆由 render_dd／dd.css 承接，writer 不寫。
- 所有中文字型確保正常顯示。

### dd-meta JSON 區塊（schema v15.0，BODY 第 1 段，必填）

BODY 檔第一段必須是 `<script id="dd-meta" type="application/json">{...}</script>`，schema `v15.0`，含 22 個 v12 必填欄 + 5 個 v13 必填欄 + 20 個選填欄（完整 schema + enum 見 QC-32）。**render 後跑 QC-32 自驗腳本 + `python3 scripts/validate_dd_meta.py --report` 確認全綠才 commit。** 關鍵對映：`dca_verdict` = §13 裁決晶片;`dca_role` = §13a 角色;`moat_trend` = §5 權威趨勢（單一箭頭）;`runway_post_y5` = §6.A'';`ev5y_pct` = §10.5 5Y 累積機率加權 EV%（非年化）;`irr_base_pct` = §10.5 Base IRR;`max_dd_pct` = §12c 範圍下界;`asym_ratio` = §10.5 不對稱比 AR（選填，dd-meta 照填，但**不進頁首儀表板**）。

### 輸出規格（Claude Code 本地環境）

- 檔名格式：`DD_[標的代碼]_[YYYYMMDD].html`（v13 統一報告，**不再產獨立 DCA_*.html**）
- **輸出完成後必須執行以下步驟，不得省略**:
  1. **render + 四支驗證**（見上方「render 與四支驗證」段）。
  2. **更新 INDEX.md**（**並行模式例外見下方**）:Edit append 一行到 `docs/dd/INDEX.md`，8 欄格式：`| YYYY-MM-DD | TICKER | {同 frontmatter version（現 v15.0）} | {裁決}｜{角色}·{執行語} | 陷阱定性 | 護城河等級/估值燈/MA | DD_TICKER_YYYYMMDD.html | 備註 |`。**第 4 欄 ≤40 字**（v14.12 收斂，v15 沿用）:裁決＝進場/觀望/迴避三詞、角色＝核心/衛星/追蹤/不持有四值、執行語＝§13a 首句（starter 比例·rearm/加碼條件）;承繼/翻面歸因/矩陣路徑細節留在報告 §11.3 與備註欄，不進欄 4。基本面評級 A+/A/B/C/X 不放此欄（已在 dd-meta `signal`）。備註限 3 句，每句 30-50 字，`<br>` 分隔（第 1 句 產業位置+品質;第 2 句 估值+護城河趨勢;第 3 句 關鍵判斷/觀察點）。
  2-bis. **並行 session 例外（token 紀律）**:若編排者明示「不得寫入 INDEX.md／不得碰 catalog 檔」（多個 session 同時 append 會互相覆蓋），則**不 Edit 檔案，改在最終回報中直接輸出那一行 ready-to-paste 的完整 INDEX 行**（同 8 欄格式、同 備註 密度、`$` escape 為 `\$`、`<br>` 分隔、全形標點），由編排者機械貼上。**二選一，不得兩者都不做**——漏登的代價是報告存在於磁碟卻永遠不出現在 research 頁（`update_dd_index.py` 只收 INDEX.md 有列的 DD）。
  3. **觸發網站同步**:執行 `python scripts/update_dd_index.py`（同步 research 頁主表 + dd-screener;v13+ DD 報告由 script 直接讀 dd-meta 決策層欄位，定見欄連 `/dd/DD_X.html#decision`）。失敗則提示用戶手動執行，不得跳過。
  4. **terminal 摘要**（v14.5 格式）:
     ```
     ✅ v15.0 DD 報告完成:[TICKER]
     📄 檔案:docs/dd/DD_TICKER_YYYYMMDD.html
     💰 最新股價:$__
     🎯 統一裁決:[進場 / 觀望 / 迴避]（倉位角色:__）
     📊 基本面評級:[A+/A/B/C/X]（metadata）｜陷阱定性:[🟢/🟡/🔴]
     🛡️ 護城河趨勢:[↑/→/↓]（權威）｜Y5 後跑道:[🟢/🟡/🔴]｜Max DD:[−__%]
     📈 5Y EV:[+__%]／Base IRR:[__%/yr]（三分量:EPS __ / re-rate __ / 股息回購 __）
     💡 opportunity cost:__（點名同類現持倉）
     🔗 首頁同步:[✅ 成功 / ❌ 失敗,需手動 python scripts/update_dd_index.py]
     ```
     這是 terminal 允許輸出的**唯一**文字;章節內容仍嚴禁在對話框顯示。

### 篇幅紀律（v15.2）

篇幅規則以 SKILL.md QC-38＋【分章節 byte 預算】為準（75-105KB 帶、估值 ~7%、決策層 ≤12KB 渲染結論物）。機械閘＝`python3 scripts/dd_sections.py bytes FILE`（見上方「render 與四支驗證」）。BODY 預設分 2 次 Write 再 `cat` 合併（切點 s7／s8），part 檔可小幅 Edit（`docs/dd/` 產物禁 Edit）；分三次以上＝篇幅已失控，回頭套分章節省法。


## 頁首結論儀表板（不編號，最頂部；BODY 第 4 段）

合併舊 DD §1 dashboard + 舊 DCA Status Bar + 舊 DCA §2 一句話 thesis + 舊 DCA §5 裁決 headline。HTML 用 `.hypothesis-box` 樣式 + 上方一條 `.status-bar` grid。**基本面評級（A+/A/B/C/X）／估值燈／Pure MA 的細項已移入附錄 A，儀表板不再渲染整列 metadata**。

**一行式 Status Bar（grid，6-7 格）+ 下方儀表板 bullet**，必含以下欄位（數字全部從對應章節複製，QC-7 一致）:

| 欄位 | 來源 | 顯示 |
|:---|:---|:---|
| **一句話 thesis（≤50 字）** | 敘事性，禁用財務指標當主體 | 超大字 28px 居中（`.thesis`） |
| **統一裁決** | §13 裁決晶片 | 進場 #166534 / 觀望 #92400E / 迴避 #991B1B（白字 22px 粗體）|
| **倉位角色** | §13a `dca_role` | 核心/衛星/追蹤/不持有（v14.12 四值，「條件式」語意由 §13a 執行語承載） |
| **護城河趨勢 ↑→↓** | §5 權威 moat_trend | 等級 S/A/B/C + 箭頭（↑ #166534 / → #64748B / ↓ #991B1B） |
| **Y5 後跑道 🟢🟡🔴** | §6.A'' runway_post_y5 | emoji + ≤12 字 |
| **Max DD −__%** | §12c 範圍下界 | ≥−30% 綠 / −30~−50% amber / <−50% 紅 |
| **5Y EV／IRR** | §10.5 | EV +__% 5Y ／ IRR __%/yr（**單檔資訊，非排序貨幣;跨檔排序歸 GRP 三閘;此列不得出現 AR 或任何路徑對帳句**） |

儀表板 bullet（`.hypothesis-box` 內，承襲舊 DD 10 行 + DCA 決策層，**已刪基本面評級整列**）:
```html
<div class="status-bar"><!-- 一行 grid：統一裁決 / 護城河趨勢 / Y5 後跑道 / Max DD / 5Y EV·IRR --></div>
<div class="hypothesis-box">
<ul>
<li><strong>統一裁決 <span style="font-size:22px">進場 / 觀望 / 迴避</span></strong>（§13）｜倉位角色：__｜判定理由：__</li>
<li><strong>護城河趨勢 __ ↑/→/↓</strong>（§5 權威）｜execution 趨勢 __｜pricing power 趨勢 __</li>
<li><strong>Y5 後跑道 __（🟢/🟡/🔴）</strong>（§6.A''）｜S 曲線 __ ｜Y5 末滲透率 __%｜第二曲線 __</li>
<li><strong>Max DD −__%</strong>（§12c 範圍 −__~−__%，路徑風險 🟢/🟡/🔴）｜最快復原 __</li>
<li><strong>5Y 機率加權 EV +__%／IRR __%/yr</strong>（§10.5）｜Base IRR __%/yr（三分量 §10.6：EPS __ / re-rate __ / 股息回購 __）</li>
<li><strong>opportunity cost：</strong>__（§13a，點名同類現持倉，比較 R:R / conviction）</li>
<li><strong>長期持有信心：高/中/低</strong>（附錄 A）｜建議持有年限：__（§13c）</li>
<li><strong>Inception DD：</strong><code>DD_{ticker}_YYYYMMDD.html</code>（YYYY-MM-DD）— 累積漂移對照基準</li>
<li><strong>下次年度對照倒數：</strong>YYYY-MM-DD（距今 N 天）— Inception + 365 天</li>
</ul>
</div>
<p class="note"><strong>讀法：</strong>本份報告的人面對結論是「統一裁決 進場/觀望/迴避」（§13）。倉位組合佔比由 portfolio-manager skill 依組合狀態決定。</p>
```

**Inception 判定規則**:生成前掃描 `docs/dd/DD_{ticker}_*.html` 找最早一份 schema v12.2+ 的報告;找到 → Inception = 那份日期;找不到（本份是第一份）→ Inception = 本份日期，標 `(本份為 Inception)`。一旦設定不變更。
