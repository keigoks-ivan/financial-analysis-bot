# ID Taxonomy — 大類別 × 子群組對照表

**用途**：industry-analyst skill 在生成新 ID 時，必須從本檔的「controlled vocabulary」選擇 `mega` × `sub_group` 標籤；index.html 內每個 sub_group 都有對應的 HTML anchor comment（如 `<!-- subgroup-anchor: semi.memory -->`），新 ID 卡片自動插入到該 anchor 之後。

**規則**：
- `mega` 必須從本檔表 1 選擇（15 個大類別）
- `sub_group` 必須從本檔表 2 選擇（每個大類別內的子群組）
- 若 ID 跨 mega（如 GLP1RestaurantImpact 跨 bio + staples），主 mega 為「下游受影響」端
- 子群組目前若沒有 ID（empty），index.html 內保留 anchor，未來自動填入
- 新增子群組時，需更新本檔 + index.html anchor

---

## 表 1：15 大類別（Mega-sections）

| `mega` 標籤 | data-cat | 中文標題 | icon | hint |
|:---|:---|:---|:---|:---|
| `semi` | semi | 半導體 / AI 基建 | 🔷 | AI Accelerator / 封裝 / 記憶體 / 製程 / 互連 |
| `bio` | bio | 生技 / 醫療 | 🧬 | GLP-1 / 基因治療 / 醫材 / 數位健康 |
| `cloud` | cloud | 雲端 / SaaS / 軟體 | ☁️ | 資安 / Agentic AI / Token / 媒體 SaaS |
| `energy` | energy | 能源 / 電動車 / 新能源 | ⚡ | 核能 / EV / 太陽風能 / 油氣 |
| `consumer` | consumer | 消費 / 零售 / 精品 | 🛍️ | 服飾 / 餐飲 / 奢侈品 / E-commerce |
| `finance` | finance | 金融 / 保險 / FinTech | 🏦 | 支付 / 銀行 / Stablecoin / 財富 |
| `industrial` | industrial | 工業 / 航太 / 自動化 | 🔧 | 國防 / 機器人 / 重機 / 自駕 |
| `staples` | consumer (legacy) | 必選消費 / 飲料 / 個護 | 🥫 | 飲料 / 包裝食品 / 個護 |
| `reits` | reits | REITs / 數位基建房東 | 🏢 | 數位基建 / 倉儲 / 老人公寓 |
| `space` | space | 太空經濟 / 衛星 / 低軌道 | 🛰️ | 衛星 / Launch / 太空材料 |
| `housing` | housing | 住房 / 房貸 / Builders | 🏠 | 美國 builders / 海外房產 / 房貸 |
| `transport` | transport | 運輸 / 物流 / 航運 / 旅遊 | ✈️ | 航空 / 海運 / 鐵路 / 旅遊 / 賭博 |
| `materials` | materials | 材料 / 礦業 / 特殊化學 | ⛏️ | 銅 / 鋰 / 鋼鐵 / 化工 / 稀土 |
| `agri` | agri | 農業 / 食品 / 大宗商品 | 🌾 | 牛肉 / 穀物 / 漁業 / 肥料 |
| `macro` | macro | 跨域 / 地緣 / 其他 | 🌐 | 地緣政治 / 跨域影響 |

---

## 表 2：子群組（Sub-groups within each mega）

