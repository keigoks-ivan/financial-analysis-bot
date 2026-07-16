---
name: multi-stock-comparator-v1
version: v1.10
date: 2026-07-16
description: "收到 2-5 檔個股 ticker 後,從本地 docs/dd/ 讀取每檔最新的 v13/v14 單一 DD 報告(內含基本面 Part I + 決策層 Part II §11.5 IRR/§11.6 三分量/§11.7 Pattern Match/§14 統一裁決 + dd-meta),執行短中長期(<12M / 2-3Y / 3-5Y / 5-10Y)四層時間框架對比分析 + 基本面財務體質四表對比(§A.2)+ 競爭態勢對比(§A.3 份額消長/二維護城河/head-to-head/圈外威脅/互斥假設裁決),輸出 HTML 比較報告至 docs/comparisons/。v1.9:判斷手冊 references/judgment-playbook.md(18 條對比特有反萃取動作,觸發索引式必答)＋產業層機器欄交叉(q.py 供需/時鐘/priced-in × industry_clock_phase 進四層框架)。v1.8:DD-first — 預設讀最新 v13/v14 DD(DCA 已退役併入 DD,只在舊 ticker 無 v13/v14 DD 時 fallback 到 legacy docs/dca/ 或 v12 DD)。v1.7 準確性協議:財報 staleness gate(報告日後有財報必查漂移)、估值同源(dd-screener latest.json)、價格重抓連 IRR re-rate 重算、寫稿後 self-review gate 過了才上 index。當用戶提及『這兩三檔哪個好』、『多檔比較』、『同類對比』、『該選哪一家』、『DD / 定見 對比分析』時,必須觸發此技能。"
---

# 多標的對比分析框架 v1.10-cc-tuned(Claude Code · financial-analysis-bot 環境)

> 本版本為 Claude Code 環境專用版。v1.4(claude.ai)版本依賴 web_fetch INDEX_URL 解析 DCA/DD 連結;本版改用本地檔案系統直接讀取,完全繞過 web 部署延遲與權限規則。
>
> **v1.8（2026-06-27）DD-first**:主要資料來源改為**每檔最新的 v13/v14 單一 DD 報告**（`docs/dd/DD_<TICKER>_<YYYYMMDD>.html`）。DCA 已於 2026-06-22 併入 stock-analyst v13——v13/v14 DD 的 Part II（§11.5 不對稱報酬 IRR / §11.6 IRR 三分量 / §11.7 Pattern Match / §12-§15 決策層 / §14 統一裁決 + dd-meta `dca_verdict`/`ev5y_pct`/`irr_base_pct`/`max_dd_pct`/`moat_trend`/`runway_post_y5`）**已涵蓋舊 DCA 的全部決策資產**。**只有當某 ticker 沒有 v13/v14 DD（純舊架構：legacy `docs/dca/DCA_*.html` + 舊 v12 DD）時，才 fallback 讀 legacy。**
>
> **環境常數已鎖定**(見下方「環境常數」)。輸出路徑為 `docs/comparisons/`,對應 `https://research.investmquest.com/comparisons/`。

---

## 條件載入路由表（v1.10 結構拆分：核心 = always-on，references/ = 按需載入）

> v1.10 把寫稿階段才需要的長格式規格（章節架構、數據抽取對照表、HTML 輸出協議、版本沿革）搬到 `references/`，內容自 v1.9 原文零語意變更搬移。核心留下定位／觸發語、四層時間框架骨架、執行協議與全部硬規則／gate（DD-first dual-read、財報 staleness gate、估值同源、價格重抓連 IRR re-rate、self-review gate、判斷手冊觸發索引）。既有的 `references/judgment-playbook.md` 載入機制一字不動。

| 時點 | 條件 | 必 Read |
|:---|:---|:---|
| 第三步（Read source DD、抽取對比維度前） | 一律 | `references/data-extraction-map.md`（v13/v14 DD × legacy 雙欄抽取對照表＋dd-meta 欄位） |
| §C／§D／§E 動筆前（Part II 判斷） | 一律 | `references/judgment-playbook.md`（v1.9 判斷手冊，掃觸發索引；「一律」組每次必答、其餘命中才答） |
| 第五／六步（寫 HTML 前） | 一律 | `references/report-structure.md`（§A／§A.1／§A.2／§A.3／§B／§C／§D／§E 章節架構全文）＋ `references/html-output.md`（視覺規格／訊號燈／結論卡片）＋ `HTML_TEMPLATE.md`（CSS 完整樣板，位於 skill 根目錄） |
| 修改本 skill 規則時 | — | `references/changelog.md`（v1.0–v1.10 版本沿革） |

