# 產業深度報告（Industry DD / ID）索引

由 `industry-analyst` skill v1.0 維護。每份 ID 為跨多檔個股共用的產業研究；公司 DD（`docs/dd/`）會在護城河 / 競爭 / 產業演進章節引用對應 ID。

**欄位說明**：
- **涵蓋 ticker 數**：§11 關聯個股清單總數
- **深度分布**：🔴 核心（營收 >40% 依賴）/ 🟡 次要（10-40%）/ 🟢 邊緣（<10%）
- **投資時鐘 Phase**：I（CAPEX 爆發）/ II（材料高毛利）/ III（封裝 / 應用端集中）
- **🟡 比例**：judgment bullet 占全篇 bullet 的比例（QC-I1 上限 20%）
- **鮮度**：tech（§1-§3，半衰期 365 天）/ market（§4-§6、§10.5，90 天）/ judgment（§8-§13，60 天）
  - 🟢 在半衰期內 ｜ 🟡 tech 過期 ｜ 🟠 market 過期 ｜ 🔴 judgment 過期（建議刷新）

---

| 日期 | 主題 | 涵蓋 ticker | 深度分布 | Phase | 🟡 比例 | 鮮度 | 檔名 | 備註 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 2026-04-19 | 先進封裝（Advanced Packaging）| 10 | 4🔴 / 4🟡 / 2🟢 | I → II 轉換期 | 18% | tech 🟢 / market 🟢 / judgment 🟢 | ID_AdvancedPackaging_20260419.html | 首篇；CoWoS / SoIC / CoPoS / hybrid bonding 四主軸 |
| 2026-04-19 | AI 加速器需求（AI Accelerator Demand）🔴 母題 | 12 | 5🔴 / 5🟡 / 2🟢 | Phase II（訓練→推論混合期）| 19% | tech 🟢 / market 🟢 / judgment 🟢 | ID_AIAcceleratorDemand_20260419.html | 母題 Root ID；涵蓋 NVDA / AVGO / AMD / MRVL / 2330 / ASML / GOOGL / META / MSFT / AMZN / CRDO / ANET；3 條非共識：ASIC 份額 35-40%（vs 共識 20-25%）、2027 非峰值為轉折、電力永久瓶頸重塑 FLOPS/W 競爭 |
| 2026-04-19 | HBM 記憶體超級循環（HBM Supercycle）| 7 | 3🔴 / 2🟡 / 2🟢 | Phase II（擴產 + 緊供給）| 17% | tech 🟢 / market 🟢 / judgment 🟢 | ID_HBM_Supercycle_20260419.html | 涵蓋 MU / SK hynix / Samsung / NVDA / AMD / ASML / 2330；3 條非共識：Samsung HBM4 份額 35%（vs 共識 25%）、HBM 已脫離 DRAM 週期不會 2028 crash、TSMC 透過 HBM4 base die 成隱性贏家 |
