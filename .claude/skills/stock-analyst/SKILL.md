---
name: stock-analyst
version: v14.5
released: 2026-07-05
description: "收到股票 ticker 後，產出單一 v14.5 DD 報告 — 基本面深度（Part I，骨幹 ≥60%）＋ 投資決策層（Part II），收斂為**一個人面對的統一裁決：進場 / 觀望 / 迴避**（+ 倉位角色）。**v14.5 摘要**：§14 新增 row 8b 循環衛星條件式進場路徑（附錄 B 循環位置經五閘 + critic 冷讀後接 §14 並落 dd-meta）＋ row 4 六態機退役改進場節奏調節（MA 狀態不再單獨封鎖裁決）＋ row 8a 放寬（估值 🟠/🔴，🔴 附 F2 紀律）＋ Part II 動筆前 q.py 先讀後裁（錯過成本強制入 §12/§15）＋ QC-49 裁決 hysteresis（90 天翻面須引前次觸發器）＋ dd-meta 新增 4 選填欄（archetype/rearm_trigger/cycle_position/cycle_verdict）。v13 把舊 DD（v12.7）與舊 DCA（v1.5）整併成單一 `DD_{TICKER}_{YYYYMMDD}.html`，不再產獨立 DCA 檔。基本面研究只做一次（Part I），決策層（§12 矛盾裁決 / §13 pre-mortem+Max DD / §14 決策 / §15 複審）疊在其上不重搜。A+/A/B/C/X 訊號燈降為 metadata-only 的基本面評級（餵 screener），不再是並列 headline。短期擇時（週線結構趨勢過濾 / R:R / 估值燈）降為末段擇時附錄，純資訊不主導裁決。dd-meta schema=v14.5，新增 dca_verdict / dca_role / moat_trend（權威）/ runway_post_y5 / ev5y_pct 等決策層欄位供下游聚合器直接讀。保留 v12.6/12.7 全部深度量化模組（分部前瞻建模 / 對手 P&L 對照 / DuPont+營運資金 / 逐段 TAM/SAM / 10Y 資本配置）、yfinance 批量採集、Excel buy-side consensus（步驟零'）、QC-1~QC-49 規則、dd-meta JSON validator、隨附文件處理協議。**v14.x（schema 與 skill 版號一號到底，現 v14.5；下游 pipeline 相容讀取 v13.x 舊報告）方法論升級**：QC-39 產業態勢變化**三軸**掃描（強制搜 + 回填「競爭惡化」「結構 durability」「其他結構變數＝法規/通路/替代/商業模式的開放式 catch-all」，避免 AVGO 型過度樂觀與 SNDK 型對結構性順風 credit 不足）+ QC-40 輸出潔淨（內部 QC 鷹架不渲染進 HTML）+ QC-41 寫稿後產業態勢獨立 critic（不同 model instance 冷讀紅隊，兜底模板沒覆蓋的全新形狀）+ QC-42 循環交易鏡頭（附錄 B，僅循環/商品 archetype 觸發；平行投機軌，不碰 §14/dd-meta，治 SNDK/MU 型「一路噴卻一路不推薦」的單一鏡頭脫節;**v14.4 升級為按循環子型路由的位置錶族**——商品 through-cycle / capex 建設循環 / 需求量循環三張錶，反動能硬閘跨子型通用並新增「倍數 vs 自身歷史」閘）+ QC-43 archetype 分類器（§0 判 primary+secondary+信心，路由 §5/§11/QC-31 換 gate-set;適配基石;**v14.4 增第 7 類 EMS/ODM 代工服務**）+ QC-44 金融 gate-set（bank/insurer/broker 子型:ROTCE/CET1/NIM/P-TBV 取代 FCF/ROIC/D/E/EV-EBITDA;JPM 原型驗證）+ QC-45 未獲利高成長 gate-set（Rule-of-40/NRR/EV-S 取代 EPS-CAGR/PEG;MDB 原型）+ QC-46 轉機·受監管公用 gate-set（資產重估/SOTP/DDM/regulated ROE）+ QC-47 archetype×QC 適用矩陣（Stage 5 修剪:非複利下通用 tripwire 由 gate-set 取代不重複套，深度·契約·流程紀律永不修剪）+ **v14.3 爆發候選路徑（長抱數倍股 mandate 校準）**：§6.A'' runway_post_y5 🟢/🟡/🔴 邊界量化（🟢=Y5 末滲透率 ≤35% 或 sourced 第二 S 曲線）+ §11.5 不對稱比 AR=(P_bull×|Bull%|)/(P_bear×|Bear%|) 與 10Y 二段延伸（runway 🟢 必填）+ §14 row 8a 進場·條件式（爆發候選）（估值 🟠 可被 runway 🟢+AR≥4+非估值依賴型+moat≠↓ 推翻，衛星級 2-3% starter、雙軌加碼含論點增強觸發）+ §14b 長抱賣出分軌（核心/爆發候選的清倉觸發必須 thesis 級，估值/漲幅只准 trim）+ QC-48 爆發候選 Bull 冷讀 gate（row 8a 命中強制獨立 critic，打回降觀望）;dd-meta 新增選填 asym_ratio，enum 不變、下游 6 pipeline 零改動。觸發語：ticker / 個股分析 / DD 報告 / 股票研究 / 估值分析 / 『{ticker} dca』『{ticker} 定見』『conviction analysis {ticker}』『最終判斷 {ticker}』『該不該進場 {ticker}』『買不買 {ticker}』。"
---

## 【v13 變更：DD × DCA 整併為單一裁決報告】

**核心**：把買側深度研究（舊 DD）與投資決策層（舊 DCA）合成**一份報告、一個裁決**。讀者面對的結論只有一個 — **進場 / 觀望 / 迴避**（+ 倉位角色），不再有「訊號燈 A+ vs 裁決進場」兩個並列頭銜互相打架。

| 主軸 | v13 動作 |
|---|---|
| **統一裁決** | 人面對的唯一結論 = §14 的 **進場 / 觀望 / 迴避**（由基本面驅動）。`<section id="decision">` 為其唯一居所，research 頁「定見」欄連到 `/dd/DD_X.html#decision`。 |
| **A+/A/B/C/X 降級** | 仍照舊計算（quality × valuation 的基本面評級），但**只進 dd-meta `signal`/`verdict`（screener 依賴）+ 附錄可選顯示**，**不再是並列 headline**。 |
| **決策層疊加（不重搜）** | 舊 DCA Phase A1/A2/A3 的獨立搜尋**取消** — 基本面研究在 Part I 做一次。DCA 真正加值的決策模組（矛盾裁決 / pre-mortem+Max DD / 統一裁決 / opportunity cost / 複審）成為 Part II 疊在 Part I 之上。 |
| **DCA 獨特輸出落 Part I** | moat trend ↑→↓（§7）、runway_post_y5 🟢🟡🔴（§6）、利潤池位置（§9）、5Y IRR Bull/Base/Bear+三分量拆解+Pattern match（§11）— 這些原 DCA Phase A 才搜的東西，現在在對應 Part I 章節**就地產出**，§11-§15 直接引用，**禁止二次搜尋**。 |
| **擇時降級** | 週線結構趨勢過濾 + 短期 R:R + 估值燈收進**附錄 A（擇時，~3%）**，純資訊，**不主導 §14 裁決**（v14.5 起 MA 狀態只餵 row 4 節奏調節，不封鎖裁決）。其品質 gate / 估值燈仍餵儀表板與 metadata。 |
| **章節重編** | 舊 DD §4-§13 統一 **−2 位移**（§4→§2、§5→§3、§6→§4、§7→§5、§8→§6、§9→§7、§10→§8、§11→§9、§12→§10、§13→§11），**子節字母全保留**（§5.F→§3.F、§8.I→§6.I、§9.F→§7.F、§10.E→§8.E、§11.F→§9.F、§12.D→§10.D、§12.E→§10.E）。舊 DD §1→v13 §1。舊 DD §2 擇時機制→附錄 A。舊 DD §3 三方辯論已砍（v12.5 起）。 |
| **Single Thing 統一** | 舊 DD §5.F 與舊 DCA §5 統一成 **v13 §3.F 的「一個」binary trigger**；§13b pre-mortem 必須 cross-check 並可修正它。 |
| **dd-meta v13** | `schema: "v14.5"`、`<meta name="dd-schema-version" content="v14.5">`；保留 22 個 v12 欄 + 5 個 v13 必填欄（`dca_verdict`/`dca_role`/`moat_trend`/`runway_post_y5`/`ev5y_pct`）+ 20 個選填欄（`irr_base_pct`/`max_dd_pct`/`asym_ratio`/… + v14.5 新增 `archetype`/`rearm_trigger`/`cycle_position`/`cycle_verdict`）。見 QC-32。 |
| **size floor** | v13 單檔 hard ~110KB / soft ~125KB（added-only）。Part I 基本面 ≥60%；Part II 決策層是淨增深度（非灌水）。pre-commit gate 對 `schema":"v13` 檔強制 110KB。見 QC-38。 |

**設計守則（不可違反）**：① 只有**一個**人面對裁決（§14 進場/觀望/迴避）；A+/A/B/C/X 是 metadata，不重複當頭銜。② 基本面研究 Part I 做一次，Part II 不重搜（明確標注引用來源章節）。③ 反灌水鐵律不變（QC-38）：篇幅是深度的結果，不是目標。④ moat_trend（§7）為**權威趨勢線**，對齊 memory `dca_trend_authoritative` — 下游聚合器一律以 dd-meta.moat_trend 為準。

---

## 報告結構（v13 三層）

讀者由上而下看到的順序：

```
頁首  結論儀表板（不編號）
        一句話 thesis ≤50字 ｜ 統一裁決 進場/觀望/迴避 ｜ 倉位角色 ｜ 護城河趨勢 ↑→↓
        ｜ Y5 後跑道 🟢🟡🔴 ｜ Max DD −__% ｜ 品質燈/護城河等級/估值燈 ｜ 持有年限
        ｜ opportunity cost 一行（點名同類現持倉）｜ 5Y 機率加權 EV／IRR

Part I — 基本面深度（骨幹，≥60% 篇幅）
  §1   投資結論詳述（trap 四問 + 最關鍵監測指標表）
  §2   序章：第一性原理 × 逆向
  §3   投資論點錨定（持有期/三假設/12M對照/三風險/邊際/決策主線/§3.F Single Thing）
  §4   即時財報情報（§4.5 隨附文獻 read-through，條件式）
  §5   核心門檻檢核（Munger）
  §6   長期成長性（七問儀表板/Runway/驅動/ROIIC/壓測/AI/Y5後跑道/分部前瞻 §6.I）
  §7   護城河（報告核心）（二維拆解/Moat-to-Numbers/市佔/定價事件帳/護城河趨勢↑→↓/威脅三級/對手P&L §7.F）
  §8   財務品質監測（§8.E 長期趨勢+DuPont+營運資金）
  §9   產業格局（§9.F 逐段 TAM/SAM；利潤池位置/流向）
  §10  治理與資本配置（§10.D 10Y 資本配置 / §10.E FCF 去向+M&A 飛輪）
  §11  估值與報酬（最大融合點）
        11.1 Fwd PE 5Y分位 / 11.2 PEG / 11.4 同業(tier-correct)
        11.5 不對稱報酬 Bull/Base/Bear 5Y + 機率 + IRR/yr
        11.6 IRR 三分量拆解（EPS CAGR / re-rate / 股息+回購）
        11.7 Pattern match 歷史相似 case / 內生天花板 sanity check

Part II — 決策層（疊在基本面上，不重搜，~22% 篇幅）
  §12  矛盾辨識與強制裁決
  §13  Pre-mortem 與 Max DD（13a 不確定假設 / 13b 失敗故事三段倒推 / 13c Max DD 範圍）
  §14  決策（id="decision"）— 統一裁決 + 決策矩陣 + 14a 倉位+opportunity cost / 14b 加減碼 / 14c 持有年限
  §15  複審觸發與保質期

附錄 A — 擇時（降級，~3%）
        週線結構趨勢過濾 + 短期 R:R(3數字) + 估值燈。INFORMATIONAL ONLY，只餵 §14 row 4 節奏調節。

附錄 B — 循環交易讀數（條件性，僅循環子型 archetype；~3%）
        按循環子型選位置錶（商品 through-cycle / capex 建設 / 需求量三選一）→ 循環位置
        （深谷投降/早/中/晚/過熱頂部）+ 交易姿態 + 反動能硬閘（含閘 5 倍數 vs 自身歷史）。
        SPECULATIVE 交易姿態。位置結論（v14.5）落 dd-meta 選填欄並接 §14 row 8b 循環衛星。成長股整段省略。
```

**顯示順序（HTML 呈現）**：頁首儀表板 → §1 → §2 → … → §11 → §12 → §13 → §14 → §15 → 附錄 A →（附錄 B，僅循環/商品股觸發）。
**內部分析順序（LLM 執行）**：§0 archetype 判定（QC-43）→ §2 → §3 → §4 → §5 → §6 → §7 → §8 → §9 → §10 → §11 → 附錄 A →（附錄 B，若 QC-42 觸發）→ §12 → §13 → §14 → §15 → §1 → 頁首儀表板（先把基本面與決策層做完，再回頭寫 §1 結論詳述與頁首儀表板）。

**三個強制不變**（從 v12 繼承）：
1. 一份報告一口氣跑完，不中斷問用戶（QC-8 執行不中斷）。
2. 基本面研究只在 Part I 做一次；Part II 引用 Part I 結論，不另起獨立搜尋。
3. 裁決單一居所：人面對裁決完整陳述只在「頁首儀表板 + §14」兩處；其餘章節提及一律一行引用「見 §14」（QC-37 升級版）。

---

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

---

## 【v12.0 重要變更：分析師 / 基金經理人分工】（v13 維持，語意調整）

**本 skill 是「分析師 + 決策層」角色。** v13 起，**單一報告同時產出基本面評級（A+/A/B/C/X，metadata）與人面對的統一裁決（進場/觀望/迴避，§14）**。倉位 % 仍由 portfolio-manager skill 在組合層決定；v13 §14a 只給「倉位角色 + 初始/目標倉位區間 + opportunity cost」作為 PM 的輸入，不替 PM 拍板組合佔比。

**基本面評級（A+/A/B/C/X）對應表**（供下游 PM skill / screener 引用；v13 為 metadata，不是 headline）：

| 訊號 | 條件 | PM 層面語意 |
|:---|:---|:---|
| **A+** | quality S/A + gate 🟢 + MA 🟢/✅ + trap 🟢 + 大盤正常 | 核心候選，滿格訊號 |
| **A** | quality S/A + gate 🟡 + MA ✅ + trap 🟢 | 核心候選，進場訊號 |
| **B** | quality B + gate 🟢/🟡 + trap 🟢/🟡，或 S/A 級有一項訊號減半 | 衛星候選 |
| **C** | 多項訊號減半 / 觀察池狀態 | 觀察名單 |
| **X** | trap 🔴 或 gate 🔴 或 quality 拒絕（**v14.5:MA ❌ 移出 X 觸發**——六態機退役後 MA 狀態只餵 §14 row 4 節奏，不再單獨判 X/封鎖裁決;以 QC-31 為權威） | 迴避 / 清倉訊號 |

**v13 注意**：A+/A/B/C/X 計算邏輯不變（quality × valuation × trap × 大盤;**v14.5 起 MA 狀態只作 A+/A 的正向升級門檻，不再作 X 觸發**，見附錄 A 機制 + QC-31），但它**不是讀者面對的頭銜**。讀者頭銜 = §14 統一裁決。兩者關係：基本面評級是「這標的本身值不值得持有」的靜態品質分類；§14 統一裁決是「現在/這個價位該不該進場 + 在組合中扮演什麼角色」的決策。§14 裁決由基本面驅動（決策矩陣 Hard/Soft Veto + Baseline，見 §14）。

---

## 【品質管控強制規則(v9.0 起，v13 renumber)】

**執行原則**:本 skill 必須一口氣跑完整份報告,不得中斷詢問使用者任何問題,除非資料經 2 次 web_search 仍無法取得(此時直接停止並回報「資料不足」,不要問「你能提供嗎」)。所有規則在每份報告執行時無條件強制遵守。**v13 § 交叉引用已按 −2 位移更新**（舊 DD §8→§6、§9→§7、§10→§8、§11→§9、§12→§10、§13→§11、§7→§5、§6→§4、§5→§3、§4→§2；舊 DD §2 訊號機制移到附錄 A / metadata / 頁首儀表板）。

### QC-1｜業務權重必須引用 §9

§6 B 成長品質判斷中涉及的各業務段營收權重**必須**直接引用 §9 產業格局的營收組成數字。禁止自行估算權重。所有超過 5% 營收占比的業務段必須完整列出,權重加總必須 = 100%。若 §9 尚未完成,先完成 §9 再回來算。

### QC-2｜MA104w 必須查實際數據

MA104w（104 週移動均線）**必須**查實際數值（用於附錄 A 週線結構趨勢過濾）。**W52/W104/W250 已由 yfinance 批量採集腳本第 4 段直接算出**（見【即時數據協議】），毋須另跑 web_search/TradingView 查詢。**禁止**使用「雙年均值外推」「起點終點平均」或任何估算法。若批量腳本無法取得 MA104w,可用 MA100w 或 MA520d 替代,但必須備注「替代指標:MA100w（非 MA104w）」。同理 MA60→MA50 須備注。

### QC-3｜下檔錨點必須標示數據來源

附錄 A / §11.5 的下檔錨點必須明確標示:
- Bear PE 的來源（引用 §6.E 成長熄火壓力測試的「成長降至 10%」情境）
- Bear EPS = FY+1 EPS × 0.9 的計算過程
- Bear 股價 = Bear PE × Bear EPS
- W52 Low 和 W104 Low 仍須查詢並列為參考,但不用於 R:R 計算
- 若 Bear 股價 > 現價，標註「上行空間為負，即使 Bear Case 仍高於現價」

### QC-4｜Forward P/E 分位必須列公式

§11.1 的 Forward P/E 歷史分位必須用以下公式計算並顯示:
  分位 = (當前值 − 5Y 低) / (5Y 高 − 5Y 低) × 100%
不得使用「~70%」等概數,必須算到整數位（如 68%）。§3 或 §1 引用 5Y 均值時,數字必須與 §11.1 完全一致,禁止出現同一份報告內兩個不同的 5Y 均。

### QC-5｜§8 同業比較組必須與 §11.4 一致

§8 財務品質的同業比較表必須使用與 §11.4 橫向比較相同的對手組（至少 3 家直接競爭對手）。禁止只放 1 家對手做比較。

### QC-6｜§10 治理必須涵蓋四項

§10 公司治理章節必須包含:① 股東/股權結構（含 dual-class 投票權說明）② 資本配置方向（Capex / 回購 / 分紅的優先順序與金額）③ 管理層薪酬結構（固定薪 vs 績效獎金 vs 股權激勵的比例）④ 過去 12 個月重大內部人交易。若 web_search 無法取得第 3 或第 4 項,在該小節標註「數據限制」,不得跳過整個小節。

### QC-7｜頁首儀表板與各章節核心數字必須一致（v13 更新）

頁首結論儀表板必須與 Part I 各章節數字**完全一致**（到小數點後一位）,包括：
- 護城河等級（取自 §7 / 附錄 A B）
- 估值燈與 Fwd PE / PEG（取自 §11 / 附錄 A D）
- Pure MA 狀態（取自 附錄 A F）
- 大盤豁免狀態（取自 附錄 A G）
- 基本面評級 A+/A/B/C/X（取自 附錄 A H 機制；metadata-only）
- **統一裁決 進場/觀望/迴避**（取自 §14）
- 護城河趨勢 ↑→↓（取自 §7，權威）/ Y5 後跑道 🟢🟡🔴（取自 §6）/ Max DD（取自 §13c）/ 5Y EV·IRR（取自 §11.5）

**v13 禁止項目**：
- 禁止出現「最終倉位 X%（組合佔比）」等替 PM 拍板組合佔比的語言（§14a 只給倉位角色 + 區間）
- 禁止把基本面評級 A+/A/B/C/X 當成讀者頭銜並列於統一裁決旁（它是 metadata，附錄/小字呈現）

禁止在頁首重新計算或四捨五入。直接從對應章節複製。

### QC-7b｜§1 / 頁首禁止技術面語言

§1 投資結論詳述與頁首儀表板的所有論述必須基於基本面與 §11.5 R:R 框架內的數字推導。**嚴禁使用技術面語言作為進場/觀望/迴避的理由**（52 週高低點、支撐壓力突破、均線、RSI、成交量型態、「股價已在高位」）。技術面僅存在於附錄 A，且不主導 §14。正確做法:引用 §11.5 的目標價與 R:R 數字說明上行/下行空間。

### QC-8｜執行不中斷

LLM 必須按所有 QC 規則自動執行所有章節,不得中斷詢問使用者任何問題（技術細節、評級判斷、數據來源選擇）。所有有客觀依據的判斷必須自行決定並在 HTML 內文說明依據。若資料經 2 次 web_search 仍無法取得,標註「數據限制」後繼續執行剩餘章節,不得停下。

### QC-9｜品質分強制計算

附錄 A 開頭（基本面評級機制）必須先計算品質分:
  底分 = (護城河 + 成長持久性) / 2
  品質分 = min(底分 + 體質加減分, 10)　　← 滿分 10 分
  - 護城河:§7 評分(1-10)
  - 成長持久性:綜合 §6 成長跑道 + 成長品質 + AI 影響,給 1-10 分(AI 受益加分、AI 威脅扣分)
  兩個輸入分數必須在 §7、§6 各章節明確列出,不得只給綜合分。
  **體質檢核採附錄 A veto 降級制（v14.5 統一，取代舊「±0.5 加到底分」）**:5 項體質檢核 veto 制——0-2 項不過 等級不變 / 3 項不過 降 1 級 / 4-5 項不過 直接拒絕（完整定義見附錄 A「基本面評級機制」）。
  品質分決定品質等級:≥ 7.5 → A 級 / 6.0-7.4 → B 級 / < 6.0 → 迴避。
（v13：品質分是基本面評級的一個輸入維度，metadata-only；不直接輸出倉位 %。**品質分計算與本規則衝突時，一律以附錄 A「基本面評級機制」為單一居所/權威。**）

### QC-10｜Bollinger 位置 Python 計算

附錄 A 必須執行 Bollinger 位置計算,使用 yfinance 自動取得週線資料,Python 計算 BBand 2σ,判定現價位於上軌之上 / 軌道之間 / 下軌之下。若 yfinance 失敗,標註「數據限制:Bollinger 無法計算」並使用預設「合理」處理(不停下)。

### QC-11｜倉位角色框架定義（v13）

v13 不在報告輸出「組合佔比 X%」的硬拍板。§14a 輸出**倉位角色**（核心/衛星/投機/條件式/不持有）+ 初始/目標倉位**區間**作為 PM skill 的輸入。HTML 必須在 §14a 加註:「實際組合佔比由 portfolio-manager skill 依組合配置紀律決定;此處的倉位角色與區間為決策輸入,非組合拍板。」

### QC-12｜近 90 天產業/競爭掃描（v14.0 併入 QC-39 雙向掃描）

即時數據協議執行完畢後,在進入章節撰寫前,必須額外執行針對性搜尋。**v14.0 起此掃描升級為「產業態勢變化雙向掃描」**——不只搜「對手出新品」（靜態快照），而是強制搜「產業/競爭結構正在往哪變」（兩個方向），完整規格見 **QC-39**。最低限度仍須含:
```
[標的代碼] competitor new product / roadmap 2026
[標的產業] latest roadmap capacity 2026
```
目的:抓住生成報告當週可能剛發布的產業新聞。若有「發布日期 < 30 天」且與 §3 核心假設或 §7 護城河相關的事件,必須納入 §3 C 風險表或 §7 威脅清單,不得省略。**QC-39 是本規則的強化版,凡有明確大客戶 program / 客製設計 / B2B 集中型 / 循環性商品標的,QC-39 強制執行。**

### QC-13｜自我攻擊裁決

§14 統一裁決（與 §1 trap 定性）確定後,在寫入 HTML 前必須先執行一輪 inner monologue:
```
「假設你要推翻此裁決（進場/觀望/迴避），找出最強的 3 個反駁點。」
```
若 ≥ 1 個反駁點觸及核心論據（品質分、估值判斷、R:R 計算、護城河趨勢任一），必須:① 回頭檢查對應章節推論;② 在 §1「⚠️ 這是價值陷阱嗎？」答題區（含「空頭最強一擊」一行）明確列出該反駁點並回應;③ 若反駁成立,修正終判。禁止只列裁決結論而不做反駁測試。（注：v13 此測試同時是 §13b pre-mortem 的前置思考。）

### QC-14｜核心數據交叉一致性

以下數據在 頁首 / §11 / 附錄 A 出現時,必須引用同一來源、完全一致（到小數點後一位）:Forward P/E（指定 FY+1 或 FY+2 口徑,全文統一）、PEG、短期/中期 R:R、合理 P/E。若發現三處數字不一致 > 1%,必須停下重新計算。

### QC-15｜時效性檢查

HTML 中引用的產業/市場數據,必須標註資料發布日期或搜尋日期。若數據發布日期 > 180 天,必須加註「⚠️ 數據可能過時,需以 web_search 重新驗證」或補搜更新版本。

### QC-16｜關鍵時程具體化

以下敘述禁止模糊表述,必須帶具體日期或量化門檻:「次世代產品量產」→ MP 月份與客戶;「產能擴張」→ wafers/月 或 年化 wafers;「客戶採用」→ design win、訂單金額或時程。若無法取得具體數字,§3 假設表 H1/H2/H3 的「驗證指標」必須寫明需觀察的量化門檻。

### QC-17｜先前報告結構化讀取

執行前,先檢查 `docs/dd/DD_[TICKER]_*.html` 是否存在。**若存在,僅讀取三個區塊,其他章節嚴禁讀取:**① 最近一份的【版本修訂紀錄】② §3 B 三個核心假設 H1/H2/H3 + §3 C 三個風險 R1/R2/R3 ③ §1 最關鍵監測指標表。**禁止讀取:** §1 統一裁決（避免錨定）、§11 估值/附錄 A 數字（用當下數據重算）、§6/§7 成長護城河評分（重新獨立打分）、§9 TAM 產業數據（重搜最新）。

讀取後,本次報告跑完後在 HTML 尾部「版本修訂紀錄」下方新增【假設驗證對照】區塊（H1/H2/H3 上次→本次→邊際變化 + R1/R2/R3 是否觸發 + 裁決變化）。**嚴禁在正文章節直接複製上次文字**;institutional memory 只存在於【假設驗證對照】區塊。

### QC-18｜只讀最近一份報告

若 `docs/dd/DD_[TICKER]_*.html` 存在多份:① 依檔名日期戳排序,僅讀取日期最新的一份 ② 嚴禁讀取較早版本 ③ 嚴禁合併比較。理由:更早版本假設可能已被推翻;只讀最近一份確保比較基準為「上次對世界的最新理解」。
**例外（v14.5，§3.B' 12 個月前對照 + Inception 累積漂移）**:§3.B' 需要對照 today−365d 那份與 Inception 那份，此時**允許讀取指定舊檔的 §3.B 核心假設區塊（僅此區塊）**做 YoY / vs Inception 漂移對照,不得讀該舊檔其他章節、不得合併其裁決。QC-49 hysteresis 引用前次 §14b/§13 觸發器同屬此類「指定區塊讀取」例外。

### QC-19｜標的自身重大事件強制搜尋（BSX 教訓）

必須針對標的公司自身近 12 個月重大事件執行至少 4 組搜尋:
```
[TICKER] [公司名] acquisition merger 2025 2026
[TICKER] [公司名] class action lawsuit securities fraud
[TICKER] [公司名] clinical trial FDA approval 2025 2026        ← 醫療/生技類必搜
[TICKER] [公司名] product launch recall warning letter
[TICKER] [公司名] SEC investigation restatement
```
針對不同產業額外強制搜尋（醫療臨床/FDA、半導體客戶流失/export control、金融監管壞帳、消費食安召回、所有行業 10-K/10-Q/8-K 近 90 天）。
必須檢查的重大事件:① M&A(金額 > 市值 5% 或 5 年單筆最大 2 倍)= 🔴 列入 §3 R / §8·§10 治理 / §11 估值稀釋;② 集體訴訟 = 列入 §10 治理 + §1 陷阱重評;③ 臨床/FDA 讀數 = 引用具體讀數;④ CEO/CFO 離職、SEC 調查、財報重編 = 🔴 高風險陷阱初篩;⑤ 主要客戶流失 = 重算 §6 成長假設。若確認無重大事件,在 §10 末尾標註正面確認(🟢 過去 12 個月無...)。

### QC-20｜催化劑實現檢查

報告中若出現「即將到來」「即將發表」「預期在 X 月」等表述,**必須搜尋該催化劑是否已經發生**。
| 催化劑狀態 | 處理方式 |
|:---|:---|
| 尚未發生 | 維持「即將到來」,併列具體日期與驗證指標 |
| **已發生,市場已消化** | **絕對禁止**寫成「即將到來」;必須引用實際結果與市場反應 |
| 已發生但結果模糊 | 必須獨立分析技術細節是否與表面結論一致 |
凡 §4 Earnings Call 萃取、§3 假設、§11 估值結論提及具體時程催化劑,必須有對應 web_search 查核紀錄。

### QC-21｜R:R 數學假象防禦（BSX 教訓）

當 Bear 股價 ≈ 現價（差距 < 5%）時,下行距離 → 0 → R:R 分母趨近 0 → R:R 爆到 100x 但無實質意義。**這代表「Bear Case 已被市場完全定價」,安全邊際實際為零。**
| 下行距離 | 判斷 | R:R 處理 |
|:---|:---|:---|
| > 15% | 正常 | 直接使用 |
| 5-15% | 警示 | 有效但備註「Bear Case 已接近定價」 |
| < 5% | **R:R 失效** | 標註「⚠️ 數學假象」,禁止直接引用做進場判定 |
| Bear > 現價 | Bear 高於現價 | 標註「市場過度悲觀或 Bear 假設過樂觀,需重檢 §6.E 壓力情境」 |
R:R 失效時用「極端 Bear」(Bear PE × 0.8 + Bear EPS × 0.85)作替代下檔錨點重算。此規則適用於附錄 A R:R 與 §11.5。


### QC-22｜股價漂移檢查（CRDO 教訓）

報告撰寫期間（首次搜尋日 vs 最終報告日）若股價漂移 > 10%:① 頁首儀表板標註「⚠️ 入場窗口可能已關閉 - 近期股價 +__% 漂移」;② 附錄 A R:R 表顯示 3 個價位 R:R（當前報告日股價 / 4 週前均價 / 建議進場價）;③ 漂移 > 20%（CRDO 類三週 +79%），§1 加註「追高風險極高，建議等待 Pure MA 🟢最佳進場或回測 Bollinger 中軌」。漂移亦同步反映在 §14 進場節奏。

### QC-23｜競爭威脅 3 級分類（CRDO/ONTO 教訓）

§7 護城河「24 個月最可能瓦解護城河的變化」清單必須分級:
| 等級 | 定義 | 影響 |
|:---:|:---|:---|
| 🟡 點對點 | 單一產品 vs 單一產品 | 護城河不扣分 |
| 🔴 生態攻擊 | 對手推全棧方案、聯盟、多代合約綁定 | 護城河 **−1 分** |
| ⛔ 架構替代 | 客戶架構層級切換 | 護城河 **−2 分**，§1 陷阱定性重新評估 |
觸發 🔴 或 ⛔ 時，§7 護城河等級相應下調並在 §1 明確標註。範例：Marvell Golden Cable + AWS 五年協議 = 🔴;Trainium3 PCIe SerDes 改用 Synopsys = ⛔。

### QC-24｜Intraday 訊號檢查（ONTO 教訓）

yfinance 取資料時必須同時抓近 5 交易日 OHLC:
```python
daily5 = yf.download(ticker, period="5d", interval="1d", progress=False)
for idx, row in daily5.iterrows():
    gap_up = (row['Open'] - prev_close) / prev_close if prev_close else 0
    close_vs_high = (row['High'] - row['Close']) / row['High']
    if close_vs_high > 0.05: flag "盤中衝高回落 shooting star"
    if gap_up > 0.05 and row['Close'] < row['Open']: flag "gap up 收紅 K"
```
若任一日觸發，附錄 A 建倉建議標註「近 5 日 intraday 警示」並在 §1 提醒。範例：ONTO 4/16 intraday $295 vs 收 $266 = 🔴 動能末段訊號。

### QC-25｜Beta 雙來源驗證（CRDO/ONTO 教訓）

yfinance Beta 與 TradingView 交叉驗證:
| 差異 | 處理 |
|:---:|:---|
| < 30% | 使用 yfinance 值 |
| ≥ 30% | 兩者都顯示，WACC 用較高值（保守） |
| ≥ 50% | 附錄 A 估值燈判定的 WACC/合理倍數用較高 Beta，reasoning 註明雙情境差異 |
範例：CRDO 2.72 vs 3.35（23%）;ONTO 1.47 vs 2.35（60%，雙情境）。

### QC-26｜Margin 結構性測試（ONTO 教訓）

毛利率 YoY 下滑 > 1.5pp 時必須執行 3 項對照:① 同業同期毛利率趨勢 ② 產品組合 mix 變化 ③ 同業用相似技術 margin。
| 結果 | 判斷 |
|:---:|:---|
| 同業擴張，本標的下滑 | **結構性質變**，護城河 −0.5 分，§1 陷阱定性降為 🟡 |
| 全產業同步下滑 | 週期性，不扣分 |
| 產品組合一次性稀釋 | 記錄「管理層承諾 recover」，列入監測指標 |
範例：ONTO 49.7% vs Camtek 51.6%（同業擴張），更低階技術 margin 反而更低 = 結構性質變。

