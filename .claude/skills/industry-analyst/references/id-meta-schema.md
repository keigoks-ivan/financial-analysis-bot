# industry-analyst v2.6 — id-meta-schema.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-08 v2.6 結構拆分，內容自 v2.5 原文搬移）。必讀時點見 SKILL.md 對應 stub。

## 【id-meta JSON Schema（原樣保留，schema 不准動）】

> **v2.0→v2.2 相容說明**：id-meta JSON schema 在 v2.2 新增 **3 個 optional 欄位** `now_state` / `future_state` / `action`（§0 三句話）— validator **不 reject unknown key**（實測；只有 `sections_refreshed` 子鍵走白名單），故對 legacy 零影響；這三欄**只在 `skill_version` 為 `v2.x` 時必填**（`V2_RE` 阻斷、各 ≤240 字元），v1.x legacy ID 不受影響。`skill_version: "v2.x"` 即新格式標記（validator 只 regex 驗 vN.N）。`sections_refreshed` 沿用 `technical / market / judgment` 三桶，v2 章節 mapping：**technical → §1-§2、market → §3-§5、judgment → §6-§9**。`related_tickers[]` / taxonomy（mega + sub_group）/ oneliner 規則全部不變 → stock-analyst、DCA、earnings-synthesis 零感知（新欄位純為 §0 + 下游索引/screener 之後可選用）。**v2.4 再新增 3 個 optional 欄**：頂層 `demand_5y_multiple`（number，5Y 需求倍數）+ `related_tickers[]` 每項 `purity_pct`（number 0-100）/ `mcap_bucket`（enum mega/large/mid/small）——validator 只在 present 時驗型/驗 enum，legacy v1.x-v2.3 全豁免；**v2.4+ 新報告三欄皆必填**（skill 流程要求，非 validator 阻斷）。用途＝多倍候選機器初篩：`depth=🔴 ∧ purity_pct ≥ 40 ∧ mcap_bucket ∈ {mid,small}`（個股層）× `demand_5y_multiple ≥ 2 ∧ 供需裁決=短缺`（產業層）。**v2.5 再新增 5 欄並把跨 ID 趨勢排序鍵升為 validator 必填**：`sd_verdict`（enum shortage/balanced/surplus/split，§5 供需裁決機器形態）+ `sd_verdict_detail`（string ≤160，`split` 時必填）+ `clock_phase`（enum I/II/III/IV，投資時鐘）+ `conviction`（enum high/mid/low，與 §0 綠卡同步）+ `kill_metrics[]`（array，§8 證偽表機器化，≥3 條）。**驗證邏輯升級**：`skill_version` ≥ v2.5 時 `sd_verdict` / `clock_phase` / `conviction` / `kill_metrics(≥3)` **及 v2.4 三欄**（頂層 `demand_5y_multiple`；`related_tickers[]` 每個 `depth=🔴` 項的 `purity_pct` / `mcap_bucket`，🟡🟢 選填以免對邊緣股過苛）全升為 **validator 阻斷式必填**；v2.0–v2.4 present 才驗型/驗 enum、absent 放行；v1.x legacy 全豁免。至此 v2.4 獵場篩選條件 `demand_5y_multiple ≥ 2 ∧ sd_verdict==shortage ∧ conviction ≥ mid` 欄位齊備、可直接機器執行，證偽表也由 position-thesis-monitor 直接掃 `kill_metrics`（不再依賴 DD 存在）。

每份 ID HTML 的 `<head>` 內必含 `<script id="id-meta" type="application/json">{...}</script>`，在 `<title>` 之後、第一個 `<style>` 之前，與既有 `<meta name="id-*">` tags 並存。這是下游消費者（stock-analyst §9 自動引用、CI validator、未來 sector index）的 SSOT。**漏寫 → CI `Validate DD + ID metadata` workflow strict gate fail，整 push 連坐被擋**。

**必填欄位**：

