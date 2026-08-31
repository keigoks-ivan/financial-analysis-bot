# stock-analyst v14.7 — changelog.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-07 v14.7 結構拆分，內容自 v14.6 原文搬移、語意零變更）。必讀時點見 SKILL.md 條件載入路由表。修改規則請同步 SKILL.md stub 與 references/changelog.md。

## 制度沿革（lineage 摘要 — 保留每條規則的 WHY）

各版核心改動的「為什麼」濃縮如下；規則本體在【品質管控強制規則】與各章節。**注意：本檔為血統記載，§ 編號保留寫成當時版本的編號**（v15.0 起章節重排，v14→v15 對映見 SKILL.md「章節重編」列）。

- **v15.0（2026-08-05 持有人拍板；章節重排＋篇幅帶下修＋§5.R）**：①**章節重排＝商業本質優先**——結論→論點（序章併入 ≤1KB 引子）→產業→商模+Munger→護城河→成長→財務品質→財報（＋read-through）→治理→估值→決策層；統一裁決移至 §13（`id="decision"` 錨點與 dd-meta 契約不變，validator/qc/pre-commit/九站 startswith 已 additive 放寬收 v15）。②**篇幅帶 150-200KB → 75-105KB（目標 ~100KB）**、hard floor 110→70KB、含附文獻上界 115KB。WHY：實測「150-200KB＝帶內合格」把 median 從 v14.2-14.11 的 116KB 錨上 v14.12 的 153.5KB（n=72，max 509KB）——帶下緣變成目標；BKNG/ANET（228-229KB）vs SIMO（116KB）同結構對比證明肥的是散文不是模組，分章節預算全面超標且無機械執行點。故「帶內合格」語言廢除、分章節預算全表重訂（以略低於 SIMO 各章實測為錨、表自證加總 ~95KB）＋§7 中場檢查 >70KB 加嚴＋估值（§10+附A）≤~7%（原 ≤20%）＋決策層 ≤12KB 只渲染結論物。③**§5.R 報酬持續期檢核**（ROIC 四象限定位×持續期四檢查點〔需求基礎值/決策層級/價值鏈分配/社會容忍度〕×增量 ROIC×再投資率→`endo_growth_ceiling`；判準集中 `references/roic-durability.md` 條件載入，源自持有人提供的 ROIC 持續期文章；屬分析框架提示語非判斷類規則，不登 rule_ledger）。④**北極星宣言**入 skill 開頭（找真的值得長期投資的公司；生意決定買不買、價格決定何時買）＋**研究採集外包 sonnet**（步驟 0＋gap 搜尋＋QC-39 證據端；判斷端不外包）。品質不可退讓清單除 floor 數字外原樣；判斷機器（矩陣/critic 四關卡/PREREG）一字未動。舊「防壓縮指令」殘塊自 html-output.md 移除。