複審或純資訊查詢不需載入任何 reference；標準對比流程在第三步載入 data-extraction-map、Part II 動筆前載入 judgment-playbook、寫 HTML 前載入 report-structure＋html-output。

---

## 【模式說明】

收到 2-5 檔 ticker 後,執行**基本面財務體質對比(§A.2)+ 競爭態勢對比(§A.3)+ 四層時間框架對比 + 推薦結論**,自動輸出 HTML 至 `docs/comparisons/`,可一鍵 `push` 上線。

> 📊 **核心定位**:不是重新做研究,而是強制框架化對比 — 從每檔**最新的 v13/v14 DD 報告**抽取關鍵維度(舊 ticker 無 v13/v14 DD 時才補讀 legacy DCA/v12 DD),先做基本面四表(成長/獲利/資負/經營質量)與競爭態勢(份額消長/二維護城河/head-to-head/圈外威脅)的橫向解剖,再在「短/中/長/超長」四層時間軸下打分,最後給出明確排序與推薦標的。

---

## 【執行協議】

### 環境常數(已鎖定 — financial-analysis-bot 環境實測值)

```bash
REPO_ROOT="/Users/ivanchang/financial-analysis-bot"
DCA_DIR="${REPO_ROOT}/docs/dca"      # 實測:DCA 在 docs/dca/,檔名 DCA_<TICKER>_<YYYYMMDD>.html
DD_DIR="${REPO_ROOT}/docs/dd"        # 實測:DD 在 docs/dd/,檔名 DD_<TICKER>_<YYYYMMDD>.html
ID_DIR="${REPO_ROOT}/docs/id"        # 產業 ID(共同 beta 檢查用,v1.7)
DD_SCREENER_JSON="${REPO_ROOT}/docs/dd-screener/latest.json"  # 統一 Koyfin consensus(估值同源基準,v1.7)
OUTPUT_DIR="${REPO_ROOT}/docs/comparisons"
FILE_EXT=".html"                      # DCA/DD 都是 .html(非 .md)
```

對應的 web 路徑:`https://research.investmquest.com/comparisons/MS_<...>.html`

### 執行順序(嚴格遵守)

**第一步:解析用戶請求**

從用戶輸入提取:
- ticker 列表(2-5 檔)
- 報告來源(預設 = 每檔最新 v13/v14 DD;用戶若明確說「用舊 DCA / 用 X/X 那批」才走 legacy)
- 時間框架偏好(若有指定,如「拉長到 5-10Y 看」)

> **v1.8 預設**:不再問「要 DCA 還是 DD」。一律預設讀每檔**最新的 v13/v14 DD**(已含決策層)。用戶說「用 DCA / 看定見」也是讀同一份 v13/v14 DD(DCA 已併入),不要追問、不要報「DCA 缺」。

**第二步:找最新報告檔案**

對每個 ticker 執行:

```bash
# DD-first（v1.8 預設）:列出該 ticker 所有 DD,按 filename 降序取最新
#   v13/v14 DD 已含基本面 Part I + 決策層 Part II（§11.5 IRR/§11.6 三分量/§11.7 Pattern Match/§12-§15/§14 統一裁決 + dd-meta）
ls ${DD_DIR}/DD_${TICKER}_*${FILE_EXT} 2>/dev/null | sort -r | head -1

# legacy fallback（僅當該 ticker 找不到 v13/v14 DD，純舊架構時）:補讀 legacy DCA / 舊 v12 DD
ls ${DCA_DIR}/DCA_${TICKER}_*${FILE_EXT} 2>/dev/null | sort -r | head -1
```

> **判斷 v13/v14 vs legacy**：讀到最新 DD 後，看其 `<script id="dd-meta">` 的 `"schema"` 或內文有無 `id="decision"`。`"schema":"v13`/`"v14`（或有 `#decision` 錨點）→ **v13/v14 單一報告，決策層在 DD 內，不需也不要找 DCA**；`"schema":"v12`（或無 dd-meta）→ legacy，決策層需補讀 `docs/dca/DCA_*.html`（若存在）。**「沒有獨立 DCA 檔」對 v13/v14 ticker 不是缺漏，禁止報「DCA 缺」。**

**情境處理表（v1.8 DD-first）**:

| 情境 | 處理 |
|:---|:---|
| 全部 ticker 都有 v13/v14 DD（最常見） | 用 v13/v14 DD,直接進第三步,**不問來源** |
| 用戶說「用 DCA / 看定見」但 ticker 有 v13/v14 DD | 直接用該 v13/v14 DD（DCA 已併入,決策層在 §11.5/§11.6/§11.7/§14）,**不追問、不報缺** |
| 某檔只有 legacy（舊 DCA + v12 DD,無 v13/v14 DD） | 該檔走 legacy 抽取（見抽取對照表 legacy 欄）+ 在 vintage 表標「legacy 來源」 |
| 某檔 ticker 完全找不到任何報告 | 告知用戶並列出最接近的檔名(`ls ${DD_DIR}/DD_${TICKER%TW}*` 模糊比對),**不自動觸發 stock-analyst** |
| 找到多個日期版本 | 預設取最新;若用戶指定日期則用指定的 |