### QC-27｜Revenue vs OI 增長率 Divergence（AMZN 教訓）

§4 即時財報情報必須額外計算核心業務 Revenue YoY − Operating Income YoY = divergence:
| Divergence | 判斷 |
|:---:|:---|
| < 0% | OI 成長快於 Revenue（margin 擴張） |
| 0~3% | 接近平衡 |
| **> 3%** | **Margin 壓縮警示**，列入 §6.E 壓力測試 |
| > 7% | 嚴重 margin 壓縮，頁首儀表板加紅色警示 |
範例：AMZN Q4 2025 AWS Rev +24% vs OI +17% = 7pp divergence → 嚴重壓縮閾值。

### QC-28｜絕對成長 vs 相對成長對照（AMZN 教訓）

對於有明確可比競爭對手的業務，§7 市佔競爭表必須呈現營收 YoY %、**絕對美元新增**（季）、市場份額變化（標的 vs 主要對手）。當**對手絕對美元新增 ≥ 本標的 90%** → 觸發「規模優勢質變」警示，護城河評分重審。範例：AMZN AWS vs GCP 2025Q4，GCP 絕對新增 $10.0B ≈ AWS $10.3B → AWS 規模優勢在消失。

### QC-29｜R:R 壓力測試（v13：退役為附錄 A 的 base+bear 2 情境）

v12.0 §2 E 的 4 情境壓力測試表（Base + 壓力 A/B/C）已於 v12.3 砍除（基本面壓測已在 §6.E / §7 / §9 各章節深度覆蓋，附錄 A 重複計算無增量 alpha）。**v13 維持**：附錄 A R:R 只留 3 個數字（短/中/5Y）+ 1 行 Bear anchor;dd-meta `stress` 欄位記錄 base+bear 2 情境推導的 pass/total（標記 2/2，不是 0/4）。完整成長熄火壓測見 §6.E。

### QC-30｜同業溢價收斂壓測（LLY 教訓）

若標的 Fwd PE > 同業中位 50% 以上:① §11.4 同業比較加「收斂情境」（情境 A 對手 PE 上修至同業均 → 上行壓縮;情境 B 標的 PE 收斂 50% → 下行）;② 情境 B 股價作替代 Bear Case 與 §6.E Bear 取保守者;③ §1 標註「相對同業溢價 __%，收斂風險列為 R4」。範例：LLY Fwd PE 26x vs NVO 11x = 138% 溢價 → 必須測試 NVO 追趕情境。

### QC-31｜基本面評級 A+/A/B/C/X 定義表（強制對映，v13 metadata-only）

dd-meta JSON 的 `signal` 欄位（A+/A/B/C/X）必須按以下定義表對映，**不得自由發揮**。這張表是 thesis-level 基本面分類（metadata），與附錄 A 的 R:R 進場時機判定**正交獨立**，且與 §14 統一裁決分屬兩件事（評級 = 標的本身品質;裁決 = 現價該不該進場 + 角色）:

| 訊號 | 含義 | 觸發條件（thesis-level） |
|:---|:---|:---|
| **A+** | 滿格品質 | 品質 ≥ 7.5 + 估值🟢 + 週線結構過濾多頭（MA 🟢/✅）;**短期/中期 R:R ≥ 2.0 為參考項**（R:R informational doctrine，不作 A+ 硬性必要條件——技術/時機不主導評級） |
| **A** | 高品質進場級 | 品質 ≥ 7.5 + 長期持有信心 = 高（定義見附錄 A I）;中期 R:R ≥ 1.0 為參考項 |
| **B** | 衛星/時機不到 | 品質 ≥ 6.0 + thesis 完整，但時機不到（R:R 不足 / 估值🔴 / 過熱 / Bollinger 上軌之上） |
| **C** | thesis 存疑 | 任一觸發:品質分 < 6.0;護城河 X 級或侵蝕信號 ≥ 3;陷阱定性 = 🔴;§6F AI 取代風險 = 🔴 |
| **X** | 結構性迴避 | 任一觸發:重大治理問題/舞弊;結構性產業衰退（TAM 萎縮 + 倍數系統下移）;獲利品質崩壞（FCF/NI < 0.5 連 2 年） |

**核心規則**：
1. **R:R 不足 ≠ C**:R:R 是「進場時機」參考，不單獨觸發 thesis-level 迴避。品質 A/B 若 R:R 不過門檻，落 **B**。
2. **估值🔴 ≠ C**:估值極端高估只代表現在不該進,標的本身品質 A 級仍落 **B**。
3. **C/X 必須有 thesis-level 失敗證據**:不是「現在 R:R 不夠」，而是「這標的長期不該持有」。選 C/X 時必須在 §1 列出觸發條件對應的具體章節數據（§7 護城河、§6 衰退信號、§1 陷阱四問、QC-9 品質分）。
4. **附錄 A 的「都不過 → 迴避」是時機語意，不是 signal 對映**:該行描述「現在不進場」的時機,不是 signal grade 指派。範例:PANW 短期 R:R −0.17、中期 0.23 → 不新進;但 thesis 完整（品質 10、護城河 A、估值🟡）→ signal = **B**。
5. **批次一致性**:同批中所有「估值🔴 + 4 週動能爆衝 + 品質 A/B」的標的一律落 B（觀望，等修復），不得隨機歸 C。

**v13 與 §14 的關係**：signal（metadata）餵 screener;§14 統一裁決（進場/觀望/迴避）是讀者頭銜。典型對映:signal A+/A 多半 §14 進場或觀望（視估值/時機/Veto）;signal B 多半 §14 觀望;signal C/X 多半 §14 迴避。但**最終以 §14 決策矩陣為準**（Hard/Soft Veto 可把品質好的標的壓成觀望，moat_trend↓+moat≤B 可壓成迴避）。

### QC-32｜dd-meta JSON 硬性 schema（v14.5，validator 強制）

`scripts/validate_dd_meta.py` 對所有 v12/v13 DD 在 commit 階段強制檢查;違規 → push 失敗。LLM 必須在生成 HTML 前自我驗證 dd-meta JSON 區塊。

**v13 canonical schema（22 個 v12 必填欄 + 5 個 v13 必填欄 + 20 個選填欄）**：

```json
{
  "ticker": "NVDA",
  "schema": "v14.5",
  "date": "2026-06-21",
  "price_at_dd": 223.47,
  "signal": "A+",
  "trap": "🟢",
  "trap_label": "🟢 非陷阱",
  "moat": "S",
  "val": "🟢",
  "ma": "✅",
  "fpe_fy2": 19.21,
  "pct_5y": 22.0,
  "peg_fy2": 0.69,
  "upside_short_pct": 31.0,
  "upside_mid_pct": 66.0,
  "stress": {"pass": 2, "total": 2},
  "moat_score": 10.0,
  "growth_durability": 10.0,
  "quality_score": 10.0,
  "ai_risk": "🟢",
  "long_term_confidence": "高",
  "verdict": "A+",
  "oneliner": "≤ 200 chars 壓縮敘述",

  "dca_verdict": "進場",
  "dca_role": "核心持倉",
  "moat_trend": "↑",
  "runway_post_y5": "🟢",
  "ev5y_pct": 88.0,
  "irr_base_pct": 13.5,
  "max_dd_pct": -45.0,
  "asym_ratio": 6.2,
  "bull_5y_price": 610.0,
  "bear_5y_price": 165.0,
  "p_bull_pct": 30.0,
  "p_bear_pct": 25.0,
  "archetype": "品質複利成長",
  "rearm_trigger": "估值回落至 Fwd PE 21x（$545）或 N2 量產如期",

  "catalysts": [{"date": "2026-09-10", "type": "product", "event": "Rubin CPX 出貨節點", "impact": "高", "watch": "若延後一季 → §11.5 Bull 機率下修"}],
  "base_eps_path": {"FY26": 4.95, "FY27": 6.00, "FY28": 7.25},
  "fy_end_month": 1,
  "eps_basis": "non-gaap-usd"
}
```

**v12 沿用 22 欄的 Enum 白名單**（不變，validator 不放過）：
- `signal` / `verdict`：`A+` | `A` | `B` | `C` | `X`
- `moat`：`S` | `A` | `B` | `C` | `X`（**字母**，不是數字）
- `trap` / `ai_risk`：`🟢` | `🟡` | `🔴`（純 emoji）
- `val`：`🟢` | `🟡` | `🟠` | `🔴`
- `ma`：`🟢` | `✅` | `🟡` | `🟠` | `❌` | `-`
- `long_term_confidence`：`高` | `中` | `低`（單字）
- `growth_durability` / `moat_score` / `quality_score`：**number 1-10**

**v13 新增 5 個必填欄（schema 為 v13.x ∪ v14.x 時 validator 強制）+ Enum**：
- `dca_verdict`：`進場` | `觀望` | `迴避`（取自 §14 統一裁決，與頁首儀表板 + §14 裁決晶片三處一致）
- `dca_role`：`核心持倉` | `條件式核心持倉` | `衛星持倉` | `條件式衛星持倉` | `投機部位` | `不持有/迴避` | `候選/追蹤池`（取自 §14a，對齊 `aggregate_dca_stats.py` CATEGORY_ORDER）
- `moat_trend`：`↑` | `→` | `↓`（**單一 Unicode 箭頭**，取自 §7 權威護城河趨勢;禁止寫「持平」「holding」等文字）
- `runway_post_y5`：`🟢` | `🟡` | `🔴`（取自 §6 Y5 後跑道）
- `ev5y_pct`：**number**（取自 §11.5 的 **5Y 累積機率加權期望值 %**，**不是**年化 IRR;下游 `compute_dca_irr` 會自行年化）

**v13 選填欄（present 時才驗型）**：
- `irr_base_pct`：number（§11.5/11.6 Base case 年化 IRR %）
- `max_dd_pct`：number（§13c Max DD 範圍取下界，負數，例 −45.0）
- `asym_ratio`：number（v14.3;§11.5 不對稱比 AR，1 位小數;Bear 5Y% ≥ 0 時省略此欄）
- `bull_5y_price` / `bear_5y_price`：number（v14.3 F4;§11.5 Bull/Bear 5Y 目標價，AR Live 掛單輸入）
- `p_bull_pct` / `p_bear_pct`：number（v14.3 F4;§11.5 Bull/Bear 機率 %，與 asym_ratio 同源）
- `catalysts`：list（2026-07-05 T-minus 鏈;§1/§15 已寫入的非財報 catalyst 日程，3-6 條）
- `base_eps_path`：dict（2026-07-05 T-minus 鏈;§6.I Base-case build 的 FY EPS 終值）
- `fy_end_month`：int（2026-07-05 T-minus 鏈;會計年度截止月 1-12）
- `eps_basis`：str（2026-07-05 T-minus 鏈;`{gaap|non-gaap}-{幣別小寫}`）
- `endo_growth_ceiling`：number（§6.D 內生成長天花板 %，供 §11.6 IRR sanity check;既有欄，v14.5 補登記）
- `capalloc_grade`：str（§10 資本配置等級 `A`｜`B`｜`C`，供 §14 row 7b;既有欄，v14.5 補登記）
- `moat_execution` / `moat_pricing_power`：number 1-10（§7 二維護城河 sub-scores;既有欄，v14.5 補登記）
- `upside_5y_pct`：number（§11.5 5Y 目標價 upside %，QC-36 四處一致;既有欄，v14.5 補登記）
- `archetype`：str（v14.5;QC-43 判定的 primary archetype，7 類 enum 之一，格式照 QC-43 詞彙;三軌路由需要它——grp_route 現以 moat 分軌，分不出衛星結構 vs 衛星循環）
- `rearm_trigger`：str ≤120 字（v14.5;§14a 觀望分支「觸發條件:___」的機器可讀版——在等什麼:事件／估值門檻／回檔位。觀望裁決建議填，soft，不進 validator 必填）
- `cycle_position`：str（v14.5;附錄 B B.1 循環位置 `深谷投降`｜`早循環`｜`中循環`｜`晚循環`｜`過熱頂部`;非循環 archetype 不填）
- `cycle_verdict`：str（v14.5;附錄 B B.3 `右側可追蹤`｜`等回踩`｜`頂部觀望`｜`未觸發`;非循環 archetype 不填）

**常見 alias 錯誤**（沿用 v12，照 canonical 名稱，禁用別名）：`schema_version`→`schema`、`report_date`→`date`、`current_price`→`price_at_dd`、`peg`/`peg_3y`→`peg_fy2`、`fwd_pe`→`fpe_fy2`、`fwd_pe_5y_percentile`→`pct_5y`、`val_gate`→`val`、`ma_status`→`ma`;省略 `verdict`/`trap_label` 必補;帶文字 emoji（`🟢 受益`）→ 純 emoji;`中高`→`中`/`高` 擇一。**v13 新增 alias 警示**：`role`→`dca_role`、`verdict_human`→`dca_verdict`、`ev_5y`/`ev_pct`→`ev5y_pct`、`moat_arrow`→`moat_trend`、`runway`→`runway_post_y5`、`ar`/`asymmetry_ratio`→`asym_ratio`。

**生成 HTML 前自驗 checklist**（在輸出 JSON 前 LLM 心裡跑一遍）：
1. 22 個 v12 required field 名稱對得上 canonical
2. **5 個 v13 required field（`dca_verdict` / `dca_role` / `moat_trend` / `runway_post_y5` / `ev5y_pct`）全部存在**
3. 所有 enum 欄位值在白名單內（含 v13 五欄的 enum）
4. number 欄位是 int/float 不是 string / emoji（含 `ev5y_pct` / `irr_base_pct` / `max_dd_pct` / `asym_ratio`）
5. `moat_trend` 是單一箭頭 ↑/→/↓（非文字）
6. `dca_verdict` 與頁首儀表板 + §14 裁決晶片三處完全一致
7. `oneliner` ≤ 200 chars
8. `schema` = `v14.5`，且 HTML `<head>` 有 `<meta name="dd-schema-version" content="v14.5">`
9. `ev5y_pct` 是 5Y **累積** EV%（不是年化 IRR）

**JSON 字串內禁止 HTML**：嚴禁 `<a>`/`<strong>`/`<br>` 嵌入 JSON value（引號未跳脫會 parse error）;跨 ID 引用寫純文字檔名;換行用 `\n` 或全形分號 `；`。

**生成後自驗腳本**（HTML 寫完後跑一次）：
```bash
python3 -c "import json,re; t=open('docs/dd/DD_X_YYYYMMDD.html').read(); m=re.search(r'<script id=\"dd-meta\"[^>]*>(.*?)</script>', t, re.DOTALL); d=json.loads(m.group(1)); assert d['schema'].startswith(('v13','v14')); [d[k] for k in ('dca_verdict','dca_role','moat_trend','runway_post_y5','ev5y_pct')]; assert len(d['oneliner'])<=200"
python3 scripts/validate_dd_meta.py --report   # 確認 v13 欄位 + enum 全綠
```

#### T-minus 鏈選填欄（2026-07-05 新增）

四個選填欄（`catalysts` / `base_eps_path` / `fy_end_month` / `eps_basis`），additive-optional，validator 只驗型不驗形狀（跟 F4 群同級，不 bump schema）。落底稿規則:

- **`catalysts`**（list，3-6 條）：只收 §1 最關鍵監測指標表／§15 復審觸發表**已寫入**的、有明確日期的非財報事件。
  - `type` enum:`product` | `regulatory` | `capacity` | `guidance` | `macro` | `other`（**不含 `earnings`**——財報日由下游 yfinance 動態供給，不落底稿）。
  - `impact`:`高` | `中` | `低`。
  - `watch`:一句話寫「若怎樣 → 對 §11.5 情境的影響」。
  - 沒有合格事件就**整欄省略**（honest-fail，禁止為填欄位發明催化劑）。
  - 日期只到月/季精度時,`date` 填該期末日並加選填 `"date_precision": "month" | "quarter"`。
- **`base_eps_path`**（dict）：直接抄 §6.I Base-case build 的 FY EPS 終值,key 用 §6.I 原生 FY 標籤,**只填明文寫出的年份**（禁止內插）;幣別跟 DD 計價幣別走。
- **`fy_end_month`**（int，1-12）：會計年度截止月,從報告自身的季度標籤推（如「Q1 FY2026（2026-05-07 公布）」→ 1 月截止）;無法確定就省略。
- **`eps_basis`**（str）：格式 `{gaap|non-gaap}-{幣別小寫}`（如 `non-gaap-usd`、`gaap-twd`）,依 §6.I 用的 EPS 口徑判定。

**提醒**:yfinance 批量採集抓到的「下次財報日期」繼續**只進 §15，不進 dd-meta**（動態資料不落底稿）。

### QC-33｜推導可追溯性原則（全章節硬性）

**任何結論數字（PE / PEG / 訊號燈 / 品質等級 / 目標價 / 漂移判定 / IRR / Max DD）必須附 ≤ 3 行壓縮推導**：`輸入數字 → 計算過程 → 對下游章節 implication`。**禁止**:光寫結論不寫過程;抽象描述代替計算;implication 與下游脫鉤。

**範例（合格）**：
> PEG = 26.06x ÷ 17.9% (共識 EPS CAGR) = 1.46
> Post-Q1 print 共識上修 22% → PEG 1.18，在 1-2 合理區間
> → §11.5 implication：維持 75th 分位作合理 PE 基礎

**適用範圍**：頁首儀表板、§1、§3 三層時間軸、§5 門檻檢核、§6 ROIC/FCF 趨勢、§7 護城河變遷、§8 趨勢表、§9 議價權判定、§11 全部子節（11.1/11.2/11.4/11.5/11.6）、§13c Max DD、附錄 A。每個結論性數字旁附 1 個 `<div class="reasoning">` 三段推導。

### QC-34｜季節性過濾（YoY 對照硬性）

**§3.B' 12 個月前對照、QC-17 假設驗證、§11 估值分位、§7 護城河變遷判定**：一律使用 TTM 或年度數據，**禁用單季 snapshot**。理由：強季節性產業單季 GM/Rev 可達 ±5-10pp，會把季節雜訊誤判為結構性漂移。例外：剛公布的最新季度（催化劑判定 / §4 即時財報）可用單季，但不可用於漂移判定。

### QC-35｜漂移分級（三層時間軸觸發門檻）

§3.B 三層時間軸假設的削弱/反轉判定門檻按時間軸分級，**禁止同一閾值套所有時間軸**:
| 假設時間軸 | 觸發削弱 | 觸發反轉 |
|---|---|---|
| 2Y 假設 | 連 2 季 TTM 偏離 ≥ 5% | 連 3 季 TTM 偏離 ≥ 10% |
| 5Y 假設 | 連 4 季 TTM 偏離 ≥ 5% | 連 6 季 TTM 偏離 ≥ 10% |
| 10Y 假設 | 跨 2 年度持續偏離 | 跨 3 年度持續偏離 |
**§3.B' 漂移判定僅標示狀態（🟢/🟡/🔴），不直接觸發動作**;動作觸發回到 §3.E 既有的「連 X 季 + 絕對閾值」雙條件。

### QC-36｜5Y 目標價一致性（2308.TW 教訓）

附錄 A R:R 表的「長期（FY+5）」格 + 頁首儀表板「參考 R:R 長期」+ §11.5 5Y 目標價 + dd-meta `upside_5y_pct`（若帶）**四處數字必須完全一致**。
```
5Y 目標價 = §6.E Base 情境 5Y EPS × 長期合理 PE（由 §7 護城河分數 + §6 成長評級決定）
```
**禁止錯誤**:用 §6.E 的 10Y EPS 當 5Y;不同 EPS/PE 來源;dd-meta 與 HTML 不一致;用間接推導取代直接引用 §6.E 5Y EPS。**Bear Case 5Y 處理**:R:R 下行取**短中期 Bear**（持有期間最大跌幅）作下行錨點，而非 5Y end state Bear。

### QC-37｜裁決單一居所（v13 升級，消滅抄寫）

**人面對的統一裁決（進場/觀望/迴避）只允許完整陳述於兩處**：頁首結論儀表板 + §14（裁決晶片 + 決策矩陣）。**基本面評級 A+/A/B/C/X 完整機械推導只允許出現於附錄 A H + dd-meta**。其餘任何章節提及結論 / 裁決 / 評級，**僅允許一行引用**（「見 §14」/「見附錄 A H」），**禁止重述數字組合**（訊號燈 + 估值燈 + Pure MA + trap 的完整列舉只能出現在上述居所）。

**理由**:QC-7（核心數字一致）需存在是因為同一數字被抄寫多遍才有抄寫錯誤。消滅抄寫，一致性檢查需求自然萎縮。**trap 定性同步收斂**:保留 §6 衰退信號偵測表（數據感測器）+ §1 終判（裁決）兩處;§7 / §11 對 trap 的掛鉤改為一行引用。

### QC-38｜v13 篇幅與深度標準（hard 110KB / soft 125KB；added-only）

**目標 v13 HTML ~110-125KB**（band 上緣，由量化深掘 + 決策層自然達成），**Part I 基本面（§1+§3+§5+§6+§7+§8+§9+§10+§11）佔 ≥ 60%**;Part II 決策層（§12-§15）是淨增深度（不是灌水）。達標方式 = 完成 v12.6 五個深度模組（§6.I 分部前瞻 / §7.F 對手 P&L / §8.E DuPont+營運資金 / §9.F 逐段 TAM/SAM / §10.D 10Y 資本配置）+ Part II 四個決策模組（§12 矛盾裁決 / §13 pre-mortem+Max DD / §14 決策 / §15 複審），**不是拉長結論或回填估值/技術面**。

**pre-commit gate**:`scripts/hooks/pre-commit` 對 added 的 `"schema":"v13` 檔強制 **110KB hard / 125KB soft**;legacy v12 DD 維持 80/90KB;真要放行 lean-but-complete 報告用 `git commit --no-verify`。

**【非灌水量化閘｜每個深度模組必須產出「量化表格」而非段落】**

| 模組 | 必交量化表格（最低規格） | 數字來源 |
|---|---|---|
| §6.I 分部前瞻建模 | 每 >10% 營收業務段一列「量×價 build」:FY0 → FY+1/+2E（拆量驅動% + ASP/mix 驅動%）+ 段 OM 軌跡 + 對合併 EPS 成長貢獻% | 財報分部 + 法說 guidance + 自算 |
| §7.F 對手財務對照 | (a) top 2-3 對手完整 P&L 對照;(b) 絕對規模對照（R&D/capex 絕對額）;(c) 市佔演變表（N 年前→當前，誰吃誰） | 對手財報 + 產業報告 |
| §8.E 長期趨勢+DuPont+WC | (a) 5-7 年關鍵指標時序;(b) DuPont 逐年表;(c) DSO/DIO/DPO/CCC 逐年實算 | yfinance 三表自算 |
| §9.F 逐段 TAM/SAM | 每段 TAM（現/5Y）+ 滲透率 + 段 CAGR + value chain 位置;利潤池地圖附 $ 或 OI margin 代理 + 占比遷移 | sell-side + 自算 |
| §10.D 資本配置 track | (a) 股息/回購/capex 逐年表;(b) R&D 投入軌跡（絕對額 + R&D/Rev 逐年） | yfinance cashflow/income 自算 |
| §11.5/11.6 IRR | Bull/Base/Bear 5Y % + 機率 + 年化 IRR;三分量拆解（EPS CAGR / re-rate / 股息+回購）三列加總校驗 | consensus + 同業 multiple band + 自算 |
| §13c Max DD | 範圍（寬度 ≥ 10%p）+ 觸發時點 + 路徑風險 🟢🟡🔴 | §13b pre-mortem 推估 |

**強化自驗（HTML 寫完後）**：
1. 五個 v12.6 模組 + 七個量化表格是否都產出（不是只有段落）？缺表 → 補表。
2. 估值（§11 + 附錄 A）佔比是否仍 ≤ 20%？因擴篇幅而回填估值/技術 → 違反瘦身底線，打回。
3. 每個擴充段是否含新量化或 sourced 敘述（非同義重寫）？§8.E DuPont / CCC / DSO 必須是 yfinance 三表自算真數字，禁止概估佔位。
4. 凡引用某 §X.Y（如「見 §7.D 時間軸」），該 §X.Y 必須實際存在（禁止 dangling reference，含 v13 renumber 後）。
5. **Part I 佔比 ≥ 60%**;檔案 < 110KB（與 hard floor 一致）→ 深度不足，優先補上表缺的量化表格。
6. Part II 是否真的疊加（決策矩陣 / opportunity cost / Max DD / pre-mortem 三段倒推都到位），而非把 Part I 結論換句話重貼？

**反灌水（不變的底線）**:篇幅是深度的結果，不是目標本身。達 ~115KB 的正道是「五個基本面模組 × 真量化表格 + 四個決策模組 × 真決策內容」，**不是**同一數字換句話重寫、無 source 的長篇定性、或回填估值/技術。寧可 105KB 全自算，不要 125KB 注水。

**深度標竿（flagship 全深度，v14.2 起預設）**:每份新 DD **第一次生成就要達 flagship 全深度**（~110KB hard floor 不是事後補、更不是用 `--no-verify` 放行 lean 版）。參考範本 = `docs/dd/DD_TSM_20260623.html`（110KB）：五個量化模組全部「yfinance 三表自算的真數字表」——§8.E（DuPont 三因子 + CCC 逐年 DSO/DIO/DPO + ROIC 含/剔現金時序）、§10.D（多年 capex/股息/FCF/折舊 track + M&A 全史）、§6.I（分部 量×價 $ build）、§7.F（對手完整 P&L + 市佔演變 + 各對手策略敘述）、§9.F（逐段 TAM/SAM + 利潤池 OI margin 代理 + 三維營收 + 單位經濟）。**執行紀律**:搜尋階段就把 §8.E/§10.D 需要的多年三表（income/balance/cashflow 全欄 + AR/Inv/AP 營運資金項）一次抓齊（見【即時數據協議】yfinance 腳本），章節撰寫時直接建表，不要先寫精簡版再回頭補。`--no-verify` 僅限「純驗證/拋棄用、不上站」的報告;要上站的報告一律走 flagship 全深度 + 正常 commit 過 floor。

### QC-39｜產業態勢變化雙向掃描（v14.0，AVGO / SNDK 教訓）

**WHY（兩個鏡像翻車）**:① **AVGO**——報告把 moat_trend 標 ↑ widening、裁決進場，但**沒搜到**「Google 把 TPU 份額從 Broadcom 分散給 MediaTek（~95%→80%→65%, 2026→28）」這個競爭惡化 → 過度樂觀。② **SNDK**——NAND 產業面明顯很缺（結構性短缺可能到 2027/2030），報告卻**只用歷史「NAND 一定硬反轉」的均值回歸 pattern 外推**，對「這輪缺貨多結構」credit 不足、bear 機率可能壓太重 → 對結構性產業順風判斷過嚴。**兩者同根:DD 把「產業態勢」當靜態處理,該搜「它正在往哪變」時沒搜——而且兩個方向都會錯。**

**核心規則:產業態勢變化必須「主動搜尋」+「雙向評估」+「橫切回填」,不得靠靜態快照或歷史 pattern 外推。**

**① 強制搜尋（雙向，在 §9/§7 撰寫前完成；凡大客戶 program / 客製設計 / B2B 集中 / 循環性商品標的必跑）**

| 方向 | 強制 query（≥3 條/方向）| 抓什麼 |
|:---|:---|:---|
| **A. 競爭惡化（防 AVGO 型過度樂觀）** | `[ticker] market share gaining OR losing 2026`；`[ticker] largest customer second-source OR dual-source OR in-house`；`[competitor] design win at [ticker's biggest customer]`；`[ticker] new entrant OR displace threat 2026` | 標的在**大客戶/program 的份額是否流失**、新進入者點名、客戶是否主動分散供應商 |
| **B. 結構轉好 / durability（防 SNDK 型過嚴）** | `[industry] shortage OR oversupply structural OR cyclical 2026 2027`；`[industry] supply discipline new capacity timeline 2027 2028`；`[ticker product] demand durability AI structural` | 這輪供需是**結構性還週期性**、缺貨/過剩**能撐多久**、供給紀律、新產能時點、需求基底黏不黏 |
| **C. 其他結構變數（開放式 catch-all，防「全新形狀」）** | `[ticker OR industry] regulation OR policy OR tariff OR antitrust 2026`；`[ticker OR industry] channel disruption OR D2C OR disintermediation 2026`；`[ticker OR industry] substitute technology OR business model shift 2026`；**+ 一個開放問句**:「除了競爭與供需，這個產業/公司還有沒有任何**結構性變數正在改變**？」 | **法規/政策**（出口管制、關稅、反壟斷、補貼、藥價如 IRA）、**通路重構**（D2C、平台去中介、經銷整併、主力通路崩）、**商業模式轉移**、**替代技術/跨界蠶食**、**客戶結構性轉移**——任何「不屬於 A/B 兩軸」的產業變化 |

**② 三軸裁決(必填一句)**:綜合 A+B+C，本標的所處產業態勢 = **競爭惡化中 / 結構性轉好中 / 其他結構變動中（指名哪軸）/ 雙向拉鋸 / 靜態** + 一句 sourced 依據。**禁止只報單向**(只講利多或只講利空都是偷懶)。**A/B 是可機械化的兩軸（有閘 A/B 強制）；C 是開放式 catch-all，無法窮舉，故由 QC-41 獨立 critic 兜底**——QC-39 負責「強迫自己去看 A/B/C」，QC-41 負責「獨立 skeptic 找出你還是漏掉的（尤其 C 軸的全新形狀）」。

**③ 橫切回填（產業態勢變化影響整份 DD，必須路由進下游各節並各自留接線）**

| 下游 | 回填要求 |
|:---|:---|
| §3.C 風險 | 競爭惡化方向若成立 → 必成為一條 R(份額流失/新進入者) |
| §6 成長持久性 / §6.E 壓測 | 份額流失 → durability 扣分；**結構性 durability 證據 → §6.E 熄火情境的「合理 normalized」須據此上修或維持(不得只用歷史谷底外推)** |
| §7 moat_trend | **份額軌跡(前瞻)決定箭頭**;市佔表「3 年趨勢」改「回看 3 年 + 前瞻 2-3 年」;接 moat_trend 硬閘(見下) |
| §9 產業格局 | 供需 durability 裁決(結構/週期)寫入;利潤池流向是否可逆須明說 |
| §11.4/11.5 | **循環股 normalized 與 bear 機率必須引用『searched 的供需 durability 證據』,不得只用歷史 pattern 外推**(見下硬閘) |
| §14 裁決 | 雙向裁決進入決策矩陣考量 |

**④ 兩條硬閘(直接擋下 AVGO / SNDK 兩種病)**

- **閘 A(防過度樂觀,AVGO):** **若 #1 / 領先玩家在其最大客戶或 program 的份額正在下滑(sourced),moat_trend 不得標 ↑**(最多 →,視程度可 ↓)。例外:有 sourced 反證說明「為何此份額分散不損長期護城河」(如總 TAM 擴張使絕對額仍增 + 新客戶補上),且須在 §7 明列反證,否則一律降。
- **閘 B(防過嚴,SNDK):** **循環/商品股的 §11.5 bear 機率與 §6.E normalized 假設,必須註明依據是『searched 供需 durability 證據』還是『歷史 pattern 外推』。** 若產業有 sourced 的結構性 durability 證據(供給紀律 / 無新產能 / 需求結構黏),而報告仍用歷史谷底硬套 bear,須在 §11.5 明確說明「為何不採信結構性論點」,否則 bear 機率不得高於 base。**反向亦然**:若 durability 證據薄弱(供給可逆 / 玩家多無紀律 / 純價格無量增),則不得因「產業在缺」就調低 bear——須點明脆弱性。

**⑤ 反灌水**:QC-39 不是要寫長,而是要「搜到 + 雙向 + 接線」。產出是「雙向裁決一句 + 回填到既有各節 + 兩閘狀態各一行」,不另立冗長新章。**裁決與產業好壞無關時(如純內需公用事業)可標『產業態勢靜態,雙向掃描無重大變化』,但仍須留掃描紀錄證明有搜。**

### QC-40｜輸出潔淨：內部 QC 鷹架不得渲染進讀者面前的 HTML（v14.0）

**WHY**:本 skill 對 LLM 寫了大量「指令式鷹架」（`必填` / `Guardrail:` / `硬接線:` / `判定規則接線:` / `(QC-XX 教訓)` / `三段式校驗` / `三處一致`），這些是**給 LLM 執行用的內部機制**，不是給讀者看的分析。多份報告把這些**逐字抄進 HTML**，讓報告讀起來像「分析師在跟自己對帳有沒有照規則做」，而非對讀者的判斷。**LLM 必須執行這些 QC，但 HTML 只呈現分析結論本身。**