| 欄位 | 型別 | 說明 |
|:---|:---|:---|
| `theme` | string | 產業主題（e.g. `"AI EDA + IP"`、`"HBM 供需循環"`）|
| `skill_version` | string | 建立時 skill 版本（填當前版本，現 = `"v2.5"`）|
| `id_version` | string | 此 ID 自身版本（`"v1.0"` 初版）|
| `publish_date` | string | `"YYYY-MM-DD"` |
| `thesis_type` | enum | `"structural"` / `"event-triggered"` / `"mixed"` |
| `ai_exposure` | enum | `"🟢"` 直接受益 / `"🟡"` 部分受益 / `"🔴"` 中性或受害 |
| `oneliner` | string | ≤ 200 chars，核心 thesis 一句話 |
| `now_state` | string | **v2.x 必填**，≤ 240 chars，§0 三句話之「現在」（產業現況裁決 + 證據錨點）|
| `future_state` | string | **v2.x 必填**，≤ 240 chars，§0 三句話之「未來」（3-5 年走向 + 最大結構裂縫）|
| `action` | string | **v2.x 必填**，≤ 240 chars，§0 三句話之「怎麼做」（標的層級 + 動作，可寫「都不買」）|
| `related_tickers` | array | 關聯個股；每項 `{ticker, role, depth, beneficiary}` |
| `sd_verdict` | enum | **v2.5+ 必填**；`"shortage"` / `"balanced"` / `"surplus"` / `"split"`（§5 供需裁決機器形態；`split`＝分段結論不一致）|
| `clock_phase` | enum | **v2.5+ 必填**；`"I"` / `"II"` / `"III"` / `"IV"`（投資時鐘 phase，與 §0 6-box 同步）|
| `conviction` | enum | **v2.5+ 必填**；`"high"` / `"mid"` / `"low"`（與 §0 PM 綠卡 conviction pill 同值）|
| `kill_metrics` | array | **v2.5+ 必填（≥3 條）**；§8 證偽表機器形態，每項 `{metric, bear_threshold, window}`（+ 選填 `source` / `last_status`）|
| `demand_5y_multiple` | number | **v2.5+ 必填**（頂層）；5Y 需求倍數 = §4 base 情境 5Y TAM ÷ 現 TAM（爆發獵場排序鍵；v2.4 為 skill 流程必填、v2.5 升 validator 阻斷）|

**選填欄位**（不強制）：

| 欄位 | 型別 | 說明 |
|:---|:---|:---|
| `tam_usd_2030` | number | 2030 TAM in billion USD |
| `cagr_pct_5y` | number | 5Y CAGR % |
| `sd_verdict_detail` | string | **v2.5**；≤160 chars，`sd_verdict=="split"` 時**必填**（例：「商業段=過剩；政府段=短缺」），其他值時選填 |
| `growth_phase` | enum | `"early"` / `"mid"` / `"late"` / `"declining"` |
| `value_chain_position` | enum | `"upstream"` / `"midstream"` / `"downstream"` / `"cross-tier"` |
| `industry_structure` | enum | `"monopoly"` / `"duopoly"` / `"oligopoly"` / `"fragmented"` |
| `sections_refreshed` | object | `{"technical": "YYYY-MM-DD", "market": "YYYY-MM-DD", "judgment": "YYYY-MM-DD"}` |
| `sister_ids` | array | 兄弟 ID HTML 檔名列表 |
| `quality_tier` | enum | `"Q0"` Flagship / `"Q1"` Standard / `"Q2"` Quick（影響 Claim Taxonomy enforcement 與 Step 8.7 blocking 強度）|
| `mega` | enum | 15 大類白名單（`docs/id/taxonomy.md`）— validator 選填但**本 skill 流程必填**（Step 0 分類 + index.html 卡片插入依賴它）|
| `sub_group` | enum | 對應 mega 的子群白名單（同 taxonomy.md）— 同上，**本 skill 流程必填** |

