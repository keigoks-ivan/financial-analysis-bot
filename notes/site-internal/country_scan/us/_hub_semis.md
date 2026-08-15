> ⚠ STALE（2026-08-15）：本檔為 hub／子頁組裝前研究素材，opus critic 修正未回填；數字以已發布的 docs/backtest/country_scan/us*.html 為準。

# Hub fragment — 鏡頭二・半導體與 AI 基礎設施（semis.html）

## thecall（一段式，供 hub §2 引用）

半導體與電子供應鏈相關母體 140 檔（GICS 十個子產業，已扣除歸屬鏡頭一的 AAPL）合計市值約 US$16.3 兆，NVDA 一家佔 33.4%，前五大（NVDA／AVGO／MU／AMD／INTC）佔 60.1%，前十大佔 71.5%（as-of 2026-08-15）。本鏡頭把 AI 供給側拆成運算引擎、網通光通訊、EDA／IP 授權、設備材料、類比電源、記憶體、資料中心電源散熱、EMS 通路八層，逐層問同一個問題：這輪 AI capex 潮結束後誰還握有定價權。結論分三層——機制性護城河成立（NVDA、AMAT／LRCX／KLAC 設備三巨頭、CDNS、TXN／ADI）、結構真實但曝險集中（AVGO／MRVL 客製化 ASIC、MPWR、ANET、VRT／APH）、量在飛漲但定價權未證實（MU／SNDK 記憶體 supercycle、EMS 代工與通路群、NVTS）。

## hub 卡片摘要素材（1-2 張，供 hub §2 鏡頭二卡片使用）

**卡片一・集中度事實**：半導體與電子供應鏈母體 139 檔（ex-AAPL）市值加權集中度極端——NVDA 一檔佔 33.4%，前十大佔 71.5%；本鏡頭獨立交叉驗證：56 檔站內 DD 覆蓋範圍內，運算引擎單一層即佔本鏡頭 DD 覆蓋市值 60.6%，兩套口徑互相印證。

**卡片二・三層答案**：第一層（護城河機制性成立）＝NVDA（生態系＋系統互連）、AMAT／LRCX／KLAC（設備寡占 88.2%）、CDNS（EDA 訂閱制收費站）、TXN／ADI（終端市場分散的類比龍頭）；第二層（結構真實但曝險集中）＝AVGO／MRVL（客製化 ASIC，客戶集中度風險）、MPWR（AI capex 槓桿高但曝險集中）、ANET（Ethernet 陣營，架構路線之爭未定）、VRT／APH（資料中心電源散熱，繫於 AI capex 總量不逆轉）；第三層（量在飛漲但定價權未證實）＝MU／SNDK（HBM／NAND supercycle，遠期本益比僅 6.2-6.3 倍反映市場高度懷疑其持續性）、DELL／JBL／FLEX／SANM／ARW（EMS 代工與通路，毛利結構性偏低）、NVTS（站內裁決 X，本鏡頭最負面名字）。

## Exhibit 素材一張（供 hub 引用或改編）

**八層供給地圖：運算引擎一層佔本鏡頭 DD 覆蓋市值 60.6%**（來源：`_universe.json`，2026-08-15 快照；56 檔站內 DD 覆蓋範圍內市值加總，7 檔資料缺不計入）

| 層 | 檔數 | 合計市值 | 營收成長中位數 |
|---|---:|---:|---:|
| 運算引擎（NVDA／AMD／INTC／AVGO／MRVL／QCOM） | 6 | US$9,078億 | +37.8% |
| 記憶體（MU／WDC／STX／SNDK／NTAP） | 5 | US$1,774億 | +48.5% |
| 設備材料（AMAT／LRCX／KLAC 等 9 檔） | 9 | US$1,231億 | +30.0% |
| 網通光通訊（CSCO／ANET／CIEN 等 7 檔） | 7 | US$974億 | +39.3% |
| 類比電源（TXN／ADI／MPWR 等 7 檔） | 7 | US$640億 | +35.8% |
| 資料中心電源散熱（VRT／GLW／APH 等 6 檔） | 6 | US$614億 | +27.8% |
| EMS／通路（HPE／CRWV／DELL 等 7 檔） | 7 | US$560億 | +40.0% |
| EDA／IP（CDNS／RMBS） | 2 | US$100億 | +22.3% |

## .basket 答案段（可直接搬用或濃縮）

供給側的錢集中流向少數幾個真正的收費站；代工財與商品循環財即便成長再快，也沒有換到定價權。第一層護城河機制性成立——NVDA（CUDA 生態系＋系統級互連，資料中心營收仍加速至年增 92%）、AMAT／LRCX／KLAC（設備三巨頭寡占 88.2%，客戶切換成本極高）、CDNS（EDA 訂閱制收費站，全鏈抗週期性最強）、TXN／ADI（終端市場高度分散的類比龍頭）；第二層結構真實但曝險集中——AVGO／MRVL（客製化 AI ASIC 設計服務，客戶集中度風險真實）、MPWR（電源管理晶片，AI capex 槓桿高但曝險集中於資料中心）、ANET（Ethernet 開放標準陣營，與 NVDA 生態系路線之爭未定）、VRT／APH（資料中心電源散熱連接，需求時間常數長但仍繫於 AI capex 總量不逆轉）；第三層量在飛漲但定價權未證實——MU／SNDK（HBM／NAND supercycle 驅動營收年增超過 340%，遠期本益比卻僅 6.2-6.3 倍）、DELL／JBL／FLEX／SANM／ARW（EMS 代工與通路，毛利結構性偏低）、NVTS（站內裁決 X，本鏡頭 56 檔中最負面的名字）。

## 一句一檔（代表作）

**NVIDIA（NVDA）**——資料中心營收 US$752 億、年增 92%仍在加速，CUDA 生態系切換成本與系統級互連效能是本鏡頭護城河機制最完整的單一名字，但也是超大規模雲端客戶最有動機、最有資本繞開的護城河。

## DD 候選提名（公司／缺口理由）

1. **Synopsys（SNPS）**——EDA 雙寡占另一半，缺口：站內僅 CDNS 有 DD，SNPS 覆蓋為結構性缺口，無法完整比較 EDA 兩大玩家相對位置。
2. **Microchip Technology（MCHP）**——類比／MCU 龍頭之一，缺口：本頁類比電源層尚無覆蓋。
3. **Super Micro Computer（SMCI）**——AI 伺服器組裝代表性名字，缺口：站內尚無覆蓋。
4. **Emerson Electric（EMR）**——工業自動化與電氣設備，缺口：資料中心曝險程度需查證後決定歸屬鏡頭二或鏡頭八。
5. **CDW Corporation（CDW）**——企業 IT 通路商，缺口：與 ARW 同屬通路型商業模式，尚無覆蓋可供對照。

站內已有 DD 覆蓋 56 檔（九鏡頭最多，92.9% 在 90 天複審窗內），完整對帳表見 `semis.html` §10 Exhibit 10；4 檔逾窗（CDNS／FN／CAMT／NVMI，均為 2026-05 初 v12.3 legacy 檔），集中於 §4 EDA 與 §5 設備材料兩層，是本鏡頭複審優先級最高的兩層。