- **v9.0**：建立 QC-1~QC-11 品質規則骨架（業務權重引用、MA104w 查實值、品質分公式、Bollinger Python 計算、執行不中斷）；EPS 用 yfinance 程式化抓取（步驟零）。
- **v11.2**：QC-12~QC-21（近 90 天產業掃描、自我攻擊裁決、核心數據交叉一致、時效性、先前 DD 結構化讀取、催化劑實現檢查、R:R 數學假象防禦）。WHY：多次因「裁決後沒反駁測試」「催化劑寫成即將到來但已發生」「R:R 分母趨零爆假數字」翻車。
- **v12.0**：分析師/PM 分工 — DD 輸出綜合訊號 A+/A/B/C/X，不建議倉位 %（倉位歸 PM skill）；護城河單一決定品質等級；估值燈取代 R:R 裁決；Pure MA 六態機 + 大盤豁免；QC-22~QC-31（股價漂移、威脅三級、intraday、Beta 雙源、margin 結構性、Rev/OI divergence、絕對 vs 相對成長、R:R 壓測、溢價收斂、訊號燈定義表）。
- **v12.1/v12.2**：dd-meta JSON SSOT + validator（QC-32）；推導可追溯性（QC-33）、季節性過濾（QC-34）、漂移分級（QC-35）、5Y 目標價一致性（QC-36）；Inception 標記。WHY：下游反向 parse HTML 不穩 → 改 emit 結構化 JSON。
- **v12.3**：估值瘦身（§2+§13 從 ~40%→~18%）× 基本面擴充（→~55%）；§9 強制 execution+pricing power 二維拆解；§5.F Single Thing 從 DCA 借入；QC-37 裁決單一居所。
- **v12.4**：EPS 接 Koyfin/Excel buy-side consensus（步驟零'，最高優先），解 yfinance FX-ratio 陷阱（TSM 鬼數）。
- **v12.5/v12.6/v12.7**：基本面再深掘 — ROIIC/內生天花板、利潤池地圖、Moat-to-Numbers、資本配置計分卡；深度量化模組（分部前瞻 §6.I、對手 P&L §7.F、DuPont+營運資金 §8.E、逐段 TAM/SAM §9.F、10Y 資本配置 §10.D）；成長品質 7 問儀表板（§6.0）、FCF 去向+M&A 飛輪（§10.E）；隨附文件 read-through（§4.5）。size floor 80→90KB，非灌水量化閘（QC-38）。
- **舊 DCA（已併入）**：三軸獨立研究 + 矛盾強制裁決 + PM 決策框架（thesis / Asymmetry IRR / Single Thing / pre-mortem / Max DD / opportunity cost / 複審）。v13 把**決策層**留下（§12-§15）、把**重複的基本面搜尋**砍掉（料落 Part I）。
- **v14.0（方法論升級；schema 與 skill 版號一號到底 = v14.0，pipeline 相容 v13.x）**：QC-39 產業態勢變化雙向掃描（防 AVGO 型「沒搜到競爭惡化→過度樂觀」+ SNDK 型「只用歷史 pattern 外推→對結構性產業順風過嚴」）；QC-40 輸出潔淨（內部 QC 鷹架不得渲染進讀者面前的 HTML）。WHY：AVGO 把 moat ↑/進場 開在 Broadcom 於 Google TPU 份額 95%→65% 流失之上；SNDK 在 NAND 結構性缺貨下仍機械套歷史硬反轉 bear。兩者同根:產業態勢被當靜態處理。
- **v14.1（schema/skill 一號到底 = v14.1，pipeline 仍相容 v13.x ∪ v14.x）**：① QC-39 加**第三軸（其他結構變數，開放式 catch-all）**——法規/政策/關稅/反壟斷、通路重構、商業模式轉移、替代技術、客戶結構轉移，治「全新形狀」（非競爭/非供需）；② 新增 **QC-41 寫稿後產業態勢獨立 critic**——Part I/II 草稿完成後、最終 Write 前 spawn 不同 model instance（general-purpose sonnet）冷讀紅隊，沿 4 軸（競爭/durability/其他結構/priced-in）找報告漏判或低估，🔴 有 sourced 證據則回頭修正章節再 finalize。WHY：QC-39 是 in-loop 自律（同一個腦自己抓不到「想了卻錨定」與 C 軸全新形狀）；獨立 critic 是 Boris verify-app pattern 的 backstop（寫 DD ≠ 驗 DD）。**強制觸發**:強方向裁決（進場/迴避）OR 方向性 moat_trend（↑/↓）OR 競爭動態/循環/法規敏感/B2B 集中型標的。
- **v14.1 增補（同日，附錄 B 循環交易鏡頭 / QC-42;SNDK·MU 教訓）**：對循環/商品 archetype 加**第二條平行鏡頭**——投資軌（§14）回答「值不值得長抱」（循環股幾乎永遠迴避/觀望），附錄 B 回答 Game 2「做為循環**交易**，在 cycle 哪一格、該怎麼動」（5 檔位置 + 交易姿態 + 反動能硬閘）。WHY:SNDK（$40→$2,185）/MU（$103→$1,134）一路噴而 DD 一路「不推薦」的脫節，根因**非 gate 算錯**（基本面裁決對:SNDK 報告已 §11.5 正規化算出公允 $150-500、識破 peak-EPS 假象、moat↓ 迴避），是**缺一條鏡頭**——單一鏡頭量得到「長抱品質」、量不到「循環交易」。附錄 B 明標投機、**不碰 §14**、`cycle_position`/`trade_stance` **僅進 HTML 不入 dd-meta**（schema 維持 v14.1，下游 6 pipeline 零影響）。
- **v14.1 Stage 1+2（同日，QC-43 archetype 分類器 + QC-44 金融 gate-set;JPM 原型）**：把「現行 gate 是通用成長複利股尺」明確化——QC-43 加 §0 archetype 分類（6 類，primary + secondary + 信心），路由 §5/§11/QC-31 換尺;QC-44 補金融 gate-set（bank/insurer/broker 子型:ROTCE/CET1/NIM/效率比/P-TBV/combined ratio，取代 FCF/ROIC/Capex/D/E/EV-EBITDA）。WHY:JPM 實證成長股 gate 對 balance-sheet 金融**整組失效**（FCF −$148B、D/E None、EV-EBITDA None、grossMargins 0、ROA 1.27% 看似差實為常態）。護欄:只換 gate-set/估值錨/signal，**不碰**深度地板/資料契約/流程紀律;§0 宣告 HTML-only 不入 dd-meta（schema 維持 v14.1）。支付網絡(MA)/資產輕金融科技留品質複利不誤歸金融。
- **v14.1 Stage 3-5（同日，QC-45 未獲利高成長 + QC-46 轉機·公用 + QC-47 修剪矩陣）**：QC-45 補未獲利高成長 gate-set（MDB 原型:GAAP 負 EPS → §5 EPS-CAGR/PEG/ROIC/EV-EBITDA 全 undefined、QC-31 FCF/NI=−7 誤觸發 X;改 Rule-of-40 45.5% / NRR / EV-S / FCF margin 20.3%）;QC-46 補轉機（資產重估/SOTP/normalized）+ 受監管公用（DDM/殖利率/regulated ROE），輕量、模型 prose 為主;QC-47 archetype × QC 適用矩陣（Stage 5 修剪）——非複利 archetype 下被 gate-set 取代的通用 PE/EPS/FCF tripwire 不重複機械套用（消 effort tax / 雙觸發），但深度·資料契約·流程紀律（QC-8/13/17-19/32/33/38/39/40/41/43）**全 archetype 永不修剪**。**全程 schema 維持 v14.1、零下游;非 default archetype 的 gate-set 皆走 §0 路由、明寫換了哪套。**
- **v14.2（row 5 動能過熱降級;TSM 教訓）**：§14 決策矩陣 row 5（動能過熱）由「Soft Veto 上限觀望」降為「節奏修飾」——命中只把 §14a 進場節奏改為條件式分批（首階 1/3 ＋ 回檔加碼），**不再把裁決頭銜從進場壓成觀望**。WHY:TSM 實證——signal A／moat S↑／PEG 0.95／val🟡／MA✅／IRR 15.5% 每條進場 baseline 全過、報告自稱「本質是進場級標的」，卻僅因 row 5（貼 ATH／布林上軌／短期 R:R 負）被鎖觀望 → ①「好公司因漲多被判不能買」過度保守 ②與 QC-7b（禁「股價已在高位」當裁決理由、技術面不主導 §14）自相矛盾。估值把關不受影響（過熱+偏貴仍由 row 8 落觀望）。schema 隨「一號到底」慣例 bump 至 v14.2（dd-meta 欄位契約與 v14.1 完全相同，純版號對齊）、dd-meta enum 不變、下游 6 pipeline 零改動（validator `^v1[234]\.\d+$` 與 `startswith(("v13","v14"))` 已接受）;僅裁決分布從觀望往「進場·條件式」移。**只動 row 5;row 4（Pure MA❌）/6/7/7a 不變。**
- **v14.2 F1/F2/F3（長波段校準;mandate = 抓長波段股）**：審完整條決策脊椎後，發現進場邏輯本質是「順勢擇時（買已確認強勢、別過熱）」，與「長波段佈局（在結構上升的好公司回檔時分批、抱穿回撤）」方向相反。① **F1 進場閘**:row 9/10 的「MA ✅」→「MA 🟢/✅」+ 新增 row 9b（MA 🟡/🟠 回檔/成熟、W250 未轉負 → 進場·條件式逢回分批）+ 補裁決落空漏洞（🟢 最佳進場/🟠 回檔 + 便宜原本對不到任何 baseline row）。原閘只祝福追強勢、封殺買回檔——對長波段反向;只有 MA ❌（價 < W250 或斜率轉負）才壓觀望（row 4）。② **F2 §13c Max DD 🔴 倉位**:由「一律自動砍倉」改條件式——🔴 且 thesis 脆弱（moat↓/runway🔴/估值依賴型）才砍;🔴 但 thesis 完整只註記深回撤心理準備、不因波動本身砍倉。WHY:偉大長波段複利股幾乎都有 >50% 回撤，純按回撤砍倉＝篩掉最會漲的贏家。③ **F3 §5 EPS CAGR 門檻**:>20%（高成長）**或** 12-20% 且 runway ≥10Y 高 durability（穩健長複利;走此路徑須明標「非高成長股」），不再讓穩健長複利被成長尺低估。**dd-meta 欄位契約/enum 不變（schema 版號隨「一號到底」升至 v14.2）、下游零改動。**
- **v14.3 爆發候選路徑（2026-07 全鏈 audit 教訓:裁決函數避損優先、upside 是死數據）**：audit 發現三個結構性偏誤——① ev5y_pct 算出來只進 metadata，§14 矩陣完全不消費 Bull 列（NVDA Bull +292% 判進場靠的是估值回落，不是 upside 本身）;② runway_post_y5 接線單向（🔴 → Soft Veto，🟢 無任何獎勵）;③ §11.5 反偏差防線（Bear ≥20-30%/Base ≤50%）數學上封死 ev5y ≥200%，36 份實檔 0 筆 ≥200%、69% 觀望。修法＝**消費端接線，不放鬆估計紀律**：(a) §6.A'' runway 邊界量化（🟢=Y5 末滲透率 ≤35% 或 sourced 第二曲線;🟡=35-70%;🔴=>70% 無第二曲線），🟢 成為可靠觸發器;(b) §11.5 新增不對稱比 AR——防線押住 Bear 機率下限後「比率」仍可辨識真不對稱（NVDA AR≈21.9 vs 平庸股 ~2.4）;(c) §11.5 10Y 二段延伸（runway 🟢 必填）:數倍報酬要 7-10 年複利，5Y 框架裝不下，Y5→Y10 第二段 CAGR + 10Y 累積倍數給「數倍路徑」正式落點;(d) §14 新增 row 8a:估值 🟠 的觀望可被「runway 🟢 + AR ≥4 + 非估值依賴型 + moat ≠↓ + 無 Soft Veto」推翻為進場·條件式（爆發候選），倉位上限衛星級 2-3% starter（小輸大贏，倉位即風控），加碼雙軌（回檔 或 論點增強）;(e) 對價＝QC-48:row 8a 命中強制獨立 critic 冷讀 Bull 依據（AR 分子是自己估的，防樂觀機率經新路徑漏進裁決），打回 → 降 row 8 觀望;(f) 內生天花板例外:超出但缺口已歸因 sourced 新 S 曲線 → Bear 下限 25% 不強制 30%（新曲線成長不受「現有生意天花板」類別錯誤懲罰）;(g) §14b 長抱賣出分軌:核心/爆發候選的減碼清倉觸發必須 thesis 級（證偽指標/moat 侵蝕/滲透率軌跡斷裂），估值偏高/漲幅本身最多 trim 回目標倉、永不單獨清倉——F2 修了「抱不住回撤」，此條修「抱不住漲幅」。**估值 🔴 仍然擋、Hard Veto 全保留、反偏差防線一字不動、dd-meta enum 不變（新增選填 asym_ratio），下游 6 pipeline 零改動（prefix 檢查已接受 v14.3）。**
- **v14.3 F1/F2/F3（2026-07-02，WING/RKLB/ALAB 決策脊椎乾跑抓到的三個規格洞）**：乾跑 = 只抓最小市場數據把 §0→§6.A''→§11.5→§14 走一遍，測機制不測深度。① **F1 QC-45 估值燈懸空（大洞，RKLB 暴露）**:估值燈定義只有 Fwd PE 分位 + PEG，QC-45 未獲利股兩者全 undefined，但 `val` 必填且 §14 全部 baseline row 依賴它 → 未獲利高成長（十倍股最常出現的類別）§14 結構性走不完、row 8a 永遠不可達。修:附錄 A 加 QC-45 版雙尺（growth-adjusted EV/S = fwd EV/S ÷ fwd 營收成長%，0.5/1.0/1.5 切點 + 自身上市 EV/S 分位，取較嚴;毛利 < 50% 附 EV/GP 對照），§11.6 三分量改「營收 CAGR / EV/S re-rate / 稀釋」拆解、§11.5 以轉正年推 5Y 目標。② **F2 估值 🔴 裁決落空（ALAB 暴露）**:row 8 只寫 🟠，🔴 + 無 veto + signal ≥ B 對不到任何 row → row 8 擴為 ∈ {🟠, 🔴}（🔴 時重啟條件必含估值回落門檻）。③ **F3 ma = "-" 落空（ALAB 暴露，IPO < 250 週）**:baseline row 全要求 MA 狀態，樣本不足的新股落空 → 視同 🟡 走 row 9b（年輕股風險歸 Max DD 與倉位，不歸 MA 閘）。乾跑同時確認:row 4（WING 破 W250 → 觀望）、8a 對 🔴 的封鎖（ALAB）、QC-45 分流（RKLB）機制皆如設計運作。④ **F4 AR Live 掛單（RKLB 全跑後補;治「AR 是快照」）**:報告日 AR 是快照——RKLB $84 時 AR ~1.9、跌到 $60 會過 4 但沒人自動重算，「觀望等回檔」靠人記得。修:dd-meta 加 4 個選填欄（bull_5y_price/bear_5y_price/p_bull_pct/p_bear_pct，§11.5 本來就算出來只是沒 emit），`build_dd_screener` 每日以現價重算 `ar_live = (p_bull×(bull/price−1))/(p_bear×(1−bear/price))`，runway 🟢 + moat ≠↓ + ar_live ≥4 → /dd-screener/ 主頁「🎯 爆發獵場 watch」條自動亮燈。裁決函數從「報告時點的一次性判斷」升級為「持續執行的掛單系統」——audit 主訴「upside 是死數據」的最終閉環。
- **v14.4 QC-42 循環鏡頭轉正 v0.2（三樣本原型 ORCL/JBL/MU 定案）**：三份手跑原型（附錄 B）證明「單一商品 through-cycle 投票錶」對非商品循環失效——ORCL（capex 建設循環）只 ~3/6 訊號有效、JBL（EMS 需求量循環）~2.5-3/6，且失效子集與頂部訊號機制各異；MU（記憶體）作為原生商品對象 6/6 全可用。三點轉正:① **QC-42 升級為「按循環子型路由的位置錶族」**——商品錶（現行 6 訊號，MU 驗證原樣保留）/ capex 建設循環錶（ORCL 型:capex/折舊比、產能利用率爬坡、RPO/capex 覆蓋、交易對手信用、情緒部位、量vs價）/ 需求量循環錶（JBL 型:book-to-bill 或需求量拐點、客戶庫存去化、倍數 vs 自身歷史、終端/hyperscaler capex 週期位置、情緒部位）;由 QC-43 archetype 先判子型再選錶，無真商品/循環 sleeve 者不啟動附錄 B（ORCL 的 B.4 判別式）。② **反動能硬閘跨子型通用 + 新增「倍數 vs 自身歷史」閘**——JBL 發現現行硬閘為 peak-EPS 商品頂設計（頂部 P/E 低），對 46x TTM re-rate 頂全盲;既有四閘（晚循環禁新建、P/B 高區、高熱 12M、訊號矛盾）保留。③ **QC-43 增第 7 archetype「資本輕·低毛利·需求週期·代工服務（EMS/ODM）」**——gate-set＝ROIC + 資產周轉（取代 FCF margin）+ 客戶集中 + 需求量週期 + 倍數均值回歸，JBL §5 手動換尺轉正。**v0.1 原有的「平行投機軌、明標投機、不碰 §14/dd-meta 語意」一字不動;`cycle_position`/`trade_stance` 仍僅進 HTML 不入 dd-meta。dd-meta 欄位契約/enum 與 v14.3 完全相同（純版號一號到底 bump），下游 6 pipeline 零改動（`^v1[234]\.\d+$` / `startswith(("v13","v14"))` 已接受 v14.4）。** 參考實作:`docs/dd/DD_ORCL_20260703.html`（capex 循環）/ `docs/dd/DD_JBL_20260703.html`（EMS 需求量循環，B.5 為錶族設計母本）/ `docs/dd/DD_MU_20260622.html`（原生商品 6/6）附錄 B。
- **v14.5 三軌落地 + 決策函數校準（2026-07-05 五路審查、持有人拍板）**：
  - **row 8b 循環衛星條件式進場（推翻 QC-42 v0.2「不碰 §14/不寫 dd-meta」）**——附錄 B 循環位置經反動能五閘 + 獨立 critic 冷讀後接 §14 並落 dd-meta（`cycle_position`/`cycle_verdict`）。WHY:v0.2 使三軌循環軌 0 檔可執行、picks 爆發正式榜 5 檔 0 檔有 DD 進場、被迫用 screener 代理規則（原型 ORCL 1/5、JBL 0/5 不可靠）。
  - **row 4 六態機退役改進場節奏調節**——MA ❌ 不再單獨封鎖裁決（Soft Veto → pacing 分批 starter，與 row 5 對稱）。WHY:SE（PEG 0.63/AR 8.8/runway 🟢）、NOW（AR 7.7）被舊 row 4 鎖觀望＝「便宜＋不對稱被趨勢閘擋在門外」型 miss;且舊條文與附錄 A INFORMATIONAL ONLY 自相矛盾（2026-07-04 持有人退役六態機）。
  - **row 8a 放寬**——估值條件 🟠 → {🟠, 🔴}（🔴 附 F2 式紀律），治 ALAB 型熱名 miss;撞名消歧（結構型數倍候選 ≠ picks 循環拐點型）。
  - **q.py 先讀後裁**——Part II 動筆前必跑，前次觀望/迴避但 to-date +30% 的錯過成本強制入 §12/§15。WHY:與 CLAUDE.md「動部位前先跑 q.py」對稱。
  - **QC-49 裁決 hysteresis**——90 天內翻面須引前次 §14b/§13 觸發器已發火，否則承繼。WHY:89 檔 35 檔翻面、14 天相鄰複查 27% 翻面率、TSM 1 天觀望→進場＝方法論 churn 非資訊。
  - **IRR 語言對齊 GRP mandate**——跨檔排序歸 GRP 三閘，5Y IRR 降為單檔確信刻度（2026-07-04 GRP 拍板）。
  - **dd-meta 新增 4 選填欄**（archetype/rearm_trigger/cycle_position/cycle_verdict）＋ 補登記 5 個既有選填欄（endo_growth_ceiling/capalloc_grade/moat_execution/moat_pricing_power/upside_5y_pct）;選填欄計數校正為 20。
  - **衛生修訂**（審查逐條）：QC-40 機械 sweep + 章節標題 lineage 括注不渲染（NU ×49 洩漏教訓）;品質分統一附錄 A veto 制;補回 `long_term_confidence` 定義（附錄 A I）＋ 補回附錄 A 字母錨點 B/D/F/G/H/I;懸空「產業風向燈」閘改接 QC-39;§14d→§14c、§6.A' 等 dangling 引用修復;QC-18 加 §3.B' 例外;靜默輸出收斂;QC-38 內部門檻 100→110KB;QC-17 R1/R2/R3、QC-31 表格對齊 + A+/A R:R 軟化為參考項。**enum 契約僅新增選填欄，schema 隨「一號到底」bump v14.5，下游 6 pipeline 前綴檢查（`^v1[234]\.\d+$` / `startswith(("v13","v14"))`）零改動。**
