---
name: multi-stock-comparator-v1
description: "收到 2-5 檔個股 ticker(可選 DCA / DD)後,從本地 dca/ 或 dd/ 目錄讀取最新報告,執行短中長期(<12M / 2-3Y / 3-5Y / 5-10Y)四層時間框架對比分析,輸出 HTML 比較報告至 docs/comparisons/。當用戶提及『這兩三檔哪個好』、『多檔比較』、『同類對比』、『該選哪一家』、『DCA / DD 對比分析』時,必須觸發此技能。"
---

# 多標的對比分析框架 v1.5-cc-tuned(Claude Code · financial-analysis-bot 環境)

> 本版本為 Claude Code 環境專用版。v1.4(claude.ai)版本依賴 web_fetch INDEX_URL 解析 DCA/DD 連結;本版改用本地檔案系統直接讀取,完全繞過 web 部署延遲與權限規則。
>
> **環境常數已鎖定**(見下方「環境常數」)。輸出路徑為 `docs/comparisons/`,對應 `https://research.investmquest.com/comparisons/`。

---

## 【模式說明】

收到 2-5 檔 ticker(可選 DCA / DD)後,執行**四層時間框架對比 + 推薦結論**,自動輸出 HTML 至 `docs/comparisons/`,可一鍵 `push` 上線。

> 📊 **核心定位**:不是重新做研究,而是強制框架化對比 — 從現有 DCA/DD 報告抽取關鍵維度,在「短/中/長/超長」四層時間軸下橫向打分,最後給出明確排序與推薦標的。

---

## 【執行協議】

### 環境常數(已鎖定 — financial-analysis-bot 環境實測值)

```bash
REPO_ROOT="/Users/ivanchang/financial-analysis-bot"
DCA_DIR="${REPO_ROOT}/docs/dca"      # 實測:DCA 在 docs/dca/,檔名 DCA_<TICKER>_<YYYYMMDD>.html
DD_DIR="${REPO_ROOT}/docs/dd"        # 實測:DD 在 docs/dd/,檔名 DD_<TICKER>_<YYYYMMDD>.html
OUTPUT_DIR="${REPO_ROOT}/docs/comparisons"
FILE_EXT=".html"                      # DCA/DD 都是 .html(非 .md)
```

對應的 web 路徑:`https://research.investmquest.com/comparisons/MS_<...>.html`

### 執行順序(嚴格遵守)

**第一步:解析用戶請求**

從用戶輸入提取:
- ticker 列表(2-5 檔)
- 報告類型偏好(DCA / DD / 混合 / 預設)
- 時間框架偏好(若有指定,如「拉長到 5-10Y 看」)

**第二步:找最新報告檔案**

對每個 ticker 執行:

```bash
# 主邏輯:列出該 ticker 所有 DCA,按 filename 降序取最新
ls ${DCA_DIR}/DCA_${TICKER}_*${FILE_EXT} 2>/dev/null | sort -r | head -1

# 若用戶指定 DD 或 DCA 不存在則 fallback
ls ${DD_DIR}/DD_${TICKER}_*${FILE_EXT} 2>/dev/null | sort -r | head -1
```

**情境處理表**:

| 情境 | 處理 |
|:---|:---|
| 全部 ticker 都有 DCA(且用戶未指定 DD) | 用 DCA,進入第三步 |
| 用戶指定 DCA 但某檔只有 DD | 詢問用戶:(a) 該檔換用 DD(混合)(b) 換 ticker (c) 等該檔 DCA |
| 用戶指定 DD | 全用 DD |
| 某檔 ticker 完全找不到 | 告知用戶並列出最接近的檔名(`ls ${DCA_DIR}/DCA_${TICKER%TW}*` 等模糊比對) |
| 找到多個日期版本 | 預設取最新;若用戶指定日期則用指定的 |

**第三步:`Read` 平行讀取所有確認的報告**

直接讀本地 HTML(`.html`),**不需 web_fetch、不需網路**。

**第四步:股價時效性協議**(可選,視用戶習慣)

