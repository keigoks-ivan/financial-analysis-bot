# 寫稿後獨立 critic — DD_MRVL_20260831.html（v15.0, 115.3KB）

- **critic 模型**：opus（跨模型冷讀；writer＝sonnet，未參與寫稿）
- **合併載具**：QC-41 ＋ QC-48（未觸發，26 週漲幅 +165.4% 已擋下 8a）＋ QC-50（不適用，本次非觀望）＋ **持有人加簽：翻面驗證**（最高優先）
- **as-of**：2026-08-31｜查證輪次：14 輪 WebSearch（合併載具上限 14）＋ 全檔內部複算＋前份 DD（2026-06-23）逐條對讀
- **機械 gate**：`scripts/verify_dd_math.py` → pass（唯一告警「§5.F 僅 1 處痕跡」經人工核對為**誤報**，本體俱在）
- **裁決標的**：統一裁決 進場・核心（自 2026-06-23 的觀望翻面）

---

## 〇、翻面驗證（持有人加簽任務，最高優先）

### (1) 前份 DD 觸發器原文比對

前份 `DD_MRVL_20260623.html` 對「加碼重啟」的表述**在同一份報告內有三個版本，彼此不一致**：

| 出處 | 原文 | 條件數 |
|:---|:---|:---|
| §3.E 可執行決策主線 | 「FY+2 PE 回落至 ≤35x（≈ $216，估值🟡）**且** DC 段 YoY 仍 >20%」→ 分批建/加，**首階 1/3** | 2 |
| §14b 加碼與減碼條件 | 「FY+2 PE ≤35x（≈$216）**+** DC 段 YoY >20% **+ custom 守住 Maia**」→ ~4% | **3** |
| §14a 目標倉位 | 「條件＝FY+2 PE ≤35x **+ custom 風險出清**」 | 3 |
| §1 最關鍵監測指標 #3 | 「PE(FY+2) 回落至 **30x 以下**（＝估值修復、轉進場觀察）」 | 另一門檻 |

新報告 §13 寫：「上份報告（2026-06-23）**§2.E／§13b** 明訂加碼重啟觸發器為『FY+2 PE 回落至 ≤35x（≈$216）且 DC 段 YoY 仍 >20%』……**三項觸發器條件皆已發火**」，並於 §11.3 斷言「**方法論未變（同一套決策矩陣、同一組門檻）**」。

**比對結論**：對 §3.E（新報告誤稱 §2.E）而言引用忠實；**對 §14b（新報告誤稱 §13b）而言不忠實**——第三條件「custom 守住 Maia」被整條刪除，§14a 的「custom 風險出清」亦未出現，§1 的 30x 版本亦未揭露。前份報告內部的**分歧被轉述為一致**，違反站內引用忠實性原則；而 QC-49 指名的引用對象正是「前次報告 **§13b 加減碼觸發**」，即三條件版本。

### (2) 現行數字獨立查證（全部通過）

| 承重數字 | 報告值 | 獨立查證 | 判定 |
|:---|:---|:---|:---|
| 收盤價 | $216.62（8/28） | $216.62，−10.28%，日高 $228.88／日低 $216.00 | ✅ |
| FY+2 PE | 34.27x | 216.62 ÷ 6.32 = 34.276 ✅ 算術正確；6.32 為 Excel buy-side snapshot（外部無同口徑公開值可交叉，見 🟡-8） | ✅（算術）／⚠（分母口徑） |
| DC 段 YoY | +46%（Q2 FY27） | $2.172B，+46% YoY、+18% QoQ、占營收 79% | ✅ |
| Q3 DC guide | ~+75% YoY | 管理層「DC 環比 >20%、YoY 約 75%」 | ✅ |
| 總營收／EPS | $2.739B／$0.94 非 GAAP | $2.739B（+37%）／非 GAAP $0.94／GAAP $0.33 | ✅ |
| Q3 guide | $3.15B±5% | $3.15B±5%，非 GAAP EPS $1.10±0.05，GM 57.5-58.5% | ✅ |
| FY27／FY28 展望 | ~$12B／~$18B | ~$12B（+45%）／~$18B（+50%，前值 $16.5B） | ✅ |
| Google warrant | 58.97M 股＠$206.58、~$12.2B、240×$500M、上限 $120B 至 FY2033 | 逐項相符 | ✅ |
| 分析師目標 | 高 $400／中位 $276／低 $126（n=44） | n=44、均值 $279.62／中位 $275／區間 $126-400 | ✅ |
| AVGO Q3 FY26 AI 半導體 | guide $16B（+200%） | $16.0B，+200% YoY | ✅ |

**價格腿與成長腿確實發火**，此部分無疑義；問題全在第三條件與轉述完整性。

### (3) 被靜默丟棄的條件／保留（本次最重要的發現）

- **「custom 守住 Maia」條件**：公開資訊顯示 Microsoft Maia 200（2026-01 發表）**Marvell 並非該加速器供應商**，僅被點名可望在 Ethernet ASIC 側受惠；Maia 300 目前僅有 Wedbush「可能是機會」等級的賣方推測，非確認贏單。新報告 §6.H 卻寫「Microsoft（Maia 客製 + Azure HSM 長期合作，**關係穩定**）」，全檔未出現「Maia 200／Maia 300 socket 歸屬」的正面交代。**前份報告設下的第三道閘，證據面偏向未通過，而新報告的處理是不提。**
- **§2.F Single Thing 被窄化**：前份為「下一個 top-4 hyperscaler custom socket 的去向：**Trainium4、Microsoft Maia gen3、或 Meta MTIA 次代**」；新份改為「**AWS 旗艦 custom XPU 社羣下一代**」單一標的。Maia／MTIA 兩個證偽點被移出證偽集，§14 複審表亦未保留。窄化本身可以是正確的判斷，但**必須寫出來並給理由**，不能靜默發生在一份翻面報告裡。
- **H1 前提被改寫**：前份 H1 白紙黑字「AWS **連兩代失單（Trn3+Trn4 均落 Alchip）**」（當既成事實處理）；新份改為「Trainium3/4 **部分份額**……賣方通路調查指向轉移，公司從未證實或否認」。就外部證據論，新份的軟化其實**更接近事實**（Benchmark 事後已實質收回「全失」說法、JPM 明言未失份額），但 §11.3 只做了「價格變了／基本面變了／方法論未變」三元歸因，**完全沒有記錄前份的核心事實前提已被推翻並重寫**。翻面報告最該交代的一件事被漏掉。

---

## 一、🔴 必須修（must fix）