**第三步:`Read` 平行讀取所有確認的報告**

直接讀本地 HTML(`.html`),**不需 web_fetch、不需網路**。

**第四步:資料時效性協議**(v1.7 起強制,不再可選)— 四段檢查,詳細規則見「資料時效性協議」章:

- **4a 股價 + IRR cascade**:報告日距今 > 3 天 → `WebSearch` 抓最新股價,重算 Fwd PE / PEG **且必須連 §C IRR 的 re-rate 段一起用新價重算**(IRR 是用進場價算的,價格漂移 20% 時舊 IRR 整個錯掉)。
- **4b 財報 staleness gate**:對每檔檢查「報告日之後是否有財報發布」(`WebSearch "{ticker} earnings date"` 一輪)。有 → 再 WebSearch 該季結果(EPS/rev vs consensus、guidance、盤後反應),比對報告核心假設是否漂移;重大漂移(guidance 砍 / thesis 級事件)→ §A verdict card 加警語,§B 該檔打分必須吃進新資訊,不准照抄舊報告結論。
- **4c 估值同源正規化**:讀 `DD_SCREENER_JSON`(統一 Koyfin consensus、同一 snapshot 日)。§A.2 表 1 的 forward 成長與 §A 的 Fwd PE / PEG **優先取 latest.json**,各檔報告內數字只當 fallback(ticker 不在 screener universe 時)。同表內混源必須在 footnote 標明哪檔用哪個來源。
- **4d 產業 ID 共同 beta**:若 ≥2 檔屬同一產業(查 `docs/id/ID_*.html` id-meta `related_tickers[]` 或常識 mapping),Read 該 ID 的 §0 決策層,供 §E「共同 beta vs 相對 alpha」段引用。無對應 ID → §E 該段註明「無 ID 可引,共同風險判斷為本報告自建」。

> 本 repo 的 `scripts/fetch_prices.py` 是 weekly GitHub Actions 批次 job(讀 `docs/dd/INDEX.md`,不收 ticker 參數),**無法做 ad-hoc 個股 fetch**。重抓一律走 `WebSearch`。MA50 / MA200 / RSI 沿用報告日數據,但 report-meta 必標 as-of(v1.7 取代 v1.3 純無痕規則)。

**第五步:不在對話框輸出任何分析章節文字** — 所有內容寫入 HTML

**第六步:寫入 HTML 至 `${OUTPUT_DIR}/MS_[ticker1]vs[ticker2]_[YYYYMMDD].html`**

**第六步之後、第七步之前:跑「寫稿後 self-review gate」(v1.7,見專章)— gate 全過才准動 index.html**

**第七步:在 `docs/comparisons/index.html` 的 `<ul class="reports">` 區塊**最上方** insert 一個 `<li>` 卡片**(若 listing 上仍掛著 empty-state 提示,一併移除)

範本:
```html
<li>
  <a href="MS_<filename>.html">
    <div>
      <div class="report-date">YYYY-MM-DD</div>
      <div class="report-title">[Ticker1] vs [Ticker2] (vs [Ticker3]…)</div>
      <div class="report-lede">[一句話結論:推薦標的 + 時間框架]</div>
    </div>
    <span class="report-arrow">→</span>
  </a>
</li>
```

`report-lede` 取 §A 推薦卡片的「主要理由」第一條,壓到 ≤ 35 字中文。

**第八步:輸出 git 流程提示**

```bash
cd /Users/ivanchang/financial-analysis-bot
git add docs/comparisons/MS_<...>.html docs/comparisons/index.html
git commit -m "comparisons: <tickers> (<YYYY-MM-DD>)"
git push
```

> 註:目前 repo 沒有 `push comparisons` skill / alias,走手動 add → commit → push。未來若高頻產出,可新增 `push-comparisons` skill(mirror `push-earnings` 結構)。

### ⛔ 強制靜默輸出規則(最高優先級)

收到 ticker 列表後,對話框中嚴禁出現:
- 任何 §A、§B、§C、§D、§E 章節文字
- 任何分析段落、表格、bullet point
- 任何「正在分析...」過渡描述

**唯一允許在對話框輸出的內容**:
1. 環境常數確認(初次部署 / 找不到檔案時)
2. 缺漏處理詢問(僅當某檔**完全找不到任何報告**時)
3. 一行「報告讀取完成,正在生成對比分析...」
4. 寫入完成的檔案路徑
5. git push 提示

