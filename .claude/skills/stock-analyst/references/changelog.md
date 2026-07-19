# stock-analyst v14.7 — changelog.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-07 v14.7 結構拆分，內容自 v14.6 原文搬移、語意零變更）。必讀時點見 SKILL.md 條件載入路由表。修改規則請同步 SKILL.md stub 與 references/changelog.md。

## 制度沿革（lineage 摘要 — 保留每條規則的 WHY）

v13 是長演進的最新一層。各版核心改動的「為什麼」濃縮如下；規則本體在【品質管控強制規則】與各章節。

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