### 🔴-1｜§13 hysteresis 引用／§11.3｜觸發器引用不忠實，且「同一組門檻」為不實陳述
- **問題**：見上 (1)(3)。新報告漏引前份 §14b 的第三條件「custom 守住 Maia」與 §14a 的「custom 風險出清」，將 §3.E 的二條件版本同時掛名 §13b（章號亦誤，前份決策層是 §14 不是 §13），並宣稱「三項觸發器條件皆已發火」「同一組門檻」。同時前份 §1 監測表的 30x 門檻（現值 34.27x 未達）未揭露。首階倉位亦由前份指定的 **1/3 改為 1/2**，無說明。
- **證據**：`docs/dd/DD_MRVL_20260623.html` §1／§3.E／§12 矛盾表／§14a／§14b 原文（見上表）；Maia 200 供應商歸屬（Wedbush 評論，2026）。
- **為什麼是 🔴**：QC-49 的引用對象即前次 **§13b（本案為 §14b）加減碼觸發**；引用不全＝無法證明觸發器「完整發火」，而 QC-49 的 fail-safe 是**承繼前次裁決（觀望）**。這是唯一直接通往裁決層的缺陷。
- **最小修法**：§13 hysteresis 段改為忠實三行——① 逐字列出前份 §14b 三條件；② 逐條標記發火狀態（PE ✅／DC ✅／custom 守住 Maia ＝**未達成或無法證實**，附 sourced 說明）；③ 明寫「前份報告內部對重啟門檻有 30x 與 35x 兩個版本、對 custom 條件有 2 條與 3 條兩個版本，本次採用 ___ 版本，理由是 ___」，然後才下翻面結論。§11.3 刪除「同一組門檻」，改為「門檻項目已變更（減一條 custom 條件），變更理由＝___」。首階 1/2 vs 前份 1/3 的差異寫一句。

### 🔴-2｜§2.F／§14｜Single Thing 靜默窄化，Maia／MTIA 退出證偽集
- **問題**：見上 (3)。單一 binary trigger 由「三選一 top-4 socket」縮成「AWS 一家」，§14 複審表第 3 項同步只剩 AWS。結果是：即使 Maia 300 或 MTIA 次代落給對手，本報告的證偽機制**不會亮燈**。
- **最小修法**：§2.F 恢復三 socket 並列，或明寫「本次將 Single Thing 窄化為 AWS，理由＝___（例：Maia 本體本就非 Marvell 承接、MTIA 規模不足以撼動 thesis）」，並在 §14 補回對應觸發列。§6.H 對 Microsoft 的「關係穩定」須改為有 sourced 的具體陳述（哪一代、哪一個產品線）。

### 🔴-3｜§6.D／§5.R③｜內生天花板算錯：ΔWC 與 10-K 對不上，疑似把 FY27 的產能預付款計入 FY26
- **問題**：報告寫「(Capex−D&A+ΔWC)÷NOPAT=(0.36−1.29+**2.15**)/2.546≈48%」，天花板＝48%×70%≈34%。但 FY2026 10-K（截至 2026-01-31）：AR $2,186.6M（前期 $1,028.4M）、Inventories $1,388.0M、**Accounts payable $1,073.8M**。ΔWC(AR+存貨−應付) ≈ +1,158 +360 −350 ≈ **+$1.17B**，不是 $2.15B。差額 ≈ $1.0B，恰等於報告自己描述為「**FY2027** 規劃約 $1B 產能預付款」——高度疑似**期別錯置**（FY27 的現金流出被計入 FY26 的 ΔWC）。報告 §7.E 自陳「DPO 因採集腳本應付帳款欄位對齊異常暫缺」，即**應付帳款這一項當時取不到**，卻仍output了一個含應付的 ΔWC。
- **重算後果**：再投資率 48% → **~9.4%**；天花板 34% → **~6.6%/yr**（沿用同一個仍未推導的 70%）。§10.5 的「內生天花板 sanity check：Base EPS CAGR 貢獻 30.1% vs 天花板 34% → **在天花板內 ✅**」隨之翻為 **⚠ 超出**，依 SKILL.md 規則「超出 ⚠ → §10.5 Bear 機率**強制 ≥30%**」（例外只給「缺口已歸因到 §3.F 有 sourced 的新 segment／新 S 曲線」，而報告給的歸因是 OM 擴張＋淨回購，不符例外）。dd-meta `endo_growth_ceiling=34.0` 為下游直讀欄位，錯值會外溢。
- **附帶（PLTR 型退化）**：增量 ROIC 「**~70%**（fabless 模式下成長多靠費用化 R&D……**此為估算值**）」全無推導。這正是強化職責書 (b) 要抓的形狀：一個沒有算式的數字乘上一個算錯的數字，得出全報告最承重的天花板。fabless 的正解是把 R&D（~25-30% of revenue、年 $2.2-2.5B）資本化後再算 ROIIC；若不做，就應誠實輸出「本案 ROIIC 不可計算」並走 ⚠ 路徑。
- **最小修法**：① 用 10-K 三個科目重算 ΔWC 並標 as-of；② 增量 ROIC 要嘛給資本化 R&D 的推導、要嘛標「不可計算」；③ 依重算結果重跑 §10.5 sanity check，若 ⚠ 則 Bear 機率調至 ≥30%（重算 EV：Bull30/Base40/Bear30 → **+64.6%**、年化 ~10.5%，方向不變但須誠實下修）；④ 修正 dd-meta `endo_growth_ceiling`。

### 🔴-4｜覆蓋面缺軸：記憶體（DRAM／HBM）成本通膨 vs 毛利率企穩假設
- **問題**：全檔零次提及記憶體成本。而「非 GAAP GM 守住 57.5-58.5%」同時是 **H3 的數字門檻**、**R2 的減碼觸發**、**兩條加碼條件之一**、**§1 陷阱判定的第三條退出信號**——是全報告被引用最多次的單一假設。報告把毛利率下修 100% 歸因於「custom 組合稀釋」，並全盤採信 CFO 的「非競爭定價壓力」，未檢驗任何成本側變數。
- **證據（as-of 2026）**：DRAM 價格 2025→2027 累計漲幅約 275-300%；TrendForce（2026-06-02）預期 HBM 合約價 2027 年**倍數級上漲**，三大廠售罄、短缺延續至 2027 以後；Goldman 預估 custom ASIC 用 HBM 需求 +82%、占市場三分之一。Google 協議本身涵蓋 **memory interface controllers 與 near-memory compute**，Marvell 另有儲存控制器線——成本與客戶系統預算兩條路徑都通到毛利率。
- **為什麼是 🔴**：缺軸本身即 🔴，不需先證明結論錯（強化職責書 (a)）。且此軸若成立，打的正是報告最承重的那條假設。
- **最小修法**：§7 或 §5 加一段「記憶體成本通膨對 GM 企穩假設的敏感度」，帶 sourced 數字與 as-of；§2.C R2 的警戒閾值補上「若毛利率未達 57.5% 且公司歸因由 mix 轉為投入成本 → 性質改變，須重評 H3」。