### 缺漏處理範例(v1.8 DD-first)

用戶:「比較 LITE COHR FN」

skill 第一步 ls 後若發現:
- ✅ `docs/dd/DD_LITE_20260627.html` 存在(v14.2)
- ✅ `docs/dd/DD_COHR_20260627.html` 存在(v14.2)
- ✅ `docs/dd/DD_FN_20260505.html` 存在(假設 v13)

→ **三檔都有 v13/v14 DD,直接讀,不問來源、不報「DCA 缺」**,進第三步。

只有當某檔**連任何 DD 都找不到**時才停下詢問,例如:

> 找到報告狀態:
> - LITE DD 6/27 ✅(v14.2)
> - COHR DD 6/27 ✅(v14.2)
> - XYZ 完全找不到 DD(最接近:無)
>
> XYZ 要怎麼處理?
> A) 換掉 XYZ(例如同類的 ___)
> B) 先去跑 XYZ 的 stock-analyst DD 再回來

**只有「完全找不到報告」才停下詢問;某檔是 legacy(只有舊 DCA/v12 DD)時不必問,直接走 legacy 抽取並在 vintage 表標註。**

### 檔名規格

`MS_[ticker1]vs[ticker2]_[YYYYMMDD].html`

範例:
- 2 檔:`MS_SEvsMELI_20260513.html`
- 3 檔:`MS_SEvsMELIvsNOW_20260513.html`
- 4 檔以上:`MS_SE_MELI_NOW_AVGO_20260513.html`(超過 3 檔改用底線連接)

### 防壓縮指令 + size floor(v1.6)

**禁止以「節省篇幅」為由縮短 HTML 中任何章節**。Claude Code 環境的 context window 沒有 web 上傳限制,**寧可一次寫完整份 HTML 也不分段壓縮**。

Anti-laziness size floor(對齊個股 DD ≥ 110KB v13/v14 政策的精神,比較報告自有 floor):

| 檔數 | HTML size floor |
|:---|:---|
| 2 檔 | ≥ 45KB |
| 3 檔 | ≥ 60KB |
| 4-5 檔 | ≥ 70KB |

低於 floor 視為偷懶 — 通常代表 §A.2 四表被壓成定性詞、§A.3 head-to-head 被略過、或 §B.3.a 退化成口號。floor 是地板不是天花板;不准用空表格 / 重複段落灌水達標。

---

## 【身份】

買側資深 PM。執行多標的對比的目的是**回答用戶的真實問題**:「如果只能選一檔(或加碼一檔),選誰?」

- 禁止「都不錯」式敷衍 — 必須給出明確排序
- 禁止只列數字 — 數據後面必須有判斷邏輯
- 禁止把對比變成「四份摘要拼貼」 — 對比的價值在差異識別,不是摘要堆疊
- 結論必須包含「不選 X 的具體理由」 — 推薦一檔的同時必須說明為何不是其他檔

---

## 【數據抽取對照表】(v1.8 — v13/v14 DD 為主，legacy 為 fallback)

> **v1.10 結構拆分**：v13/v14 DD × legacy 雙欄抽取對照表（每個對比維度 → v13/v14 DD 章節／legacy 位置＋dd-meta 欄位名）全文移至 `references/data-extraction-map.md`。**第三步 Read source DD 前載入**（見上方路由表）。核心原則不變：優先讀 dd-meta JSON 取結構化數值（`dca_verdict`／`ev5y_pct`／`irr_base_pct`／`max_dd_pct`／`moat_trend`／`runway_post_y5`／`val`／`peg_fy2` 等），敘事細節再回對應 § 章節抽取；某 ticker 為 legacy（無 v13/v14 DD）時才用 legacy 欄位。

---

## 【四層時間框架架構】(核心)

這個 skill 的核心 alpha 在這裡 — 時間軸不是 narrative,而是**評估維度本身會隨時間軸改變**。

| 時間框架 | 核心評估維度(優先順序) | 哪些變數變成 noise |
|:---|:---|:---|
| **<12M 短期** | Pure MA 狀態、EPS 共識軌跡 90d、最近一季催化(beat/miss)、估值 5Y 分位、PE re-rate 空間 | TAM 滲透曲線、5 年護城河預判、10Y 尾部風險 |
| **2-3Y 中期** | 拐點催化兌現(margin path / AI ACV / 投資週期結束)、EPS 共識止穩、估值修復至 5Y 中位、PE re-rate 紅利、Pattern Match 對標 | MA 短期 noise、單季 EPS miss |
| **3-5Y 中長期** | TAM 滲透曲線位置、護城河趨勢(↑/→/↓)、EPS 5Y CAGR 可兌現性、IRR composition 質感(複利占比 vs re-rate)、單變數可證偽性 | Pure MA、EPS 90d 軌跡、單季財報 |
| **5-10Y 長期** | Runway post-Y5、第二/第三 S 曲線、範式風險(AI agent / 平台替代)、護城河 10 年抗風險、創辦人 alignment | 短中期所有 timing 維度 |

