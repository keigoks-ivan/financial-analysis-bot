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
