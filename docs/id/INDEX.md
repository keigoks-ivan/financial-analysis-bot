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
| 2026-04-19 | 先進製程節點（Leading Edge Node）| 9 | 4🔴 / 3🟡 / 2🟢 | Phase II（2nm 爆發 + A16 起點）| 18% | tech 🟢 / market 🟢 / judgment 🟢 | ID_LeadingEdgeNode_20260419.html | 涵蓋 2330 / ASML / AMAT / LRCX / KLAC / NVDA / AMD / INTC / Samsung；3 條非共識：Samsung 2nm 2028 市佔 15%+（vs 共識 7-10%）、Intel 18A 2026-2027 基本無外部客戶、TSMC A16 backside power 是真正 2027-2028 護城河 |
| 2026-04-19 | AI 網路互連（AI Networking）| 9 | 4🔴 / 3🟡 / 2🟢 | Phase II（Ethernet 逆襲 + UALink 規格完成）| 18% | tech 🟢 / market 🟢 / judgment 🟢 | ID_AINetworking_20260419.html | 涵蓋 NVDA / AVGO / CRDO / MRVL / ANET / COHR / APH / LITE / FN；3 條非共識：Scale-up / Scale-out 非 zero-sum、UALink 商用 2027+ 非 2026、CRDO + ALAB 連接器稀缺被低估 |
| 2026-04-19 | AI 資料中心基建（AI Data Center）| 7 | 3🔴 / 2🟡 / 2🟢 | Phase II（基建爆發 + 電力瓶頸）| 19% | tech 🟢 / market 🟢 / judgment 🟢 | ID_AIDataCenter_20260419.html | 涵蓋 VRT / ETN / GEV / HWM / ROK / NuScale / Schneider；3 條非共識：VRT 比 NVDA 更安全 AI pure play、GEV gas turbine 不是過渡是 2030+ 主力、ETN Boyd Thermal 是結構轉型 |
| 2026-04-19 | 矽光子 / CPO（Silicon Photonics / CPO）| 8 | 3🔴 / 3🟡 / 2🟢 | Phase I 末（首批量產）| 19% | tech 🟢 / market 🟢 / judgment 🟢 | ID_SiliconPhotonicsCPO_20260419.html | 涵蓋 NVDA / 2330 / COHR / LITE / AVGO / MRVL / FN / GFS；3 條非共識：CPO 2026 H2 已商用（比共識早 2-3 年）、pluggable + CPO 並存（LITE/COHR 不淘汰）、TSMC COUPE 重演 CoWoS 獨家 |
| 2026-04-19 | Data Center 液冷（Liquid Cooling）| 8 | 3🔴 / 3🟡 / 2🟢 | Phase II（滲透擴張）| 18% | tech 🟢 / market 🟢 / judgment 🟢 | ID_LiquidCooling_20260419.html | 涵蓋 VRT / ETN / Asetek / Nidec / Schneider / PH / Trane / Chemours；3 條非共識：CDU 是真正瓶頸、Immersion 2028+ 超越 DTC、Asetek 被低估的 AI 液冷 pure play |
| 2026-04-19 | AI DC 變壓器（Power Transformers）| 9 | 4🔴 / 3🟡 / 2🟢 | Phase II 後期（5 年 lead time + 800V DC 換代）| 19% | tech 🟢 / market 🟢 / judgment 🟢 | ID_Transformers_20260419.html | 涵蓋 Hitachi（6501.T）/ Siemens Energy / GEV Prolec / ETN / ABB / Schneider / PWR / Mitsubishi / Hyundai；3 條非共識：變壓器 5 年 lead time 是比晶片更硬的 bottleneck、Eaton 800V DC SST 是被低估的 AI 共設計夥伴、GEV Prolec 是被 gas turbine 熱度蓋過的 pure play；AI DC 子題（Gate 7 通過）|
| 2026-04-19 | AI ASIC 設計服務供應鏈（Custom AI Silicon）| 11 | 4🔴 / 4🟡 / 3🟢 | Phase II（爆發期 + 玩家分化） | 19% | tech 🟢 / market 🟢 / judgment 🟢 | ID_AIASICDesignService_20260419.html | 涵蓋 AVGO / MRVL / 3661 Alchip / 3443 GUC / 2454 MediaTek / Socionext / GOOGL / AMZN / MSFT / META / NVDA；3 條非共識：hyperscaler ASIC 2028 市占 40%+（vs 共識 20-25%）、台系 Alchip + MediaTek 2028 合計超越 MRVL（22% vs 共識 10-12%）、AVGO 2027+ 毛利壓縮至 40-45%（vs 共識維持 50%）；AI Accelerator 母題子章節 |
| 2026-04-20 | 玻璃基板封裝（Glass Substrate Packaging）| 11 | 4🔴 / 4🟡 / 3🟢 | Phase I 末 → II 初（Intel 全球首款量產） | 19% | tech 🟢 / market 🟢 / judgment 🟢 | ID_GlassSubstrate_20260420.html | 涵蓋 INTC / LPK.DE / 011790.KS SKC / GLW / 5201.T AGC / 2330 TSMC / 3037 Unimicron / AMD / 005930 Samsung / 6146 DISCO / 5214 NEG；3 條非共識：Intel 真正護城河是 glass substrate（非 18A）、LPKF 類比 2015 ASML（LIDE 獨家到 2035）、glass 2028 佔 AP 15%（共識 5-8%）；先進封裝子題，觸發 AP thesis #2 + LEN thesis #2 patch |
| 2026-04-20 | Hybrid Bonding / SoIC（3D IC 整合）| 11 | 4🔴 / 4🟡 / 3🟢 | Phase II（HVM 量產期 + 設備寡占化）| 19% | tech 🟢 / market 🟢 / judgment 🟢 | ID_HybridBondingSoIC_20260420.html | 涵蓋 BESI.AS / ADEA Adeia / AMAT / 2330 TSMC / INTC / 0522 ASMPT / MU / AMD / AAPL / 005930 Samsung / 000660 SK Hynix；3 條非共識：Adeia 是 Dolby-style 隱性收費 royalty 玩家、BESI+AMAT 是 ASML-like 設備寡占雛形、Intel Foveros 落後 TSMC 2 年且毛利被 Adeia 稀釋；深化 AP thesis #1（BESI 類比 ASML）從預測到已兌現 |