**禁止渲染進 HTML 的「鷹架語言」（執行於心、不落於紙）**:
1. **自我稽核紀錄**:「校驗紀錄：…」「Guardrail：…✓/✗」「§3.F 修正狀態 ✅ 不需修正」「trigger 數未變」「範圍寬度 18pp（≥10pp）✓ 非假精準」這類「我有沒有照規則做」的對帳。
2. **§13b pre-mortem 的機械三段顯示**:「第二段｜校驗 §3.F Single Thing」「第三段｜修正 §3.F」這兩段是**內部步驟**——LLM 照做（若 §3.F 需修正就**直接默默改 §3.F**），但 HTML 只呈現 **第一段失敗故事 narrative**。不顯示校驗 checklist 與「✅ 不需修正」。
3. **skill 機制詞**:「硬接線：…」「判定規則接線：…」「（必填）」「（防 X 教訓）」「（QC-XX）」當作正文呈現。**規則編號不是讀者內容**;真正的 sourced 來源（機構/日期）照常引用。
4. **dd-meta 路由/一致性註記**:「寫入 dd-meta `xxx`」「三處一致」「取下界」這類 producer-側 plumbing。
5. **章節內的「給自己看的提醒」**:「此處引用 §X.Y」式交叉註解可保留**輕量**指向，但不要寫成「我已確認 §X.Y 存在」。
6. **章節標題的 lineage 括注**（v14.5）:「（DCA Phase B 移入）」「（吸收 DCA A1/A2）」「（v13 吸收 DCA §4）」「（DD 估值 + DCA Asymmetry 合一）」這類**制度沿革括注不得渲染進 HTML 章節標題**——制度沿革已記在 skill 的制度沿革節，HTML 標題只寫章節名（如「§12 矛盾辨識與強制裁決」，非「…（DCA Phase B 移入）」）。**WHY**:2026-07-03 批次 6/6 報告違反此鷹架不渲染原則（NU 單檔 ×49 處洩漏），規則寫了卻零 enforcement;v14.5 起機械 sweep（見【HTML 輸出指令】）強制攔截。

**允許且鼓勵呈現的（這些是分析，不是鷹架）**:失敗故事 narrative（§13b 第一段）、Max DD 範圍與路徑、`<div class="reasoning">` 推導（輸入→計算→implication）、矛盾裁決的「我選哪邊 + 依據」、所有 sourced 數字與機構來源、雙向產業態勢裁決一句話結論。

**判準（一句話）**:**「這句話是寫給讀者理解這檔股票，還是寫給我自己證明我照 skill 做了？」** 後者一律不渲染。內部 QC 仍在「最終自檢清單」靜默跑，不進 HTML。

**對既有報告**:做 scaffolding sweep 時，刪鷹架語言、保留分析實質;§13b 三段壓成「失敗故事 narrative + （若有）§3.F 已據此調整」一句，不顯示校驗 checklist。

### QC-41｜寫稿後產業態勢獨立 critic（v14.1，Boris verify-app pattern）

**WHY**:QC-39 是 **in-loop 自律**——同一個模型「強迫自己去看」競爭/供需/其他三軸。但「想了卻錨定多頭/空頭」「C 軸全新形狀沒想到」這種漏判，**同一個腦自己抓不到**。解法是**獨立 critic**（不同 context / 不同 model instance），專門問「這份 DD 漏了或低估了什麼產業變化」。寫 DD 的 agent ≠ 驗 DD 的 agent（Boris verify-app pattern，對齊 repo CLAUDE.md「Decision-time critic」與 industry-analyst Step 8.7 強制 critic 的精神，但這裡是**寫時、DD 級**）。

**何時強制**（任一即觸發）:① 裁決是**強方向**（進場 或 迴避）;② moat_trend 是**方向性**（↑ 或 ↓）;③ 標的屬**競爭動態 / 循環商品 / 法規敏感 / B2B 客戶集中**型。**其餘**（穩定內需 + 觀望）→ 建議但可選。理由:misjudgment 在強方向 + 方向性 moat 時代價最高（AVGO 過度樂觀 進場、SNDK 過嚴 迴避都是這類）。

**怎麼跑**（Part I + Part II 草稿完成後、最終 Write HTML 前）:
```
Agent({
  description: "Industry red-team {TICKER} DD",
  subagent_type: "general-purpose",
  model: "sonnet",          // 不同 model instance，獨立視角
  prompt: "你是獨立產業 critic（冷讀，未參與寫稿）。以下是一份 {TICKER} DD 對產業態勢的關鍵判讀：\n
    - moat_trend = {↑/→/↓} + 依據：{§7 一句}\n
    - §9 供需 durability 裁決：{一句}\n
    - §3 核心假設 H1/H2/H3：{三句}\n
    - 統一裁決：{進場/觀望/迴避} + 主因：{一句}\n
    請沿 4 軸找出這份 DD **漏掉或低估**的產業結構變化，每軸給「有沒有 sourced 證據顯示報告判錯」：\n
    ① 競爭惡化（份額流失 / 新進入者 / 客戶 second-source / 大客戶轉單）\n
    ② 供需 durability（緊缺/過剩是結構還週期、能否撐住、供給可逆性）\n
    ③ **其他結構變數（法規/政策/關稅/反壟斷/補貼、通路重構、商業模式轉移、替代技術、客戶結構轉移）** ← 開放軸，重點找報告完全沒提到的\n
    ④ priced-in（市場是否已反映；共識/賣方目標價 vs 現價）\n
    輸出每軸：🔴 報告判錯（附 sourced 證據 + 該怎麼改）/ 🟡 報告低估（補強）/ 🟢 報告判讀無虞。只講有 sourced 依據的，不臆測。"
})
```

**收到 critic 回覆後**:
- 任一軸 🔴（且 critic 附 sourced 證據）→ **回頭實際修正受影響章節**（moat_trend / §3.C 風險 / §6.E normalized / §11.5 bear / §14 裁決），改完才 finalize。**尤其 ③ 軸 🔴 = 抓到了模板沒覆蓋的全新形狀**，必須補進 §3.C + 反映到裁決。
- 🟡 → 補強對應章節敘述。
- 全 🟢 → 不動，finalize。
- **QC-40 適用**:critic 的**結果**若改了分析，渲染的是「修正後的分析」（如 §3.C 多一條 sourced 風險），**不是**「critic 說 X / 我跑了 critic」這種過程對帳。critic 過程不進 HTML。

**撞名消歧**:row 8a 的「爆發候選」＝**結構型數倍候選**（runway 🟢 的長抱 starter），與 picks 頁的「爆發榜」（循環拐點 × 站上年線型）是兩個概念共用一詞——後者走 §14 row 8b 循環衛星 + 附錄 B 循環位置，不走 8a/QC-48。enum 值與 dd-meta 字串不動（下游在讀），僅 prose 層以括注消歧。
- **2 次 spawn 仍失敗 / critic 無回覆** → 標「獨立 critic 未能執行」於內部自檢，不阻斷 finalize（但 high-stakes 進場裁決建議人工補一輪）。

**邊界**:QC-41 是 backstop 不是主力——主力仍是 QC-39（強迫去搜）。critic 只負責「找你漏的」，尤其 C 軸無法窮舉的部分。**不要因為有 QC-41 就鬆懈 QC-39 的三軸搜尋。**

### QC-48｜爆發候選 Bull 冷讀 gate（v14.3，row 8a 命中強制）

> **編排說明**:QC-48 緊接 QC-41 排列（兩者同屬「寫稿後獨立 critic」類規則），依主題相鄰、非編號遺漏;數字序的 QC-42~QC-47 接於其後。

**WHY**:§14 row 8a 的 AR 分子（P_bull × |Bull%|）是本報告自己估的——爆發候選路徑等於給樂觀估計開了一條通往「進場」的新管道，對價是消費端加一道獨立驗證（防線從「估計端」移到「消費端」）。

**觸發**:row 8a 條件（runway 🟢 + AR ≥ 4 + 非估值依賴型 + moat ≠ ↓ + 估值 ∈ {🟠, 🔴};v14.5 放寬，🔴 時另附 F2 式紀律）全過時，**必須 spawn 不同 model instance 的獨立 critic**（spawn 機制同 QC-41），專門冷讀 §11.5 Bull 列三件事:
1. Bull 依據是否引用 §9.F 滲透率算術（含關鍵分部量×價骨架），非敘事式 Bull;
2. P_bull 是否與 §11.7 pattern match 的歷史實現 IRR 相容（歷史 case 5 年 IRR 遠低於本案 Bull 隱含 IRR → 要求解釋差距）;
3. §6.A'' runway 🟢 的 sourced 證據（滲透率推導 / 第二曲線來源）是否真實存在、可回溯。

**收到 critic 回覆後**:critic 判「Bull 依據不成立」（任一項 🔴）→ 裁決降 row 8 觀望，§14 以一句話記錄 critic 結論（QC-40:過程對帳不渲染，只留修正後結論）。critic 通過 → 頁首儀表板裁決晶片副標必標「爆發候選」。2 次 spawn 失敗 → 標「QC-48 未能執行」，**裁決保守降 row 8 觀望**（與 QC-41 的不阻斷不同——8a 是升級路徑，驗證失敗不得升級）。

**邊界**:QC-48 只驗 Bull 依據與 runway 證據，不重審整份報告（那是 QC-41 的職責）;兩者可同時觸發、各跑各的。

### QC-42｜循環交易鏡頭（v14.1 增補、v14.4 轉正 v0.2、v14.5 附錄 B 結論落 §14 row 8b + dd-meta；SNDK / MU 教訓）

> **v0.2 一句話（v14.4 三樣本 ORCL/JBL/MU 轉正）**:QC-42 從「單一商品 through-cycle 錶」升級為「**按循環子型路由的位置錶族**」（商品 / capex 建設 / 需求量三張錶），反動能硬閘跨子型通用並新增閘 5「倍數 vs 自身歷史」。參考實作:`docs/dd/DD_ORCL_20260703.html`（capex 循環）/ `docs/dd/DD_JBL_20260703.html`（EMS 需求量循環，B.5 為錶族設計母本）/ `docs/dd/DD_MU_20260622.html`（原生商品 6/6）附錄 B。**明標投機的位置錶族本體 v0.1 不變。**
> **v14.5 轉正（推翻 v0.2「不碰 §14/不寫 dd-meta」拍板）**:附錄 B 的循環位置結論改**落 dd-meta 選填欄**（`cycle_position`／`cycle_verdict`，非循環 archetype 不填）並**接 §14 row 8b「循環衛星條件式進場」**。WHY:v0.2 曾為保護下游過渡而不落 dd-meta，但這使三軌循環軌 **0 檔可執行**（handoff Task 2 要求循環衛星進場須「DD 裁決＝進場」，而 §14 對拐點循環股結構上永遠給不出進場、trailing 品質閘必掛 veto → picks 爆發正式榜 5 檔 0 檔有 DD 進場），picks 被迫改用 screener 代理規則（`fail_criteria ∩ {fcf,roic}`）路由，原型驗證 ORCL 1/5、JBL 0/5 不可靠。2026-07-05 持有人批准轉正:附錄 B 位置經 QC-42 反動能五閘與獨立 critic 冷讀後，可作 row 8b 的進場依據，並機器可讀落 dd-meta。**明標投機的交易姿態語言（trade_stance）與 SPECULATIVE 標籤仍在附錄 B，不改。**

**WHY**:本 skill 是**單一鏡頭**——只問「值不值得長抱的好公司、在合理價」。循環/商品股在 cycle **每一個點**（含底部 GAAP 虧損、Munger gate 最紅）都答不過這題 → 投資軌（§14）結構上幾乎永遠「迴避/觀望」。但循環股的錢在 **Game 2**（在投降買、在延伸賣），是**另一種紀律**。SNDK（$40→$2,185）、MU（$103→$1,134）一路噴而 DD 一路「不推薦」的脫節，根因**不是 gate 算錯**（基本面裁決是對的——SNDK 報告已用 §11.5 正規化盈餘力算出公允 $150-500、識破 peak-EPS 假象、moat↓ 迴避），而是**缺一條鏡頭**：單一鏡頭量得到「長抱品質」，量不到「循環位置 + 交易姿態」。QC-42 加一條**平行、明標投機**的循環交易讀數（附錄 B）;**v14.5 起其位置結論經五閘 + critic 冷讀後接 §14 row 8b（循環衛星條件式進場）並落 dd-meta 選填欄**（沿革見上方 v14.5 轉正框）。

**① 觸發（v0.2 改由 QC-43 驅動）**:**QC-43 判定 primary 或 secondary ∈ 循環子型（archetype #2 循環/商品、或 #7 EMS/ODM 帶需求量 sleeve、或標的下跌本質是 capex 建設循環）即觸發附錄 B**，並選對應位置錶;非循環的成長複利股整段省略、零行為改變。（v0.1 用「≥2 商品觸發項」當窄門，會把 ORCL[命中 1/5]、JBL[0/5] 這類非商品循環擋在門外——原型證明它們需要的是別張錶，不是被排除。）

**商品子型判定（下列 ≥2 命中 → 用商品 through-cycle 錶）**:
- 近 5-7 年 ≥1 個 GAAP 虧損年（循環見骨）
- peak-to-trough 毛利率擺動 > ~20pp
- 營收主由商品 ASP 驅動（price-taker，非自主定價）
- 產業 ∈ {記憶體/DRAM/NAND、礦業/材料/稀土、化工、航運、鋼鐵、太陽能、油氣 E&P、部分晶圓/設備}
- capex/rev 結構性 > 15% 且 ROIC 高度擺動
未達商品 ≥2 但 QC-43 仍判循環 → 依循環驅動來源選 **capex 建設循環錶（ORCL 型）** 或 **需求量循環錶（EMS/ODM，JBL 型）**。

**路由判別式（v0.2 核心;三樣本 ORCL/JBL/MU 定案；ORCL B.4）**:先判標的有無「真商品/循環 sleeve」——下跌若是 capex 建設循環或需求量週期（非商品 ASP through-cycle），選對應子型錶並明標「非商品 through-cycle」;若根本無循環 sleeve（純成長 mis-route，如漏斗代理規則比 QC-42 商品定義寬而誤路由），B.0 註明後整段可省略。原型證明單一商品錶對非商品循環只 ~2.5-3/6 訊號有效（ORCL capex、JBL EMS），失效子集與頂部訊號機制各異。

**② 循環位置錶族（按子型路由;錨自身 through-cycle 區間，非動能）**——位置一律落 深谷投降 / 早循環 / 中循環 / 晚循環 / 過熱頂部，多數決 + 一句 sourced 裁決;差別在用哪張錶:
- **商品錶（through-cycle，MU 型）**——6 訊號原樣保留（MU 驗證 6/6 可用）:P/B vs **自身**區間（非絕對值）/ 量 vs 價（bit·出貨 vs ASP）/ GM vs 自身區間 / 供給紀律 / 庫存 / 情緒部位。用於記憶體/礦業/航運/鋼鐵/化工/太陽能/油氣等 ASP price-taker。
- **capex 建設循環錶（ORCL 型）**——6 訊號:capex/折舊比 / 產能利用率爬坡 / RPO（或 backlog）vs capex 覆蓋 / 交易對手信用（客戶集中 + 付款能力）/ 情緒部位 / 量 vs 價。商品錶的 P/B、GM-swing、商品供給紀律對 capex 循環 N/A（資本輕轉基建，book value 非有效錨）。
- **需求量循環錶（EMS/ODM，JBL 型）**——5 訊號:book-to-bill（或需求量拐點）/ 客戶庫存去化（唯一從商品錶直接沿用者，EMS 最有效）/ **倍數 vs 自身歷史（re-rate 均值回歸）** / 終端·hyperscaler capex 週期位置 / 情緒部位。商品錶的 P/B、GM-swing 對結構性薄毛利 + 買回縮權益的 EMS N/A。

**③ 交易姿態 + 反動能硬閘（跨子型通用）**:
位置→姿態:深谷投降→積極分批建立 / 早→分批建立 / 中→持有不加 / 晚→分批了結 / 頂→清光不碰。
硬閘（override 上表，反動能;逐條檢查;**跨三張錶通用**）:
- 閘 1:位置 = 晚/頂 → 姿態**不得**為任何「建立」，無論漲多兇。
- 閘 2:成長 = ASP-only + 量持平/降 → 最多「持有」，傾向了結（商品錶適用;需求量錶無商品 ASP 時此閘退化）。
- 閘 3:P/B > 自身 through-cycle 中位 2x → 禁新建立（商品錶適用;capex/EMS 型 P/B N/A 時由閘 5 承接）。
- 閘 4:訊號互相矛盾 → 標「位置不明，觀望」，不硬給姿態。
- **閘 5（v0.2 新增，倍數 vs 自身歷史;跨子型通用，補 re-rate 頂盲區）**:TTM/Fwd 本益比或 EV 倍數 > 自身歷史高區（如 > 5Y 中位 ×1.5、或貼/破歷史峰）→ 禁新建立。**WHY**:JBL 發現既有四閘全為 peak-EPS 商品頂設計（商品頂部 P/E 低、因盈餘見頂），對「倍數重估頂」（高 P/E、非 peak-EPS，如 JBL 46x TTM 均值回歸）完全不可見;此閘給 re-rate 型循環頂部防護。
- 核心:**最敢在投降出手、最戒備在延伸段。若它在 blow-off 喊買 = 設計失敗。**

**④ 標籤 / 與投資軌關係 / 落欄接線（v14.5 改）**:
- 附錄 B 交易讀數全程冠「投機/交易，非投資」;交易姿態（trade_stance）+ 時間框架（循環，季-年）僅出現在附錄 B HTML，屬**交易**語言。
- 兩軌可（且常）背離:頂部多收斂（皆遠離）;**底部背離**（投資軌長抱視角「迴避」+ 交易軌「積極建立」）= 現行 skill 產不出、本鏡頭的**獨門價值**——v14.5 的 row 8b 正是把這種「深谷投降/早循環 + 五閘全過」的底部背離收斂成一個**可執行的循環衛星進場**（倉位上限 3% 軌別天花板）。
- **落 dd-meta 選填欄（v14.5）**:附錄 B 位置結論寫入 `cycle_position`（深谷投降｜早循環｜中循環｜晚循環｜過熱頂部）＋ `cycle_verdict`（右側可追蹤｜等回踩｜頂部觀望｜未觸發）;非循環 archetype 不填（整欄省略）。**接 §14 row 8b**:位置 ∈ {深谷投降, 早循環} + 五閘全過 + moat 底線 + 獨立 critic 通過 → row 8b 進場·條件式（循環衛星）;critic 失敗 → 降回 row 8 觀望（不對稱原則:驗證失敗不得升級）。`trade_stance` 仍**僅進 HTML 不入 dd-meta**（交易姿態是投機語言，不進機讀決策層）。schema 版號隨「一號到底」bump（見 QC-32，enum 契約僅新增選填欄，下游 pipeline 前綴檢查零改動）。

**⑤ 雙制度（MU 型）**:有 secular sleeve（如 HBM）+ commodity sleeve → 循環鏡頭只套 commodity sleeve，secular sleeve 一句話另計（不隨循環賣）。

**⑥ 復用 + 反灌水**:~80% 是把**已有模組**（§11.5 正規化盈餘力 / QC-39 軸 B 供需 durability / §8 GM·庫存 / §11 倍數分位 / P/B）合成成交易讀數 + 子型 cycle 位置錶 + 紀律閘，**不新增搜尋、不另立冗長章**。產出 = 觸發/子型判別一句 + 位置一句 + 姿態一句 + **對應子型位置錶（商品 6 訊號 / capex 6 訊號 / 需求量 5 訊號其一）** + 兩軌背離一句。QC-40 適用（不渲染鷹架語言）。

**⑦ priceToBook 採集**:批量採集腳本 info 欄位加抓 `priceToBook`、`bookValue`（循環股 P/B 是核心錨）;非循環股不用即可。

### QC-43｜Archetype 分類器 + gate-set 路由（v14.1 Stage 1，§5/§11/QC-31 適配的基石）

**WHY**:現行 §5 Munger gate / §11 估值主錨 / QC-31 signal 是**通用「品質複利成長股」的尺**;對非複利 archetype（循環/金融/未獲利/轉機）靠模型在 prose 裡臨時換尺——SNDK 證明強模型做得到，但 ① 不一致（無人監督批次跑會時好時壞）② 不可稽核 ③ 有盲點（模板沒位置就不會出現）。QC-43 把這個隱性 override 變成**一個明確、可稽核的前置決策 + 路由**:先判 archetype，再讓各核心 gate 去讀它換尺。**這是讓 §5/§11/QC-31 適配的基石;循環（QC-42 附錄 B）、金融（QC-44）等掛在它下面。**

**執行**（搜尋完成後、進章節前;§0 宣告）:判定本標的 archetype，在 §1 開頭/頁首寫 **primary（必填）+ secondary（選填，blend 用）+ 信心（高/中/低）+ 財務指紋證據一句**。

**archetype 列舉（v14.1 起手 6 類 + v14.4 增第 7 類）**:
1. `品質複利成長`（default;現行通用 gate）
2. `循環/商品`（投資軌維持 + QC-39 閘 B normalized + QC-42 附錄 B 交易軌;子型見 QC-42 錶族——商品 / capex 建設 / 需求量）
3. `金融`（細分 bank / insurer / broker;gate-set 見 **QC-44**）
4. `未獲利高成長`（gate-set 見 **QC-45**;Rule-of-40 / NRR / FCF 轉正路徑）
5. `轉機/特殊情境`（gate-set 見 **QC-46**;資產重估 / SOTP / normalized earning power）
6. `受監管公用/穩定內需`（gate-set 見 **QC-46**;DDM / 殖利率 / regulated ROE + QC-39「態勢靜態」）
7. `資本輕·低毛利·需求週期·代工服務（EMS/ODM）`（**v14.4，JBL 原型**）——毛利結構性薄（~8-10% 窄帶、非商品 ASP、非品質複利 pricing power），品質的正確度量是 **ROIC + 資產周轉 + CCC**（非 FCF margin，後者對 EMS 結構性 fail 是類別錯誤）。**gate-set**:§5 FCF margin → **ROIC + 資產周轉**（買回縮權益使 P/B、ROE、D/E 皆失真，改看資本效率）;加 **客戶集中風險**（top-1/5 客戶% + 議價權）+ **需求/量週期位置**;§11 主錨加 **倍數 vs 自身歷史（re-rate 均值回歸）**——EMS 頂部是倍數重估頂（高 P/E、非 peak-EPS）。循環軌走 **QC-42 需求量循環錶**。WHY:JBL 用通用成長尺在 FCF margin/D-E 兩格 fail 會被誤判成「循環谷底低品質股」，換 EMS 尺（ROIC 24%✓✓、淨負債/EBITDA ~1x、ROIC 穩定）才看得出它是健康的資本輕代工商——問題不在品質而在**估值 × 週期位置**。

**路由規則**:
- primary 決定 §5 門檻組 / §11 估值主錨 / QC-31 signal 對映用哪套（複利 = 現行;金融 = QC-44;循環 = 現行投資軌 + 附錄 B 對應子型錶;EMS/ODM = 第 7 類 gate-set[ROIC+周轉+客戶集中+需求量週期+倍數均值回歸] + QC-42 需求量循環錶）。
- **blend（有 secondary）**:兩套都跑、標背離。範例:MU = 循環 + secular(HBM);GRAB/HOOD = 金融 + 未獲利;fintech 常見。
- **信心低**:預設用 `品質複利` gate + 把疑似 archetype 當疊加/附錄跑 + 明標「archetype 待確認」。
- **支付網絡（MA 型）/ 交易所 / 資產輕金融科技**:雖名為「金融」，但**資產輕、高 ROIC/FCF** → 歸 `品質複利`，**不套 QC-44 銀行/保險 gate**（避免把好複利股誤判成金融）。

**護欄（同 QC-42 精神，防新僵化）**:archetype 只換 **gate-set / 估值主錨 / signal 對映**;**永不碰**深度地板（QC-38）、流程紀律（QC-13/39/41）——那些全 archetype 通用。模型必須明寫「archetype + 信心 + 換了哪套 gate」（隱性 override → 可稽核 logged decision）。**§0 primary archetype 落 dd-meta 選填欄 `archetype`（v14.5，additive-optional，格式照本規則 7 類 enum 詞彙;信心低時仍填疑似 primary 並在 HTML 標「待確認」）**——WHY:三軌路由（核心複利 / 衛星結構 / 衛星循環）需要它，grp_route 現以 moat 分軌，分不出衛星結構 vs 衛星循環;落欄後下游可直接讀 archetype 分群，不必反推。（僅新增選填欄，dd-meta schema 契約其餘不動;下游 pipeline 前綴檢查零改動。）

### QC-44｜金融 archetype gate-set（v14.1 Stage 2;JPM 原型驗證;bank / insurer / broker 子型）

**WHY**:成長股 gate 對 balance-sheet 金融**整組失效**——JPM 實證:FCF = **−$148B**（成長銀行 OCF 結構性為負）、`debtToEquity` None（算不出;raw debt $1.3T 是存款/funding）、`enterpriseToEbitda` None、grossMargins 0、Capex 不在表上、ROA 1.27%「看似差」實為銀行常態。**唯一能用的右錨是 P/TBV**（P/B 2.58）+ ROE 16.5%，而 §11 主錨卻是 PE/PEG/EV-EBITDA。

當 §0 archetype = 金融，§5/§11/QC-31/§6 **改用下列 gate-set**（明寫在報告，QC-43 路由）:

**§5 門檻組（金融）**:
| 成長股 gate | 金融替代 | 達標基準 |
|:---|:---|:---|
| FCF Margin | **ROTCE 有形權益報酬** | > 15%（穿越循環） |
| ROIC | **ROE 且 > 權益成本（COE ~10%）** | ROE > 12-15% |
| 10Y ROIC 穩定 | **跨信用循環 ROTCE 穩定**（含 2008/2020 壓力年） | 壓力年仍正 / 不破底 |
| 毛利率定價 | **NIM 趨勢 + 效率比（cost/income）** | 效率比 < ~60% |
| Capex/Rev | **不適用** → operating leverage / 效率比改善 | — |
| EPS CAGR > 20% | **EPS + TBVPS 複合 + 股息（總回報）** | ~10-12% 即優（金融非 20% 機器） |
| PEG | **P/TBV vs ROTCE**:Warranted P/TBV =（ROTCE−g）/（COE−g） | 實際 P/TBV ≤ warranted |
| D/E < 0.7 | **不適用** → **CET1 ratio** | > 監管要求 + 緩衝（~11-13%） |
| 負債安全性 | **NPL/NCO 趨勢 + 撥備覆蓋 + CET1 緩衝** | 信用品質穩、撥備足 |

**§11 估值主錨（金融）**:**P/TBV 分位 + P/E**;用 Warranted P/TBV 判貴賤;**EV/EBITDA 拿掉**（銀行 None）。
**QC-31 signal（金融）**:X 觸發改 ROTCE 跨循環 < COE / CET1 跌破監管 / NPL·NCO 結構惡化 / 重大舞弊;移除 FCF·NI、EV-EBITDA、Capex 觸發。
**§6 跑道（金融）**:放款·存款·AUM 成長 + 費收業務（財管/IB）+ 市佔，非 TAM 滲透。

**子型（§0 secondary 細分）**:
- **bank**（JPM）:CET1 / NIM / 效率比 / NPL·NCO / ROTCE / P-TBV
- **insurer**（如 PGR / CB / Allianz `ALV.DE`;**注意:US 掛牌 `ALV` = Autoliv 汽車安全件＝循環工業，非保險，勿誤歸**）:**combined ratio < 100%** / float / Solvency II ratio / book value / ROE;**不看 NIM/CET1**
- **broker·交易所**（HOOD）:ARPU / AUC / take rate / 活躍戶;偏 fintech，常與「未獲利高成長」blend
- **支付網絡**（MA）:**不歸金融**——資產輕高複利，走 `品質複利`

**batch script 補搜**（金融 archetype 啟動時加一組強制 web/10-K，類 QC-19）:`[ticker] CET1 ratio NIM efficiency ratio ROTCE`（bank）/ `[ticker] combined ratio Solvency II book value`（insurer）。yfinance `.info` 給 ROE/ROA/P-B/股息，但 CET1/NIM/效率比/NPL/ROTCE/TBV **給不出**。

**反灌水**:金融 gate-set 不是新增冗章，是**把 §5/§11/QC-31 既有格子換成金融正確指標**;產出長度同等，只是尺對了。

### QC-45｜未獲利高成長 archetype gate-set（v14.1 Stage 3;MDB 原型驗證）

**WHY**:成長股 gate 對 GAAP 未獲利的高成長 SaaS 失效——MDB 實證:trailing EPS −$0.37 / Diluted EPS −1（負）→ §5 EPS-CAGR 負基期 undefined、PEG undefined、trailingPE None、EV/EBITDA −304、ROE/ROA 負;**但公司健康**:GM 72%、FCF +$500M（margin 20.3%）、營收成長 25.2% → Rule-of-40 = 45.5%。**最毒的是 QC-31 X 觸發 FCF/NI<0.5:NI 負 → FCF/NI = −7.0 < 0.5 → 機械把健康公司判迴避。**

當 §0 archetype = 未獲利高成長，§5/§11/QC-31/§6 **改用下列 gate-set**（QC-43 路由）:

**§5 門檻組（未獲利高成長）**:
| 成長股 gate | 替代 | 達標基準 |
|:---|:---|:---|
| EPS CAGR > 20% | **Rule-of-40**（營收成長% + FCF margin%） | ≥ 40 |
| PEG < 2 | **EV/S ÷ 營收成長**（growth-adjusted）或 EV/gross-profit | growth-adjusted 合理 |
| ROIC > 15%（GAAP 負無意義） | **NRR + 毛利率 + 增量 OI margin 改善軌跡** | NRR > 110% / GM > 65-70% |
| FCF Margin > 15% | **FCF margin + 轉正軌跡**（已正:看 margin 升;未正:現金跑道 + 明確轉正路徑） | FCF 升軌或跑道足 |
| 體質 FCF/NI | **NI 負時 FCF/NI 比無意義** → 改看 FCF margin 絕對值 + 淨現金 + 跑道 | FCF 正 或 跑道 > 12 個月 |

**§11 估值主錨（未獲利）**:**EV/S（+ EV/gross-profit）+ Rule-of-40-adjusted**;轉正後接 forward P/E;**trailing PE / PEG 拿掉**（負 EPS undefined）。
**QC-31 signal（未獲利）**:**不因 GAAP NI 負觸發 X**;X 改:NRR 跌破 100% / Rule-of-40 < 20 連 2 季 / 毛利結構崩 / 現金跑道 < 12 個月且無轉正路徑 / SBC 稀釋失控（股數 > 10%/yr 無營收槓桿）。
**§6 跑道（未獲利）**:NRR + 淨增客戶 + TAM 滲透 + SBC-adjusted 轉正時程（非 EPS 外推）。
**blend 提醒**:fintech broker（HOOD）常 = 金融 × 未獲利，兩套都跑、標背離。
**反灌水**:換尺不增章;Rule-of-40 / NRR / FCF margin 須 sourced 真數字。

### QC-46｜轉機 + 受監管公用事業 gate-set（v14.1 Stage 4;低密度，模型 prose 為主）

**WHY**:這兩類較少且模型 prose 已能處理八成，故給**輕量尺**不展開大表;重點是別硬套成長複利 gate。

**轉機/特殊情境**（深度價值 / 重整 / 分拆 / activist）:
- §5/§11 主錨 → **資產重估 / SOTP（分部加總）/ normalized earning power / P-TBV**，非成長外推;EPS-CAGR/PEG 不適用（盈餘受抑或為負）。
- §3.F Single Thing → **轉機觸發**（債務重組完成 / 出售虧損部門 / 新管理層 / catalyst 里程碑），非「moat 擴張」。
- §6/§7 → 「為何現在會轉」的 catalyst + 下行保護（資產底 / 清算價值），非 TAM/runway。
- QC-31 X → 流動性危機（跑道 < 12 個月 + 無再融資）/ 重整失敗 / 治理舞弊。

**受監管公用 / 穩定內需**（utility / regulated / staple）:
- §5/§11 主錨 → **DDM / 殖利率 + 股息成長 / regulated ROE（rate base × allowed ROE）/ P/B**;PEG/高成長門檻不適用（個位數成長為常態）。
- §6 成長 → **rate base 成長 + 費率案（rate case）+ 准許 ROE**，非 TAM 滲透。
- §7 護城河 → 監管特許 / 天然獨佔（single-axis，同 QC-44 §7 單軸 escape）。
- 產業態勢 → QC-39「態勢靜態」即可（已有）。
- QC-31 X → 准許 ROE 結構下調 / 費率案連敗 / 監管轉敵 / 過度槓桿（利率敏感）。

**反灌水**:此兩類**不強制長表**，但換尺與 catalyst/下行保護必須 sourced。模型若判標的明顯屬此兩類，§0 標明並用上述主錨，不硬跑成長 gate。

### QC-47｜archetype × QC 適用矩陣（v14.1 Stage 5 修剪;防博物館跨型誤觸）

**WHY**:QC-1~QC-46 多為**通用成長複利股**累積的 tripwire;當 §0 判為非複利 archetype，部分 **PE/EPS/FCF-based 通用 tripwire 會與 archetype gate-set 重複或誤觸**（如金融跑 §5 FCF gate、未獲利跑 QC-31 FCF/NI）。Stage 5 = 把這些**降為「該 archetype 下由 gate-set 取代、不重複機械套用」**（**不是刪除**——刪 load-bearing 規則風險高，留人工複審）。

**通用但永不修剪（全 archetype 強制）**:QC-8 不中斷 / QC-13 自我攻擊 / QC-17·18 先前報告 / QC-19 重大事件 / QC-32 dd-meta / QC-33 推導可追溯 / QC-38 深度地板 / QC-39 產業態勢 / QC-40 輸出潔淨 / QC-41 獨立 critic / QC-43 分類器。**深度·資料契約·流程紀律不分 archetype。**

