# industry-analyst v4.0 — sources.md（來源與紀律，條件載入 reference）

> 寫 mechanics 段（供給／需求／估值皆涉及來源判斷）之前 Read 本檔。內容搬自 v3.0 SKILL.md 全文，語意不變，只重編排、去除舊 QC／機械閘編號。

## 【資料來源四級】

資料來源分 4 級，**Tier 1（公司官方簡報／技術 keynote／10-K／IR deck）為最高優先**，必須先嘗試。低階層只能在高階層找不到時作為補充，且必須標註等級。

- 核心承重數字（TAM／裁決／玩家矩陣）必須 T1，否則直接返工。
- 若某主題 T1 全無可得（少見），必須在 summary 下方加警語：「本報告依賴 T2/T3 為主，結論偏觀點」。

### Tier 1（Primary · 一手原始）— 優先搜

| 類別 | 範例 | 搜尋方式 |
|:---|:---|:---|
| 公司投資人簡報（IR deck） | `nvidianews.nvidia.com/events/gtc`／`investor.amd.com` | `{公司} investor day 2026 slides`、`{公司} quarterly presentation Q4` |
| 技術 keynote 簡報 | NVIDIA GTC／Apple WWDC／Intel Tech Tour／TSMC Symposium | `{公司} GTC 2026 architecture slides`、`{公司} technology roadmap keynote` |
| 財報電話會議逐字稿 | Seeking Alpha transcript、公司官網 IR 頁 | WebFetch 公司 IR 頁或 motleyfool.com/earnings-call-transcripts |
| 10-K／10-Q／20-F | SEC EDGAR／TWSE 公開資訊觀測站／HKEX | WebFetch `sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}` |
| 公司官網技術白皮書 | `nvidia.com/technologies/`、`asml.com/en/technology` | WebFetch 直接抓 HTML |
| 專利庫查詢 | USPTO、EPO、Google Patents | `{technology} patents holder 2025 USPTO` |

### Tier 2（Authoritative Third-party · 權威第三方）

產業協會／研究機構（SEMI、SIA、Yole Group、IC Insights、TechInsights、IDC、Gartner、IEA、USDA、IFR）；學術期刊／IEEE；政府／政策文件（US CHIPS Act、EU Chips Act、工研院、Fed、ECB、BLS、Eurostat）；標準組織（JEDEC、IEEE P1838、OCP）；權威財經媒體（Bloomberg、Reuters、FT、WSJ、Nikkei）。

### Tier 3（Analyst／Media · 分析師媒體）— 內部再分三級

**T3-A｜券商產業研究報告**（highest in T3，**優於 T2 部分資料**）：產業深度 Primer／Initiation（Morgan Stanley「AI Infrastructure Primer」、TD Cowen「Advanced Packaging Deep-Dive」）、Sector Update／Thematic、Channel Check（券商引用實地供應鏈訪談，數據質量接近 T1）。券商「產業報告」優先級與 T2 並列、部分情境高於 T2；券商「個股目標價」維持 T3。引用標 `[T3-A: Morgan Stanley AI Infra Primer 2026-03-15 p.24]`。遇 T3-A vs 公司 T1 IR deck 衝突，IR deck 為準，T3-A commentary 可作反方依據。

**T3-B｜券商個股報告／主流財經媒體**：券商個股 PT、Barron's、Forbes、Fortune。

**T3-C｜專業媒體／Substack 深度**：AnandTech、SemiAnalysis、Tom's Hardware、The Information、SemiWiki、EE Times；付費 Substack（Dylan Patel、Ben Thompson）。署名分析師可信度升至 T3-A 等級。

### Tier 4（Social／Wiki · 社群維基）— 僅作線索

Wikipedia（歷史時間軸，不用於數字）、Reddit／Twitter／Seeking Alpha 評論（僅作 lead）。**禁止作為 data claim 的唯一來源**。

### 券商研究的特殊地位

| 規則 | 說明 |
|:---|:---|
| 優先抓取 | 主動搜 `{主題} Morgan Stanley primer`／`{主題} Goldman initiation`／`{主題} Jefferies deep dive` |
| 多券商交叉 | 單一券商結論不可作唯一依據，需 ≥2 家券商支持（或與 T1/T2 交叉） |
| 偏見校準 | 記錄券商 stance（Long／Short／Neutral）；三家都 Long → debates 段要特別小心 |
| 時效性 | 券商 primer 通常 12–24 個月一次大更新；確認最新版 |
| 頁碼標註 | 引用必須含 `p.XX` 或 slide number |