- **v14.6 裁決校準輪（2026-07-07，兩份驗屍實證驅動:knowledge/calibration_legacy_dca_20260707.md + calibration_v13_20260707.md）**：
  - **附錄 A 盲點 3 上修救援**——FY1/FY2 共識 3 個月上修 ≥ +10%（sourced）→ 🟠 救回 🟡;consensus 落後註記升級為觸發偵測器。WHY:DELL 5/14 觀望後三週 FY1 +40.7%、股價 +66%——5Y 分位的分母在共識快速上修時系統性過時;躲掉組同窗上修全 ≈0%，救援不誤放。
  - **row 8a 資格換變數**——AR ≥ 4 降為參考資訊（36 份實檔 0 命中，被 §11.5 機率地板數學封死＝資格死在資料上），改 26 週漲幅位置閘（< +100% 放行 / > +150% 擋 / 邊界帶 QC-42 裁量;PREREG 凍結至 2026-10）。WHY:回溯校準顯示 26 週漲幅是錯過組（+20~101%，後 +40~117%）與躲掉組（≥ +178%，後 −23~−51%）唯一乾淨分割線——爆發早期放行、爆發尾端照擋。
  - **QC-49 加「規則已退役」例外**——前次觀望係已退役閘（舊 row 4 MA / row 5 過熱 Soft Veto）所致者不受承繼保護，重跑按現行矩陣重裁。WHY:NOW 型殭屍觀望不該被 hysteresis 鎖 90 天。
  - **QC-50 錯過成本反向 critic**——觀望＋（前次錯過 >+30% 或上修 ≥+10%）強制 spawn 反駁觀望的獨立 critic;只能建議升級為條件式進場、不能強制翻面;spawn 失敗 fail-safe 維持觀望。WHY:QC-41/42/48 全部單向往下打＋QC-49 承繼＝結構性觀望棘輪;校準顯示強勢段錯過尾（33 筆 +42.7%）≈ 3× 躲掉尾（15 筆 −29.7%）。
  - **QC-51 同形狀 peer 裁決一致性對帳**——§14 定稿前 q.py --theme 查 30 天內同 archetype peer 裁決，不同裁決須在 §12 明文差異理由。WHY:2026-05-07 同日 KLAC 進場/AMAT 觀望/MU 迴避，事後 60 天全漲——橫向不一致無人對帳。
  - **反偏差防線、Hard Veto、防灌水/sourcing/管轄權規範全部不動;門檻數字 PREREG 凍結，2026-10 校準第二輪憑記分板調整。** schema 隨「一號到底」bump v14.6，下游 8 pipeline 前綴檢查同步放寬（additive）。

---