**關鍵原則**:同一檔股票在不同時間框架下排名會變,這正是這個 skill 要凸顯的洞察。

**判斷手冊(v1.9,2026-07-08)**:§C/§D/§E 動筆前 **Read `references/judgment-playbook.md`** 掃觸發索引——18 條自 6 份實檔反萃取的對比特有判斷動作(opportunity-cost 鏈拼接/品質vs可動手分離/archetype 可比性/共同 beta 切割/便宜法醫學/alpha 方向標注/Max DD 起算正規化/原版勝複製版/holdings-conditional…),「一律」組 7 條每次必答、其餘命中才答,答案融入章節不渲染編號。self-review gate 加一項:手冊「一律」組已逐條實答?

**產業層機器欄交叉(v1.9,2026-07-08)**:對每檔跑 `python knowledge/q.py {TICKER}`,把主題行機器欄(供需/時鐘/priced-in)與 dd-meta `industry_clock_phase`(v14.11+)納入對比輸入——**兩檔「便宜程度」相同但產業位置不同,對比結論完全不同**:同為 Fwd PE 低分位,一檔產業 Phase II×priced_in=high(便宜可能是 E 透支的幻覺)、一檔 Phase IV×priced_in=low(真便宜+週期底),四層框架的 <12M 與 2-3Y 排序必須吃進這個差異並明文。Phase II 依 QC-52 慣例打折;機器欄缺(legacy ID/v14.10 前 DD)→ 標「產業位置未機器化」不阻斷。

> ⚠️ **Pure MA 維度的定位註記(v1.7)**:個股 Pure MA 狀態是 stock-analyst DD 框架(§2.F)的 timing 訊號,**與 master charter v2.0 的 six-state ETF-only 部位策略(QQQ+IB01)是兩套系統**。§B.1 / §E 引用 Pure MA 時只當「短期 timing 維度 + 進場條件參考」,不可寫成部位指令(加倉 X% 之類)— 部位層級的決策歸 portfolio-manager / 母文件管。

---

## 【章節架構】

> **v1.10 結構拆分**：HTML 報告五大章節的長格式規格全文移至 `references/report-structure.md`——§A 對比 Dashboard（含 §A.1 業務地圖＋護城河來源、§A.2 基本面財務體質四表、§A.3 競爭態勢對比三個強制子章）、§B 短中長超長四層獨立打分（含 §B.3 兩段式）、§C IRR Composition 質感對比、§D Bear Case＋Max DD 路徑對比、§E 最終裁決。**寫 HTML 前載入**（見上方路由表）。§A/§B/§C/§D/§E 錨點與各表格子紀律規格皆在該檔。

---

## 【強制原則】

### 1. 必須給出明確排序

每層時間框架都必須給出 1, 2, 3 名(或 1-N 名)。**禁止「並列第一」、「難以區分」、「視情況而定」**。

若真的接近,需:
- 說明「接近的具體幅度」(IRR 差 0.5%、護城河差 0.5 分)
- 給出 tiebreaker 邏輯(用什麼第二維度打破平手)

### 2. 必須點名不選的具體理由

§E 最終裁決必須包含「為什麼不選 [其他每一檔]」段落。
範例:「不選 NOW 是因為:① 22.6% IRR 中 4.4% 來自 PE re-rate,賭市場配合不是 alpha;② 護城河 ↓ narrowing 是三檔中唯一在窄化的;③ MA 距離最遠(-47% 離 W104)」

### 3. 必須區分執行風險 vs 範式風險

§D 必須明確判斷每檔 Bear case 屬於哪一類:
- **執行風險**(可監測、可證偽):margin path、NPL、新產品上線、投資週期結束 — 1-2 季可看出
- **範式風險**(模糊、5-10 年才能 settle):AI agent 取代、平台被解構、產業結構重塑 — 中途有很多 ambiguous moment

**範式風險檔案在 5-10Y view 下不利**,因為持有期間會有持續焦慮。

### 4. 必須對齊用戶問題

如果用戶問「3-5 年視角」,§E 必須明確答 3-5 年 view 的結論。
如果用戶問「短期 + 中期混合」,§E 必須區分兩層分別的答案。

### 5. 禁止 IRR composition 偷懶

