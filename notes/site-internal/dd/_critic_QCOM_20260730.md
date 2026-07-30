# Cold-Review Critic — QCOM DD（2026-07-30，財報後 D+1）

**角色**：獨立產業 critic（未參與寫稿），冷讀本 DD 對產業態勢的關鍵判讀。
**背景**：QCOM 已於 2026-07-29 盤後公布 Q3 FY2026（季末 2026-06-28）；正常盤收 $155.68（−4.4%）、盤後再 −4.7% 至 $148.40。

---

## ① 競爭惡化

**🔴 報告判錯／漏掉：Qualcomm 手機 AP-SoC 整體份額已從 26% 掉到 22%（H1 2026 YoY），且輸給同業平均**
Counterpoint Research：H1 2026 全球智慧型手機 SoC 出貨量 YoY −15%，其中「Qualcomm 與 MediaTek 受創最重，出貨量估下滑約 25%」，Qualcomm AP-SoC 份額由 26%（H1 2025）降至 22%（H1 2026）。（[Counterpoint: Global smartphone chipset shipments down 15% in first half of 2026 - GSMArena](https://www.gsmarena.com/counterpoint_global_smartphone_chipset_shipments_down_15_in_first_half_of_2026-news-73928.php)；[Counterpoint SoC insight](https://counterpointresearch.com/en/insights/global-smartphone-soc-shipments-fall-15percent-yoy-in-h12026)）
這是**業界罕見的量化、可證偽的份額流失數字**，而且 Qualcomm 下滑幅度（−25% 出貨）超過同期 Apple／Samsung（皆有自研晶片撐盤，跌幅較輕）。本 DD 的「execution 8/10 擴大」敘事完全建立在新興線（Auto／hyperscaler custom CPU／IoT design win）上，卻沒有記錄核心業務（手機 SoC，佔 FY26 營收 ~56%）本身在**萎縮的市場裡還額外丟份額**這件事——這與「pricing power 縮減」是不同軸線的傷害（份額流失代表被排擠出設計，不只是議價力下降），且與 Apple 流失一樣屬於「已發生、可量化」的證據，不應該被完全排除在 moat_trend 判讀之外。
**建議修改**：把 26%→22% 這個數字明確納入 moat_trend 的判讀依據（獨立於 Apple、獨立於 pricing power），並在 §3 H1 中加註「非手機引擎需要跑贏的，不只是 Apple 缺口，還有手機主業自身持續流失的份額」。

**🟡 報告低估：Samsung Galaxy S26 是三星旗艦近三代來首次真正雙軌（Exynos 回歸），不只是「維持 70%」這麼簡單**
BofA／PhoneArena／SamMobile 等來源確認：Snapdragon 8 Elite Gen 5 整體拿下 Galaxy S26 系列約 70% 份額，Exynos 2600 拿下 30%；但拆分是**美/中/日全 Snapdragon、Ultra 全球固定 Snapdragon，歐洲與 RoW 的 S26／S26+ 標準款則是 Exynos**（[PhoneArena: The Exynos and Snapdragon split is real](https://www.phonearena.com/news/the-exynos-and-snapdragon-split-is-real-in-the-galaxy-s26-lineup_id178509)；[SamMobile 區域拆分](https://www.sammobile.com/news/galaxy-s26-plus-ultra-snapdragon-exynos-region-split-explained/)）。這是三星在 S23-S25 幾乎全 Snapdragon 之後，**首次系統性重建 Exynos 二源能力**（2nm 製程，[AndroidAuthority](https://www.androidauthority.com/exynos-vs-snapdragon-galaxy-s26-benchmarks-3653459/)）。「70% 份額守住」這個靜態快照沒錯，但**趨勢方向是三星正在建立可規模化的替代供應**——這是本 DD 完全沒提到的結構變化，即使這一代份額數字還撐得住。
**建議修改**：把「三星雙軌重建」記為 execution 軸的負向新證據（不是 pricing power），因為這是客戶主動培養二源、降低對 QCOM 議價依賴的具體行動，性質上與 Apple 流失同構。

**🔴 報告漏掉：Arm 自研 AGI CPU 與 Qualcomm Dragonfly C1000 的通路衝突已經是事實，不是假設性風險**
Arm 於 2026 年推出自研 AGI CPU（首次跳過純 IP 授權模式，136 核 Neoverse V3、TSMC 3nm），且已在 Computex 2026 公布 **ByteDance 與 Oracle 已採用** Arm 自家 AGI CPU（[Arm Newsroom](https://newsroom.arm.com/blog/introducing-arm-agi-cpu)；[EE Times](https://www.eetimes.com/arm-launches-first-silicon-cpu-targets-data-center-agentic-ai-workloads/)）。這代表 Qualcomm 鎖定的同一批 hyperscaler 客戶，**已有至少 2 家（ByteDance、Oracle）直接向 Qualcomm 的架構授權方（Arm）買競品晶片**——而 Dragonfly C1000 本身還是建立在 Arm 架構（Oryon 核心）之上，等於 Qualcomm 要跟自己的 IP 供應商正面搶客戶。美國 FTC 已於 2026-05 對 Arm 開反壟斷調查，正是查 Arm 是否會利用自己下場做晶片的地位「降級或拒絕」授權給 Qualcomm／Apple／Nvidia（[Data Center Knowledge](https://www.datacenterknowledge.com/data-center-chips/arm-enters-data-center-chip-fray-with-agi-cpu-for-ai-infrastructure)）。FTC 調查對 QCOM 是保護性的（若成立可保障其授權），但**現況本身（Arm 已搶下 2 家目標客戶）是對 H1／Data Center 論點的直接殺傷**，本 DD 完全沒有提及此矛盾。
**建議修改**：H1 的「已簽約/已下 PO」錨點需要加註「同一批潛在客戶中已有部分直接投向 Arm 自研方案」的抵銷風險。

**🟡 報告低估：Meta 對 Qualcomm 的「承諾」本質上是多源避險，不是排他委身**
Meta 與 Qualcomm 的 Dragonfly C1000 合作是「多世代」但**要到 2028 年才出貨**（[HotHardware](https://hothardware.com/news/qualcomm-lands-meta-as-partner-for-dragonfly-ai-chips)），同時 Meta 自身仍以 Nvidia GPU 為主、且持續投資自研 MTIA 晶片——Meta 是在同時下注 Nvidia／自研 MTIA／Qualcomm C1000（未來還可能加 Arm AGI CPU），並非把資源集中委身 Qualcomm。把「Meta 承諾」寫成 H1 的強錨點，容易讓讀者誤以為這是排他型合作。
**建議修改**：H1 措辭改為「Meta 已把 Qualcomm 納入多源名單之一」，降低錨點的確定性權重。

**🟢 報告判讀無虞**：MediaTek 維持龍頭（34% 2026E）、Apple 自研持續成長、Google Tensor／Xiaomi XRING 逐步擴大自研——這些既有威脅本 DD 的產業時鐘與 pricing power 判讀方向正確，無需修改。

---

## ② 供需 durability

**🟢 報告判讀無虞，且外部證據進一步強化本 DD 立場**
- BofA（2026-07 前後）明確指出記憶體供給限制「可能持續至 CY28」，直接支持 DD「無明確解除日期」的判讀（BofA downgrade 摘要）。
- SK Hynix「可能延續至 2030 後」與 Kearney PERLab 分析（短缺至少到 2030）皆與 DD 引用一致（[tech-insider.org](https://tech-insider.org/memory-chip-shortage-2026-ai-consumer-electronics/)）。
- IDC／Omdia 數據顯示 2027 僅溫和復甦（+1.9%）、2028 才明顯反彈（+5.2%），驗證「結構性而非週期性」且「無明確解除日期」的框架，同時補充了一個 DD 沒有的細節：**即使 2027-28 逐步復甦，$400 以下手機 2026 出貨仍將萎縮 22%**，代表低階機型的需求破壞可能比 DD 假設的更持久（[IDC](https://www.idc.com/resource-center/blog/global-memory-shortage-crisis-market-analysis-and-the-potential-impact-on-the-smartphone-and-pc-markets-in-2026/)）。
- 管理層「中國 Q3 見底、Q4 序列回升」的說法在 2026-07-29 法說會確認為「QCT handset revenues from Chinese customers estimated to reach a bottom in Q3...return to sequential growth in the following quarter」——與 DD「這是通路庫存去化完成、非終端需求復甦」的判讀一致，沒有證據顯示 DD 對此過度樂觀或悲觀。

**🟡 報告可補強一點**：DRAM/NAND 成本轉嫁的漲價（9/1 生效）本身會**進一步壓抑中低階手機終端需求**（memory 已佔中階機型 BOM 40%），形成「QCOM 漲價 → OEM 轉嫁給消費者 → 終端需求進一步萎縮 → QCT 出貨量再降」的負向循環，這一層傳導鏈本 DD 沒有明確畫出，值得在 §9 補一句因果閉環。

---

## ③ 其他結構變數

**🔴 報告漏掉：華為授權已經到期（既成事實，非假設性風險），且已實質壓縮 QTL**
本 DD H3 把「華為未續約」列為**風險項**（「不被…華為未續約結構性壓縮」），但事實是**該授權已經到期**，公司在 2026-07-29 法說會中已明確表示：假設不會有和解挹注本財年營收，且授權業務（佔總營收 14.8%）「本年度不會有成長」（[Yahoo Finance](https://ca.finance.yahoo.com/news/qualcomm-shares-fall-licensing-business-072726561.html)）。這不是「H3 的假設性風險」，而是**已經在發生、已被公司自己確認的基準情境**。QTL Q3 FY26 授權收入僅 $1,278M。
**建議修改**：H3 措辭應從「風險（尚未發生）」改為「已發生的既定利空，需回答的是華為是否會補簽 / 補簽後金額多大」，這是完全不同性質的假設風險敘述。

**🔴 報告完全未提：中國 SAMR 對 Autotalks 併購案的反壟斷調查，開案迄今未裁，最高罰款可達 $17.8 億**
2025-10-10，中國 SAMR 就 Qualcomm 收購 Autotalks（V2X 車用晶片，2025-06 完成交割但未依《反壟斷法》申報）立案調查，涉嫌「搶跑（gun-jumping）」。中國未申報併購案罰則上限為年度銷售額 10%——以 QCOM 2024 中國營收 $178 億計算，理論最高罰款達 **$17.8 億**（[Caixin Global](https://www.caixinglobal.com/2025-10-13/qualcomm-faces-china-antitrust-probe-over-unapproved-autotalks-deal-102371002.html)；[CNBC](https://www.cnbc.com/2025/10/10/qualcomm-shares-today-after-china-opens-antitrust-probe.html)）。截至 2026-07-30 尚未見裁決報導。
這件事本 DD 完全沒有提及，但時點上很敏感：**QCOM 對中國曝險本來就在惡化**（AP-SoC 份額流失、OEM 通路去化、Huawei 授權已到期），此時疊加一個開放中、罰款上限逾 17 億美元、且性質上帶有「中美科技摩擦籌碼」意味的監管懸案（多篇報導把此案定性為「不對稱貿易談判的一記警告彈」，見 [Tom's Hardware](https://www.tomshardware.com/tech-industry/china-probes-qualcomm-with-antitrust-investigation-in-the-latest-asymmetric-trade-negotiation-salvo-autotalks-acquisition-risks-fouling-anti-monopoly-laws)）。這屬於 §13 pre-mortem／§14 裁決應該至少列為監測指標的尾部風險，目前完全不在 DD 的雷達上。
**建議修改**：加入 §13 pre-mortem 情境或 §1 監測指標，追蹤 SAMR 裁決結果與罰款金額。

**🟢 報告判讀無虞（背景資訊，非對 QCOM 不利）**：FTC 對 Arm 的調查（見①）本質上是保護 Qualcomm 的授權地位，不構成對 QCOM 的額外結構性利空,但反向印證 Arm-Qualcomm 通路衝突的真實性（見①的 🔴）。

---

## ④ Priced-in

**🟡 報告方向正確，但低估了 Street 目標價「已經開始下修」的幅度與時間點**
- 盤前共識目標價 $221.23（對應 Monday 開盤 $166.97 有 31.27% 上檔，[TradingKey](https://www.tradingkey.com/analysis/stocks/us-stocks/262061307-qualcomm-qcom-q3-fy2026-earnings-preview-july-29-2026-tradingkey)）。
- 但**在正式財報公布前**，至少兩家主要券商已經下修：Cantor Fitzgerald 7/27-28 前後將目標價從 $220 下修至 $200（維持中性），理由是 CY2026 手機營收看衰至 $219 億（YoY −22%，遜於共識 $220 億），CY2027 EPS 估 $11.00（遜於共識 $11.40）（[Investing.com](https://www.investing.com/news/analyst-ratings/cantor-fitzgerald-cuts-qualcomm-stock-price-target-on-earnings-outlook-93CH-4814164)）；另有報導指 BofA 已將評等下調至「中性」並將目標價砍至 **$155**——這個數字已經非常接近財報後的實際股價（$148.40 盤後）。
- 這代表 $221 這個「共識」數字本身**已經是滯後指標**：市場真實定價早在財報公布前就已經開始朝下修正，不是本 DD 假設的「財報後才會被迫下修」這種未來式。換句話說，priced-in 的落差**沒有 DD 暗示的那麼大**——至少部分賣方（BofA）已經把目標價下修到接近甚至低於目前股價，代表「便宜」的判斷需要對照的不是 $221 這個過時均值，而是已經反映利空的個別下修後目標。
- 補充：財報前選擇權市場隱含波動對應約 9.34% 的預期波動（[TipRanks](https://www.tipranks.com/news/qualcomm-is-about-to-report-q3-earnings-options-traders-brace-for-a-9-34-move-in-qcom-stock)），實際兩日跌幅（−4.4% 正盤 + −4.7% 盤後，合計約 −9%）大致落在市場預期波動範圍內，**不算意外性巨大 outlier**，代表這不是一次「新增未知資訊」的黑天鵝式衝擊，QCT margin 下滑、記憶體壓力、中國疲弱這些訊息在財報前已被相當程度定價。

**建議修改**：§11.5／§14 的 priced-in 論述應更新為「共識均值滯後，但個股層級的目標價下修已經開始（Cantor $200／BofA $155），且盤前選擇權隱含波動已大致覆蓋實際跌幅」，這會讓「進場」論點更誠實（便宜是真的便宜，但不是「市場完全沒反應」式的便宜），也讓後續加碼判斷（本 DD 已設「加碼凍結至獲利橋樑數據點」）更站得住腳。

---

## 定向問題回答

### (a) moat_trend 標 → 是否站得住？

**站不太住——證據的重量已經接近推向 ↓，但不是壓倒性。**

站得住的理由（DD 原有論點仍成立）：
- 非手機引擎的錨點是「已簽約/已下 PO」而非純敘事：BMW 十年約、Meta 多世代 CPU 承諾、2 家 hyperscaler 客製矽已開晶圓（每家 FY27 預期 >$1B）、Azure HBC 部署——這些是真實、可查證的商業里程碑，execution 8/10 的評分邏輯是自洽的。

站不住／推向 ↓ 的新證據（本 DD 未處理）：
1. **26%→22% AP-SoC 份額流失（H1 2026 YoY）**——這是量化、可證偽、且輸給同業平均（−25% 出貨 vs Apple/Samsung 較輕）的份額流失，不是「Apple 一次性歸零」可以完全解釋的（Apple 是已知的既有事實，這是額外的、持續的侵蝕）。
2. **Samsung 首次真正雙軌重建**（Exynos 2600 進 S26/S26+ 標準款）——三星在 S23-S25 幾乎全 Snapdragon 之後首次系統性建立二源能力，這是客戶主動降低依賴的具體行動證據，性質與 Apple 流失相同（都是「大客戶內部化/轉單」），理論上應該用同一把尺衡量，而不是只記 Apple 不記三星。
3. **Data Center 引擎本身有未被記錄的執行風險**（見 (c)）：Arm 自研 AGI CPU 已拿下 2 家目標 hyperscaler（ByteDance、Oracle），與 Qualcomm 產生直接的通路衝突——若非手機引擎是 H1 用來抵銷手機主業惡化的支柱，而這根支柱本身開始出現裂縫，"holding" 的邏輯基礎就弱了。

**我的判斷**：如果 moat_trend 的定義是「護城河的方向性變化」，那麼「手機主業份額持續流失＋三星二源重建＋Data Center 抵銷引擎本身面臨 Arm 通路衝突」這三件事同時發生，比單純「Apple 流失（已計入等級）+ pricing power 縮減」的敘事更接近「多線同時弱化」。**這已經非常接近觸發 ↓ 的門檻。**是否真的翻轉為 ↓ 取決於一個判斷：非手機引擎的「已簽約/已下 PO」證據力道，是否強到可以完全抵銷上述三項新惡化證據——這是一個實質判斷而非機械公式，但本 DD 完全沒有討論前兩項證據（份額流失、三星二源），等於在沒有秤這把尺的情況下就判了 →。**至少應該把這三項證據明確納入討論，誠實秤重後再決定 → 或 ↓，而不是略過不提。** 鑑於 Hard Veto 的高槓桿後果（↓ + moat ≤ B → 迴避），這個秤重動作不能省略。

### (b) 「進場」是否過早？最強的「應維持觀望」論證

最強觀望論證如下：

1. **QCT margin 明確處於下降軌跡中，且尚未看到底部**：Q3 實際 EBT margin 26%（guidance 內），Q4 guidance 直接下修到 23–25%——這不是穩定在區間，是**guidance 本身就在往下修正**，而管理層唯一的對策（9/1 全面漲價）本質是成本轉嫁，DD 自己在 H2 也承認這只是 pass-through 非價值捕捉。在「guidance 本身正在惡化、修復手段是把壓力轉嫁給已經在萎縮的終端需求」的情況下入場，等於在下降趨勢中間接刀。
2. **FY27 EPS 共識尚未重設到位**：本 DD 自建 FY27 EPS $9.90（較盤前共識 $10.99 低約 10%），而外部賣方（Cantor）7 月底也才剛把 CY2027 EPS 從共識 $11.40 下修到 $11.00——代表**共識下修才剛開始，還沒完成**。历史上，在一個「guidance 連續下修 + 分析師估值模型還在追趕」的階段進場，承擔的是「下修尚未出盡」的風險，等 1-2 季看到 EPS 修正企穩後再進場，錯過的上檔有限，但躲開的是最不確定的階段。
3. **兩個未被計入的尾部風險同時存在**：SAMR Autotalks 反壟斷案（開案 9 個月未裁，罰款上限 $17.8 億）與華為授權已到期（非假設，已發生），兩者都在中國曝險已經惡化（份額流失、通路去化）的背景下疊加，構成 DD 沒有定價的額外不確定性。
4. **Data Center 抵銷引擎全部是未來式**：C1000 要到 2028 年才出貨，2 個 hyperscaler 客製矽方案「稍晚於 2026 年内首批出貨」，Meta 是多世代但非排他承諾——FY27 非手機 $21B 的目標（H1）要在營收貢獻幾乎還是零的當下就全額計入模型，是在為一個 2+ 年後才能驗證的敘事現在買單，而 Broadcom（>70%）與 Marvell（20-25%）在客製 ASIC 設計服務市場已有多年的 hyperscaler 關係與規模優勢。
5. 技術面 RSI 17.5、自高點 −43% 確實極度超賣，但**超賣出現在一個「連續兩季 guidance 下修 + 記憶體短缺展延到 2028 + 核心份額流失」的基本面惡化週期中間**，「便宜」與「觸底」是兩回事——等 QCT EBT margin 至少連續一季站穩在 guidance 區間下緣以上再進場，犧牲的上檔有限（衛星倉位帽 3%、首階僅 1/3），但可以避免在下修週期未走完前被迫承受最深的那一段。

**結論**：觀望論證相當紮實，尤其（b）與（a）互相加強——如果 moat_trend 的秤重結果偏向 ↓，兩者疊加會直接觸發 Hard Veto。即使維持「進場」，本 DD 至少應該把「加碼凍結」的邏輯，延伸成「首階進場本身也應等到 QCT margin 出現企穩訊號」的更保守版本，或明確承認這是在下修週期未完成時進場的主動選擇（並說明為何值得承擔這個時序風險）。

### (c) Data Center $5B（FY27）／$15B（FY29）目標可信度

**可信但不宜當作「已鎖定」的核心假設，屬於高變異、需要持續驗證的押注，而非可押注的既定事實。**

支持面（DD 已正確引用，真實可查證）：
- 2 個 hyperscaler 客製矽合作，每個 FY27 預期 >$1B（[TrendForce](https://www.trendforce.com/news/2026/04/30/news-qualcomm-reportedly-to-supply-custom-chips-to-a-hyperscaler-in-december-quarter-expands-data-center-push/)）。
- HBC/C1000 從立項到 tape-out 約 9 個月，速度確實優於一般 ASIC 開發週期（Futurum 分析）。
- Meta 多世代 CPU 承諾、BMW 十年約，都是真實簽約而非意向書。

質疑面（sourced，本 DD 未涵蓋或未充分權重）：
1. **C1000 旗艦產品 2028 年才出貨**——屆時 Broadcom（Google TPU、OpenAI custom chip）與 Marvell（AWS Trainium、Microsoft Maia）已經是多世代量產、合計占客製 ASIC 設計服務市場 90%+ 的在位者（[hashrateindex](https://hashrateindex.com/blog/design-partners-ai-asic-market-part-2/)）。Qualcomm 是後進者，時間窗口對它不利。
2. **Arm 自研 AGI CPU 已經拿下 ByteDance 與 Oracle**——這兩者都是 Qualcomm 潛在目標客戶池的一部分，且 Arm 的方案某種程度上與 Qualcomm 自家（同樣架構於 Arm 之上的）Dragonfly 直接競爭。這是「TAM 被自己上游供應商分食」的具體先例，不是假設性威脅。
3. **「中立性」信任問題已被賣方分析師公開點名**：「一個可信的第三方客製夥伴不應該同時跟自己的商用產品競爭」（[jonpeddie.com](https://www.jonpeddie.com/news/qualcomm-ai-asic-hyperscalers-automotive-data-center-arm-broadcom/)）——Qualcomm 同時是merchant CPU/SoC 供應商、又要當客製 ASIC 夥伴，這個雙重身份本身就是客戶疑慮的來源；ByteDance ASIC 交易宣布當天 QCOM 股價還一度重挫 8%（連動 Marvell −10%），顯示市場對這類交易的解讀本身充滿不確定性（出口管制疑慮＋零和競爭疑慮），並非單純利多。
4. **Meta 的承諾是多源避險，非排他委身**（見①）——即使 Meta logo 算入 win，也不保證錢包份額，只保證「入圍資格」。
5. 本次搜尋沒有找到 Qualcomm 相關客製 ASIC 專案被取消的具體先例，但 hyperscaler「雙軌並行（自研 ASIC + Nvidia GPU + 多家供應商）」本身就是產業公認的預設策略（非特例），意味著即使關係維持,實際訂單規模仍可能被稀釋或延後,而不需要正式「取消」。

**淨判斷**：這些錨點（已下 PO、已 tape-out、已簽約）比純敘事型的產業展望強，值得在 GRP／衛星倉位邏輯裡保留席位——但 $5B/$15B 這兩個數字本身建立在「Qualcomm 在 2028 年才交付的旗艦產品要打贏一個已經被 Broadcom/Marvell 佔據 90% 份額、且 Qualcomm 自己的 IP 供應商 Arm 已經親自下場搶客戶」的競爭格局，屬於**高變異、多年期才能驗證**的押注,不應該被當作可以直接拿來抵銷「手機主業份額流失＋華為到期＋中國監管懸案」這些已發生負面證據的等重籌碼。這正是回答 (a) 的關鍵——如果 H1／Data Center 這根抵銷手機惡化的支柱本身可信度打了折扣,moat_trend 標 → 而非 ↓ 的理由就更站不住。

---

## 總結（給用戶的一句話）

四軸中，②供需 durability 判讀站得住甚至被外部證據加強；①競爭惡化與③其他結構變數各有至少一項本 DD 完全沒提及、且 sourced 的實質性負面證據（AP-SoC 份額 26%→22%、三星 Exynos 二源重建、Arm 自研 AGI CPU 搶下 ByteDance/Oracle、華為授權已到期非假設、SAMR Autotalks 反壟斷案未裁）；④priced-in 方向正確但低估了目標價下修「已經在發生」的事實。這些證據合在一起，**足以要求對 moat_trend → vs ↓ 的判斷重新秤重**——這直接牽動 Hard Veto（↓ + moat ≤ B → 迴避）的觸發與否，是本次 critic 最需要用戶/寫手正視的單一問題。