> #### 🚫 **嚴禁複合 enum 值 / 自創字串 / 加修飾詞**（CI strict gate 阻斷）
>
> Validator 嚴格匹配 enum 字串集合。**禁止以下實際發生過的錯誤**：
>
> | ❌ 違規寫法 | ✅ 正確寫法 | 說明 |
> |:---|:---|:---|
> | `"thesis_type": "structural+event"` | `"mixed"` | 用 `mixed` 表達雙重屬性，不要 `+` 拼接 |
> | `"growth_phase": "mature_diverging"` | `"late"` | mature 對應 `late`；diverging 是敘事細節 |
> | `"growth_phase": "structural_supercycle_expansion"` | `"mid"` 或 `"early"` | 自創長字串映射到四選一 |
> | `"growth_phase": "consolidation"` | `"late"` | consolidation 屬 mature 後期 |
> | `"value_chain_position": "concentrate-to-shelf"` | `"cross-tier"` | 跨多段一律 `cross-tier` |
> | `"value_chain_position": "upstream_commodity"` | `"upstream"` | 不要加修飾詞 |
> | `"value_chain_position": "intermediation"` | `"cross-tier"` | 中介性質 = 跨上下游 |
> | `"industry_structure": "oligopoly+disruption"` | `"oligopoly"` | disruption 是動態描述 |
> | `"industry_structure": "regional_oligopoly"` | `"oligopoly"` | 地區性質寫進 oneliner |
>
> **規則**：metadata 是給 validator + 下游 parser 讀的「分類標籤」，不是給人讀的「敘事描述」。複雜二元性、地區屬性、disruption 動態都寫進章節內文，metadata 只保留 enum 主分類。
>
> #### 🚫 **`oneliner` 嚴格 ≤ 200 chars**（含中英文混合）
>
> Validator hard cap 200 字元。實際發生過 308 / 468 / 483 / 614 字元 violation。**正確做法**：① oneliner 只放 3-5 個關鍵數字錨點 + 1 個結論動詞；② 詳細論述留給 §0 thesis / §7 章節；③ 寫完用 `len(d['oneliner'])` 自測，> 180 立刻精簡（留 20 char buffer 應付下游 emoji / 全形字元計算差異）。
>
> 範例（180 chars 內）：「銅 2026 預期 \$11K–13K（Citi \$13K / GS \$10.7K / MS 600kt deficit「20 年最嚴」）；三引擎共振：AI DC + Grid + EV；Anglo-Teck \$53B + Codelco \$40B 響應。」

#### `related_tickers` 物件 schema

```json
{
  "ticker": "AVGO",
  "role": "AI ASIC 設計 + 網通 silicon photonics",
  "depth": "🔴",
  "beneficiary": true,
  "purity_pct": 41,
  "mcap_bucket": "mega"
}
```

- `depth`: 🔴 核心受益 / 🟡 中度 / 🟢 輕度。
- `beneficiary`: `true` 受益 / `false` 受害。
- `purity_pct`（v2.4 選填；**v2.5+ 對 `depth=🔴` 項 validator 必填**，🟡🟢 選填）: number 0-100，該產業營收占比（§9 表「純度%」欄；每檔須附一行 segment 營收推導，見 §9）。
- `mcap_bucket`（v2.4 選填；**v2.5+ 對 `depth=🔴` 項 validator 必填**，🟡🟢 選填）: `"mega"`（>$200B）/ `"large"`（$10-200B）/ `"mid"`（$2-10B）/ `"small"`（<$2B）。**下游用法**：`depth=🔴 ∧ purity_pct ≥ 40 ∧ mcap_bucket ∈ {mid, small}` = 多倍候選初篩，配合 `demand_5y_multiple ≥ 2` 的 ID 即爆發獵場名單。

#### `kill_metrics` 物件 schema（v2.5）

```json
{
  "metric": "商業段 net booking YoY",
  "bear_threshold": "連兩季 < +15%（base 假設 +40%）",
  "window": "18M",
  "source": "IR 季報 / SpaceX 官方",
  "last_status": "ok"
}
```