若報告日距今 > 3 天,執行 `WebSearch` 抓最新股價並重算 Fwd PE / PEG。詳見「股價時效性協議」段。

> 本 repo 的 `scripts/fetch_prices.py` 是 weekly GitHub Actions 批次 job(讀 `docs/dd/INDEX.md`,不收 ticker 參數),**無法做 ad-hoc 個股 fetch**。報告日 >3 天且需重抓時,直接走 `WebSearch` fallback。MA50 / MA200 / RSI 沿用報告日數據(v1.3 無痕呈現規則保留)。

**第五步:不在對話框輸出任何分析章節文字** — 所有內容寫入 HTML

**第六步:寫入 HTML 至 `${OUTPUT_DIR}/MS_[ticker1]vs[ticker2]_[YYYYMMDD].html`**

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
2. 缺漏處理詢問(用戶指定 DCA 但某檔沒有時)
3. 一行「報告讀取完成,正在生成對比分析...」
4. 寫入完成的檔案路徑
5. git push 提示

### 缺漏處理範例

用戶:「比較 LITE COHR FN 用 DCA」

skill 第一步 ls 後若發現:
- ✅ `docs/dca/DCA_LITE_20260512.html` 存在
- ✅ `docs/dca/DCA_COHR_20260510.html` 存在
- ❌ `docs/dca/DCA_FN_*.html` 不存在(但 `docs/dd/DD_FN_20260505.html` 在)

對話框輸出:

> 找到三檔的最新報告狀態:
> - LITE DCA 5/12 ✅
> - COHR DCA 5/10 ✅
> - FN DCA 缺,DD 5/5 有
>
> 要怎麼處理?
> A) FN 用 DD 替代(混合,FN 將缺 §4 IRR composition + Pattern Match)
> B) 換掉 FN(例如 CRDO、ALAB)
> C) 等你跑出 FN DCA 再回來

**禁止在用戶確認前自行決定處理方式**。

### 檔名規格

`MS_[ticker1]vs[ticker2]_[YYYYMMDD].html`

範例:
- 2 檔:`MS_SEvsMELI_20260513.html`
- 3 檔:`MS_SEvsMELIvsNOW_20260513.html`
- 4 檔以上:`MS_SE_MELI_NOW_AVGO_20260513.html`(超過 3 檔改用底線連接)

### 防壓縮指令

**禁止以「節省篇幅」為由縮短 HTML 中任何章節**。Claude Code 環境的 context window 沒有 web 上傳限制,**寧可一次寫完整份 HTML 也不分段壓縮**。

---

## 【身份】

買側資深 PM。執行多標的對比的目的是**回答用戶的真實問題**:「如果只能選一檔(或加碼一檔),選誰?」

- 禁止「都不錯」式敷衍 — 必須給出明確排序
- 禁止只列數字 — 數據後面必須有判斷邏輯
- 禁止把對比變成「四份摘要拼貼」 — 對比的價值在差異識別,不是摘要堆疊
- 結論必須包含「不選 X 的具體理由」 — 推薦一檔的同時必須說明為何不是其他檔

---

## 【DCA vs DD 數據抽取對照表】

不同來源的報告章節結構不同,skill 自動依來源類型抽取對應數據:

| 對比維度 | DCA 抽取自 | DD 抽取自 |
|:---|:---|:---|
| 護城河評分 + 趨勢 | Phase A1 | §9 護城河、§2.0 產業風向燈 |
| Runway 跑道 | Phase A2 | §8.A Runway / §8.A' S 曲線 |
| EPS CAGR 預估 | EPS 預測參考表 + §4 IRR composition | §7 + §8.E 壓力測試 |
| 5Y IRR(Bull/Base/Bear) | §4 Asymmetry Analysis | §8.E + §13 估值 |
| Max DD 評級 | §6c 路徑壓力測試 | §13 同業比較推導 |
| Pure MA 狀態 | §7c | §2.F |
| 估值 + PEG | EPS 預測表 + §4 IRR re-rate | §2.D、§13.2 |
| 5 年後護城河預判 | §6b Pre-mortem + Phase A1 趨勢 | §9.D 護城河變遷時間軸 |
| §5 Single Thing | §5 | §5.C 三大風險 |
| Pattern Match | §4 Pattern Match | §3 估值仲裁員 + §13 |
| FCF Margin / ROIC | Phase A3 | §10、§7 門檻檢核 |

