# ID judgment refresh 優先序隊列（2026-07-17 建）

**背景**：v2.3 regen 專案（semi＋nonsemi 全部 waves）已全數完成——nonsemi B/C/D/E 由視窗 B 於 2026-06-21 收官、Wave G 於 2026-06-29 以新日期檔收官（見 `_v23_nonsemi_manifest.md` 2026-07-17 對帳更正）。**下一個真實工作不是 regen，是 60 天 judgment 過期潮**：6/21 cohort 於 **2026-08-20** 同日過期、6/29 cohort 於 **2026-08-28** 過期。本隊列供屆時分批 refresh 排程，避免一次爆量。

**方法**：機械掃描全部 canonical id-meta（排除 stub/superseded；同 theme 取最新日期檔），優先級＝
- **P0＝持倉鏈結**（related_tickers ∩ 三軌可執行名單 NVDA/TSM/AVGO/GOOGL/LLY/PLTR/COHR/APH）
- **P1＝conviction high**（無持倉鏈結）
- **P2＝循環候選鏈結**（∩ cyclical-track 候選）／**P3＝其餘**

**統計**：P0 32 篇｜P1 30 篇｜P2 3 篇｜P3 15 篇（共 80 篇 active canonical）。

**建議排程**（refresh＝judgment 段更新＋機器欄複核，非全文 regen；走 id-review 或 industry-analyst 增量路徑）：
- 8 月第 1 週起每週 8–10 篇，P0 先行（過期日 8/19–20 前清完 P0）；
- P1 排 8 月第 2–3 週；P2/P3 過期後按需，不趕潮。
- 有實際動部位意圖的主題隨時插隊（決策時 critic 規則本來就會觸發深讀）。

## P0 — 持倉鏈結（32 篇）

| 檔案 | conviction | judgment 刷新日 | 60 天到期 | 持倉鏈結 | 循環候選鏈結 |
|---|---|---|---|---|---|
| ID_AIComputeCapexCycle_20260611.html | high | 2026-06-11 | 2026-08-10 | AVGO、GOOGL、NVDA、TSM | MU、ORCL |
| ID_AIAcceleratorDemand_20260419.html | mid | 2026-06-20 | 2026-08-19 | AVGO、GOOGL、NVDA | — |
| ID_AIInferenceEconomics_20260430.html | high | 2026-06-20 | 2026-08-19 | AVGO、GOOGL、NVDA | NET |
| ID_AdvancedPackaging_20260419.html | mid | 2026-06-20 | 2026-08-19 | AVGO、NVDA | CRDO |
| ID_CUDARocmMoat_20260501.html | high | 2026-06-20 | 2026-08-19 | AVGO、GOOGL、NVDA | — |
| ID_HBM_Supercycle_20260419.html | mid | 2026-06-20 | 2026-08-19 | NVDA | MU |
| ID_AIAdRetailMedia_20260429.html | high | 2026-06-21 | 2026-08-20 | GOOGL | — |
| ID_AICrossDomainImpact_20260429.html | high | 2026-06-21 | 2026-08-20 | GOOGL、NVDA、PLTR | — |
| ID_AIEDAIP_20260427.html | high | 2026-06-21 | 2026-08-20 | AVGO、NVDA | — |
| ID_AINetworking_20260419.html | mid | 2026-06-21 | 2026-08-20 | APH、AVGO、COHR、NVDA | CRDO |
| ID_AgenticAIPlatform_20260424.html | high | 2026-06-21 | 2026-08-20 | GOOGL、PLTR | NET |
| ID_AppleIntelligencePlatformThreat_20260429.html | high | 2026-06-21 | 2026-08-20 | GOOGL | — |
| ID_CybersecurityPlatformConsolidation_20260423.html | high | 2026-06-21 | 2026-08-20 | GOOGL | NET |
| ID_DataSecurityBackupConvergence_20260423.html | high | 2026-06-21 | 2026-08-20 | GOOGL | NET |
| ID_DefenseModernization_20260430.html | high | 2026-06-21 | 2026-08-20 | PLTR | — |
| ID_EdgeAI_20260427.html | mid | 2026-06-21 | 2026-08-20 | NVDA | — |
| ID_FoundryGeography_20260427.html | high | 2026-06-21 | 2026-08-20 | NVDA | — |
| ID_GLP1Master_20260429.html | high | 2026-06-21 | 2026-08-20 | LLY | — |
| ID_GLP1RestaurantImpact_20260427.html | high | 2026-06-21 | 2026-08-20 | LLY | — |
| ID_GLP1Treatment_20260428.html | high | 2026-06-21 | 2026-08-20 | LLY | — |
| ID_HumanoidIndustrialRobotics_20260427.html | mid | 2026-06-21 | 2026-08-20 | NVDA | — |
| ID_HyperscalerCloudBigThree_20260505.html | high | 2026-06-21 | 2026-08-20 | AVGO、GOOGL、NVDA | ORCL |
| ID_IdentityNewPerimeter_20260423.html | high | 2026-06-21 | 2026-08-20 | GOOGL | NET |
| ID_LLMVendorSecurityEconomics_20260423.html | high | 2026-06-21 | 2026-08-20 | GOOGL、NVDA | NET |
| ID_LeadingEdgeNode_20260419.html | high | 2026-06-21 | 2026-08-20 | NVDA | — |
| ID_OTAandAITravel_20260429.html | mid | 2026-06-21 | 2026-08-20 | GOOGL | — |
| ID_ProductivityCopilot_20260427.html | high | 2026-06-21 | 2026-08-20 | GOOGL | — |
| ID_PublishersStructuralReset_20260430.html | high | 2026-06-21 | 2026-08-20 | GOOGL | — |
| ID_QuantumComputing_20260427.html | mid | 2026-06-21 | 2026-08-20 | COHR、GOOGL、NVDA | — |
| ID_RobotaxiAutonomous_20260429.html | mid | 2026-06-21 | 2026-08-20 | NVDA | — |
| ID_TokenEconomics_20260427.html | high | 2026-06-21 | 2026-08-20 | AVGO、GOOGL、NVDA | NET |
| ID_SpaceEconomy_20260629.html | mid | 2026-06-29 | 2026-08-28 | NVDA | — |