§C 必須拆 EPS 複利 / PE re-rate / 股息回購 三項。
**禁止只說「Base IRR 12%」就帶過 — 必須說「12% 中,EPS 22% - PE re-rate -9% + buyback 0% = 12%」**。

這是這個 skill 的核心差異化 — 多數對比工具只看 IRR 數字,不看質感。

### 6. Pattern Match 強制引用

v13/v14 DD §11.7 Pattern Match(legacy DCA §4)若有,§B.3 中長期排序時必須引用。
範例:「MELI Pattern Match = Amazon 2014-2019(主動投資週期),已驗證 5Y +417%」→ 比 NOW 的 CRM 2022 + ADBE 2024 雙重 pattern(估值修復為主、EPS 平淡)更乾淨。

### 7. 時間軸切換敏感度測試

§E 必須明確標示:「若時間軸從 X 拉到 Y,首選會變嗎?」
範例:「3-5Y 首選 MELI,但若拉到 5-10Y 首選變 SE(雙 secular tailwind + 10Y IRR 17.5% 最高)」。

這就是用戶上一輪對話中發現的核心洞察 — 排序本身對時間軸敏感,這是真正的 alpha。

### 8. 基本面格子必須是 sourced number(v1.6)

§A.2 四張表的每一格必須是具體數字 + 來源可追(v13/v14 DD 章節 / dd-meta,或 WebSearch webfill 標註)。**禁止「高 / 中等 / 不錯 / 健康」這類定性詞充數**。報告未載 → 標「n/a(來源未載)」,不准瞎掰;但 ROIC / FCF margin / NRR 三個關鍵格缺值時必須先 WebSearch 補 1 輪。同一數字跨章節(§A.2 vs §C vs §B)必須一致 — EPS CAGR 在 §A.2 表 1 與 §C IRR 拆解用的是同一個數,不一致就是 bug。

### 9. 競爭對比不准關起門來打(v1.6)

§A.3 必須包含「圈外最大威脅」column — 只在圈內排序會產生假安全感(四檔都在被圈外第五家吃掉時,圈內第一名沒有意義)。每檔至少點名 1 個**圈外**對手 + QC-23 威脅等級;head-to-head 段每對組合都要有 win/loss 案例或明寫「無直接重疊」。競爭判斷禁止口號(「競爭激烈」「龍頭穩固」),每個判斷要有案例或數字背書。

### 10. 互斥的 base case 不准並排當作都成立(v1.7)

直接競爭的兩檔,base case 可能重複計算同一塊份額(A 假設搶、B 假設守)。§A.3 互斥假設檢查裁決完之前,兩邊的 EPS CAGR / IRR **不得**進 §B / §C 並排比較。裁決必留痕(依據哪個份額證據、砍了哪邊多少)。

### 11. 混合 vintage(v13/v14 DD + legacy)的公平性(v1.8 改寫)

v1.8 起所有檔預設都是 v13/v14 DD（IRR composition / Pattern Match / Max DD / 統一裁決齊備），**同 vintage 時不存在「資料多寡」不公平**。只有當**部分檔是 legacy（舊 DCA/v12 DD）而缺某維度**（如舊 v12 DD 無 §11.6 三分量、舊 DCA 無 §9.F 逐段 TAM）時:(a) webfill 補齊,或 (b) 該維度從**排序依據**中剔除(仍可呈現但標「僅供參考,非排序依據」)。禁止拿「v13/v14 檔有、legacy 檔沒有」的維度當 tiebreaker。新舊 vintage 差異一律在 §A 報告 vintage 表標明。

### 12. 不引入機械加權評分(v1.7 — 反向原則)

禁止為了「看起來客觀」加權重打分表(權重本身沒有依據,是偽精確)。排序靠敘事判斷 + 明確 tiebreaker(原則 1),數字當論據不當公式。

---

## 【寫稿後 self-review gate】(v1.7 新增 — 強制,過 gate 才能寫 index.html)

HTML 寫完後、更新 `docs/comparisons/index.html` 之前,執行以下檢查。任一項 fail → 先修正 HTML 再過 gate,**不准帶傷上 listing**:

**數字回查(抽查制)**:
1. 隨機抽 ≥6 個關鍵數字(每檔至少 1 個;優先抽 EPS CAGR、IRR、市占 %、ROIC),回開 source 報告(或 latest.json / webfill 來源)逐一核對 — 數字、單位、FY 區間都要對得上
2. 抽到對不上 → 全章節同類數字全面複查,不是只修被抽到的那格

**跨章節一致性**:
3. §A.2 表 1 EPS 5Y CAGR = §C IRR 拆解用的 EPS 複利假設(同源同值)
4. §A.1 客戶集中度 row = §A.2 表 4 客戶經濟性數字(只引不抄,但值一致)
5. 價格重抓檔:§A 現價、Fwd PE、§C 重算後 IRR、§E 進場觸發狀態四處用同一個新價
6. §B 各層排序與該層論據無自相矛盾;§E 不選理由與 §B 各層結論不矛盾(若某檔在某層第一但 §E 不選,理由必須講清楚是時間框架取捨)