**若報告類型混合(DCA + DD)**:優先取 DCA 的 IRR composition + Pattern Match,優先取 DD 的 §13 同業估值 + §9.D 護城河變遷時間軸。

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

---

## 【章節架構】

HTML 報告結構固定五大章節:

### §A 對比 Dashboard(綜合一覽)
- 三檔基本資料表(現價 / 市值 / Fwd PE / 5Y 分位 / 護城河 / Runway / 訊號燈)
- 四層時間框架排序卡片
- 一句話結論(推薦標的 + 主要理由)

### §A.1 業務地圖 + 護城河來源對照(v1.5 新增 — 強制章節)

這節要回答:**「四檔到底做什麼、靠什麼賺錢、競爭對手是誰、護城河的具體 mechanism 是什麼?」** — 不是評分,是 anatomy。

必含一張「業務地圖 + 護城河來源」對照表,N + 1 columns(維度 + 每檔一欄),固定 6 rows:

| Row | 內容要求 |
|:---|:---|
| **營收 mix**(latest FY) | 各 segment 占比 + 1 行 trend(例:Auto 50% / Industrial 30% / Comm 20%,Auto 過去 2 年由 45% → 50%) |
| **主要產品線**(具體 part / platform) | 不是「賣晶片」這種抽象描述,要寫具體 product family(例:S32 platform、SiC MOSFET 1200V、ASIL D MCU) |
| **客戶集中度** | Top 1 / Top 5 / Top 10 客戶占比 + 是否有 OEM dual-track risk(in-house 替代) |
| **直接對打的 socket** | 在這次比較圈裡,該檔直接對打誰的什麼 socket(例:NXPI vs STM 在 SDV central compute、TXN vs ADI 在 BMS DAC) |
| **護城河來源**(具體 mechanism) | 禁止只寫「scale / brand / IP」這種抽象詞。要寫具體 mechanism(例:ASIL D + S32 toolchain → Tier-1 7-15 年 lock-in;300mm Analog fab → cost lead 25-30%) |
| **護城河趨勢來源** | 趨勢箭頭 ↑/→/↓ + 1 行根因(例:↑ ← 200mm SiC 量產顯著拉開成本 / → ← 認證體系穩定但中國 local 追上中) |

表後必含一段「**業務地圖洞察**」 box(box-alpha),內容:
- 在這個比較圈裡,**業務 overlap 最深的是哪兩檔**(用相同 product family 直接對打)
- 哪檔業務最 differentiated(有獨家 segment 不在其他三檔產品線裡)
- 哪檔護城河 mechanism 是「結構性硬 lock-in」(認證 / 平台 / 7+ 年 design cycle) vs 「執行領先」(良率 / 成本曲線 / scale)— 前者抗擊穿能力強很多

### §B 短中長超長四層獨立打分
四個獨立小節,每層獨立評估、獨立給排序:
- **§B.1 <12M 短期**:Pure MA + EPS revision + 最近催化
- **§B.2 2-3Y 中期**:拐點催化 + 估值修復 + PE re-rate
- **§B.3 3-5Y 中長期**:護城河來源解剖(深) + TAM + EPS 兌現 + IRR 質感(兩段式 — v1.5 強制)
- **§B.4 5-10Y 長期**:Runway post-Y5 + 範式風險 + 第二曲線

每層必須:
- 列出該時間框架最關鍵的 3-5 個維度
- 三檔(2-5 檔)横向對比表
- 給出該層的排序(第一 / 第二 / 第三)
- 一段「為什麼這個排序」的判斷邏輯(不是堆疊數字)

### §B.3 兩段式架構(v1.5 強制)

