# QC-41 寫稿後產業態勢獨立 critic — DD_CRS_20260901.html

- **受檢檔**：`docs/dd/DD_CRS_20260901.html`（Carpenter Technology，v15.0，92,101 bytes，帶內）
- **critic 模型**：opus（獨立冷讀，未參與寫稿；writer＝sonnet）
- **critic 日期**：2026-09-01
- **搜尋預算**：10 / 10（用滿）
- **機械 gate**：`verify_dd_math.py` 已 PASS（恆等式部分不重算，火力集中在推導真偽與正文層對帳）

## 總判定：PASS-with-fixes

| 軸 | 燈號 | 一句話 |
|---|---|---|
| ① 競爭惡化 | 🔴 | 「全球僅 3 家」是錯的；漏掉 Aubert & Duval、Acerinox/Haynes、Aperam/Universal Stainless 三組結構性玩家 |
| ② 供需 durability | 🟡 | 供給側證據基礎只做了三分之一；「ATI 是唯一對稱擴產」的框架低估近 24 個月的產能與所有權移動 |
| ③ 其他結構變數 | 🔴 | §6.H「未見 in-house 化跡象」被直接證偽（Airbus+Safran 全資 A&D、Safran 明言垂直整合是「戰略必需」）；關稅／貿易政策整軸 0 提及 |
| ④ priced-in | 🟡 | 52 週高點 $625.94（現價 −23.9%）、YTD +70.9%、KeyBanc 明講「因估值」下修目標價——三個事實全部缺席，且「近月盤整 $465-496」是錯的 |
| ⑤ 覆蓋面掃描 | 🔴 | 關稅／貿易政策＋原料地緣＝整軸未查（0 命中）；歐洲／日本競爭者整軸未查；勞工、能源成本、環保未查 |
| ⑥ 量化模組 | 🔴 | (a) 🟡 再投資率與穩態增量 ROIC 皆無推導；(b) 🟢 情境樹 EPS 價差實質（但 Bull 標籤算錯）；(c) 🔴 §10.6 與 §10.5 不對帳，Bull 差 4pp、Base re-rate 差 4.7pp、且回購被雙重計算 |
| ⑦ QC-54 白話呈現 | 🟢 | §1 與 §13 皆有真白話開場，矩陣已收進 `<details>`，無承重結論僅靠燈號 |

**為何不是 FAIL**：兩個 🔴（③、⑥c）與一個 🔴（①）都不推翻「進場｜核心」的方向。裁決的承重證據——SAO 調整後營益率 37.8%（YoY +730bp）、8/8 筆 LTA 全數提價且 0 客戶流失、FY27 營益 guidance $850-880M（+21-25%）——在我查證的範圍內**沒有任何一條被反面證據推翻**。我找到的東西要求的是「把宣稱收緊、把 §10.6 重算、把監測項補上」，不是改成觀望。

**但附一條升級條件**：把 A&D／Haynes-Acerinox／Universal-Aperam 補進 §5 市佔競爭表與 §5.F 之後，若 writer 無法在新的競爭地圖上守住 `moat_pricing_power=8` 與「理性寡占」賽局判定，則 `moat=A`、`dca_role=核心` 必須重新裁決一次。

---

## ① 競爭惡化 — 🔴 報告判錯

### 判錯的具體宣稱

「全球僅 3 家能量產航太引擎級鎳基超合金的公司之一」（CRS／ATI／PCC）。這句話出現在**最承重的四個位置**：`<h1>` 下方 hypothesis-box 主論點句、§1 第一段、§2 存在意義、以及 dd-meta `oneliner`（下游 screener 直讀）。

### sourced 反證