**被 archetype gate-set 取代（非複利時不重複套用，改用對應 gate-set）**:
| 通用 tripwire | 循環/商品 | 金融 | 未獲利高成長 | 轉機/公用 |
|:---|:---|:---|:---|:---|
| §5 FCF/ROIC/Capex/D-E 門檻 | normalized（QC-39 閘B） | QC-44（ROTCE/CET1） | QC-45（Rule-of-40/NRR） | QC-46（資產/DDM） |
| §11 PE 分位·PEG·EV-EBITDA（QC-4/QC-14） | §11.5 normalized + P/B | QC-44 P/TBV | QC-45 EV/S | QC-46 SOTP/DDM |
| QC-21 R:R / QC-3 Bear / QC-36 5Y 目標 | Bear 用 normalized/P-B | P/TBV-based | EV/S-based | 資產底-based |
| QC-31 X 觸發（FCF/NI 等） | cycle-aware | QC-44 X | QC-45 X（NI 負不誤判） | QC-46 X |
| QC-26 margin / QC-27 Rev-OI / QC-28 絕對成長 | 適用（製造/競爭型） | **不適用**（無毛利→NIM/效率比） | 適用（看毛利/槓桿） | 視個案 |

**規則**:非複利 archetype 下，模型**用 gate-set 那一格、不再機械跑被取代的通用 tripwire**（消除「每行標失真」的 effort tax 與雙重觸發）;但若 gate-set 未涵蓋某風險，通用 tripwire 仍可作 checklist 提醒。**寫報告時不渲染本矩陣**（QC-40，內部鷹架）。

### QC-49｜裁決 hysteresis（v14.5，防方法論 churn 誤當資訊）

**WHY**:89 檔多報告 ticker 中 35 檔裁決翻面、14 天內相鄰複查 27% 翻面率、TSM 曾 1 天內觀望→進場——多數翻面不是世界變了，而是同一份資料被不同 run 用不同尺重讀（方法論 churn）。裁決若無「新事件觸發」門檻，會在噪音上反覆橫跳，下游 picks/PM 被迫追隨假訊號。

**規則**:同一 ticker **90 天內裁決翻面**（進場↔觀望↔迴避任一方向改變）時，§14 必須引用**前次報告 §14b 加減碼觸發或 §13 證偽指標的哪一條具體觸發器（編號 + 事件）已經發火**（如「R2 份額流失連 2 季觸發」「§3.F Single Thing 命中」「估值回落至 row 8b 重啟門檻 $__」）。**引用不出已發火的觸發器 → 承繼前次裁決**（維持不翻面），並在 §12.3 交叉矛盾記一句「本次傾向翻面但無 sourced 觸發器發火，依 QC-49 承繼前裁決」。

**邊界**:① 與 QC-17/18（只讀最近一份的假設 + 監測表，不讀舊裁決避免錨定）不衝突——QC-49 引用的是**上一份的觸發器清單**（§14b/§13，屬結構化 institutional memory 區塊），非上一份的裁決結論本身;② 跨 90 天的翻面不受此閘（時間夠久，世界確實可能變）;③ QC-49 只擋「無觸發器的翻面」，不擋「有觸發器發火的翻面」（後者正是系統該做的事）。與 QC-42 row 8b、QC-48 升級路徑並存:那些是「新增進場」不是「翻面」，各自的 critic gate 照跑。

---

# 買側標的研究框架 v14.5

---

## 【模式說明】

收到 ticker 後，直接開始深度版分析（單一 v14.5 DD 報告:基本面 Part I + 決策層 Part II + 擇時附錄 A）。無需詢問模式選擇。

> 🔍 **v13 深度版**：完整單檔報告，自動生成 HTML，輸出統一裁決（進場/觀望/迴避）。

---

## 【執行協議】

### Ticker 正規化

收到 ticker 後先做正規化：美股 `AVGO`→`AVGO`;台股 `2330.tw`/`2330`→ 檔名用 `2330TW`、yfinance 用 `2330.TW`;港股 `9988.hk`→ 檔名 `9988HK`。檔名格式 `DD_{TICKER}_{YYYYMMDD}.html`。

### 執行順序

收到 ticker 後，依以下順序執行，不得跳過或壓縮任何步驟：

0. **隨附文件前置處理（條件性）**：若用戶在給 ticker 的同時**提供外部文件**（PDF / 研究報告 / 法說逐字稿 / 產業報告等路徑），在跑搜尋之前先把這些文件**消化成「與本公司相關」的產業 read-through**（見【隨附文件處理協議】），其產出寫入報告 §4.5（緊接 §4 最新財報之後）。**只擷取會影響本公司業務前景 / 護城河 / §3 假設的內容**。無隨附文件 → §4.5 整段省略，不留佔位。
1. **先執行所有搜尋**（見【即時數據協議】），搜尋完成後在心中整理所有數據。**基本面研究只在此做一次**;Part II 決策層引用 Part I 結論，不另起獨立搜尋。
1.5. **Archetype 判定（QC-43）**:搜尋資料齊後、進章節前，判定 primary（+ secondary）+ 信心，路由 gate-set（金融 → QC-44 / 循環 → 投資軌 normalized + 附錄 B 對應子型錶[商品/capex/需求量] / EMS·ODM → 第 7 類 ROIC+周轉 gate-set + 需求量循環錶 / 未獲利 → Rule-of-40 / default 品質複利）。在 §1 開頭/頁首明寫「archetype + 信心 + 換了哪套 gate」。
1.6. **知識帳本先讀後裁（v14.5，Part II 動筆前必跑）**:寫 Part II 決策層（§12-§14）**動筆前**必跑 `python knowledge/q.py {TICKER}`（衍生物不存在時 q.py 自動 rebuild），載入本 ticker 歷次裁決、thesis 演進、已回填 outcome（結算 forward return）。與 CLAUDE.md「動部位前先跑 q.py」對稱。**硬規則**:若前次裁決為觀望/迴避且 to-date 報酬 > +30%（`q.py --calibration` 的錯過成本警報線），該證據**強制列入 §12.3（與上一份報告的交叉矛盾）**，且 §15 複審**不得只以「估值更貴了」維持觀望而不正面處理錯過成本**——必須明寫「上次觀望/迴避後漲 __%，本次維持/翻面的理由是 ___（正面回應錯過成本，非僅估值變貴）」。這是決策層的另一隻錨（帳本＝我過去實際下的判斷 vs QC-41 critic＝事前冷讀，互補）。
2. **⛔ 禁止在對話框輸出任何分析文字章節** —— 所有章節內容（頁首儀表板、§1 到 §15、附錄 A）全部直接寫入 HTML 檔案。
3. **草稿 → critic gate → Write（v14.5）**:Part I + Part II 草稿完成後、最終 Write 前，跑 QC-41（強制觸發範圍時）與 QC-48（row 8a 命中時）／row 8b 循環 critic（命中時）獨立 critic gate，把 🔴/🟡 findings 實際回填修正章節，再 **QC-40 機械 sweep**，最後才呼叫 Write 生成完整 HTML。
4. 搜尋與 critic gate 完成後唯一允許輸出的文字：「搜尋完成，正在生成 v14.5 DD 報告（含 critic gate）...」，然後直接呼叫 Write。

### 【隨附文件處理協議】

**觸發條件**：用戶在請求報告時，**同時附上一份或多份外部文件**（券商研究報告 / 法說逐字稿 / 產業白皮書 / 新聞 PDF / Excel 等）。

**處理步驟**：
1. **讀取**：PDF 若 Read 工具無法 render，改用 `python3 -c "from pypdf import PdfReader; ..."` 抽成純文字到 `/tmp/{ticker}_{src}.txt` 再讀。大型報告（>50 頁）優先 spawn 平行 sub-agent（general-purpose, sonnet）各讀一份並回傳「與本公司相關」的 digest，避免主線 context 爆掉。
2. **過濾**：只保留會改變本公司買/賣/加/減/持有年限判斷的內容 — ① 影響需求跑道的產業供需/TAM/週期位置;② 影響護城河的技術演進/製程路線/競爭格局位移;③ 對 §3 H1/H2/H3 假設加分或減分的數據點;④ 對本公司的 forecast/目標價/估值倍數。**捨棄**與本公司無關的他股深度、總經背景、純宏觀鋪陳。
3. **標註**：每個擷取點必須帶**來源機構 + 日期 + 信心度（high/med/low + 一句依據）**，並指出它影響哪一項（需求跑道 / 定價權 / 競爭護城河 / margin / 哪個 §3 假設）。多份文件對同一議題有分歧時，並列分歧並裁決。
4. **接線**：§4.5 read-through 是上游素材，必須在下游被實際引用 — §3（假設 sourced floor）、§6（成長跑道/分部建模）、§7（護城河/對手對照）、§9（產業格局/利潤池）。§4.5 自身只做「整理 + 標來源 + 指向」，深度推導留在下游章節。

**反灌水**：§4.5 不是把 PDF 複製貼上，而是**壓縮成決策相關的 read-through 表 + 分歧裁決**。冗長照搬 = 違規。

### ⛔ 強制靜默輸出規則（最高優先級）

**收到 ticker 後，對話框中嚴禁出現以下內容：** 任何章節文字、分析段落、表格、bullet point;任何「正在分析...」過渡描述。
**唯一正確流程：** ① 執行所有 web_search（不輸出文字）② 草稿完成後跑 critic gate（QC-41 / QC-48 / row 8b 循環 critic，命中時）並回填修正 + QC-40 機械 sweep ③ 輸出一行「搜尋完成，正在生成 v14.5 DD 報告（含 critic gate）...」④ 立即呼叫 Write 生成完整 HTML ⑤（Claude Code 本地環境,不需 present_files）。

### 搜尋集中原則

**所有網路搜尋必須在分析開始前一次性完成**，包含:股價/市值/52 週高低點;最新財報關鍵數字、Earnings Call 摘要;EPS 共識（FY+1/+2/+3）;FCF Margin 5 年/ROIC 10 年/毛利率 10 年（Macrotrends）;Forward P/E / EV/EBITDA / P/FCF 當前與 5 年區間;同業估值比較、分析師目標價;**§11.5 IRR 所需的 5Y 末 multiple band 與 consensus EPS（同一輪搜尋取得，不在 Part II 重搜）**。

搜尋完成後**禁止重新搜尋**;所有章節直接引用已取得數據。**Part II 決策層（§12-§15）一律引用 Part I 已搜得的數字，禁止為決策層另起搜尋**。若有數據缺口，額外補搜後立即進入 HTML 生成。

### HTML 輸出指令

搜尋完成後**立即使用 Write 工具生成完整 HTML 檔案**:包含所有章節完整分析;套用【HTML 輸出協議】;輸出至 `docs/dd/`;檔名 `DD_[標的代碼]_[YYYYMMDD].html`。

**QC-40 機械 sweep（Write 前強制自檢，v14.5）**:在呼叫 Write 之前，對 HTML 草稿正文（**dd-meta JSON `<script>` 區塊本身除外**）逐一 grep 下列 pattern，命中即改寫為讀者語言後才 Write:
```
QC-\d   硬接線   接線：   （必填   必填，餵   寫入 dd-meta   取下界   三處一致   Guardrail：   餵 §   餵 dd-meta
（DCA…移入）   （吸收 DCA   （…DCA…合一   校驗紀錄   判定規則接線
```
命中章節標題的 lineage 括注（「（DCA Phase B 移入）」等）→ 直接刪除括注只留章節名（QC-40 第 6 項）;命中正文的鷹架語言 → 改寫為分析結論。**sweep 未過不得 Write。** WHY:規則寫了卻零 enforcement（2026-07-03 NU ×49 處洩漏），機械 sweep 把「執行於心」變成「Write 前硬攔」。

### 防壓縮指令

**禁止以「節省篇幅」為由縮短 HTML 中任何章節內容。** 若單一 Write 呼叫無法容納全部內容，先輸出前半部章節，說明「HTML 第一部分已生成，繼續生成第二部分...」，等待用戶回覆「繼續」後以 Edit 工具追加剩餘章節。**寧可分段追加,絕不壓縮內容,也絕不改為文字輸出。**

---

## 【身份】

買側資深分析師 + 基金經理人決策層。融合彼得林區（一句話說清為什麼買）、查理蒙格（反過來想 + 多學科交叉驗證）、巴菲特（護城河永恆，只在好價格買好公司）。禁止摘要式敷衍,每節須有數據支撐與邏輯推演。
- **估值節的核心任務是「判斷當前股價隱含了什麼預期」**，而非「預測股票未來值多少」。
- **每當出現低估值訊號，必須觸發反向驗證**：這是被錯誤定價的機會，還是市場已提前定價惡化？
- **最終產出不是觀點，而是可執行的決策主線**：如果 A 發生我做 X，如果 B 發生我做 Y。Part II 是這個決策主線的居所。

---

## 【即時數據協議】（yfinance-first 批量採集）

**執行順序強制規則**：① 第一步（強制）執行「yfinance 批量採集腳本」一次抓齊所有可由 yfinance 提供的資料;② 第二步（僅補漏）針對 yfinance 無法提供的執行 web_search（降至 6-8 次）;③ 禁止對 yfinance 已涵蓋的項目重複 web_search。

### yfinance 涵蓋範圍（禁止用 web_search 重搜）

| 類別 | 項目 |
|:---|:---|
| 價格 | current, 52W H/L, 歷史週線 OHLC（6 年）、近 5 日日線 OHLC |
| 技術指標 | W52 / W104 / W250 SMA、W250 斜率（13 週）、Bollinger Band 2σ |
| 估值 | Forward PE, Trailing PE, EV/EBITDA, Beta, Market Cap |
| 預估 | FY+1 / FY+2 EPS 共識（+ 修正軌跡）、Revenue estimates |
| 財報 | 5 年 Income / Balance / Cashflow |
| 股權 | insider %, institutional %, top holders |
| 事件 | 下次財報日期 |
| 大盤 | ^GSPC / ^TWII 週線 W104 判定系統性風險 |

### web_search 必查（yfinance 無法提供）

| 類別 | 關鍵字範例 |
|:---|:---|
| 5Y Forward P/E 歷史分位 | `[ticker] forward PE history Macrotrends` / GuruFocus |
| 同業當前估值倍數 | `[competitor] forward PE EV/EBITDA 2026` |
| 重大事件（M&A、訴訟、臨床）| `[ticker] acquisition lawsuit 2026`（QC-19） |
| 競爭者新品 / 產業趨勢 | QC-12 產業掃描 |
| 分析師目標價 consensus | `[ticker] price target analyst consensus` |
| 5Y 平均 ROIC、毛利率 | `[ticker] ROIC history Macrotrends` |
| TradingView Beta | `[ticker] beta TradingView`（QC-25 雙源驗證）|
| **§11.5 IRR 用** | `[ticker] 5-year forward PE band` + `[ticker] EPS consensus FY+3 long-term growth`（IRR re-rate 與 EPS CAGR 基底，同輪搜得） |
| **QC-39 產業態勢變化（雙向，強制）** | 競爭惡化:`[ticker] market share gaining OR losing 2026` + `[ticker] largest customer second-source OR in-house` + `[competitor] design win at [ticker's customer]` + `[ticker] new entrant 2026`；結構 durability:`[industry] shortage OR oversupply structural OR cyclical 2026 2027` + `[industry] supply discipline new capacity timeline` + `[ticker product] demand durability AI structural`（完整規格見 QC-39） |

### yfinance 批量採集腳本（強制第一步）

```python
import yfinance as yf
import numpy as np

ticker = "TICKER_PLACEHOLDER"  # 替換為實際標的（台股用 "2330.TW" 格式）
t = yf.Ticker(ticker)
info = t.info

# 1. 基本資訊
print("=== 基本資訊 ===")
for k in ['currentPrice', 'regularMarketPrice', 'marketCap', 'fiftyTwoWeekHigh',
          'fiftyTwoWeekLow', 'forwardPE', 'trailingPE', 'enterpriseToEbitda',
          'priceToBook', 'bookValue',  # 循環/商品股 P/B 錨（QC-42 附錄 B；非循環股忽略即可）
          'beta', 'heldPercentInsiders', 'heldPercentInstitutions']:
    print(f"{k}: {info.get(k)}")

# 2. EPS / Revenue 共識
print("\n=== EPS Estimates ===")
print(t.earnings_estimate)  # 0q, +1q, 0y (FY+1), +1y (FY+2)
print("\n=== EPS Trend（7/30/60/90d 修正軌跡）===")
print(t.eps_trend)
print("\n=== Revenue Estimate ===")
print(t.revenue_estimate)

# 3. 財務三表（多年）— flagship 深度模組所需全欄一次抓齊（robust 逐行，缺行不報錯）
#    §8.E DuPont/CCC 需:Pretax/Tax(NOPAT)、AR/Inventory/AP(CCC)、Total Assets/Invested Capital(DuPont)
#    §10.D 資本配置需:D&A、Dividends Paid、Repurchase
def _dump(df, keys, title):
    print(f"\n=== {title} ===")
    if df is None or df.empty:
        print("N/A"); return
    for k in keys:
        try: print(k, "=", [round(float(v)/1e9,2) if v==v else None for v in df.loc[k].values])
        except Exception: pass  # 該公司無此行（如金融股無 Gross Profit）→ 跳過不報錯
_dump(t.income_stmt, ['Total Revenue','Gross Profit','Operating Income','Pretax Income',
                      'Tax Provision','Net Income','Diluted EPS'], "Income Statement (TWD/USD bn)")
_dump(t.balance_sheet, ['Cash And Cash Equivalents','Accounts Receivable','Receivables','Inventory',
                        'Accounts Payable','Total Debt','Stockholders Equity','Total Assets',
                        'Invested Capital','Working Capital'], "Balance Sheet")
_dump(t.cashflow, ['Operating Cash Flow','Capital Expenditure','Free Cash Flow',
                   'Depreciation And Amortization','Cash Dividends Paid',
                   'Repurchase Of Capital Stock'], "Cash Flow")

# 4. 週線 MA + Bollinger + 近 5 日 intraday
weekly = yf.download(ticker, period="6y", interval="1wk", auto_adjust=True, progress=False)
closes = weekly['Close'].values.flatten()
current = float(closes[-1])
w52 = float(np.mean(closes[-52:])) if len(closes) >= 52 else None
w104 = float(np.mean(closes[-104:])) if len(closes) >= 104 else None
w250 = float(np.mean(closes[-250:])) if len(closes) >= 250 else None
slope_pct = (w250 / float(np.mean(closes[-263:-13])) - 1) * 100 if len(closes) >= 263 else None
sma20 = float(np.mean(closes[-20:]))
std20 = float(np.std(closes[-20:], ddof=0))

print(f"\n=== MA / Bollinger ===")
print(f"現價: {current:.2f}")
print(f"W52: {w52:.2f}" if w52 else "W52: N/A（樣本不足）")
print(f"W104: {w104:.2f}" if w104 else "W104: N/A")
print(f"W250: {w250:.2f}" if w250 else "W250: N/A")
print(f"W250 斜率（13w）: {slope_pct:.2f}%" if slope_pct else "W250 斜率: N/A")
print(f"BB 上/中/下: {sma20+2*std20:.2f} / {sma20:.2f} / {sma20-2*std20:.2f}")

# 5. 近 5 交易日 OHLC（QC-24 intraday 訊號）
daily5 = yf.download(ticker, period="10d", interval="1d", auto_adjust=False, progress=False)
print(f"\n=== 近 5 交易日 OHLC ===")
print(daily5.tail(5)[['Open', 'High', 'Low', 'Close', 'Volume']])

# 6. 大盤豁免檢查（附錄 A 必需）
idx = "^TWII" if ticker.endswith(".TW") else "^GSPC"
idx_w = yf.download(idx, period="3y", interval="1wk", auto_adjust=True, progress=False)
idx_closes = idx_w['Close'].values.flatten()
idx_current = float(idx_closes[-1])
idx_w104 = float(np.mean(idx_closes[-104:]))
print(f"\n=== 大盤 {idx} ===")
print(f"現價 vs W104: {idx_current:.2f} vs {idx_w104:.2f} | 破線: {idx_current < idx_w104}")
```

**執行上述腳本後**，所有 §4、§5、§8、§10、§11、附錄 A 需要的原始數據均已取得。進入各章節撰寫時直接引用，不得針對同一項目再 web_search。

### 報告頂部必須標註

資料抓取時間 ｜ 最新股價 ｜ 最近財報季 ｜ yfinance 採集 + 補充 web_search 次數

---

## 【價值陷阱警戒協議】

**本框架內建四層防禦機制，在以下節點強制觸發反向驗證：**

| 觸發位置 | 觸發條件 | 反向驗證任務 |
|:---|:---|:---|
| §1 trap 定性（強制回答題） | 選擇進場且估值偏低 / 衰退信號 ≥ 1 個 | 必須在 §1 4 問表回答「這是價值陷阱嗎？」並給最終定性 🟢/🟡/🔴 |
| §6 長期成長性 | 衰退信號偵測表有任一項亮燈 | 強制輸出「價值陷阱風險評級」（0/1-2/3-4/5+ 級） |
| §7 護城河 | 衰退信號 ≥ 1 個亮燈 | §7 必須正面回應對應的護城河侵蝕信號 |
| §11 估值 + 附錄 A 估值燈 | Fwd PE 或 PEG 出現偏低訊號 | 走 §1 trap 定性回路 |

**四種最常見的價值陷阱模式**（分析全程保持警覺）：護城河侵蝕型（定價下滑、市佔流失）/ 盈餘品質型（EPS 靠回購撐、FCF 與淨利背離）/ 產業結構衰退型（低 P/E 因 TAM 萎縮）/ 隱性資本密集型（維持競爭力的 capex 被系統性低估）。

---

# Part I — 基本面深度（骨幹，≥60% 篇幅）

---

## §2｜序章：第一性原理 × 逆向思考

### 存在意義

剝離財務表象，這家公司解決了哪個長期且不可逆的人類痛點？若它明天消失，世界會出現什麼不可替代的混亂？論述須具體，不接受「提升效率」這類空泛答案。

### 逆向推演（Munger Inversion）

若要讓這筆投資在 3 年內虧損 50% 以上，最可能的路徑是什麼？逐一分析（每維度最多 1 個歷史對標案例，不逐維鋪陳）：
- **地緣政治曝險**：生產地 / 供應鏈集中度與相關政治風險
- **技術替代風險**：誰或什麼技術可以讓它變得多餘，時間軸為何
- **管理層失職**：壓成 1-2 行，並標注「自我毀滅決策路徑詳見 §10 資本配置計分卡」
- **價值陷阱路徑**：若這是一個價值陷阱，最可能的惡化劇本是哪一種？（護城河侵蝕 / 盈餘品質 / 產業衰退 / 隱性資本密集，四選一，說明理由;架構性替代分級見 QC-23 ⛔）

> 護城河如何累積而成，見 §7.D 護城河變遷時間軸（不在 §2 重複此表）。

**字數預算**：§2 全節 ≤ 2.5K。逆向推演不做「三維各 1-2 條 + 每條歷史對標」的鋪陳式擴張。

---

## §3｜投資論點錨定

**本節的唯一目的：在分析開始前，把「這筆投資在賭什麼」顯性化。** 沒有清晰的論點錨定，後續章節的分析只是資訊搬運，無法轉化為可執行的決策。本節在搜尋完成、資料齊備後、進各章節前先寫（對齊【執行順序】——基本面研究只在搜尋階段做一次），作為整份報告的骨架;報告完成後回頭檢查每個章節的結論是否強化或挑戰了這裡寫下的假設。

### A｜持有期與時間軸宣告

| 項目 | 填寫 |
|:---|:---|
| **預設持有期** | __ 個月 / __ 年 |
| **主要驅動這個時間軸的理由** | （催化劑時間表 / 估值修復週期 / 成長兌現節點） |
| **這個持有期決定了哪些變數是訊號、哪些是噪音** | 短期財報波動是噪音 / 護城河趨勢是訊號（依持有期調整） |

**時間軸一旦設定，後續所有章節的「重要性」判斷必須與之一致。** 持有期 < 6 個月:財報 newsflow 權重提高,估值分位次之。持有期 > 2 年:護城河趨勢與 ROIC 方向為主,短期 EPS 波動降噪。

### B｜三個核心假設 + 三層時間軸（sourced floor + 漂移觸發條件）

這筆投資的論點成立，依賴以下三個假設同時為真。**每個假設在 2Y / 5Y / 10Y 三個時間軸上各有可驗證指標**，避免長期 thesis 被短期戰術視角綁架。

| # | 核心假設 | 2Y 驗證點 | 5Y 驗證點 | 10Y 驗證點 | 具體數字門檻 | 信息來源 | 漂移觸發條件 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| H1 | （最關鍵的結構性假設） | （短期戰術觸發點） | （中期 thesis 結構驗證） | （長期複利可維持性） | （可量化具體門檻） | （公司法說 / sell-side / 產業報告） | 連 2 季 TTM 偏離 ≥ X% → 削弱（對齊 QC-34/35） |
| H2 | （成長兌現的操作性假設） | | | | | | |
| H3 | （估值修復的市場假設） | | | | | | |

**sourced floor 強制規則**（每個假設必須含三要素）：① 具體數字門檻（不接受「YoY 增加」「持續成長」，需明確閾值，例「HBM 市佔 ≥ 50%」）;② 信息來源（公司法說 / sell-side / 第三方產業研究，標名稱，非訓練數據推測）;③ 漂移觸發條件（對齊 QC-34/35;2Y 假設連 2 季,5Y 假設連 4 季）。

**強制規則**：三層時間軸內容必須從 §4 / §6.A Runway / §6.E 壓力測試 / §7 護城河趨勢 / §9 TAM 等 raw 章節抓取重組，**禁止**從上一份報告的 §3.B 結論延用（避免棘輪偏誤 / 青蛙煮水）;每個格子具體可驗證,不接受廢話。

### B'｜12 個月前報告對照（thesis review 機制）

**邏輯**：找 `docs/dd/DD_{ticker}_*.html` 中日期最接近 today − 365d 的那份，抓出當時 H1/H2/H3 → 對照本次兌現/削弱/反轉判定 → 補「YoY 漂移」+「vs Inception 累積漂移」兩欄。

**情境 1：進場未滿一年（找不到 12 個月前報告）** — 顯示 placeholder（不留空）:「狀態：進場未滿一年（最早 Inception = YYYY-MM-DD，距今 N 天）。本欄位將於 YYYY-MM-DD 起首次有資料對照。在此之前，僅以 §3.B 戰術假設視角追蹤。」

**情境 2：有 12 個月前報告**

| 假設 | 12 個月前判定 | 本次判定 | YoY 漂移 | vs Inception 累積漂移 | 結論 |
|:---|:---|:---|:---|:---|:---|
| H1 | （🟢 兌現 / 🟡 削弱 / 🔴 反轉 + 關鍵數字） | | | | （持續 / 警戒 / 砍倉） |
| H2 | | | | | |
| H3 | | | | | |

**強制規則**：QC-34 季節性過濾（TTM 或年度）;QC-35 漂移分級;漂移判定僅標示狀態，不直接觸發動作（動作回到 §3.E 雙條件）;長期假設禁止從本次報告 §1-§2 結論延用（B' 像獨立 review 從 raw 數據重推）。
**動作建議（早期信號 + PM 風險權重輸入）**：全綠→持有;一個削弱→警戒;兩個削弱或一個反轉→減倉 1/3（回 §3.E 確認）;兩個以上反轉→全砍 + 更新 thesis。
**Inception 標記**：本份若是該 ticker 第一份 v12.2+ 報告 → 頁首儀表板標記「Inception DD: <檔名>(<日期>)」，後續每份引用此 Inception 作累積漂移對照基準。

### C｜三個最可能推翻論點的風險（時間尺度分層 ⚡🔥🐢）

| # | 風險 | 對應假設 | 時間尺度標記 | 監測指標 | 警戒閾值 |
|:---|:---|:---|:---|:---|:---|
| R1 | | H__ | ⚡ 短期（1-2 季可觸發） | | |
| R2 | | H__ | 🔥 中期（4-6 季）| | |
| R3 | | H__ | 🐢 長期（2+ 年慢變數）| | |

| 標記 | 時間尺度 | 應對速度 | 觸發大動作條件 |
|---|---|---|---|
| ⚡ 短期 | 1-2 季可觸發 | 季度監控 | 連 2 季觸發即減倉 |
| 🔥 中期 | 4-6 季 | 半年回顧 | 連 4 季觸發才大動作 |
| 🐢 長期 | 2+ 年慢變數 | 跨年度監控 | 需 ≥ 50% 機率才砍倉 |

**禁止**:用同一閾值套所有時間軸的風險;R1-R3 寫成 binary discrete event（那是 §3.F 的職責）。

### D｜邊際貢獻判斷框架

每當新事件出現,用以下框架判斷其對論點的影響,而非直覺反應:① 時間軸匹配？（持有期內有影響嗎）② 假設關聯？（影響 H1/H2/H3 哪個）③ 邊際方向？（＋強化/0 無關/－削弱）④ 閾值判斷？（達到重新評估閾值嗎）。**如果一個新消息既不影響任何假設、也不改變估值分位，它對這筆投資就是噪音，不需要行動。**

### E｜可執行決策主線預設

在分析完成前先預設框架，分析完成後填入具體條件（引用 §11.4 / §14）：

| 情境 | 觸發條件 | 對應行動 |
|:---|:---|:---|
| **進場** | 估值條件：__；基本面確認：__ | 建倉 __%（角色:__），首次進場 |
| **加碼** | 假設驗證進度：H1 + H2 均確認 | 加碼至 __%，目標倉位 |
| **減碼** | R__ 風險信號出現，或估值突破 __x | 減至 __%，重新評估 |
| **撤退** | 核心假設 H__ 被推翻，或陷阱信號 __ 確認 | 清倉，記錄推翻理由 |

（v13：此框架的填寫結果直接餵 §14b 加減碼條件表;一處推導，兩處對齊。）

### F｜Single Thing（v13 統一：DD §5.F 與 DCA §5 合一，唯一 binary trigger）

**1 個明確、可觀測、binary discrete event**：若這件事發生，立刻改變整個判斷。不是「ROIC 連 3 年下降」這種慢變數，而是「Mariana 占比超過 50%」/「Apple 切換 modem 供應商」/「Intel 18A 良率突破 80% 並取得 Apple 訂單」/「FDA Phase III readout 結果」這類具體 trigger。

> **v13 統一規則**：舊 DD §5.F 與舊 DCA §5「The Single Thing That Could Change My Mind」**合併成這一個 §3.F**;不再有兩個各自寫不相關 trigger 的 single thing。§3.F 是全報告唯一的「single thing」居所;§13b pre-mortem 必須 cross-check 它（故事倒推的關鍵觸發是否就是 §3.F），並依校驗結果**實際修正** §3.F（補 secondary trigger 或重寫 primary）。

| 項目 | 內容 |
|:---|:---|
| **Single Thing 描述** | （一句話描述這個 binary event;明確、單點、可驗證） |
| **為什麼這個事件是致命的** | （它直接撞哪個假設 / 護城河 / 利潤池） |
| **如果發生** | （立刻做什麼：清倉 / 加倉 / 重新評估 thesis） |
| **如何監測** | （資料來源、頻率、目前離發生有多遠：具體日期 / 財報 / 里程碑） |
| **機率估計** | （未來 12-24 個月發生的主觀機率） |

**禁止**:模糊表述（「市場情緒轉變」）;不可觀測事件;process risk（那是 §3.C R1-R3）。

**三者職責矩陣（強制對齊，禁止混淆）**：
| 角色 | 定義 | 時間軸 | 類型 |
|:---|:---|:---|:---|
| **§1 trap 定性** | thesis 整體是否「價值陷阱」的靜態裁決（🟢/🟡/🔴） | 現在（static） | 狀態判斷 |
| **§3.C R1-R3** | thesis 持有期間的過程性風險 + 監測 + 閾值 | 未來持續（⚡🔥🐢） | 過程風險 |
| **§3.F Single Thing** | 單一具體 binary trigger event（discrete、可觀測、改變判斷） | 未來某 specific moment | 觸發事件 |

**寫的時候反向 check**：R1-R3 中若有 binary event 性質 → 移到 §3.F;§3.F 若有 process risk 性質 → 移到 R1-R3;§1 trap 不該重複 §3.F;三者各司其職、不重疊。

---

## §4｜即時財報情報

資料來源：最新 10-Q / 8-K / Earnings Call transcript

### ① 最新一季財報關鍵數字

| 指標 | 本季實際 | 市場預期 | Beat/Miss | YoY 成長 |
|:---|:---|:---|:---|:---|
| Revenue | | | | |
| EPS（Non-GAAP） | | | | |
| FCF | | | | |
| Gross Margin | | | | |
| Operating Margin | | | | |

**財報對 §3 假設的邊際貢獻**（每份財報後必填）：

| 假設 | 本季財報的邊際方向 | 關鍵佐證 |
|:---|:---|:---|
| H1 | ＋ / 0 / － | |
| H2 | ＋ / 0 / － | |
| H3 | ＋ / 0 / － | |

（QC-27 Rev/OI divergence 在此計算:核心業務 Revenue YoY − OI YoY > 3% → margin 壓縮警示,列入 §6.E。）

### ② Earnings Call 語氣解析（持有期 > 2 年時語氣屬 §3.A 噪音層，只留 2 行）

- **Guidance vs 共識**：下季 / 全年 guidance 與市場共識的差距（**數字化**，上調/下調/維持 + 幅度）。
- **被迴避的問題**：一個分析師追問但未正面回答的議題（潛在風險點）。

### ③ 產業 Imply 萃取（1 行綜合推論）

- **產業隱含信號**：本次 call 對產業供需與競爭強度方向的最關鍵 imply 是 ___，**餵入 §9 產業格局**（利潤池 / 議價權判定的時點佐證）。

---

## §4.5｜隨附研究文獻：產業 read-through（條件性）

**僅當用戶在請求報告時同時附上外部文件（券商報告 / 法說逐字稿 / 產業白皮書 / 新聞 PDF / Excel）才產出本節；無附件 → 整段省略，不留佔位。** 處理規則見【執行協議 → 隨附文件處理協議】。

