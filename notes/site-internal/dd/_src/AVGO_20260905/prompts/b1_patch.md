你是 stock-analyst v17 判斷 agent，回來做**一輪定點修補**。標的 AVGO（20260905）。判斷物已由跨模型閘（gate）冷讀過，下面是它點名的判斷級發現。你的任務只有一件：**針對被點名的欄位做最小修正**，不重寫判斷。

## 讀（僅此一個檔，一次讀完；其餘輸入已在下方 findings 內）

`.dd_build/runs/AVGO_20260905/judgment.json`

不要重讀 bundle、evidence.json、gate_audit.md、`docs/dd/` 任何檔，也不要回讀你等一下寫出的新版 judgment。你需要的稽核意見全文已附在下方。

## 閘的發現（gate findings）

### 發現 1：3 其他結構變數 🔴
- **依據**：substitute_technology#2（光學／光子 AI 加速器，2027-2031 商用，affects moat_trend、thesis.R）與 reg_tariff_export#2（BIS 2026-01-15 對中先進 AI 晶片改逐案審查）在 coverage 有料，judgment 全文無對應條目，亦未列入 evidence_dismissed[]
- **建議改法**：moat.threats 增「替代技術：光子計算 2027-2031」一條並在 premortem.blind_spots 記為 Y5 後假設；reg_tariff_export#2 併入 triggers[n=11] metric，或入 evidence_dismissed[] 寫明理由
- **指向欄位**：moat.threats／evidence_dismissed[]／triggers[n=11]

**受影響子樹原文**：

`moat.threats`：
```json
[
  {
    "level": "🔴 生態攻擊",
    "text": "Google 四夥伴供應鏈：MediaTek 推論 Zebrafish（Q4 2026 量產、成本低 20-30%）、Marvell 商業協議（2026-07-29）、Intel 處理器；Google 藉此取得定價與產能槓桿",
    "p": "60-70%（份額稀釋已在發生）",
    "evidence_refs": [
      "competitive_share_entrants#3",
      "customer_second_source#0",
      "customer_second_source#1"
    ]
  },
  {
    "level": "🔴 生態攻擊",
    "text": "MediaTek 目標 2027 搶 15-20% 客製 AI 晶片市場（$80B 估計），2026 資料中心營收 >$2B",
    "p": "50%",
    "evidence_refs": [
      "competitive_share_entrants#2"
    ]
  },
  {
    "level": "🟡 點對點",
    "text": "六大客戶各自投資內部設計能力，關係「深而黏但非永久」；風險因子明列客戶可能改採自有工具鏈（COT）或租賃模式",
    "p": "3-5 年 30%",
    "evidence_refs": [
      "customer_second_source#2",
      "customer_concentration_credit#2",
      "substitute_technology#1"
    ]
  },
  {
    "level": "🟡 點對點",
    "text": "VMware 資安事件（Aria Operations 零日遭中國國家背景組織利用；Clop 經 Oracle EBS 零日入侵 Broadcom 內部）削弱軟體信任",
    "p": "20%（信任型流失）",
    "evidence_refs": [
      "major_events#1",
      "major_events#2",
      "product_recall_warning#0",
      "product_recall_warning#1"
    ]
  }
]
```

**相關 evidence finding 原文**：

`substitute_technology#2`：
```json
{
  "claim": "光學 AI 加速器（optical/photonic computing）市場正快速成長，Ayar Labs、LightOn、Luminous Computing、Q.ANT、Salience Labs、Lightmatter、Optalysys 等新創正開發顛覆性架構，光學矩陣乘法引擎可在晶片層級以皮秒等級完成神經網路核心線性代數運算、耗能遠低於等效 GPU 運算，商用部署預期落在 2027-2031 年區間；Broadcom 本身也將光子能力納入其 AI 產品組合（如封裝內光學 I/O）。",
  "source": "GlobeNewswire, \"Optical AI Accelerator Market, 2026-2040 Industry Trends and Global Forecasts\"; yieldWerx, \"2026 Trends and Challenges in Photonics & Optical I/O Innovations\"",
  "as_of": "2026-05-13",
  "direction": "0",
  "affects": [
    "moat_trend",
    "thesis.R"
  ],
  "id": "substitute_technology#2"
}
```

`reg_tariff_export#2`：
```json
{
  "claim": "BIS (Bureau of Industry and Security) published a final rule effective January 15, 2026 revising export license review policy for advanced AI/computing semiconductors destined for China and Macau: applications now reviewed case-by-case instead of under a presumption of denial, but exporters must still confirm no restricted/Entity List/Military End-User parties are involved.",
  "source": "Morgan Lewis, \"BIS Revises Export Review Policy for Advanced AI Chips Destined for China and Macau\"",
  "as_of": "2026-01-15",
  "direction": "0",
  "affects": [
    "thesis.H",
    "decision_inputs.bear",
    "triggers"
  ],
  "id": "reg_tariff_export#2"
}
```


## 修補紀律

1. **只准改被點名的欄位**——findings 的「指向欄位」是你的動刀範圍。沒被點名的欄位一字不動，包含 `decision_out`（由 `dd_decision.py` 回填，你不要手改）與未涉及的 `reasoning` 段。
2. **裁決方向不由你主動翻**——修正欄位後若 `judge check` 重算出的 `decision_out.verdict` 自己翻面，那是機械層的結果，照實接受並在回報點名；但你不得為了配合閘的語氣直接改寫裁決字串。
3. **可以不採納**——閘的意見不是命令。判斷你認為原判正確時，該條不改欄位，改為在頂層 `evidence_dismissed[]` 補一條 `{"ref": "<閘點名的 finding ref 或欄位路徑>", "reason": "<不採納的具體理由>"}`。理由要指得出證據或推導本身的問題（口徑不可比、來源不可回溯、已被更新一季數字取代、閘誤讀了哪個欄位…），不得寫「影響不大」這類無內容句。**每一條 🔴 都必須有處置**：要嘛改欄位，要嘛進 `evidence_dismissed[]`，不得沉默略過。
4. **🟡 選擇性處理**——能一句話補上就補（通常是 `contradictions[]`／`triggers[]` 加一條或補 `formula_note`），代價過大就依第 3 條寫不採納理由。
5. **不得編造數字**——證據包未涵蓋的數字不准補；該欄位標「證據包未涵蓋」並在回報請 orchestrator 判斷是否回 Stage 0 補軸。
6. 禁 WebSearch／WebFetch。

## 寫（一次 Write 整檔）

改完後把**完整的 judgment.json**一次 `Write` 回 `.dd_build/runs/AVGO_20260905/judgment.json`（不要分次 Edit、不要只寫片段），接著跑：

```
python3 scripts/ddreport.py judge check AVGO 20260905
```

這支會依序重跑 `dd_scenario.py`、`dd_decision.py run`、`validate_judgment.py --evidence --fix --report`，一次把結果回給你；你不需要也不得自行分別呼叫這三支腳本。

FAIL → **只准改 FAIL 訊息點名的欄位**，重跑同一條 `judge check`，**≤1 輪**。一輪後仍 FAIL 就照實回報，交給 orchestrator 處置，不得為湊過驗證而改動判斷實質。

**輪次上限 `6` 輪。** 逼近上限時停下並照實回報。

## 回報（≤200 字）

① 逐條列閘的發現與你的處置（改了哪個欄位／或進 `evidence_dismissed[]` 及理由摘要）
② `judge check` 最後一次的 `validate_judgment.py --report` 原文
③ `decision_out.verdict`／`role`／`row_hit`，以及是否與修補前不同（翻面要明講）