- **v14.7 結構拆分＋規則治理（2026-07-07，注意力稀釋與規則棘輪的制度解）**：
  - **核心/條件載入拆分**——六塊搬 `references/`（制度沿革 / QC-32 schema / QC-42+附錄 B 循環鏡頭 / QC-44-46 gate-sets / 即時數據協議 / HTML 輸出協議＋頁首儀表板），核心 144k→~103k 字元;各原地留 stub（硬摘要＋必讀時點），路由表在核心頂部、自檢清單加載入閘。WHY:2500 行 51 條 QC 同時在 context 稀釋寫手深度預算（QC-40 鷹架洩漏即協議過載症狀）;複利股標準流程現在只載 3 個 reference。**語意零變更**——所有規則全文原樣搬移。
  - **規則治理制度**——新增 `knowledge/rule_ledger.md`（判斷類規則登記簿:生日/事故/kill condition/歷輪審計），repo CLAUDE.md 加治理條款（判斷類規則「加一提刪一」＋新規則必填 kill condition＋每輪校準附規則審計）。WHY:規則史「每次事故 +1 條」只加不減，無刪除機制則十輪後淤泥化。
  - frontmatter description 由 ~5k 瘦身至 ~0.9k 字元（掛在每個 session 的 skill 清單，是全域 context 成本）;歷版摘要全文移入本檔。schema 隨一號到底 bump v14.7，8 個下游 pipeline prefix 檢查零改動。

- **v14.8 QC-52 DD↔ID 對帳（2026-07-08，接線輪）**：
  - **事實先讀、結論後對**——Part I 只准讀 canonical ID 的事實區塊（§3/§4 sourced 數據、產能時間表、利潤池），禁讀 §0/§5/§7 分歧敘事（防錨定，QC-17/18 哲學跨層版）;草稿完成後強制對帳 q.py 主題行機器欄（sd_verdict/clock_phase/conviction/priced_in）：一致 → §9 事實錨句式引用、分歧 → §12 明文＋terminal「建議重跑 ID」訊號（污染流轉糾錯流）、Phase II 打折（校準唯一失效格，須自身位置閘交叉驗證）、priced_in=high 須 §12 正面處理、無 ID → 標 ID gap。Fail-safe：加值層非依賴層，永不阻斷。
  - **配套**：knowledge/build_knowledge.py 產業節點加 4 欄（sd_verdict/clock_phase/conviction/priced_in）＋ q.py 主題行加印機器欄;industry-analyst v2.6 priced_in 落欄（validator 阻斷）;rule_ledger QC-52 行生效。WHY 全鏈：calibration_id_20260707（sd_verdict 量物理供需非可投資性、shortage×PhaseII 勝率 7/25、同週 DD 層無錨定判對 MU/SNDK）。

- **v14.9 判斷反萃取三件套（2026-07-08，趁強模型在把 override 能力寫成程序）**：
  - **§12.4b 裁決推理品質三檢**——① 分母爭議檢查（ORCL 20260703 原型:機械矩陣進場、人 override 觀望，「便宜的分母本身是爭議標的、壞消息是已實現事實」）② 證據權重三級制 L1 已實現事實 > L2 sourced 估計 > L3 敘事（同 ORCL）③ steelman 義務方向對稱（SNOW 20260705 §12.3b 原型:維持觀望前先寫最強買進論證再逐點回應）。
  - **§13b' 成功但劣化第二敗局**（TSLA 20260705 原型:robotaxi 成功但成低毛利營運生意、倍數框架切換吃掉勝利）——成立時強制反映進 §11.5 Bull 終端倍數。
  - **§11 多尺矛盾明文化**（MU 20260705 原型:Fwd P/E 6.5x 便宜 vs P/B 15.2x 絕對峰值——用成長股尺給循環股估值是類別錯誤）——兩尺相反禁報單尺，archetype 定優先。
  - WHY:同一套協議，強模型跑出「有護欄的判斷」、弱模型跑出「合規清單」——差距集中在這幾個 override 動作。把動作寫成必答程序，弱底座也被逼著走完。三件套為判斷類規則，已登記 rule_ledger（kill condition:兩輪校準顯示三檢從未改變任何裁決或改變後更差）;候刪提名＝盲點 1 救援（其 PEG<2+AI🟢 條件與盲點 3 上修救援及 row 9 baseline 高度重疊）。

- **v14.10 判斷反萃取第二輪（2026-07-08，系統性挖掘）**：
  - **QC-53 情境判斷手冊**——四個獨立 agent 對 18 份 v14.x DD 決策層系統性挖掘＋去重，得 32 條「協議沒要求、強模型自己做出」的判斷動作，落 `references/judgment-playbook.md`（觸發索引式:命中情境才逐條必答，防注意力稀釋）。代表條目:觸發錨型路由、第三分支/反向分支、override 附「機器對了」分支、領先導數 tripwire、管理層歸因 escrow、內部人賣出三步模板、共識三件套、Bear 地板非平穩→AR 失效、核心可守測試、AI 淨增量會計＋附著點。
  - **§14 裁決品質四問**（always-on 級，inline）——相鄰裁決雙向檢核（DECK/PLTR）/問題屬性路由:價格 vs 結構＋下限驗傷（SNDK/NKE）/唯一約束隔離（SE/ISRG）/裁決翻譯層:持有者 vs 新資金＋三選一表（SNDK/GLW/TT）。
  - **§12 補兩問**——矛盾拓撲判定:集中 vs 瀰漫（UBER）;翻面三元歸因:基本面/價格/方法論（NU/PLTR/DECK）。
  - 審計制:playbook 條目個別可審計，2026-10 逐條統計「觸發後是否改變過裁決/倉位/觸發器」，純儀式者降選做/刪。候刪提名＝附錄 A 盲點 2 救援（其救援對象 MA ❌ 已於 v14.5 退役為 pacing，疑似死碼）。

- **v14.11 商業模式解剖＋產業時鐘全 archetype（2026-07-08，補完「產業洞察」提案 #2/#3）**：
  - **§5.G 商業模式解剖（必填三件套）**——單位經濟學一張表（量價拆解餵 §11 多尺）＋價值鏈位置與 ⚑ 單點依賴（**首次消費 supply-chain 圖資料**:build_knowledge supplies 邊帶 `single` 旗標、q.py 供應鏈位置印 ⚑，掛旗者一體兩面必答護城河 or 集中度）＋營收品質拆解（recurring/量價/合約，與 §11 倍數、§6.B 口徑一致）。WHY:DD 量化模組全在數字端，機制端（怎麼賺錢、議價權卡哪節點）無固定居所;supply-chain 圖的鎖喉點資料躺著沒人消費。
  - **§9 產業時鐘一格（全 archetype 必答）**——落 dd-meta 選填欄 `industry_clock_phase`（enum I-IV，validator present 才驗）;有 ID 引 clock_phase（Phase II 依 QC-52 打折），無 ID 自判附依據。與 QC-42 `cycle_position`（循環股自身位置）分工明確。供 screener 做「產業 Phase × 個股裁決」交叉。

## v14.12（2026-07-10）— 裁決輸出收斂（大道至簡）

- **顯示稅制收斂，判斷機器一字未動**（持有人拍板;PREREG 凍結不受影響）:
  - 裁決頭銜全站只有三詞（進場/觀望/迴避），「·條件式」「（爆發候選）」等後綴/括注禁止出現在頭銜、chip、dd-meta、INDEX
  - `dca_role` canonical 四值:核心/衛星/追蹤/不持有——爆發候選/循環衛星/投機部位歸「衛星」、候選/追蹤池歸「追蹤」、「條件式」前綴廢除（盤點 85 份報告 80% 掛此前綴＝零資訊量）;legacy 7 值 validator 續收（dual-read）、新報告禁用
  - 條件性（starter 比例/倉位帽/rearm）唯一居所＝§14a 首句一行執行語（≤40 字，「{首階倉位}·{rearm 或加碼條件}」），dd-meta `rearm_trigger` 同步
  - INDEX.md 欄 4 格式＝`{裁決}｜{角色}·{執行語}`（≤40 字）
  - 下游:aggregate_dca_stats CATEGORY_ORDER 8→5、_categorize 四值歸一映射;validate_dd_meta dca_role enum additive 加四值
- WHY:2026-07-10 生產批驗屍——dca_verdict 機器層本來就只有 3 值，複雜度全在標籤層（角色 7 種 enum、頭銜自由發揮、INDEX 欄 4 動輒 150 字、五個顯示面各自表述）。矩陣內部路徑名（row 8a/8b）保留於推理層，僅輸出時翻譯。



## 2026-07-17 — QC-38 篇幅目標帶依「有無隨附文獻」分兩模式（規格校準，非規則變更）

- **改了什麼**（純目標帶擴充，實質規則零變動）：
  - 舊：單一目標帶 `~110-125KB`
  - 新：**標準模式（無隨附文獻）~110-135KB** ／ **隨附文獻模式（§4.5 觸發）~250-400KB**
  - 觸點：SKILL.md v13 變更表 size floor 列、QC-38 全節、反灌水段、深度標竿段（新增隨附文獻模式範本）；repo CLAUDE.md 篇幅 floor 表；scripts/hooks/pre-commit 註解區塊
