# `facts.json`｜DD v19 六問事實表（WP-H1，2026-09-11）

> Schema：`scripts/dd_schema/facts.schema.json`。產生器：`scripts/dd_facts.py extract`（零 LLM，只抽機械可抽的部分）＋整理 agent 補（H2 的 `facts.md.tmpl`，本包不做）。消費者：v19 判斷檔的 `answers[].fact_refs[]`、`scripts/dd_project.py`（投影 `price_at_dd`／`week26_return_pct`／`consensus_rev_3m_pct` 三個純事實欄）、判斷 bundle 與 gate bundle。

## 一、為什麼有這張表

v18 的判斷 agent 要自己從 250KB 的證據包裡挖數字、對齊期間與單位，挖完再寫進判斷檔。v19 把「找資料、對口徑」從判斷層搬走：事實只收一次、寫成有 id 的條目，判斷層只引 id。

**這張表不替判斷者決定哪些事實可信**。它的職責是定位與口徑，不是篩選。因此：

1. **`findings_digest[]` 不按方向裁掉**——正向反證、中性結構變化、來源衝突、查無的軸都要在。FIX 的 PFAS 是 `direction=0`、關稅緩解是 `direction=+`，只帶負向原文不能完整呈現問題。
2. **只帶「已被引用過」的 finding 也不行**——那會把前一份或整理者沒注意到的資料繼續排除。
3. **沒有篇幅硬上限**。15KB 是目標不是品質上限，判斷需要的資料不因超過配額而失去。

## 二、一條事實長什麼樣

```json
{
  "id": "f_q1_rev_advanced_tech_share",
  "label": "先進科技專案占總營收比重",
  "value": 56,
  "period": "Q1 FY2026",
  "unit": "%",
  "basis": "占合併總營收（GAAP）",
  "kind": "realized",
  "source": {
    "type": "evidence_finding",
    "ref": "customer_second_source#1",
    "as_of": "2026-03-31",
    "citation": "Zacks／Yahoo Finance"
  },
  "quote": "先進科技相關專案（主要為資料中心建設）占 FIX 2026 年第一季總營收 56%"
}
```

必填六欄：`id`／`value`／`period`／`unit`／`basis`／`kind`／`source`。

- **`id`**：`^f_[a-z0-9_]+$`，跨輪穩定。判斷檔的 `fact_refs[]` 只准引這個 id；引不到的 id 由 `validate_judgment` 報 FAIL。
- **`period`／`unit`／`basis`**：口徑三件。`basis` 要寫清楚分母是誰、是不是 GAAP、含不含一次性——口徑不明的數字不是事實。
- **`kind`**：`realized`（已實現）／`guidance`（管理層指引）／`estimate`（分析師或共識預估）／`claim`（來源的說法）。**「將成長」是預期不是事實**，一律 `guidance` 或 `estimate` 或 `claim`，不得記成 `realized`。
- **`source`**：定位到 evidence 的 finding id、`numbers` 路徑、逐字稿檔加段落、或 digest item。逐字稿來源必須定位到段落（`locator`），否則閘無法核對。
- **`quote`**：承重或有衝突的條目要附原文片段。gate 必須看得到判斷者實際採用的原文。
- **`conflict`**：與另一條事實或 finding 衝突時，記對造 id 與一句說明；衝突不得靜默擇一。

## 三、六題分組

| key | 題目 | 典型事實 |
|---|---|---|
| `q1_business` | 怎麼賺錢 | 誰付錢、分部與客戶占比、單價與量、最新一季營收與利潤率 |
| `q2_moat` | 競爭優勢 | 毛利率與同業對照、ROIC／ROIIC 輸入、份額數字、轉換成本證據 |
| `q3_growth` | 成長 | 共識三年 EPS、TAM 與滲透率、在手訂單、分部成長 |
| `q4_capital` | 現金與資本配置 | FCF／NI、SBC 占比、回購與股息、負債到期與利率 |
| `q5_valuation` | 估值 | 現價、Forward P/E 與五年分位、PEG 輸入、共識修正、同業倍數 |
| `q6_how_wrong` | 可能看錯在哪 | 歷史回撤、空方數字、訴訟與監管事實、集中度風險數字 |

每題可帶 `needs_sonnet: true`＋`needs_sonnet_note`，表示機械抽取抽不完、仍須整理 agent 補。**程式不得為了填滿欄位而編造**——抽不到就留空並標記。

## 四、機械可抽 vs 必須由人（或整理 agent）補

`scripts/dd_facts.py extract` 從 `evidence.json` 的 `numbers` 與 `coverage`／`events` 抽下列：

| 產出 | 來源 | 落在哪題 |
|---|---|---|
| `f_price_at_dd`／`f_price_as_of` | `numbers.price_at_dd`／`price_as_of` | q5 |
| `f_week26_return_pct` | `numbers.momentum_26w` | q5 |
| `f_consensus_rev_3m_pct` | `numbers.consensus_revision` | q5 |
| `f_fwd_pe_latest`／`f_pe_percentile_*` | `numbers.valuation_history` | q5 |
| `f_q_*`（最新一季 KPI 逐項） | `numbers.latest_quarter_kpis.items[]` | q1（營收與利潤率）／q4（FCF、SBC） |
| `f_peer_*` | `numbers.peer_financials` | q2 |
| `f_earnings_recency` | `numbers.earnings_recency` | q1 |
| `findings_digest[]` 全部 | `coverage`／`events` 逐條 | 不分題 |

抽不到而必須由整理 agent 或人補的（本包的 fixture 即以此標記）：分部與客戶占比的結構化值、護城河機制的量化證據、TAM 與滲透率、負債到期表、歷史回撤幅度、逐字稿原話。

## 五、複審（delta）模式

第二次起以上一份 `facts.json` 為底（`meta.prior_facts_ref`），每條事實標 `carry`：`carried_forward`（沿用，仍須帶原來源）／`updated`（有新資料）／`new`。**沿用不等於免責**：來源被修訂、期間過期、口徑改變都算 `updated`，不得把舊結論當事實沿用。

## 六、不做的事

- 不下判斷、不排序重要性、不寫「因此……」。
- 不因方向、篇幅或「上次沒用到」而刪條目。
- 不把 `prior_dd` 的結論（裁決、評級、門檻）寫成事實；前份結論只能以 `kind=claim`＋`source.type=prior_dd` 出現，且必須標明那是上一份判斷而非外部事實。