### `semi` 半導體 / AI 基建（11 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `semi.compute_demand` | AI 需求 / Compute Demand | AIInferenceEconomics(★), AIAcceleratorDemand(P), AIASICDesignService | 需求源頭 |
| `semi.memory` | 記憶體 / Memory | MemorySupercycle(P), HBM_Supercycle | DRAM + NAND + HBM |
| `semi.storage` | 儲存 / Storage | AIStorage | SSD / NVMe |
| `semi.networking` | 互連 / Networking | AINetworking(P), SiliconPhotonicsCPO | switch + CPO + 光模組 |
| `semi.dc_infra` | AI DC 基建 / Power | AIDataCenter(P), LiquidCooling, Transformers, AIDCPowerElectronics | 散熱 + 電力 + 變壓器 |
| `semi.advanced_packaging` | 先進封裝 | AdvancedPackaging(P), GlassSubstrate, HybridBondingSoIC | CoWoS + SoIC + glass |
| `semi.foundry_process` | 製程 / Foundry | LeadingEdgeNode, FoundryGeography | 2nm + CHIPS Act |
| `semi.equipment_test` | 設備 / 測試 | WaferFabEquipment(P), AITestEquipmentATE | WFE 五寡占 + ATE |
| `semi.eda_ip` | 設計工具 / EDA & IP | AIEDAIP | Synopsys + Cadence + ARM |
| `semi.edge_ai` | 邊緣 / 端側 AI | EdgeAI | NPU + 端側推論 |
| `semi.emerging_compute` | 量子 / 新興運算 | QuantumComputing | Quantum + Neuromorphic |

### `bio` 生技 / 醫療（7 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `bio.glp1` | GLP-1 / 代謝藥物 | GLP1Master(P), GLP1Treatment | LLY / NVO 母題 |
| `bio.gene_cell` | 基因治療 / 細胞治療 | (空) | CRISPR / CAR-T |
| `bio.medical_device` | 醫材 / 設備 | (空) | 心導管 / 影像 / 透析 |
| `bio.cdmo_cro` | CDMO / CRO 服務 | (空) | Catalent / Lonza / Charles River |
| `bio.digital_health` | 數位健康 / 遠距醫療 | (空) | Teladoc / Hims |
| `bio.hospital_chain` | 醫院 / 連鎖診所 | (空) | UNH / HCA |
| `bio.china_pharma` | 中國 / 印度藥企 | (空) | 中國本土創新藥 |

### `cloud` 雲端 / SaaS / 軟體（7 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `cloud.cybersecurity` | 資安 SaaS | CybersecurityPlatformConsolidation(P), AICybersecurityDoubleEdge, IdentityNewPerimeter, DataSecurityBackupConvergence, LLMVendorSecurityEconomics | CRWD / PANW / ZS / NET |
| `cloud.agentic_ai` | AI Agent / Agentic AI | AgenticAIPlatform(P), AgenticAICommercialization, TokenEconomics, ProductivityCopilot | PLTR / CRM Agentforce |
| `cloud.ai_cross_domain` | AI 跨域影響 / Platform Threats | AICrossDomainImpact, AppleIntelligencePlatformThreat, AIAdRetailMedia | GOOGL AI Overview / WWDC Siri |
| `cloud.media_publishing` | 媒體 / 出版 SaaS | PublishersStructuralReset | NYT / DJCO / Substack |
| `cloud.vertical_saas` | Vertical SaaS | (空，已部分散落) | WDAY / NOW / INTU |
| `cloud.devops_data` | DevOps / Data Platform | (空) | DDOG / SNOW / MDB |
| `cloud.communication` | 通訊 SaaS | (空) | TWLO / ZM / TEAM |

### `energy` 能源 / 電動車 / 新能源（8 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `energy.nuclear` | 核能 / SMR / Fusion | NuclearRenaissance | OKLO / SMR / NNE |
| `energy.solar` | 太陽能 | (空) | FSLR / ENPH |
| `energy.wind` | 風能 | (空) | VWS / 6505 等 |
| `energy.hydrogen` | 氫能 / 燃料電池 | (空) | PLUG / BLDP |
| `energy.ev_oem` | EV 整車 | (空) | TSLA / BYD / Rivian |
| `energy.battery_metals` | 電池 / 上游金屬（鋰鎳鈷） | (空，部分跨 materials) | ALB / SQM |
| `energy.oil_gas` | 油氣 traditional | (空) | XOM / CVX |
| `energy.utilities` | 公用事業 / Grid | (空) | NEE / SO |

