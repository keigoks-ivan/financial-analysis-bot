# stock-analyst v14.7 — html-output.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-07 v14.7 結構拆分，內容自 v14.6 原文搬移、語意零變更）。必讀時點見 SKILL.md 條件載入路由表。修改規則請同步 SKILL.md stub 與 references/changelog.md。

## 【HTML 輸出協議】

完成所有章節後，**立即使用 Write 工具生成完整 HTML 報告檔案**，不得省略或延後。HTML 必須包含所有章節完整分析，不得摘要化。

### 視覺規格

- **配色**:主背景 #F8FAFC，卡片白底 #FFFFFF，章節標題深藍 #1E3A5F
- **字型**:Noto Sans TC（內文）+ IBM Plex Mono（數字/代碼），引用 Google Fonts
- **表格**:白底交替淺藍灰列（#F1F5F9），標題列深藍底（#1E3A5F）白字
- **章節標題**:深藍 #1E3A5F 底色，左側 4px accent 線（#3B82F6），h2 加 `scroll-margin-top: 80px`
- **頁首 Status Bar**:一行 grid（`display:flex; gap:12px; justify-content:center`），每格上方標籤 11px #64748B + 下方主體 22px 粗體;整條底色 #F1F5F9，左右各 4px accent 線 #3B82F6;任一格缺資料顯示「—」不砍格
- **Thesis 區塊**:超大字 28px 居中，底色 #EFF6FF
- **§14 Decision 區塊**:背景 進場 #F0FDF4 / 觀望 #FEF9C3 / 迴避 #FFF1F2;左 4px 線 進場 #166534 / 觀望 #92400E / 迴避 #991B1B;裁決晶片 inline-block padding 6px 20px border-radius 4px font-size 18px font-weight 700 + 左 4px 線;晶片副標籤 13px #475569 斜體
- **§12 矛盾區塊**:底色 #FFF7ED（淺橘），左 4px 線 #F97316;不可調和 🔴、可調和 🟡;強制裁決表用 #FED7AA 區隔
- **§13b Pre-mortem 區塊**:底色 #FEF2F2（淺紅警示），左 4px 線 #DC2626，narrative 引用框
- **§13c Max DD 區塊**:主數字 32px（`−45% ~ −55%`），下方 color bar 視覺化（0~−30 綠 / −30~−50 amber / <−50 紅）
- **§11.5 Pattern match / §11.6 IRR Composition**:底色 #F0F9FF（淺藍學習感），左 4px 線 #0EA5E9/#0284C7;IRR mini-table 3×4，分量年化 % 正綠負紅灰中性 + 下方橫向 stacked bar（綠 EPS + 藍 re-rate + 灰 股息回購）
- **價值陷阱警示區塊**:橘紅底 #FFF0E6，左 4px 線 #F97316，標題字 #C2410C
- **§3 核心假設區塊**:淺藍底 #EFF6FF，左 4px 線 #3B82F6
- **狀態標記**:Beat/符合 #DCFCE7 綠底 #166534 字;Miss/不符合 #FEE2E2 紅底 #991B1B 字;中性/待確認 #FEF9C3 黃底 #92400E 字;情境表 樂觀 #DCFCE7 / 中性 #FEF9C3 / 悲觀 #FEE2E2;估值訊號 🔴 #FEE2E2 / 🟡 #FEF9C3 / 🟢 #DCFCE7 / 🔵 #EFF6FF
- **整體風格**:金融研究報告質感，無圓角過度裝飾，線條簡潔，留白充足。**禁止**漸層背景、過重陰影、非專業裝飾。

### 章節顯示順序（HTML 呈現）