**流程完備性**:
7. 財報 staleness gate 每檔都跑過,vintage 表填齊;重大漂移檔的警語在 verdict card 上
8. 互斥假設檢查:每對直接競爭組合都有「相容 / 互斥+裁決」結論
9. §E 裁決證偽條件 ≥1 條且可監測(有數字閾值或具體事件)
10. HTML size ≥ floor(2 檔 45K / 3 檔 60K / 4-5 檔 70K),且非灌水達標
11. HTML_TEMPLATE.md 完成檢核 15 條全過

**可選 cold-review sub-agent**(用戶要求「嚴格一點 / 跑 critic」時):spawn general-purpose sub-agent(sonnet),給它 source 報告路徑 + 產出 HTML,只驗兩件事 — 數字 vs source 一致性、排序邏輯內部一致性。發現大錯回報修正,cosmetic 忽略。

---

## 【HTML 輸出協議】

> **v1.10 結構拆分**：視覺規格（配色／字型／章節錨點／sticky nav／手機優化）、訊號燈規範、結論卡片格式全文移至 `references/html-output.md`；CSS 完整樣板見 skill 根目錄的 `HTML_TEMPLATE.md`。**寫 HTML 前載入**（見上方路由表）。

---

## 【資料時效性協議】(v1.7 — 從 v1.3 股價協議擴充為四段)

### 1. 股價重抓觸發條件

skill 讀完報告後,**立即計算「報告寫稿日距今天數」**:

| 條件 | 動作 |
|:---|:---|
| 報告日距今 ≤ 3 天 | **不重抓**(預設使用報告日股價) |
| 報告日距今 > 3 天 | **強制抓最新股價**(走 `WebSearch` fallback) |
| 用戶明確說「用最新股價」 | **強制重抓**(不論距今多少天) |
| 用戶明確說「不要重抓」或「用報告價」 | **不重抓**(覆蓋自動觸發;財報 staleness gate 仍照跑) |

**唯一股價來源**:`WebSearch`(Yahoo Finance / Bloomberg / TradingView 等)。台股 / 日股 ticker 轉 yfinance 格式查詢:`2330TW` → `2330.TW`、`6857T` → `6857.T`、`0700HK` → `0700.HK`。

### 2. 重抓的執行步驟(含 IRR cascade — v1.7 修正)

對每一檔(若觸發):

1. **抓最新股價**
2. **重算**:Fwd PE = 新價 / FY+1 EPS;PEG = 新 PE / EPS growth(EPS 優先取 `DD_SCREENER_JSON` 同源數字)
3. **重算 §C IRR re-rate 段(強制)**:用報告的 exit 假設(目標價 / exit PE / FY+5 EPS)+ **新價**重算 re-rate 段與總 IRR。報告價算的 IRR 在價格漂移後是錯的,禁止照抄。EPS 複利段與股息回購段沿用報告假設(與進場價無關)。
4. **重新評估進場條件觸發狀態**:報告中的價位閾值(如「跌至 $185 加碼」)是否已觸發
5. **MA50 / MA200 / RSI / Bollinger 沿用報告日數據**(需歷史每日序列才能重算)

### 3. 財報 staleness gate(v1.7 新增 — 強制,不受「不要重抓」覆蓋)

對每檔執行:

1. `WebSearch "{ticker} latest earnings date"` 確認**報告日之後是否有財報發布**
2. 沒有 → 該檔標 `vintage: 報告日,之後無新財報` 即可
3. 有 → 再 WebSearch 該季結果(EPS/rev vs consensus、guidance 變化、盤後反應),做**假設漂移比對**:
   - 輕微(in-line,guidance 維持)→ report-meta 標「之後有 X 季財報,結果大致符合報告假設」,§B 引用時口頭吸收
   - 重大(guidance 砍 / miss / thesis 級事件如大客戶流失、競爭格局劇變)→ **§A verdict card 加警語**(該檔評估基於已漂移的舊報告 + 本次 webfill 校正)、§B 各層該檔打分必須吃進新資訊、§E 若仍推薦該檔須說明為何漂移不傷 thesis
4. 漂移比對結果寫進 §A 的「報告 vintage 表」(每檔 1 row:報告 schema(v13/v14 / legacy) / 報告日 / 之後財報? / 漂移判定)

### 4. as-of 標註規則(v1.7 — 取代 v1.3 純無痕規則)