**本節定位**：把隨附文件消化成「與本公司相關」的產業 read-through — 最重要的產業重點、技術演進、供需循環、競爭格局位移，**逐點標來源 + 信心度 + 影響項**，作為 §3/§6/§7/§9 的上游素材。**不是逐份摘要**，只擷取會改變買/賣/加/減/持有年限判斷的內容。

### ① 文件清單

| 文件 | 機構 / 作者 | 日期 | 對本公司的相關度 |
|:---|:---|:---|:---|
| （檔名簡稱） | | | 高 / 中 / 低 + 一句話 |

### ② 產業 read-through（決策相關擷取）

| # | 擷取點（含具體數字） | 影響項 | 來源 | 信心度 | 對應 §3 假設 / 下游章節 |
|:--:|:---|:---|:---|:---|:---|
| 1 | | 需求跑道 / 定價權 / 競爭護城河 / margin / 週期位置 | 機構 + 頁碼 | high/med/low + 依據 | H_／§6.A／§7／§9 |

（最重要的 8-15 點；技術演進與供需循環優先）

### ③ 跨文件分歧裁決（必填，若有分歧）

| 議題 | 文件 A 觀點 | 文件 B 觀點 | 本報告裁決 + 理由 |
|:---|:---|:---|:---|

### ④ 對本公司 thesis 的淨影響（≤ 80 字）

綜合隨附文件，對 §3 H1/H2/H3 與護城河的淨方向是 ＋強化 / 0 中性 / －削弱，以及最關鍵的單一 read-through。**禁止**在此下與下游章節無支撐的新結論。

---

## §5｜核心門檻檢核（Munger）

### 【EPS CAGR 強制搜尋協議】

執行本節前，必須完成以下步驟取得 EPS 共識預估，禁止使用訓練資料估算：

**步驟零'（最高優先）：Excel buy-side consensus（每月人工 refresh）**

DD universe（≈141 檔含 US/ADR/TW）已有 Koyfin/Excel 每月匯出的 normalized consensus（FY+1/+2/+3 + growth + 2Y CAGR），ADR/TW 自動換成 USD 統一單位。這是 buy-side standard、比 yfinance 少 GAAP/non-GAAP 歧義、比 web_search 穩定。

寫 §11 估值前先跑：
```bash
python3 scripts/get_eps_for_ticker.py {TICKER}      # 文字格式，貼進報告 §11 附註
python3 scripts/get_eps_for_ticker.py {TICKER} --json   # JSON，程式化解析
```
判讀規則：
- exit 0 + 印出 FY1/FY2/FY3：用這份當 §11 估值的 anchor，**毋需再做步驟零的 yfinance fetch 或步驟一的 web_search**。記得在 §11 註明「EPS 來源：Excel snapshot YYYY-MM-DD」供 audit。**§11.5/11.6 IRR 的 EPS CAGR 基底也用這份**（一份 snapshot 全報告一致）。
- exit 1（NOT in Excel）：ticker 未覆蓋，fall back 到「步驟零（yfinance）」。
- exit 2（Excel 缺檔）：通知用戶 `cp ~/Downloads/DD_universe_EPS_estimates_*.xlsx data/eps-estimates/`，然後 fall back yfinance。

FY+3 取得後仍照「§6 邏輯推導」做業務邏輯描述（不可只貼數字），但**不再需要機械外推**。

**步驟零（v9.0，步驟零' 失敗時 fallback）：yfinance 程式化抓取**
```python
import yfinance as yf
t = yf.Ticker("TICKER")  # 台股用 "2383.TW" 格式
ee = t.earnings_estimate  # 欄位：avg, low, high, numberOfAnalysts, growth；列：0q, +1q, 0y(FY+1), +1y(FY+2)
```
記錄:FY+1E（0y 列）avg/n/YoY growth;FY+2E（+1y 列）;季度趨勢（0q,+1q）交叉驗證;EPS Trend（t.eps_trend）觀察 7/30/60/90d 修正方向。**yfinance 限制**:僅 FY+1/FY+2,無 FY+3。

**FY+3 推導方式（v9.0 邏輯分析法，禁止機械外推）—— 僅在步驟零' Excel 未覆蓋時適用**：FY+3 EPS 必須基於 §6 長期成長性分析推導,不得用「FY+2 growth × 0.7」機械公式。① 從 §6.A Runway 判斷 3 年後成長階段 ② 從 §6.B 判斷定價 vs 量貢獻是否遞減 ③ 從 §6.D（ROIC × 再投資率）計算內生成長率作上限參考 ④ 綜合給出 FY+3 YoY growth 具體數值與一句話邏輯依據 ⑤ FY+3E = FY+2E × (1 + FY+3 growth)，標注「§6 邏輯推導」。禁止「遞減外推」「線性外推」等無邏輯描述。（v12.4 補:Excel 步驟零' 直接給 FY+3 consensus 時，仍要寫 §6 邏輯描述作 sanity check——若 consensus 與業務邏輯明顯矛盾，要在 §11 標明分歧並提 PM 修正值。）

**若 yfinance 失敗**,退回步驟一的 web_search 流程。

**步驟一（備援）：web_search** — 僅在 yfinance 失敗時:「[標的代碼] EPS analyst consensus estimate [FY+1] [FY+2] [FY+3]」+「[標的代碼] earnings per share forecast [FY+1] [FY+2] [FY+3] Zacks」。
**步驟二（備援）：來源優先** — ① Zacks（區分 GAAP/Non-GAAP，記 n）② StockAnalysis.com Forecast ③ Yahoo Finance EPS Trend ④ 均無 FY+3 → 用 FY+2 替代並標「FY+2 外推」。
**步驟三：記錄數字** — 基期 EPS（最新完整財年實際，GAAP）/ FY+1E / FY+2E / FY+3E（共識中位數或遞減外推，標來源 + n）。
**步驟四：計算** — GAAP CAGR = (FY+3E GAAP ÷ 基期 GAAP) ^ (1/3) − 1;Non-GAAP CAGR 同理。
**步驟五：口徑差距說明** — 說明 GAAP 與 Non-GAAP 差距來源（SBC / 重組 / 攤銷）。台股不區分,標「不適用（台股法定口徑）」。

### 【Munger 護城河維度強制搜尋協議】

執行門檻檢核表前，須補充搜尋（與 EPS CAGR 並行）：
- **FCF Margin 歷史**（5 年年度）:「[標的代碼] free cash flow margin history Macrotrends」,記錄每年 + 5 年均值 + 最低谷年份。
- **ROIC 穩定性**（10 年年度）:「[標的代碼] ROIC history 10 year annual Macrotrends」,Macrotrends→TIKR→Wisesheets,記錄每年 + 達標年數。
- **毛利率趨勢**（10 年年度）:「[標的代碼] gross margin history 10 year Macrotrends」,記錄每年 + 改善年份數/總年數。
- **Capex / Revenue**（近 3 年）:最新 10-K 或 §4 財報。
- **D/E ratio 與現金 / Revenue**:最新 10-Q/10-K。

**若 10 年數據取得困難**：以 5 年替代，並在表格備注「5 年樣本」。

**archetype 適配（QC-43）**:本表為 `品質複利成長` 預設尺。若 §0 判定 **金融** → **QC-44**（ROTCE / CET1 / NIM / 效率比 / P-TBV，不套 FCF/ROIC/Capex/D/E）;**循環/商品** → §11.5 normalized（QC-39 閘 B）;**未獲利高成長** → **QC-45**（Rule-of-40 / NRR / EV-S / FCF 轉正路徑，不套 EPS-CAGR/PEG）;**轉機·受監管公用** → **QC-46**（資產/SOTP/normalized · DDM/殖利率/regulated ROE）。被取代的通用 tripwire 不重複機械套（QC-47）。換尺須在報告明寫（QC-43）。

### 門檻檢核表

| 項目 | 標準 | 符合? | 關鍵數據與趨勢 |
|:---|:---|:---|:---|
| FCF Margin（當前） | > 15% | | 當前值：__%，近 3 年趨勢：↑ / → / ↓ |
| 正規化 FCF Margin【Munger維度】 | 5 年均值 > 15%；單年最低谷 > 10% | | 5 年各年值 + 均值 + 最低谷 + 判斷 |
| ROIC（當前） | > 15%，且高於 WACC | | 當前 ROIC：__%，WACC：__%，超額：__%p |
| ROIC 穩定性【Munger維度】 | 過去 10 年中 ≥ 70% 的年份 ROIC > 15% | | __/10 年達標,最低谷年份,趨勢 |
| 毛利率定價能力【Munger維度】 | 過去 10 年中 ≥ 70% 的年份毛利率持續改善 | | 改善年份 __/10,當前/10 年前,趨勢 |
| 資本密集度【Munger維度】 | Capex / Revenue < 5%（優）/ < 10%（尚可） | | 當前/近 3 年均值,評級 |
| EPS CAGR（未來 3 年） | > 20%（高成長）**或** 12-20% 且 runway ≥10Y 高 durability（穩健長複利路徑;**此路徑須在右欄明標「非高成長股，靠長 runway 複利達標」**） | | 基期/FY+1E/FY+2E/FY+3E + GAAP/Non-GAAP CAGR + 口徑差距 + 資料來源 +（走 durable 路徑時）引用 §6.A runway + 標「非高成長股」 |
| PEG（Non-GAAP） | < 2 | | 引用 §11.2 計算結果 |
| 負債安全性【Munger維度】 | D/E < 0.7；現金 / Revenue 10∼50% | | D/E,現金/Revenue,評級 |
| 現金覆蓋總負債 | 是 / 否 | | |
| 護城河強度 | > 8 分，趨勢擴大 | | |

**Munger 三維護城河快速評級**（ROIC 穩定性 + 毛利率定價能力 + 資本密集度）：🟢 三項全達標 / 🟡 兩項達標（§7 說明哪維偏弱）/ 🔴 一項或以下（§7 需強力反駁或重新評分）。
表格後加一行：**最大財務弱點**：＿＿;Munger 三維評級：🟢/🟡/🔴 → 傳遞至 §7 護城河分析作定量起點。

**v13 注意**：低估值四問 + 便宜理由檢驗五問已移除（重複 §1 trap 定性）。價值陷阱判斷統一在 §1「這是價值陷阱嗎？」處理。

---

## §6｜長期成長性評估

### 0｜成長品質 7 問儀表板（放 §6 最前，明確化不藏段落）

**強制**：§6 開頭先給一張「成長品質 7 問」綜合儀表板——把基本面最核心的 7 個拷問**明確列出 + 一句裁決 + 關鍵數字 + 指向詳見章節**。這是基本面判斷的單頁可掃讀摘要。

| # | 成長品質拷問 | 裁決（≤2 行） | 關鍵數字 | 詳見 |
|:--:|:---|:---|:---|:---|
| 1 | 成長是**結構性**還是**週期反彈**？ | 結構為主 / 週期為主 / 混合 + 理由 | 催化、能見度年數、backlog | §6.A / §9 durability |
| 2 | 成長需**多少資本投入**？ | 輕/中/重資產 + 一句 | Capex/Rev __%、再投資率 __% | §6.D |
| 3 | **增量 ROIC** 是否 > 資金成本？ | 是/否 + M&A 是否扭曲 | ROIIC __% vs WACC __% | §6.D |
| 4 | 成長變**現金流**還是被**下輪擴張吃掉**？ | FCF / 被 M&A 吃 / 混合 | FCF margin __%、FCF 去向 | §10.E |
| 5 | **競爭者**會否被高成長吸引進來？ | 已進/將進/壁壘高 + 誰 | 新進者市佔/客戶 | §7 賽局/§7.F |
| 6 | 股價**反映多少期待**？ | 過熱/合理/便宜 + 一句 | Fwd PE 分位 __%、PEG __ | §11.1/附錄 A D |
| 7 | 成長率**下修**估值撐得住嗎？ | 撐/不撐 + 跌幅 | 熄火情境 -__% | §6.E/§11.5 |

**規則**：① 每題裁決必須在「詳見」章節有完整推導（§6.0 只負責明確化 + cross-ref）;② 7 題要有「最弱的一題」標紅;③ 與 §1 trap 定性 + §14 裁決一致。

**本節核心目的**：判斷未來 3 年 EPS CAGR 之後，成長能持續多久、靠什麼撐住、會不會反噬財務品質。這是決定估值倍數「應給幾倍」的最關鍵依據,所有結論將直接傳遞至 §11.5 與 §1。

### A｜成長跑道（Runway）估算

| 維度 | 數據 | 推論 |
|:---|:---|:---|
| 當前 TAM（億美元） | | 來源：搜尋，標注年份 |
| 估計可達 TAM（億美元） | | 說明擴張假設 |
| 當前市佔 / 滲透率 | | |
| 若維持現有成長率，幾年達 30% 滲透率 | | 即自然放緩的時間點 |
| **成長可持續年數估計（Runway）** | **__ 年** | |

**Runway 解讀基準**（直接影響 §11.5 / 附錄 A 合理倍數溢價幅度）:Runway ≥ 10 年 高確信長期複利,支撐高溢價;5∼9 年 中等可見度,估值對應折扣;< 5 年 短期成長股,倍數保守,必須有「下一條成長曲線」論述。

### A''｜Y5 後跑道 runway_post_y5（v13 吸收 DCA A2，必填，餵 dd-meta）

**目的**：Runway（§6.A）量的是「現在起算的成長年數」;runway_post_y5 量的是「**Y5 之後 5-10 年是否還有跑道**」——長抱者真正在賭的尾巴。**v13 把舊 DCA Phase A2 的此項移入此處就地產出，dd-meta `runway_post_y5` 由此填**;§11.5/§14c 直接引用，不另搜。

| 項目 | 內容 |
|:---|:---|
| S 曲線位置 | 早期 / 中期 / 晚期（一句依據） |
| Y5 末 TAM 滲透率預估 | __%（推導:當前滲透率 + 5 年成長軌跡） |
| 是否有下一條 S 曲線銜接 | 有（哪條 / 何時啟動）/ 無 |
| **runway_post_y5（必填）** | **🟢 寬 / 🟡 中 / 🔴 窄** |

**判準（v14.3 量化邊界;判定必須引用滲透率推導或 sourced 來源，禁憑感覺）**：

| 燈號 | 邊界 |
|:---|:---|
| 🟢 寬 | Y5 末 TAM 滲透率 ≤ 35%（≥ ~3x 剩餘空間）**或** 有 sourced 下一條 S 曲線（具體名字 + 預估啟動時點 + 來源;「AI 選擇權」一句話不算） |
| 🟡 中 | 滲透率 35-70%，且無已 sourced 的第二曲線 |
| 🔴 窄 | 滲透率 > 70%（量價齊飽和）或成長段已見頂且無第二曲線 |

範例:「🟢 寬:Y5 末 TAM 滲透率 ~22%，仍有 4-5x 空間;下一條 S 曲線（XX 應用）2027 啟動」、「🔴 窄:Y5 末 滲透率 >70%，量價齊飽和，無第二曲線」。
**硬接線（v14.3 起雙向）**:**🔴 直接觸發 §14c 持有年限 ≤ 3Y 警示 + §14 決策矩陣 Soft Veto（≥ 觀望）**;**🟢 為 §14 row 8a 爆發候選路徑的必要條件之一**（非充分，還需 AR ≥ 4 等，見 §14），且觸發 §11.5「10Y 二段延伸」必填。寫入 dd-meta `runway_post_y5`。

### B｜成長品質判斷（具體% + 3Y 趨勢 + 併購清單）

**① 成長來源：有機 vs 無機**

| 類型 | 定義 | 此標的占比估計 | 佐證 |
|:---|:---|:---|:---|
| 有機成長 | 定價提升、現有客戶深化、新市場自然滲透 | __% | |
| 無機成長 | 併購貢獻的營收與 EPS | __% | |

若無機成長占比 > 30%，**必須**列出近 5 年主要併購清單（年份/被收購方/金額/整合結果/達預期?），並計算剔除併購後有機成長率。

**② 成長驅動結構：定價 vs 量（必須含具體% + 3Y 趨勢）**

| 類型 | 定義 | 此標的判斷（**必須含具體%**） | 過去 3 年趨勢 |
|:---|:---|:---|:---|
| 定價驅動（Price） | 提價 / 組合升級 / ARPU | ASP YoY：__%（FY23/24/25） | 擴大/穩定/縮減 |
| 量驅動（Volume） | 用戶數 / 交易量 / 出貨量 | 出貨量 YoY：__%（FY23/24/25） | 擴大/穩定/縮減 |

**禁止**僅寫「定價驅動為主」無量化描述。若難拆分,說明具體原因。

**③ 營業槓桿結構：增量利潤率 3Y**

| 列 | 內容 |
|:---|:---|
| 增量 OI margin | ΔOI ÷ ΔRev，FY−2/FY−1/FY0 逐年 + 3Y 合計 |
| 增量 vs 存量對照 | 增量 margin __% vs 當前 OI margin __% → 結構性擴張/中性/燒錢買成長 |
| 前瞻結論（必填一行） | 「在 Rev +__% base case 下，此增量結構隱含合併 OI margin 每年 ±__bp」 |

**接線**:前瞻結論 bp 強制餵入 (a) §6.D ROIIC 對賬列;(b) §6.E 壓力測試 margin 假設。
**判定規則**:增量 margin 連 2 年 < 存量 margin → 成長在稀釋獲利結構，§3.B 對應假設觸發「削弱」+ §6.E 衰退信號表自動補一盞燈。

### C｜成長護城河連動評估

| 類型 | 定義 | 具體表現 |
|:---|:---|:---|
| **強化型**（最佳） | 成長帶來更強網路效應/規模/數據壁壘 | |
| **中性型** | 成長與護城河各自獨立 | |
| **消耗型**（警示） | 為維持成長犧牲定價 / 擴張至低 ROIC / 大幅增 SBC | |

判斷此標的屬於哪一類,給出具體財務或營運佐證,不可僅憑印象。

### D｜ROIC 與 FCF 的長期可維持性

| 指標 | 當前值 | 3 年前 | 趨勢 | 標準門檻 | 是否符合 |
|:---|:---|:---|:---|:---|:---|
| ROIC | | | ↑/→/↓ | 產業頂尖,且 > WACC | |
| ROIC − WACC（超額報酬） | | | ↑/→/↓ | 持續正值,且擴大 | |
| FCF Margin | | | ↑/→/↓ | > 15% | |
| FCF / Net Income 轉換率 | | | ↑/→/↓ | > 85%（輕資本） | |
| Reinvestment Rate（再投資率） | | | ↑/→/↓ | 成長期合理偏高,需有對應 ROIC | |

**ROIIC 與內生成長天花板（強制計算）** — 四列必算,附完整推導數字：

| 列 | 計算 | 規則 |
|:---|:---|:---|
| ROIIC（3Y） | (NOPAT_t − NOPAT_t−3) ÷ (投入資本_t − 投入資本_t−3) | 附兩端數字;ΔIC ≤ 0 或受大型 M&A 扭曲 → 標「剔除 M&A 重算」或「不適用 + 原因」 |
| 再投資率 | (Capex − D&A + ΔWC + 收購淨額) ÷ NOPAT，3Y 均 | 與上表 Reinvestment Rate 一致 |
| 內生成長天花板 | ROIIC × 再投資率 | |
| 共識對賬 | §5 共識 EPS CAGR − 內生天花板 = 缺口 __pp | 缺口強制歸因:margin 擴張（§6.B③）/ 淨回購（§8）/ 無法歸因 |

**判定規則**:缺口可閉合 → 標「共識不依賴 re-rate」;缺口無法歸因 → §3.B 對應假設加註「依賴 re-rate / 無基本面引擎支撐」警示,且附錄 A I 長期持有信心上限「中」。**內生天花板數字寫入 dd-meta optional 欄位 `endo_growth_ceiling`,供 §11.6 IRR sanity check 引用**。

### E｜成長熄火情境壓力測試

若長期成長提前終止，估值將承受多大壓力？此數字在 §1 下行風險與 §11.5 Bear 中引用。

| 情境假設 | 對應成長特徵 | 合理 Forward P/E 壓縮至 | 潛在估值跌幅 |
|:---|:---|:---|:---|
| 3 年後成長率降至 15% | 成長放緩但仍高於市場 | __x | __% |
| 3 年後成長率降至 10% | 回歸市場平均成長 | __x | __% |
| 3 年後成長率降至 5% | 成熟期低成長 | __x | __% |

目標 P/E 引用 §11.5 / 附錄 A 的合理 P/E 基準（由 §7 護城河分數 + §6 成長評級決定）,與主報告數字保持一致。

### ⚠️ 衰退信號偵測表

**凡出現任一亮燈項目，需在本節末尾輸出「價值陷阱風險評級」，不得省略。**

| 信號類型 | 偵測指標 | 數據 | 亮燈？ |
|:---|:---|:---|:---|
| 護城河侵蝕 | Gross Margin 連續 2 季 YoY 下滑 | | 🔴/⬜ |
| 護城河侵蝕 | 核心市場市佔率縮減（過去 12 個月） | | 🔴/⬜ |
| 護城河侵蝕 | 主力產品定價能力測試:最近一次提價後銷量是否下滑（引用 §7 定價事件帳） | | 🔴/⬜ |
| 盈餘品質 | EPS CAGR 顯著高於 Revenue CAGR（差距 > 5%p） | | 🔴/⬜ |
| 盈餘品質 | FCF / Net Income 轉換率 < 0.75（連續 2 年） | | 🔴/⬜ |
| 盈餘品質 | SBC / Revenue > 5% 且逐年上升 | | 🔴/⬜ |
| 產業結構衰退 | TAM 本身在萎縮或被替代技術壓縮 | | 🔴/⬜ |
| 產業結構衰退 | 整個產業估值倍數過去 3 年系統性下移 | | 🔴/⬜ |
| 隱性資本密集 | Maintenance Capex 占 FCF 比例 > 60%（引用 §8 maint capex 估算） | | 🔴/⬜ |
| 隱性資本密集 | 若停止投資新產能,收入是否在 3 年內下滑？ | | 🔴/⬜ |

**價值陷阱風險評級**（根據亮燈數量，必選一個）：0 個 🟢 低風險（正常流程）/ 1∼2 個 🟡 中度警戒（§7 必須正面回應）/ 3∼4 個 🔴 高度警戒（§1 trap 4 問標 🔴 + §7 回應侵蝕）/ 5+ 個 ⛔ 極高風險（§1 預設迴避，需明確反駁才改進場）。

**長期成長性綜合評級**（必選一個，傳遞至 §11.5 / 附錄 A 合理 P/E 基準與 §1）：🟢 高確信（Runway ≥ 10 年、有機+定價驅動為主、護城河強化型、ROIC 擴大、衰退信號 0）/ 🟡 中等可見度（Runway 5∼9 年，1∼2 個衰退信號）/ 🔴 存疑（Runway < 5 年、無機占比高、消耗型或 ROIC 下滑、衰退信號 ≥ 3）。

### H｜客戶結構深度（3661 Mariana 教訓）

**① 客戶集中度**

| 指標 | 數值 | 年份 | 資料來源 |
|:---|:---|:---|:---|
| Top 1 客戶占營收% | | | 10-K / 法說會 |
| Top 5 客戶合計% | | | |
| Top 10 客戶合計% | | | |
| 最大客戶過去 3 年% 趨勢 | FY23/24/25 | | |

**② 主要客戶議價權結構**（最大/第 2/第 3 大客戶 × 占比 × 議價權類型 Dual-track/Second-source/Sole-source × 說明）。

**③ 客戶生命週期定位**:Grow with 客戶（良性相互依賴）/ 客戶可能 in-house（Apple silicon/Google TPU 路徑）/ 客戶可能 second-source（最常見風險）。

**④ 留存經濟（按商業模式選一指標，3 年時間序列）**:SaaS→NRR;半導體→最大平台 design win 留存 + attach rate;消費→回購率/VIC 占比;平台→cohort 留存/take rate。禁止跨模式硬套;禁止 LTV/CAC 通用要求。
**判定規則**:留存指標 3 年向下 **且** ②表存在 dual-track 信號 → 客戶結構風險自動升 🔴。

**客戶結構風險評估**（必選一個）：🟢 分散 + Sole/Grow-with 主導 / 🟡 集中但 Grow-with 邏輯強 / 🔴 高集中 + Dual-track 信號（前 1-2 客戶占比 > 40% 且有 second-source 扶植動作）。

### F | AI 取代風險評級

評估 AI 浪潮對該標的核心業務的影響,獨立於護城河和長期成長性,作為品質分維度之一。
- 🟢 **AI 受益或免疫**:核心業務因 AI 需求擴張（半導體/資料中心/AI 軟體平台/雲端）或商業模式與 AI 無關。範例:NVDA、TSMC、AVGO、MSFT。
- 🟡 **中等不確定**:部分業務受 AI 衝擊但護城河可能轉化。範例:GOOGL、META、Adobe、Salesforce。
- 🔴 **高風險被取代**:核心業務直接被 AI 取代且護城河薄弱。範例:Stitch Fix、Chegg、Upwork。
**必填證據**:具體業務占比 vs AI 侵蝕區域;公司 AI 策略;過去 2 年 AI 相關營收變化。**禁止留空或「待評估」**。評級分數對應（供品質分）:🟢 = 9 / 🟡 = 6 / 🔴 = 3。

### I｜分部前瞻建模（深度模組）

**目的**：把 §6.A-E 的「成長品質判斷」深化到「成長的可驗證來源拆解」——回答「FY+1→FY+3 的 EPS 成長，具體是哪個業務段、靠量還是價貢獻的」。

每個 >10% 營收業務段一張前瞻 build 表：

| 業務段 | FY0 營收 | 驅動式（量×價 或 客戶×ASP） | FY+1E | FY+2E | FY+3E | 段 OM 軌跡 | 對合併 EPS 成長的貢獻 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| （段 A） | $__ | 例:出貨量 +__% × ASP +__% | $__ | $__ | $__ | __%→__% | 貢獻 FY+1→+3 EPS 成長的 ~__% |

**規則**:驅動式必須拆「量 vs 價」或「客戶數 × 單客戶營收」,不接受「YoY +X%」黑盒;各段貢獻加總應對得上 §5 整體 EPS CAGR（差異 > 5pp 須解釋）;至少標明「哪一段是 EPS 成長的主引擎」+「若該段 miss，EPS CAGR 降至多少」;sourced（段營收/成長來自財報分部 + 法說 guidance，標來源）。

---

## §7｜護城河分析（報告核心）

**評分強制二維拆解（default）**:execution moat（能力護城河）+ pricing power moat（議價權護城河），各打 1-10 分，最終分取兩者均值或加權合併。**Single-axis escape rule**:SaaS / 銀行 / 保險 / 寡占型公用事業這類 execution 與 pricing 緊密耦合難拆的業務，允許「綜合分 + narrative 說明哪維主導」單軸寫法，明確標 **"single-axis"**，但必須寫**為什麼這業務不適合二維**。**QC-23 威脅三級分類強制使用**（🟡/🔴/⛔，每級列具體事件 + 機率）。**護城河來源 sourced evidence 強化**:網路效應需具體規模閾值;無形資產需列 IP/專利清單;競爭鴻溝需給「為什麼資本充足對手仍跨不過」的具體 mechanism。

**若 §6 衰退信號偵測表有亮燈，本節必須正面回應對應的護城河侵蝕信號，說明是暫時現象還是結構性惡化。**

### 評分：二維拆解（default）或 single-axis（escape rule）

**判斷路徑**:是否適合二維？**是（default）**:execution moat 與 pricing power moat 可獨立評分（製造業、設備、半導體設計）→ 強制二維;**否（single-axis escape）**:SaaS 訂閱型 / 銀行 / 保險 / 寡占公用事業 → 允許 single-axis + narrative。

| 維度 | 評分（1-10） | 關鍵佐證 |
|:---|:---:|:---|
| **Execution Moat**（製造工藝/研發深度/供應鏈整合/規模效率） | __ / 10 | |
| **Pricing Power Moat**（轉換成本/無形資產/網路效應/客戶依賴度） | __ / 10 | |
| **合併分**（均值或加權合併，說明邏輯） | __ / 10 | |
| **等級** | S/A/B/C/拒絕 | （10=S, 9=A, 7-8=B, 5-6=C, <5=拒絕） |

**dd-meta optional 欄位**:`moat_execution` + `moat_pricing_power`（兩 sub-scores，validator 不強制）。

### 護城河數字驗收（Moat-to-Numbers）

護城河分數必須在數字上留下痕跡。最直接的單一量測:**ROIC 對最強同業的利差（spread）及其 5 年方向**。

| 指標 | 本標的 | 最強直接同業 | Spread | 5 年前 Spread | 方向 |
|:---|:---|:---|:---|:---|:---|
| ROIC（TTM） | __% | __%（公司名） | __pp | __pp | 擴大/持平/收窄 |
| 毛利率 | __% | __% | __pp | __pp | |
| 已實現價格溢價（若適用） | ASP / 定價 vs 同業 __% | — | | | 引用 §7 定價事件帳 |

同業 = §11.4 同 tier peer group 中最強者（與 QC-5 一致）。
**判定規則（硬 gate，直接動品質等級）**:護城河合併分 ≥ 8 的必要條件 = ROIC spread 為正且（擴大或持平）;Spread 連 2 年收窄而分數仍打 ≥ 8 → 必須寫具體反駁，反駁不成立 → **合併分強制 −1，並同步更新附錄 A B 品質等級**。本 gate 與 QC-26、QC-28 並列為「護城河三道數字閘」，§7 結尾以一行匯總三閘狀態。

### 護城河來源（強化 sourced evidence）

逐一檢驗,真實存在的深度論述,表象的直接否定;**強制要求具體 sourced evidence**:
- **網路效應**:規模閾值（多少用戶/節點才觸發 flywheel）
- **無形資產**:具體 IP 清單 / 專利數量 / 牌照護城河年期
- **轉換成本**:換掉此供應商需多少 CapEx / 多長時間 / 哪些流程重建
- **規模優勢**:規模前 vs 後 unit cost 差距;對手需多大規模才能追上

### 競爭鴻溝（具體 mechanism）

為什麼**資本充足的對手仍無法跨越**？必須給出具體 mechanism:①時間壁壘（需 X 年追上）②資本壁壘（需 $X 億研發/設備）③認證壁壘（客戶認證/監管 X 年）三維度至少說明 2 個。

### 市佔競爭表（對手經濟體質 + 賽局結構判定）

| 競爭對手 | 目前市佔 | 3 年趨勢 | 核心威脅 | 誰在吃誰（需 sourced 數字） | OI margin | FCF（TTM） | 戰爭承受力 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| | | | | | __% | $__B | 高/中/低（依據:margin 緩衝 + 現金 + 母體補貼意願） |

**禁止**「彼此競爭中」無數字描述。每個「誰在吃誰」必須引用具體市佔變化或客戶流失/獲取案例。
**賽局結構判定（≤ 80 字，必填）**:理性寡占 / 紀律鬆動 / 破壞性競爭。必附 sourced 證據（上一輪下行週期的實際價格行為:守價/跟跌/主動降價）。
**判定規則（硬接線）**:存在「結構性成本更低 + FCF 足以攻擊 + 承受力高」的對手 → pricing power moat 維度分數上限 7;賽局 = 破壞性競爭 → QC-23 對應威脅機率下限 30% 且 §6.E 壓測含「ASP 戰」;賽局 = 理性寡占 + sourced 守價證據 → 可作 pricing power 高分行為佐證。

### 定價事件帳（pricing power 實證，去重）

pricing power 維度下建單一「定價事件帳」,作為 §6.B②、§9 議價權下游段、§6.E 衰退信號「最近一次提價」、§7 護城河數字驗收「已實現價格溢價」列的**唯一資料源**（其餘各處改一行引用,禁止重抓）:

| 日期 | 提價幅度 | 量與留存反應 | 其後 2 季 GM 反應 |
|:---|:---|:---|:---|
| | | | |

近 3 年 ≤ 3 個事件。

### D｜護城河變遷時間軸（護城河如何累積而成）

3 年以上關鍵事件時間軸:護城河如何一步步累積（製程代次、design win 累積、客戶綁定深化、IP 護城河擴大）。§2 序章引用此處,不重複此表。

### E｜對手 Capex / R&D 對照（看投入強度）

top 2-3 對手的 Capex 與 R&D 絕對額 + 強度（R&D/Rev），看誰在加碼投入追趕。與 §7.F 對手 P&L（看承受力）互補。

### 護城河趨勢（v13：權威趨勢線 ↑→↓，吸收 DCA A1 的 12M sourced 證據，餵 dd-meta）

> **v13 升權威**:護城河趨勢是全報告與下游聚合器的**權威趨勢線**（對齊 memory `dca_trend_authoritative`）。舊 DCA Phase A1 才搜的「moat_trend ↑/→/↓ + 12 個月內變化具體證據」**移入此處就地產出**;dd-meta `moat_trend` 由此填。

**雙線標 + 權威 moat_trend**:execution dimension 趨勢 + pricing power dimension 趨勢各自獨立評估（兩者可能不同方向），並彙整出**單一權威 moat_trend ↑/→/↓** 寫入 dd-meta:

| 維度 | 趨勢 | 3 年關鍵事件 |
|:---|:---|:---|
| **Execution Moat 趨勢** | 擴大 / 穩定 / 縮減 | |
| **Pricing Power Moat 趨勢** | 擴大 / 穩定 / 縮減 | |
| **權威 moat_trend（必填，寫 dd-meta）** | **↑ widening / → holding / ↓ narrowing** | **必附 ≥ 1 個 12 個月內變化的 sourced data point**（例:「2024 vs 2025 同業 ROIC gap 從 8pp 擴大到 12pp（公司 4Q25 法說 vs 同業均值）」） |