§B.3 不能再是「Moat 評級 1 row + IRR 表」的快剪。必須拆成上下兩段:

**§B.3.a 護城河來源解剖**(必含)

對每檔回答三個問題,逐檔寫一段 100-200 字:
1. **這檔的護城河 mechanism 具體是什麼?**(引 §A.1 的「護城河來源」row 並 expand)
2. **這個 mechanism 為什麼能撐 3-5 年?**(時間因素:認證年限 / 設計週期 / 客戶切換成本 / 良率學習曲線斜率)
3. **3-5 年內最可能讓 mechanism 失效的單一事件是什麼?**(對齊 §5 Single Thing)

這 3 段不是堆疊數字 — 是 mechanism 級別的判斷。**禁止只寫「ASIL D 很硬 / 300mm 成本領先很強」** 這種口號,必須寫「ASIL D 從新 OEM 評估到投產要 5-7 年,所以 2030 前歐美 Top 5 OEM 不會切換」這種有時間軸的因果鏈。

**§B.3.b 排序判斷**(必含)

承接 §B.3.a,給排序 + 判斷邏輯。原本的 IRR 表 / Pattern Match 表保留在這段。

---

### §C IRR Composition 質感對比(縱深層)
這是 3-5Y view 真正的 alpha 所在,必須獨立成章:
- 各檔的 EPS 複利 / PE re-rate / 股息+回購 拆解
- **強調「靠自己跑」vs「靠市場配合」的差別**
- 拆解 Base IRR 的依賴假設(單變數 vs 多變數)
- 可證偽性比較

### §D Bear Case + Max DD 路徑對比
- 各檔的 §5 Single Thing
- Bear 觸發機率與時間軸
- Max DD 評級對比
- 觸發後復原時間
- **誰的 Bear case 是「執行風險」(可控可監測),誰是「範式風險」(模糊不可控)**

### §E 最終裁決
- 四層時間框架最終排序矩陣(誰在哪層第一)
- 用戶問題重新審視:用戶問的是「3-5Y view 對嗎?」、「能不能拉長到 10Y?」
- **推薦標的明確點名 + 不選其他的具體理由**
- 進場條件與監測指標(若有 Pure MA ❌ 等限制)
- 一句話 takeaway

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

若 DCA 報告有 Pattern Match 段落,§B.3 中長期排序時必須引用。
範例:「MELI Pattern Match = Amazon 2014-2019(主動投資週期),已驗證 5Y +417%」→ 比 NOW 的 CRM 2022 + ADBE 2024 雙重 pattern(估值修復為主、EPS 平淡)更乾淨。

### 7. 時間軸切換敏感度測試

§E 必須明確標示:「若時間軸從 X 拉到 Y,首選會變嗎?」
範例:「3-5Y 首選 MELI,但若拉到 5-10Y 首選變 SE(雙 secular tailwind + 10Y IRR 17.5% 最高)」。

這就是用戶上一輪對話中發現的核心洞察 — 排序本身對時間軸敏感,這是真正的 alpha。

---

## 【HTML 輸出協議】

### 視覺規格(對齊 InvestMQuest research.investmquest.com 風格)

CSS 規格詳見 `HTML_TEMPLATE.md`。核心要點:

- **背景**:`#ffffff`(白底)
- **主文字**:`#1a1d24`
- **強調**:`#000000`(粗體)
- **強調色**:藍 `#1565c0`、橘 `#c2410c`、綠 `#15803d`、紅 `#991b1b`
- **表格邊框**:`#d0d8e0`
- **字型**:`-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", Roboto, sans-serif`
- **章節錨點**:`#sA`、`#sB1`、`#sB2`、`#sB3`、`#sB4`、`#sC`、`#sD`、`#sE`
- **頂部導航**:固定 sticky,提供快速跳轉
- **手機優化**:`@media (max-width: 768px)` 內字級放大、padding 縮小

### 訊號燈規範

四種主要訊號燈(對齊 DCA / DD):
- 🟢 高確信 / 寬 / 便宜
- 🟡 中性 / 中等 / 觀察期
- 🔴 警示 / 窄 / 昂貴
- ⚫ X(迴避)