## 【T1 floor（依 mega 分型，v4.0 新增）】

| mega 分型 | T1（+T1-zh）floor |
|---|---:|
| `macro`／`cloud`／`space` | 45% |
| 其餘 11 個 mega（`semi`／`bio`／`energy`／`consumer`／`finance`／`industrial`／`staples`／`reits`／`housing`／`transport`／`materials`／`agri`） | 60% |

WHY：v3.0 首發（cloud 主題）固定 60% 造成結構性卡稿——時事快變／macro 型主題 T1 供給天生較薄。`mega` 從 id-meta 必填欄讀取，由 `docs/id/taxonomy.md` controlled vocabulary 決定，不由 writer 自報。唯一覆蓋出口：主題屬時事快變型但分類落在 60% 組（如 semi 底下的 AI 推論經濟學）時，可用 `check_id.py --t1-floor 45` 覆蓋，**不得低於 45%**，且須在 check 報告與 summary 折疊內各寫一句理由。floor 未達標 → summary 下方加警語「本報告依賴 T2/T3 為主，結論偏觀點」。核心承重數字（TAM／裁決／玩家矩陣）無論分型，優先 T1。

## 【中文來源分類】

| 對應 Tier | 來源類別 | 具體名稱 | 使用規則 |
|:---|:---|:---|:---|
| T1-zh | 公司中文 IR／法說材料 | 台積電／聯電／聯發科／日月光／光寶官網法說 PDF 或公開資訊觀測站 | 等同 T1，優先使用 |
| T1-zh | 公開資訊觀測站年報／重訊 | `mops.twse.com.tw` | 等同 T1 |
| T1-zh | 台股法說會逐字／簡報錄影 | 公司官網 IR 直播、YouTube 官方帳號 | 等同 T1（需寫引用時間戳） |
| T2-zh | 政府／法人研究機構 | 工研院 IEK／資策會 MIC／金工中心／國發會 | 等同 T2 |
| T2-zh | 專業研究公司 | TrendForce（集邦）、DRAMeXchange、CINNO | 等同 T2，但半導體預測需與英文 T1 交叉 |
| T3-zh | 半導體專業媒體 | DIGITIMES、電子時報 | 等同 T3，單一來源需交叉驗證 |
| T3-zh | 主流財經媒體 | 工商時報、經濟日報、財訊、商周、天下、鉅亨網 | 等同 T3 |
| T3-zh | 中文付費 Substack／產業分析 | 大叔美股筆記、半導體行業觀察、Medium 中文產業專欄 | 等同 T3，署名分析師可升 T2 |
| T3.5-zh | 知名 Named-analyst 貼文 | 天風郭明錤、Dan Nystedt、DIGITIMES 謝達志 | 高可信度 T3，仍需交叉驗證 |
| T4-zh | 社群／論壇 | PTT Stock 板、Mobile01、Facebook 社團 | 僅作 lead，不可作唯一來源 |

引用規範：中文來源條目 tier 加 `-zh` 後綴；中文與英文 T1 衝突時優先英文 T1（保留中文觀點作補充）；工研院／TrendForce 預測與英文 T2（Yole／IC Insights）差異 >20% 時，須並列兩者並註明差異。

## 【常見來源搜尋捷徑】

| 主題 | 首選 T1 來源 |
|:---|:---|
| AI 硬體／GPU | NVIDIA GTC、AMD Advancing AI、Intel Innovation |
| 半導體設備 | ASML Investor Day、AMAT IMEC Symposium、TSMC Technology Symposium |
| 先進封裝 | TSMC OIP、ASE SEMICON、IMEC Future Summit |
| 記憶體 HBM | Micron Investor Day、Samsung Memory Tech Day、SK Hynix 韓國 IR |
| EV／電池 | Tesla Battery Day、BYD IR、Panasonic Tech Day |
| 生技／GLP-1 | Novo Nordisk R&D Day、Lilly Investor Day、ACC/ADA 學術年會 |
| 雲端／SaaS | Microsoft Ignite、Google Cloud Next、AWS re:Invent |
| 航運／大宗 | Clarksons、Drewry、Baltic Exchange、LME、Citi/GS commodity desk |