**規則**:**禁止寫「持平」當逃避** — 任何體系都在動，必須選邊 ↑/→/↓;dd-meta `moat_trend` 必須是**單一 Unicode 箭頭**;權威 moat_trend 由雙維趨勢彙整（兩維皆擴大→↑;一擴一縮→以對 thesis 更關鍵的維度為準並說明;皆縮減→↓）。
**moat_trend 必須前瞻、不得只看後照鏡**:箭頭要反映「未來 2-3 年份額/護城河往哪走」,須引用 QC-39 雙向掃描搜到的**前瞻份額軌跡**,不是只看過去 3 年。市佔競爭表的「3 年趨勢」欄改為「回看 3 年 + 前瞻 2-3 年(sourced)」。
**🔴 QC-39 閘 A（防 AVGO 型過度樂觀，硬性）**:**若標的 / 領先玩家在其最大客戶或 program 的份額正在下滑（sourced），moat_trend 不得標 ↑**（最多 →，視程度可 ↓）。例外:有 sourced 反證說明「為何此份額分散不損長期護城河」（如總 TAM 擴張使絕對額仍增 + 新客戶補位），且須在本節明列反證並通過 QC-13 自我攻擊,否則一律降。範例:Broadcom 在 Google TPU 份額 95%→65%（2026→28，MediaTek 切入）→ 即使絕對額仍增,moat_trend 至少 →,不得 ↑,且 §3.C 補一條份額流失風險。
**硬接線（餵 §14 決策矩陣）**:**moat_trend = ↓ 且 moat 等級 ≤ B → §14 決策矩陣 Hard Veto（迴避）**。

列出 24 個月內最可能瓦解護城河的技術或市場變化，按 QC-23 三級分類排序。**新進入者打進 top-3 客戶/program 一律列入（QC-39 競爭惡化方向的回填）**。

### F｜對手財務深度對照（深度模組）

**目的**：Moat-to-Numbers 只給 ROIC spread 單點;本模組給 top 2-3 直接對手的**完整財務體質對照**，讓「威脅可信度」有全面經濟基礎（與 §7 賽局判定接線）。

| 指標 | 本標的 | 對手 A（名） | 對手 B（名） | 對手 C（名/新進） |
|:---|:---|:---|:---|:---|
| 營收成長（YoY） | | | | |
| Gross Margin | | | | |
| Operating Margin | | | | |
| R&D 強度（R&D/Rev） | | | | |
| FCF Margin | | | | |
| 淨現金/淨債 | | | | |

**每家對手一段「策略與經濟體質」敘述（≥ 60 字）**:該對手用什麼策略攻擊（低價/全棧/補貼）、其 margin 與 FCF 能否支撐這場仗、母體是否願補貼 → 接 §7 賽局判定。**新進入者（如切入客製 ASIC 的新玩家）必須單獨成段**，評估切入點、客戶、對本標的 top 客戶的威脅。

---

## §8｜財務品質監測

### 三年趨勢表（強制加同業對比欄）

每項必須加「同業中位數」欄，不只給絕對值。同業選用與 §11.4 peer group 一致的公司。

| 指標 | 2023 | 2024 | 2025(E) | 同業中位數（引用 §11.4 peer group） | 相對評估 |
|:---|:---|:---|:---|:---|:---|
| FCF Margin | | | | | 優/平/劣 |
| EBITDA Margin | | | | | |
| ROIC − WACC | | | | | |
| SBC / Revenue | | | | | |
| ROE | | | | | |

### 獲利品質警訊

四項完整檢驗:淨利 vs OCF 連動性（盈餘操縱）/ AR 成長 vs 營收成長（應收膨脹）/ 存貨成長 vs 營收成長（庫存積壓）/ FCF 轉換率趨勢（資本密集度變化）。

### 回購品質評估（剔除回購後 EPS CAGR 必算）

| 指標 | 數據 | 判斷 |
|:---|:---|:---|
| 過去 3 年回購總金額 vs FCF 總額 | | 回購/FCF = __%（> 80% 警示） |
| **若剔除回購，EPS CAGR 降為多少？（必算）** | | **原 CAGR __% → 剔除後 __%（差距 > 5%p 警示）** |
| 回購均價 vs 當前股價 | | 高於/低於（高於 = 資本配置不當） |
| Revenue CAGR（同期）| | 若 EPS CAGR 遠高於 Revenue CAGR，說明差距來源 |

### FCF lumpiness 評估

部分業務（ASIC 客製 / EPC / 訂單型）天然 lumpy，單年 FCF 低不等於 red flag。

| 指標 | 數值 |
|:---|:---|
| 過去 5 年 FCF 各年值 | FY20∼FY24 |
| 5Y 滾動均 FCF | $__ |
| 最低谷年份 + FCF | FY__: $__（占 5Y 均的 __%） |
| Maintenance capex 估算（方法強制標明:D&A 錨定法 或 管理層揭露） | $__ → **Owner earnings = OCF − maint. capex = $__** |
| Lumpiness 性質判斷 | 業務天然 lumpy / 一次性資本支出 / 結構性惡化 |
| 結論 | 🟢 屬正常週期 / 🟡 需關注低谷頻率 / 🔴 FCF 穩定性存疑 |

### E｜長期趨勢 + DuPont + 營運資金（深度模組）

**目的**:把三年表深化到長期結構 + 拆解 ROIC 驅動來源 + 看現金品質的營運面。

**① 5-10 年關鍵指標趨勢**（看結構性方向，非單點）：

| 指標 | FY-9~FY-5 區間 | FY-4 | FY-3 | FY-2 | FY-1 | FY0 | 結構判讀 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| Gross Margin | | | | | | | 升/平/降 |
| Operating Margin | | | | | | | |
| ROIC | | | | | | | |
| FCF Margin | | | | | | | |

**② ROIC DuPont 拆解**:ROIC = NOPAT margin × 投入資本周轉率 → 判斷 ROIC 由「獲利力」還是「資本效率」驅動，及哪個在變化（逐年表，每格附數字）。
**③ 營運資金趨勢**:DSO / DIO / DPO 3 年趨勢 + cash conversion cycle（CCC = DSO+DIO−DPO，逐年實算，AR/Inv/AP ÷ 日均，非概估）→ 看現金被營運資金佔用方向（惡化 = 盈餘品質警訊）。
**④ 債務到期結構**:近 3 年到期金額 + 加權平均利率 + 再融資風險（高利率環境下到期牆）。

---

## §9｜產業格局

**展開三維度**:① 議價權三段獨立（各 ≥ 60 字）② 營收三維（業務段 × 地區 × 客戶集中度）③ 單位經濟逐業務段。

**市場量化**:TAM 規模（現在 / 5Y / 10Y）、CAGR、當前滲透率、供需狀態（過剩 / 緊缺）。

**供需 durability 裁決（v14.0 QC-39 閘 B，循環/商品/供需驅動標的必填一句）**:當前供需失衡（緊缺或過剩）是**結構性還是週期性**？能撐多久？必引用 QC-39 searched 證據（供給紀律 / 新產能時點 / 需求結構黏性 / 供給是否可逆），裁決:**結構性持久（normalized 該上修）/ 週期性將反轉（normalized 守歷史中樞）/ 供給可逆性高（緊缺脆弱，下行更猛）**。此裁決**直接餵 §6.E normalized 假設與 §11.5 bear 機率**（閘 B），禁止只用「產業在缺/在過剩」的當下狀態下結論而不判 durability。範例:NAND 2026 缺貨部分來自 Samsung/SK Hynix 把晶圓挪去 HBM（供給可逆）+ YMTC 擴產 → durability 較弱 → bear 不因「在缺」而調低;HBM 缺貨由 AI 結構需求 + 3:1 晶圓轉換驅動 → durability 較強。

### 利潤池地圖（Profit Pool Map）+ 利潤池位置/流向（v13 吸收 DCA A2）

回答中長期持有人最關鍵的產業問題:這條價值鏈的經濟利潤現在堆在哪一段、正往哪一段遷移、本標的站的位置是受益還是受害。

| 價值鏈環節 | 代表公司 | 環節營收池 $B | 環節 OI 池 $B（或 OI margin 代理） | 5 年前 OI 池占比 → 當前占比 | 遷移方向 |
|:---|:---|:---|:---|:---|:---|
| （上游環節 A） | | | | __% → __% | ↑/→/↓ |
| （本標的所在環節） | **[標的]** | | | __% → __% | ↑/→/↓ |
| （下游環節 C） | | | | __% → __% | ↑/→/↓ |

- 數據來源:sell-side 產業報告 / 各環節龍頭財報加總代理，標注來源 + 年份;無法取得完整池 → 用「各環節龍頭 OI margin × 環節營收」代理，明標「代理估算」。
- **利潤池位置/流向結論（必填，v13 吸收 DCA A2）**:本標的所在環節利潤池占比方向 **↑ 流入 / → 持平 / ↓ 流出** + 1 個 sourced 證據 + 對 §6.A Runway 的含義。**↓ 流出 = 量增利不增警示，餵入 §14c 持有年限**（取代舊 DCA 的 A2 利潤池獨立搜尋 — 此處就地產出，§14 直接引用不另搜）。
**判定規則（硬接線）**:本標的環節 OI 池占比 5 年**淨流出 ≥ 5pp** → §6.A Runway 評級自動降一檔,且 **QC-39 產業態勢三軸裁決不得標「結構性轉好」**（利潤池外流是結構惡化訊號，須反映在雙向裁決的 durability 判定）;淨流入 → 可作附錄 A D 估值燈盲點 1 救援佐證。

### 議價權（三段獨立，各 ≥ 60 字）

**①對上游供應商**:供應商集中度?替代難度（High/Medium/Low）?近 3 年議價案例（成功提價/被迫接受漲價/成功壓低採購成本）?若集中度高（top 3 > 70%），列主要供應商名稱 + 占採購比例 + 切換成本。
**②對下游客戶**:客戶集中度（引用 §6.H）如何影響議價地位?合約結構（長期合約幾年/訂單型/spot）?近 3 年客戶流失 case?定價能力直接證據（提價後留存率/帶漲價條款比例）。
**③地緣曝險**:核心生產地（哪些國家/占多少）?供應鏈最高集中點?政策風險具體路徑（關稅/出口管制/地緣衝突影響哪環節）?分散化措施?

### 營收組成（三維展開）

**① 按業務段**:業務段 × 占比% × YoY% × OI Margin × 3Y 占比趨勢。
**② 按地區**:地區 × 占比% × YoY% × 監管/地緣備註。
**③ 按客戶集中度**:Top 1 占比% / Top 5 合計% / 失去最大客戶影響（占 Revenue __%，估計 __% 跌幅）。

### 單位經濟（逐業務段；加 OI margin + 資本密集度 + mix-shift 算術）

**不接受**「公司整體 ARPU $__」這類無法判斷業務健康度的數字。每個核心業務段必須有各自 unit economics:

| 業務段 | 核心 Unit 指標 | 數值 | 趨勢 | 段 OI margin | 資本密集度 proxy | 結構性洞察 |
|:---|:---|:---|:---|:---|:---|:---|
| （業務 A） | ARPU/GP per customer/ASP/margin per design win | | ↑/→/↓ | __%（從 §9 ① 表直引） | __（段資產/段營收 或 capex 歸屬;10-K 無分段資產 → 標「不揭露，以 __ 替代推估」） | （一句話） |

**mix-shift 算術（必填一行）**:以各段當前成長率外推 3 年，合併 OI margin 結構性 **±__bp/yr**。
**接線**:mix-shift bp 與 §6.B③ 增量利潤率互為驗證,差距 > 100bp 必須解釋（capex 前置/一次性），無法解釋 → 兩處重算。

### F｜逐段 TAM/SAM + 價值鏈深度（深度模組）

**目的**:「市場量化」只給全公司一個 TAM;本模組給每個業務段各自的 TAM/SAM/滲透 + 在價值鏈位置。

| 業務段 | 段 TAM（現/5Y） | 段 SAM（可服務） | 當前滲透率 | 段 CAGR | 在 value chain 位置 + 議價/被替代風險 |
|:---|:---|:---|:---|:---|:---|
| （段 A） | $__/$__ | $__ | __% | __% | 例:上游壟斷節點，被替代風險低 |

**規則**:每段一句「這段的成長天花板與被替代路徑」;與利潤池地圖接線——TAM 大但利潤池流出的段要標明。

---

## §10｜公司治理與資本配置

完整輸出（QC-6 四項保留）。

**股東結構**:創辦人持股比例、機構集中度、近期內部人大額交易（QC-6 項目 1 + 4）。

**資本配置軌跡（M&A track record 強化）**:管理層對再投資/併購/回購的實際決策，說法與行動是否一致？

過去 5 年 M&A track record（必填）:年份 / 被收購方 / 金額（$M）/ 整合結果（成功整合/達成 synergy/未達預期）/ 減損紀錄。若過去 5 年無重大 M&A（金額 > 市值 5% 或 > $100M），標明「無重大 M&A，有機成長為主」。

**管理層薪酬結構**（QC-6 項目 3）:固定薪 / 績效獎金 / 股權激勵比例與機制。

**SBC 真實稀釋（必算「剔除 SBC 後 EPS 是多少」）**:

| 指標 | 數據 |
|:---|:---|
| SBC / Revenue（近 3 年） | FY23/24/25 |
| GAAP EPS | $__ |
| Non-GAAP EPS | $__ |
| **差距（SBC + 其他 non-GAAP 調整）** | **$__（__%）** |
| **剔除 SBC 後 EPS CAGR（必算）** | **原 GAAP CAGR __% vs Non-GAAP CAGR __%（差距 > 5%p 警示）** |

**資本配置計分卡（接線到持有年限）**:

| 項目 | 計算 | 過 / 不過門檻 |
|:---|:---|:---|
| M&A 已實現 ROIIC | 被購方第 3 年 NOPAT 貢獻 ÷ 收購總價 | ≥ WACC 過;5 年無重大 M&A → 此項 N/A 不計 |
| 回購買入收益率 | 回購均價的 earnings yield | ≥（10Y 殖利率 + 2%）過 |
| SBC 淨稀釋率 | 年化淨稀釋 | ≤ 1.5%/yr 過 |

**資本配置等級**:適用項中 ≥ 2/3 過 = A;1 項 = B;0 項 = C。
**接線（等級不進品質分 — 保持護城河單一決定設計）**:C 級 → 附錄 A I 長期持有信心強制上限「中」，且 §6.D 內生天花板引用時標「打 8 折」。**等級寫入 dd-meta optional 欄位 `capalloc_grade`，供 §14 決策矩陣 Soft Veto 引用**。

### D｜10 年資本配置 track record（深度模組）

**目的**:把資本配置計分卡擴成全歷史敘事——管理層 10 年怎麼花錢、回報如何。
**① M&A 全史 ROIIC**:年份 / 標的 / 金額 / 收購當時邏輯 / 第 3 年 NOPAT 貢獻·ROIIC / 整合評價。
**② 回購/股息 10 年軌跡**:年度回購金額 + 均價 vs 當年股價（高/低位回購）+ 股息成長率 + 總股東回報率（回購+股息）/ FCF。
**③ 內部人 + 薪酬**:近 12 個月內部人交易 + 高管薪酬結構 + 薪酬與 ROIC/TSR 是否掛鉤。
**規則**:本模組是「管理層是否值得信任把錢交給他複利」的判斷依據，與計分卡等級接線——10 年敘事支撐或推翻計分卡等級。

### E｜FCF 去向 + M&A 飛輪（回答「成長變現金流還是被下輪擴張吃掉」）

**目的**:回答 §6.0 第 4 問。一家公司賺的成長，最後是變成股東口袋的現金，還是被「下一輪擴張」（capex / 營運資金 / 併購）吃掉？對 M&A 飛輪型公司尤其關鍵。
**① FCF 去向拆解（近 3-5 年）**:股息 / 回購 / 去債 / 再投資（capex+R&D）/ 下一筆 M&A 各佔 FCF % + 增量 ROIC·報酬 + 判斷。
**② M&A 飛輪判定（連續併購型公司）**:成長有多少來自「FCF → 去債 → 下一筆併購」飛輪 vs 有機?飛輪歷史增量 ROIC（引 §10.D）是否持續 > WACC?關鍵風險:FCF 是否被「越來越貴的下一筆併購」吃掉（出價紀律惡化）。
**③ 一句結論（必填）**:「這檔的成長最終 ___（變股東現金 / 被 M&A 飛輪回收再投 / 被 capex 吃掉），增量 ROIC ___（> / ≈ / < WACC），飛輪 __（健康複利 / 需警戒出價紀律 / 已現規模幻覺）。」接 §6.0 第 4 問裁決。

---

## §11｜估值與報酬

> **v13 融合**:本章把舊 DD §13（估值診斷:歷史分位/PEG/同業）與舊 DCA §4（Asymmetry Analysis:Bull/Base/Bear IRR + 三分量拆解 + Pattern match）合成一章。**11.5/11.6/11.7 的 IRR 用的 5Y multiple band 與 consensus EPS 是 §5 步驟零'/yfinance 與 §9 同一輪搜尋取得的數字，不另起搜尋。** ev5y_pct / irr_base_pct 由此填 dd-meta。

### 11.1｜歷史估值分位（5 年框架）

| 估值指標 | 當前值 | 5 年低點 | 5 年中位 | 5 年高點 | 當前分位 |
|:---|:---|:---|:---|:---|:---|
| Trailing P/E | | | | | |
| Forward P/E（NTM） | | | | | |
| EV/EBITDA | | | | | |
| P/FCF | | | | | |
| P/S | | | | | |

**解讀（1 段 ≤ 80 字，含 implication）**:當前估值情緒（過熱/合理/便宜）+ 與歷史同分位時業務基本面主要差異 + 對附錄 A 估值燈的確認或修正。QC-33 三段推導:分位計算 → 解讀 → implication。（QC-4 公式:分位 = (當前 − 5Y 低)/(5Y 高 − 5Y 低)×100%，算到整數位。）

### 11.2｜PEG 診斷

| 指標 | 數值 | 判斷基準 | 解讀 |
|:---|:---|:---|:---|
| Forward P/E | | | |
| Non-GAAP EPS CAGR（3 年，§5） | | | |
| PEG（Non-GAAP，3 年） | | < 1.0 便宜 / 1∼2 合理 / > 2 貴 | |
| PEG（GAAP，3 年） | | 同上 | |
| 5 年 EPS CAGR（含 Runway 遞減，§6.A） | | | |
| PEG（5 年，Non-GAAP） | | | |
| 3 年 vs 5 年 PEG 差異 | | 差異大 = 近期成長不可持續，需警惕 | |

**解讀（1 段 ≤ 80 字 + QC-33 三段推導）**:PEG 計算 → 矩陣落點 → implication。若 3Y vs 5Y PEG 差距 > 0.5，說明近期成長不可持續，需在 §6.E 反映。

### 11.4｜同業估值比較（強制「對的 peer group tier」）

在列同業表之前，必須先判斷標的業務模式 tier:

| 業務模式 tier | 典型公司 | Peer 選法 |
|:---|:---|:---|
| IP company / 純設計 | ARM, Qualcomm, Cadence | 同 tier IP 公司 |
| 設計服務（Turnkey ASIC） | Alchip, GUC, Faraday | 同 tier 設計服務 |
| 純代工（Foundry） | TSMC, SMIC, UMC | 同 tier foundry |
| SaaS 訂閱型 | Snowflake, Salesforce, ServiceNow | 同 tier SaaS |
| 寡占消費 / 品牌 | LV, Hermès, Apple | 同 tier 消費溢價 |

**禁止**用「同產業但不同業務模式 tier」的高倍數公司當 anchor（3661 Alchip 教訓:應跟 GUC/Faraday 比，不是 AVGO/MRVL）。若無同 tier 上市公司可比，標明「⚠️ 無 ideal peer group，本表僅供參考，溢折價邏輯需獨立推導」。
本標的業務模式 tier:**__（說明判斷依據）**。

| 公司 | 市值 | Forward P/E | EV/EBITDA | PEG | FCF Margin | EPS CAGR（3 年） | ROIC |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **[標的]** | | | | | | | |
| 同業 A（同 tier） | | | | | | | |
| 同業 B（同 tier） | | | | | | | |
| 同業 C（同 tier） | | | | | | | |
| 同 tier 中位數 | | | | | | | |

**解讀（1 段 ≤ 80 字 + QC-33 三段推導）**:溢/折價幅度 → 護城河/成長性/資本效率哪項更優支撐溢價 → 若向 tier 中位數均值回歸，股價變動方向 → implication。
**分析師目標價參考**:高 $__ / 中位 $__ / 低 $__（n=__ 位）;是否認同共識中位？若不同，一句話說明分歧點。

### 11.5｜不對稱報酬 Bull/Base/Bear 5Y + 機率 + IRR

> 5Y multiple 與 EPS 用 §5 / §9 同輪搜得的 consensus + 同業 band，不另搜。**ev5y_pct（5Y 累積機率加權 EV%）由本表填 dd-meta**;`irr_base_pct`（選填）= Base 列年化 IRR。

| 情境 | 5 年絕對 | 年化 IRR | 依據 | 機率估計 |
|:---|:---|:---|:---|:---|
| Thesis 對（Bull）5 年漲幅 | +__% | +__%/yr | ___ | __% |
| Base | +__% | +__%/yr | ___ | __% |
| Thesis 錯（Bear）5 年跌幅 | -__% | -__%/yr | ___ | __% |
| **機率加權期望值** | **+__% 5Y（= ev5y_pct）** | **IRR ≈ __%/yr** | | |

**IRR 公式**:`(1 + 5Y_pct)^(1/5) - 1`。**為何強制年化**:5Y 絕對 % 跨案件不可比;IRR 把時間納入分母，避免遠期報酬被高估。
**IRR 落點解讀**:< 8%/yr 弱（不及大盤平均）/ 8-12%/yr 中（合理 mid-conviction）/ > 12%/yr 強（裁決內部高確信）/ > 15%/yr 罕見（檢查機率分配是否過度樂觀）。**IRR 是裁決內部的確信刻度，不作跨檔排序依據**（2026-07-04 持有人拍板:核心/衛星軌別歸 moat、跨檔排序歸 GRP 三閘[成長×上修×位置]，5Y IRR 只是單檔資訊，見 GRP mandate）。
**追加壓力測試**:thesis 對但時間拉長兩倍（10 年），10Y IRR 是多少?考慮機會成本後的答案?（同期可比標的 IRR ≈ ?）

**不對稱比 AR（v14.3，必填一行）**:`AR = (P_bull × |Bull 5Y%|) / (P_bear × |Bear 5Y%|)`，取 1 位小數，寫入 dd-meta 選填欄 `asym_ratio`。**AR Live 掛單（v14.3 F4）**:同時把 Bull/Bear 5Y 目標價與機率寫入 dd-meta 選填四欄 `bull_5y_price`/`bear_5y_price`/`p_bull_pct`/`p_bear_pct`——dd-screener 每日以現價重算 `ar_live`，當 runway 🟢 + moat ≠↓ 的觀望股因回檔使 ar_live ≥ 4 時自動亮進「爆發獵場 watch」（把「觀望等回檔」從人記得變成系統掛單;報告內的 AR 是報告日快照，ar_live 是活數字）。解讀:< 2 平庸 / 2-4 偏正 / **≥ 4 顯著不對稱（§14 row 8a 爆發候選門檻）**。**AR 不是放鬆機率防線的理由**——下方反偏差防線（Bear 下限/Base 上限）照舊全部適用;AR 的意義正是「在誠實機率下仍然成立的不對稱」。Bear 5Y% ≥ 0（無下行情境）→ AR 標 N/A 並省略 dd-meta 欄（禁止用零下行製造無限大）;Bull 依據必須引用 §9.F 滲透率算術與 §11.7 pattern match IRR，且含關鍵分部的量×價骨架（用 §9.F 滲透率推 Bull 營收即可，不必全分部），不接受敘事式 Bull。

**10Y 二段延伸（v14.3;runway_post_y5 = 🟢 時必填，🟡/🔴 免填）**:數倍報酬通常需要 7-10 年複利，5Y 框架裝不下——本行給「數倍路徑」正式落點，也是 QC-48 critic 的可驗物之一。

| 項目 | 內容 |
|:---|:---|
| Y5→Y10 第二段 EPS CAGR 假設 | __%（依據:§6.A'' 第二 S 曲線 / Y5 末滲透率 → Y10 滲透率推演） |
| 10Y 累積倍數（Base 路徑延伸） | __x（= 5Y Base 終值 × 第二段複利;附一句退坡假設，第二段 CAGR 原則上 < 第一段） |
| 10Y IRR | __%/yr（與上方追加壓力測試同源，此處落成數字） |

**機率估計時間視角指引（反偏差防線）**:
| 檢查項 | 標準 |
|:---|:---|
| Bear 機率 | 5Y 視角下不應 < 20%（多數 25-30%;只有極強護城河 + 短期已兌現才壓到 15-20%）|
| Bull/Bear 散布 | 5Y 應比 1Y/2Y 寬至少 50%。太窄 = 「拿短期視角信心套到長期」 |
| Base 機率 | 不應 > 50%。太高代表沒真正壓測失敗路徑 |
| Pattern match 校準 | §11.7 歷史相似 case 年化 IRR 是多少?當前估計與其差距是否合理 |
| **QC-39 閘 B durability（雙向，必填）** | **循環/商品股的 bear 機率與 §6.E normalized 假設,必須註明依據是『QC-39 searched 的供需 durability 證據』還是『歷史 pattern 外推』。**(防 SNDK 型過嚴)若產業有 sourced 結構性 durability(供給紀律 / 無新產能至 X 年 / 需求結構黏),報告仍用歷史谷底硬套 bear → 須明說「為何不採信結構性論點」,否則 **bear 機率不得高於 base**。**反向(防純價格泡沫):**若 durability 薄弱(供給可逆 / 玩家多無紀律 / 純 ASP 無量增),不得因「產業在缺」就壓低 bear,須點明脆弱性並維持高 bear。一句話寫明:「本案 bear 機率 __% 主要依據 = ___(searched durability / 歷史 pattern),產業態勢雙向裁決見 §9」 |

**內生天花板 sanity check（必填一行）**:Base 情境 EPS CAGR 貢獻 __%（§11.6）vs §6.D 內生成長天花板 __%（+ 已歸因缺口）→ **在天花板內 ✅ / 超出 ⚠**。數據來源:dd-meta `endo_growth_ceiling`;若無此欄 → 標「本檢核 N/A」。**超出 ⚠ → §11.5 Bear 機率強制 ≥ 30%**（共識成長超過生意自身能長出來的上限 = 依賴 re-rate 或 margin 一次性，下行尾巴更肥）。**例外（v14.3）**:缺口已歸因到 §9.F 有 sourced 的新 segment / 新 S 曲線（具體段名 + TAM 數字 + 來源）→ Bear 下限回落至一般 25%、不強制 30%——新 S 曲線的成長本來就不在「現有生意內生天花板」之內，用舊天花板懲罰它是類別錯誤;但歸因必須 sourced，「AI 選擇權」一句話帶過不適用例外。

### 11.6｜IRR 三分量拆解（EPS CAGR / re-rate / 股息+回購）

> **質感**:同樣 12% IRR，90% 來自 EPS 複利 vs 60% 來自 P/E re-rate，可抱性差一大截。前者自然複利（公司自己長出來），後者要等市場配合。長抱者必須知道賭的是哪一種。

三情境各自拆解：

| 情境 | EPS CAGR 貢獻 | 估值 re-rate 貢獻 | 股息 + 淨買回 | 合計年化 |
|:---|:---|:---|:---|:---|
| Bull | +__%/yr | +__%/yr | +__%/yr | +__%/yr |
| Base | +__%/yr | +__%/yr（或 −__%/yr） | +__%/yr | +__%/yr |
| Bear | +__%/yr 或 −__%/yr | −__%/yr | +__%/yr | −__%/yr |

**換算公式**:EPS 貢獻 = EPS CAGR 直接寫;re-rate = `(end_PE / start_PE)^(1/5) - 1`;股息+淨買回 = 平均股息率 + 平均淨買回率（扣 SBC 後）;合計 ≈ 三項相加（≤ 1%p 誤差容忍）。
**Guardrail**:合計年化與 §11.5「機率加權年化 IRR」的 Base 列偏差 > 2%p → 整個 §11.5/11.6 打回校驗。
**質感解讀（表格下方 ≤ 80 字 narrative，必填）**:「Base __% IRR 中，__%/yr 來自 EPS 複利，__%/yr 來自估值 re-rate，__%/yr 來自股息+回購。可抱性主要靠 ___（EPS / re-rate / shareholder return）— ___（自然複利好抱 / 需市場配合難抱 / 防禦型穩拿）。」
**估值依賴型標記（硬規則）**:**re-rate 貢獻 ≥ Base 合計 IRR 的 40% → 強制標記「估值依賴型」**。此標記餵入 §14 決策矩陣 Soft Veto。
**QC-45 未獲利股（v14.3 F1）**:負 EPS 下 EPS CAGR 與 `end_PE/start_PE` 公式 undefined → 三分量改拆「**營收 CAGR 貢獻 / EV/S re-rate 貢獻**（`(end_EVS/start_EVS)^(1/5)-1`）/ **股權稀釋拖累**（SBC 稀釋，通常負貢獻）」;§11.5 三情境改以「轉正年 + 轉正後 EPS × 該年合理 PE」推 5Y 目標價（Bear 含「轉正失敗、以 EV/S 壓縮計」路徑），AR 公式與機率防線不變。估值依賴型標記改看 **EV/S re-rate 佔比 ≥ 40%**。

### 11.7｜Pattern match（歷史相似 case，讓機率有錨點）+ 內生天花板對照

| 項目 | 內容 |
|:---|:---|
| 歷史上 thesis 結構類似的個股 | （例:「2017 NVDA 早期 AI 賭局」） |
| 當時的 setup（估值倍數、市佔、技術節點） | |
| 最終 5 年實現報酬（含年化 IRR） | |
| 我的標的和它最像 / 最不像的地方 | |

**這不是說會複製，而是讓 5 年期望 IRR 的估計不只是憑感覺。** Guardrail:必須舉一個具體歷史 case，不接受「沒有歷史可比」。

### §11 估值診斷結論（1 段，指向 §1 / §14）

**結論格式（1 段 ≤ 100 字，整合 11.1/11.2/11.4 三個訊號）**:11.1 歷史分位（__% → 過熱/合理/便宜）+ 11.2 PEG（__ → __）+ 11.4 同業相對（溢/折價 __%，有/無基本面支撐）→ 綜合估值訊號:**🔴明顯貴 / 🟡公允 / 🟢合理至便宜**。完整裁決見 §14;倉位角色見 §14a。
**consensus 落後註記（v14.3，強制檢查一句）**:若 §9.F 滲透率算術顯示 consensus FY3 EPS 明顯低估（bottom-up 推導 vs 共識差 > 20%）→ 在結論段加標「**consensus 落後風險**:本節估值燈以 FY2 共識為錨，爆發早期共識系統性落後，燈號可能偏嚴」，供 §12 矛盾裁決消化。**此註記不改燈號判定**（放寬 🔴 需等 outcome 校準實證後另議）。

---

# Part II — 決策層（疊在基本面上，不重搜，~22% 篇幅）

> **不重搜原則**:Part II 的所有判斷以 Part I 已完成的基本面研究為素材。**§12 矛盾辨識比對的是 Part I 各章節之間（及 vs 上一份報告）的結論張力，不另起 web search**;§13 pre-mortem 從 Part I 風險與假設推估;§14 決策由 Part I 的品質/估值/護城河趨勢/runway/Max DD 驅動。

---

## §12｜矛盾辨識與強制裁決

**本章是 Part I（基本面）與 §14（決策）之間的關鍵過渡層。** 把 Part I 各章節的結論攤開，找出方向不一致處並強制下判決，避免 §14 用「兩邊都對」逃避決策。

### 1. 共識清單

列出 Part I 各章節中**方向一致**的判斷（例:§6 成長 🟢 + §7 護城河 ↑ + §9 利潤池流入 三者共振），這些是高信心區域。

### 2. 矛盾清單

| # | 矛盾點描述 | 章節 A 結論 | 章節 B 結論 | 性質 |
|:---|:---|:---|:---|:---|
| | （例:§7 護城河 ↑ widening vs §9 利潤池 ↓ 流出） | | | 可調和（程度差異）/ 不可調和（方向相反） |

（典型張力軸:護城河趨勢 §7 vs 利潤池流向 §9;成長評級 §6 vs 估值 §11;execution moat vs pricing power moat 二維分歧;共識 EPS CAGR §5 vs 內生天花板 §6.D。）

### 3. 與上一份報告的交叉矛盾（若有）

| # | 矛盾點 | 本次結論 | 上一份報告結論 | 可能原因 |
|:---|:---|:---|:---|:---|
| | | | | 時間差 / 分析深度差 / 視角差 |

### 4. ⚖ 強制裁決（每個「不可調和」矛盾必填）

> 列出矛盾不等於想清楚 — 容易產出「兩邊都有道理」的虛假平衡。**每個不可調和矛盾必須下判決。**

| # | 矛盾 | 我選哪邊 | 我的依據（不能是「直覺」「平衡考慮」） | 會 settle 此衝突的硬數據點（具體價位 / 倍數 / 季度指標 / 日期事件 + 出處 + 頻率） | 裁決後執行路徑（**≥ 2 條 if-then**） |
|:---|:---|:---|:---|:---|:---|
| | | 章節 A / 章節 B / 暫無法決定 | | （例:股價回到 $545 PE 21x、Q3 ASP YoY > +5%、N2 量產延後到 2026Q2） | (a) 觸發 X → 動作 Y;(b) 觸發 Z → 動作 W |