### `consumer` 消費 / 零售 / 精品（7 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `consumer.apparel` | 服飾 / 鞋類 | ApparelFootwear(P), AthleticFootwearSubsegments, AthleisureNewEntrants, ChannelPowerReversion, ChinaSportswearRise | NKE / LULU / DECK / ONON |
| `consumer.luxury` | 奢侈品 | GlobalLuxury | LVMH / Hermes / Kering |
| `consumer.restaurant` | 餐飲 / 連鎖 | USRestaurantChains(P), FastCasualBifurcation, CasualDiningTurnaround, RestaurantTechSaaS | CMG / SBUX / TOST |
| `consumer.discount_retail` | 折扣 / 百貨零售 | DiscountRetailKShape | DG / DLTR / WMT / TGT |
| `consumer.ecommerce` | E-commerce | GlobalEcommerce, LATAMEcommerce | AMZN / SHOP / MELI / SE |
| `consumer.fitness_personal` | 健身 / 個護 | (空) | PTON / 化妝品 |
| `consumer.home_furniture` | 家居 / 家具 | (空) | RH / W |

### `finance` 金融 / 保險 / FinTech（7 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `finance.payment_network` | 支付網路 | CardNetworkDuopoly, CobrandCardEcosystem | V / MA / AXP |
| `finance.banks` | 銀行 / 大行 ROE | GlobalBankROE | JPM / BAC / 歐洲日本大行 |
| `finance.stablecoin` | Stablecoin / Crypto | StablecoinPayments | CRCL / Tether |
| `finance.wealth_mgmt` | 財富管理 / 跨代轉移 | WealthTransfer25Year | MS / SCHW / NTRS |
| `finance.insurance` | 保險 | (空) | BRK / PGR / TRV |
| `finance.asset_mgmt_pe` | 資管 / PE / 私募信貸 | (空) | BX / BLK / KKR / APO |
| `finance.fintech_lending` | Fintech 借貸 / BNPL | (空) | SOFI / AFRM / NU |

### `industrial` 工業 / 航太 / 自動化（7 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `industrial.defense` | 國防 / 防務 | DefenseModernization(P), DefenseAerospaceUpgrade | LMT / RTX / NOC / RHM |
| `industrial.commercial_aero` | 商用航太 | CommercialAerospace | BA / GE Aero |
| `industrial.robotics` | 機器人 / 自動化 | HumanoidIndustrialRobotics, IndustrialAutomation | TSLA Optimus / FANUC / ROK |
| `industrial.heavy_machinery` | 重機械 / 礦機 / 農機 | HeavyMachineryMining | CAT / DE / Komatsu |
| `industrial.autonomous_driving` | 自動駕駛 / Robotaxi | RobotaxiAutonomous | Waymo / TSLA FSD |
| `industrial.hvac_electrical` | HVAC / 工業電氣 | (空) | CARR / TT / AOS |
| `industrial.engineering_construction` | 工程承包 | (空) | EME / PWR |