## 【來源衝突處理】

兩個 T1 給出不同數字時，必須明確列衝突：

```
項目X：A 公司投資人日報 80%（slide 12）[T1]
        B 公司技術大會 60%（slide 4）[T1]
        [衝突] → 差異原因：統計口徑不同（含/不含 OEM）
        結論採值：70%（區間中點）或選較保守值
```

禁止「偷偷擇一不說衝突」。

## 【Spurious Specificity 禁令】

**禁止精準數字**（除非 source 直接公告該確切值）：

| 類別 | ❌ 禁止 | ✅ 允許 |
|:---|:---|:---|
| 市佔（估算） | "62.7%" / "78.3%" | "~70%" / "60-65%" / "~6 成" |
| 預估時間 | "2027-09-15" / "2027 Q3 中旬" | "2027 H2" / "2027 Q3-Q4" |
| 預估 TAM | "$53.7B" | "~$50B" / "$50-60B" |
| 預估良率 | "yield 78.3%" | "~80%" / "yield 7-8 成" |
| 機率 | "60% 機率" / "p=0.6" | 詞彙級「很可能」 |
| Multiple | "5.3x EPS" | "~5x" / "4-6x" |

**例外（保留精準）**：T1 source 直接公告（10-K "Q4 revenue $63.2B"）；過去歷史已實現數字；行業標準規格（"HBM3E 8-Hi stack"、"3nm node"）。判斷原則：這個精準數字是 source 公告的、還是分析師估算的？估的就改 range。

**唯一例外（v4.0 新增，已登記 `knowledge/rule_ledger.md`）**：mechanics 3.1 需求三情境表與 3.4 三視野表允許 **5 點步進的主觀權重**（如 55／25／20），須標明「主觀」且加總 100。不得外推到其他判斷層章節或散文機率。

## 【詞彙級機率】

| 詞彙 | 對應機率區間 |
|---|---|
| 幾乎確定／near-certain | > 90%（限現場已發生 + 1 步衍生） |
| 很可能／likely | > 60% |
| 可能／possible | 30–60% |
| 不太可能／unlikely | < 30% |
| 幾乎不可能／near-impossible | < 10% |

禁止寫精準百分比（"60% 機率"），這是 spurious specificity 的高階版。

## 【Claim Taxonomy（4-class，只用於折疊層／data-attribute，不進正文）】

判斷層事實在 `evidence-fold` 或機器可讀屬性中揭露 claim 性質，正文一律白話、不帶標記：

```
🟢 [F: T1: ...]                                  事實 — 有可驗證 source（T1/T2 + 日期）
🟡 [I: A→B]                                      推論 — 寫明事實鏈與結論連結
🔵 [X: base 很可能 / bull 可能 / bear 不太可能]   情境預測 — 三情境並列，詞彙級機率
⚪ [A: ...]                                      假設 — 顯式承認的 prior
```

意見類（[O:]）刻意不設：任何 opinion 必須改寫為 `[I: A→B]` 揭露推論鏈，否則就是 `[A:]`（顯式假設）。

## 【Freshness（鮮度）半衰期】

- **事件型**（引用具體 yield／訂單／簽約／backlog／earnings 數字）→ **14 天強制 refresh**。
- **結構型**（物理定律／產業邏輯／歷史類比／TAM 結構）→ **60 天 refresh**。
- 混合型 → 兩種都跑，以較嚴格者為準。

章節桶（`sections_refreshed` key，INDEX.md 鮮度欄用）：

| 桶 | 對應章節 | 半衰期 | 超過則標示 |
|:---|:---|:---|:---|
| `technical` | 定義／歷史／技術成熟度（appendix、mechanics 3.3） | **365 天** | 🟡 stale-tech |
| `market` | 供給／需求／裁決（mechanics） | **90 天** | 🟠 stale-market |
| `judgment` | 估值／分歧／證偽／個股（valuation、debates、risks、stocks） | **60 天** | 🔴 stale-judgment |

## 【玩家矩陣禁 Q×4 推估】

玩家矩陣不得用「單季數字 × 4」推估全年。最新季已公告 → 四季加總；僅一季 → 註明「年化推估，actual 待 FY 公告」。

## 【利潤池／議價權 % 必 source 或降定性】

利潤池、議價權的所有百分比必標 source；無 source → 改定性（「主導／均勢／次要」），不留精準無源數字。