**裁決後執行路徑要求**:至少 2 條 if-then，兩條觸發條件方向相反（一條 upside、一條 downside）;「動作」要具體（升級小倉測試 / 減持 / 加碼至 X% / 清倉），禁止寫「再評估」「持續觀察」。**這些裁決直接帶入 §14，作為決策框架的主軸。**

---

## §13｜Pre-mortem 與 Max DD

### 13a. 強迫面對自己的盲點（不確定假設）

| # | 我不確定的假設 | Thesis 仍成立的前提 | 如果假設不成立的後果 |
|:---|:---|:---|:---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### 13b. Pre-mortem：失敗故事倒推（+ 內部校驗 §3.F，QC-40 適用）

> §13a 是靜態列假設，pre-mortem 強迫具體化失敗路徑。和 §3.F 互補:§3.F 是單點觸發、pre-mortem 是路徑想像。**最常見偷懶 = 寫了失敗故事卻沒回頭校驗 §3.F。** 故仍強制做校驗，**但校驗是內部步驟（QC-40）——HTML 只呈現失敗故事 narrative，不渲染校驗 checklist 與「✅ 不需修正」對帳。**

**HTML 呈現（讀者面前只有這個）｜失敗故事 narrative**（≤80 字，不是表格）:
> 「假設 5 年後這個部位虧 50%，最可能發生的故事是 ___（具體含人事時地物，例:『2027Q2 Apple 將 N2 訂單轉給 Samsung，TSMC N2 utilization 跌至 65%，毛利率掉到 48%，市場重估 forward PE 從 22x 壓縮到 14x』）。」

**內部校驗（LLM 執行於心，不渲染進 HTML）**:寫完故事後，LLM 必須自問「這個失敗觸發是否＝ §3.F 的 Single Thing？」並依結果**直接行動**:
- ✅ **是**（直接撞上）→ §3.F 不動。
- ⚠ **部分重疊** → **直接默默回 §3.F 補一條 secondary trigger**（HTML 中 §3.F 顯示為 N+1 條，但不寫「我補了一條」的對帳）。
- ❌ **完全獨立** → **直接回 §3.F 重寫 / 新增 primary**。

**唯一允許在 HTML 留下的痕跡**:若校驗導致 §3.F 實際被修正，可在 §13b 末**用一句 narrative** 帶過（如「上述失敗路徑促使我把 §3.F 的觸發補上 ___」）;若 §3.F 不需動，**什麼都不寫**（不要寫「✅ 不需修正」「trigger 數未變」這類對帳）。
**內部 Guardrail（不渲染）**:若校驗結論是 ⚠/❌ 卻沒實際改動 §3.F → 自我打回重做。此 Guardrail 是 LLM 的執行紀律，**不是 HTML 內容**。

### 13c. 路徑壓力測試（Max DD｜必填，餵 dd-meta）

> §11.5 Bear 是 5Y 終點的痛，但實務上抱不住通常死在「中途某次 −55%」而非終點 −30%。即使 5Y 終點打平，中途 max drawdown 太深，多數人會在最低點被洗出去。

從 §13b pre-mortem 失敗故事 narrative 推估:**這 5 年期間，最壞時點（peak-to-trough）的估計 drawdown 範圍是多少？**

| 項目 | 內容 |
|:---|:---|
| 估計 Max DD 範圍 | **−__% ~ −__%**（必須給範圍，禁止單點 — 避免假精準） |
| 最可能觸發時點 | __ 年後 ___（含具體事件） |
| 觸發後最快多久恢復到峰值 | __ 個月 / __ 季 / __ 年（如不會恢復則明寫「thesis 已破」） |
| 路徑風險評級 | 🟢 0~−30%（多數人扛得住）/ 🟡 −30~−50%（需要強信念）/ 🔴 <−50%（多數人會中途出場） |

**校驗（必填一句話）**:「若 max DD 落在 ___，我能否撐到復原？條件:___（例:『部位不超過 portfolio 8%、不使用槓桿、§3.F trigger 未發生』）。若無法給出明確條件 → §14a 倉位必須再打折。」
**Guardrail**:範圍寬度（上界 − 下界）必須 ≥ 10%p;< 10%p 視為假精準，打回。**評級 🔴 的倉位處理（v14.2 F2 條件式）**:🔴 **且 thesis 脆弱**（moat_trend ↓ 或 runway_post_y5 🔴 或 §11.6 估值依賴型，任一）→ §14a 倉位上限自動下修（例:6% → ≤ 3%）+ §14c 警示「中途出場風險高」。🔴 **但 thesis 完整**（上述皆無）→ **不因波動本身砍倉**，改為 §14a 註記「深回撤心理準備:Max DD −__%，僅在能承受此波動下持有;倉位上限交 PM，不因回撤幅度強制下修」+ §14c 警示。WHY:偉大長波段複利股幾乎都有 >50% 回撤，純用回撤幅度砍倉＝篩掉最會漲的贏家;砍倉只在「深回撤＋thesis 脆弱」雙重成立時才必要。
**dd-meta `max_dd_pct`（選填）**:取範圍下界（最差值，負數，例 −55.0）寫入;頁首儀表板「Max DD −__%」同取下界，三處一致。

---

## §14｜決策（id="decision"｜統一裁決唯一居所）

> **本章為人面對的唯一裁決居所。** HTML `<section>` 必須帶 `id="decision"` 錨點（research 頁定見欄連到 `/dd/DD_X.html#decision`）。統一裁決（進場/觀望/迴避）由基本面驅動，與頁首儀表板 + dd-meta `dca_verdict` 三處完全一致。

### 裁決晶片（Verdict Chip）— §14 最頂行必須輸出

每份報告必須在 §14 最頂行輸出一個且僅一個裁決晶片，由下方決策矩陣產出。三處一致:此晶片 + 頁首儀表板「統一裁決」格 + dd-meta `dca_verdict`。

| 裁決 | 色彩（背景 / 前景 / 左線） | 含義 |
|:---|:---|:---|
| 進場 | #166534 / #fff / #14532D | 立即加入或增加部位（含條件式進場） |
| 觀望 | #92400E / #fff / #78350F | 不行動;列出重啟觸發條件或維持理由 |
| 迴避 | #991B1B / #fff / #7F1D1D | 結構性不持有;§14a-14c 全部 N/A，改輸出「不持有理由」+「重啟條件 OR 永久迴避」 |

晶片正下方副標籤（13px、#475569、斜體）:一句話概括進場節奏（進場·條件式:「首階小倉＋回檔加碼」）、等待條件（觀望）或迴避核心原因（迴避）。

### 決策矩陣（執行 §14 時必須套用，由基本面驅動）

| 優先序 | 條件 | 裁決 |
|:---:|:---|:---:|
| 1（Hard Veto） | 基本面評級 signal = X | 迴避 |
| 2（Hard Veto） | §12 強制裁決:thesis 不可調和不成立 | 迴避 |
| 3（Hard Veto） | moat_trend ↓（§7）**且** moat 等級 ≤ B | 迴避 |
| 4（進場節奏調節，**非裁決閘**，v14.5） | 週線結構趨勢過濾 ❌（附錄 A:價 < W250 或 W250 斜率轉負） | **不改裁決頭銜**——裁決仍照 row 8-10 算。命中 → §14a 進場節奏強制分批（starter 1/3 ＋ 趨勢確認後加碼）＋頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」。與 row 5 對稱:row 5 治追高、row 4 治接刀，兩者皆 pacing 非 verdict cap。WHY:SE（PEG 0.63、FPE 8th pct、AR 8.8、runway 🟢）與 NOW（AR 7.7）皆被舊 row 4「Soft Veto 鎖觀望」擋下——屬「便宜＋不對稱被趨勢閘擋在門外」型 miss;且舊條文與附錄 A 自稱 INFORMATIONAL ONLY 自相矛盾（六態機退役後 MA 狀態不再單獨封鎖裁決）。 |
| 5（進場節奏調節，**非裁決閘**） | 動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A） | **不改裁決頭銜**——裁決仍照 row 8-10 算。命中 → §14a 進場節奏強制條件式分批（首階小倉＋回檔加碼）＋頁首掛「⚠️ 動能過熱，勿追高」。估值另由 row 8（🟠）獨立把關，故過熱+偏貴仍落觀望。 |
| 6（Soft Veto） | 基本面評級 signal = C | ≥ 觀望 |
| 7（Soft Veto） | runway_post_y5 = 🔴（§6.A''） | ≥ 觀望（§14c ≤ 3Y 警示） |
| 7a（Soft Veto） | §11.6 標記「估值依賴型」**且** §12 未給出「市場錯在哪」的具體理由 | ≥ 觀望，且 §14c 持有年限上限「中期 2-5 年」 |
| 7b（Soft Veto） | dd-meta `capalloc_grade` = C（DD 未提供 → N/A 不觸發） | 裁決本身不降，但 §14c 持有年限上限「中期 2-5 年」 |
| 8a（Baseline·爆發候選，v14.3;v14.5 放寬） | 無 Hard Veto + 無 Soft Veto（row 6/7/7a 皆未命中）+ signal ≥ B + runway_post_y5 = 🟢（§6.A''）+ AR ≥ 4（§11.5）+ 非估值依賴型（§11.6）+ moat_trend ≠ ↓ + 估值 ∈ {🟠, 🔴} | 進場·條件式（爆發候選——**結構型數倍候選，≠ picks 爆發榜的循環拐點型;後者走 row 8b**）——衛星級 starter，倉位/加碼見 §14a 爆發候選分支;**估值 🔴 時強制附 F2 式紀律**（必填回檔重進門檻＋倉位減半 starter，融貫 §11.5/§14a）;**命中即強制 QC-48 冷讀，critic 打回 → 降 row 8 觀望** |
| 8b（Baseline·循環衛星，條件式，v14.5） | 無 Hard Veto + archetype ∈ 循環子型（QC-43 #2 商品循環/capex 建設循環/需求量循環，含 #7 EMS/ODM 之循環面）+ 附錄 B 位置錶 ∈ {深谷投降, 早循環}+ QC-42 反動能五閘全過（逐條檢查）+ moat 底線（評級 ≠ X 且非「moat_trend ↓ 之 C 級」）| 進場·條件式（循環衛星）——`dca_role` 取「衛星持倉」或「投機部位」（禁核心）、倉位上限 3%（軌別天花板，非 PM 拍板;實際組合佔比歸 PM）、退出走循環位置錶（非 thesis 級——§14b 分軌已豁免衛星允許價格觸發，引用之）;**命中即強制 spawn 獨立 critic 冷讀循環位置判定（比照 QC-48 機制與不對稱原則:驗證失敗不得升級、只能降回 row 8 觀望）** |
| 8（Baseline） | 無 Hard Veto + signal ≥ B + 估值 ∈ {🟠, 🔴} | 觀望（等估值;🔴 時 §14b 重啟條件必含具體估值回落門檻） |
| 9（Baseline） | 無 Veto + signal ≥ B + 估值 ≤ 🟡 + MA 🟢/✅ | 進場 |
| 9b（Baseline·長波段佈局） | 無 Veto + signal ≥ B + 估值 ≤ 🟡 + MA 🟡/🟠（減半/觀察池/暫不進場，W250 斜率未轉負）| 進場·條件式（逢回分批;上升趨勢中的回檔/成熟期佈局點，非追高）|
| 10（Baseline） | 無 Veto + signal ≥ A + MA 🟢/✅ + 估值 🟢/🟡 | 進場 |

**衝突解決**:max-severity wins — 任一 Hard Veto（row 1-3）命中 → 直接鎖定迴避;Soft Veto（row 6/7/7a）命中 → 上限觀望（不得輸出進場）。**row 4 週線結構趨勢過濾 ❌ 與 row 5 動能過熱皆為進場節奏調節（v14.5 起 row 4 退出 Soft Veto）**——只修飾 §14a 進場節奏（分批），不改裁決頭銜（對齊 QC-7b:技術面不主導 §14;MA 狀態不再單獨封鎖裁決）。**row 8a 在 row 8 之前判定（v14.3）**:估值 🟠/🔴 先測爆發候選六條件，全過才推翻觀望，任一不過 → 落 row 8（估值 🔴 時 8a 需附 F2 式紀律，見 row 8a）。Soft Veto（row 6/7/7a）對 8a 同樣封鎖——爆發候選不是 veto 繞行道。**row 8b 循環衛星（v14.5）**:循環 archetype 的例外進場路徑（比照 8a 對 row 8 的推翻），可越過 row 6/7 Soft Veto，但 **Hard Veto（row 1-3）仍鎖死**（moat_trend ↓ 之 C 級由 row 3 擋，故 8b moat 底線本就排除 ↓）;row 4/5 pacing 疊加不改頭銜。**優先序:Hard Veto（1-3）> 循環股走 8b（過則進場·條件式循環衛星）/ 非循環走 8a→8→9/9b/10;row 4/5 一律當 pacing 疊加。** 循環股同時命中 row 4（MA ❌，常見於深谷投降）與 8b 時：**8b 給裁決頭銜（進場·條件式 循環衛星），row 4 只確認「分批接刀」節奏**（本就是 8b 的姿態，不衝突）。QC-42 冷讀 critic 失敗 → 8b 降回 row 8 觀望。**dd-meta `dca_verdict` = 本矩陣最終輸出**。

**MA 狀態語意（v14.2 F1;v14.5 六態機退役後改稱週線結構趨勢過濾）**:🟢 最佳進場 / ✅ 強勢進場 → 進場（row 9/10）;🟡/🟠 回檔或成熟（W250 斜率未轉負）→ 進場·條件式（row 9b，長波段逢回佈局）;**❌ 系統失效（價 < W250 或 W250 斜率轉負）不再把進場壓成觀望**——改為 row 4 進場節奏調節（starter 1/3 ＋ 趨勢確認後加碼，pacing 非 verdict cap）。**ma = "-"（IPO < 250 週樣本不足，v14.3 F3）**:baseline row 的 MA 條件視同 🟡 → 走 row 9b 進場·條件式（新股天然無 5 年均線，不得因樣本不足落空或視同 ❌;年輕股的波動風險由 §13c Max DD 與倉位處理，不由 MA 閘代管）。設計意圖:長波段 skill 鼓勵在結構上升的好公司回檔時佈局，**不要求「股價已站上所有均線」才准進場，也不因跌破均線就封鎖裁決**（原 row 9/10 字面 MA ✅ 會把 🟢 最佳進場與 🟠 回檔擋在外、且造成裁決落空;原 row 4 把破線鎖觀望＝接刀型 miss，皆已修）。

### 14a. 倉位角色與進場計畫 + opportunity cost

> **分支規則**（依裁決晶片）:進場 → 全部欄位完整填寫;**進場·條件式（row 4 週線趨勢未確認 或 row 5 動能過熱命中）→ 初始建倉倉位 = 目標的 1/3（首階小倉/starter，可現在建）、其餘 2/3 掛觸發（row 4 掛趨勢確認、row 5 掛回檔）、進場節奏 = 條件式分批、晶片副標註「進場（條件式:首階小倉＋確認/回檔加碼）」**;**進場·條件式（循環衛星，row 8b 命中，v14.5）→ `dca_role` 取「衛星持倉」或「投機部位」（禁核心）、目標倉位上限 3%（軌別天花板）、首階 = 目標的 1/3、其餘 2/3 掛循環位置錶觸發（深谷投降→分批建立、早循環→分批建立）、§14c 持有年限依循環（季-年）、退出走附錄 B 循環位置錶（非 thesis 級，衛星允許價格觸發）、晶片副標註「進場（循環衛星:循環位置分批）」、**強制附循環位置獨立 critic 已通過的一句結論**;**進場·條件式（爆發候選，row 8a 命中，v14.3）→ `dca_role` 取「衛星持倉」或「投機部位」（禁核心）、目標倉位上限 2-3%（小輸大贏，倉位本身就是風控）、首階 = 目標的 1/3、其餘 2/3 掛雙軌加碼——(a) 回檔觸發（價格）或 (b) 論點增強觸發（§9.F 滲透率 / 訂單 / design win 實績超前推演軌跡，須寫具體數字門檻）、§14c 持有年限標「長期 5-10Y」+ §13c F2 深回撤心理準備註記（爆發候選幾乎必有 >40% 回撤，thesis 完整不因波動砍倉）、晶片副標註「進場（爆發候選:衛星級分批）」**;觀望 → 「初始建倉倉位」= 0%、「目標倉位」= 條件成立後 __%、「進場節奏」改為「觸發條件:___」（**同時把此觸發條件寫 dd-meta 選填 `rearm_trigger` ≤120 字:在等什麼——事件／估值門檻／回檔位，v14.5 建議填**）、§14b 只填「進場條件」path;迴避 → 整表替換為「不持有理由」（≥ 2 條具體論點，對應命中的 Veto）+「重啟條件」（具體事件/數字門檻 OR 標「永久迴避」），§14b/14c 全 N/A。

| 項目 | 具體內容 |
|:---|:---|
| **在投資組合中的角色（必填，寫 dd-meta `dca_role`）** | 核心持倉 / 條件式核心持倉 / 衛星持倉 / 條件式衛星持倉 / 投機部位 / 不持有/迴避 / 候選/追蹤池 |
| 初始建倉倉位 | __% of portfolio（區間，PM 拍板組合佔比） |
| 目標倉位 | __% of portfolio |
| 進場價位區間 | $__ ~ $__ |
| 進場節奏 | 一次建倉 / 分批（幾次、間隔）;若附錄 A 動能過熱 → 強制條件式分批:**首階 1/3 目標倉位可現在建**，其餘 2/3 等回檔觸發（RSI 回 50-60 / 回測 MA60 / Bollinger 中軌）。**與觀望的差別:觀望首階 = 0%、條件式進場首階 = 1/3。** |
| **vs 現有組合的同類曝險（opportunity cost，必填）** | **___（具體點名 portfolio 中已持有的同類，用 GRP 三閘語言比較[成長×EPS 上修×股價位置]，說明為何邊際資金放新標的更優;若已持有同類但排序較弱 → 該減舊加新還是兩個都減？）跨檔比較以 GRP 三閘為準，**5Y IRR 不作跨檔排序依據**（2026-07-04 GRP mandate;IRR 只是單檔確信刻度）**（進場與觀望必填;迴避時整行省略，由「不持有理由」取代） |

> 絕對 value 高 ≠ 該買 — 真正的決策是「邊際資金放這支 vs 加碼現有部位」。沒這一行就只是孤立估值，不是 portfolio 決策。
> **dd-meta `dca_role` enum** 對齊 `aggregate_dca_stats.py` CATEGORY_ORDER:核心持倉 / 條件式核心持倉 / 衛星持倉 / 條件式衛星持倉 / 投機部位 / 不持有/迴避 / 候選/追蹤池。迴避裁決 → `dca_role` = 不持有/迴避;觀望裁決 → 依角色性質取「條件式核心持倉」「條件式衛星持倉」或「候選/追蹤池」。
> **§13c Max DD 路徑風險 🔴 → 倉位處理依 §13c 條件式規則（v14.2 F2）**:thesis 脆弱（moat↓/runway🔴/估值依賴型）才自動下修;thesis 完整則只註記深回撤心理準備、不因波動本身砍倉。§14c 一律標註「中途出場風險高」。

### 14b. 加碼與減碼條件

| 行動 | 觸發條件（價位或事件） | 調整至倉位（區間，PM 拍板組合佔比） |
|:---|:---|:---|
| 加碼 | | __% |
| 加碼 | | __% |
| 減碼 | | __% |
| 清倉 | | 0% |

（對齊 §3.E 決策主線預設;一處推導，兩處對齊。倉位%為區間輸入，實際組合佔比由 portfolio-manager 拍板，對齊 QC-7/QC-11。）

**長抱賣出分軌（v14.3 硬規則）**:`dca_role` 為核心持倉／條件式核心持倉，或裁決為進場·條件式（爆發候選）時——**減碼與清倉的觸發條件必須是 thesis 級**（§13 證偽指標命中、moat 侵蝕 sourced、滲透率/訂單軌跡斷裂、§15 複審觸發），**「估值偏高」「漲幅本身」「觸及目標價」最多觸發 trim 回目標倉位，永不單獨觸發清倉**。這是 F2（不因回撤砍倉）的賣出端對稱條款:F2 治「抱不住回撤」，本條治「抱不住漲幅」——多倍股的大段報酬正是在「看起來已經很貴」之後發生的。衛星／投機角色不受此限（可用價格/估值觸發）。爆發候選裁決時，上表加碼列**至少一條必須是「論點增強」觸發（非價格）**，對齊 §14a 雙軌。

### 14c. 建議持有年限

| 持有年限 | 條件 |
|:---|:---|
| 短期（< 2 年） | 如果___成立 |
| 中期（2-5 年） | 如果___成立 |
| 長期（5-10 年） | 如果___成立 |

**建議持有年限**:___，原因:___（引用 §6.A'' runway_post_y5、§9 利潤池流向、§10 capalloc_grade）。
> **runway_post_y5 = 🔴 → 上限 ≤ 3Y;capalloc_grade = C 或 §11.6 估值依賴型 → 上限「中期 2-5 年」。**
> **迴避路徑終止點**:裁決 = 迴避時，§14c 整節替換為:不持有理由（1-3 句，對應命中 Veto）+ 重啟觀察條件（具體:若 ___ 發生 → 重新啟動完整 DD 決策流程;或標「結構性迴避，無重啟條件」）。

**EPS 預測參考表**:年份（2026E/2027E/2030E 外推）× EPS 估計 × 來源 × 備注（外推假設）。
**假設長期持有（5-10 年），現在的股價適合嗎？**（一段論述，引用 §11.5 Asymmetry 與 EPS 預測。）

---

## §15｜複審觸發與保質期

| # | 重新評估觸發點 | 類型 | 具體時間/條件 |
|:---|:---|:---|:---|
| 1 | | 財報日期 | |
| 2 | | 產業事件 | |
| 3 | | 價位觸發 | |
| 4 | | §3.F 的 Single Thing | |

**這份報告的保質期**:___（明確日期 YYYY-MM-DD 或「下一次財報發布前有效」，**不接受「長期有效」**）。
**最可能發生的 upside 因素**:___
**最可能發生的 downside 因素**:___

---

## 附錄 A｜擇時（降級，~3%。INFORMATIONAL ONLY — 不主導 §14 裁決）

> **定位（v14.5）**:進場板機＝sop-funnel（A1/B 訊號、T+1 執行）;本附錄僅供**結構趨勢過濾**（餵 §14 row 4 節奏調節）與 metadata（`signal`/`val`/`ma`），非擇時系統。**ETF 六態機已於 2026-07-04 退役，本過濾器與其無承繼關係**——本附錄的週線 W52/W104/W250 狀態機只是把「價相對長期均線的結構位置」量化成節奏訊號，不是曾用於 ETF 的那套六態擇時機。

> **降級說明（v13、v14.5 更新）**:舊 DD §2 的週線結構趨勢過濾、短期 R:R、估值燈、品質分機制收進此附錄。它們**不是讀者頭銜，也不主導 §14 統一裁決**。其角色:① 週線結構趨勢過濾 ❌（價 < W250 或 W250 斜率轉負）作為 §14 決策矩陣 **row 4 進場節奏調節**（v14.5 起不再是 Soft Veto——命中只強制 §14a 分批 starter，不把進場壓成觀望;MA 狀態不單獨封鎖裁決）;動能過熱 / 短期 R:R 同為「節奏修飾」（row 5，只把進場改條件式分批，**不改裁決頭銜**——對齊本附錄「不主導 §14」與 QC-7b）;② 品質分 / 估值燈餵頁首儀表板與 dd-meta `signal`/`val`/`ma`（基本面評級 metadata）。完整基本面壓測在 §6.E;此附錄不重複。

### B / H｜基本面評級機制（品質分等級＝B 錨點、綜合訊號 final_signal＝H 錨點，metadata-only）

品質分:底分 = (護城河 §7 + 成長持久性 §6) / 2;品質分 = min(底分 + 體質 veto 加減, 10)。體質檢核 5 項 veto 制（毛利率近 3 年未連續下滑 >2%p / FCF·NI ≥ 0.7 / FY+1 EPS 共識近 90 天未連續下修 / 近 4 季營收 YoY 未全部為負 / Net Debt·EBITDA ≤ 3.0 非金融）:0-2 項不過 等級不變;3 項 降 1 級;4-5 項 直接拒絕。品質等級 ≥ 7.5 A 級 / 6.0-7.4 B 級 / < 6.0 迴避。
**綜合訊號 final_signal = A+/A/B/C/X**:依 quality × 估值燈 × 週線結構過濾 × 大盤豁免 × trap 組合（步驟見下表;A+/A/B/C/X 的**權威定義以 QC-31 為準**，本步表與 QC-31 衝突時以 QC-31 為準;R:R 為參考項不作評級硬條件）。**輸出進 dd-meta `signal`/`verdict`**。

| 步驟 | 條件 | 輸出 |
|:---|:---|:---|
| 1 拒絕檢核 | trap 🔴 或 gate 🔴 或 quality 拒絕（**v14.5:MA ❌ 不再列入拒絕檢核**——MA 只餵 row 4 節奏調節，不封鎖裁決/評級） | X（但 QC-31 cross-check:thesis 完整、僅估值過熱 → 降為 B） |
| 2 高強度 | quality S/A + gate 🟢 + MA 🟢/✅ + trap 🟢 + 大盤正常 | A+ |
| 3 中高強度 | quality S/A + gate 🟡 + MA ✅ + trap 🟢 | A |
| 4 衛星級 | quality B + gate 🟢/🟡 + trap 🟢/🟡;或 S/A 有一項訊號減半 | B |
| 5 時機不到（thesis 完整） | gate 🟠 + MA stretched，或多項訊號減半但無 QC-31 C 觸發 | B（非 C） |
| 6 thesis 失敗 | 觸發 QC-31 任一:品質 < 6.0;護城河侵蝕 ≥ 3;陷阱 🔴;AI 風險 🔴 | C |

### D｜估值燈（FY+1/+2 共識輸入 + 盲點 1 救援）

資料來源:Fwd PE 5Y 分位 = (當前 − 5Y 低)/(5Y 高 − 5Y 低)×100%;PEG = 當前 Fwd PE ÷ 3Y EPS CAGR（§5）。
| 燈號 | 條件 | 邏輯 |
|:---:|:---|:---|
| 🟢 便宜 | 分位 < 30% 或 PEG < 1.0 | 歷史少見便宜 |
| 🟡 合理 | 30-70% 且 1.0 ≤ PEG ≤ 2.0 | 正常估值 |
| 🟠 偏貴 | 70-85% 或 2.0 < PEG ≤ 2.5 | 偏高位置 |
| 🔴 過熱 | > 85% 或 PEG > 2.5 | 透支未來 |
優先序:分位與 PEG 取**較嚴**者。**盲點 1 救援**:結構性高成長股觸發 🟠 偏貴時，若三條件同時滿足（§6 綜合評級 🟢 高確信 + PEG < 2.0 + §6.F AI 🟢）→ 🟠 救回 🟡;不適用情境（分位 > 85% / PEG ≥ 2.0 / QC-19 近 90 天重大利空）維持 🟠。觸發須在附錄 A 明確標註。**輸出進 dd-meta `val`**。

**QC-45 未獲利高成長版估值燈（v14.3 F1;RKLB 乾跑抓到的洞）**:GAAP 負 EPS 時上表的 Fwd PE 分位與 PEG 全部 undefined，但 `val` 是必填 enum 且 §14 全部 baseline row 依賴它——未獲利股不定義燈色 = §14 對十倍股最常出現的類別整組懸空。改用雙尺取**較嚴**者:① **growth-adjusted EV/S** = fwd EV/S ÷ fwd 營收成長%（PEG 的營收版）:< 0.5 🟢 / 0.5-1.0 🟡 / 1.0-1.5 🟠 / > 1.5 🔴;② **自身上市以來 fwd EV/S 分位**（同 30/70/85 切點;上市 < 3 年時僅輔助、不單獨定色）。毛利率 < 50% 的硬體/服務型須另列 EV/gross-profit 對照（防高 EV/S 低毛利被 growth-adjust 美化）。燈色判定推導必須寫明。EPS 轉正（FY+1 > 0）後改回上表 PE/PEG 尺。輸出照常寫 dd-meta `val`。

### F｜週線結構趨勢過濾（週線 W52 / W104 / W250，SMA）

> 本狀態機把「價相對長期均線的結構位置」量化成 §14 row 4 節奏訊號 + dd-meta `ma`（必填欄，8 條下游管線在讀，欄名不動）。**它不輸出倉位乘數**——倉位歸 PM（QC-11），狀態只調節進場節奏（❌ → 分批接刀，非封鎖）。與已退役的 ETF 六態機無承繼關係。

| 狀態 | 條件 |
|:---:|:---|
| 🟢 最佳進場 | 價 < W52 且 價 > W104 且 W52/W104/W250 三條斜率全正 |
| ✅ 強勢進場 | 價 > W52 > W104 > W250 且 W250 斜率正 |
| 🟡 減半進場 | 四條件過但 W250 斜率持平（\|13 週變化\| < 3%）|
| 🟡 觀察池 | 剛站回 W104（站上 < 4 週） |
| 🟠 暫不進場 | 價 < W104 但 > W250，W250 斜率仍正 |
| ❌ 系統失效 | 價 < W250 或 W250 斜率轉負（→ §14 row 4 節奏調節，分批 starter，非封鎖裁決） |

W250 斜率定義:當週 W250 vs 13 週前 W250（正 > +3% / 持平 −3~+3% / 負 < −3%）。**盲點 2 救援**:MA ❌ 但三條件全滿足（附錄 A I 長期持有信心高 + §6 綜合 🟢 + 護城河 §7 ≥ 8）→ 降級為「🟠 暫不進場（追蹤池）」;例外失效（大盤破 W104 / QC-19 重大利空 / W250 斜率 < −10%）。Python 計算同 yfinance 批量採集腳本第 4 段。**輸出進 dd-meta `ma`**。
**「過熱」定義註記**:本附錄之過熱（RSI > 70 / 4 週漂移 +10%）只管 §14 進場節奏;GRP P 閘（週線布林 +2σ）與 picks 爆發 🔥（12M > +250%）各自獨立定義，不互相覆蓋。

```python
# 狀態判定（接續批量採集腳本的 closes / w52 / w104 / w250 / slope_pct）
w52_slope = (w52 / float(np.mean(closes[-65:-13])) - 1) * 100 if len(closes) >= 65 else None
w104_slope = (w104 / float(np.mean(closes[-117:-13])) - 1) * 100 if len(closes) >= 117 else None
if w250 is None: state = "樣本不足（< 250 週）"
elif current < w250 or slope_pct < -3: state = "❌ 系統失效"
elif current < w104: state = "🟠 暫不進場"
elif current < w52 and w52_slope > 0 and w104_slope > 0 and slope_pct > 0: state = "🟢 最佳進場"
elif current > w52 > w104 > w250 and slope_pct > 3: state = "✅ 強勢進場"
elif current > w52 > w104 > w250 and abs(slope_pct) <= 3: state = "🟡 減半進場"
else: state = "🟡 觀察池"
```

### G｜大盤豁免層（系統性風險）

大盤週收 < 自身 W104 → 系統性風險。對應大盤:美股 SPX、台股 TAIEX、ADR/跨市場 母市場 + 上市市場取保守。係數 × 1.0（正常）/ × 0.5（破 W104）。此係數作為 final_signal 的減半輸入（metadata），不主導 §14。

### I｜長期持有信心（dd-meta `long_term_confidence`，必填 enum 高/中/低）

**定義（v14.5 補回;隨 v13 改版一度被刪，QC-31 A 級條件與頁首儀表板都引用它卻無計算規則）**:長期持有信心 = 「這標的**值不值得抱穿 5-10 年**」的綜合信念，由四個既有訊號合成（非另搜）:

| 輸入 | 來源 | 高分方向 |
|:---|:---|:---|
| moat 等級 | §7 合併分 → S/A/B/C | S/A 佳 |
| moat_trend | §7 權威趨勢 | ↑ 或 → 佳，↓ 扣 |
| runway_post_y5 | §6.A'' | 🟢 佳，🔴 扣 |
| §13 證偽距離 | §13a/§13b 失敗故事離發生有多遠 + §3.F 機率 | 遠/低機率佳 |

**映射規則**:
- **高**:moat S/A **且** moat_trend ∈ {↑, →} **且** runway_post_y5 ∈ {🟢, 🟡} **且** §13 證偽距離遠（§3.F 12-24M 機率 < ~20%）。
- **低**（任一）:moat_trend = ↓;或 runway_post_y5 = 🔴;或 §13 證偽近在眼前（§3.F 機率 > ~40% 或 §13b 失敗故事已在發生）;或 §10 capalloc_grade = C（接線見 §10）;或 §11.6 估值依賴型。
- **中**:其餘（不滿足「高」全部條件、也未觸發任何「低」條件）。

**接線**:此值寫 dd-meta `long_term_confidence`、進頁首儀表板、且是 QC-31 A 級的必要條件之一（QC-31「A = 品質 ≥ 7.5 + 中期 R:R ≥ 1.0 + 長期持有信心 = 高」引用此定義）。**其他章節對「長期持有信心上限『中』」的硬接線**（§6.D 內生天花板無法歸因、§10 capalloc_grade C）依上表「低/中」規則收斂。

### R:R 三時距（資訊性，3 個數字 + 1 行 Bear anchor）

合理 P/E 參考自 §7 護城河分數 + §6 成長評級決定的倍數基準。
| 時距 | 計算 | 目標價 | R:R |
|:---|:---|:---|:---|
| 短期（1 年）| FY+1 EPS × 合理 P/E | $__ | __x |
| 中期（2 年）| FY+2 EPS × 合理 P/E | $__ | __x |
| 5Y（長期）| §6.E Base 5Y EPS × 長期合理 PE | $__ | __x |