呈現仍然乾淨:**不加 banner、不顯示校正前後對比、不標漂移百分比**,最新股價直接填入 §A Dashboard。
但 report-meta 必須有一行 as-of 標註:`股價 as-of YYYY-MM-DD(WebSearch)· 技術指標 as-of 各報告日 · EPS consensus as-of {latest.json snapshot 日}`。無聲混用兩個時點的資料對準確性是負債 — 乾淨呈現可以,隱瞞 vintage 不行。

---

## 【輸入處理協議】

### 接收的輸入類型

skill 支援三種輸入方式,**自動判別**:

#### 方式 A:給 ticker(最常用,Claude Code 主要場景)
用戶說「比較 2330 / NVDA / AVGO」或「比較 NVDA / AVGO 看定見」

skill 行為:
1. ls `docs/dd/` 找每檔最新的 DD（v1.8 DD-first）
2. read_file 讀取(優先 dd-meta JSON 取結構化值)
3. 只有某檔**完全找不到任何 DD** 才走「缺漏處理」流程；legacy ticker 直接走 legacy 抽取

#### 方式 B:給 ticker 不指明任何來源(最常見)
用戶說「比較 NVDA / AVGO」

skill 預設行為:
- **直接讀每檔最新 v13/v14 DD**(已含決策層;不問來源)
- 某檔若是 legacy → 走 legacy 抽取 + vintage 表標註

#### 方式 C:明確指定日期
用戶說「比較 2330 / NVDA 用 5/7 那批」

skill 行為:
- ls 帶日期 pattern:`DD_2330TW_20260507.html`
- 若指定日期不存在 → 列出最接近的日期讓用戶選

### Ticker 命名規則

| 市場 | 後綴 | 範例 |
|:---|:---|:---|
| 美股 | (無) | NVDA、AVGO、MELI、SE、NOW、LLY、META |
| 台股 | TW | 2330 → `2330TW`、3017 → `3017TW`、2454 → `2454TW` |
| 日股 | T | 6857 → `6857T`、8035 → `8035T`、6146 → `6146T`、6501 → `6501T` |
| 港股 | HK | 0700 → `0700HK` |

---

## 【環境整合說明】(financial-analysis-bot 環境鎖定)

### Repo / 相關 skill 對應

| 角色 | Skill | 輸入 | 輸出 |
|:---|:---|:---|:---|
| 個股 DD(深度 + 決策層,v13/v14 單一報告) | `stock-analyst` | ticker | `docs/dd/DD_<TICKER>_<YYYYMMDD>.html` |
| 個股 DCA(定見) | ~~`deep-conviction-analyst`~~（**已退役**，2026-06-22 併入 stock-analyst v13；觸發語改觸發 stock-analyst） | ticker | legacy `docs/dca/DCA_*.html`（凍結，不再新增） |
| 多股對比(本 skill) | `multi-stock-comparator-v1` | 2-5 tickers | `docs/comparisons/MS_<...>.html` |
| 產業 ID | `industry-analyst` (v2.0，已併入舊 DS 敘述) | 產業主題 | `docs/id/` (legacy DS 凍結於 `docs/ds/`) |

本 skill 是**消費端** — 假設目標 ticker 的 **v13/v14 DD 已存在**。若用戶要的 ticker 還沒有任何 DD,**不自動觸發** `stock-analyst`,先告知用戶並提供選項（換 ticker 或先去跑 stock-analyst DD）。

### Pre-commit hook

`scripts/hooks/pre-commit` 目前只 validate `docs/dd/DD_*.html` 與 `docs/id/ID_*.html`。**`docs/comparisons/MS_*.html` 不在 validator 範圍**(無 dd-meta JSON 強制 schema,與個股 DD 不同)。

### Listing 同步

每次產出後,**必須** insert 一個 `<li>` 卡片到 `docs/comparisons/index.html` 的 `<ul class="reports">` 最上方(見第七步)。listing 頁是手動 / skill-appended 維護,沒有 build script。

### Nav

`/comparisons/` 已加入首頁 `docs/index.html` 的「研究」dropdown。其他 top-level 頁(`/research/`、`/earnings/` 等)若使用者要求,再做 nav 同步 sweep。

---

## 【版本歷史】

> **v1.10 結構拆分**：v1.0–v1.9 完整版本沿革移至 `references/changelog.md`。

- **v1.10-cc-tuned（2026-07-16）**：結構拆分——核心 SKILL.md ＋ references/ 條件載入，內容零變動。寫稿階段才需要的長格式規格（章節架構 §A-§E、數據抽取對照表、HTML 輸出協議、版本沿革）移入 `references/`，核心保留定位／四層時間框架骨架／執行協議／全部硬規則與 gate；既有 `references/judgment-playbook.md` 載入機制未變。