## P1 — conviction high（30 篇）

| 檔案 | conviction | judgment 刷新日 | 60 天到期 | 持倉鏈結 | 循環候選鏈結 |
|---|---|---|---|---|---|
| ID_AICybersecurityDoubleEdge_20260423.html | high | 2026-06-21 | 2026-08-20 | — | NET |
| ID_AIDCPowerElectronics_20260421.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_AIDataCenter_20260419.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_ApparelFootwear_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_AthleisureNewEntrants_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_AthleticFootwearSubsegments_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_BeverageEnergyDrink_20260428.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_BoomerTravelSupercycle_20260429.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_CardNetworkDuopoly_20260428.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_CasinoGamingIR_20260429.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_ChannelPowerReversion_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_ChinaSportswearRise_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_CobrandCardEcosystem_20260429.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_CommercialAerospace_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_DiscountRetailKShape_20260430.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_FastCasualBifurcation_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_GlobalBankROE_20260428.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_GlobalEcommerce_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_GlobalLuxury_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_HeavyMachineryMining_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_HotelChains_20260429.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_LATAMEcommerce_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_LiquidCooling_20260419.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_LuxuryTravelCruise_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_NuclearRenaissance_20260430.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_RestaurantTechSaaS_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_StablecoinPayments_20260430.html | high | 2026-06-21 | 2026-08-20 | — | HOOD、SOFI |
| ID_USRestaurantChains_20260427.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_WaferFabEquipment_20260430.html | high | 2026-06-21 | 2026-08-20 | — | — |
| ID_DataCenterREITDuopoly_20260629.html | high | 2026-06-29 | 2026-08-28 | — | — |

## P2/P3 — 其餘（18 篇）

| 檔案 | conviction | judgment 刷新日 | 60 天到期 | 持倉鏈結 | 循環候選鏈結 |
|---|---|---|---|---|---|
| ID_AIStorage_20260427.html | mid | 2026-06-21 | 2026-08-20 | — | MU、WDC |
| ID_HybridBondingSoIC_20260420.html | mid | 2026-06-21 | 2026-08-20 | — | MU |
| ID_MemorySupercycle_20260430.html | mid | 2026-06-21 | 2026-08-20 | — | MU、WDC |
| ID_AerospaceMetals_20260427.html | mid | 2026-06-21 | 2026-08-20 | — | — |
| ID_AirlineLoyaltyRepricing_20260429.html | mid | 2026-06-21 | 2026-08-20 | — | — |
| ID_CasualDiningTurnaround_20260427.html | mid | 2026-06-21 | 2026-08-20 | — | — |
| ID_CopperSupercycle_20260428.html | mid | 2026-06-21 | 2026-08-20 | — | — |
| ID_FusionCommercialization_20260505.html | mid | 2026-06-21 | 2026-08-20 | — | — |
| ID_GLP1PackagedFood_20260428.html | mid | 2026-06-21 | 2026-08-20 | — | — |
| ID_GlassSubstrate_20260420.html | mid | 2026-06-21 | 2026-08-20 | — | — |
| ID_HydrogenFuelCell_20260505.html | mid | 2026-06-21 | 2026-08-20 | — | — |
| ID_IndustrialAutomation_20260427.html | mid | 2026-06-21 | 2026-08-20 | — | — |
| ID_WealthTransfer25Year_20260429.html | mid | 2026-06-21 | 2026-08-20 | — | — |
| ID_BeefSupercycle_20260629.html | mid | 2026-06-29 | 2026-08-28 | — | — |
| ID_PublicBuilderEntryLevel_20260629.html | mid | 2026-06-29 | 2026-08-28 | — | — |
| ID_FertilizerSeeds_20260629.html | mid | 2026-06-29 | 2026-08-28 | — | — |
| ID_GrainsOilseeds_20260629.html | mid | 2026-06-29 | 2026-08-28 | — | — |
| ID_BackEndPackagingEquipment_20260702.html | mid | 2026-07-02 | 2026-08-31 | — | — |

---
產生方式：id-meta 機械掃描（本檔手跑重生即可更新；scratchpad 腳本邏輯內嵌於 2026-07-17 session）。