- **沒改什麼（刻意）**：hard floor 110KB、soft warn 125KB、Part I ≥60%、七個量化表格、反灌水鐵律、pre-commit gate 數字——**全部原封不動**。gate 本來就全是下界、無上界，四份超帶報告從未觸發任何機械閘；壞掉的只有 skill prose 裡的目標帶敘述。
- **WHY**：2026-07 六份實測呈**雙峰**且成因明確——無附件的 JNJ 117KB／ASML 125KB **精準落在舊帶內**（證明規格對標準模式有效，不該動）；四份帶 §4.5 者全落 308-384KB（NFLX 308／TSM 356／ISRG 364／GE 384）。兩個獨立執行者各自做過完整壓縮重寫（NFLX 345→308、ISRG 386→364）後回報同一結論：**再壓需砍約 60% 的「分析」而非「修辭」**——因為隨附文獻模式的強制內容（§4.5 逐點 read-through ＋ 跨文件分歧裁決 ＋ 證據等級 L1/L2/L3 標註 ＋ 下游各節回填）本身就撐開篇幅。四份不是各自失控，**是規格從未為這個模式建模**。
- **治理歸類**：size floor 屬 **防灌水／格式類**，非判斷類規則（repo CLAUDE.md 規則治理條款明列「純 sourcing/格式/防灌水不在此列」）→ **不需登記 rule_ledger kill condition、不適用加一提刪一**。
- **新帶不是新配額（防誤用）**：標準模式無附件卻寫到 250KB+ ＝ 灌水嫌疑；隨附文獻模式落 250KB 且模組全實優於 400KB 注水；§4.5 是**壓縮成 read-through**，逐頁摘要 PDF ＝ 違規。
- **未 bump skill 版號**：本次不動 dd-meta schema、不動任何判斷閘，僅 prose 目標帶校準 → 維持 v14.12，下游 8 pipeline 零影響。

## 2026-07-19 — dd-meta 新增選填 `kill_metrics[]`（P2 結構化證偽，validator 選填不阻斷）

- **改了什麼**：dd-meta 新增選填欄 `kill_metrics[]`——把散文的證偽／減碼／清倉條件（§14b、§15、§11.5 Bear 觸發）抽成機器可讀條目，供市場偵測器 kill-watch（`docs/detective/data/kill_registry.json` → `scripts/build_kill_watch.py`）持續監控 thesis。每條 `metric`／`bear_threshold`／`window`（必填）＋ `source`／`last_status`（選填），與產業 ID 的 `kill_metrics[]` byte 對齊（`scripts/validate_id_meta.py`），一條 backfill／parse 路徑同時服務 DD 與 ID 兩庫。
- **紀律**：新 DD 建議填、**裁決＝進場者應填 3–5 條**；來源限報告原文寫過的觸發條件，禁止為填欄位發明門檻（honest-fail，同 catalysts 規）；可量化給數字＋方向、純質性照寫、寧缺勿造。詳見 `references/dd-meta-schema.md`「結構化證偽表」小節。
- **沒改什麼（刻意）**：validator 對 DD 端**永遠選填、不設最少條數**（與 ID v2.5+ 必填 ≥3 的差異刻意保留）→ 既有 v13/v14 全庫（444 檔）零回歸驗證通過。既有 32 檔進場 DD 走 registry backfill（`source: "dd_backfill_2026-07-19"`、llm_only）補進 kill registry，**不動任何已發布 HTML**。
- **未 bump skill 版號**：新增選填欄、additive、下游零影響（validator `^v1[234]\.\d+$` 已接受）→ 維持 v14.12。

---

## QC 條文沿革與實案全文（2026-08-07 自核心 SKILL.md 外移，A1 瘦身）

以下為 `SKILL.md`【品質管控強制規則】節原本內嵌的「給改規則的人看的」沿革敘事、WHY 論證與實案來龍去脈，2026-08-07 逐字外移至此（核心只留 writer 執行所需的條文本體）。**條文本身未變、QC 編號未變、spawn prompt 未動**;此處僅是搬家，一個案例都沒刪。

### 節首｜v13 章節 renumber 位移對照

> **v13 § 交叉引用已按 −2 位移更新**（舊 DD §7→§6、§3→§5、§9→§7、§10→§3、§11→§9、§12→§10、§5→§4、§6→§8、§4→§2、§8→§2；舊 DD §2 訊號機制移到附錄 A / metadata / 頁首儀表板）。

### QC-29｜R:R 壓力測試

> v12.0 §2 E 的 4 情境壓力測試表（Base + 壓力 A/B/C）已於 v12.3 砍除（基本面壓測已在 §6.E / §5 / §3 各章節深度覆蓋，附錄 A 重複計算無增量 alpha）。**v13 維持**：

### QC-37｜裁決單一居所

> **理由**:QC-7（核心數字一致）需存在是因為同一數字被抄寫多遍才有抄寫錯誤。消滅抄寫，一致性檢查需求自然萎縮。

### QC-38｜篇幅預算與深度標準

> **2026-08-05 改制（WHY，持有人裁決）**:v14.12「150-200KB＝帶內合格、不觸發省法」把帶下緣變成目標——實測 median 由 v14.2-14.11 的 116KB 錨上 153KB（n=72，max 509KB）;2026-08-05 對 BKNG/ANET（228-229KB）與 SIMO（116KB，2026-07-10）做同結構對比，肥的是散文不是模組（分章節預算全面超標且無機械執行點）。故：①帶下移至 75-105KB（新表以略低於 SIMO 各章實測為錨）;②合格帶語言**廢除**——不設「帶內不觸發省法」句，省法從 §2 起 binding;③分章節預算＋中場檢查升為主閘。沿革（2026-07-30 位元組解剖：附文獻只佔 3-5%、主敘事與程序性自檢是肥肉;12-gram 重複率僅 7.2-7.5%）見 changelog。三條省法依序：① 不印程序性自檢 ② 深度表只留承重列 ③ 主敘事同一數字只出現一次。

反灌水段原本附帶的實測依據（核心現只留「超帶檔案的文字實測大多是真內容，非複製貼上」一句）：

> 反向亦成立：超帶不是深度勳章，但**不得以「那是複述」草率打回**——實測 12-gram 字面重複率僅 7.2-7.5%，超帶檔案的文字大多是真內容。

### QC-39｜產業態勢變化雙向掃描

> **WHY（兩個鏡像翻車）**:① **AVGO**——報告把 moat_trend 標 ↑ widening、裁決進場，但**沒搜到**「Google 把 TPU 份額從 Broadcom 分散給 MediaTek（~95%→80%→65%, 2026→28）」這個競爭惡化 → 過度樂觀。② **SNDK**——NAND 產業面明顯很缺（結構性短缺可能到 2027/2030），報告卻**只用歷史「NAND 一定硬反轉」的均值回歸 pattern 外推**，對「這輪缺貨多結構」credit 不足、bear 機率可能壓太重 → 對結構性產業順風判斷過嚴。**兩者同根：DD 把「產業態勢」當靜態處理，該搜「它正在往哪變」時沒搜——而且兩個方向都會錯。**

### QC-40｜輸出潔淨

> **WHY**:本 skill 對 LLM 寫了大量「指令式鷹架」（`必填` / `Guardrail:` / `硬接線:` / `判定規則接線:` / `(QC-XX 教訓)` / `三段式校驗` / `三處一致`），這些是**給 LLM 執行用的內部機制**，不是給讀者看的分析。多份報告把這些**逐字抄進 HTML**，讓報告讀起來像「分析師在跟自己對帳有沒有照規則做」，而非對讀者的判斷。**LLM 必須執行這些 QC，但 HTML 只呈現分析結論本身。**

第 6 點（章節標題 lineage 括注）的 WHY：

> **WHY**:2026-07-03 批次 6/6 報告違反此鷹架不渲染原則（NU 單檔 ×49 處洩漏），規則寫了卻零 enforcement;v14.5 起機械 sweep（見【HTML 輸出指令】）強制攔截。

### QC-41｜寫稿後產業態勢獨立 critic

> **WHY**:QC-39 是 **in-loop 自律**——同一個模型「強迫自己去看」競爭/供需/其他三軸。但「想了卻錨定多頭/空頭」「C 軸全新形狀沒想到」這種漏判，**同一個腦自己抓不到**。解法是**獨立 critic**（不同 context / 不同 model instance），專門問「這份 DD 漏了或低估了什麼產業變化」。寫 DD 的 agent ≠ 驗 DD 的 agent（Boris verify-app pattern，對齊 repo CLAUDE.md「Decision-time critic」與 industry-analyst Step 8.7 強制 critic 的精神，但這裡是**寫時、DD 級**）。

「何時強制」的取捨理由：

> 理由：misjudgment 在強方向 + 方向性 moat 時代價最高（AVGO 過度樂觀 進場、SNDK 過嚴 迴避都是這類）。