**Bear anchor（1 行）**:Bear EPS = FY+1 EPS × 0.9;Bear PE = §6.E 成長熄火「降至 10%」情境;Bear 股價 = $__（現價下行 __%）。**dd-meta `stress`**:記錄 2/2（base + bear 兩情境，QC-29）;`upside_short_pct`/`upside_mid_pct` 取短/中期 R:R 對應 upside。QC-21 R:R 數學假象防禦適用。

---

## 附錄 B｜循環交易讀數（條件性，僅循環/商品 archetype；SPECULATIVE 交易姿態 — 位置結論 v14.5 起接 §14 row 8b）

> **定位（v14.1 增補、v14.4 v0.2、v14.5 位置落 §14/dd-meta，QC-42）**:與附錄 A 並列的另一條軌，答 **Game 2**——「現在在循環哪一格、該怎麼動」。**僅當 QC-43 判定 primary/secondary ∈ 循環子型才渲染**（archetype 驅動，非商品觸發項計數）;成長複利股整段省略、不留佔位。**v14.5 改**:循環**位置**結論（B.1）落 dd-meta 選填欄 `cycle_position`／`cycle_verdict` 並接 §14 row 8b（循環衛星條件式進場，位置 ∈ {深谷投降,早循環}+ 五閘全過 + moat 底線 + 獨立 critic 通過才成立）;**交易姿態（trade_stance）與時間框架仍全程明標「投機/交易」、僅進 HTML 不入 dd-meta**。觸發/路由/紀律/落欄規格見 QC-42。**參考實作**:capex 循環 `docs/dd/DD_ORCL_20260703.html`、EMS 需求量循環 `docs/dd/DD_JBL_20260703.html`（B.5 為錶族設計母本）、原生商品 `docs/dd/DD_MU_20260622.html`。

### B.0 觸發 + 子型判別（一至二行）

QC-43 循環判定:__（primary/secondary 屬循環子型的依據一句）→ 啟動附錄 B。**選用位置錶**:商品 through-cycle（記憶體/礦業/航運…）/ capex 建設循環（ORCL 型）/ 需求量循環（EMS/ODM，JBL 型）擇一，並一句寫判別式（有無真商品/循環 sleeve、下跌驅動來源）。商品子型另列命中的商品觸發項（≥2）。

### B.1 循環位置（用 B.0 選定的子型錶;錨**自身 through-cycle 區間**，非動能）

位置一律落 深谷投降 / 早循環 / 中循環 / 晚循環 / 過熱頂部（多數投票 + 一句 sourced 裁決）。**只填選定那張錶**（三選一;非適用訊號標 N/A 並註原因）:

**商品 through-cycle 錶（MU 型，6 訊號）**
| 訊號 | 偏底（買區） | 偏頂（賣區） | 本標的讀數 | 票 |
|:---|:---|:---|:---|:--:|
| P/B vs 自身區間 | 近 1x / 下緣 | > 自身中位 2x / 上緣 | | |
| 量 vs 價（bit·出貨 vs ASP） | 量增領先 | ASP-only、量持平/降 | | |
| GM vs 自身區間 | 近谷 / 負 | 近峰 | | |
| 供給紀律 | 減產 / 無新產能 | 新產能洪水 / 補貼擴產 | | |
| 庫存 | 去化乾淨 / 精實 | 通路 + 公司同步堆積 | | |
| 情緒 / 部位 | 投降、賣方 PT > 現價 | 狂熱、PT < 現價、極端超買 | | |

**capex 建設循環錶（ORCL 型，6 訊號）**
| 訊號 | 偏底（買區） | 偏頂（賣區） | 本標的讀數 | 票 |
|:---|:---|:---|:---|:--:|
| capex/折舊比 | 低 / 正常化 | 遠高於 1（產能洪水） | | |
| 產能利用率爬坡 | 低基期回升 | 滿載 / 見頂 | | |
| RPO（backlog）vs capex 覆蓋 | backlog 領先 capex | capex 超前需求 | | |
| 交易對手信用 | 客戶分散 / 信用強 | 集中且燒錢客戶 | | |
| 情緒 / 部位 | 投降、PT > 價 | 狂熱、PT < 價 | | |
| 量 vs 價 | 量增領先 | ASP 承壓 / 量見頂 | | |

**需求量循環錶（EMS/ODM，JBL 型，5 訊號）**
| 訊號 | 偏底（買區） | 偏頂（賣區） | 本標的讀數 | 票 |
|:---|:---|:---|:---|:--:|
| book-to-bill / 需求量拐點 | > 1 / 拐點向上 | < 1 / 量見頂 | | |
| 客戶庫存去化 | 去化乾淨 | 通路 + 客戶堆積 | | |
| 倍數 vs 自身歷史（re-rate 均值回歸） | 近下緣 | > 5Y 中位 ×1.5 / 貼峰 | | |
| 終端·hyperscaler capex 週期位置 | 早週期 | 晚週期 / 見頂 | | |
| 情緒 / 部位 | 投降、PT > 價 | 狂熱、PT < 價 | | |

### B.2 交易姿態（位置 → 姿態 + 反動能硬閘;跨子型通用）

**交易姿態 = __**（深谷投降→積極分批建立 / 早→分批建立 / 中→持有不加 / 晚→分批了結 / 過熱頂部→清光不碰）

硬閘檢查（逐條，觸發即 override 向保守;跨三張錶通用）:閘 1 晚/頂禁「建立」｜閘 2 ASP-only+量平 封頂「持有」（商品錶）｜閘 3 P/B > 自身中位 2x 禁新建（商品錶）｜閘 4 訊號矛盾 → 「位置不明，觀望」｜**閘 5（v0.2）倍數 > 自身歷史高區（> 5Y 中位 ×1.5 / 貼破峰）禁新建——補 re-rate 型頂部盲區（商品硬閘為 peak-EPS 頂設計，量不到高 P/E 重估頂）**。

### B.3 兩軌對照 + 落欄（一至二句，v14.5）

投資軌（§14 長抱視角）= __；交易軌（本附錄位置）= __。{收斂 / 背離} + 一句。**底部背離（長抱視角迴避 + 循環位置深谷投降/早循環）是本鏡頭獨門訊號;頂部多收斂（皆遠離）。**（原型註:底部背離獨門價值只在「商品超賣但供需將反轉」時成立;capex/情緒循環與需求量/估值重估頂不必然產生該背離。）
**落 dd-meta（v14.5）**:寫 `cycle_position`（本標的位置）＋ `cycle_verdict`（右側可追蹤｜等回踩｜頂部觀望｜未觸發）。**接 §14 row 8b**:位置 ∈ {深谷投降,早循環} + B.2 五閘全過 + moat 底線 + 命中時獨立 critic 冷讀通過 → §14 落「進場·條件式（循環衛星）」（倉位上限 3%）;任一不成立 → 只落研究提名、§14 維持 row 8 觀望（cycle_verdict 記「等回踩/頂部觀望/未觸發」）。

### B.4 雙制度 / 無循環 sleeve 判別（如有，否則省略）

secular sleeve（如 HBM）= __（結構需求，不隨循環賣）；commodity/循環 sleeve = __（循環交易標的）。**若標的無真循環 sleeve（純成長 mis-route，如漏斗代理規則寬於 QC-42 商品定義而誤路由），此處註明並說明附錄 B 已降為「判別式演練」、不給交易訊號。**

> **倉位提醒**:交易姿態語言（trade_stance）為**投機軌交易輸入**，時間框架 = 循環（季-年）。**v14.5 起循環位置（cycle_position/cycle_verdict）落 dd-meta 並經 row 8b 接 §14**——但 row 8b 的循環衛星倉位上限 3%（軌別天花板）、實際組合佔比由 portfolio-manager 決定;命中 row 8b 強制獨立 critic 冷讀循環位置判定，驗證失敗只能降回觀望、不得升級（QC-42）。**未命中 row 8b（位置非底部 / 五閘未過 / critic 打回）時附錄 B 仍只是研究提名，§14 不進場。**

---

# §1｜投資結論詳述 + 頁首結論儀表板

> **顯示位置**:頁首結論儀表板在最頂部（不編號）;§1 投資結論詳述緊接其下，作為 Part I 第一章。兩者都在所有基本面/決策層分析完成後回頭寫。**人面對裁決完整陳述只在「頁首儀表板 + §14」兩處**（QC-37）。

## 頁首結論儀表板（不編號，最頂部）

合併舊 DD §1 dashboard + 舊 DCA Status Bar + 舊 DCA §2 一句話 thesis + 舊 DCA §7 裁決 headline。HTML 用 hypothesis-box 樣式（淺藍底 #EFF6FF，左 4px 線 #3B82F6）+ 上方一條 Status Bar grid。

**一行式 Status Bar（grid，6-7 格）+ 下方儀表板 bullet**，必含以下欄位（數字全部從對應章節複製，QC-7 一致）:

| 欄位 | 來源 | 顯示 |
|:---|:---|:---|
| **一句話 thesis（≤50 字）** | 敘事性，禁用財務指標當主體 | 超大字 28px 居中 |
| **統一裁決** | §14 裁決晶片 | 進場 #166534 / 觀望 #92400E / 迴避 #991B1B（白字 22px 粗體）|
| **倉位角色** | §14a `dca_role` | 核心/衛星/投機/條件式/不持有 |
| **護城河趨勢 ↑→↓** | §7 權威 moat_trend | 等級 S/A/B/C + 箭頭（↑ #166534 / → #64748B / ↓ #991B1B） |
| **Y5 後跑道 🟢🟡🔴** | §6.A'' runway_post_y5 | emoji + ≤12 字 |
| **Max DD −__%** | §13c 範圍下界 | ≥−30% 綠 / −30~−50% amber / <−50% 紅 |
| **5Y 機率加權 EV／IRR** | §11.5 | EV +__% 5Y ／ IRR __%/yr（爆發候選裁決時加註 AR __）**（單檔資訊，非排序貨幣;跨檔排序歸 GRP 三閘）** |

儀表板 bullet（hypothesis-box 內，承襲舊 DD 10 行 + DCA 決策層）:
```html
<div class="status-bar"><!-- 一行 grid：統一裁決 / 護城河趨勢 / Y5 後跑道 / Max DD / 5Y EV·IRR --></div>
<div class="hypothesis-box">
<p class="thesis">一句話 thesis（≤50 字敘事）</p>
<ul>
<li><strong>統一裁決 <span style="font-size:22px">進場 / 觀望 / 迴避</span></strong>（§14）｜倉位角色：__｜判定理由：__</li>
<li><strong>護城河趨勢 __ ↑/→/↓</strong>（§7 權威）｜execution 趨勢 __｜pricing power 趨勢 __</li>
<li><strong>Y5 後跑道 __（🟢/🟡/🔴）</strong>（§6.A''）｜S 曲線 __ ｜Y5 末滲透率 __%｜第二曲線 __</li>
<li><strong>Max DD −__%</strong>（§13c 範圍 −__~−__%，路徑風險 🟢/🟡/🔴）｜最快復原 __</li>
<li><strong>5Y 機率加權 EV +__%／IRR __%/yr</strong>（§11.5）｜Base IRR __%/yr（三分量 §11.6：EPS __ / re-rate __ / 股息回購 __）｜AR __（不對稱比;爆發候選裁決時必列）</li>
<li><strong>opportunity cost：</strong>__（§14a，點名同類現持倉，比較 R:R / conviction）</li>
<li><strong>基本面評級 __（A+/A/B/C/X，metadata）：</strong>品質 __/10｜估值燈 __｜Pure MA __｜陷阱定性 __（詳見附錄 A）</li>
<li><strong>長期持有信心：高/中/低</strong>（附錄 A I）｜建議持有年限：__（§14c）</li>
<li><strong>Inception DD：</strong><code>DD_{ticker}_YYYYMMDD.html</code>（YYYY-MM-DD）— 累積漂移對照基準</li>
<li><strong>下次年度對照倒數：</strong>YYYY-MM-DD（距今 N 天）— Inception + 365 天</li>
</ul>
</div>
<p class="note"><strong>讀法：</strong>本份報告的人面對結論是「統一裁決 進場/觀望/迴避」（§14）。基本面評級 A+/A/B/C/X 為 metadata（餵 screener），不是並列頭銜。倉位組合佔比由 portfolio-manager skill 依組合狀態決定。</p>
```

**Inception 判定規則**:生成前掃描 `docs/dd/DD_{ticker}_*.html` 找最早一份 schema v12.2+ 的報告;找到 → Inception = 那份日期;找不到（本份是第一份）→ Inception = 本份日期，標 `(本份為 Inception)`。一旦設定不變更。

## §1 投資結論詳述

**本節為一頁式摘要 + trap 終判，讓讀者一目了然。完整推理過程見各分析章節。** §1 頂部加一行:「本結論基於以下完整分析得出，詳見各章節;人面對裁決見 §14。」

### ⚠️ 這是價值陷阱嗎？（強制回答題）

**此節必須填寫，不得省略。**

| 問題 | 回答 |
|:---|:---|
| **最可能的價值陷阱模式是哪一種？** | 護城河侵蝕 / 盈餘品質 / 產業結構衰退 / 隱性資本密集 / 非陷阱 |
| **支持「這不是陷阱」的最強論據是什麼？** | （一段，須引用具體財務數字） |
| **支持「這可能是陷阱」的最強反駁是什麼？** | （一段，須誠實列出） |
| **空頭最強一擊** | 一句話:18 個月內造成 30%+ 虧損的最可能路徑 + 對應監測指標（引用 §3.C 的 R__;與 §13b pre-mortem 故事呼應） |
| **如何在持有期間判斷陷阱是否正在發生？** | 列出 1∼2 個領先指標與閾值 |

**最終定性**（必選一個，寫 dd-meta `trap`）：🟢 非陷阱 / 🟡 觀察期 / 🔴 高風險陷阱。

### 最關鍵監測指標

| # | 監測指標 | 對應章節 | 性質 | 觸發重新評估的閾值 |
|:---|:---|:---|:---|:---|
| 1 | __ | §3 H__ | 🔵 核心假設驗證信號（必填） | __ |
| 2 | __ | §6 / §7 | 🔵 長期成長領先信號（必填） | __ |
| 3 | __ | §11 / §4 | 短期估值或財報信號 | __ |

（與 §15 複審觸發呼應;§3.F Single Thing 為第 4 個監測點，在 §15 列出。）

---

## 【HTML 輸出協議】

完成所有章節後，**立即使用 Write 工具生成完整 HTML 報告檔案**，不得省略或延後。HTML 必須包含所有章節完整分析，不得摘要化。

### 視覺規格

- **配色**:主背景 #F8FAFC，卡片白底 #FFFFFF，章節標題深藍 #1E3A5F
- **字型**:Noto Sans TC（內文）+ IBM Plex Mono（數字/代碼），引用 Google Fonts
- **表格**:白底交替淺藍灰列（#F1F5F9），標題列深藍底（#1E3A5F）白字
- **章節標題**:深藍 #1E3A5F 底色，左側 4px accent 線（#3B82F6），h2 加 `scroll-margin-top: 80px`
- **頁首 Status Bar**:一行 grid（`display:flex; gap:12px; justify-content:center`），每格上方標籤 11px #64748B + 下方主體 22px 粗體;整條底色 #F1F5F9，左右各 4px accent 線 #3B82F6;任一格缺資料顯示「—」不砍格
- **Thesis 區塊**:超大字 28px 居中，底色 #EFF6FF
- **§14 Decision 區塊**:背景 進場 #F0FDF4 / 觀望 #FEF9C3 / 迴避 #FFF1F2;左 4px 線 進場 #166534 / 觀望 #92400E / 迴避 #991B1B;裁決晶片 inline-block padding 6px 20px border-radius 4px font-size 18px font-weight 700 + 左 4px 線;晶片副標籤 13px #475569 斜體
- **§12 矛盾區塊**:底色 #FFF7ED（淺橘），左 4px 線 #F97316;不可調和 🔴、可調和 🟡;強制裁決表用 #FED7AA 區隔
- **§13b Pre-mortem 區塊**:底色 #FEF2F2（淺紅警示），左 4px 線 #DC2626，narrative 引用框
- **§13c Max DD 區塊**:主數字 32px（`−45% ~ −55%`），下方 color bar 視覺化（0~−30 綠 / −30~−50 amber / <−50 紅）
- **§11.5 Pattern match / §11.6 IRR Composition**:底色 #F0F9FF（淺藍學習感），左 4px 線 #0EA5E9/#0284C7;IRR mini-table 3×4，分量年化 % 正綠負紅灰中性 + 下方橫向 stacked bar（綠 EPS + 藍 re-rate + 灰 股息回購）
- **價值陷阱警示區塊**:橘紅底 #FFF0E6，左 4px 線 #F97316，標題字 #C2410C
- **§3 核心假設區塊**:淺藍底 #EFF6FF，左 4px 線 #3B82F6
- **狀態標記**:Beat/符合 #DCFCE7 綠底 #166534 字;Miss/不符合 #FEE2E2 紅底 #991B1B 字;中性/待確認 #FEF9C3 黃底 #92400E 字;情境表 樂觀 #DCFCE7 / 中性 #FEF9C3 / 悲觀 #FEE2E2;估值訊號 🔴 #FEE2E2 / 🟡 #FEF9C3 / 🟢 #DCFCE7 / 🔵 #EFF6FF
- **整體風格**:金融研究報告質感，無圓角過度裝飾，線條簡潔，留白充足。**禁止**漸層背景、過重陰影、非專業裝飾。

### 章節顯示順序（HTML 呈現）

| 顯示位置 | 章節 | 說明 |
|:---|:---|:---|
| 0（最頂部） | 頁首結論儀表板 | Status Bar + thesis + 統一裁決 |
| 1 | §1 投資結論詳述 | trap 四問 + 最關鍵監測指標 |
| 2 | §2 序章 | 第一性原理 × 逆向 |
| 3 | §3 投資論點錨定 | 含 §3.F Single Thing |
| 4 | §4 即時財報情報 | |
| 4.5 | §4.5 隨附研究文獻 read-through | **條件性**:僅當有隨附外部文件才渲染 |
| 5 | §5 核心門檻檢核 | |
| 6 | §6 長期成長性 | 含 §6.A'' Y5 後跑道、§6.I 分部前瞻 |
| 7 | §7 護城河（報告核心） | 含權威 moat_trend、§7.F 對手 P&L |
| 8 | §8 財務品質監測 | 含 §8.E DuPont+營運資金 |
| 9 | §9 產業格局 | 含利潤池位置、§9.F 逐段 TAM/SAM |
| 10 | §10 治理與資本配置 | 含 §10.D 10Y track、§10.E FCF 去向 |
| 11 | §11 估值與報酬 | 11.1/11.2/11.4 + 11.5/11.6/11.7 |
| 12 | §12 矛盾辨識與強制裁決 | |
| 13 | §13 Pre-mortem 與 Max DD | |
| 14 | **§14 決策（`<section id="decision">`）** | **統一裁決唯一居所;research 頁定見欄連此錨點** |
| 15 | §15 複審觸發與保質期 | |
| 附錄 A | 擇時（降級） | Pure MA / R:R / 估值燈，折疊式（`<details>`，列印時展開） |
| 附錄 B | 循環交易讀數（條件性） | **僅 QC-43 判定循環子型才渲染（archetype 驅動）**;按子型選位置錶（商品/capex/需求量三選一）+ 循環位置 5 檔 + 交易姿態 + 反動能硬閘（含閘 5 倍數）,折疊式;明標投機;**v14.5:循環位置（cycle_position/cycle_verdict）落 dd-meta 並經 row 8b 接 §14;trade_stance 仍僅進 HTML**;成長股省略 |

### 功能規格

- 頁首固定:標的代碼 ｜ 資料抓取時間 ｜ 最新股價 ｜ DD Schema v14.5
- **版本一號到底（v14.0 起）**:frontmatter `version`、dd-meta `schema`、`<meta dd-schema-version>`、頁首字串、INDEX.md Schema 欄**全部一致（目前 = `v14.5`）**（沿用本 repo 歷史慣例:一個版號到底）。**下游相容**:validator（`^v1[234]\.\d+$`）、pre-commit floor（`"schema":"v1[34]`）、`aggregate_dca_stats` / `update_dd_index` / `dd_screener_dd_loader`（`startswith(("v13","v14"))`）已放寬接受 v13.x ∪ v14.x，既有 v13.0 報告照常運作，不需回溯重跑。**未來再升版時:bump 此 5 欄一致 + 放寬上述 6 個 pipeline 檢查多接受新版號。**
- **`<head>` 機讀標籤（全部必填）**:
  - `<meta charset="utf-8">` 之後緊接 `<meta name="robots" content="noindex,nofollow">`（私站防爬，research.investmquest.com noindex 政策）
  - `<meta name="dd-schema-version" content="v14.5">`（= frontmatter version，一號到底）
- **`<section id="decision">` 錨點**:§14 決策章節的 `<section>` 必須帶 `id="decision"`，h2 加 `scroll-margin-top: 80px`。research 頁「定見」欄 link 到 `/dd/DD_{ticker}_{date}.html#decision`，漏寫錨點 → 定見連結跳到頁首而非裁決。
- **目錄導覽列（強制）**:頁首之後緊接 `<nav class="dd-toc">`，含 anchor 連結指向各章節（§1 結論 / §2 序章 / §3 論點 / §4 財報 / §5 門檻 / §6 成長 / §7 護城河 / §8 財務 / §9 產業 / §10 治理 / §11 估值 / §12 矛盾 / §13 pre-mortem / §14 決策 / §15 複審 / 附錄 A 擇時）。pill-shape badges 樣式;每個 `<section>` 有對應 `id`;@media print 時 `.dd-toc` 隱藏。**禁止省略**。
- 右下角固定「列印為 PDF」按鈕（window.print()）
- @media print CSS:隱藏頁首與按鈕，附錄 A 折疊區全部展開，確保列印整潔
- 所有中文字型確保正常顯示

### dd-meta JSON 區塊（schema v14.5，HTML `<head>` 內，必填）

HTML `<head>` 內必須含 `<script id="dd-meta" type="application/json">{...}</script>`，schema `v14.5`，含 22 個 v12 必填欄 + 5 個 v13 必填欄 + 20 個選填欄（完整 schema + enum 見 QC-32）。**生成後跑 QC-32 自驗腳本 + `python3 scripts/validate_dd_meta.py --report` 確認全綠才 commit。** 關鍵對映:`dca_verdict` = §14 裁決晶片;`dca_role` = §14a 角色;`moat_trend` = §7 權威趨勢（單一箭頭）;`runway_post_y5` = §6.A'';`ev5y_pct` = §11.5 5Y 累積機率加權 EV%（非年化）;`irr_base_pct` = §11.5 Base IRR;`max_dd_pct` = §13c 範圍下界;`asym_ratio` = §11.5 不對稱比 AR（選填）。

### 輸出規格（Claude Code 本地環境）

- 檔名格式:`DD_[標的代碼]_[YYYYMMDD].html`（v13 統一報告，**不再產獨立 DCA_*.html**）
- 使用 Write 工具輸出至 `docs/dd/`
- **輸出完成後必須執行以下步驟，不得省略**:
  1. **生成後自驗**:跑 QC-32 自驗腳本 + `python3 scripts/validate_dd_meta.py --report`（確認 v13 五欄 + enum 全綠）;確認 `id="decision"` 錨點存在;確認 dca_verdict 三處（頁首/§14/dd-meta）一致。
  2. **更新 INDEX.md**:Edit append 一行到 `docs/dd/INDEX.md`，8 欄格式:`| YYYY-MM-DD | TICKER | {同 frontmatter version（現 v14.5）} | 統一裁決(進場/觀望/迴避) | 陷阱定性 | 護城河等級/估值燈/MA | DD_TICKER_YYYYMMDD.html | 備註 |`。第 4 欄為**統一裁決**（取自 §14;基本面評級 A+/A/B/C/X 不放此欄，已在 dd-meta `signal`）。備註限 3 句，每句 30-50 字，`<br>` 分隔（第 1 句 產業位置+品質;第 2 句 估值+護城河趨勢;第 3 句 關鍵判斷/觀察點）。
  3. **觸發網站同步**:執行 `python scripts/update_dd_index.py`（同步 research 頁主表 + dd-screener;v14.5 DD 報告由 script 直接讀 dd-meta 決策層欄位，定見欄連 `/dd/DD_X.html#decision`）。失敗則提示用戶手動執行，不得跳過。
  4. **terminal 摘要**（v14.5 格式）:
     ```
     ✅ v14.5 DD 報告完成:[TICKER]
     📄 檔案:docs/dd/DD_TICKER_YYYYMMDD.html
     💰 最新股價:$__
     🎯 統一裁決:[進場 / 觀望 / 迴避]（倉位角色:__）
     📊 基本面評級:[A+/A/B/C/X]（metadata）｜陷阱定性:[🟢/🟡/🔴]
     🛡️ 護城河趨勢:[↑/→/↓]（權威）｜Y5 後跑道:[🟢/🟡/🔴]｜Max DD:[−__%]
     📈 5Y EV:[+__%]／Base IRR:[__%/yr]（三分量:EPS __ / re-rate __ / 股息回購 __）
     💡 opportunity cost:__（點名同類現持倉）
     🔗 首頁同步:[✅ 成功 / ❌ 失敗,需手動 python scripts/update_dd_index.py]
     ```
     這是 terminal 允許輸出的**唯一**文字;章節內容仍嚴禁在對話框顯示。

### 防壓縮指令

**禁止以「節省篇幅」為由縮短 HTML 中任何章節內容。** 若單一 Write 無法容納全部，先輸出前半，說明「HTML 第一部分已生成，繼續生成第二部分...」，等用戶回「繼續」後以 Edit 追加。**寧可分段追加，絕不壓縮內容，也絕不改為文字輸出。**

### 最終自檢清單（HTML 輸出前內部靜默逐項自檢，不輸出）

```
□ 基本面研究只在 Part I 做一次,Part II 無另起 web search？
□ 頁首儀表板 + §14 裁決晶片 + dd-meta dca_verdict 三處進場/觀望/迴避完全一致？
□ §14 <section> 帶 id="decision" 錨點 + h2 scroll-margin-top？
□ dd-meta schema="v14.5" + <meta dd-schema-version v14.5>？
□ dd-meta 5 個 v13 必填欄全在（dca_verdict/dca_role/moat_trend/runway_post_y5/ev5y_pct）且 enum 合法？
□ moat_trend 單一箭頭 ↑/→/↓（非文字「持平」）且 §7 附 ≥1 個 12M sourced evidence？
□ runway_post_y5 ∈ {🟢,🟡,🔴}？判定引用滲透率推導或 sourced 第二曲線（v14.3 量化邊界）？若 🔴，§14c 反映「持有年限 ≤ 3Y 警示」+ §14 決策矩陣 Soft Veto？若 🟢，§11.5「10Y 二段延伸」已填？
□ §11.5 AR 已算（1 位小數）？若 §14 row 8a（爆發候選）命中：AR ≥ 4 且寫入 dd-meta asym_ratio、QC-48 獨立 critic 已跑且通過（失敗即降 row 8 觀望）、§14a 倉位上限 2-3%（dca_role = 衛星/投機，禁核心）、§14b 加碼列含 ≥1 條論點增強觸發、裁決晶片副標標「爆發候選」？
□ §14b 長抱賣出分軌：核心/爆發候選角色的清倉觸發全部 thesis 級（無「估值分位/漲幅/目標價」單獨清倉條款）？
□ ev5y_pct 是 5Y 累積 EV%（非年化 IRR）？來自 §11.5？
□ §11.6 IRR 三分量加總與 §11.5 機率加權 Base IRR 偏差 ≤ 2%p？
□ §13b：HTML 只呈現失敗故事 narrative；§3.F 校驗已於內部執行（若需修正已默默改 §3.F），**未把校驗 checklist / 「✅ 不需修正」/ Guardrail 對帳渲染進 HTML**（QC-40）？
□ QC-39：產業態勢**三軸**掃描已搜（A 競爭惡化 + B 結構 durability + C 其他結構變數/法規通路替代，各 ≥3 query 或開放問句）、三軸裁決一句已寫、閘 A（#1 在最大客戶份額↓→moat_trend 禁 ↑）與閘 B（循環股 bear/normalized 註明 durability 依據）已套用？
□ QC-40：全報告無「Guardrail：…✓」「校驗紀錄」「硬接線」「判定規則接線」「（必填）」「三處一致」「（QC-XX）」這類內部鷹架語言渲染成正文？
□ QC-41：若屬強制觸發範圍（強方向裁決/方向性 moat_trend/競爭動態·循環·法規敏感·B2B 集中型）→ 寫稿後最終 Write 前已 spawn 獨立 critic（不同 model instance）跑 4 軸紅隊；critic 的 🔴/🟡 findings 已實際回填修正章節（且未把「跑了 critic」過程渲染進 HTML，QC-40）？
□ §13c Max DD 為範圍（寬度 ≥ 10%p）；🔴 評級時依 F2 條件式處理（thesis 脆弱才砍倉，完整則只註記深回撤心理準備）+ max_dd_pct 寫 dd-meta？
□ §14a opportunity cost 具體點名 ≥ 1 個現有持倉同類股 + R:R/conviction 比較？
□ §15 保質期含明確日期（YYYY-MM-DD 或「下一次財報前」），非「長期有效」？
□ Part I 五個 v12.6 深度模組 + 七個量化表格全產出（QC-38）？Part I 佔比 ≥ 60%？
□ 檔案 ≥ 110KB（v13 hard floor）？< 110KB → 補上量化表格/決策模組深度,非拉長結論。
□ 凡引用 §X.Y 該節實際存在（v13 renumber 後無 dangling reference）？
□ §1 trap 四問填妥 + 空頭最強一擊（與 §13b 呼應）+ 最終定性寫 dd-meta trap？
□ QC-42（v14.5）：**QC-43 判定循環子型才觸發**附錄 B → B.0 已寫子型判別 + 選定位置錶（商品 6 訊號 / capex 6 訊號 / 需求量 5 訊號**其一**，非適用訊號標 N/A）、循環位置 + 交易姿態 + 反動能硬閘（**含閘 5 倍數 vs 自身歷史**）+ 兩軌對照、明標投機;**cycle_position/cycle_verdict 已落 dd-meta（trade_stance 仍僅 HTML）**;若循環位置 ∈ {深谷投降,早循環}+ 五閘全過 + moat 底線 → 命中 §14 row 8b（進場·條件式 循環衛星，倉位上限 3%），且**已強制 spawn 獨立 critic 冷讀循環位置、通過才升級（失敗降回 row 8 觀望）**;非循環股則附錄 B 整段省略不留佔位？
□ §14 row 4/5/8a/8b（v14.5）：row 4 MA ❌ 與 row 5 過熱皆只作進場節奏調節（未把裁決壓成觀望）;row 8a 估值 ∈ {🟠,🔴}（🔴 附 F2 紀律 + QC-48 冷讀通過）;循環股同時命中 row 4 與 8b 時由 8b 給頭銜、row 4 只調節節奏;Hard Veto（row 1-3）仍鎖死?
□ QC-49（v14.5）：若同 ticker 90 天內裁決翻面 → 已引用前次 §14b/§13 具體觸發器（編號+事件）已發火;引用不出 → 承繼前裁決並在 §12.3 記一句?
□ q.py 先讀後裁（v14.5）：Part II 動筆前已跑 `python knowledge/q.py {TICKER}`;若前次觀望/迴避且 to-date +30% → 錯過成本已入 §12.3 交叉矛盾且 §15 正面處理（非僅「估值更貴」）?
□ dd-meta（v14.5）：schema=v14.5;archetype 選填欄已填 primary（7 類 enum）;觀望裁決建議填 rearm_trigger;循環股 cycle_position/cycle_verdict 已填、非循環省略?
□ long_term_confidence：依附錄 A I 定義（moat 等級×moat_trend×runway×§13 證偽距離）判高/中/低，且與 QC-31 A 級條件一致?
□ QC-43~47：§0 已宣告 archetype（primary + secondary + 信心 + 證據，primary 落 dd-meta `archetype`）;若非品質複利，§5/§11/QC-31 已按路由換對應 gate-set（金融 QC-44 ROTCE/CET1/P-TBV｜未獲利 QC-45 Rule-of-40/NRR/EV-S 且 NI 負未誤觸發 X｜轉機·公用 QC-46 資產/DDM｜**EMS/ODM 第 7 類 ROIC+周轉+客戶集中+需求量週期+倍數均值回歸，非 FCF margin**）且明寫換了哪套;被取代的通用 PE/EPS/FCF tripwire 未重複機械套（QC-47）;支付網絡/資產輕金融科技未誤歸金融?
□ 跨檔比較（§14a opportunity cost）用 GRP 三閘語言，未以 5Y IRR 作跨檔排序依據（v14.5 GRP mandate）?
□ QC-40 機械 sweep（Write 前）已跑：正文無 `QC-\d`/`硬接線`/`（必填`/`寫入 dd-meta`/`三處一致`/章節標題 lineage 括注（「（DCA…移入）」）等鷹架洩漏（dd-meta JSON 區塊除外）?
```
自檢**內部靜默執行、不輸出逐條清單**。任一 ❌ → 回頭補完、重跑自檢，全部 ✅ 才能輸出 HTML;**僅允許一行偏差說明**（若有無法達標項，用一行「項 N 未達標:原因 ___」交代，其餘不輸出）。**禁止**:跳過自檢直接 Write;把 ❌ 偽報為 ✅;把逐條 ✅/❌ 清單渲染進對話框或 HTML。