- `metric`（≤120）: 證偽指標名，與 §8 證偽表逐條對齊。
- `bear_threshold`（≤120）: bear 閾值＝thesis 作廢點（真 falsification，非 strawman）。
- `window`（≤60）: 觀察時間窗。
- `source`（≤120，選填）: 指標數據來源。
- `last_status`（選填）: `"ok"` / `"warning"` / `"triggered"` / `"unknown"`，供 position-thesis-monitor 回填最新狀態（skill 首發時通常 `"unknown"` 或 `"ok"`）。

#### 範例（AI EDA + IP，v2.0）

```html
<script id="id-meta" type="application/json">
{
  "theme": "AI EDA + IP",
  "skill_version": "v2.5",
  "id_version": "v1.0",
  "publish_date": "2026-07-05",
  "thesis_type": "structural",
  "ai_exposure": "🟢",
  "oneliner": "AI 晶片設計爆發推動 EDA + IP 需求結構性向上，SNPS/CDNS 雙寡占受益顯著，AI-native EDA tooling 為下一個複利層。",
  "now_state": "需求結構性向上、供給雙寡占——AI 晶片設計爆發推動 EDA/IP 用量，SNPS/CDNS 合計 >70% 份額、客戶遷移成本極高，現況是賣方市場。",
  "future_state": "未來 3-5 年雙寡占護城河更深，最大變數是 AI-native EDA tooling 能否把工具鏈重定價；中國自主 EDA 仍落後兩代、暫不構成結構威脅。",
  "action": "核心倉 SNPS / CDNS 續抱；估值偏貴（Fwd P/E 高位），新進等回調而非追高，ARM 列 🟡 衛星觀察授權模式變現。",
  "sd_verdict": "shortage",
  "clock_phase": "II",
  "conviction": "high",
  "kill_metrics": [
    {"metric": "SNPS+CDNS 合計份額", "bear_threshold": "跌破 60%（base >70%）", "window": "8Q", "source": "IR / ESD Alliance", "last_status": "ok"},
    {"metric": "AI-native EDA 新進者訂單", "bear_threshold": "頭部客戶簽走 ≥1 條全流程 tape-out", "window": "18M", "last_status": "unknown"},
    {"metric": "中國自主 EDA 製程覆蓋", "bear_threshold": "追至落後 ≤1 代且拿下本土 ≥30% 新設計", "window": "3Y", "last_status": "ok"}
  ],
  "related_tickers": [
    {"ticker": "SNPS", "role": "EDA 雙寡占 + ARC IP", "depth": "🔴", "beneficiary": true, "purity_pct": 95, "mcap_bucket": "large"},
    {"ticker": "CDNS", "role": "EDA 雙寡占 + Tensilica IP", "depth": "🔴", "beneficiary": true, "purity_pct": 95, "mcap_bucket": "large"},
    {"ticker": "ARM", "role": "CPU IP 通用授權", "depth": "🟡", "beneficiary": true, "purity_pct": 30, "mcap_bucket": "mega"}
  ],
  "tam_usd_2030": 25.0,
  "cagr_pct_5y": 14.5,
  "demand_5y_multiple": 1.9,
  "growth_phase": "mid",
  "value_chain_position": "upstream",
  "industry_structure": "duopoly",
  "quality_tier": "Q1",
  "mega": "semi",
  "sub_group": "eda_ip",
  "sections_refreshed": {"technical": "2026-06-11", "market": "2026-06-11", "judgment": "2026-06-11"}
}
</script>
```

#### 寫完後自我驗證（不可省略）

Write 完 ID HTML 後**立即執行**（在 terminal 摘要之前）：

```bash
python3 scripts/validate_id_meta.py docs/id/ID_{Theme}_{YYYYMMDD}.html
```

- exit 0 → 繼續輸出 terminal 摘要。
- exit != 0 → 讀錯誤訊息，用 Edit 修 id-meta JSON，重跑直到 exit 0。**不允許帶錯誤推 commit**（CI strict gate 會擋）。

**為什麼需要 id-meta**：避免下游反向 parse HTML（每次 template 改寫就崩）。stock-analyst skill §9 可直接從 `related_tickers` array 自動 join 公司 DD ↔ 產業 ID。

---