| 顯示位置 | 章節 | 說明 |
|:---|:---|:---|
| 0（最頂部） | 頁首結論儀表板 | Status Bar + thesis + 統一裁決 |
| 1 | §1 投資結論詳述 | trap 四問 + 最關鍵監測指標 |
| 2 | §2 序章 | 第一性原理 × 逆向 |
| 3 | §3 投資論點錨定 | 含 §3.F Single Thing |
| 4 | §4 即時財報情報 | |
| 4.5 | §4.5 隨附研究文獻 read-through | **條件性**:僅當有隨附外部文件才渲染 |
| 5 | §5 核心門檻檢核 | |
| 6 | §6 長期成長性 | 含 §6.A'' Y5 後跑道、§6.I 分部前瞻 |
| 7 | §7 護城河（報告核心） | 含權威 moat_trend、§7.F 對手 P&L |
| 8 | §8 財務品質監測 | 含 §8.E DuPont+營運資金 |
| 9 | §9 產業格局 | 含利潤池位置、§9.F 逐段 TAM/SAM |
| 10 | §10 治理與資本配置 | 含 §10.D 10Y track、§10.E FCF 去向 |
| 11 | §11 估值與報酬 | 11.1/11.2/11.4 + 11.5/11.6/11.7 |
| 12 | §12 矛盾辨識與強制裁決 | |
| 13 | §13 Pre-mortem 與 Max DD | |
| 14 | **§14 決策（`<section id="decision">`）** | **統一裁決唯一居所;research 頁定見欄連此錨點** |
| 15 | §15 複審觸發與保質期 | |
| 附錄 A | 擇時（降級） | Pure MA / R:R / 估值燈，折疊式（`<details>`，列印時展開） |
| 附錄 B | 循環交易讀數（條件性） | **僅 QC-43 判定循環子型才渲染（archetype 驅動）**;按子型選位置錶（商品/capex/需求量三選一）+ 循環位置 5 檔 + 交易姿態 + 反動能硬閘（含閘 5 倍數）,折疊式;明標投機;**v14.5:循環位置（cycle_position/cycle_verdict）落 dd-meta 並經 row 8b 接 §14;trade_stance 仍僅進 HTML**;成長股省略 |

### 功能規格

- 頁首固定:標的代碼 ｜ 資料抓取時間 ｜ 最新股價 ｜ DD Schema v14.9
- **版本一號到底（v14.0 起）**:frontmatter `version`、dd-meta `schema`、`<meta dd-schema-version>`、頁首字串、INDEX.md Schema 欄**全部一致（目前 = `v14.9`）**（沿用本 repo 歷史慣例:一個版號到底）。**下游相容**:validator（`^v1[234]\.\d+$`）、pre-commit floor（`"schema":"v1[34]`）、`aggregate_dca_stats` / `update_dd_index` / `dd_screener_dd_loader`（`startswith(("v13","v14"))`）已放寬接受 v13.x ∪ v14.x，既有 v13.0 報告照常運作，不需回溯重跑。**未來再升版時:bump 此 5 欄一致 + 放寬上述 6 個 pipeline 檢查多接受新版號。**
- **`<head>` 機讀標籤（全部必填）**:
  - `<meta charset="utf-8">` 之後緊接 `<meta name="robots" content="noindex,nofollow">`（私站防爬，research.investmquest.com noindex 政策）
  - `<meta name="dd-schema-version" content="v14.9">`（= frontmatter version，一號到底）
- **`<section id="decision">` 錨點**:§14 決策章節的 `<section>` 必須帶 `id="decision"`，h2 加 `scroll-margin-top: 80px`。research 頁「定見」欄 link 到 `/dd/DD_{ticker}_{date}.html#decision`，漏寫錨點 → 定見連結跳到頁首而非裁決。
- **目錄導覽列（強制）**:頁首之後緊接 `<nav class="dd-toc">`，含 anchor 連結指向各章節（§1 結論 / §2 序章 / §3 論點 / §4 財報 / §5 門檻 / §6 成長 / §7 護城河 / §8 財務 / §9 產業 / §10 治理 / §11 估值 / §12 矛盾 / §13 pre-mortem / §14 決策 / §15 複審 / 附錄 A 擇時）。pill-shape badges 樣式;每個 `<section>` 有對應 `id`;@media print 時 `.dd-toc` 隱藏。**禁止省略**。
- 右下角固定「列印為 PDF」按鈕（window.print()）
- @media print CSS:隱藏頁首與按鈕，附錄 A 折疊區全部展開，確保列印整潔
- 所有中文字型確保正常顯示