### `staples` 必選消費 / 飲料 / 個護（6 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `staples.beverage` | 飲料 / 能量飲 | BeverageEnergyDrink | KO / PEP / MNST / CELH |
| `staples.packaged_food` | 包裝食品（含 GLP-1 衝擊） | GLP1PackagedFood | MDLZ / KHC / HSY |
| `staples.restaurant_glp1` | 餐飲 GLP-1 cross | GLP1RestaurantImpact | (餐飲被 GLP-1 影響） |
| `staples.alcohol_tobacco` | 菸酒 | (空) | DEO / BUD / MO |
| `staples.personal_care_beauty` | 個護 / 美妝 | (空) | PG / EL / CL |
| `staples.household_products` | 家用品 / 紙品 | (空) | KMB / CHD |

### `reits` REITs / 數位基建房東（5 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `reits.data_center` | 數位基建 REIT | DataCenterREITDuopoly | EQIX / DLR |
| `reits.industrial_logistics` | 物流 / 倉儲 REIT | (空) | PLD / EQT |
| `reits.retail_mall` | 零售 / 購物中心 | (空) | SPG / O |
| `reits.healthcare_senior` | 醫療 / 老人公寓 | (空) | WELL / VTR |
| `reits.cell_tower` | 電塔 REIT | (空) | AMT / CCI / SBAC |

### `space` 太空經濟 / 衛星（4 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `space.launch` | Launch / 衛星發射 | SpaceEconomy | RKLB / SpaceX |
| `space.satellite_comm` | 衛星通訊 / EO | (空) | IRDM / VIA / BKSY |
| `space.space_materials` | 太空材料 / 結構件 | (空) | (overlap with industrial) |
| `space.defense_space` | 太空軍 / 軍用衛星 | (空) | NOC SDA / LMT |

### `housing` 住房 / 房貸 / Builders（4 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `housing.us_builders` | 美國 builders | PublicBuilderEntryLevel | DHI / LEN / NVR |
| `housing.intl_property` | 海外房地產 | (空) | China / Japan / EU |
| `housing.mortgage_mbs` | 房貸 / MBS | (空) | NMR / RKT |
| `housing.land_development` | 土地開發商 | (空) | (overlap） |

### `transport` 運輸 / 物流 / 航運 / 旅遊（7 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `transport.travel_master` | 旅遊母題 / Cross-vertical | BoomerTravelSupercycle(P) | demographic 母題 |
| `transport.hotel_lodging` | 連鎖旅館 / Hospitality | HotelChains | MAR / HLT / H |
| `transport.cruise_luxury_travel` | 郵輪 / 豪華旅遊 | LuxuryTravelCruise | RCL / NCLH / VIK |
| `transport.ota_distribution` | OTA / AI 分發 | OTAandAITravel | BKNG / EXPE / ABNB |
| `transport.airline` | 航空 / loyalty | AirlineLoyaltyRepricing | DAL / UAL / AXP cobrand |
| `transport.casino_gaming` | 賭場 / IR | CasinoGamingIR | LVS / MGM / WYNN |
| `transport.shipping_freight` | 海運 / 鐵路 / 卡車 / 物流 | (空) | UPS / FDX / 海運 |

### `materials` 材料 / 礦業 / 特殊化學（8 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `materials.industrial_metals` | 工業金屬 / 銅鋁 | CopperSupercycle | FCX / BHP |
| `materials.aerospace_defense_metals` | 航太 / 國防金屬 | AerospaceMetals | HWM / ATI / CRS |
| `materials.battery_metals` | 鋰鎳鈷電池金屬 | (空) | ALB / SQM |
| `materials.steel` | 鋼鐵 | (空) | NUE / STLD |
| `materials.precious_metals` | 貴金屬 / 黃金 | (空) | NEM / Barrick |
| `materials.specialty_chemicals` | 特殊化學 | (空) | LIN / APD |
| `materials.cement_construction` | 水泥 / 建材 | (空) | VMC / MLM |
| `materials.rare_earth` | 稀土 | (空，部分在 CNTW S8) | MP / Lynas |

### `agri` 農業 / 食品供應鏈（5 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `agri.livestock_meat` | 牛肉 / 家畜 | BeefSupercycle | TSN / Cargill |
| `agri.grains_oilseeds` | 穀物 / 油籽 / 糧食 | (空) | ADM / BG |
| `agri.fishery_aqua` | 漁業 / 水產 | (空) | (NWE) |
| `agri.fertilizer_seeds` | 肥料 / 種子 | (空) | NTR / MOS / Bayer |
| `agri.farm_equipment` | 農機（連 industrial.heavy） | (空，跨指 7.4) | DE / AGCO |

### `macro` 跨域 / 地緣（4 子群組）

| `sub_group` | 中文標題 | 現存 ID | 邏輯 |
|:---|:---|:---|:---|
| `macro.geopolitics_cntw` | 中台地緣 / 兩岸 | CNTW_Master + S1-S10 | 11 份系列 |
| `macro.geopolitics_other` | 其他地緣（俄烏 / 中東） | (空) | future Russia / Iran etc |
| `macro.demographics` | 人口 / 世代議題 | (overlap with transport.travel_master) | Boomer / Gen Z |
| `macro.thematic_other` | 其他主題 | (空) | catch-all |

---

## 表 3：ID 完整對照（89 IDs → mega.sub_group）

| ID 檔名 | mega | sub_group | 角色 |
|:---|:---|:---|:---|
| AIAcceleratorDemand | semi | compute_demand | parent |
| AIASICDesignService | semi | compute_demand | child |
| AIInferenceEconomics | semi | compute_demand | standalone ★ |
| MemorySupercycle | semi | memory | parent |
| HBM_Supercycle | semi | memory | child（重整為） |
| AIStorage | semi | storage | standalone |
| AINetworking | semi | networking | parent |
| SiliconPhotonicsCPO | semi | networking | child |
| AIDataCenter | semi | dc_infra | parent |
| LiquidCooling | semi | dc_infra | child |
| Transformers | semi | dc_infra | child |
| AIDCPowerElectronics | semi | dc_infra | child |
| AdvancedPackaging | semi | advanced_packaging | parent |
| GlassSubstrate | semi | advanced_packaging | child |
| HybridBondingSoIC | semi | advanced_packaging | child |
| LeadingEdgeNode | semi | foundry_process | standalone |
| FoundryGeography | semi | foundry_process | standalone |
| WaferFabEquipment | semi | equipment_test | parent |
| AITestEquipmentATE | semi | equipment_test | standalone |
| AIEDAIP | semi | eda_ip | standalone |
| EdgeAI | semi | edge_ai | standalone |
| QuantumComputing | semi | emerging_compute | standalone |
| GLP1Master | bio | glp1 | master |
| GLP1Treatment | bio | glp1 | sub |
| CybersecurityPlatformConsolidation | cloud | cybersecurity | parent |
| AICybersecurityDoubleEdge | cloud | cybersecurity | child |
| IdentityNewPerimeter | cloud | cybersecurity | child |
| DataSecurityBackupConvergence | cloud | cybersecurity | child |
| LLMVendorSecurityEconomics | cloud | cybersecurity | child |
| AgenticAIPlatform | cloud | agentic_ai | parent |
| AgenticAICommercialization | cloud | agentic_ai | standalone |
| TokenEconomics | cloud | agentic_ai | standalone |
| ProductivityCopilot | cloud | agentic_ai | standalone |
| AICrossDomainImpact | cloud | ai_cross_domain | standalone |
| AppleIntelligencePlatformThreat | cloud | ai_cross_domain | standalone |
| AIAdRetailMedia | cloud | ai_cross_domain | standalone |
| PublishersStructuralReset | cloud | media_publishing | standalone |
| NuclearRenaissance | energy | nuclear | master |
| ApparelFootwear | consumer | apparel | parent |
| AthleticFootwearSubsegments | consumer | apparel | child |
| AthleisureNewEntrants | consumer | apparel | child |
| ChannelPowerReversion | consumer | apparel | child |
| ChinaSportswearRise | consumer | apparel | child |
| GlobalLuxury | consumer | luxury | standalone |
| USRestaurantChains | consumer | restaurant | parent |
| FastCasualBifurcation | consumer | restaurant | child |
| CasualDiningTurnaround | consumer | restaurant | child |
| RestaurantTechSaaS | consumer | restaurant | child |
| DiscountRetailKShape | consumer | discount_retail | standalone |
| GlobalEcommerce | consumer | ecommerce | standalone |
| LATAMEcommerce | consumer | ecommerce | standalone |
| CardNetworkDuopoly | finance | payment_network | standalone |
| CobrandCardEcosystem | finance | payment_network | standalone |
| GlobalBankROE | finance | banks | standalone |
| StablecoinPayments | finance | stablecoin | standalone |
| WealthTransfer25Year | finance | wealth_mgmt | standalone |
| DefenseModernization | industrial | defense | master |
| DefenseAerospaceUpgrade | industrial | defense | sub |
| CommercialAerospace | industrial | commercial_aero | standalone |
| HumanoidIndustrialRobotics | industrial | robotics | standalone |
| IndustrialAutomation | industrial | robotics | standalone |
| HeavyMachineryMining | industrial | heavy_machinery | standalone |
| RobotaxiAutonomous | industrial | autonomous_driving | standalone |
| BeverageEnergyDrink | staples | beverage | standalone |
| GLP1PackagedFood | staples | packaged_food | standalone |
| GLP1RestaurantImpact | staples | restaurant_glp1 | standalone |
| DataCenterREITDuopoly | reits | data_center | standalone |
| SpaceEconomy | space | launch | standalone |
| PublicBuilderEntryLevel | housing | us_builders | standalone |
| BoomerTravelSupercycle | transport | travel_master | master |
| HotelChains | transport | hotel_lodging | standalone |
| LuxuryTravelCruise | transport | cruise_luxury_travel | standalone |
| OTAandAITravel | transport | ota_distribution | standalone |
| AirlineLoyaltyRepricing | transport | airline | standalone |
| CasinoGamingIR | transport | casino_gaming | standalone |
| CopperSupercycle | materials | industrial_metals | standalone |
| AerospaceMetals | materials | aerospace_defense_metals | standalone |
| BeefSupercycle | agri | livestock_meat | standalone |
| CNTW_Master | macro | geopolitics_cntw | master |
| CNTW_S1_Military | macro | geopolitics_cntw | sub |
| CNTW_S2_GrayZone | macro | geopolitics_cntw | sub |
| CNTW_S3_CNEconomy | macro | geopolitics_cntw | sub |
| CNTW_S4_External | macro | geopolitics_cntw | sub |
| CNTW_S5_Tripwires | macro | geopolitics_cntw | sub |
| CNTW_S6_SemiDetw | macro | geopolitics_cntw | sub |
| CNTW_S7_DefenseIndustry | macro | geopolitics_cntw | sub |
| CNTW_S8_RareEarth | macro | geopolitics_cntw | sub |
| CNTW_S9_Shipping | macro | geopolitics_cntw | sub |
| CNTW_S10_TWDefense | macro | geopolitics_cntw | sub |

合計 89 IDs ✓

---

## 表 4：index.html anchor comment 規範

每個 sub_group 在 index.html 的 cat-body 內必須有對應 anchor comment：

```html
<!-- subgroup-anchor: semi.compute_demand -->
... 該子群組的 article cards ...
<!-- subgroup-anchor-end: semi.compute_demand -->

<!-- subgroup-anchor: semi.memory -->
... 卡片 ...
<!-- subgroup-anchor-end: semi.memory -->
```

**新 ID 自動插入規則**（industry-analyst skill Step 9.6 執行）：
1. 從 ID id-meta JSON 讀 `mega` + `sub_group`
2. 在 index.html 找 `<!-- subgroup-anchor: {mega}.{sub_group} -->` 的位置
3. 新 article 卡片插入到 anchor 之後（若 sub_group 已有卡片，附加到最末張之後）
4. 找不到對應 anchor → fail（強迫使用 controlled vocabulary）

**Empty sub_group**：anchor 之間留空（未來自動填入），或寫一行 `<!-- empty: 待建首份 ID -->` 提示。

---

## 表 5：id-meta JSON 必填欄位（v1.8 新增）

industry-analyst skill 生成的 ID HTML 必須在 `<script id="id-meta">` 內加入：

```json
{
  "mega": "semi",
  "sub_group": "memory",
  ...其他欄位
}
```

`scripts/validate_id_meta.py` 會驗證 `mega` 在表 1 白名單內、`sub_group` 在表 2 對應 mega 的子群組白名單內，違反 → push 失敗。

---

## 維護規則

- 新增子群組：先改本檔表 2 + 表 4（加 anchor），再 commit
- 改命名：先改本檔，搜尋全 codebase 替換 `mega.sub_group` 標籤
- 新增大類別：改表 1 + 在 index.html 加 cat-body section + 加所有 anchor

**版本**：v1.0（2026-04-30 首版）