### 🔴-5｜覆蓋面缺軸：AI 資本支出消化／債務融資／折舊爭議（且是前份風險表被靜默刪除的一條）
- **問題**：前份 §3.C **R3＝「AI capex 消化 + 半導體 multiple 系統性下移（2027 capex +80% vs 雲收入 +15%、ROI／電力約束）」，⚡短期（1-2 季可觸發）**，漂移觸發「top-4 capex guide 首次 YoY 轉負」。新份 §2.C 的三條風險換成 R1 custom／R2 毛利率／R3 CPO，**capex 軸整條消失且未說明**。新份 H3 雖仍宣稱「AI 資本支出多年結構性不反轉」，但其數字門檻與漂移觸發**全部是毛利率與 OM**——H3 的 capex 這條腿**沒有任何監測指標、沒有任何證偽器**。
- **證據（as-of 2026）**：主流預估 hyperscaler capex 增速由 2026 的 +51% 降至 2027 的 +13%、2028 約 +5%；增量負債占 capex 由 FY24 的 9% 升至 2026 年中的 LTM 32%，五大廠自 2024 底起舉債逾 $137.5B；折舊年限（5-6 年 vs 經濟壽命 2-3 年）爭議估計 2026-28 少認列約 $1,760 億，且 FASB 新揭露要求要到 FY2027 才上路——資訊最不透明期與折舊壓力最集中期（2027-2029）重疊。
- **為什麼是 🔴**：一份把裁決升到 **進場・核心、持有 5-10 年**的報告，對其最大外生驅動變數不設證偽器；且這是**前份報告有、本份沒有**的靜默倒退（與 🔴-1／🔴-2 同一模式）。
- **最小修法**：§2.C 補回 capex 消化風險列（時間尺度、監測指標＝top-4 capex guide 方向與融資結構、警戒閾值），H3 的漂移觸發補上 capex 腿。

### 🔴-6｜§5.F 對手 P&L 空殼化（決定性對手 Alchip 四欄「資料不足」）＋ §7 同業組違 QC-5
- **問題**：§5.F 本體確實存在（機械 gate 誤報，見 🟢-3），但 Alchip 欄位 5 格中 4 格寫「資料不足」，理由「台灣上市，非美股可比」。Alchip（3661.TW）是上市公司，法說與財報公開，且它是本報告 §2.F Single Thing、§5 威脅表 🔴 級、§5 賽局結構判定的**唯一具名對手**。另 §7 三年趨勢同業欄只有 Broadcom 一家，違反 QC-5「必須用與 §10.4 相同的對手組（至少 3 家）；**禁止只放 1 家**」。
- **可得且具決定性的公開數字（as-of 2026）**：Alchip Q2 2026 營收 **$241.7M、QoQ +82.6%**（Q1 $132.4M），由 N3 加速器量產帶動；毛利率 Q1 **50%**，因量產占比升至 80-90% 而 Q3/Q4 將落至「20% 出頭」、全年低至中 20 段；目標營業利益率「high 10s」；**下一代 N2 專案（Trainium 3）採異質 chiplet 設計、需多次 tape-out**。
- **為什麼是 🔴**：① 必交量化模組對決定性對手交白卷；② 這些數字**直接反駁**報告全盤採信的「毛利率下滑純屬 mix、非競爭定價壓力」——一個願意以 20% 出頭毛利率承接量產的對手正在同一批 socket 上放量，是「競爭定價壓力」的第一手證據，至少須被正面處理；③ Alchip 自家法說談 N2＝Trainium3 專案，是比「賣方通路調查」強一級的來源，而 §8.5 ④仍把該證據層級標為「僅賣方通路調查非公司揭露」。
- **最小修法**：§5.F 用公開數字填滿 Alchip 欄並補第三家（Astera Labs／Credo／GUC 擇一，與 §10.4 對齊）；§5 賽局結構段補一句「對手以低毛利率承接量產」的定價壓力判讀；§8.5 ④ 證據層級由 med 上修並註明來源型態。

---

## 二、🟡 應該修（should fix）