排序視覺:
- 🥇 第一名(綠底)
- 🥈 第二名(灰底)
- 🥉 第三名(橘底)
- (4 檔以上續用數字)

### 結論卡片格式

§A Dashboard 頂部必須有「綜合裁決卡片」:

```
推薦標的:[Ticker]
適用時間框架:3-5 年
主要理由(三條):
1. [一行]
2. [一行]
3. [一行]
進場條件:[Pure MA 確認 / 拐點催化 / 等等]
```

---

## 【股價時效性協議】

(從 v1.3 沿用)

### 觸發條件

skill 讀完報告後,**立即計算「報告寫稿日距今天數」**:

| 條件 | 動作 |
|:---|:---|
| 報告日距今 ≤ 3 天 | **不重抓**(預設使用報告日股價) |
| 報告日距今 > 3 天 | **強制抓最新股價**(走 `WebSearch` fallback) |
| 用戶明確說「用最新股價」 | **強制重抓**(不論距今多少天) |
| 用戶明確說「不要重抓」或「用報告價」 | **不重抓**(覆蓋自動觸發) |

### Claude Code 環境的股價來源

**唯一來源**:`WebSearch`(各大財經網站,如 Yahoo Finance / Bloomberg / TradingView 等)。

本 repo 的 `scripts/fetch_prices.py` 是 weekly GitHub Actions 批次 job(讀 `docs/dd/INDEX.md`,不收 ticker 參數),**無法做 ad-hoc 個股 fetch**。台股 / 日股 ticker 用 yfinance 格式查詢時轉換:`2330TW` → `2330.TW`、`6857T` → `6857.T`、`0700HK` → `0700.HK`。

### 重抓的執行步驟

對每一檔(若觸發 > 3 天條件):

1. **抓最新股價**(用 1. 或 2. 的方式)
2. **重算**:Fwd PE = 新價 / FY+1 EPS;PEG = 新 PE / EPS growth
3. **重新評估進場條件觸發狀態**:報告中的價位閾值(如「跌至 $185 加碼」)是否已觸發
4. **僅校正可重算指標**(現價 / Fwd PE / PEG / 進場觸發狀態)
5. **MA50 / MA200 / RSI / Bollinger 沿用報告日數據**(需歷史每日序列才能重算,Claude Code 環境可選擇連 yfinance 補,但複雜度高)

### v1.3 無痕呈現規則

**不另外標示「校正前/校正後」、不顯示「漂移百分比」、不加 banner**。
直接用最新股價填入所有 §A Dashboard 欄位,讓報告**看起來就像本來用最新股價寫的**。

---

## 【輸入處理協議】

### 接收的輸入類型

skill 支援三種輸入方式,**自動判別**:

#### 方式 A:給 ticker(最常用,Claude Code 主要場景)
用戶說「比較 2330 / NVDA / AVGO 用 DCA」或「比較 NVDA / AVGO 看 DD」

skill 行為:
1. ls 本地 dca/ 或 dd/ 目錄找最新檔
2. read_file 讀取
3. 若有缺漏 → 走「缺漏處理」流程

#### 方式 B:給 ticker 但不指明類型
用戶說「比較 NVDA / AVGO」沒講要 DCA 還是 DD

skill 預設行為:
- 優先 DCA(IRR composition + Pattern Match 完整載體)
- 若無 DCA → fallback DD

#### 方式 C:明確指定日期
用戶說「比較 2330 / NVDA 用 5/7 那批 DCA」

skill 行為:
- ls 帶日期 pattern:`DCA_2330TW_20260507.html`
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
| 個股 DD(深度) | `stock-analyst` | ticker | `docs/dd/DD_<TICKER>_<YYYYMMDD>.html` |
| 個股 DCA(定見) | `deep-conviction-analyst` | ticker | `docs/dca/DCA_<TICKER>_<YYYYMMDD>.html` |
| 多股對比(本 skill) | `multi-stock-comparator-v1` | 2-5 tickers + DCA/DD | `docs/comparisons/MS_<...>.html` |
| 產業 ID | `industry-analyst` (v2.0，已併入舊 DS 敘述) | 產業主題 | `docs/id/` (legacy DS 凍結於 `docs/ds/`) |

