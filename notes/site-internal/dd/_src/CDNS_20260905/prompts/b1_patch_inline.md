你是 stock-analyst v17 判斷 agent，回來做**一輪定點修補**。標的 CDNS（20260905）。判斷物已由跨模型閘（gate）冷讀過，下面是它點名的判斷級發現。你的任務只有一件：**針對被點名的欄位做最小修正**，不重寫判斷。

## 讀（判斷物全文附於本訊息之後，不要 Read 任何檔）

判斷物（judgment.json）全文接在本訊息最後（「===== BUNDLE =====」分隔行之後）。

不要重讀 bundle、evidence.json、gate_audit.md、`docs/dd/` 任何檔，也不要回讀你等一下寫出的新版 judgment。你需要的稽核意見全文已附在下方，判斷物全文已附在最後。

## 閘的發現（gate findings）

### 發現 1：3 其他結構變數 🔴
- **依據**：geo_supply_chain#3（中國 FY2025 $679.97M、稱占總營收 5.31%）與判斷全篇沿用的中國 12–13% 直接衝突，而該 12–13% 正是唯一事件 EPS −15–18% 敏感度的分母；R1 evidence_refs 收了 geo_supply_chain#0/1/2/4 獨漏 #3，evidence_dismissed[] 為空
- **建議改法**：evidence_dismissed[] 補一條：$679.97M ÷ FY2025 營收約 12.9%，5.31% 係來源分母口徑錯誤故不採；或於 R1 加一句對帳，維持 12–13% 不變
- **指向欄位**：thesis.R[0].evidence_refs／evidence_dismissed[]

**受影響子樹原文**：

`thesis.R[0].evidence_refs`：
```json
[
  "reg_tariff_export#0",
  "reg_tariff_export#3",
  "geo_supply_chain#0",
  "geo_supply_chain#1",
  "geo_supply_chain#2",
  "geo_supply_chain#4",
  "major_events#4"
]
```

**相關 evidence finding 原文**：

`geo_supply_chain#3`：
```json
{
  "claim": "中國區營收於 FY2025 為 $679.97M，占公司總營收 5.31%（同期美洲區占 19.38%、除中日以外亞洲區占 13.17%，皆為對總營收之占比而非互斥地理分組加總 100%）。",
  "source": "Cadence 10-K FY2025 geographic revenue disclosure, as reported via StockTitan SEC filing summary (stocktitan.net/sec-filings/CDNS/10-k-cadence-design-systems-inc-files-annual-report-6bcef311af10.html)",
  "as_of": "2025-12-31",
  "direction": "0",
  "affects": [
    "thesis.R",
    "valuation"
  ],
  "id": "geo_supply_chain#3"
}
```

`geo_supply_chain#0`：
```json
{
  "claim": "Cadence 10-K（FY2025）風險因子揭露：公司對美中地緣政治與經貿不確定性存在重大曝險，包括現行及未來美中貿易法規、關稅與其他貿易限制的未知影響，並特別點名台灣作為科技產業供應鏈核心樞紐的地緣政治風險。",
  "source": "SEC EDGAR: Cadence Design Systems Form 10-K FY2025 (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm)",
  "as_of": "2026-02",
  "direction": "-",
  "affects": [
    "thesis.R",
    "decision_inputs.bear"
  ],
  "id": "geo_supply_chain#0"
}
```

---

### 發現 2：6 量化模組完整性 🔴
- **依據**：(i) endo_ceiling 15.5%＋淨回購約 1%＝16.5% < 共識 FY1→FY3 EPS CAGR 17.0%，reasoning.moat 仍寫「在邊界內 → endo_ceiling_exceeded=false」，sanity 失敗被判為通過；且 formula_note「三年前以 14% 年均成長回推 NOPAT≈$1.37B」不可複算（14% 回推得 $1.51B，對應 ROIIC 14.8%、天花板 13.0%，缺口擴大至 3pp）。(ii) 情境樹 EPS 實質分歧成立（Bull 18.6／Base 15.7／Bear 9.4，非只有終端倍數 36/30/22）。(iii) 對帳全過：25/45/30 加權＝50.79≈ev5y_pct 50.8、Base +60.9% 年化 10.0%＋回購 0.7≈irr_base_pct 10.7、機率加權多空比 3.65≈asym_ratio 3.7
- **建議改法**：formula_note 補實際推法（營收 14% 回推 × 當年約 40% 非 GAAP 利潤率 × 0.8 ＝ $1.37B），並明說 16.5% vs 17.0% 的 0.5pp 缺口；缺口不補則 endo_ceiling_exceeded 改 true 並於 reasoning.moat 處理
- **指向欄位**：moat.roic_durability.endo_ceiling／moat.roic_durability.formula_note

**受影響子樹原文**：

`moat.roic_durability.endo_ceiling`：
```json
15.5
```

`moat.roic_durability.formula_note`：
```json
"ROIIC(3Y)≈ΔNOPAT÷Δ投入資本：FY2026E NOPAT≈$2.23B（營收 $6.30B×非 GAAP 營業利益率 44.25%×(1−20%)），三年前以 14% 年均成長回推 NOPAT≈$1.37B，ΔNOPAT≈$0.86B；Δ投入資本≈三年併購 $4.9B（Hexagon $3.2B、BETA CAE、Artisan、Secure-IC）＋資本支出減折舊≈0 → 17.6%。再投資率＝併購＋資本支出−折舊 ÷ 三年 NOPAT 合計≈$5.6B ≈ 88%。內生天花板＝17.6%×88%≈15.5%；有機部分資本輕（增量利潤率 60%、負營運資金）標準公式失效，以 ROIIC 為上界。共識 FY1→FY3 EPS CAGR 17.0%＝天花板 15.5%＋淨回購約 1%＋倍數 0 → 邊界內"
```

**相關 evidence finding 原文**：

（未定位到對應 evidence finding）


## 修補紀律

1. **只准改被點名的欄位**——findings 的「指向欄位」是你的動刀範圍。沒被點名的欄位一字不動，包含 `decision_out`（由 `dd_decision.py` 回填，你不要手改）與未涉及的 `reasoning` 段。
2. **裁決方向不由你主動翻**——修正欄位後若 `judge check` 重算出的 `decision_out.verdict` 自己翻面，那是機械層的結果，照實接受並在回報點名；但你不得為了配合閘的語氣直接改寫裁決字串。
3. **可以不採納**——閘的意見不是命令。判斷你認為原判正確時，該條不改欄位，改為在頂層 `evidence_dismissed[]` 補一條 `{"ref": "<閘點名的 finding ref 或欄位路徑>", "reason": "<不採納的具體理由>"}`。理由要指得出證據或推導本身的問題（口徑不可比、來源不可回溯、已被更新一季數字取代、閘誤讀了哪個欄位…），不得寫「影響不大」這類無內容句。**每一條 🔴 都必須有處置**：要嘛改欄位，要嘛進 `evidence_dismissed[]`，不得沉默略過。
4. **🟡 選擇性處理**——能一句話補上就補（通常是 `contradictions[]`／`triggers[]` 加一條或補 `formula_note`），代價過大就依第 3 條寫不採納理由。
5. **不得編造數字**——證據包未涵蓋的數字不准補；該欄位標「證據包未涵蓋」並在回報請 orchestrator 判斷是否回 Stage 0 補軸。
6. 禁 WebSearch／WebFetch。

## 寫（一次 Write 整檔）