### dd-meta JSON 區塊（schema v14.9，HTML `<head>` 內，必填）

HTML `<head>` 內必須含 `<script id="dd-meta" type="application/json">{...}</script>`，schema `v14.9`，含 22 個 v12 必填欄 + 5 個 v13 必填欄 + 20 個選填欄（完整 schema + enum 見 QC-32）。**生成後跑 QC-32 自驗腳本 + `python3 scripts/validate_dd_meta.py --report` 確認全綠才 commit。** 關鍵對映:`dca_verdict` = §14 裁決晶片;`dca_role` = §14a 角色;`moat_trend` = §7 權威趨勢（單一箭頭）;`runway_post_y5` = §6.A'';`ev5y_pct` = §11.5 5Y 累積機率加權 EV%（非年化）;`irr_base_pct` = §11.5 Base IRR;`max_dd_pct` = §13c 範圍下界;`asym_ratio` = §11.5 不對稱比 AR（選填）。

### 輸出規格（Claude Code 本地環境）

- 檔名格式:`DD_[標的代碼]_[YYYYMMDD].html`（v13 統一報告，**不再產獨立 DCA_*.html**）
- 使用 Write 工具輸出至 `docs/dd/`
- **輸出完成後必須執行以下步驟，不得省略**:
  1. **生成後自驗**:跑 QC-32 自驗腳本 + `python3 scripts/validate_dd_meta.py --report`（確認 v13 五欄 + enum 全綠）;確認 `id="decision"` 錨點存在;確認 dca_verdict 三處（頁首/§14/dd-meta）一致。
  2. **更新 INDEX.md**:Edit append 一行到 `docs/dd/INDEX.md`，8 欄格式:`| YYYY-MM-DD | TICKER | {同 frontmatter version（現 v14.9）} | 統一裁決(進場/觀望/迴避) | 陷阱定性 | 護城河等級/估值燈/MA | DD_TICKER_YYYYMMDD.html | 備註 |`。第 4 欄為**統一裁決**（取自 §14;基本面評級 A+/A/B/C/X 不放此欄，已在 dd-meta `signal`）。備註限 3 句，每句 30-50 字，`<br>` 分隔（第 1 句 產業位置+品質;第 2 句 估值+護城河趨勢;第 3 句 關鍵判斷/觀察點）。
  3. **觸發網站同步**:執行 `python scripts/update_dd_index.py`（同步 research 頁主表 + dd-screener;v14.9 DD 報告由 script 直接讀 dd-meta 決策層欄位，定見欄連 `/dd/DD_X.html#decision`）。失敗則提示用戶手動執行，不得跳過。
  4. **terminal 摘要**（v14.5 格式）:
     ```
     ✅ v14.9 DD 報告完成:[TICKER]
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

### 防壓縮指令

**禁止以「節省篇幅」為由縮短 HTML 中任何章節內容。** 若單一 Write 無法容納全部，先輸出前半，說明「HTML 第一部分已生成，繼續生成第二部分...」，等用戶回「繼續」後以 Edit 追加。**寧可分段追加，絕不壓縮內容，也絕不改為文字輸出。**


## 頁首結論儀表板（不編號，最頂部）

合併舊 DD §1 dashboard + 舊 DCA Status Bar + 舊 DCA §2 一句話 thesis + 舊 DCA §7 裁決 headline。HTML 用 hypothesis-box 樣式（淺藍底 #EFF6FF，左 4px 線 #3B82F6）+ 上方一條 Status Bar grid。

**一行式 Status Bar（grid，6-7 格）+ 下方儀表板 bullet**，必含以下欄位（數字全部從對應章節複製，QC-7 一致）:

| 欄位 | 來源 | 顯示 |
|:---|:---|:---|
| **一句話 thesis（≤50 字）** | 敘事性，禁用財務指標當主體 | 超大字 28px 居中 |
| **統一裁決** | §14 裁決晶片 | 進場 #166534 / 觀望 #92400E / 迴避 #991B1B（白字 22px 粗體）|
| **倉位角色** | §14a `dca_role` | 核心/衛星/投機/條件式/不持有 |
| **護城河趨勢 ↑→↓** | §7 權威 moat_trend | 等級 S/A/B/C + 箭頭（↑ #166534 / → #64748B / ↓ #991B1B） |
| **Y5 後跑道 🟢🟡🔴** | §6.A'' runway_post_y5 | emoji + ≤12 字 |
| **Max DD −__%** | §13c 範圍下界 | ≥−30% 綠 / −30~−50% amber / <−50% 紅 |
| **5Y 機率加權 EV／IRR** | §11.5 | EV +__% 5Y ／ IRR __%/yr（爆發候選裁決時加註 AR __）**（單檔資訊，非排序貨幣;跨檔排序歸 GRP 三閘）** |

儀表板 bullet（hypothesis-box 內，承襲舊 DD 10 行 + DCA 決策層）:
```html
<div class="status-bar"><!-- 一行 grid：統一裁決 / 護城河趨勢 / Y5 後跑道 / Max DD / 5Y EV·IRR --></div>
<div class="hypothesis-box">
<p class="thesis">一句話 thesis（≤50 字敘事）</p>
<ul>
<li><strong>統一裁決 <span style="font-size:22px">進場 / 觀望 / 迴避</span></strong>（§14）｜倉位角色：__｜判定理由：__</li>
<li><strong>護城河趨勢 __ ↑/→/↓</strong>（§7 權威）｜execution 趨勢 __｜pricing power 趨勢 __</li>
<li><strong>Y5 後跑道 __（🟢/🟡/🔴）</strong>（§6.A''）｜S 曲線 __ ｜Y5 末滲透率 __%｜第二曲線 __</li>
<li><strong>Max DD −__%</strong>（§13c 範圍 −__~−__%，路徑風險 🟢/🟡/🔴）｜最快復原 __</li>
<li><strong>5Y 機率加權 EV +__%／IRR __%/yr</strong>（§11.5）｜Base IRR __%/yr（三分量 §11.6：EPS __ / re-rate __ / 股息回購 __）｜AR __（不對稱比;爆發候選裁決時必列）</li>
<li><strong>opportunity cost：</strong>__（§14a，點名同類現持倉，比較 R:R / conviction）</li>
<li><strong>基本面評級 __（A+/A/B/C/X，metadata）：</strong>品質 __/10｜估值燈 __｜Pure MA __｜陷阱定性 __（詳見附錄 A）</li>
<li><strong>長期持有信心：高/中/低</strong>（附錄 A I）｜建議持有年限：__（§14c）</li>
<li><strong>Inception DD：</strong><code>DD_{ticker}_YYYYMMDD.html</code>（YYYY-MM-DD）— 累積漂移對照基準</li>
<li><strong>下次年度對照倒數：</strong>YYYY-MM-DD（距今 N 天）— Inception + 365 天</li>
</ul>
</div>
<p class="note"><strong>讀法：</strong>本份報告的人面對結論是「統一裁決 進場/觀望/迴避」（§14）。基本面評級 A+/A/B/C/X 為 metadata（餵 screener），不是並列頭銜。倉位組合佔比由 portfolio-manager skill 依組合狀態決定。</p>
```

**Inception 判定規則**:生成前掃描 `docs/dd/DD_{ticker}_*.html` 找最早一份 schema v12.2+ 的報告;找到 → Inception = 那份日期;找不到（本份是第一份）→ Inception = 本份日期，標 `(本份為 Inception)`。一旦設定不變更。