本 skill 是**消費端** — 假設 DCA / DD 已存在。若用戶要的 ticker 還沒有 DCA / DD,**不自動觸發** `stock-analyst` 或 `deep-conviction-analyst`,先告知用戶並提供選項。

### Pre-commit hook

`scripts/hooks/pre-commit` 目前只 validate `docs/dd/DD_*.html` 與 `docs/id/ID_*.html`。**`docs/comparisons/MS_*.html` 不在 validator 範圍**,與 DCA 同政策(無 meta JSON 強制 schema)。

### Listing 同步

每次產出後,**必須** insert 一個 `<li>` 卡片到 `docs/comparisons/index.html` 的 `<ul class="reports">` 最上方(見第七步)。listing 頁是手動 / skill-appended 維護,沒有 build script。

### Nav

`/comparisons/` 已加入首頁 `docs/index.html` 的「研究」dropdown。其他 top-level 頁(`/research/`、`/earnings/` 等)若使用者要求,再做 nav 同步 sweep。

---

## 【版本歷史】

- **v1.5-cc-tuned(2026-05-26)**:補強 skill 結構性缺口 — 用戶 feedback「基本面 / 業務面 / 競爭態勢 / 護城河說明過少」。新增 **§A.1 業務地圖 + 護城河來源對照**(6 rows × N 檔,強制章節 — 營收 mix、主要產品線、客戶集中度、直接對打 socket、護城河 mechanism、護城河趨勢來源)+ box-alpha 業務地圖洞察;**§B.3 拆成兩段式**(§B.3.a 護城河來源解剖每檔 100-200 字 mechanism 級判斷,禁止口號;§B.3.b 排序判斷承接 a 段),解決 v1.4 將護城河壓縮成「評分 + 趨勢箭頭」一格的問題。骨架其他章節維持不動。
- **v1.4-cc-tuned(2026-05-13)**:在 Claude Code (financial-analysis-bot) 環境完成 fine-tune — 環境常數鎖定為 `docs/dca/` / `docs/dd/` / `docs/comparisons/` / `.html`;股價來源固定走 `WebSearch`(`fetch_prices.py` 為 batch job 不適用 ad-hoc);git flow 為手動 `add / commit / push`,未啟用 push-comparisons skill;新增第七步「append 到 `docs/comparisons/index.html`」。「環境參數待確認」段刪除。
- **v1.4-cc(2026-05-13)**:Claude Code 環境專用版本。第一步改為 ls 本地 dca/ / dd/ 目錄(取代 v1.4 的 web_fetch INDEX_URL)。直接 read_file 本地 markdown(取代 web_fetch report URL)。輸出至 `docs/comparisons/` 而非 `/mnt/user-data/outputs/`,可直接 git push 上線。新增「環境參數待確認」段,部署時需與本地 Claude 確認真實路徑/檔名/git 流程。
- **v1.4(2026-05-13)**:加入 INDEX_URL 強制第一步協議,解決 Claude.ai 環境 web_fetch 權限限制。但發現 INDEX 頁更新頻率 ≠ DCA 產生頻率,導致新 DCA 仍可能 fetch 失敗(LITE/COHR/FN 案例)。本問題在 cc 版徹底解決(直接讀本地檔)。
- **v1.3(2026-05-13)**:股價校正改為「無痕呈現」 — 不再顯示「校正前/校正後對比」、不加 banner、不標漂移百分比。
- **v1.2(2026-05-13)**:加入股價時效性協議。報告日 > 3 天自動 web_search 最新股價並重算 Fwd PE / PEG。
- **v1.1(2026-05-13)**:配色翻轉成白底深字。加入「從 ticker 自動找 URL」協議。
- **v1.0(2026-05-13)**:Inception 版本。