- **🟡-1｜§1／§8②／§11.3：FY2028 展望被單向描述為「上修」**。市場當日的主導敘事是「**上修幅度不及預期**」——路透系報導「未能對長線營收展望提供有意義的上調，令期待 Google 協議加速成長的投資人失望」，CNBC「outlook underwhelms」，多家標題直指 FY2028 指引與 Google 時程。報告在 §1 陷阱表把「guidance 連兩季上修」列為「支持不是陷阱的最強論據」，在 §11.3 把它當作翻面的基本面腿，卻未載這一層保留。**修法**：§8② 補一句「FY28 上修至 ~$18B（前值 $16.5B），惟低於協議公布後的市場期待，是當日下跌的主因之一」，§11.3 的基本面腿隨之校準。
- **🟡-2｜§6.E：壓測只壓倍數不壓 EPS，結論被過度外推**。三情境對 FY29 EPS 一律用共識 $9.54（該數字內含 ~50% CAGR），只調整倍數。樣板文義允許此作法，但報告據此宣稱「15% 成長情境下跌幅有限（−3.1%）→ 現價已對成長顯著放緩有相當程度定價，是 val=🟡 而非 🔴 的數字基礎之一」——**不成立**：真的降到 15% 成長，FY29 EPS 不會還是 $9.54。**修法**：保留表格，刪除該推論句，或補一列「EPS 同步下修」的敏感度。（§10.5 Bear 有實際壓 EPS 至 $8.38，作法正確，問題只在 §6.E 的引申。）
- **🟡-3｜附錄 A Bear anchor：PE 取值與自引章節不符**。報告寫「Bear PE=22x（**§6.E 10% 成長情境**）」，但 §6.E 的 10% 情境是 **18x**（22x 是 15% 那一列）。依規則「Bear PE 來源＝§6.E 成長熄火『降至 10%』情境」，正解為 $3.654×18＝**$65.8（−69.6%）**，非 $80.4（−62.9%）。
- **🟡-4｜§5.R③ 與 §10.6 互相矛盾**。§5.R③ 把「**淨回購對每股盈餘的貢獻**」列為 16pp 缺口的歸因之一；§10.6 卻寫「股息+淨買回**約打平**（股息率 <1% 抵消淨稀釋）」；§9 資本配置計分卡更顯示 diluted WASO 由 883M 增至 921M（**+4.3%，淨稀釋**）。同一份報告三處對同一項給了三個方向。**修法**：統一為「淨稀釋／約打平」，並把缺口歸因改寫成只剩 OM 擴張一項（約 +2%/yr，遠不足以橋 16pp——這也回頭支持 🔴-3 的處置）。
- **🟡-5｜§3③ 中國曝險數字為前份 carry-forward，未以最新 10-K 更新**。報告寫「10-K 地理揭露顯示帳列中國/亞洲地區營收占比 **~38-44%**」；FY2026 10-K（FY 截至 2026-01-31）實際為**中國 $2,969.9M ＝ 36%**（台灣 20%、美國 14%）。「直接受管制營收 <5%」是把 10-K 質性語句（「輸往中國的出貨絕大多數係銷予在中國設有工廠或委外製造據點的非中國客戶」）量化成的推估，報告已標 med 信心尚屬誠實，但數字本身無一手佐證。另「2026 年 1 月 BIS 新許可政策（含潛在 15-25% 中國營收分潤／關稅要求）」本次未能獨立查證，建議降級為「待證」或補來源。
- **🟡-6｜§10.5 10Y 二段延伸內部不對帳**。5Y Base 1.676x × 第二段 EPS CAGR 15%×5 年（2.011x，倍數不變）＝ **3.37x → 10Y IRR 12.9%/yr**；報告寫 **2.7x／10.4%/yr**（其自身內部自洽：1.104^10＝2.69）。差額隱含終端倍數自 24x 再壓至 ~19x，但未言明。runway 🟢 觸發的必填欄位，推導應寫出來。
- **🟡-7｜§6.I 分部前瞻有 plug 與方向衝突**。FY29「交換/儲存/其他 DC」由 FY28 $3.45B **降至 $2.3B（−33%）**僅標「外推、占比壓縮」，實為湊出段加總 $24.0B 的配平項；一個絕對值衰退三分之一的分部不該無解釋。另 custom FY27 僅 +27%（DC 三段中最慢），與同報告 §8 引用的管理層「custom 於 FY27 下半年顯著加速」語氣相左，至少須加一句 1H/2H 拆分說明。
- **🟡-8｜§10.1 分位 ~55% 是估計、無 QC-4 公式，卻是 val 燈的兩個輸入之一**。報告已誠實揭露 EPS 基期重塑導致 5 年同口徑不可得，但 val 🟡（→ 決策矩陣 row 9/10 → 進場）實際上是「不可靠的 55% ＋ PEG 0.69 取較嚴」的產物。**修法**：明寫「val 🟡 實質由 PEG 單支撐，分位僅供背景」，或改用可算的替代錨（EV/Sales 或 P/FY+2 Sales 分位）並附公式。同理，FY+2 EPS $6.32 僅有 Excel buy-side snapshot 單一來源，建議補一個外部同口徑交叉點。
- **🟡-9｜§5 moat_trend「→」的 holding 可守，但兩側證據都需補正**。① 抵銷證據（Google 協議）依管理層自陳為 **back-end loaded、FY2029+ 才有實質貢獻**，而 AWS／Maia 風險的解析窗是 12-24 個月——**時間錯配**應在 §5 寫明，否則「反證足以防止降為 ↓」的推理少了一層；② 反向亦然：Benchmark 事後已實質收回「Trn3/4 全失」的說法（改稱 AWS 增列 Alchip 支援而 Marvell 仍在位）、JPM 明言 Microsoft／Amazon 均未失份額、CEO 公開稱未丟訂單——§8.5 ③跨文件分歧只列了 RBC 一側，漏了這兩條，使「AWS 份額確有 sourced 下滑證據」的力度被高估。兩處都補上後 → 仍維持 →，但推理才站得住。
- **🟡-10｜§10.4／§13a opportunity cost：對 AVGO 的溢價論證與 sourced 數字相左**。報告以「MRVL 成長更快」支撐 34.3x vs AVGO 20 出頭倍，並據 GRP 三閘建議「邊際資金優先回補 MRVL 而非新增 AVGO」。但 Broadcom 已重申 **FY2026 AI 半導體 $56B、FY2027 >$100B（+79%）**，高於 Marvell DC 段隱含的 +54~60%；相對份額不只是「未見擴大」，而是**持續被稀釋**。**修法**：§10.4 的溢價理由改用可辯護的口徑（例如 MRVL 公司級營收成長 vs AVGO 公司級），並在 §13a 重新論證 GRP 結論或降低其強度。

---

## 三、🟢 判讀無虞（記錄以供對照）

- **🟢-1｜情境樹 EPS 價差實質，非倍數驅動退化**。FY31 EPS Bull $19.01／Base $15.13／Bear $8.38（Bull vs Base +25.6%，Bear vs Base −44.6%），倍數 30x/24x/16x；Bull 相對 Base 的 +163% vs +67.6% 約由 EPS（1.256x）與倍數（1.25x）各半貢獻——**未出現 PLTR 式「Bull 全靠終端倍數」的退化**。三情境股價、5Y%、IRR、機率加總（30/45/25）、EV +69.9%、年化 11.2%、AR 5.14 全部複算相符。
- **🟢-2｜IRR 內部對帳自洽**。§10.6：EPS 腿 (15.13/4.06)^(1/5)−1＝+30.1%；re-rate 腿 (24/53.35)^(1/5)−1＝−14.8%；幾何合成 1.301×0.8524−1＝**10.9%**，與 §10.5 Base 一致；現價 FY+1 口徑 53.35x＝216.62/4.06 正確。§10.5↔§10.6↔頁首三處無分歧。
- **🟢-3｜§5.F 本體存在**——`verify_dd_math.py` 的「僅 1 處痕跡」為誤報（表格＋兩段 ≥60 字對手經濟體質敘述俱在）。內容品質問題見 🔴-6，非存在性問題。
- **🟢-4｜承重外部數字全數通過獨立查證**（見〇(2) 表，10 項全 ✅）。§4 EPS CAGR 49.8%、PEG 0.69、FCF margin 17.0%、D/E 0.335、ROIC 13.5%＝31.0%×0.4364、回購/FCF 76.6%、品質分 (8.5+9.5)/2＝9.0、§6.E 四列隱含股價與跌幅、附錄 A 短中期 R:R 亦逐一複算相符。
- **🟢-5｜決策矩陣機械面正確**。無 Hard Veto（signal A、moat_trend →、thesis 非不可調和）；Soft Veto 四項未命中；row 8a 因 26 週漲幅 +165.4% > +150% 被反動能閘正確擋下（該數字亦合理——2026-03-24 DD 記載當時股價 $89.81，216.62/2.654≈$81.6 與 26 週前價位相容）；落 row 9/10（signal ≥A ＋ val ≤🟡 ＋ MA ✅）→ **進場**，推導無誤。
- **🟢-6｜QC-51 無需分歧說明**。30 天內同形狀 peer：NVDA（2026-08-31，進場・核心）、TSM（2026-08-08，進場・核心）皆同向；CRDO（2026-06-23，觀望）已逾 30 天，且其 signal B 觸發 row 6 Soft Veto，與本檔 signal A 的差異可由矩陣解釋。（惟報告未寫該一句話，屬 checklist 形式缺漏，不另計。）
- **🟢-7｜篇幅**：115.3KB vs 115KB 含附文獻上界，超出 0.3KB 屬警告層級。本次未發現鷹架語言或流程劇場。若要壓，**唯一乾淨的可砍處是重述**：Avera／Inphi／Innovium／剝離／Celestial-XConn 這串併購史在 §5.D、§6.B①、§9 資本配置軌跡、§9.D **重複四次**；空頭故事在 §1 陷阱表、§2 逆向推演、§12b 重複三次。合併後可省 3-5KB。**量化模組、§8.5 read-through、sourcing 密度一律不得動。**

