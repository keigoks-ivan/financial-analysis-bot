# industry-analyst v4.0 — research-queries.md（Axis A-E 查詢模板，只給採集 agent）

> 本檔只在 spawn 採集 agent 時附給該 agent（見 SKILL.md【研究流程分級】模板①）；writer 本身寫稿不需通讀本檔。

## Axis A — 歷史（含 cycle 統計）

- `{theme} history evolution 1990 2000 2010 2020`、`{theme} technology generations`、`{theme} historical analog`
- `{theme} cycle length peak trough amplitude`、`{theme} stock price lead lag fundamentals`（cycle 統計表素材）
- 產出：appendix 歷史敘事＋cycle 統計表；mechanics 3.3（為什麼是現在）S 曲線素材，優先官方 roadmap。

## Axis B — 供給（利潤池、成本曲線、capex pipeline）

- `{theme} top suppliers 2026 market share`、`{theme} capex pipeline 2026 2027`、`{theme} capacity utilization`、`{theme} new entrants`
- `{theme} profit pool value chain margin distribution`（利潤池遷移）、`{theme} cost curve marginal producer`（成本曲線）
- 對每家關鍵玩家：WebFetch IR 頁抓最新簡報 → WebFetch SEC EDGAR 10-K/20-F 查業務組成 → WebSearch earnings transcript 找 commentary。
- 產出：mechanics 3.2 玩家矩陣（T1 source）＋利潤池表＋成本曲線。

## Axis C — 需求（TAM 推導鏈）

- `{theme} demand drivers 2026 end markets`、`{theme} TAM forecast 2030`、`{theme} customer concentration`、`{theme} demand inflection point`
- 回頭掃 Axis B 抓到的 IR deck 找 TAM 圖。
- 產出：mechanics 3.1 現需敘事＋TAM 三情境推導鏈。

## Axis D — 驗證（三角對帳、資本週期、priced-in、庫存指標）

- **需求三角對帳**：下游客戶 capex/採購 guidance（`{client} capex guidance 2026`）vs 上游廠商營收 consensus（`{supplier} revenue consensus 2026`）→ 對帳，差 >20% 找缺口。
- **資本週期指標**：`{theme} capex depreciation ratio`、`{theme} industry ROIC WACC`、`{theme} capacity lead time`。
- **sector 估值歷史分位**：`{sector} EV/Sales historical band`、`{sector} forward PE percentile cycle`（valuation 段 priced-in）。
- **庫存/訂單指標**：`{theme} book-to-bill`、`{theme} channel inventory weeks`、`{theme} backlog visibility`（軟體服務類找 NRR/RPO/billings）。
- 產出：mechanics 3.1 三角驗證、mechanics 3.4 資本週期證據＋庫存指標、valuation 段 priced-in 分位。

## Axis E — 替代與圈外掃描（機械化查詢，每項至少一輪，不得因「顯然無關」跳過）

- `{theme} China competitors open source alternative`、`{theme} 中國 替代 國產`
- `{theme} substitute technology disruption`、`{theme} leapfrog next generation`
- `{theme} in-house self-supply hyperscaler`（需求方自供／垂直整合）
- `{theme} regulation export control antitrust`（監管／地緣）
- 產出：debates 段替代威脅卡素材。**查無實質威脅時仍要回報**：「已掃描，現階段無一階威脅，判別訊號＝…」——掃描本身不可省，空白結論也是結論。

## 回傳格式（封閉式，禁推估）

每項證據回傳結構化格式：

```
{數字或事實}｜{來源 URL}｜{as-of 日期}｜{T1/T2/T3-A/T3-B/T3-C/T4}
```

查不到就回報「查不到」，**不得用訓練知識推估或以合理猜測代替**。彙整成一份證據包，按 Axis A-E 分節交回 writer。