撞名消歧（原置於 QC-41「收到 critic 回覆後」清單中；其中「8a ≠ picks 爆發榜、後者走 row 8b」的路由含意已收進 QC-48 邊界段）：

> **撞名消歧**:row 8a 的「爆發候選」＝**結構型數倍候選**（runway 🟢 的長抱 starter），與 picks 頁的「爆發榜」（循環拐點 × 站上年線型）是兩個概念共用一詞——後者走 §13 row 8b 循環衛星 + 附錄 B 循環位置，不走 8a/QC-48。enum 值與 dd-meta 字串不動（下游在讀），僅 prose 層以括注消歧。

「無效輸出必重試」的實案（規則本體留在核心）：

> **無效輸出＝失敗一次，必重試（2026-08-06 PLTR 盲測教訓）**……實案：PLTR 盲測中 QC-48 critic 誤讀他檔後指控 writer 造假，writer 正確隔離污染輸出，但未重試就維持了需該 critic 背書的 8a 路徑——隔離對、跳過錯。

### QC-43｜Archetype 分類器 + gate-set 路由

> **WHY**:現行 §4 Munger gate / §10 估值主錨 / QC-31 signal 是**通用「品質複利成長股」的尺**;對非複利 archetype（循環/金融/未獲利/轉機）靠模型在 prose 裡臨時換尺——SNDK 證明強模型做得到，但 ① 不一致（無人監督批次跑會時好時壞）② 不可稽核 ③ 有盲點（模板沒位置就不會出現）。QC-43 把這個隱性 override 變成**一個明確、可稽核的前置決策 + 路由**:先判 archetype，再讓各核心 gate 去讀它換尺。**這是讓 §4/§10/QC-31 適配的基石;循環（QC-42 附錄 B）、金融（QC-44）等掛在它下面。**

第 7 類（EMS/ODM，JBL 原型）的 WHY：

> WHY:JBL 用通用成長尺在 FCF margin/D-E 兩格 fail 會被誤判成「循環谷底低品質股」，換 EMS 尺（ROIC 24%✓✓、淨負債/EBITDA ~1x、ROIC 穩定）才看得出它是健康的資本輕代工商——問題不在品質而在**估值 × 週期位置**。

`archetype` 落 dd-meta 選填欄的 WHY：

> ——WHY:三軌路由（核心複利 / 衛星結構 / 衛星循環）需要它，grp_route 現以 moat 分軌，分不出衛星結構 vs 衛星循環;落欄後下游可直接讀 archetype 分群，不必反推。（僅新增選填欄，dd-meta schema 契約其餘不動;下游 pipeline 前綴檢查零改動。）

### QC-47｜archetype × QC 適用矩陣

> **WHY**:QC-1~QC-46 多為**通用成長複利股**累積的 tripwire;當 §0 判為非複利 archetype，部分 **PE/EPS/FCF-based 通用 tripwire 會與 archetype gate-set 重複或誤觸**（如金融跑 §4 FCF gate、未獲利跑 QC-31 FCF/NI）。Stage 5 = 把這些**降為「該 archetype 下由 gate-set 取代、不重複機械套用」**（**不是刪除**——刪 load-bearing 規則風險高，留人工複審）。

### QC-48｜爆發候選 Bull 冷讀 gate

> **編排說明**:QC-48 緊接 QC-41 排列（兩者同屬「寫稿後獨立 critic」類規則），依主題相鄰、非編號遺漏;數字序的 QC-42~QC-47 接於其後。

> **WHY**:§13 row 8a 的 AR 分子（P_bull × |Bull%|）是本報告自己估的——爆發候選路徑等於給樂觀估計開了一條通往「進場」的新管道，對價是消費端加一道獨立驗證（防線從「估計端」移到「消費端」）。

### QC-49｜裁決 hysteresis

> **WHY**:89 檔多報告 ticker 中 35 檔裁決翻面、14 天內相鄰複查 27% 翻面率、TSM 曾 1 天內觀望→進場——多數翻面不是世界變了，而是同一份資料被不同 run 用不同尺重讀（方法論 churn）。裁決若無「新事件觸發」門檻，會在噪音上反覆橫跳，下游 picks/PM 被迫追隨假訊號。

④ 規則已退役例外（v14.6）的 WHY：

> WHY:hysteresis 保護的是「資訊未變時的裁決穩定」，不是已廢除規則的遺產;NOW 20260703 型案例（基本面全綠、純 MA Soft Veto 壓觀望、兩天後該閘退役）不該再被承繼鎖 90 天。

### QC-50｜錯過成本反向 critic

> **WHY**:QC-41/QC-42 冷讀/QC-48 全部是**只能往下打**的 critic（打回 → 降觀望，連 spawn 失敗都降級），加上 QC-49 承繼，結構上形成觀望棘輪——裁決校準（calibration_legacy_dca_20260707.md）證實錯過尾（33 筆、平均超額 +42.7%）在強勢段約為躲掉尾（15 筆、−29.7%）的 3 倍成本。本條補上對稱的向上通道：讓「觀望」在特定證據形狀下也要接受一次獨立反駁，而不是預設安全。

### QC-51｜同形狀 peer 裁決一致性對帳

> **WHY**:2026-05-07 同一天 KLAC 判進場、AMAT 判觀望、MU 判迴避——三檔同屬半導體設備/記憶體循環、同一產業順風，事後 60 天全部大漲（+28%/+40%/+52%）。每檔 DD 獨立裁決、無人對橫向一致性負責，裁決函數對「同形狀名字」輸出隨機差異而系統從未察覺（calibration_legacy_dca_20260707.md）。

### QC-52｜DD↔ID 對帳

> **WHY**:站內 188 份 ID（80 份有機器裁決）過去在 DD 寫作時零消費——每份 DD 用 ad-hoc 搜尋從零重建產業認知，而 ID 是花了幾天四軸研究的存量。但「動筆前先讀 ID 裁決」會錨定污染（先讀到的結論變 prior）;ID 校準（knowledge/calibration_id_20260707.md）證實 `sd_verdict` 量**物理供需**非**可投資性**（shortage×Phase II 勝率 7/25、清一色 AI 硬體;同週 DD 層對 MU/SNDK 判對——正因未被 ID 錨定）。故接線鐵律＝**ID 的結論永遠不出現在輸入位置，只出現在對帳位置**（QC-17/18「指定區塊讀取」哲學的跨層版）。

### QC-53｜情境判斷手冊

> **WHY**:2026-07-08 對 18 份 v14.x DD 決策層做系統性挖掘（四個獨立 agent＋去重），萃取出 32 個「協議沒要求、但強模型自己做出來且改變了裁決/倉位/觸發器品質」的判斷動作（觸發錨型路由、領先導數 tripwire、內部人賣出三步模板、Bear 地板非平穩、核心可守測試…）。全部塞進核心會重演注意力稀釋，故走**情境觸發式手冊**:多數動作只在特定情境需要（內部人賣出、訴訟、消費品牌、單日暴跌），命中才作答。

審計制（治理層，非 writer 執行項）：

> **審計制（rule_ledger）**:手冊條目個別可審計——2026-10 校準逐條統計「觸發後是否改變過任何裁決/倉位/觸發器設計」，純儀式條目降選做或刪；新增條目走治理條款（kill condition＋加一提刪一）。

---

## 正文沿革段落（2026-08-07 A2 外移）

> 以下段落原本散在核心 SKILL.md 正文（QC 區塊以外）。它們記錄「規則為什麼變成現在這樣」，但寫手在執行時不需要——現行規則本身仍留在核心。逐字保存於此供改規則時查。

### 【v13 變更】表：章節重編列（v14→v15 映射全文）

> | **章節重編（v15，2026-08-05 商業本質優先重排）** | v14→v15 映射：§3 論點→§2（舊 §2 序章壓縮為 §2 開頭引子）、§9 產業→§3、§5 商模+Munger→§4、§7 護城河→§5（新增 §5.R）、§6 成長不動、§8 財務品質→§7、§4 財報→§8（§4.5→§8.5）、§10 治理→§9、§11 估值→§10、§12–§15 決策層→§11–§14；**子節字母全保留跟章走**（§7.F→§5.F、§8.E→§7.E、§9.F→§3.F、§10.D→§9.D、§13a-c→§12a-c、§14a-c→§13a-c）。更早的 v12→v13 位移細節見 `references/changelog.md`。 |

同表其餘被移除的沿革語：決策層疊加列原寫「舊 DCA Phase A1/A2/A3 的獨立搜尋**取消**」；「DCA 獨特輸出落 Part I」列原寫「這些原 DCA Phase A 才搜的東西」；Single Thing 列原寫「舊 DD §4.F 與舊 DCA §4 統一成 **v13 §2.F**」；擇時降級列原寫「v14.5 起 MA 狀態只餵 row 4 節奏調節」。

### 篇幅預算：v15 帶下移的 WHY

> **篇幅預算（v15，2026-08-05 持有人重議）** … WHY：v14.12「150-200KB＝帶內合格」實測把 median 從 116KB 錨上 153KB——帶下緣變目標；同結構 SIMO 116KB vs BKNG/ANET 228KB 證明肥的是散文不是模組。