---

## 四、未及查證清單（預算 14 輪用罄）

| 軸 | 未查證項 | 建議查詢詞 |
|:---|:---|:---|
| 政策 | 「2026-01 BIS 新許可政策含 15-25% 中國營收分潤／關稅」是否真實存在、是否及於高速網通矽 | `BIS January 2026 license policy semiconductor China revenue share networking silicon` |
| 共識 | FY2028 $6.32／FY2029 $9.54 非 GAAP EPS 的外部同口徑交叉點（現僅 Excel 單一來源） | `MRVL consensus EPS FY2028 FY2029 non-GAAP Visible Alpha / Koyfin` |
| 競爭 | Meta MTIA 次代、Google TPU v8 的設計服務歸屬（MediaTek／GUC／Broadcom 分工） | `MTIA next gen design partner 2026`, `Google TPU v8 MediaTek Broadcom 2026` |
| 客戶 | Marvell FY2026 10-K 是否揭露 >10% 單一客戶及其百分比（報告稱「未揭露精確數字」，未經查證） | `Marvell 10-K fiscal 2026 customer concentration 10% of net revenue Customer A` |

---

## 五、Gate 裁決

**FAIL**

理由（僅取足以致 FAIL 的兩條，其餘為必修但非致命）：

1. **翻面的必要證明不完整且陳述不實**（🔴-1／🔴-2）。QC-49 要求引用前次 §13b 加減碼觸發的**具體條件已發火**；前次該區塊是三條件，第三條「custom 守住 Maia」被整條刪除，公開證據又偏向該條件未成立（Maia 200 的加速器本體並非 Marvell 承接），而報告寫的是「三項觸發器條件皆已發火」「同一組門檻」。QC-49 對「引用不出已發火觸發器」的 fail-safe 是**承繼前次裁決＝觀望**——因此這不是排版瑕疵，是直達裁決層的缺口。同時 Single Thing 被靜默窄化，使被丟棄的那條件在未來也不會亮燈。
2. **§5.R／§6.D 承重模組對一手申報算錯**（🔴-3）。ΔWC $2.15B 與 FY2026 10-K（AR $2,186.6M／存貨 $1,388.0M／應付 $1,073.8M）對不上，正解約 $1.17B，差額恰為報告自陳屬 **FY2027** 的 ~$1B 產能預付款；且報告 §7.E 自承當時應付帳款欄位取不到。重算後天花板由 34% 落至個位數，§10.5 的「在天花板內 ✅」翻為 ⚠，依規則 Bear 機率**強制 ≥30%**，dd-meta 對外欄位 `endo_growth_ceiling=34.0` 亦為錯值。乘上一個全無推導的「增量 ROIC ~70%」，即強化職責書 (b) 指名要攔的量化模組退化形狀。

**補充判斷（避免過度解讀本裁決）**：修好之後 **裁決方向很可能仍是「進場」**——價格腿（$216.62、FY+2 34.27x）與成長腿（DC +46%、Q3 guide ~+75%）都經獨立查證確實發火，決策矩陣機械面正確，情境樹與 IRR 對帳乾淨，Bear 機率調至 30% 後 EV 仍有 +64.6%／年化 ~10.5%。FAIL 的意思是**這份報告目前無法依它自己的規則被稽核**，不是「MRVL 不該買」。建議修補順序：🔴-1／🔴-2（翻面正當性）→ 🔴-3（天花板與 dd-meta）→ 🔴-4／🔴-5（兩條缺軸）→ 🔴-6（對手模組）→ 🟡 群。倉位角色「核心」在 🔴-1 的第三條件釐清前，建議先按「首階 1/3」（前份原訂節奏）而非 1/2 執行。

---

## Sources

