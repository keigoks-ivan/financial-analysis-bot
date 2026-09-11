# v19 WP-H1 交接（給 Codex 複審）

日期：2026-09-11。commit `1e5730591`（23 檔，+7,269／−21）。實作說明：`_v19_h1_impl_notes_20260911.md`。版面定案：`_v19_layout_spec_20260911.md`（H2 依此組頁）。未跑模型。

## 做了什麼

- **facts.json**：`scripts/dd_schema/facts.schema.json`＋`facts.md`＋零 LLM 抽取器 `scripts/dd_facts.py`。每條事實帶 id／值／期間・單位・口徑／來源定位／kind；`findings_digest[]` 不按方向裁（FIX：正 24／中 7／負 14／查無 3）；抽不到標 `needs_sonnet`。
- **v19 契約**：schema 頂層 `v19_contract`（判別 `meta.contract="v19"`），歸屬表 `judgment-v19.md`。`decision_inputs` 22 欄只留 9 欄 judge-owned，13＋2 欄投影；判斷者手填投影欄即 FAIL。
- **一處轉接** `scripts/dd_project.py`：25 條投影規則；validate／gen_dd_tables／dd_brief／dd_bundle gate／dd_delta 五處在載檔點接上；舊形狀 identity。程式只算不判：path_risk、capalloc_grade、moat 合併分可算；moat 等級／估值燈／品質分／signal／EPS 路徑／機率／Max DD 範圍由判斷者明示，缺即報缺。
- **終端年契約**：第 5 個完整會計年度；base_eps_path＝共識三年錨；v19 J2 年期 FAIL、舊形狀 WARN。
- **渲染**：brief 只維持相容；完整版路徑（section_map v19 對映、七表從投影視圖、`render_dd --assemble` 可組 v19 頁）。

## 驗收

舊格式 36 份 PASS／FAIL 與改前逐行相同（22 PASS／14 FAIL，含 J2 修好後揭露的既有數字缺口）；14 份 brief 逐 byte 相同；v19 fixture 投影後 0 FAIL；J1 14 條負向 finding 逐條可追（拔掉 refs 即逐條報回）；J2 真跑（Max DD 恆等式、終端年）；J6 讀得到前份；kill_metrics 4 條與 E12 拿得到致命指標；dd-meta 52 欄逐欄相同；pytest 311 passed（+21）。

## 請 Codex 裁定的三題

1. **`catalysts` 保留為可選頂層欄**（非純投影）：`judgment-to-ddmeta.md` 明文它與 triggers 是獨立居所；缺席才從帶日期的 triggers 投影。與計劃書第六節「其餘欄位由程式投影」有出入，是刻意取捨。
2. **required 沒降**（137→145，同尺 128）：多的 17 條是 `scenario_inputs`（v18 寫在 scenario.json 未計入）。再降只能砍情境輸入或六問四件式。H1 判斷「required 數不是目標，判斷段回合數與時間才是」——同意嗎？
3. **`moat.spread_table`／`competitors`／`checkpoints` 仍 judge-owned**：一半是事實，照 v19 該住 facts，但舊 schema `minItems` 綁著檢查語義。要不要在 H2 搬？

## 已知未接

`ddreport.py` 未接 dd_project（H2）；判斷 bundle 的 schema 速查仍舊形狀（H2 換 `judge.md.tmpl` 時一起切）；投影視圖 `_projected_from` 標記可能讓 J4 多收一個 token「19」。