> **2026-08-05 改制（WHY，持有人裁決）**:v14.12「150-200KB＝帶內合格、不觸發省法」把帶下緣變成目標——實測 median 由 v14.2-14.11 的 116KB 錨上 153KB（n=72，max 509KB）;2026-08-05 對 BKNG/ANET（228-229KB）與 SIMO（116KB，2026-07-10）做同結構對比，肥的是散文不是模組（分章節預算全面超標且無機械執行點）。故：①帶下移至 75-105KB（新表以略低於 SIMO 各章實測為錨）;②合格帶語言**廢除**——不設「帶內不觸發省法」句，省法從 §2 起 binding;③分章節預算＋中場檢查升為主閘。

> **舊規則已廢除**:舊條文寫「禁止以節省篇幅為由縮短任何章節內容／絕不壓縮內容」，實測證明它是篇幅失控的主因（三份 378-411KB）。持有人裁決＝**控 token 成本**，故改為明確預算制。

> **誠實聲明（不得對自己或用戶粉飾）**:實測 12-gram 字面重複率僅 **7.2-7.5%**，主敘事**不是**複製貼上灌水。把篇幅由 v14.12 實態 ~150-230KB 壓到 75-105KB，**確實等於再少寫下一層推導過程**——這是持有人在知情下為控 token 成本與可讀性所做的取捨（「報告長到我都不想讀」）。

### 分章節 byte 預算的 WHY

> **WHY**:2026-07-31 已證明總檔案目標不可操作（寫手到後段才知道超支，而重寫被禁）;2026-08-05 再證明「合格帶」會被錨定（150-200 帶讓 median 116→153KB），且 BKNG/ANET（228-229KB）vs SIMO（116KB）同結構對比顯示各章預算全面超標而無機械執行點。v15 預算以**略低於 SIMO 各章實測**為錨。

### §7 中場邊界檢查的 MPWR 教訓

> WHY:MPWR 教訓——**省法必須從 §2 就 binding，不是後半段補救**。

（另：「**表格與解釋的取捨方向**」一節原標「2026-07-31 反轉，v15 維持」。）

### QC-40 機械 sweep 的 WHY（實案）

> WHY:規則寫了卻零 enforcement（2026-07-03 NU ×49 處洩漏;2026-07-09/10 ANET+DELL 正文漏 row N ×29、盲點 N ×7、版號括注 ×6——清單缺這三族 pattern），機械 sweep 把「執行於心」變成「Write 前硬攔」。

### Token 紀律：critic 只餵摘錄的實測，與「約 8k」誤數字

> **「約 8k」是 2026-07-30 初版寫錯的數字，不得引用**——critic 拿到摘錄後仍會自行跑約 13 次 WebSearch 查證，8k 只在「純推理不查證」時成立;而那些查證正是產出 🔴 發現的原因（PWR 訴訟與電網政策反彈、MPWR 的 Delta×Infineon 垂直整合威脅），**不得為省 token 取消查證**。

（另：「步驟 0 資料採集與 gap 搜尋外包 sonnet」原標「v15 新增」；QC-41/48/50 critic 用 opus 原標「2026-08-06 起，隨 writer 改 sonnet 而對調」。）

### §13 決策矩陣 row 4：退出 Soft Veto 的 WHY（SE / NOW）

> WHY:SE（PEG 0.63、FPE 8th pct、AR 8.8、runway 🟢）與 NOW（AR 7.7）皆被舊 row 4「Soft Veto 鎖觀望」擋下——屬「便宜＋不對稱被趨勢閘擋在門外」型 miss;且舊條文與附錄 A 自稱 INFORMATIONAL ONLY 自相矛盾（六態機退役後 MA 狀態不再單獨封鎖裁決）。

### baseline rows 9/9b/10 的 MA ❌ 空格明文化（RMS / ROP）

> **推論（v14.11 明文化，非新規則）**… WHY:2026-07-10 批 RMS/ROP 兩個獨立執行者同批撞上此空格，皆須自行援引 v14.5 意圖補洞;本句只是把該意圖寫進矩陣，不改變任何門檻。

### 裁決輸出收斂（v14.12）的 WHY

> WHY:2026-07-10 盤點 85 份 v13/v14 報告，dca_verdict 本來就只有 3 值，但角色 7 種 enum、頭銜自由發揮、INDEX 欄 4 動輒 150 字——複雜度全在標籤層。判斷機器（矩陣路由、閘、critic）一字未動，PREREG 凍結不受影響。

（原標題為「**裁決輸出收斂（v14.12，2026-07-10 持有人拍板「大道至簡」——顯示稅制，不動判斷機器）**」。）

### row 8a 資格換變數的校準依據（全文）

> **row 8a v14.6 資格換變數的校準依據（PREREG）**:AR ≥ 4 上線以來 36 份實檔 0 命中——§10.5 反偏差防線（誠實機率紀律，**一字不動**）在數學上壓住 AR 高值，使資格條件死在自家地板上、形同虛設＝ALAB 型 miss 的直接機制。2026-07-07 回溯校準（knowledge/calibration_legacy_dca_20260707.md）:錯過組（ALAB/AMAT/SEZL/DELL，裁決後 +40%~+117%）裁決日 26 週漲幅僅 +20%~+101%;躲掉組（GLW/FORM/AXTI/RKLB/LITE/CIEN，裁決後 −23%~−51%）全部 ≥ +178%;MU +171% 落邊界帶（裁決後先 +48% 再崩——正確地曖昧）。**26 週漲幅是兩組唯一乾淨的分割線**（52 週高點距離與 13 週漲幅皆不可分），而上修軸在可得資料中多數靜態（僅 DELL/MRVL 有訊號）——故位置閘為必要條件、上修降為加強證據，**避免資格條件再次死在資料可得性上（AR ≥ 4 的覆轍）**。

### §11.4b 裁決推理三檢的 WHY

> WHY:2026-07 實讀六份決策層發現，最好的裁決全是「規則之外的判斷動作」（ORCL 燈綠而人說不、SNOW steelman 後拒絕追高、TSLA 想出第二敗局）。此三檢把這些動作變成任何底座模型都必須走的程序——**每項必須實際回答，不是宣告已檢查**。

### 附錄 A 盲點 3 上修救援的校準證據

> 校準證據（calibration_legacy_dca_20260707.md）:DELL 5/14 觀望後三週 FY1 共識 +40.7%、股價 +66%（該救未救）;躲掉組 GLW/FORM/AXTI/RKLB 同窗上修全部 ≈ 0%（救援不會誤放爆發尾端）。

（原文另註「v14.3 的 consensus 落後註記自本版升級為本救援的觸發偵測器」。）

### MA 狀態語意修訂的由來

> （原 row 9/10 字面 MA ✅ 會把 🟢 最佳進場與 🟠 回檔擋在外、且造成裁決落空;原 row 4 把破線鎖觀望＝接刀型 miss，皆已修）

（該段原標「**MA 狀態語意（v14.2 F1;v14.5 六態機退役後改稱週線結構趨勢過濾）**」。）

### v13 整併期的「移入」紀錄（各章原文）

- §2.F：「**v13 統一規則**：舊 DD §4.F 與舊 DCA §4「The Single Thing That Could Change My Mind」**合併成這一個 §2.F**;不再有兩個各自寫不相關 trigger 的 single thing。」
- §5 護城河趨勢：「**v13 升權威**:護城河趨勢是全報告與下游聚合器的**權威趨勢線**（對齊 memory `dca_trend_authoritative`）。舊 DCA Phase A1 才搜的「moat_trend ↑/→/↓ + 12 個月內變化具體證據」**移入此處就地產出**;dd-meta `moat_trend` 由此填。」
- §6.A''：「**v13 把舊 DCA Phase A2 的此項移入此處就地產出，dd-meta `runway_post_y5` 由此填**」
- §3 利潤池：「（取代舊 DCA 的 A2 利潤池獨立搜尋 — 此處就地產出，§13 直接引用不另搜）」
- §10：「**v13 融合**:本章把舊 DD §12（估值診斷：歷史分位/PEG/同業）與舊 DCA §8（Asymmetry Analysis:Bull/Base/Bear IRR + 三分量拆解 + Pattern match）合成一章。」
- §4 門檻檢核：「**v13 注意**：低估值四問 + 便宜理由檢驗五問已移除（重複 §1 trap 定性）。」
- 附錄 A：「**降級說明（v13、v14.5 更新）**:舊 DD §2 的週線結構趨勢過濾、短期 R:R、估值燈、品質分機制收進此附錄。」
- 附錄 A I：「**定義（v14.5 補回;隨 v13 改版一度被刪，QC-31 A 級條件與頁首儀表板都引用它卻無計算規則）**」
- 附錄 A §F 原重複一句「與已退役的 ETF 六態機無承繼關係。」（六態機退役的權威敘述保留在附錄 A 開頭定位段，其餘重複已刪）。