- [Marvell Q2 FY2027 results — Investor Relations press release](https://investor.marvell.com/news-events/press-releases/detail/1031/marvell-technology-inc-reports-second-quarter-of-fiscal-year-2027-financial-results)
- [Converge Digest — Q2 revenue $2.74B, data center 79% of sales](https://convergedigest.com/marvell-q2-fy2027-data-center-ai-revenue/)
- [BigGo — Marvell raises FY2028 outlook to $18B, Google warrant deal](https://finance.biggo.com/news/US_MRVL_2026-08-27)
- [GuruFocus — MRVL Q2 FY2027 earnings call highlights](https://www.gurufocus.com/news/9057517/marvell-technology-inc-mrvl-q2-2027-earnings-call-highlights-record-revenue-and-massive-aidriven-growth-outlook)
- [The Next Platform — Peeling apart that supposed $120 billion chip deal Google inked with Marvell](https://www.nextplatform.com/compute/2026/08/27/peeling-apart-that-supposed-120-billion-chip-deal-google-inked-with-marvell/5292984)
- [Motley Fool — Google's Marvell warrant doesn't fully vest until Google buys $120 billion of chips](https://www.fool.com/investing/2026/08/20/google-s-marvell-warrant-doesnt-fully-vest-until-google-buys-usd120-billion-of-chips/)
- [Motley Fool — Stock Market Today, Aug 28: Marvell slides 10% on softer fiscal 2028 guidance and Google deal timing](https://www.fool.com/coverage/stock-market-today/2026/08/28/stock-market-today-aug-28-marvell-slides-10-on-softer-fiscal-2028-guidance-and-google-deal-timing/)
- [CNBC — Marvell shares tumble as outlook underwhelms despite 37% revenue growth](https://www.cnbc.com/2026/08/28/marvell-mrvl-q2-earnings-outlook.html)
- [MarketScreener — Marvell raises annual forecasts, but shares fall as Google deal questions linger](https://www.marketscreener.com/news/marvell-forecasts-quarterly-revenue-above-estimates-on-ai-chip-demand-ce7858ded08ffe23)
- [Motley Fool — Marvell's AI bookings are stellar, but its gross margin guide is what moved the stock](https://www.fool.com/investing/2026/08/28/marvell-s-ai-bookings-are-stellar-but-its-gross-margin-guide-is-what-moved-the-stock/)
- [Sherwood News — Marvell sinks after Benchmark says it lost Amazon custom chip design business](https://sherwood.news/markets/marvell-sinks-after-benchmark-cuts-company-saying-that-it-lost-its-amazon/)
- [Yahoo Finance — Marvell CEO says the company didn't lose any orders](https://finance.yahoo.com/news/marvell-ceo-says-company-didn-171831882.html)
- [Yahoo Finance / Wedbush — Microsoft's new AI chip could be a big win for Marvell and TSMC (Maia 200 / Maia 300)](https://finance.yahoo.com/technology/ai/articles/microsoft-ai-chip-could-big-192055770.html)
- [Marvell FY2026 Form 10-K (period ended 2026-01-31)](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm)
- [TradingView / Quartr — Alchip Q2 2026 revenue $241.7M, +82.6% QoQ, N3 accelerator ramp](https://www.tradingview.com/news/urn:summary_document_slides:quartr.com:4023382:0-alchip-technologies-q2-2026-revenue-jumped-82-6-qoq-to-241-7m-led-by-n3-accelerator-and-hpc-growth/)
- [Investing.com — Alchip Q2 2026 earnings call transcript (gross margin mix, N2 / Trainium 3 chiplet project)](https://ca.investing.com/news/transcripts/earnings-call-transcript-alchip-q2-2026-tops-eps-view-as-ai-ramp-drives-growth-93CH-4800784)
- [TrendForce — HBM contract prices expected to surge multiples higher in 2027 (2026-06-02)](https://www.trendforce.com/presscenter/news/20260602-13074.html)
- [The Diligence Stack — Memory's $200B inflection (DRAM +275–300% 2025→2027)](https://www.thediligencestack.com/p/memorys-200b-inflection)
- [FactSet Insight — Hyperscalers tap external financing as AI capex outruns cash flow](https://insight.factset.com/hyperscalers-tap-external-financing-as-ai-capex-outruns-cash-flow)
- [Silicon Analysts — Hyperscaler AI capex and the depreciation wall, 2026](https://siliconanalysts.com/analysis/hyperscaler-ai-capex-depreciation-wall-2026)
- [Broadcom Q2 FY2026 results 8-K (Q3 AI semiconductor guidance $16.0B)](https://www.sec.gov/Archives/edgar/data/0001730168/000173016826000051/avgo-05032026x8kxex99.htm)
- [stockanalysis.com — MRVL analyst forecasts (n=44, median $275, range $126–$400)](https://stockanalysis.com/stocks/mrvl/forecast/)

---
---

# 第二輪 Re-gate（同一 critic，2026-08-31）

> 第一輪判 FAIL 後 writer 已修訂。本節為重新冷讀；上方第一輪內容原文保留供稽核軌跡。
> 檔案：115.3KB → **134.8KB**（+19.5KB）｜`verify_dd_math.py` **pass（本輪連 §5.F 告警都消失）**
> 新增查證：4 輪 WebSearch（Astera Labs 實績／Maia 200 官方供應商／BNP-GUC 出處／Marvell FY25 應付帳款）＋前份 DD 五處觸發器逐字回比＋全檔算術複算

## 一、第一輪 6 條 🔴 逐條驗收

| # | 第一輪 🔴 | 驗收 | 依據 |
|:---|:---|:---:|:---|
| 🔴-1 | 觸發器引用不忠實 | **已解決** | §11.3 逐字列出前份五處版本，我對 `DD_MRVL_20260623.html` 逐條回比——①§1「PE≤30x」②§3.E 二條件＋首階 1/3 ③§12 四項 settle 點 ④§14a「custom 風險出清」⑤§14b 三條件——**五處全部引用正確、無竄改**。裁定 §14b 為權威版本並說明理由；初稿「同一組門檻」的不實陳述已刪除並留痕；首階 1/3 已恢復且公開記錄更正 |
| 🔴-2 | Single Thing 靜默窄化 | **已解決** | §2.F 恢復 Trainium4／Maia gen3／MTIA 三選一，且 §1 監測表 #1、§12 13a 盲點、§13b 轉迴避列、§14 第 3 項全部同步為三選一（非只改一處） |
| 🔴-3 | ΔWC 期別錯置／天花板算錯 | **已解決** | 我複算：ΔWC＝1,158.2＋358−350≈**$1.17B** ✓；(0.36−1.29+1.17)/2.546＝**9.4%**（報告 9.3%，捨入內）✓；天花板 9.3%×[13.5%~70%]＝**1.3~6.5%** ✓；§10.5 由 ✅ 翻 ⚠、Bear 25%→30%、Base 45%→40%、EV 重算 0.30×163.3＋0.40×67.6＋0.30×(−38.1)＝**+64.6%** ✓、年化 1.646^0.2−1＝**10.5%** ✓、AR＝(30×163.3)/(30×38.1)＝**4.29→4.3** ✓、dd-meta `endo_growth_ceiling` 34.0→7.0 ✓。期別錯置的成因（把 FY2027 產能預付款計入 FY2026）被明文寫出，且「淨稀釋不是正貢獻」已統一到 §6.D／§7 回購表／§10.6 三處 |
| 🔴-4 | 缺記憶體成本軸 | **已解決** | §2.C R2 擴為含成本側子軸（DRAM 2025→27 +275~300%、TrendForce 2026-06-02 HBM 2027 倍數級、GS custom ASIC HBM 需求 +82%），並新增可證偽的監測語言「歸因是否從 mix 轉為投入成本」；§14 第 4 項、§12 13b 同步接線 |
| 🔴-5 | 缺 AI capex 消化軸 | **已解決** | §2.C **R4 恢復**（+51%→+13%→+5%、負債占 capex 9%→32%、$137.5B、折舊少認列 $1,760 億、FASB FY2027），監測指標與警戒閾值具體；§14 第 2 項、§13b 轉迴避列、§12 13b 同步。且誠實註記「前份原有、本次初稿一度靜默刪除」 |
| 🔴-6 | §5.F 空殼＋QC-5 只放 1 家 | **已解決** | §5.F 補入 Alchip 真實數字與 Astera Labs 第四欄；§7 三年趨勢表補 Alchip／Astera 兩欄（達 ≥3 家）；最關鍵的是**「毛利率下滑純屬 mix」的說法被正面對質並改寫**為「custom 組合＋客戶/對手雙重議價力共同驅動，公司全歸因於 mix 的說法應打折看待」，並回填 §5 moat_trend、§1 陷阱表、§12 13b' |

**六條全數實質解決，非表面應付。** 另第一輪 🟡 中的 §10.4 溢價論證、§10.1 val 燈揭露、§7.E DPO/CCC（226→126.4 天更正，我複算 AP 1,073.8/COGS 4,016×365＝97.6 天 ✓）、附錄 A Bear anchor（18x／−69.6% ✓）、§10.5 10Y 二段（3.37x／12.9% ✓）、moat 時間錯配、中國 36%、§5.D/§9 併購史去重 —— 均已照規格改。

## 二、本輪新發現 🔴（3 條，皆非裁決層）

### 🔴 R2-1｜`dca_role`＝衛星：理由書與 canonical enum 不符，且隱含把既有核心持倉降級為衛星（＝解除長抱賣出保護）
- **問題**：`references/decision-layer.md` 明訂「**迴避 → 不持有；觀望 → 追蹤（既有持倉等觸發則衛星）**」。§13a 給的理由是「非『不持有』等級的追蹤池，而是……衛星狀態」——把 **追蹤** 誤描述成「不持有等級」。四值制裡 `追蹤`＝「觀望但值得盯」，正是本檔情形（§13a 自己寫「初始建倉倉位（新資金）0%」）。
- **為什麼不只是標籤問題**：同檔 line 101 規定「長抱賣出分軌」只保護 `核心`，而「**衛星角色不受此限（可用價格/估值觸發）**」。前份 DD 的 `dca_role` 是「條件式核心持倉」；本份改為 `衛星`＝在未經討論的情況下**解除了既有部位的 thesis 級賣出保護**，讓價格/估值可以單獨觸發賣出。`dca_role` 是 portfolio-manager／picks／research 頁直讀欄位，不是敘述文字。
- **最小修法**：二選一並寫明——(a) 改 `追蹤`（新資金 0% 的預設對映）；或 (b) 維持 `衛星`，但必須引用 enum 的「既有持倉等觸發則衛星」條款、並明寫「本次將前份的核心角色降為衛星，代價是長抱賣出分軌保護解除」。現行理由書兩者都不是。

### 🔴 R2-2｜BNP Paribas／GUC 這條證據**無法佐證**，而它在五處撐著裁決
- **問題**：報告在 §1 裁決 bullet、§1 陷阱表、§2.F 如何監測、§11.3、§13 共五處引用「BNP Paribas（2026-01-27，Maia 200 發表後即時分析）明確判斷 Marvell／Broadcom 均不太可能是核心晶片設計商，較看好 GUC」，並在 §11.4b 把它與「官方沉默」並列為 L1/L2 證據。
- **查證結果**：兩種查詢式（Maia 200 供應商＋BNP＋GUC／GUC 創意電子＋Maia 200＋Marvell）皆**未能檢得此判斷**。檢得的是：Microsoft 官方部落格（2026-01-26）、TrendForce（**2026-01-27**，與報告所引日期同日）——內容為 **Maia 200 採 TSMC 3nm、SK 海力士為 HBM3E 獨家供應商**，全文未提 BNP、GUC、Marvell 或 Broadcom 的設計歸屬。賣方 note 未被索引屬常態，故不能斷為虛構；但一條**扛著翻面否決權**的具名分析師判斷，critic 查不到就必須降級處理。
- **關鍵補充（避免過度懲罰）**：**裁決不依賴這條**。裁決一致性規則的門檻是「引用不出**已發火**的觸發器」——已查證的事實（Microsoft 官方只點名 TSMC 與 SK 海力士、未點名任何 ASIC 設計夥伴；Marvell 亦無官方確認）本身即足以認定第三條件「無法確認發火」。BNP 只是把結論從「未決」推到「證據偏向不利」。
- **最小修法**：補出可回溯出處（刊名／URL／報告標題），或把五處改寫為只承載已查證的部分——「Maia 200 官方揭露僅 TSMC＋SK 海力士，無任何 ASIC 設計夥伴具名，Marvell 角色無官方確認」——並把 §11.4b 的證據權重敘述相應改為只靠 L1 官方沉默。刪掉 BNP 後 §13 一字不必改。

### 🔴 R2-3｜修訂未貫通：7 處舊值殘留，其中 2 處直接打臉本輪兩大更正
- §2.A 持有期表：「**本次進場為財報後估值修正窗口**」——裁決已是觀望，此句與 §13 直接衝突。
- §6.0 成長品質 7 問 #2：「再投資率(WC-based)**~48%**」／#3：「改用混合估算 **≈70%**」——**正是本輪 🔴-3 修掉的兩個錯值**，在同一份報告裡與 §6.D 的 9.3%／「不可精算」並存。
- §5 市佔競爭表 Alchip OI margin：「資料有限（台灣上市，非美股可比）」——§5.F 已寫「目標 high teens」。
- §10.4 開頭：「Alchip（純設計服務）規模量級差距過大缺乏可比性，僅供質化參考」——同節表格與 §7、§5.F 已把 Alchip 量化使用。
- §10 估值診斷結論：「同業相對（對 Broadcom 顯著溢價，**惟有更高成長率支撐部分**）」——§10.4 本輪已推翻此前提並改用小基期效應立論。
- 衰退信號表 EPS/Rev 列：「差距源自營運槓桿**與回購**」——與本輪統一的「淨稀釋非正貢獻」框架相斥。
- §2.B' 近月邊際：「AWS 旗艦社羣爭議未解但**無新增惡化證據**」＋「H1 邊際＝正向」——本輪新增的 Maia 官方未具名證據未反映。
- **最小修法**：以上 7 處改為與 §6.D／§10.4／§13 一致的措辭。這是 QC-7 一致性層級的問題，逐格改即可，不需重寫章節。

## 三、本輪 🟡

- **🟡 R2-1｜第一輪 🟡-2 未修**：§6.E 下方「15% 成長情境下跌幅有限（−3.1%）顯示現價已對『成長顯著放緩』有相當程度定價，是 val=🟡 而非🔴 的數字基礎之一」一字未動。三情境仍把 FY29 EPS 固定在內含 ~50% CAGR 的共識 $9.54、只壓倍數；真的降到 15% 成長，EPS 不會還是 $9.54，故此推論不成立（表格本身合乎樣板，問題只在這句引申）。回報稱「10 條 🟡 全數處理」與實況不符。
- **🟡 R2-2｜§14b vs §12 的裁定需補一句**：裁決一致性規則原文是「引用前次報告 **§13b 加減碼觸發 _或_ §12 證偽指標**」——兩者並列。前份 §12 矛盾表的**執行路徑欄**寫的是「(a) 觸發 PE≤35x + DC 仍 >20% → 分批進場/加碼（首階 1/3）」，即走 §12 分支時**二條件已乾淨發火**。報告把 §12 描述為「矛盾裁決過程中的參考數據點，非最終行動閘」，略低估了它自帶執行路徑欄的事實。選 §14b 是**保守且我認同的取捨**（fail-safe 方向本就朝不翻面），但必須明說「規則允許引用 §12，走該分支會得出進場；本報告選 §14b 的理由是 ___」——否則下一份 DD 會繼承一個未經辯論的裁定。
- **🟡 R2-3｜FY25 應付帳款 $723.8M 是「估」，且估法源自第一輪 critic 的示意數字**：我第一輪寫的是「若應付增加約 $0.3B」作為敏感度示意；本輪被固化為前期餘額並據以產出 §7.E 的 DPO/CCC 時序（97.6／77.8 天）。FY2026 10-K 的比較式資產負債表本身就有 FY25 實數，應直接取用。**方向性提醒**：若實際 ΔAP 更大 → ΔWC 更小 → 再投資率更低 → 天花板更低 → ⚠ 結論只會更強，故不影響裁決，但數字不該建立在 critic 的示意值上。
- **🟡 R2-4｜`endo_growth_ceiling`＝7.0 vs 推導上界 6.5**：捨入方向已標「粗略量級」尚屬誠實，但下游是直讀欄位，建議填 6.5 或在欄位旁註明取整規則。另 1.3% 那端用「當期 ROIC 13.5%」當增量 ROIC 的保守代理，宜一句話說明這是下界代理而非估計值。
- **🟡 R2-5｜`rearm_trigger` 欄位破格**：規格為「§13a 首句 ≤40 字、`rearm_trigger` 同步此句」，現值約 100 字且夾帶推理。建議壓成「rearm＝10/6 ID 或法說對三旗艦 socket 任一正面確認＋GM 守 57.5-58.5%」。
- **🟡 R2-6｜篇幅 134.8KB（超 115KB 上界 19.5KB）**：整體是實質內容不是鷹架——五版本逐字比對、§6.D 重算、R2/R4 兩軸、§5.F 四欄、§10.4 改寫都必要。但**本輪確實長回了重述**：§14b 三條件「① PE ✅ ② DC ✅ ③ Maia ⚠️」完整重述於頁首裁決 bullet／§1 散文／§2.E 表／§11.3／§11.4／§13／§13a **共 6 處**；Maia-BNP 證據句重複 **4 處**。建議完整推導只留 §11.3，其餘改「見 §11.3」，可回收約 4-6KB。量化模組、§8.5、sourcing 密度一律不動。
- **🟢 小疵**：§11.3 首句寫「本身在**四處**不完全一致」，其後列 ①–⑤ 共五處。

## 四、新增內容的獨立查證

| 本輪新數字 | 報告值 | 查證 | 判定 |
|:---|:---|:---|:---:|
| Astera Labs Q2 2026 | $392.4M、+104% YoY／+27% QoQ；Q3 guide $540-560M | 完全相符（Q3 中位 +40% QoQ，非 GAAP EPS $1.16-1.21） | ✅ |
| Maia 200 官方供應商 | 僅 TSMC（晶圓）＋SK 海力士（HBM） | 相符：TSMC 3nm、SK 海力士 216GB HBM3E 獨家（TrendForce 2026-01-27） | ✅ |
| BNP Paribas 判斷 Marvell/AVGO 不太可能、看好 GUC | 五處引用 | **兩輪查詢皆未檢得**（見 🔴 R2-2） | ❌ |
| Alchip Q2 2026 $241.7M／+82.6% QoQ／GM 50%→20% 出頭／目標 high teens／N2＝Trainium3 | §5.F、§7 | 第一輪已查證相符 | ✅ |
| 記憶體與 capex 兩軸數字 | §2.C R2／R4 | 第一輪已查證相符 | ✅ |
| Benchmark 部分收回／CEO 否認丟單／JPM 未認同流失 | §5 moat 雙向證據 | 相符（Benchmark 改稱 Amazon 增列 Alchip 為輔助設計；JPM Harlan Sur 稱 Microsoft/Amazon 均未失份額；CEO 公開稱未丟訂單） | ✅ |
| Marvell FY25 應付帳款 $723.8M | §6.D／§7.E | 未能檢得（見 🟡 R2-3） | ⚠ |

## 五、觀望裁決本身的對稱檢查（防「critic 一路往下打」）

critic 只往一個方向棘輪就是壞掉的 critic，故對本輪的**保守方向**同樣加壓：

- **不是為了討好 critic 而過度修正。** 走進場的論據被完整保留且被正面回應：§13 明白寫出「矩陣機械輸出就是進場」、§11.4b Steelman 寫的是「現在就買的最強論證」並逐點回應（等 5 週的機會成本 vs 在未證實條件上建倉的下行不對稱），§13c 甚至寫明「現價 $216.62 附近適合建倉——只是『適不適合買』與『現在能不能買』是兩個問題」。這是把分歧攤開，不是把結論倒過來。
- **fail-safe 方向與規則一致**：裁決一致性規則的失敗方向本就是「維持不翻面」，且 §14 已定義乾淨的重啟條件（三旗艦 socket 任一獲官方 sourced 確認，取代語意已失效的「守住 Maia」），`rearm_trigger` 亦已落 dd-meta——下一份 DD 不會再繼承一組模糊觸發器。**這正是第二輪最該達成的事，已達成。**
- **唯一的不對稱殘留**是 🔴 R2-1（`dca_role` 衛星）與 🟡 R2-2（§12 分支未辯論）：前者在裁決之外**放鬆**了既有部位的賣出紀律，後者在裁決之內**收緊**了翻面門檻——兩個方向剛好相反，都應攤開。

## 六、Re-gate 裁決

**PASS-with-fixes**

- 第一輪 6 條 🔴 **全數實質解決**，且經一手來源與算術複算逐條驗收；翻面所需的引用忠實性已建立，五處版本逐字可回溯，裁定理由寫在紙上。
- 本輪 3 條新 🔴 **均不觸及裁決層**：R2-1 是 dd-meta 角色欄與 enum／賣出紀律的接線錯誤；R2-2 是一條可移除而不影響結論的無法佐證引用；R2-3 是修訂未貫通的 7 格舊值。三者皆為「逐格改」等級，不需重跑分析。
- **裁決 觀望・（角色待更正）本身站得住**：價格腿與成長腿確實發火（已獨立查證），第三條件在已查證的官方揭露下無法確認發火，fail-safe 方向正確；§10.5 的 Bear 30%／EV +64.6%／IRR 10.5% 全部複算相符；重啟條件已重新定義並落 dd-meta。
- **建議放行順序**：先修 R2-1（dd-meta 直讀欄位，影響下游 PM）→ R2-2（改寫五處引用）→ R2-3（7 格舊值）→ 🟡 群（其中 🟡 R2-1 的 §6.E 那句與 🟡 R2-2 的 §12 分支說明務必補）。四項改完即可 commit；篇幅去重（🟡 R2-6）可順手做，但不是放行條件。

## Sources（第二輪新增）

- [Astera Labs Q2 2026 results — $392.4M revenue, +104% YoY, Q3 guide $540–560M](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-second-quarter-2026-financial-results)
- [TrendForce (2026-01-27) — Microsoft unveils Maia 200 on TSMC 3nm; SK hynix reportedly sole HBM3E supplier](https://www.trendforce.com/news/2026/01/27/news-microsoft-unveils-maia-200-ai-chip-on-tsmc-3nm-sk-hynix-reportedly-sole-hbm3e-supplier/)
- [Microsoft official blog (2026-01-26) — Maia 200: the AI accelerator built for inference](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)
- [Marvell FY2025 Form 10-K (period ended 2025-02-01) — comparative balance sheet source for FY25 accounts payable](https://www.sec.gov/Archives/edgar/data/1835632/000183563225000057/mrvl-20250201.htm)