**(1) Aubert & Duval（法國）＝第 4 家，且是引擎盤件級。**
- 「one of the world's leading producers of specialty steels, titanium alloys, **nickel-based superalloys** and high-performance aluminum materials」，航太用途明列「**turbine discs, engine hot sections**, and landing gear」，並自陳「Producing material certified for aerospace-grade applications can take up to 10 years or more」——與 CRS 的認證週期論述同一條護城河、同一個產品段。
- 規模：**營收約 €960M、10 個工業廠區（8 個在法國）、約 4,400 名員工**。以 CRS SAO 分部年營收約 $3.0B 對照，A&D 不是可以忽略的邊角玩家。
- 來源：[metal-am.com](https://www.metal-am.com/airbus-safran-and-tikehau-capital-finalise-acquisition-of-aubert-duval/)、[Safran 新聞稿](https://www.safran-group.com/pressroom/airbus-safran-and-tikehau-capital-finalize-acquisition-aubert-duval-2023-04-27)、[Airbus 新聞稿 2026-06](https://www.airbus.com/en/newsroom/press-releases/2026-06-airbus-safran-and-tikehau-capital-sign-an-agreement-for-the-sale-of-tikehau-capitals-stake-in-aubert)

**(2) Acerinox 買下 Haynes International（US$798M，US$61/股，已完成交割）。**
- Haynes ＝「a U.S. leading manufacturer and marketer of technologically advanced high-performance alloys」，專長「**nickel and cobalt-based alloys, which are critical for aerospace applications**」。
- 交易讓一家歐洲不鏽鋼大廠（透過美國子公司 North American Stainless）直接持有美國本土航太鎳鈷合金產能，且 Acerinox 明講策略優先項是「美國市場、高性能合金、航太」。
- **NAS 肯塔基廠擴產於 2026 年初動工，年增 308,000 短噸**（不鏽鋼為主，但同一資本與客戶通道）。
- 來源：[Acerinox 官方](https://www.acerinox.com/en/comunicacion/noticias/Acerinox-completes-the-acquisition-of-Haynes-International/)、[Metalnomist 2026-08](https://www.metalnomist.com/2026/08/nas-stainless-mill-expansion.html)

**(3) Aperam 買下 Universal Stainless & Alloy Products（2025-01-23 完成）。**
- Universal Stainless ＝「a leading manufacturer of specialty steel products for **key aerospace** and industrial applications in the U.S.」，且其 North Jackson 廠具備 VAR/ESR premium 重熔線——與 CRS 的 primary melt 業務直接相鄰。
- 來源：[Barchart](https://www.barchart.com/story/news/30577657/universal-stainless-announces-completion-of-its-acquisition-by-aperam)

### 為何這是 🔴 而不是 🟡

不是「報告漏了一家小公司」。是**報告的競爭地圖漏掉了整整一輪產業整併**：兩家歐洲不鏽鋼母公司（Acerinox、Aperam）在過去約 24 個月內用併購買進了美國航太合金產能，一家法國超合金廠（A&D）被它自己的客戶買走。§5「市佔競爭表」只有 ATI／HWM／PCC 三列，§5.F「對手財務深度對照」只做了 ATI 與 HWM，§5「競爭鴻溝」宣稱「新進者更難獨立跨過此門檻」——但實際發生的事情是**沒有人「獨立跨過」門檻，大家用併購繞過去了**，而報告對這條路徑完全沒有討論。

同時，報告 §5「無形資產」段自己提到「過去 CRS 對 ATI 提起過專利訴訟」，卻沒有把智財／人才／製程 know-how 外流當成競爭軸做任何前瞻。

### 修正指令

1. **改掉「全球僅 3 家」的表述**（h1 hypothesis-box、§1、§2、dd-meta `oneliner` 四處同步）。可接受的收緊版本例如：「在美國本土 open-market 具備航太引擎級鎳基超合金 primary melt 資格的供應商僅 CRS 與 ATI 兩家；全球尚有 PCC（Berkshire，主要自用）與 Aubert & Duval（Airbus/Safran 全資，主要供歐系引擎）」——必須是可查證的口徑，不是行銷句。
2. **§5 市佔競爭表新增三列**：Aubert & Duval、Haynes（Acerinox/NAS）、Universal Stainless（Aperam），每列填「目前定位／3 年回看+前瞻／核心威脅等級／可比 margin／戰爭承受力」。母公司資本規模是關鍵欄位——Acerinox 與 Aperam 的資產負債表深度改變了「不具備發動價格戰的財務動機」這個判定的前提。
3. **重新裁決「理性寡占」賽局結構**。現行判定的唯一依據是「ATI 新產能 80% 已鎖 LTA」。在四到六個玩家、其中兩個有歐洲母公司補血、一個由客戶擁有的結構下，「理性寡占」需要重新論證或降級。
4. **重新檢視 `moat_pricing_power=8`**。目前扣 1 分的理由只寫 ATI；補上其餘三組後，8 分是否還成立要重答。若降至 7，合併分 = 9×0.6 + 7×0.4 = 8.2，仍在 A 級帶，`moat=A` 大機率可守——但這個推導必須寫出來，不能沿用舊分數。
5. `moat_trend=↑` 我認為**可以維持**：其依據（12 個月 SAO OM 32.0%→37.8%、+580bp）是實測數字，未被任何反證推翻。不要在這一欄過度修正。

---

## ② 供需 durability — 🟡 報告低估

### 報告怎麼寫的

§3「供需 durability 裁決（雙向）」做得其實不差：正面四條（3 家合格供應商／5-10 年認證／16,000 架積壓／FY27 國防預算請求 $1.45T／IGT 第二曲線）、反面兩條（Airbus GTF 延誤下修至 2027 年底、FY22 GAAP 淨損 -$49.1M）、供給側一條（ATI 9,000 噸、2027H2、80% 鎖 LTA），結論「結構性持久為主，但已出現同業對稱式的紀律型擴產回應，非永久性稀缺」。**方向我同意，而且 ATI 這條是 writer 自己查出來推翻管理層舊敘事，值得記一筆。**

### 低估在哪

**供給側只寫了一條，實際上至少有五條**（除①已列的併購三條外）：

- **Safran 自建鍛造產能**：Gennevilliers 廠 **€150M 鍛造擴產**（2026 年公布）。Safran 高層明講「vertical integration has become a **strategic necessity** rather than merely a competitive advantage」，策略目標是「reduce dependence on a **narrow group of specialized suppliers**」。這句話的主詞就是 CRS 這類供應商。來源：[Metalnomist 2026-06](https://www.metalnomist.com/2026/06/safran-forging-press-expansion.html)
- **Ellwood Group 在賓州 New Castle 裝設 20 噸 VIM 熔煉爐**（2024-04 宣布）。與 CRS 的 Reading, PA 同州、同製程段。來源：[Research and Markets — Superalloy Melting Equipment Report 2026](https://www.researchandmarkets.com/reports/6035420/superalloy-melting-equipment-market-report)
- 產業層：VIM 設備市場 2026 年 US$1.94B → 2034 年 US$3.42B，CAGR 7.3%，且趨勢是「large-capacity VIM（20 噸級）」——熔煉端整體在擴，不是只有 ATI 一家。

### 為何是 🟡 不是 🔴

以上沒有一條可以明天就取得 GE／P&W 引擎盤件的認證資格。5-10 年認證週期是真的，報告拿它當防線是對的。所以裁決方向（結構性持久為主）我不推翻。但**「ATI 是唯一對稱擴產、且 80% 鎖 LTA 因此是紀律型」這個敘事，是在一個只看到五分之一供給側訊號的資訊集上做的**，而報告把這個敘事一路餵進 §5 賽局判定、§10.5 bear 機率 25%、§13b 加碼條件。證據基礎不完整，結論就不該講得那麼定。

### 修正指令

1. §3 供給側③改寫為「近 24 個月供給側移動清單」，至少涵蓋：ATI Bakers South、Acerinox/Haynes、Aperam/Universal、Safran Gennevilliers、Ellwood New Castle。每條標「是否具備引擎盤件認證資格／預計時點／是否已鎖客戶」——**沒有認證資格的產能要明確標為『不構成 24 個月內威脅』**，這樣才誠實，也才守得住原本的結論。
2. §14 複審觸發表新增一列：「歐系／併購系產能取得美系引擎認證的首例」，這是把上面那條「目前沒有認證資格」變成可證偽的追蹤項。
3. §10.5 bear 機率 25% 的「供需 durability 依據一句」要重寫——目前只援引 ATI 與 GTF 兩條脆弱性證據；補上完整供給側清單後，25% 是否要動要重答（我的判斷是不必動，但推導要更新）。

---

## ③ 其他結構變數 — 🔴 報告判錯

這一軸有兩個獨立問題：一個是明確宣稱被證偽（客戶垂直整合），一個是整軸未查（關稅／貿易政策，見⑤）。

### 3-1 客戶 in-house 化：明確宣稱被 sourced 證據直接推翻 🔴

**報告的宣稱**（§6.H③客戶生命週期）：

> 「Grow with 客戶為主（LTA 續約擴大而非萎縮），**未見 in-house 化跡象**（引擎級超合金 in-house 化的資本／技術門檻對 OEM 本身也極高）」

**sourced 反證**：

1. **Airbus 與 Safran 已於 2026-06-25 簽定具約束力協議，買下 Tikehau Capital 手上的 Aubert & Duval 股權，取得 A&D 的完整、對等共同所有權**（此前為 Airbus／Safran／Tikehau 三方各三分之一，自 2023-04 從 Eramet 收購而來）。也就是說：**機身 OEM ＋ 引擎 OEM 聯手擁有一家 €960M 營收的鎳基超合金／鈦合金／特殊鋼廠，而且就在 DD 寫稿日前兩個月完成加碼。** 這正是「in-house 化」，只是走的是買下供應商而不是自建產線的路徑——報告只設想了後者（「資本／技術門檻對 OEM 本身也極高」），完全沒設想前者。
   來源：[Airbus 2026-06 新聞稿](https://www.airbus.com/en/newsroom/press-releases/2026-06-airbus-safran-and-tikehau-capital-sign-an-agreement-for-the-sale-of-tikehau-capitals-stake-in-aubert)、[avitrader 2026-06-25](https://avitrader.com/2026/06/25/airbus-safran-take-full-control-of-aubert-duval/)、[aerotime](https://www.aerotime.aero/articles/airbus-safran-buy-tikehau-out-aubert-duval)
2. **Safran 高層公開表態：垂直整合已從「競爭優勢」升級為「戰略必需」，策略明確是「reduce dependence on a narrow group of specialized suppliers by strengthening domestic capabilities and consolidating key production stages」**，並以 €150M 擴充 Gennevilliers 鍛造產能落實。Safran 是 CFM（LEAP）的 50% 股東，LEAP 是 737 MAX 與 A320neo 的引擎——正是報告 H2 假設的需求載體。
   來源：[Metalnomist 2026-06](https://www.metalnomist.com/2026/06/safran-forging-press-expansion.html)、[Safran / CFM](https://www.safran-group.com/companies/cfm-international)

**這條 🔴 的擴散範圍**（不只 §6.H 一處）：

- **§5.R 檢查點「決策層級 🟢」**：判定理由是「決策最小單位是整條認證合格的供應商關係，換供應商＝重跑 5-10 年認證」。但客戶的實際答案不是「換供應商」也不是「second-source」，是**把供應商買下來**。這條路徑繞過了認證週期（A&D 的資格是既有的），所以 🟢 的推導不完整。
- **§5「24 個月內最可能瓦解護城河的變化」表**：三列（ATI 擴產／Airbus GTF 延誤／陶瓷基複材）**沒有一列是客戶垂直整合**。
- **§12a 盲點表**：三列（SAO 單引擎集中／治理連續性／ATI 是否維持紀律）**沒有一列是客戶垂直整合**。
- **dd-meta `kill_metrics[]`**：四條（SAO OM／A&D 訂單動能／治理／ATI 定價影響）**沒有一條追蹤 OEM 垂直整合**。下游 position-thesis-monitor 因此看不見這條風險。
- **§6.H 客戶結構風險評級 🟡「集中但 Grow-with 邏輯強」**：這個評級建立在「未見 in-house 化」之上，前提被推翻後評級要重答。

**平衡說明（不要過度修正）**：A&D 的三方持股結構自 2023-04 就存在，2026-06 只是買斷少數股東，**不是新事件**。而且 A&D 主要服務歐系引擎與法國國防，CRS 的 60-65% LTA 綁定的是美系引擎鏈。所以這條的正確定性是「**報告的競爭與客戶地圖從一開始就不完整**」，不是「世界剛剛變了」。它應該進監測清單與盲點表，不應該被寫成迫在眉睫的 thesis 破口。

### 3-2 修正指令（3-1）

1. §6.H③ 刪除「未見 in-house 化跡象」，改寫為 sourced 事實陳述：Airbus+Safran 已全資持有 A&D（2026-06 完成買斷）、Safran 明言垂直整合為戰略必需並投入 €150M 擴鍛造，並說明**為何這對 CRS 的美系客戶敞口影響有限**（若 writer 認為有限，要把理由寫出來，不能靠沉默）。
2. §5「24 個月內最可能瓦解護城河的變化」表新增一列：「客戶（引擎／機身 OEM）以併購取得既有合格產能，繞過 5-10 年認證週期」，等級與機率由 writer 判定。
3. §12a 盲點表新增一列：「假設：引擎 OEM 不會垂直整合進 primary melt。若不成立的後果：LTA 續約提價空間結構性收斂。」
4. **dd-meta `kill_metrics[]` 新增一條**（這是下游 monitor 唯一看得見的介面，必須落機器欄不能只寫散文）：例如「OEM 垂直整合／自有合格產能取得美系引擎盤件資格」，bear_threshold 寫成可觀察事件（如「GE／P&W／Safran 任一宣布收購或取得美國本土鎳基超合金 primary melt 合格產能」），window「12 個月」。
5. §5.R「決策層級」保留 🟢 或降 🟡 由 writer 判，但**推導必須加上一句處理「客戶買下供應商」這條繞道路徑**。

### 3-3 關稅／貿易政策：整軸 0 提及 🔴（詳見⑤）

見⑤覆蓋面掃描。這裡只放結論與最關鍵的兩條 sourced 事實，方便 writer 直接引用：

- **Section 232 金屬與衍生品重構**：2026-04-02 總統公告大幅修訂鋼、鋁、銅及其衍生品的 232 條款適用方式，**從按金屬含量課稅改為按成品全額關稅價值課稅**；外國金屬含量按重量 >15% 者，**全額關稅價值適用 25% 統一稅率**，≤15% 者不課。2026-06-01 白宮再發修訂公告，**2026-06-08 生效至 2027-12-31**。來源：[White & Case](https://www.whitecase.com/insight-alert/united-states-modifies-steel-aluminum-and-copper-section-232-tariffs)、[BDO](https://www.bdo.com/insights/tax/section-232-metals-tariffs-expanded-and-recalibrated-what-importers-need-to-know)、[PwC](https://www.pwc.com/us/en/services/tax/library/pwc-steel-and-aluminum-goods-subject-to-section-232-tariffs-expanded.html)
- **Section 232 加工critical minerals**：2026-01-14 兩份公告（半導體＋加工關鍵礦物及其衍生品）。**目前不直接課稅**，而是指示商務部與 USTR 談判，180 天內（即 **2026-07-13**）提交報告；總統明講「depending on the outcome... I may consider alternative remedies in the future, **including minimum import prices**」。後續行動的風險標的**明列「processed lithium, cobalt, nickel, manganese and graphite compounds... and specialty alloys and chemical inputs incorporating critical minerals」**。來源：[White & Case](https://www.whitecase.com/insight-alert/president-trump-orders-critical-minerals-trade-negotiations-section-232-action)、[Covington](https://www.cov.com/en/news-and-insights/insights/2026/01/trump-administration-announces-results-of-critical-minerals-investigation-under-section-232-and-directs-us-officials-to-initiate-negotiations)、[Recycling Today](https://www.recyclingtoday.com/news/usa-trump-proclamation-critical-minerals-nickel-cobalt-rare-earths-import-negotiations-tariffs/)

**為何這對 CRS 是實質變數而非背景噪音**：CRS 的整套定價機制建立在 surcharge（原料成本轉嫁）上，§3「議價權（三段）」明講「以 surcharge 機制直接轉嫁原料價格波動，不承擔庫存週期風險」。鎳與鈷若進入 232 條款的關稅或最低進口價機制，改變的是 surcharge 的基準與時滯，而報告對 surcharge 的唯一著墨是把它歸為「噪音」（§2.A「訊號 vs 噪音」）。**方向上關稅對美國本土產能大概率是淨正面（進口替代保護），但淨正面不是「不必查」的理由——報告目前的狀態是根本沒問這個問題。**

**修正指令**：§3「地緣曝險」段目前只有一句「生產基地集中美國本土…無顯著海外地緣風險」——這是把地緣當成廠址問題。改寫為兩段：(a) 貿易政策（232 金屬衍生品現行稅率／加工關鍵礦物談判進度與 2026-07-13 報告後續），(b) 原料來源地緣（鎳／鈷／鈦的供應地與制裁曝險），各自標明對 CRS 是正面／負面／中性，並標 as-of。

---

## ④ priced-in — 🟡 報告低估

### 報告寫了什麼

- §11.4 註腳：「分析師目標價：跨來源分歧大（$466-$700，中位約 $556-$608，n=9-14），JPMorgan 2026-07 由 $470 上修至 $705；**分歧點在於市場對 ATI 對稱擴產利空的定價程度不一**」
- §13 決策矩陣 row 5：「動能過熱? 否（**近月盤整 $465-496**，未見過熱）」
- §2.B'：僅與 2026-05-18 inception 價 $414.94 對照（+14.8%）
- 附錄A：現價 $476.42／W52 $400.90／W104 $302.18／W250 $158.47；20 週布林中軌 $512.38，「現價位於中軌下方，非過熱」

### 缺席的 sourced 事實

**(1) 52 週高低點完全沒出現在報告任何一處。**
- **52 週高 $625.94、52 週低 $228.88（as of 2026-08-13）**。現價 $476.42 ＝**距 52 週高 −23.9%**、距 52 週低 **+108.2%**。
- 2026-08-27 收盤 $490.58。
- 來源：[stockinvest.us](https://stockinvest.us/stock/CRS)

**(2)「近月盤整 $465-496」是錯的。** 2026-08-11 收盤 **$537.57**（當日 −4.0%，且該報導同時記載「過去一個月 −7.1%、**YTD +70.9%**」）。若 8/11 是 $537.57、8/27 是 $490.58、8/31 是 $476.42，過去一個月的實際區間下緣約 $476、上緣至少 $538——**不是 $465-496**。這是 §13 決策矩陣 row 5 的唯一證據，而它與可查資料矛盾。
- 來源：[GuruFocus 2026-08-11](https://www.gurufocus.com/news/9026079/a-look-at-carpenter-technology-corp-crs-after-40-decline-gf-value-20737-vs-price-53757)

**(3) YTD +70.9%（as of 2026-08-11）這件事整份報告沒有出現。** 報告唯一的價格脈絡是「距 inception 105 天 +14.8%」——這個框架把一年翻倍級的行情裁掉，只留下最近三個半月的溫和漲幅。對一份要判「進場｜核心」的報告，這是最不該被裁掉的 priced-in 事實。

**(4) 分析師目標價下修的真實理由與報告的歸因不符。** 報告說分歧點是「市場對 ATI 對稱擴產利空的定價程度不一」——這是無 source 的推測。實際可查的是：**KeyBanc 明確以「估值」（on valuation）為由把目標價自 $644 下修至 $608**，同時維持 Overweight；Deutsche Bank $722→$689（Buy）；Susquehanna $680→$600（Positive）；BTIG 逆勢自 $450 上調至 $620（Buy）。**三家在財報 beat ＋ guidance 大幅上修之後仍下修目標價，理由是估值不是 ATI。**
- 來源：[Investing.com — KeyBanc lowers on valuation](https://www.investing.com/news/analyst-ratings/keybanc-lowers-carpenter-technology-stock-price-target-on-valuation-93CH-4831726)、[public.com forecast](https://public.com/stocks/crs/forecast-price-target)

**(5) 存在成形的公開空方論述，報告未對質。**
- Seeking Alpha：「Carpenter Technology Stock: **From Strong Buy To Sell After A 78% Rally**」。
- Simply Wall St：「CRS Stock Looks **Rich** After Aerospace Demand Rebound」（2026-07-01）。
- GuruFocus GF Value **$207.37** vs 當時股價 $537.57。
- 空方核心：「over 60% of revenue」集中於循環性航太國防、destocking 風險、以及「the real divide between bulls and bears is how durable that earnings power proves to be, **because even small disappointments could matter a lot when the starting valuation is this full**」。
- 來源：[Seeking Alpha](https://seekingalpha.com/article/4925638-carpenter-technology-from-strong-buy-to-sell-after-a-78-percent-rally)、[Simply Wall St](https://simplywall.st/stocks/us/capital-goods/nyse-crs/carpenter-technology/news/carpenter-technology-crs-stock-looks-rich-after-aerospace-de)

### 為何是 🟡 不是 🔴

報告的估值結論（🟡 公允、PEG 1.36、Fwd PE 30.0x 相對 ATI 42x／HWM 51x 折價）**在數字上站得住**，而且「現價低於 20 週布林中軌」這條事實報告自己有寫。所以估值燈 🟡 我不推翻。但報告把一個 **YTD +70%、距高點 −24%、多家在 beat 之後因估值下修目標價、有成形賣出論述**的標的，呈現成「近月盤整、未見過熱、市場只是在爭論 ATI」——**priced-in 這一軸的事實基礎是選擇性的**，而選擇的方向剛好都對裁決有利。

### 修正指令

1. **§13 決策矩陣 row 5 的證據句必須改**：把「近月盤整 $465-496」換成可查證的區間與 52 週高低點。結論（未過熱）我認為仍成立——距 52 週高 −23.9% 本來就不是過熱——但**要用對的數字得到對的結論**。
2. **附錄A 價格表補上 52 週高 $625.94／52 週低 $228.88／距高點 −23.9%／YTD 漲幅**，並標 as-of。
3. **§11.4 目標價註腳改寫**：把「分歧點在 ATI」這個無 source 的歸因刪掉，換成實際可查的分析師行動與其**自陳理由**（KeyBanc「on valuation」、DB、Susquehanna 下修；BTIG 上修）。
4. **§10 或 §11 新增一段「空方最強論述對質」**：正面回應「78% 漲幅後轉賣出」與「valuation is this full, small disappointments matter a lot」這條，說明為何 writer 不接受。§1 trap box 的「空頭最強一擊」目前寫的是 Boeing FAA ＋治理，這兩條都是自己設計的假想情境，不是市場上真實存在的空方論述——**用真實存在的空方論述去對質，才是 pre-mortem 的本意**。
5. §2.B' 除了 inception 對照，補一行 YTD／52 週框架，避免把長漲幅裁掉。

---

## ⑤ 覆蓋面掃描（強制） — 🔴

逐軸點名。「未查」＝全文關鍵字 0 命中（已用 grep 對 HTML 全文機械確認）。

| 軸 | 狀態 | 證據 |
|---|---|---|
| **關稅／貿易政策** | 🔴 **整軸未查** | `關稅`/`tariff`/`Section`/`232` 全部 **0 命中**。對一家美國本土特殊金屬熔煉商、在 2026-04 與 2026-06 兩次 232 條款重構、2026-01 加工關鍵礦物 232 公告（報告期限 2026-07-13，明列「specialty alloys」為後續行動標的）的年份，這是不可接受的缺軸 |
| **原料地緣／供應鏈** | 🔴 **整軸未查** | `nickel`/`鎳價`/`Russia`/`俄羅斯`/`Indonesia`/`印尼` 全部 **0 命中**。報告的整套定價論述架在 surcharge 轉嫁上，卻從未問「鎳鈷從哪來、會不會被課稅或制裁」 |
| **歐洲／日本競爭者** | 🔴 **整軸未查** | `Aubert`/`Duval`/`VDM`/`Aperam`/`Acerinox`/`Haynes`/`Universal`/`Nippon`/`Daido` 全部 **0 命中**（見①） |
| **地緣政治（廣義）** | 🟡 **一句帶過** | §3 唯一一句：「生產基地集中美國本土…無顯著海外地緣風險」。把地緣化約為廠址問題；未觸及貿易政策、出口管制、盟國供應鏈政策 |
| **勞工／工會** | 🟡 **整軸未查** | `工會`/`union`/`勞工` **0 命中**。CRS 主力廠在 Reading, PA，熔煉業為典型工會密集製造業；勞資合約到期與罷工是這類公司的標準營運風險軸 |
| **能源成本** | 🟡 **整軸未查** | `能源成本` 0 命中（`電力` 2 命中但都是講資料中心需求＝需求側）。VIM/VAR 真空熔煉是極度耗電製程，而報告自己主張資料中心正在推高電力需求——**同一份報告用電價上漲當需求利多，卻沒問電價上漲對自己的成本影響**，這是明顯的單向論證 |
| **環保／排放／PFAS** | 🟡 **整軸未查** | `環保`/`排放`/`PFAS` **0 命中**。金屬熔煉的空污與廢棄物法遵是常態成本項 |
| **反壟斷** | 🟢 **合理不適用** | 0 命中，但雙寡頭且無併購動作，此軸確實不適用，不記缺失 |
| **政策（國防預算）** | 🟢 **有查** | FY27 DOD 預算請求 ~$1.45T（CSIS），並落入 §3／§6.A''／§10.5 |
| **終端市場覆蓋** | 🟢 **完整** | 航太商用（引擎／緊固件／結構）、國防、能源 IGT、醫療、工業消費五段全覆蓋，且都帶 YoY 成長率與分項拆解。這一項做得好 |
| **替代技術** | 🟡 **半查** | 陶瓷基複材（CMC）有列入 §5 表且判 <10%，合理。但**積層製造（AM）降低 buy-to-fly ratio 對每台引擎合金用量的影響完全沒問**——`buy-to-fly` 0 命中，`additive` 0 命中（`積層` 3 命中都是講 PEP 分部自己的業務）。對一家按磅賣材料的公司，AM 減少每架飛機的材料採購量是結構性需求變數 |

### 修正指令

1. **必補（🔴）**：§3 新增「貿易政策與原料供應鏈」小節，涵蓋 232 金屬衍生品現行規則、232 加工關鍵礦物談判進度、鎳鈷來源地與制裁曝險，每條標方向（正／負／中性）＋ as-of。
2. **必補（🔴）**：§5 競爭地圖補歐系玩家（見①修正指令 2）。
3. **建議補（🟡）**：§7 或 §4 補一句能源成本曝險（VIM/VAR 電力密集度 vs 電價走勢），這條與報告自己的 IGT 需求論述互為鏡像，不補會顯得單向。
4. **建議補（🟡）**：§5「24 個月」表或 §6.F 附近補一句 AM／buy-to-fly 對材料用量的長期影響（可判低風險，但要問過）。
5. 勞工／環保兩軸可以各用一句帶過並標「未發現異常揭露」，但**不能是 0 提及**。

---

## ⑥ 量化模組完整性抽查（強制）

### (a) §5.R 增量 ROIC × 再投資率 — 🟡 報告低估

**做對的部分（先講，避免過度修正）**：
- §5.R 的 ROIC 象限定位是**真算的**且可複驗：稅後營業利益率 17.3% ＝ $540.5M ÷ $3,124.2M ✅（我算 17.30%）；投入資本周轉率 1.16x ＝ $3,124.2M ÷ $2,698M ✅（我算 1.158）；兩者相乘 20.03% ＝ 報告的 ROIC ~20.0% ✅ **內部自洽**。
- ROIIC（3Y）＝(540.5−56)/(2698−2089) ＝ 484.5/609 ＝ **79.55%** ✅ 算式與數字都對，且報告主動說明此值橫跨谷底到高峰、不具穩態代表性——**這是誠實的處理，記一筆**。
- **內生天花板 vs 共識的交叉檢查有做，而且沒有帶過**：共識 3Y EPS CAGR 22.1% − 天花板 14.0% ＝ 缺口 8.1pp，並歸因於「①回購對 EPS 的槓桿②margin 擴張尚未到穩態」。§10.5 還做了第二次 sanity check（Base FY26→FY31 EPS CAGR 18.9% vs 14.0%「超出⚠」，歸因 Athens 增量段）。**我複驗 18.9%：(25.50/10.76)^(1/5)−1 ＝ 18.8% ✅。** 這比 PLTR 那類「估計約 X% 然後不處理 sanity 失敗」好得多。

**缺陷（這是 🟡 的理由）**：

1. **再投資率沒有真算。** §6.D 表寫「再投資率（3Y 均）**估 ~55-65%**」，備註只給了公式名 `(Capex − D&A + ΔWC) ÷ NOPAT`，**三個輸入值（Capex、D&A、ΔWC）一個都沒填**。分母 NOPAT $540.5M 是有的，分子完全沒有。要落在 55-65%，分子須為 $297-351M；但報告 §1 trap box 說 FY26 資本支出是 **$242.7M**——若 D&A 為正、ΔWC 不大，分子根本到不了 $297M。**這個數字目前無法從報告內任何地方複驗。**
2. **穩態增量 ROIC ~22% 也沒有推導。** 報告明講「非用上表失真的 3Y ROIIC」，這個判斷是對的，但它用來取代的那個 22% 是憑空出現的——既不是 ROIIC 79.5%，也不是當期 ROIC 20.0%，也不是管理層給的 Athens 專案 ROIC >20%。**兩個輸入都是斷言，乘出來的天花板自然也是斷言。**
3. **算術不對帳**：22% × 60% ＝ **13.2%**，但 dd-meta 寫 `endo_growth_ceiling=14.0`。正文寫「估 ~13-15%」然後取 14.0（區間中點）——但正文的推導式給的是 13.2。機器欄與推導差 0.8pp。
4. **缺口歸因未定量**。缺口 8.1pp 歸給「回購槓桿＋margin 擴張」。回購：FY26 買回 $179.1M ÷ 市值 $23.6B ＝ **0.76%/yr**；即使新的 $1.0B 授權在 3 年內用完也只有約 1.4%/yr。**回購最多解釋 8.1pp 中的 1pp 上下。** 剩下的 ~7pp 全落在「margin 擴張」，但報告 §6.I 給的 margin 路徑是 37.8% → 39-41%（3 年 +120~320bp），相對增幅約 3-8%，年化約 **1-2.6pp**。**兩項加總約 2-3.6pp，離 8.1pp 還有一半沒歸因。** 報告的結論句是「非無法歸因，屬可解釋缺口」——這個結論在沒有把兩項定量的情況下下得太快。
5. **§4「FY26 guidance 資本支出 $300-315M」與 §1「資本支出 $242.7M」互相矛盾。** FY26 已於 2026-06-30 結束，對一個已結束的會計年度引用 guidance 區間本身就不對（$300-315M 幾乎確定是 FY27 的數字）。這個矛盾直接污染兩處：§4 資本密集度 9.6-10.1%（用 $242.7M 應為 **7.8%**），以及 (a) 的再投資率分子。

**修正指令**：
1. §6.D 再投資率一列**填入實際三個輸入值**（FY24-26 三年的 Capex、D&A、ΔWC）與逐年計算，或明確標為「無法取得 ΔWC 明細，改以 Capex/NOPAT 為代理，值為 X%」——**要嘛真算，要嘛誠實降級為代理指標，不接受「估 ~55-65%」**。
2. 穩態增量 ROIC 22% 給出推導路徑（例如：以 Athens 專案管理層 guided ROIC >20% ＋ 既有業務維持性資本的混合權重，或以 FY24→FY26 剔除週期復甦成分後的增量 ROIC）。
3. `endo_growth_ceiling` 與正文推導對齊（要嘛正文改成 22%×63.6%，要嘛機器欄改 13.2）。
4. 缺口 8.1pp 的兩項歸因各給一個數字（回購 ~0.8-1.4pp、margin ~1-2.6pp），並**誠實處理剩餘部分**——剩餘若歸因於「產能利用率提升的一次性營運槓桿」，那要明講它是一次性的、不進入長期複利，這反而會強化報告 §12 的「成功但劣化」敗局論述。
5. §4 資本支出數字與 §1 對齊，並註明是 FY26 實際還是 FY27 guidance。

### (b) 情境樹 Bull/Base/Bear EPS 價差實質性 — 🟢（含一個 🟡 標籤錯誤）

**結論：不是退化的情境樹。** 逐項複驗：

| 檢查 | 結果 |
|---|---|
| FY31 EPS：Bull $33.00 / Base $25.50 / Bear $12.50 | Bull vs Base **+29.4%**；Bear vs Base **−51.0%** — **EPS 價差實質** |
| 終端倍數：Bull 32x / Base 28x / Bear 15x | Bull 倍數僅比 Base 高 **14.3%**，遠小於 EPS 的 +29.4% — **Bull 由 EPS 主導，非倍數主導** ✅ 不觸發退化 🔴 |
| Bull 終端價 33.00×32 | $1,056.00 ✅；1056/476.42 ＝ +121.6% ✅（報告 +121.7%）；年化 2.2164^0.2 ＝ **+17.3%/yr** ✅ |
| Base 終端價 25.50×28 | $714.00 ✅；714/476.42 ＝ **+49.9%** ✅；年化 1.4987^0.2 ＝ **+8.43%/yr** ✅ |
| Bear 終端價 12.50×15 | $187.50 ✅；187.5/476.42 ＝ **−60.6%** ✅ |
| EV | 0.25×121.7 + 0.50×49.9 + 0.25×(−60.6) ＝ **+40.2%** ✅ 與 dd-meta `ev5y_pct=40.2` 一致 |
| AR | (25×121.7)/(25×60.6) ＝ **2.008 → 2.0** ✅ 與 `asym_ratio=2.0` 一致 |

**🟡 標籤錯誤**：Bull 列註記「**20%/yr CAGR**」。從 FY26 基期 $10.76 到 FY31 $33.00 的實際 CAGR ＝ (33.00/10.76)^(1/5)−1 ＝ **25.1%/yr**，不是 20%。20% 只有在「FY27 $13.38 起算、除以 5 期」時才成立——但 FY27→FY31 只有 **4 年**。而 Base 列用的是 FY26 基期（報告 §10.5 自陳 18.9%）。**兩列基期不一致，且 Bull 被標低了 5pp。** 這個錯誤的方向是**讓情境樹看起來比實際更退化**（讀者會以為 Bull EPS 只比 Base 高 1.1pp/yr，實際是高 6.2pp/yr）。

**🟡 附帶**：Base EPS 路徑自陳「逐年遞減成長率」，但實際是 FY27 +24.3% → FY28 **+18.7%** → FY29 **+23.4%**（加速）→ FY30 +15.0% → FY31 +13.1%。FY29 那一年不是遞減。敘述與數字不符。

**關於 writer 自提的「Base 終端倍數 28x 是否循環論證」——我的判定：🟡，非 🔴，但有一個真實缺口。**
- 報告**有給外部錨**（低於 ATI 現值 42x／HWM 現值 51x，高於一般工業股 18-20x），也**主動揭露了口徑不對稱**（現價用 FY28 forward 30.0x、終端用 FY31 當年 EPS），這兩點做得對，不算循環論證。
- **但缺口在於：28x 承擔了整個裁決的重量，而報告沒有做倍數敏感度。** 我替它算：Base EPS $25.50 若給 **22x**（＝報告自己 §6.E「成長降至 10%」情境用的倍數）→ 終端價 $561 → 5Y 總報酬 **+17.8%** → 年化 **+3.3%/yr**；若給 20x → $510 → +7.1% → **+1.4%/yr**。**也就是說，「進場｜核心」所依賴的 8.4%/yr IRR，幾乎全部由「五年後一家循環性合金廠仍值 28x」這個假設支撐。** §6.E 明明已經算過 28x/22x/16x 三檔，卻沒有把它接回 §10.5 的 Base。
- **修正指令**：§10.5 下方加一行倍數敏感度（Base EPS 固定 $25.50，終端倍數 28x／24x／22x／20x 對應終端價 $714／$612／$561／$510，年化 IRR **8.4%／5.1%／3.3%／1.4%**），讓讀者看見裁決對這一個變數的曝險。這**不會改變裁決**，但會讓 §13 的「合理但非驚豔的長期複利路徑」這句話有量化支撐。

### (c) IRR 內部對帳（§10.5 ↔ §10.6 ↔ 5Y/10Y） — 🔴 報告判錯

**這是本次抽查最硬的一條。§10.6 三分量拆解與 §10.5 情境樹在四個地方不對帳，其中一個是同一份報告對同一情境給出兩個相差 4pp 的答案。**

**錯誤 1（最嚴重）：Bull 情境合計年化，§10.6 說 +13.3%/yr，§10.5 說 +17.3%/yr。**
- §10.6 Bull 列：EPS +13.3% ＋ re-rate −1.7% ＋ 股息買回 +1.7% ＝ 合計「**≈+13.3%**」。
- §10.5 Bull 列年化 IRR：「**+17.3%/yr**」（我已複驗此值正確）。
- **同一報告、同一情境、相差 4.0pp，且兩處都是渲染給讀者的數字。**

**錯誤 2：Base 估值 re-rate 分量 −6.1%/yr 與 §10.5 的倍數路徑矛盾。**
- §10.5 Base 是 30.0x → 28x，**五年**。正確年化 ＝ (28/30)^(1/5) − 1 ＝ **−1.37%/yr**。
- §10.6 寫 **−6.1%/yr**。−6.1%/yr 持續五年意味終端倍數 30×(1−0.061)^5 ＝ **21.9x**，不是 28x。
- **§10.6 的 Base 列在用一個 §10.5 沒有採用的倍數路徑。**

**錯誤 3：Base EPS 分量 +13.3%/yr 對不上任何一個口徑。**
- FY26→FY31 CAGR ＝ 18.9%（§10.5 自陳）；
- 前瞻口徑（起點 FY28 $15.88 → 終點 FY31 $25.50，五年跨度）＝ (25.50/15.88)^(1/5)−1 ＝ **+9.93%/yr**；
- **13.3% 兩者皆非。**

**錯誤 4：回購被雙重計算。** Base 列 EPS 分量的備註明寫「diluted EPS 成長，**已含買回股數效果**」，然後同一列又加「+1.7%（股息 0.2%＋**買回貢獻 ~1.5%**）」。同一列裡買回算了兩次。

**正確且自洽的分解（請 writer 直接採用）**：報告 §10.5 已揭露現價用 FY28 forward 倍數、終端用 FY31 當年 EPS。在這個（報告自己選的）口徑下，唯一自洽的三分量是：

```
前瞻 EPS 成長：$15.88(FY28) → $25.50(FY31) 對應 5 年價格窗
                = (25.50/15.88)^(1/5) − 1 = +9.93%/yr
估值 re-rate  ：30.0x → 28.0x
                = (28/30)^(1/5) − 1     = −1.37%/yr
股息＋淨買回  ：0（已內含於 diluted EPS，不得另計）
合計           ：1.0993 × 0.9863 = 1.0842 → +8.42%/yr
```

**這個分解精確複現 §10.5 的 +8.4%/yr（我算 8.42% vs 報告 8.43%）**，證明 §10.5 本身是對的、錯的是 §10.6 的敘事。

**錯誤 5：Bear 列「≈-11.3%（單年，非 5 年年化，供對照）」在一張年化分量表裡不成立。** §10.5 Bear ＝ −60.6% 累積，年化 ＝ 0.3936^0.2 − 1 ＝ **−17.0%/yr**。§10.6 的 +2.9 − 15.1 + 1.0 ＝ −11.2% 既不是年化也不是累積，那句括號註記等於承認這一列沒有對帳。

**10Y 二段延伸複驗（這部分是對的）**：25.50 × 1.10^5 ＝ $41.07 ✅「~$41」；÷ $10.76 ＝ 3.82x ✅「3.8x」；$41 × 24x ＝ $984 ✅；(984/476.42)^(1/10) − 1 ＝ **7.52%/yr** ✅「7.5%」。10Y 這段自洽，不需修。

**為何機械 gate 沒攔到**：`verify_dd_math.py` 驗的是 §10.5 情境樹的 EV／IRR／AR 恆等式與必交模組存在性——§10.5 本身完全正確，所以 gate 正確地 PASS。**§10.6 是正文層的敘事分解，不在恆等式覆蓋範圍內。這正是 LLM critic 該補的位置。**

**修正指令（依序）**：
1. **§10.6 Base 列三分量整列換成上面的自洽分解**（+9.93% / −1.37% / 0），並在「質感解讀」段修正結論——目前寫「EPS 複利 +13.3%/yr 但幾乎被估值正常化 −6.1%/yr 吃掉大半」，**在正確數字下這句話是錯的**：真實情況是 EPS 貢獻 +9.9%、倍數只拖累 −1.4%，估值正常化根本沒有「吃掉大半」。這個修正**對裁決有利**（下行來自倍數的成分比報告自陳的小），所以更沒有理由不改。
2. **§10.6 Bull 列合計改為 +17.3%/yr**（與 §10.5 對齊），三分量按同法重算：EPS (33.00/15.88)^(1/5)−1 ＝ **+15.75%/yr**，re-rate (32/30)^(1/5)−1 ＝ **+1.30%/yr**，1.1575×1.0130 ＝ 1.1725 → **+17.25%/yr** ✅ 與 §10.5 的 17.3% 對上。
3. **§10.6 Bear 列改為年化口徑 −17.0%/yr**，刪掉「單年，非 5 年年化」那句自我豁免；三分量：EPS (12.50/15.88)^(1/5)−1 ＝ **−4.68%/yr**，re-rate (15/30)^(1/5)−1 ＝ **−12.94%/yr**，0.9532×0.8706 ＝ 0.8298 → **−17.02%/yr** ✅ 與 §10.5 的 −60.6% 累積對上。
4. **刪掉所有「股息＋淨買回」獨立分量**，或改為在 EPS 分量備註寫「已內含」並把該欄填 0——不得兩處都算。
5. 改完後**重跑 `verify_dd_math.py`** 確認恆等式仍 PASS。

### ⑥ 其他發現的內部不一致（非強制項，順手記錄）

- §9：「2024 年 7 月啟動 $400M 回購授權，2026 年 8 月用罄（累計 FY25-26 回購共約 **$281M**）」——$281M 用罄 $400M 授權需要 FY24 存量約 $119M，報告沒交代。
- §6「價值陷阱風險評級：**0個🟢低風險**」——「0個」後面沒有受詞，語句破碎（應為「0 個亮燈 → 🟢 低風險」）。
- §11.4 市值 $23.6B ÷ 現價 $476.42 ＝ 約 49.5M 股，× FY26 adj EPS $10.76 ＝ $533M，與 NOPAT $540.5M 量級一致 ✅ 這條對得上。

---

## ⑦ QC-54 白話呈現核 — 🟢 通過

| 檢核項 | 結果 |
|---|---|
| §1 結論開場為 2-4 句白話敘事（是什麼生意／為何這個裁決／什麼會改變它） | ✅ **通過**。「這是一門『只有三家公司做得出來』的生意…」整段四句，三個問題全答（生意＝航太引擎鎳基超合金與認證門檻；裁決＝治理已落地＋財測上修；會改變它的＝ATI 新產能會不會稀釋提價步調）。非矩陣語言開場 |
| §13 統一裁決開場為白話敘事 | ✅ **通過**。verdict-chip「進場」→ verdict-sub 一句話理由 → **「白話：」整段**（16,000 架積壓／全球只有兩家半／財報財測更好／CEO 插曲已由最熟的人接手／唯一新訊號是對手蓋一樣規模的產能）。不是機器矩陣開場，不觸發 🔴 |
| 決策矩陣逐 row 檢核表已收進 `<details>` 或附錄 | ✅ **通過**。完整 12 列矩陣＋裁決品質四問全部包在 `<details><summary>決策矩陣逐row檢核（點開看完整表）</summary>` 內，正文只留白話段 |
| 承重結論是否有僅靠燈號／emoji 而無完整白話句者 | ✅ **無違反**。逐項檢查：`moat_trend ↑`（§5 有完整句＋sourced 依據）、`runway_post_y5 🟢`（§6.A'' 有完整句）、`Max DD 🔴`（§12 有完整段落＋觸發時點＋復原路徑）、`trap 🟢`（§1 五問全文）、`val 🟡`（§10 診斷結論段）、§5.R 四個檢查點（每格都有 sourced 證據文字，非僅燈號） |

**唯一 🟡 nit**（不記違反）：§6 末「價值陷阱風險評級：0個🟢低風險」語句破碎，讀者無法從字面得知「0 個」指的是衰退信號亮燈數。建議改為「衰退信號偵測表 10 項 0 個亮燈 → 價值陷阱風險 🟢 低」。

**平衡評語**：這一軸報告做得確實好，§13 的「白話：」段落是我讀過的 v15 DD 裡呈現得比較乾淨的一份——它把「什麼會讓我改變主意」（對手也在蓋一樣規模的產能）放進白話段而不是藏在矩陣裡，這正是 QC-54 想要的東西。

---

## 需要 writer 修正的清單（依嚴重度）

### P0 — 必修，不修則報告的承重宣稱站不住

1. **【⑥c 🔴】§10.6 三分量整表重算**（Bull/Base/Bear 三列 ＋ 質感解讀段）。用上文給的自洽分解；刪除股息買回的雙重計算；改完重跑 `verify_dd_math.py`。**這是同一份報告對同一情境給出兩個相差 4pp 答案的問題，優先於一切。**
2. **【① 🔴】改掉「全球僅 3 家」四處**（h1 hypothesis-box／§1／§2／dd-meta `oneliner`），改為可查證的口徑；§5 市佔競爭表補 Aubert & Duval、Haynes(Acerinox/NAS)、Universal Stainless(Aperam) 三列。
3. **【③ 🔴】§6.H③ 刪除「未見 in-house 化跡象」**，改為 sourced 事實陳述（Airbus+Safran 2026-06 全資 A&D；Safran 明言垂直整合為戰略必需＋€150M 擴鍛造），並說明對 CRS 美系客戶敞口的實際影響。
4. **【③ 🔴】dd-meta `kill_metrics[]` 新增「OEM 垂直整合」一條**——這是下游 monitor 唯一看得見的介面，只寫散文等於沒寫。
5. **【⑤ 🔴】§3 新增「貿易政策與原料供應鏈」小節**（232 金屬衍生品 2026-04/06 重構、232 加工關鍵礦物 2026-01 公告與 2026-07-13 報告後續、鎳鈷來源地緣），每條標方向與 as-of。

### P1 — 應修，影響證據品質但不改變裁決

6. **【④】§13 決策矩陣 row 5 的「近月盤整 $465-496」換成正確區間**；附錄A 補 52 週高 $625.94／低 $228.88／距高點 −23.9%／YTD 漲幅。
7. **【④】§11.4 目標價註腳刪除「分歧點在 ATI」的無 source 歸因**，換成分析師自陳理由（KeyBanc「on valuation」下修等）。
8. **【④】新增空方論述對質段**（「78% 漲幅後轉賣出」、「valuation is this full, small disappointments matter a lot」），§1 trap box「空頭最強一擊」目前用的是自己設計的假想情境，應換成市場上真實存在的論述。
9. **【⑥a】§6.D 再投資率填入實際三個輸入值**或誠實降級為代理指標；穩態增量 ROIC 22% 給推導；`endo_growth_ceiling` 與正文算式對齊（22%×60%＝13.2 vs 機器欄 14.0）；缺口 8.1pp 的兩項歸因各給數字。
10. **【⑥b】§10.5 加倍數敏感度一行**（Base EPS $25.50 × 28x/24x/22x/20x → 年化 8.4%/5.1%/3.3%/1.4%），讓「進場」對終端倍數的曝險可見。
11. **【⑥b】Bull 列「20%/yr CAGR」標籤改為 25.1%/yr**（FY26 基期，與 Base 同口徑）；Base 路徑「逐年遞減成長率」的敘述與 FY29 加速的數字不符，二選一改。
12. **【② 】§3 供給側③改寫為「近 24 個月供給側移動清單」**（五條，每條標認證資格狀態）；§14 複審觸發新增「歐系／併購系產能取得美系引擎認證首例」。
13. **【⑥ 內部一致性】§4 資本支出 $300-315M 與 §1 的 $242.7M 二擇一並標明年度**；資本密集度比率隨之重算。

### P2 — 建議修，補完覆蓋面

14. 【⑤】§7 或 §4 補一句能源成本曝險（VIM/VAR 電力密集 vs 電價走勢），與報告自己的 IGT 需求論述互為鏡像。
15. 【⑤】補一句 AM／buy-to-fly 對每架飛機材料用量的長期影響（可判低風險，但要問過）。
16. 【⑤】勞工／工會、環保排放各補一句「未發現異常揭露」，不接受 0 提及。
17. 【⑥其他】§9 回購 $281M vs $400M 授權「用罄」的差額交代；§6「0個🟢低風險」語句補完。

---

## 未及查證清單（搜尋預算 10/10 用滿）

| 軸 | 想下的查詢詞 | 為何重要 |
|---|---|---|
| ⑤ 勞工 | `Carpenter Technology Reading PA United Steelworkers contract expiration 2026 strike` | 熔煉業工會合約到期是標準營運風險，報告 0 提及 |
| ⑤ 能源 | `specialty metals melting electricity cost 2026 PJM capacity price industrial power rates Pennsylvania` | 報告用資料中心電力需求當需求利多，卻沒問同一件事對自己的成本影響 |
| ⑤ 替代技術 | `additive manufacturing buy-to-fly ratio nickel superalloy demand reduction jet engine 2026` | 對按磅賣材料的公司，AM 降低每架飛機用量是結構性需求變數 |
| ① 競爭 | `VDM Metals Nippon Yakin Daido Steel aerospace nickel superalloy qualification GE Pratt 2026` | 日／德玩家是否具備美系引擎盤件資格，直接決定「僅 3 家」該改成幾家 |
| ② 供給 | `ATI Bakers South Monroe NC VIM furnace 2026 update capacity timeline` `Carpenter Athens Alabama commissioning progress 2026` | 兩條 H3／R2 的核心產能時程，我只有 writer 的二手轉述，未獨立驗證 |
| ③ 原料 | `nickel cobalt price 2026 surcharge lag Carpenter gross margin sensitivity` | surcharge 轉嫁的時滯與基準風險，報告直接歸為「噪音」未驗證 |
| ④ priced-in | `CRS short interest institutional ownership change Q2 2026` | 擁擠度／部位面，本次未觸及 |
| ④ 治理 | `Carpenter Technology board CEO succession plan after Thene August 2026` | §2.F Single Thing 的機率估計 5-8% 未獨立查證 |

---

## critic 給 orchestrator 的一句話

這份 DD 的**判斷機器沒壞**——ATI 對稱擴產是 writer 自己查出來推翻管理層舊敘事的，§10.5 情境樹的恆等式全對且 EPS 價差實質，§13 白話呈現是我讀過比較乾淨的一份。**壞的是三件事：競爭地圖漏掉整整一輪產業併購（含客戶把供應商買走這件事）、關稅／原料地緣整軸沒查、以及 §10.6 這張渲染給讀者的分解表跟它自己的 §10.5 對不起來。** 前兩件要求收緊宣稱與補監測項，第三件是純技術債必須重算。修完之後「進場｜核心」我認為守得住。