改完後把**完整的 judgment.json**一次 `Write` 回 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260905/judgment.json`（不要分次 Edit、不要只寫片段），接著跑：

```
python3 scripts/ddreport.py judge check CDNS 20260905
```

這支會依序重跑 `dd_scenario.py`、`dd_decision.py run`、`validate_judgment.py --evidence --fix --report`，一次把結果回給你；你不需要也不得自行分別呼叫這三支腳本。

FAIL → **只准改 FAIL 訊息點名的欄位**，重跑同一條 `judge check`，**≤1 輪**。一輪後仍 FAIL 就照實回報，交給 orchestrator 處置，不得為湊過驗證而改動判斷實質。

**輪次上限 `6` 輪。** 逼近上限時停下並照實回報。

## 回報（≤200 字）

① 逐條列閘的發現與你的處置（改了哪個欄位／或進 `evidence_dismissed[]` 及理由摘要）
② `judge check` 最後一次的 `validate_judgment.py --report` 原文
③ `decision_out.verdict`／`role`／`row_hit`，以及是否與修補前不同（翻面要明講）


===== BUNDLE =====

{
  "meta": {
    "ticker": "CDNS",
    "date": "2026-09-05",
    "schema": "v15.2",
    "company_name": "Cadence Design Systems"
  },
  "oneliner": "EDA 雙寡占的 AI 放大器：Q2 營收 +24.2%、非 GAAP 營業利益率 45.5%、積壓 $8.1B 創高、全年上修至 +19%；股價自高點 −30% 跌回前份等待的回測帶，FY2027 本益比 30.7x／PEG 1.8 落合理帶；進場·核心，首階三分之一，加碼掛 $260 或 token 營收揭露；清倉級＝對華 EDA 許可制恢復",
  "archetype": {
    "primary": "品質複利成長",
    "secondary": null,
    "confidence": "高",
    "fingerprint": "毛利 85.9%、非 GAAP 營業利益率 45.5%、FCF 利潤率 28.6%（TTM）、研發強度 33%、經常性營收 78%、資本支出佔營收約 3%——典型資本輕、高留存、寡占定價的軟體複利體"
  },
  "thesis": {
    "headline": "AI 晶片設計活動量爆發把 EDA 的收費基底從人頭改成活動量，Cadence 在 IP／硬體驗證／系統模擬三條線同時取份額；市場卻把它當「被 AI 顛覆的軟體股」定價",
    "holding_period": {
      "horizon": "長期 5-10 年",
      "driver": "護城河趨勢與 ROIC 方向為主：多年 ELA、代工廠簽核鎖定、agentic 收費模式兌現；財報單季波動是噪音",
      "signal_vs_noise": "訊號＝積壓年增、Core EDA 有機成長、系統廠客戶佔比、中國營收佔比與許可狀態；噪音＝單季硬體出貨時點、單季 FCF 起伏、軟體股板塊輪動"
    },
    "H": [
      {
        "id": "H1",
        "text": "EDA 雙寡占結構穩定，Cadence 在 IP／硬體／系統三線持續取份額，總營收年增維持雙位數中段以上",
        "2y": "FY2027 營收年增 ≥13%（共識 EPS 9.54 隱含）；積壓每季年增為正；Core EDA 有機成長 ≥12%",
        "5y": "FY2031 營收約 $11-12B（5 年 CAGR 約 13%）；EDA 市佔維持 ≥30%（2024 年約 30%）",
        "10y": "2036 年 EDA＋IP＋系統仍為三寡占，Cadence 份額不低於今日；系統廠客戶佔比 >50%",
        "threshold": "積壓 TTM 年增 <0 連 2 季＝削弱；Core EDA 有機成長 TTM <8% 連 3 季＝反轉",
        "source": "季度新聞稿（積壓／12 個月 RPO）、法說分段成長率；SemiAnalysis EDA 份額",
        "drift_rule": "2Y 假設連 2 季 TTM 偏離 ≥5% 削弱、連 3 季 ≥10% 反轉；5Y 假設連 4 季 ≥5% 削弱"
      },
      {
        "id": "H2",
        "text": "agentic AI（ChipStack／AgentStack）以「基礎訂閱＋token 用量」計費，把成長天花板從客戶工程師人數解綁，AI 是放大而非顛覆",
        "2y": "FY2027 法說首次揭露 token／消費型營收或 AI 工具 ARR 佔比；客戶合約年期無縮短（管理層 2026-02 稱未見變化，來源：摘要）",
        "5y": "FY2031 AI 工具／消費型營收佔比 ≥20%；Core EDA 成長不因客戶人力減 30% 而降至個位數",
        "10y": "EDA 營收與 AI 晶片流片量掛鉤而非人頭；每顆先進晶片 EDA＋IP 投資持續上升",
        "threshold": "FY2028 仍無任何 token／消費型營收揭露＝削弱；Core EDA 成長連 4 季 <8% 且客戶引述 AI 減席＝反轉",
        "source": "法說與投資人會議管理層揭露；10-K 經常性／一次性營收拆分",
        "drift_rule": "5Y 假設連 4 季 ≥5% 削弱、連 6 季 ≥10% 反轉"
      },
      {
        "id": "H3",
        "text": "增量利潤率 60% 的營運槓桿把非 GAAP 營業利益率自 44-45% 推向 48-50%，Rule of 60 常態化",
        "2y": "FY2027 非 GAAP 營業利益率 ≥46%（Hexagon 轉為增益後）；FY2026 落在 43.75-44.75% 指引內",
        "5y": "FY2031 非 GAAP 營業利益率 ≥48%；SBC 佔營收 ≤9%",
        "10y": "營業利益率 50% 上下、FCF 利潤率 ≥35%",
        "threshold": "非 GAAP 營業利益率 TTM 年減 >100bp 連 2 季＝削弱；增量利潤率 <40% 連 2 年＝反轉",
        "source": "季度新聞稿非 GAAP 營業利益率；法說增量利潤率揭露",
        "drift_rule": "2Y 假設連 2 季 TTM 偏離 ≥5% 削弱、連 3 季 ≥10% 反轉"
      }
    ],
    "R": [
      {
        "id": "R1",
        "text": "中國營收 12-13% 曝險於美國出口管制：2025-05 至 07 曾被要求許可六週、2025-07 認罪付 $140M、BIS 50% 規則暫停至 2026-11-09 到期；管理層財測明寫「假設管制維持現狀」",
        "h_ref": "H1",
        "clock": "🔥",
        "threshold": "中國營收佔比 TTM 連 4 季 <9%，或任一季因許可／管制致營收遞延 → 減碼；許可制正式恢復＝清倉級（見唯一事件）",
        "evidence_refs": [
          "reg_tariff_export#0",
          "reg_tariff_export#3",
          "geo_supply_chain#0",
          "geo_supply_chain#1",
          "geo_supply_chain#2",
          "geo_supply_chain#4",
          "major_events#4"
        ]
      },
      {
        "id": "R2",
        "text": "AI 資本支出增速 2027 年降檔：EDA 流片量與續約漲幅落後資本支出 6-12 個月，2026 為三年續約週期的低年、積壓創高靠新客；若 2027 超大規模業者資本支出年增跌破 +20%，token 收入與續約漲幅都要重談",
        "h_ref": "H2",
        "clock": "🔥",
        "threshold": "任一 Big-4 超大規模業者 2027 AI 資本支出指引年增 <+20%，且 Cadence 積壓年增連 2 季轉負 → 減碼；連 4 季 → 大動作",
        "evidence_refs": [
          "supply_demand_durability#3"
        ]
      },
      {
        "id": "R3",
        "text": "客戶集中與信用：約 60 家公司貢獻 70% 營收、系統廠 45%；最大單一帳戶 Intel 信評降至 BBB（距非投資級兩級）、Samsung 代工部門虧損延至 2028；無單一客戶 ≥10%，但前段客戶專案延遲直接打單季",
        "h_ref": "H1",
        "clock": "🐢",
        "threshold": "應收帳款任一客戶 ≥10%（10-Q）或前十大客戶任一破產／重組致營收遞延 >$100M → 減碼；系統廠佔比反轉下降連 2 年 → 重評 H1",
        "evidence_refs": [
          "customer_second_source#2",
          "customer_concentration_credit#1",
          "customer_concentration_credit#2",
          "customer_concentration_credit#3"
        ]
      }
    ],
    "single_thing": {
      "description": "美國商務部 BIS 正式恢復對中國（或中國軍事最終用戶）EDA 軟體與技術的出口許可要求（2025-05-23 那類通知），且未在 90 天內撤銷",
      "why_fatal": "中國佔營收 12-13%、增量利潤率 60% 意味遞減利潤率同樣陡：損失約 $750M 營收對應約 $450M 營業利益（約 16%），FY EPS 下修 15-18%；同時市場把政策風險折價疊上 AI 顛覆折價，倍數與盈餘雙殺",
      "if_happens": "首階倉位清倉，不等財報；重啟條件＝許可撤銷或中國佔比降至 <5% 且積壓仍年增",
      "how_monitor": "BIS 公告（bis.gov）、公司 8-K、每季法說中國佔比；2026-11-09 BIS 50% 規則暫停到期為第一個觀察日",
      "probability": "12-24 個月約 15%（2025 年曾發生一次且六週撤銷；美中談判中 10-K 明列可能重施）"
    }
  },
  "industry": {
    "clock_phase": "II",
    "sd_verdict_source": "產業物理供需＝shortage（ID：AI EDA + IP，as-of 2026-04-27，Phase II、信心 high、priced_in 未填）。Phase II 經自身位置閘交叉驗證：積壓 $8.1B 創高、硬體交期 8-22 週中段、2027 設備銷售預期創高但 AI 資本支出增速減速——屬擴張中段偏後而非過熱，載入 II；priced_in 由本檔自判：股價 −30% 後已由「大多反映」退回「部分反映」",
    "bargaining": {
      "up": "上游＝雲端算力與 FPGA／ASIC 供應（Palladium 自研晶片）、模型供應商（NVIDIA Nemotron 合作）；無 top3 >70% 的集中供應揭露，議價權在 Cadence；硬體交期 8-22 週顯示供給端非瓶頸",
      "down": "下游＝約 60 家公司佔 70% 營收，多年 ELA、換工具＝重跑驗證；無單一客戶 ≥10%；系統廠 45%（兩年前 40%）自研晶片反而擴大用量；但 AVGO 與超大規模業者內製設計能力壓 IP 議價；管理層對定價權提問以「交付價值」帶過（來源：摘要）",
      "geo": "中國 12-13% 營收受出口管制、台灣為供應鏈樞紐風險（10-K）；2025 六週許可事件已實證政策可瞬間切斷；Section 232 半導體關稅不含 EDA 軟體"
    },
    "profit_pool_dir": "利潤往 EDA 雙寡占＋ARM IP 集中且皆 ↑（ID 供給側）；新分支＝EDA AI 平台層（per-tapeout／token 重定價）與 IP 子系統化；Cadence 環節 5 年池佔比淨流入（IP 三年高成長、系統業務年增約 25%）→ 非淨流出，Runway 不降檔",
    "tam_table": [
      {
        "segment": "Core EDA（Q1 2026 佔 71%，年增 18%）",
        "tam_now": "純 EDA 2026 約 $18.2B",
        "tam_5y": "2033 約 $33.5B（CAGR 9.1%）；另一口徑 2031 $30.7B（CAGR 8.1%）",
        "sam": "先進節點數位／類比／驗證全流程；代工廠簽核工具",
        "penetration": "Cadence 全球 EDA 份額約 30%（Synopsys 31%、Siemens 13%）",
        "cagr": "市場 8-9% vs Cadence Core EDA 18%",
        "position": "工具層（利潤最厚），簽核鎖喉點由 Siemens Calibre 持有",
        "pool_shift": "從人頭授權流向活動量計費；三寡占集體毛利高檔",
        "ceiling": "天花板＝設計活動量與 AI 資本支出；被替代路徑＝AI-native 設計流程繞過既有工具（目前三大廠自己在做 agent，無新進入者）"
      },
      {
        "segment": "半導體 IP（佔 14%，Q1 年增 22%、Q2 年增逾 40%）",
        "tam_now": "證據包未涵蓋（ID 稱 ARM CSS 權利金率約 10%）",
        "tam_5y": "證據包未涵蓋",
        "sam": "先進節點五大 star IP（UCIe／HBM／DDR／PCIe／SerDes）",
        "penetration": "與一家全球代工大廠簽 IP 史上最大單一合約（2 奈米）；Synopsys 承認 FY26 IP 清淡年",
        "cagr": "連續第三年高成長",
        "position": "從「賣藍圖」升級到「賣子系統」的中游",
        "pool_shift": "自 Synopsys／ARM 流向 Cadence（客戶不想被綁死，來源：摘要）",
        "ceiling": "天花板＝大客戶內製 IP；被替代路徑＝ARM CSS 子系統化與 AVGO 內製"
      },
      {
        "segment": "System Design & Analysis（佔 15%，Q2 年增 37%；含 Hexagon D&E）",
        "tam_now": "SD&A 2026 年化跨 $1B（含 Hexagon 約 $160M）",
        "tam_5y": "管理層稱矽與系統整合可讓 TAM 隨時間翻倍（來源：摘要）",
        "sam": "3D-IC、多物理模擬、physical AI（機器人／車用）模擬",
        "penetration": "Synopsys 併 Ansys 後在 multiphysics 全棧領先 18-24 月（ID）",
        "cagr": "系統業務過去 5-6 年年增約 25%（來源：摘要）",
        "position": "系統層新環節，Cadence 為追趕者",
        "pool_shift": "從 Ansys／Siemens 分食；Hexagon 補機器人模擬",
        "ceiling": "天花板＝physical AI 採用時點「很難說」（CEO，來源：摘要）；被替代路徑＝Synopsys-Ansys 綁定 device-to-system"
      }
    ]
  },
  "moat": {
    "execution": 9,
    "pricing": 8,
    "combined": 8.5,
    "grade": "A",
    "score": 8.5,
    "trend": "↑",
    "trend_evidence": "執行面擴大：IP 年增逾 40%（Q2 2026）對照 Synopsys 自認 FY26 IP 清淡年；硬體 30 家以上新客、前十大硬體客戶 7 家雙產品、Palladium 連續六年紀錄；系統廠客戶 45%（兩年前 40%）；一家超大規模業者以 Cadence 數位全流程完成首顆全 COT AI 晶片流片（2026-04）。定價面穩定：token 計費尚未揭露營收、CEO 對定價權提問以價值帶過（來源：摘要）。皆非縮減、對 thesis 更關鍵的執行維度擴大→↑；前瞻 2-3 年份額：IP／硬體續升、multiphysics 對 Synopsys-Ansys 追趕",
    "spread_table": [
      {
        "metric": "GAAP 營業利益率（TTM）",
        "self": 30.82,
        "peer": "SNPS 9.73／QCOM 23.28／ARM 17.3",
        "spread_pp": 21.09,
        "trend": "Q2 2026 GAAP 28.4% vs Q2 2025 19.0%（+940bp）；SNPS 受 Ansys 攤銷壓低",
        "note": "閘一：對最強直接同業 spread 為正且擴大 → 合併分 ≥8 成立"
      },
      {
        "metric": "毛利率（TTM）",
        "self": 85.87,
        "peer": "SNPS 73.47／ARM 97.54／QCOM 54.23",
        "spread_pp": 12.4,
        "trend": "逐季年減證據包未涵蓋；硬體佔比上升結構性壓毛利但仍 85%+",
        "note": "閘二未觸發（無 >1.5pp 年減證據）"
      },
      {
        "metric": "FCF 利潤率（TTM）",
        "self": 28.64,
        "peer": "SNPS 30.35／ARM 28.55／QCOM 23.64",
        "spread_pp": -1.71,
        "trend": "Q2 2026 單季 36.8%、Q1 20.8%（硬體與 IP 出貨時點）",
        "note": "與 SNPS 同級，非護城河差異來源"
      },
      {
        "metric": "研發強度（TTM）",
        "self": 33.02,
        "peer": "SNPS 32.11／ARM 57.49／QCOM 22.45",
        "spread_pp": 0.91,
        "trend": "與 SNPS 同水位；閘三絕對美元新增對照證據包未涵蓋 SNPS 季度數字",
        "note": "軍備競賽對等，無規模優勢質變警示"
      }
    ],
    "threats": [
      {
        "level": "⛔ 架構替代",
        "text": "AI-native 設計流程繞過既有 EDA 工具、或客戶以 agent 減人力後總支出持平——市場 2026-08 已用軟體股拋售定價此疑慮；Siemens Fuse EDA AI Agent 宣稱設計週期減半。目前三大既有廠都在做 agent、無新進入者，CEO 稱基礎工具是 V6/V8 引擎；扣分反映在定價 8 而非 9，不在趨勢重複記帳",
        "p": "15-20%（5 年內 Core EDA 成長因 AI 減席降至個位數）",
        "evidence_refs": [
          "substitute_technology#0",
          "substitute_technology#2",
          "competitive_share_entrants#3"
        ]
      },
      {
        "level": "🔴 生態攻擊",
        "text": "Synopsys 併 Ansys 後推 device-to-system 全棧（multiphysics 領先 18-24 月）；NVIDIA 與 Synopsys 非獨家合作；Cadence 以 Hexagon（$3.2B）追趕 physical AI",
        "p": "30%（SD&A 份額被 Synopsys-Ansys 壓制）",
        "evidence_refs": [
          "regulatory_antitrust#0",
          "major_events#0"
        ]
      },
      {
        "level": "🟡 點對點",
        "text": "超大規模業者自研晶片團隊擴大 COT，目前是擴大採用 Cadence 而非自建工具；中國本土 EDA 業者在成熟節點競爭",
        "p": "10%（5 年內任一 Big-4 自建 EDA 取代 Cadence 全流程）",
        "evidence_refs": [
          "customer_second_source#0",
          "customer_second_source#1"
        ]
      }
    ],
    "competitors": [
      {
        "name": "Synopsys（SNPS）",
        "rev_growth": "證據包未涵蓋（FY26 IP 自認清淡年）",
        "gm": 73.47,
        "om": 9.73,
        "rd_intensity": 32.11,
        "fcf_margin": 30.35,
        "net_cash": "證據包未涵蓋（Ansys 交易 $35B 後負債上升）",
        "strategy_note": "龍頭 31% 份額，併 Ansys 開 multiphysics 全棧；續約靠 token 漲價約 20%（ID）；IP 作風轉交易型（CFO 觀察，來源：摘要）。GAAP 營業利益率被攤銷壓到 9.7%，FCF 與 Cadence 同級——經濟體質相當、資產負債表較重"
      },
      {
        "name": "Siemens EDA（私有）",
        "rev_growth": "證據包未涵蓋",
        "gm": "證據包未涵蓋",
        "om": "證據包未涵蓋",
        "rd_intensity": "證據包未涵蓋",
        "fcf_margin": "證據包未涵蓋",
        "net_cash": "母公司 Siemens",
        "strategy_note": "約 13% 份額，Calibre 簽核 85%+ 為代工廠強制鎖喉點（結構性 tenure，非成長主軸）；2026 推 Fuse EDA AI Agent 主打設計週期減半"
      },
      {
        "name": "ARM（IP 對手）",
        "rev_growth": "證據包未涵蓋",
        "gm": 97.54,
        "om": 17.3,
        "rd_intensity": 57.49,
        "fcf_margin": 28.55,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "CSS 子系統化把 IP 從藍圖升級（權利金率約 10%）；Cadence 買下其 Artisan foundation IP，兩者在 star IP 上互補多於對撞"
      }
    ],
    "roic_durability": {
      "quadrant": "高利益率 × 高周轉（非 GAAP NOPAT 利潤率約 36%、資本支出僅營收 3%、年度預收使營運資金為負）；GAAP 投入資本因併購商譽偏重，周轉率被拉低但仍屬資本輕",
      "checkpoints": [
        {
          "item": "需求基礎值",
          "light": "🟢",
          "evidence": "需要型：先進晶片不經簽核不能流片、代工廠強制工具；TSMC 稱五年電晶體數成長 48-50 倍（來源：摘要）；設計需求與工程師供給落差是結構性"
        },
        {
          "item": "決策層級",
          "light": "🟢",
          "evidence": "多年 ELA、換工具＝重跑整套驗證；FY26 營收 67% 來自期初積壓；合約年期未縮短（CEO 2026-02，來源：摘要）；經常性營收 78%"
        },
        {
          "item": "價值鏈分配",
          "light": "🟡",
          "evidence": "EDA＋IP 對超大規模業者是 COGS，AVGO 等 ASIC 大戶內製設計壓 IP 議價（ID）；但每顆先進晶片 EDA＋IP 投資自 $50-200M 升至 $200-400M，總量在漲"
        },
        {
          "item": "社會容忍度",
          "light": "🟡",
          "evidence": "產品必要性高但政治敏感：美國出口管制可在數週內切斷 12-13% 營收（2025-05 至 07 實證）；DOJ 認罪三年緩刑期強化合規稽核；法源＝EAR ECCN 3D991/3E991"
        }
      ],
      "roiic": 17.6,
      "reinvest_rate": 88,
      "endo_ceiling": 15.5,
      "formula_note": "ROIIC(3Y)≈ΔNOPAT÷Δ投入資本：FY2026E NOPAT≈$2.23B（營收 $6.30B×非 GAAP 營業利益率 44.25%×(1−20%)），三年前以 14% 年均成長回推 NOPAT≈$1.37B，ΔNOPAT≈$0.86B；Δ投入資本≈三年併購 $4.9B（Hexagon $3.2B、BETA CAE、Artisan、Secure-IC）＋資本支出減折舊≈0 → 17.6%。再投資率＝併購＋資本支出−折舊 ÷ 三年 NOPAT 合計≈$5.6B ≈ 88%。內生天花板＝17.6%×88%≈15.5%；有機部分資本輕（增量利潤率 60%、負營運資金）標準公式失效，以 ROIIC 為上界。共識 FY1→FY3 EPS CAGR 17.0%＝天花板 15.5%＋淨回購約 1%＋倍數 0 → 邊界內"
    }
  },
  "growth": {
    "runway_years": 12,
    "runway_post_y5": "🟢",
    "seven_questions": [
      "①結構性或週期反彈：結構性為主——EDA 市場 CAGR 8-9%、設計複雜度與 AI 晶片流片量上升；但疊了一層 AI 資本支出週期（2027 為考驗年）",
      "②資本投入多少：有機幾乎不需資本（資本支出佔營收約 3%、增量利潤率 60%）；無機部分重——三年併購約 $4.9B，Hexagon $3.2B 換 $160M 營收",
      "③增量 ROIC 是否 >資金成本：有機遠高於；併購含 Hexagon 的 ROIIC 約 17.6% 仍高於資金成本，但 Hexagon 單案首年遠低於",
      "④成長變現金流或被吃掉：FCF 利潤率 28.6%（TTM）、50% FCF 回購——成長變股東現金，但 2026 併購現金流出 $3.2B 吃掉一年多 FCF",
      "⑤競爭者會否被吸引：三寡占＋簽核鎖喉，新進入者查無；吸引的是既有對手的 AI 軍備競賽與 Synopsys-Ansys 全棧",
      "⑥股價反映多少期待：FY2027 本益比 30.7x、PEG 1.8、四年分位約 33%——反映「雙位數中段成長」但不再反映「AI 放大器」；短窗前瞻本益比 47x→36x 已消化一輪",
      "⑦成長率下修估值撐得住嗎：熄火至 10% 對應本益比 22-24x，自現價再跌 30-40%——撐不住，這是最弱的一題，與陷阱定性「觀察倍數下移」一致"
    ],
    "segments": [
      {
        "name": "Core EDA（71%）",
        "fy0": "FY2025 約 $3.75B（以 FY26 指引中值 $6.30B×71% 回推 FY26≈$4.47B，FY25 以年增 18% 回推）",
        "driver": "量：授權席次×活動量（token）×硬體台數；價：續約漲幅（同業 token 漲價約 20%，本標的未揭露）",
        "fy1e": "FY2026 約 $4.47B（+18%）",
        "fy2e": "FY2027 約 $5.10B（+14%）",
        "fy3e": "FY2028 約 $5.75B（+13%）",
        "om_path": "分段營業利益率證據包未涵蓋；合併非 GAAP 44.25%→46%→47%",
        "eps_contrib_pct": "約 70%"
      },
      {
        "name": "半導體 IP（14%）",
        "fy0": "FY2025 約 $0.72B",
        "driver": "量：先進節點 design win 數（2 奈米代工大單）；價：star IP 溢價",
        "fy1e": "FY2026 約 $0.95B（+30%）",
        "fy2e": "FY2027 約 $1.15B（+20%）",
        "fy3e": "FY2028 約 $1.35B（+17%）",
        "om_path": "CEO 稱比產業 IP 更賺錢（來源：摘要），分段數字證據包未涵蓋",
        "eps_contrib_pct": "約 15%"
      },
      {
        "name": "SD&A（15%，含 Hexagon）",
        "fy0": "FY2025 約 $0.80B",
        "driver": "量：3D-IC／多物理模擬席次＋Hexagon $160M 併入；價：轉年度訂閱短期壓成長",
        "fy1e": "FY2026 約 $1.05B（+31%，其中無機約 $160M）",
        "fy2e": "FY2027 約 $1.22B（+16%）",
        "fy3e": "FY2028 約 $1.40B（+15%）",
        "om_path": "Hexagon 2026 稀釋 EPS $0.28、2027 轉增益",
        "eps_contrib_pct": "約 15%"
      }
    ],
    "decay_signals": [
      "護城河侵蝕｜毛利率連 2 季年減：未亮（TTM 85.9%，逐季證據包未涵蓋）",
      "護城河侵蝕｜核心市佔縮減：未亮（IP／硬體／系統皆取份額）",
      "護城河侵蝕｜提價後銷量下滑：未亮（無定價事件揭露）",
      "盈餘品質｜EPS CAGR 顯著高於營收 CAGR：未亮（EPS 17% vs 營收約 13-15%，差距 <5pp）",
      "盈餘品質｜FCF/NI <0.75 連 2 年：未亮（TTM FCF 利潤率 28.6% vs GAAP 營業利益率 30.8%，轉換率高）",
      "盈餘品質｜SBC/營收 >5% 且逐年上升：未亮（9.3%，較 Q1 9.4% 持平微降；絕對水位高列觀察）",
      "產業結構衰退｜TAM 萎縮或被替代：未亮（TAM CAGR 8-9%；AI 替代屬威脅未實現）",
      "產業結構衰退｜產業倍數近 3 年系統性下移：亮——trailing 本益比 2024 年 78.9x→現 60.6x，2026 軟體股整體重定價",
      "隱性資本密集｜維護資本支出佔 FCF >60%：未亮（資本支出僅營收約 3%）",
      "隱性資本密集｜停止投資新產能致收入下滑：未亮（Z4 硬體 2030 前，來源：摘要）"
    ],
    "trap_rating": "🟡（1 燈：倍數下移）；長期成長性綜合 🟢 高確信——跑道 ≥10 年、有機為主（無機約 2pp）、強化型、ROIC 高檔、信號 1"
  },
  "quality": {
    "three_year": [
      {
        "metric": "FCF 利潤率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "TTM 28.64（Q2 2026 單季 36.8、Q1 20.8）",
        "peer_median": "SNPS 30.35／ARM 28.55／QCOM 23.64",
        "assessment": "同級；季度起伏來自硬體與 IP 一次性出貨"
      },
      {
        "metric": "非 GAAP 營業利益率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "FY2025 約 44.5%（CEO 2025-12，來源：摘要）；Q2 2026 45.5%；FY2026 指引 43.75-44.75%",
        "peer_median": "證據包未涵蓋",
        "assessment": "逐年擴張、增量 60%；2026 因 Hexagon 略低於 2025"
      },
      {
        "metric": "GAAP 營業利益率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "TTM 30.82；Q2 2026 28.4（年增 940bp）",
        "peer_median": "SNPS 9.73／QCOM 23.28",
        "assessment": "遠優於 Synopsys；GAAP 與非 GAAP 差 17pp＝SBC＋攤銷"
      },
      {
        "metric": "SBC 佔營收",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "Q2 2026 9.3%（$146.9M）；佔 GAAP 營業利益 32.7%",
        "peer_median": "證據包未涵蓋",
        "assessment": "高位持平；回購覆蓋稀釋"
      },
      {
        "metric": "ROIC−WACC",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "投入資本數字證據包未涵蓋；以 FCF 利潤率 28.6%、資本支出 3% 代理，現金報酬遠高於資金成本",
        "peer_median": "證據包未涵蓋",
        "assessment": "資本輕高報酬"
      }
    ],
    "dupont": [
      {
        "component": "NOPAT 利潤率",
        "value": "GAAP 30.8%×(1−20%)≈24.7%；非 GAAP 45.5%×0.8≈36.4%",
        "note": "兩口徑差 12pp 為 SBC 與併購攤銷"
      },
      {
        "component": "投入資本周轉率",
        "value": "證據包未涵蓋（投入資本數字不在證據包）",
        "note": "年度預收→負營運資金、資本支出 3%，周轉率結構上高；併購商譽是唯一重資產"
      },
      {
        "component": "ROIC",
        "value": "證據包未涵蓋",
        "note": "象限判讀：高利益率×高周轉"
      }
    ],
    "ccc": [
      {
        "metric": "DSO／DIO／DPO／CCC 三年逐年",
        "value": "證據包未涵蓋",
        "note": "經常性營收 78% 隨時間認列、硬體與 IP 一次性 22% 在出貨時點認列；應收帳款集中度 2024 年末一客戶 11%→2025 Q3 無 ≥10%"
      }
    ],
    "buyback": {
      "authorization": "政策＝每年約 50% 以上 FCF 回購；2025 全年 $925M；Q1 2026 $200M、Q3 2025 $200M（來源：摘要）",
      "q1_capital_return": "Q1 2026 $200M；Q2 2026 金額證據包未涵蓋",
      "buyback_to_fcf": "約 50%（政策），遠低於 80% 警示線；2026 另有 $3.2B Hexagon（30% 股票／70% 現金）",
      "avg_price_vs_now": "回購均價證據包未涵蓋；2025-2026 股價區間 $250-377，現價 $292.7 落區間中低段",
      "eps_cagr_ex_buyback": "淨回購約 1%／年（回購略高於 SBC 8-9%，CEO 稱確保不稀釋，來源：摘要）；剔除後 EPS CAGR 約 16% vs 共識 17%，差距 <5pp"
    },
    "lumpiness": {
      "five_year_fcf": "證據包未涵蓋逐年值；2026 上半年 OCF $990.7M、資本支出 $101.4M、FCF $889M",
      "min_vs_avg": "證據包未涵蓋",
      "maint_capex": "以總資本支出（營收約 3%，含 Palladium 自研硬體）為維護資本支出上限——方法：軟體公司資本支出幾乎全屬維護",
      "owner_earnings": "上半年 OCF−資本支出≈$889M，年化約 $1.8B（FY26 營收中值 $6.30B 的 28-29%）",
      "verdict": "🟢 正常——單季起伏（Q1 20.8%／Q2 36.8%）來自硬體與 IP 出貨時點與稅款時序，非結構性"
    }
  },
  "governance": {
    "capalloc_grade": "B",
    "scorecard": [
      {
        "item": "M&A 已實現 ROIIC",
        "value": "Hexagon D&E $3.2B（2026-02 交割）換 2026 營收約 $160M、年化約 $200M——20x 營收，首年 EPS 稀釋 $0.28、2027 轉增益；第 3 年 NOPAT 尚不可觀測；BETA CAE（2024）第 3 年貢獻證據包未涵蓋 → 未證，不計過",
        "pass": false
      },
      {
        "item": "回購買入收益率",
        "value": "現價盈餘殖利率 8.14÷292.7＝2.8%；門檻（10 年期公債＋2%，公債殖利率證據包未涵蓋，以 4% 計）≈6% → 未過；2025-2026 回購價區間與現價相近，收益率同樣 <3%",
        "pass": false
      },
      {
        "item": "SBC 淨稀釋率",
        "value": "SBC 8-9% 營收，回購 ≥SBC（CEO：買回比 SBC 多，來源：摘要）→ 年化淨稀釋 ≤0，過",
        "pass": true
      }
    ],
    "capital_returns": [
      {
        "type": "回購",
        "detail": "2025 $925M；每年約 50% FCF；目標不因 SBC 淨稀釋"
      },
      {
        "type": "股息",
        "detail": "無"
      },
      {
        "type": "併購",
        "detail": "2025-08 Arm Artisan foundation IP；2025-11 Secure-IC；2026-02 Hexagon D&E $3.2B（史上最大）；2026-03 EMA（PCB）；管理層稱未來 1-2 年重心在整合、只做小型 tuck-in、不做變革型交易（來源：摘要）"
      },
      {
        "type": "治理事件",
        "detail": "2025-07-28 就 2015-2021 年對 NUDT 非法出口向 DOJ 認罪、合計逾 $140M（DOJ 罰金＋沒收約 $117M、BIS 民事 $95M 部分重疊）、三年緩刑＋年度出口合規稽核——合規失靈紀錄，非財報重編亦非 SEC 會計調查；無近 12 個月證券集體訴訟"
      }
    ],
    "sbc": {
      "pct_revenue": 9.3,
      "pct_gaap_oi": 32.7,
      "trend": "Q1 2026 9.4% → Q2 9.3%；CEO 定義真實利潤率＝營業利益率減 SBC（來源：摘要）",
      "note": "股東結構（雙重股權／創辦人持股／機構集中度）、管理層薪酬結構、近 12 個月內部人交易：證據包未涵蓋（數據限制）"
    }
  },
  "valuation": {
    "tier": "EDA 寡占（IP company／設計軟體）；同 tier 尺＝SNPS 唯一 anchor；ARM（IP）與 QCOM 不同層級只作體質對照",
    "peers": [
      {
        "name": "SNPS",
        "fwd_pe": "證據包未涵蓋",
        "note": "唯一同 tier；GAAP 營業利益率被 Ansys 攤銷壓低，倍數對照須用非 GAAP"
      },
      {
        "name": "ARM",
        "fwd_pe": "證據包未涵蓋",
        "note": "IP 純 play，倍數通常高於 EDA，不作 anchor"
      },
      {
        "name": "QCOM",
        "fwd_pe": "證據包未涵蓋",
        "note": "客戶而非同業，體質對照用"
      }
    ],
    "fwd_pe": 35.96,
    "peg": 2.12,
    "percentile_5y": 33,
    "val_light": "🟡",
    "val_light_derivation": "分位：trailing 本益比現值 60.6x 在年度樣本點（n=4，高 78.9／低 51.7）分位 32.8%；P/S 13.8x 分位 26.8%；EV/S 分位 30.3%——三尺取本益比 33%，落 30-70% 合理帶（樣本僅 4 個年度點，非連續五年，信心中）。PEG：EPS CAGR 以前瞻窗 FY2026 8.14→FY2028 11.14＝17.0%；FY2026 本益比 35.96x÷17.0＝2.12（偏貴帶）、FY2027 本益比 30.68x÷17.0＝1.80（合理帶）；距財年結束僅四個月，NTM 混合約 32x÷17≈1.9。取較嚴讀法為偏貴，但盲點一救援三條件同時成立（長期成長 🟢 高確信＋FY2027 PEG 1.80 <2.0＋AI 🟢）→ 救回 🟡；盲點三不適用（90 天共識上修 FY1 +2.4%／FY2 +1.7%，遠低於 +10%）。旁註：本站短窗前瞻本益比 2026-05 47.4x→現 36.0x 為窗內最低（四個月短窗，非五年分位）",
    "targets": {
      "short_1y": {
        "eps": 9.54,
        "pe": 33,
        "price": 314.8,
        "upside_pct": 7.6,
        "basis": "FY2027 共識 EPS×合理 33x（護城河 A、成長 15%、Rule of 60）"
      },
      "mid_2y": {
        "eps": 11.14,
        "pe": 33,
        "price": 367.6,
        "upside_pct": 25.6,
        "basis": "FY2028 共識 EPS×33x"
      },
      "five_y": {
        "eps": 15.7,
        "pe": 30,
        "price": 471.0,
        "upside_pct": 60.9,
        "basis": "Base FY2031 EPS×長期 30x（成長降至 12% 時的合理倍數）"
      },
      "bear_anchor": {
        "eps": 7.33,
        "pe": 24,
        "price": 175.8,
        "downside_pct": -39.9,
        "basis": "Bear EPS＝FY2026 共識 8.14×0.9；Bear 本益比＝成長熄火降至 10% 情境 24x；下行 40% >15% 正常可用，短期 R:R 0.19 屬弱、僅參考"
      },
      "sell_side": "Q2 財報後 BofA $420、KeyBanc $425、Stifel $432；2026-09 初 25 位分析師中位數 $405（區間 $300-470，全距 1.6x 未達 2.5x 離散警戒）、買進佔 84%；Zacks 量化 Hold。現價 $292.7 低於中位數 28%——共識目標價仍高於本檔一年目標 $315，本檔比賣方保守，不靠上修也有空間"
    },
    "upside_short_pct": 7.6,
    "upside_mid_pct": 25.6
  },
  "trap_analysis": {
    "pattern": "最可能模式＝「倍數下移中的成長股」——盈餘持續成長但市場把軟體類估值框架整體下調（AI 顛覆敘事），不是盈餘陷阱",
    "evidence_against": "Q2 營收 +24.2%、非 GAAP 營業利益率 45.5% 優於自身指引高標、積壓 $8.1B 與 12 個月 RPO $4.2B 雙創高、全年指引上修至 +19%、共識 90 天上修為正（FY1 +2.4%）；FCF 利潤率 28.6%——盈餘與現金同向、加速中",
    "evidence_for": "trailing 本益比自 2024 年 78.9x 降至 60.6x、短窗前瞻本益比 47x→36x 而盈餘只升 2%——跌的是倍數；2026 為續約低年、積壓創高靠新客，若 2027 AI 資本支出減速，新客動能不可持續；Hexagon 20x 營收的併購是資本配置疑點",
    "bear_case": "18 個月內 −30% 路徑：2027 超大規模業者資本支出指引年增 <+20% → 流片與續約遞延 → FY2027 EPS 由 9.54 下修至 8.6 → 市場以 22-24x 定價成熟軟體 → $190-205。監測：Big-4 資本支出指引（每季）、Cadence 積壓年增、Core EDA 有機成長",
    "monitor": [
      "積壓與 12 個月 RPO 年增（每季新聞稿）：連 2 季轉負＝陷阱顯影",
      "Core EDA 有機成長 TTM（法說）：<10% 連 2 季＝框架切換確認",
      "中國營收佔比與許可狀態（法說／BIS 公告）",
      "短窗前瞻本益比：<28x 且盈餘未下修＝倍數陷阱而非盈餘陷阱，反向加碼"
    ],
    "verdict": "🟢",
    "label": "非陷阱（倍數觀察）"
  },
  "appendix_a": {
    "signal": "A",
    "moat_score": 8.5,
    "growth_durability": 8,
    "quality_score": 8.3,
    "ai_risk": "🟢",
    "long_term_confidence": "高",
    "val": "🟡",
    "ma": "-",
    "fpe_fy2": 30.68,
    "pct_5y": 33,
    "peg_fy2": 1.8,
    "upside_short_pct": 7.6,
    "upside_mid_pct": 25.6,
    "stress": {
      "pass": 2,
      "total": 2
    },
    "verdict": "A"
  },
  "scenario_ref": "/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260905/scenario.json",
  "eps_meta": {
    "base_eps_path": {
      "FY2027": 9.45,
      "FY2028": 10.9,
      "FY2029": 12.4,
      "FY2030": 14.0,
      "FY2031": 15.7
    },
    "fy_end_month": 12,
    "eps_basis": "non-gaap-usd"
  },
  "catalysts": [
    {
      "date": "2026-10",
      "date_precision": "month",
      "type": "guidance",
      "event": "Q3 2026 財報：非 GAAP EPS 指引 $2.01-2.07、營業利益率 43.5-44.5%；看積壓年增與 Core EDA 有機成長",
      "impact": "中",
      "watch": "積壓 ≥$8.1B、FY26 指引再上修＝H1 強化；ChipStack Level-5 早期存取客戶數"
    },
    {
      "date": "2026-11-09",
      "date_precision": "month",
      "type": "regulatory",
      "event": "BIS 50% 規則暫停到期，恢復或再延；同時是美中談判中 EDA 許可制會否重施的觀察窗",
      "impact": "高",
      "watch": "恢復＋任何 EDA 許可通知＝唯一事件觸發；再延＝R1 降溫"
    },
    {
      "date": "2026-12",
      "date_precision": "quarter",
      "type": "product",
      "event": "ChipStack Level-5 全自主虛擬工程師早期存取（2026 下半年）；token 計費模式首批客戶",
      "impact": "中",
      "watch": "FY2027 法說是否首次揭露 token／消費型營收＝H2 驗證"
    },
    {
      "date": "2027-02",
      "date_precision": "month",
      "type": "guidance",
      "event": "Q4 2026 財報與 FY2027 指引：Hexagon 轉增益、期初積壓覆蓋率、中國佔比預期",
      "impact": "高",
      "watch": "FY2027 營收指引 ≥+13%、非 GAAP 營業利益率 ≥46%；2027 積壓覆蓋率 ≥65%"
    },
    {
      "date": "2027-01",
      "date_precision": "quarter",
      "type": "macro",
      "event": "Big-4 超大規模業者 2027 資本支出指引（Q4 法說季）",
      "impact": "高",
      "watch": "任一年增 <+20%＝R2 發火；EDA 流片量落後 6-12 個月"
    }
  ],
  "decision_inputs": {
    "signal": "A",
    "trap": "🟢",
    "val": "🟡",
    "ma": "-",
    "runway_post_y5": "🟢",
    "moat_trend": "↑",
    "moat": "A",
    "capalloc_grade": "B",
    "archetype": "品質複利成長",
    "cycle_position": null,
    "cycle_verdict": null,
    "asym_ratio": 3.7,
    "irr_base_pct": 10.7,
    "ev5y_pct": 50.8,
    "price_at_dd": 292.7,
    "thesis_irreconcilable": false,
    "valuation_dependent": false,
    "market_wrong_reason_given": true,
    "week26_return_pct": -1.43,
    "momentum_overheated": false,
    "cycle_gates_pass": null,
    "consensus_rev_3m_pct": 2.4,
    "val_denominator_disputed": false,
    "qc49_inherit_prior": false,
    "prior_verdict": null,
    "prior_role": null,
    "held_now": null
  },
  "decision_out": {
    "verdict": "進場",
    "role": "衛星",
    "row_hit": "9b",
    "pacing": [],
    "holding_cap": null,
    "requires_critic": [
      "QC-41：裁決強方向（進場）＋護城河趨勢 ↑＋法規敏感（對華出口管制）＋B2B 集中型——需跨模型複核「AI 放大而非顛覆」是否低估了架構替代軸，以及 ↑ 是否只靠管理層自述",
      "手冊 27：Synopsys 資本量級大於本標的（併 Ansys $35B），↑ 是否應降為 →——請閘核對 IP +40% 與硬體新客 30 家是否足以撐方向性判定"
    ],
    "audit_rows": [
      {
        "row": "1",
        "condition": "基本面評級 signal = X → 迴避",
        "hit": false,
        "basis": "signal='A'"
      },
      {
        "row": "2",
        "condition": "§11 強制裁決：thesis 不可調和不成立 → 迴避",
        "hit": false,
        "basis": "thesis_irreconcilable=False"
      },
      {
        "row": "3",
        "condition": "moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避",
        "hit": false,
        "basis": "moat_trend='↑', moat='A'"
      },
      {
        "row": "4",
        "condition": "週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）",
        "hit": false,
        "basis": "ma='-'"
      },
      {
        "row": "5",
        "condition": "動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）",
        "hit": false,
        "basis": "momentum_overheated=False"
      },
      {
        "row": "6",
        "condition": "基本面評級 signal = C → ≥ 觀望",
        "hit": false,
        "basis": "signal='A'"
      },
      {
        "row": "7",
        "condition": "runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）",
        "hit": false,
        "basis": "runway_post_y5='🟢'"
      },
      {
        "row": "7a",
        "condition": "§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年",
        "hit": false,
        "basis": "valuation_dependent=False, market_wrong_reason_given=True"
      },
      {
        "row": "7b",
        "condition": "dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）",
        "hit": false,
        "basis": "capalloc_grade='B'"
      },
      {
        "row": "8a",
        "condition": "無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）",
        "hit": false,
        "basis": "signal='A', runway='🟢', val='🟡', moat_trend='↑', week26=-1.43, valuation_dependent=False"
      },
      {
        "row": "8b",
        "condition": "無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）",
        "hit": false,
        "basis": "archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='↑', cycle_gates_pass=None"
      },
      {
        "row": "11.4b-denom",
        "condition": "§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）",
        "hit": false,
        "basis": "val_denominator_disputed=False"
      },
      {
        "row": "8",
        "condition": "無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）",
        "hit": false,
        "basis": "signal='A', val='🟡'"
      },
      {
        "row": "9",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅} → 進場",
        "hit": false,
        "basis": "signal='A', val='🟡', ma='-'"
      },
      {
        "row": "9b",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟡,🟠,-}（W250斜率未轉負）→ 進場·條件式（長波段佈局）",
        "hit": true,
        "basis": "signal='A', val='🟡', ma='-'"
      },
      {
        "row": "10",
        "condition": "無 Veto + signal≥A + MA∈{🟢,✅} + val∈{🟢,🟡} → 進場",
        "hit": false,
        "basis": "signal='A', val='🟡', ma='-'"
      },
      {
        "row": "QC-49",
        "condition": "qc49_inherit_prior=False，不套用",
        "hit": false,
        "basis": "qc49_inherit_prior=False"
      }
    ],
    "rearm_trigger": "價 ≤$260（FY2027 本益比 27x）或 token 營收首次揭露 → 加第二個三分之一；BIS 50% 規則落地無 EDA 許可 → 第三段",
    "exec_line": "新資金：首階三分之一現價建倉，餘掛 $260／token 揭露／BIS 落地三段。已持有：不加不減；清倉只認唯一事件（對華 EDA 許可制恢復），估值偏高最多 trim（前瞻本益比 >50x）"
  },
  "triggers": [
    {
      "n": 1,
      "text": "積壓與 Core EDA 有機成長守住（H1）",
      "type": "假設驗證",
      "maps_to": "H1",
      "metric": "積壓 TTM 年增；Core EDA 有機成長 TTM",
      "threshold": "積壓年增 <0 連 2 季＝削弱；Core EDA <8% 連 3 季＝反轉",
      "action": "削弱＝停止加碼；反轉＝減至首階",
      "source_freq": "季度新聞稿／法說，每季",
      "date": "2026-10-31",
      "evidence_refs": [
        "competitive_share_entrants#0",
        "supply_demand_durability#0"
      ]
    },
    {
      "n": 2,
      "text": "token／消費型營收揭露（H2）",
      "type": "假設驗證",
      "maps_to": "H2",
      "metric": "AI 工具 ARR 或 token 營收佔比首次揭露；合約年期",
      "threshold": "FY2028 仍無揭露＝削弱；Core EDA 連 4 季 <8% 且客戶引述 AI 減席＝反轉",
      "action": "揭露＝加第二個三分之一（論點增強）；反轉＝減碼一半",
      "source_freq": "法說／投資人會議，每季",
      "date": "2027-02-28",
      "evidence_refs": [
        "substitute_technology#0",
        "substitute_technology#2"
      ]
    },
    {
      "n": 3,
      "text": "非 GAAP 營業利益率擴張（H3）",
      "type": "假設驗證",
      "maps_to": "H3",
      "metric": "非 GAAP 營業利益率 TTM；增量利潤率",
      "threshold": "TTM 年減 >100bp 連 2 季＝削弱；增量 <40% 連 2 年＝反轉",
      "action": "削弱＝停止加碼；反轉＝重評 H3 與終端倍數",
      "source_freq": "季度新聞稿，每季",
      "date": "2027-02-28"
    },
    {
      "n": 4,
      "text": "中國出口管制與佔比（R1）",
      "type": "風險",
      "maps_to": "R1",
      "metric": "中國營收佔比 TTM；BIS 許可／規則狀態",
      "threshold": "佔比連 4 季 <9% 或任一季因管制遞延營收 → 減碼；許可制正式恢復 → 唯一事件",
      "action": "減碼三分之一；恢復許可制＝清倉",
      "source_freq": "法說每季；BIS 公告事件驅動",
      "date": "2026-11-09",
      "evidence_refs": [
        "reg_tariff_export#0",
        "reg_tariff_export#3",
        "geo_supply_chain#0",
        "geo_supply_chain#1",
        "geo_supply_chain#2",
        "geo_supply_chain#4",
        "major_events#4",
        "sec_investigation_restatement#0"
      ]
    },
    {
      "n": 5,
      "text": "AI 資本支出 2027 降檔（R2）",
      "type": "風險",
      "maps_to": "R2",
      "metric": "Big-4 超大規模業者 2027 AI 資本支出指引年增；Cadence 積壓年增",
      "threshold": "任一 <+20% 且積壓年增連 2 季轉負 → 減碼；連 4 季 → 大動作",
      "action": "減碼三分之一；連 4 季減至首階",
      "source_freq": "超大規模業者法說每季（2027-01 起）",
      "date": "2027-01-31",
      "evidence_refs": [
        "supply_demand_durability#3"
      ]
    },
    {
      "n": 6,
      "text": "客戶集中與信用（R3）",
      "type": "風險",
      "maps_to": "R3",
      "metric": "10-Q 應收帳款集中度；前十大客戶重組事件；系統廠佔比",
      "threshold": "任一客戶應收 ≥10% 或前段客戶重組致遞延 >$100M → 減碼；系統廠佔比連 2 年下降 → 重評 H1",
      "action": "減碼三分之一",
      "source_freq": "10-Q 每季；信評事件驅動",
      "date": "2026-10-31",
      "evidence_refs": [
        "customer_second_source#2",
        "customer_concentration_credit#1",
        "customer_concentration_credit#2",
        "customer_concentration_credit#3"
      ]
    },
    {
      "n": 7,
      "text": "對華 EDA 出口許可制恢復",
      "type": "Single Thing",
      "maps_to": "Single Thing",
      "metric": "BIS 通知／最終規則要求 EDA（ECCN 3D991/3E991）對華出口許可，且 90 天內未撤銷",
      "threshold": "正式通知＝觸發",
      "action": "清倉，不等財報；重啟＝撤銷或中國佔比 <5% 且積壓仍年增",
      "source_freq": "BIS 公告、公司 8-K，事件驅動",
      "date": "2026-11-09",
      "evidence_refs": [
        "geo_supply_chain#1",
        "geo_supply_chain#2"
      ]
    },
    {
      "n": 8,
      "text": "加碼雙軌",
      "type": "加碼",
      "maps_to": "估值／論點增強",
      "metric": "價格 vs FY2027 本益比；token 營收揭露",
      "threshold": "價 ≤$260（27x）或 token 營收首次揭露",
      "action": "加第二個三分之一；兩者皆到不重複加",
      "source_freq": "每週價格；法說每季",
      "date": "2027-02-28"
    },
    {
      "n": 9,
      "text": "估值偏高 trim",
      "type": "減碼",
      "maps_to": "估值",
      "metric": "FY1 前瞻本益比",
      "threshold": ">50x 且共識未同步上修 ≥10%",
      "action": "最多 trim 三分之一，不清倉（核心角色長抱分軌）",
      "source_freq": "每週",
      "date": "2027-09-05"
    },
    {
      "n": 10,
      "text": "thesis 級清倉",
      "type": "清倉",
      "maps_to": "H1/H2",
      "metric": "Core EDA 有機成長 TTM；積壓年增；客戶 AI 減席引述",
      "threshold": "Core EDA <8% 連 3 季且積壓年增連 2 季為負",
      "action": "清倉；重啟須重跑 DD",
      "source_freq": "法說每季",
      "date": "2027-08-31",
      "evidence_refs": [
        "substitute_technology#0"
      ]
    },
    {
      "n": 11,
      "text": "複審",
      "type": "複審日期",
      "maps_to": "全部",
      "metric": "Q4 2026 財報與 FY2027 指引後",
      "threshold": "—",
      "action": "重跑判斷：H1-H3 漂移、Hexagon 增益、中國佔比預期",
      "source_freq": "半年",
      "date": "2027-02-28"
    }
  ],
  "contradictions": [
    {
      "axis": "共識清單與矛盾拓撲",
      "side_a": "方向一致：寡占＋簽核鎖定＋多年 ELA（護城河 A）；營收 +24%、營業利益率 45.5%、積壓創高（成長與品質）；估值自高點回落至合理帶；賣方 84% 買進",
      "side_b": "矛盾拓撲＝集中兩軸：①AI 是放大器還是顛覆者（護城河定價維度與終端倍數）；②中國出口管制（政策軸）。其餘（Hexagon 稀釋、Intel 信評、2027 資本支出）為程度差異",
      "ruling": "爭議集中→點名兩軸；信心不整體下修，但進場改分批、唯一事件鎖政策軸",
      "evidence_level": "L1",
      "settle_metric": "Core EDA 有機成長與 token 營收揭露；BIS 2026-11-09",
      "if_then": [
        "若 FY2027 指引 ≥+13% 且 token 營收揭露 → 完成三段建倉",
        "若 Core EDA <8% 連 3 季 → 減至首階"
      ]
    },
    {
      "axis": "AI 放大 vs AI 顛覆（不可調和）",
      "side_a": "A 側：設計先進晶片需要精確物理與數學簽核，AI agent 是 Cadence 自己在賣（ChipStack／Level-5 與 NVIDIA）；客戶沒有減少使用的討論（CEO 2026-02，來源：摘要）；系統廠 45% 擴大採用而非自建；三大廠都在做 agent、無新進入者",
      "side_b": "B 側：2026-08 軟體股拋售把 CDNS 一併重定價，市場怕 AI 自動化設計流程壓縮 TAM；Siemens Fuse 宣稱設計週期減半；CEO 自己也說每專案人力至少減 30%（來源：摘要）——人頭計費基底在縮；token 計費至今無營收揭露，且管理層對變現時點以「可以有耐心」帶過（來源：摘要）",
      "ruling": "選 A 側但打折：L1 實績（+24%、積壓創高、IP／硬體取份額）勝過 L3 敘事（軟體股拋售）；以 L2 反駁 L1 的理由只有「token 未揭露」——這是時間差不是方向。執行：進場但終端倍數以 30x（非 36x）為 Base、Bear 30% 且 Bear 終端 22x 反映框架切換。現在就賣的最強論證：(1) 人頭減 30% 若 token 補不回，Core EDA 成長掉到個位數；(2) 2027 AI 資本支出減速讓積壓創高只是續約低年的錯覺；(3) 中國許可制隨時可回來——逐點回應：(1) 故以 H2 的 FY2028 揭露期限與 Core EDA <8% 連 3 季當清倉閘，不等 GRR 顯影；(2) 12 個月 RPO $4.2B 覆蓋 FY2027 約 60%，減速最快 2027 下半年才傳導，觸發器 5 已掛；(3) 列為唯一事件，觸發即清倉而非減碼",
      "evidence_level": "L1 vs L3",
      "settle_metric": "FY2027-2028 Core EDA 有機成長與 token 營收佔比",
      "if_then": [
        "若 token 營收於 FY2027 揭露且 Core EDA ≥12% → 加第二段",
        "若 Core EDA <8% 連 3 季且積壓年增連 2 季負 → 清倉"
      ],
      "evidence_refs": [
        "substitute_technology#0",
        "substitute_technology#1",
        "substitute_technology#2",
        "customer_second_source#1",
        "substitute_technology#3"
      ]
    },
    {
      "axis": "AI 資本支出泡沫 vs 積壓創高（可調和）",
      "side_a": "永續性測試 2027 浮現、AI 產業需 $2 兆年營收撐當前投資（市場評論）",
      "side_b": "積壓 $8.1B 在續約低年創高、新增 12 客、系統廠自研 ASIC 讓每顆晶片 EDA＋IP 投資倍增（ID）",
      "ruling": "程度差異：積壓鎖合約量不鎖續約定價權（ID 需求側原話）。採信短期（FY2026-27 底部有合約），不採信「2027 一定持續加速」——Base 把 FY2027 EPS 對共識打 1% 折、Bear 情境 FY2027 只 +6%",
      "evidence_level": "L2 vs L3",
      "settle_metric": "Big-4 2027 資本支出指引",
      "if_then": [
        "若任一 Big-4 2027 指引 <+20% → 停止加碼並看積壓",
        "若四家皆 ≥+20% → R2 降為 🐢"
      ],
      "evidence_refs": [
        "supply_demand_durability#3",
        "supply_demand_durability#0",
        "supply_demand_durability#2"
      ]
    },
    {
      "axis": "ID 對帳：AI EDA + IP（as-of 2026-04-27）",
      "side_a": "ID 機器欄：shortage／Phase II／信心 high／priced_in 未填",
      "side_b": "本檔：Phase II 經交叉驗證載入；shortage 只當事實錨；priced_in 本檔自判由「大多反映」退回「部分反映」（股價 −30%、短窗前瞻本益比 47x→36x）",
      "ruling": "一致，無分歧；ID 已四個月餘、寫於股價高點前，其 priced_in 缺值應於下次 refresh 補填——不阻斷",
      "evidence_level": "L2",
      "settle_metric": "ID refresh 的 priced_in 欄",
      "if_then": [
        "若 ID refresh 改判 balanced → Bear 終端倍數不變、Base 成長降 1pp",
        "若 ID 維持 shortage 且 priced_in 判 low → 可提前完成第二段"
      ]
    },
    {
      "axis": "前份對照：裁決承繼與回測帶",
      "side_a": "前份（2026-05-04，v12.3）：A 核心候選、4 週 +22% 接近警戒、「等回測 BB 中軌約 303」；當時無統一裁決欄（決策層尚未併入）",
      "side_b": "本次：價 $292.7 已落 303 之下（前份等待的位置到了），盈餘共識 FY1 自 7.95 升至 8.14；裁決首次正式落「進場·核心」",
      "ruling": "非翻面（前份無正式裁決可翻）；本次進場理由＝前份預設的回測條件已成立＋基本面加速，不是估值更便宜的單一理由。90 天內 hysteresis 不適用（跨 124 天）",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "若 Q3 財報後價回 $330 以上未完成三段 → 不追，剩餘段改掛論點增強",
        "若跌破 $260 且 H1-H3 無損 → 第二段"
      ],
      "prior_field": "dca_verdict"
    },
    {
      "axis": "前份漂移：dca_role／archetype／cycle_position（前份格式無此三欄，首次出現）",
      "side_a": "本次：核心／品質複利成長／不適用（非循環）",
      "side_b": "前份：無此欄（v12.3 無決策層與分類欄）",
      "ruling": "方法論驅動（v12.3→v15.2 新增欄位），非基本面或價格變化",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "dca_role"
    },
    {
      "axis": "前份漂移：price_at_dd",
      "side_a": "本次 $292.7",
      "side_b": "前份 $340.94",
      "ruling": "價格變了（主因，−14%）；基本面反向變好（FY1 共識 +2.4%、指引上修）；方法論不涉。歸因排序：價格 > 基本面（反向）> 方法論",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "price_at_dd"
    },
    {
      "axis": "前份漂移：ma",
      "side_a": "本次「-」（週線均線證據包未涵蓋，不得填燈）",
      "side_b": "前份 ✅ 強勢進場",
      "ruling": "資料／方法論驅動為主（v17 證據包未含週線結構）；價格驅動為次——13 週 −22%、距 52 週高 −30%，✅ 幾乎確定不再成立，最可能落「價低於兩年線、高於五年線」帶，交閘複核",
      "evidence_level": "L1（價格）",
      "settle_metric": "週線 W52／W104／W250 位置",
      "if_then": [
        "若價低於五年線 → 首階仍三分之一但改分四段",
        "若站回兩年線 → 依原三段"
      ],
      "prior_field": "ma"
    },
    {
      "axis": "前份漂移：signal／val／trap（三欄皆未變：A／🟡／🟢）",
      "side_a": "本次 A／🟡／🟢",
      "side_b": "前份 A／🟡／🟢",
      "ruling": "無漂移；val 維持 🟡 的路徑不同——前份靠 PEG 1.55，本次靠盲點一救援（FY2026 PEG 2.12 偏貴、FY2027 PEG 1.80），方法論細節變、結論同",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "signal"
    },
    {
      "axis": "前份漂移：val 路徑（同上）",
      "side_a": "🟡",
      "side_b": "🟡",
      "ruling": "無漂移，見 signal 條目",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "val"
    },
    {
      "axis": "前份漂移：trap（同上）",
      "side_a": "🟢",
      "side_b": "🟢",
      "ruling": "無漂移；成長信號表新亮「倍數下移」一燈但五問定性仍非陷阱",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "trap"
    },
    {
      "axis": "前份漂移：moat_trend／runway_post_y5／rearm_trigger（前份格式無此三欄）",
      "side_a": "本次 ↑／🟢／$260 或 token 揭露",
      "side_b": "前份無此欄（v12.3 只有 moat 二維分 8/9）",
      "ruling": "方法論驅動（新欄）；護城河分由 9 降至 8.5 是本次對定價維度更保守（CEO 對定價權提問迴避，來源：摘要），屬判斷收緊非基本面惡化",
      "evidence_level": "L2",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "moat_trend"
    },
    {
      "axis": "前份漂移：asym_ratio／ev5y_pct／irr_base_pct／max_dd_pct／bull_5y_price／bear_5y_price／p_bull_pct／p_bear_pct（前份格式無情境樹六欄）",
      "side_a": "本次 3.7／50.8／10.7／−50／$669.6／$206.8／25／30",
      "side_b": "前份無此欄（v12.3 只有 5Y 目標價 $540、upside +58%）",
      "ruling": "方法論驅動（情境樹為 v13 後新增）；可比部分：前份 5Y 目標 $540 vs 本次 Base $471——差異主因終端倍數本次取 30x 更保守，次因基準價下移",
      "evidence_level": "L2",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "asym_ratio"
    },
    {
      "axis": "同形狀 peer 對帳",
      "side_a": "SNPS／ARM 近 30 天無本站裁決可對",
      "side_b": "—",
      "ruling": "一句帶過：無近期 peer 裁決，不阻斷",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ]
    },
    {
      "axis": "指引上修卻低於共識 vs 賣方目標價全面上修（可調和）",
      "side_a": "FY2026 指引中值營收 $6.30B／EPS $8.10 略低於當時共識 $6.329B／$8.12",
      "side_b": "BofA／KeyBanc／Stifel 上修目標價至 $420-432",
      "ruling": "程度差異：公司一貫「一年一次、年初保守」（來源：摘要），共識已跑在指引前；本檔一年目標 $315 低於賣方，不依賴共識上修",
      "evidence_level": "L1",
      "settle_metric": "FY2027 指引 vs 共識 9.54",
      "if_then": [
        "若 FY2027 指引 <9.2 → 停止加碼",
        "若 ≥9.6 → 第二段"
      ],
      "evidence_refs": [
        "capital_markets_pricing#1",
        "capital_markets_pricing#4"
      ]
    }
  ],
  "premortem": {
    "blind_spots": [
      {
        "text": "最新一季（Q2 2026，2026-07-27）法說逐字稿不在證據包，只有新聞稿 KPI；四季摘要止於 Q1 2026——管理層對 8 月軟體股拋售與 token 變現的最新口徑未親讀，AI 顛覆軸的判斷信心因此打折",
        "evidence_refs": [
          "substitute_technology#0"
        ]
      },
      {
        "text": "出口合規紀錄：2015-2021 對軍方大學非法出口、認罪＋$140M、三年緩刑——前提「管理層合規把關已修復」未經第三方驗證；若緩刑期內再違規，罰則與許可制風險同時升高",
        "evidence_refs": [
          "sec_investigation_restatement#0",
          "major_events#4",
          "reg_tariff_export#0"
        ]
      },
      {
        "text": "客戶信用：Intel（最大單一帳戶）BBB 展望負向、Samsung 代工虧損延至 2028——前提「前段客戶專案不延遲」在 2027 資本支出降檔時最脆弱；10-Q 應收集中度 2024 年末曾一客戶 11%",
        "evidence_refs": [
          "customer_concentration_credit#1",
          "customer_concentration_credit#2",
          "customer_concentration_credit#3",
          "customer_second_source#2"
        ]
      },
      {
        "text": "Hexagon $3.2B 換年化 $200M 營收（20x）——前提「physical AI 3-7 年兌現」由 CEO 自己說時點很難說（來源：摘要）；若 2027 未如承諾轉增益，資本配置等級降 C，長期信心上限降中",
        "evidence_refs": [
          "major_events#0"
        ]
      },
      {
        "text": "週線結構與五年連續分位皆證據包未涵蓋（分位只有 4 個年度點）——擇時層是本檔最薄的一層，首階三分之一即為此設計",
        "evidence_refs": [
          "geo_supply_chain#0"
        ]
      }
    ],
    "failure_story": "2027 年超大規模業者 AI 資本支出增速反轉，流片量遞延、續約漲幅歸零；BIS 同時恢復對華 EDA 許可，中國營收腰斬；市場把 EDA 由 AI 受惠者改列成熟軟體，倍數壓到 20x——5 年虧半。與唯一事件對照：⚠ 部分重疊（中國段撞上，資本支出段獨立）→ 已回補 secondary trigger（觸發器 5：Big-4 2027 指引）",
    "second_failure": "核心 thesis 完全兌現但以「AI 讓每專案人力減 30%、token 計費只補回人頭損失」的形態兌現：營收成長落在 8-10% 而非 15%，市場把估值框架從「AI 放大器 35x」切到「成熟工具商 22x」，5 年報酬近零——機率不可忽略，已反映在 Bear 終端 22x 與 Base 終端 30x（非現價 36x）",
    "max_dd": {
      "lo": -50,
      "hi": -35,
      "path_risk": "🟡",
      "trigger_time": "2027 上半年：Big-4 2027 資本支出指引（1-2 月）＋BIS 50% 規則落地後（2026-11）疊加 Q4 財報 FY2027 指引若 <+13%；恢復峰值需 FY2028 盈餘（約 2028 下半年）——若唯一事件觸發則 thesis 已破不談恢復"
    }
  },
  "kill_metrics": [
    {
      "metric": "積壓 TTM 年增",
      "bear_threshold": "連 2 季 <0",
      "window": "每季",
      "source": "季度新聞稿",
      "last_status": "ok"
    },
    {
      "metric": "Core EDA 有機成長 TTM",
      "bear_threshold": "<8% 連 3 季",
      "window": "每季",
      "source": "法說分段成長率",
      "last_status": "ok"
    },
    {
      "metric": "中國營收佔比／許可狀態",
      "bear_threshold": "許可制恢復（唯一事件）；佔比連 4 季 <9%",
      "window": "每季＋事件",
      "source": "法說、BIS 公告",
      "last_status": "warning"
    },
    {
      "metric": "Big-4 2027 AI 資本支出指引年增",
      "bear_threshold": "任一 <+20%",
      "window": "2027-01 法說季",
      "source": "超大規模業者法說",
      "last_status": "unknown"
    },
    {
      "metric": "非 GAAP 營業利益率 TTM",
      "bear_threshold": "年減 >100bp 連 2 季",
      "window": "每季",
      "source": "季度新聞稿",
      "last_status": "ok"
    },
    {
      "metric": "應收帳款客戶集中度",
      "bear_threshold": "任一客戶 ≥10%",
      "window": "每季",
      "source": "10-Q",
      "last_status": "ok"
    }
  ],
  "reasoning": {
    "archetype": "指紋：毛利 85.9%、非 GAAP 營業利益率 45.5%、FCF 利潤率 28.6%、經常性 78%、資本支出約 3% → 資本輕高留存寡占 → 品質複利成長，信心高；無循環子型特徵（積壓 $8.1B 覆蓋 FY26 67%，非訂單型），不需 blend。implication：§4 用複利尺、§10 用前瞻本益比與 PEG。",
    "thesis": "H1 份額：IP +40%（Q2）vs SNPS IP 清淡年、硬體新客 30 家、系統廠 45%（兩年前 40%）→ 取份額有 sourced；H2 收費模式：CEO 稱 token-based＋基礎訂閱（來源：摘要）但無營收揭露 → 列驗證期限 FY2028；H3 槓桿：增量利潤率 59-60%（來源：摘要）、Q2 45.5% 優於指引高標。R1-R3 各對應 15 條負向 finding 中的 12 條，餘 3 條落威脅與盲點。唯一事件取政策軸：2025-05 已發生一次、10-K 明列可能重施、EPS 敏感度 −15-18% 為最大單一項。",
    "industry": "ID shortage／Phase II 以積壓創高、硬體交期中段、2027 設備銷售預期創高交叉驗證後載入；三軸裁決＝雙向拉鋸：A 競爭惡化（Siemens agent、Synopsys-Ansys 全棧）與 B 結構轉好（活動量計費、系統廠自研）並存，C 其他結構變數指名法規軸（BIS 50% 規則 2026-11-09）。閘 B：供需 durability 判結構性持久（TAM CAGR 8-9%、設計複雜度單向），bear 機率不因「產業在缺」壓低。TAM：純 EDA $18.2B→$33.5B（9.1%）。",
    "moat": "執行 9（份額三線同升、Palladium 六年紀錄）×定價 8（rational oligopoly、續約漲價 sourced 只在 SNPS、CEO 迴避定價權提問）→ 8.5 → A。閘一：GAAP 營業利益率 30.8% vs SNPS 9.7%，spread 正且擴大（Q2 +940bp）✓。閘二毛利無 >1.5pp 年減證據；閘三對手絕對美元新增證據包未涵蓋。趨勢 ↑：≥1 個 12 個月內 sourced data point（IP +40% 2026-07；COT 流片 2026-04）；閘 A 無最大客戶份額下滑證據（Intel 是在擴大灘頭）。§5.R：ROIIC 17.6%×再投資 88%＝天花板 15.5%，共識 17% 含淨回購 1% 在邊界內 → endo_ceiling_exceeded=false。",
    "growth": "Runway：EDA 市場 2026 $18.2B→2033 $33.5B，Cadence 30% 份額；以 13% 成長 vs 市場 9%，Y5 末份額約 35%、滲透遠未達 70% → 跑道 12 年、Y5 後 🟢（S 曲線中段＋sourced 第二曲線：ChipStack token 2026 下半年早期存取、physical AI／Hexagon）。分部加總：Core EDA 13-14%＋IP 17-20%＋SD&A 15-16% → 合併約 14%，與 Base EPS 14% 對得上（差 <5pp）。有機 vs 無機：三年併購貢獻約 2pp（CFO：14% 中約 2% 併購，來源：摘要）<30%。熄火壓測：成長降至 15%／10%／5% 對應本益比 30／24／18x → 自現價 −17%／−33%／−50%（以 FY1 EPS）。衰退信號 1 燈（倍數下移）→ 🟡。",
    "quality": "Q2：營收 $1,584M（+24.2%）、非 GAAP 營業利益率 45.5%、GAAP 28.4%、FCF $582.3M（36.8%，YTD 減 Q1 換算）、SBC 9.3%。TTM：GAAP 營業利益率 30.8%、FCF 利潤率 28.6% → FCF/營業利益 ≈0.93，轉換率高。營收 YoY 24.2%−GAAP 營業利益 YoY（19.0%→28.4% 隱含 +85%）→ divergence 深負＝利潤率擴張，無壓縮警示。回購 50% FCF、淨稀釋 ≤0。5 年 FCF 逐年與 CCC 證據包未涵蓋 → 標明，不推估。lumpiness 🟢：Q1 20.8%／Q2 36.8% 為出貨時點。",
    "governance": "計分卡 1/3 過（SBC 淨稀釋過；M&A ROIIC 未證——Hexagon 20x 營收；回購收益率 2.8% <6%）→ B。四項必涵蓋：股權結構／薪酬／內部人交易證據包未涵蓋（數據限制）；資本配置＝50% FCF 回購＋史上最大併購 $3.2B。重大事件：DOJ 認罪 $140M 為合規失靈（非 SEC 調查、非重編），進盲點與 R1；無集體訴訟。B 級不觸發持有年限上限。",
    "valuation": "FY1 8.14／FY2 9.54／FY3 11.14（2026-09-04 快照，stale=false）→ 前瞻本益比 35.96／30.68／26.27x；EPS CAGR (11.14÷8.14)^(1/2)−1＝17.0%；PEG 2.12（FY1）／1.80（FY2）。分位：trailing 本益比 60.6x 在 4 個年度點分位 32.8%（P/S 26.8、EV/S 30.3）→ 🟡 帶。較嚴讀法（FY1 PEG 2.12）落 🟠，盲點一（成長 🟢＋PEG_fy2 1.80 <2＋AI 🟢）救回 🟡；盲點三不成立（90 天上修 +2.4%）。目標：1Y 9.54×33＝$314.8（+7.6%）、2Y 11.14×33＝$367.6（+25.6%）、5Y 15.7×30＝$471（+60.9%）；Bear anchor 7.33×24＝$175.8（−39.9%）。Base IRR 約 10.0% 不含息＋淨回購 0.7 ≈10.7%（中）；re-rate 貢獻為負（36→30x）→ 非估值依賴型。市場錯在哪：把「AI 減人頭」等同「AI 減 EDA 支出」，忽略活動量計費與每顆晶片 EDA＋IP 投資倍增。",
    "trap_analysis": "五問：模式＝倍數下移中的成長股；反證＝營收 +24.2%、積壓 $8.1B、指引上修、共識上修 +2.4%；正證＝trailing 本益比 78.9x→60.6x 而盈餘只升 2%、2026 為續約低年；空頭一擊＝2027 資本支出 <+20% → FY2027 EPS 8.6×22-24x＝$190-205（−30-35%）；持有期判別＝積壓年增連 2 季負＋Core EDA <10% 連 2 季。定性 🟢 非陷阱（倍數觀察）。自我攻擊三點：(1) ↑ 只靠管理層自述？→ 有第三方（datagravity 多代工卡位、Next Platform COT 流片）但仍交閘複核；(2) 進場是否只因跌 30%？→ 否，一年目標 +7.6% 弱、靠 5 年 +61% 與品質，故首階三分之一；(3) 中國風險是否該直接觀望？→ 12-13% 曝險已在唯一事件與 Bear 30% 定價，觀望需 binding constraint 而非多因素模糊——三點皆未推翻。",
    "premortem": "Max DD：Bear anchor −40%、Bear 5Y −29%、2022 年 trailing 本益比低點 51.7x 對現 60.6x 隱含 −15% 倍數＋盈餘下修 10% → 範圍 −35%~−50%（寬 15pp ≥10pp），🟡；觸發 2027 上半年；thesis 完整（趨勢 ↑、跑道 🟢、非估值依賴）→ 不因波動砍倉，註記深回撤心理準備。失敗故事與唯一事件 ⚠ 部分重疊 → 回補觸發器 5。第二敗局成立 → Bear 終端 22x、Base 終端 30x。"
  },
  "evidence_dismissed": [],
  "plain": {
    "verdict_line": "進場，當核心持股，但先買三分之一。",
    "verdict_sub": "現價先建三分之一，跌到 $260 或公司公布 token 營收再加一段，BIS 十一月規則落地無新管制再補最後一段。",
    "five": {
      "how_it_makes_money": "賣晶片設計軟體、驗證硬體與設計 IP 給全球約 60 家大晶片與系統公司，多年合約、78% 是經常性收入。",
      "why_now": "股價從高點跌了 30%，跌到前一份報告等待的位置以下；同時營收年增 24.2%、積壓創高、全年展望上修。市場在怕 AI 顛覆軟體，公司卻在加速。",
      "why_this_size": "五年基本情境年化報酬約 10.7%，屬中等；一年內上檔只有 7.6%、下檔可到 −40%。好生意、價格只是合理，所以核心角色但分三段買。",
      "biggest_fear": "美國恢復對中國的 EDA 出口許可制——中國佔營收 12-13%，2025 年已經發生過一次六週的版本。",
      "how_to_act": "首階三分之一現價買；第二段看 $260 或 token 營收揭露；第三段看 2026-11-09 BIS 規則落地。清倉只認許可制恢復。"
    },
    "business": {
      "what_to_whom": "把設計、驗證、模擬晶片的工具與現成 IP 賣給晶片公司、代工廠與自研晶片的雲端／車廠，約 60 家客戶貢獻 70% 營收。",
      "why_customers_stay": "先進晶片不經簽核工具不能流片；換工具等於整套驗證重跑；合約多年、67% 的今年營收在年初就已鎖在積壓裡。",
      "moat_direction": "護城河 A 級、方向擴大：IP 年增逾 40% 而對手自認清淡年，硬體新增 30 家客戶。最弱處是定價：AI 代理的 token 計費還沒變成營收，執行長對定價權提問也只談交付價值。"
    },
    "bets": [
      {
        "claim": "AI 讓晶片設計活動量增加，Cadence 的收費會跟著活動量走，不會被客戶減人頭拖垮。",
        "wrong_when": "到 2028 年仍看不到任何 token 或消費型營收揭露，且核心 EDA 成長連三季低於 8%。"
      },
      {
        "claim": "三線同時取份額會延續：IP、驗證硬體、系統模擬。",
        "wrong_when": "積壓年增連兩季轉負，或系統廠客戶佔比連兩年下降。"
      },
      {
        "claim": "增量利潤率 60% 會把營業利益率推向 48% 以上。",
        "wrong_when": "非 GAAP 營業利益率連兩季年減超過 100 個基點，或增量利潤率連兩年低於 40%。"
      }
    ],
    "fears": [
      {
        "clock": "🔥",
        "text": "對中國出口管制收緊：中國佔 12-13% 營收，BIS 50% 規則 2026-11-09 到期，許可制若恢復是清倉級。"
      },
      {
        "clock": "🔥",
        "text": "2027 年 AI 資本支出降檔：任一大型雲端業者指引年增低於 20%，流片與續約會延後 6-12 個月傳導。"
      },
      {
        "clock": "🐢",
        "text": "客戶集中與信用：最大單一帳戶 Intel 信評已到 BBB，Samsung 代工虧損延到 2028；約 60 家客戶佔七成營收。"
      }
    ],
    "market_wrong": "市場把「AI 讓每個專案少 30% 工程師」讀成「AI 讓 EDA 支出減少」。但 Cadence 的成長來自設計活動量，不是人頭；自研晶片的雲端業者把每顆晶片的 EDA 與 IP 投資推高一倍。賣方共識目標價中位數 $405 也高於本檔的一年目標 $315，本檔不靠共識上修就成立。",
    "growth_funding": "內生成長天花板約 15.5%（增量報酬 17.6% 乘再投資 88%），共識 17% 的盈餘成長扣掉約 1% 淨回購後落在邊界內，不需要靠估值重評。",
    "stories": {
      "bull": "token 計費在 2027 年變成看得見的營收，Hexagon 的 physical AI 模擬開始賣，成長守住 18-20%，市場維持 36 倍本益比，五年翻一倍多。",
      "base": "成長從 16% 緩降到 12%，營業利益率擴到 48%，本益比從 36 倍降到 30 倍，五年上漲約 61%、年化約 10.7%。",
      "bear": "2027 資本支出降檔加上中國管制回來，盈餘五年只從 8.14 走到 9.4，市場改用成熟軟體 22 倍定價，五年跌 29%。"
    },
    "change_my_mind": [
      {
        "what": "BIS 是否恢復對華 EDA 出口許可制",
        "threshold": "正式通知且 90 天內未撤銷",
        "then": "清倉，不等財報",
        "when": "2026-11-09 起持續"
      },
      {
        "what": "核心 EDA 有機成長與積壓",
        "threshold": "成長低於 8% 連三季且積壓年增連兩季為負",
        "then": "清倉，重啟須重跑報告",
        "when": "2027-08-31"
      },
      {
        "what": "token 營收是否揭露、股價是否到 $260",
        "threshold": "任一成立",
        "then": "加第二個三分之一",
        "when": "2027-02-28"
      }
    ],
    "prior_compare_reason": "與 2026-05-04 前份相比，主因是價格：股價從 $340.94 跌到 $292.7，落到前份等待的回測帶以下；基本面反而更好，方法論新增了決策層與情境樹。",
    "how_to_lose": "第一種死法：2027 年 AI 資本支出反轉加上中國管制回來，盈餘停滯、倍數壓到 20 倍，五年虧一半。第二種死法：AI 真的讓每個專案少 30% 人力，token 計費只補回人頭損失，成長掉到 8-10%，市場把它當成熟工具商用 22 倍定價，五年報酬接近零。",
    "evidence_quality": "十四軸覆蓋，營運數字以 2026 年第二季（7 月 27 日公告）為準；最新一季法說逐字稿缺檔、四季內容全靠摘要（2025 年第三季至 2026 年第一季）與六場投資人會議摘要，沒有親讀任何一季。週線均線與五年連續分位不在證據包。"
  }
}