---

## v15.1（2026-08-08）文本層重寫（判斷機器零變動）

**WHY**：SKILL.md 227KB 底噪（~69k tokens）是每份 DD cache_read 的最大固定成本；三段接力實測失敗（MELI 108% vs 80% 退場門檻，同日收回）證明真槓桿是底噪本身。**改動**：核心壓至 154KB（−31%，散文壓縮＋事故敘事外移本檔）＋三塊階段性內容逐字移出為條件載入 references（`critic-gates.md` 寫稿後 critic 協議／`decision-layer.md` §11-§13 決策層全文與矩陣／`timing-appendix.md` 附錄 A 擇時）；狀態判定 Python 移 `data-collection.md`。編號系統（QC-1~53、§1-14）與全部門檻、fail 方向、觸發條件凍結未動；dd-meta schema 維持 v15.0（報告輸出契約零變動，skill 版號與 schema 本次刻意不同步）。驗收＝rule_ledger 22/22 逐條對帳＋獨立 opus diff 稽核（3 必修全補）。

### v15.1 收容：自 SKILL.md 移出的個案敘事（QC-21/QC-22 為補個案，規則層 WHY 原已在本檔）

## 1. QC-19｜標的自身重大事件強制搜尋（BSX 教訓）

規則標題所掛的「BSX 教訓」四字為 changelog 未載之唯一線索；SKILL.md 內無更長敘事，僅標題括注。**新檔壓成子句「防漏併購與訴訟」。**

> ### QC-19｜標的自身重大事件強制搜尋（BSX 教訓）

## 2. QC-21｜R:R 數學假象防禦（BSX 教訓）

> 當 Bear 股價 ≈ 現價（差距 < 5%）時，下行距離 → 0 → R:R 分母趨近 0 → R:R 爆到 100x 但無實質意義。**這代表「Bear Case 已被市場完全定價」,安全邊際實際為零。**

（門檻表 >15% / 5-15% / <5% / Bear>現價 與「極端 Bear = Bear PE × 0.8 + Bear EPS × 0.85」已逐字保留於新檔；上引「爆到 100x 但無實質意義／安全邊際實際為零」的解釋敘事被壓成子句「防分母趨零的 R:R 假象」。）

## 3. QC-22｜股價漂移檢查（CRDO 教訓）

> ③ 漂移 > 20%（**CRDO 類三週 +79%**），§1 加註「追高風險極高，建議等待 Pure MA 🟢最佳進場或回測 Bollinger 中軌」。

（「CRDO 類三週 +79%」括注被刪；10%／20% 門檻與三項動作逐字保留。）

## 4. QC-23｜競爭威脅 3 級分類（CRDO/ONTO 教訓）

> 觸發 🔴 或 ⛔ 時，§5 護城河等級相應下調並在 §1 明確標註。**範例：Marvell Golden Cable + AWS 五年協議 = 🔴;Trainium3 PCIe SerDes 改用 Synopsys = ⛔。**

## 5. QC-24｜Intraday 訊號檢查（ONTO 教訓）

> 若任一日觸發，附錄 A 建倉建議標註「近 5 日 intraday 警示」並在 §1 提醒。**範例：ONTO 4/16 intraday $295 vs 收 $266 = 🔴 動能末段訊號。**

## 6. QC-25｜Beta 雙來源驗證（CRDO/ONTO 教訓）

> **範例：CRDO 2.72 vs 3.35（23%）;ONTO 1.47 vs 2.35（60%，雙情境）。**

## 7. QC-26｜Margin 結構性測試（ONTO 教訓）

> **範例：ONTO 49.7% vs Camtek 51.6%（同業擴張），更低階技術 margin 反而更低 = 結構性質變。**

## 8. QC-27｜Revenue vs OI 增長率 Divergence（AMZN 教訓）

> **範例：AMZN Q4 2025 AWS Rev +24% vs OI +17% = 7pp divergence → 嚴重壓縮閾值。**

## 9. QC-28｜絕對成長 vs 相對成長對照（AMZN 教訓）

> **範例：AMZN AWS vs GCP 2025Q4，GCP 絕對新增 $10.0B ≈ AWS $10.3B → AWS 規模優勢在消失。**

## 10. QC-30｜同業溢價收斂壓測（LLY 教訓）

> **範例：LLY Fwd PE 26x vs NVO 11x = 138% 溢價 → 必須測試 NVO 追趕情境。**

## 11. QC-31｜基本面評級定義表 · 核心規則 4 的 PANW 範例

> 4. **附錄 A 的「都不過 → 迴避」是時機語意，不是 signal 對映**:該行描述「現在不進場」的時機，不是 signal grade 指派。**範例：PANW 短期 R:R −0.17、中期 0.23 → 不新進;但 thesis 完整（品質 10、護城河 A、估值🟡）→ signal = B。**

（規則 4 本體逐字保留，僅刪範例。）

## 12. QC-36｜5Y 目標價一致性（2308.TW 教訓）

規則標題括注「（2308.TW 教訓）」為唯一敘事線索，SKILL.md 內無更長段落。

## 13. §6.H 客戶結構深度（3661 Mariana 教訓）

> ### H｜客戶結構深度（**3661 Mariana 教訓**）
> …**「Mariana 占比超過 50%」**（此字串同時作為 §2.F Single Thing 的示例，該處已於新檔保留為 trigger 寫法示例）

## 14. §10.4 同業估值比較 · Alchip / GUC 教訓

> **禁止**用「同產業但不同業務模式 tier」的高倍數公司當 anchor（**3661 Alchip 教訓：應跟 GUC/Faraday 比，不是 AVGO/MRVL**）。

（禁止條文本體逐字保留；括注教訓被壓成子句「防跨 tier 錨定」。）

---

## 附註：已在 changelog 有記載、故本次直接丟棄不再收錄者

QC-39（AVGO 型過度樂觀 / SNDK 型過嚴的全文敘事）、QC-40（鷹架滲入 HTML 實案）、QC-41（Boris verify-app pattern 由來、PLTR A/B 對質）、QC-43（archetype 誤尺實案）、QC-47、QC-48、QC-49、QC-50、QC-51、QC-52、QC-53、§11.4b（ORCL / SNOW pattern 全文）、§12b'（TSLA robotaxi pattern 全文——新檔保留其 ≤80 字模板與「原型：robotaxi…」一句作判準錨，僅刪長敘事）、§11.3 翻面三元歸因（NU/PLTR/DECK）、§10 多尺矛盾（MU 20260705 原型——新檔保留「原型：MU 20260705」一句，因該句是判準的類別錯誤示範）、§13 四問（DECK/PLTR、SNDK/NKE、SE/ISRG、SNDK/GLW/TT——pattern 名稱作為觸發索引保留於括注）、§11.1 拓撲判定（UBER pattern）、row 4 退出 Soft Veto（SE / NOW）、baseline rows 9/9b/10 MA ❌ 空格（RMS / ROP）、§7 中場邊界（MPWR）、篇幅帶（BKNG/ANET vs SIMO）。

---

## 2026-09-01 — QC-54 白話呈現規則新增（呈現層，源頭改 = option a）

- **持有人拍板**：2026-08-31 批次（NVDA/MRVL/CRWD/CRM/VIK/ADI）4/4 首輪 QC-40 合規 0/4——§13 開場直接渲染決策矩陣機器語言（「Row 1-3 Hard Veto…皆未命中」），承重結論僅靠燈號/emoji 承載，讀起來像內部稽核文件非讀者面對的研究報告。持有人裁決＝**option (a) 源頭改**（否決另做一層白話包裝／summary layer），比照 industry-analyst v2.0→v3.0 前例（sell-side 呈現、敘事前置、附錄證據折疊、廢 dual-output）。
- **三件套**：① SKILL.md 新增 **QC-54｜白話呈現（深入淺出・賣方風）**，緊接 QC-40 之後——§1/§13 開場強制白話敘事、決策矩陣逐 row 檢核表與 Hard/Soft Veto 逐項列舉移入 `<details>`/附錄、燈號/emoji 不得單獨承載承重結論；② `references/critic-gates.md` QC-41 六軸 critic checklist 新增 **⑦ QC-54 白話呈現核**（SKILL.md 對應處同步「六軸」→「七軸」），違反一項 🟡、§13 開場全無白話敘事 ＝ 🔴；③ 範本句品質標竿——「用未確認風險的價格買進仍是為未解問題付價」（DD_VIK_20260831 §13）。
- **無版本 bump**：本次為純呈現層規則，裁決矩陣、fail-safe 方向、dd-meta schema（維持 `v15.0`）與 `id="decision"` 錨點契約一字未動，下游 pipeline 零影響——比照 QC-38（2026-07-17）等格式類規則的治理歸類，**不需登記 rule_ledger kill condition**。
- **證據**：2026-08-31 批次 4 份首輪鷹架洩漏；CRM §13 正文渲染整張 row 檢核表；兩位 critic 對「row 8」是否違規的執法標準不一致（同一份報告一位判過、一位判不過）。
