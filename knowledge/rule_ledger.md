# 判斷類規則登記簿（rule ledger）

**目的**：解決規則棘輪——「每次事故 +1 條、從不刪」堆十輪必淤泥化。每條**判斷類規則**（會影響裁決輸出的規則；純 sourcing/格式/防灌水規則不登記）在此登記：生日、觸發事故、**kill condition（什麼數據出現就該刪或降級）**、歷輪審計結果。**說不出 kill condition 的判斷類規則不准新增**（見 repo CLAUDE.md 規則治理條款）。

**審計節奏**：與裁決校準同步（下一輪 2026-10；方法＝grep 報告中的規則觸發標記 × settlement forward return）。審計結果三態：`KEEP`（有救援實績）/ `TIGHTEN|LOOSEN`（方向對但門檻偏）/ `KILL`（零救援或誤傷 > 救援）。

| 規則 | 生日 | 觸發事故（WHY） | Kill condition（出現即刪/降級） | 2026-10 審計 |
|---|---|---|---|---|
| §14 row 1-3 Hard Veto（X 訊號/矛盾未解/moat↓+≤B → 迴避） | v13 | 裁決紀律基石 | 被 veto 的名字連兩輪校準系統性跑贏（迴避組超額中位 > +10%） | — |
| §14 row 6/7/7a Soft Veto（C 訊號/runway🔴/估值依賴 → ≥觀望） | v13-v14.3 | 長抱 mandate 風控 | 同上，分 row 統計 | — |
| §14 row 8 估值燈基線（🟠/🔴 → 觀望）＋「取較嚴」 | v12 | 估值紀律 | 連兩輪「row 8 觀望組」超額顯著為正且 rearm 觸發率低（＝純粹擋住複利股） | — |
| 估值燈盲點 1 救援（高確信+PEG<2+AI🟢 → 🟠救🟡） | v12.x | 結構性成長股被分位錨誤傷 | 兩輪 0 觸發，或救援放行組超額為負 | — |
| 估值燈盲點 3 上修救援（FY1/FY2 3 個月上修 ≥+10% → 🟠救🟡） | v14.6 | DELL 型分母過時 miss（calibration_legacy_dca_20260707） | 救援放行組超額 < 0，或兩輪 0 觸發（門檻太嚴＝重蹈 AR≥4） | — |
| row 8a 26 週漲幅位置閘（<+100% 放行 / >+150% 擋） | v14.6 | AR≥4 實檔 0 命中死閘;回溯測試錯過組 ≤+101% vs 躲掉組 ≥+178% | 邊界帶（100-150%）誤判率 > 40%，或放行組超額 < 擋下組（＝閘方向反了） | — |
| row 8b 循環衛星五閘＋位置錶族（QC-42） | v14.5 | 三軌循環軌 0 檔可執行 | 8b 進場組兩輪超額為負;或反動能閘擋下的名字系統性續漲 | — |
| §11.5 反偏差防線（Bear ≥20-30% / Base ≤50%，凍結） | v12.x | 誠實機率紀律 | 兩輪校準顯示 Bear 地板系統性高估下行（實現 Bear 頻率 < 押注機率一半） | — |
| QC-48 爆發候選冷讀（downgrade-only;spawn 失敗即降觀望） | v14.3 | AR 分子自己估的，消費端驗證 | 打回組後續超額顯著為正（critic 系統性殺對的）;spawn 失敗降級誤傷 ≥2 例 | — |
| QC-49 裁決 hysteresis（90 天翻面須引觸發器）＋退役例外 | v14.5/v14.6 | 27% 相鄰複查翻面率＝方法論 churn;NOW 型殭屍觀望 | 承繼裁決 vs 反事實翻面的後續報酬差顯著為負（承繼在害人） | — |
| QC-50 錯過成本反向 critic（觀望的向上反駁通道） | v14.6 | 觀望棘輪：全部 critic 單向往下＋錯過尾 3× 躲掉尾 | 兩輪 0 次升級建議被採納，或升級組超額 < 0 | — |
| QC-51 同形狀 peer 裁決一致性對帳 | v14.6 | KLAC/AMAT/MU 同日三裁決無人對帳 | 兩輪從未觸發任何裁決修正或重審（＝純儀式）→ 降為選做 | — |
| QC-42 反動能硬閘（晚循環禁新建、倍數 vs 自身歷史等） | v14.1-v14.4 | 防在 blow-off 喊買 | 擋下的建立點兩輪後續報酬中位 > +20%（擋錯方向） | — |
| GRP R 閘單月 −2% 一票否決（scripts/engine/grp.py） | 2026-07-04 | 寧缺勿濫 mandate | 季檢記分板：被否決席位後續跑贏保留席位（owner＝GRP 季檢，非本 skill） | — |
| GRP G 閘成長門檻（FY1→FY3 EPS CAGR ≥15%；scripts/engine/grp.py） | 2026-07-04 | GRP mandate：發現力驗屍證明贏家先現於高成長×修正欄；門檻承自漏斗五條件閘 | 邊界帶（CAGR 10–15%）被擋組後續 12M 超額中位 > 放行組，連兩輪（門檻過嚴誤殺）；或全樣本 G 通過與否與後續超額無單調關係（成長軸無資訊量）→ 降門檻或降為排序因子 | — |
| GRP P 閘位置門檻（站上 52 週線＋未過熱；scripts/engine/grp.py） | 2026-07-04 | 與指數部同一條趨勢紀律：不接刀、不追 blow-off；避免另發明個股時鐘 | 兩半邊分開統計：「跌破 52 週線被擋組」或「過熱帶被擋組」任一組連兩輪超額中位 > 放行組（該半邊方向錯）→ 只降級錯的半邊，不整閘連坐 | — |
| ID conviction pill 公式（high 需 §9 ≥2 🔴 且 falsification >2σ;industry-analyst） | v2.x | conviction 機械化防灌 | high/mid/low 分級與後續籃子超額無單調關係連兩輪（偽精確無資訊量）;或單純 play 產業被公式壓 mid 的誤判 ≥3 例 | — |
| ID QC-6 T1 來源占比 ≥60% floor（industry-analyst） | v2.0 | 來源紀律 | macro 主題例外（floor 45%）落地後仍系統性卡稿;或 T1 占比與 ID 校準命中率無相關 | — |
| ID sd_verdict 三選一反騎牆＋split 出口（industry-analyst） | v2.5 | 反騎牆強迫裁決 | split 佔比連兩輪 >30%（出口被當變相騎牆用） | — |
| ID priced_in 落欄＋獵場鍵第四條件 priced_in ≠ high（industry-analyst v2.6） | 2026-07-08 | calibration_id：shortage×PhaseII 勝率 7/25，缺 priced-in 軸 | priced_in=high 的 shortage 籃子兩輪跑贏 priced_in=low（軸方向反了）;或兩輪全樣本 priced_in 與後續超額無相關 | — |
| QC-52 DD↔ID 對帳（事實先讀結論後對;sd_verdict 只當事實錨;Phase II 打折） | v14.8 (2026-07-08) | calibration_id_20260707：shortage×PhaseII 勝率 7/25 | Phase II 打折連兩輪無差別（ID 時鐘已修準）→ 移除打折 | — |
| v14.9 判斷反萃取三件套（§12.4b 三檢:分母爭議/證據 L1-L3/steelman;§13b' 成功但劣化;§11 多尺矛盾） | v14.9 (2026-07-08) | 強模型 override 動作固化（ORCL/SNOW/TSLA/MU 四原型），防弱底座退化成合規清單 | 兩輪校準顯示三檢/13b' 從未改變任何裁決（純儀式）→ 逐項降為選做;或被三檢改變的裁決後續超額更差（程序在幫倒忙） | — |
| QC-53 DD 情境判斷手冊（32 條，references/judgment-playbook.md）＋§14 四問＋§12 拓撲/三元歸因 | v14.10 (2026-07-08) | 18 份 DD 系統性挖掘（四 agent 去重），情境觸發式防注意力稀釋 | 逐條審計:觸發後從未改變裁決/倉位/觸發器的條目降選做或刪;整本兩輪零影響 → 廢除 QC-53 | — |
| ID 情境判斷手冊（20 條，industry-analyst references/judgment-playbook.md，Gate 14） | v2.7 (2026-07-08) | 5 份高密度 ID 反萃取（過剩改道/敗局劇本化/錯殺型分歧等） | 同上逐條審計制 | — |
| id-review V2-12~15（機器欄同步/熱產業時鐘施壓/kill 防呆/手冊實答抽查） | v1.6 (2026-07-08) | 守門員落後受檢對象三代＋校準教訓武器化（shortage×PhaseII 7/25） | 兩輪 critic 記錄顯示某條從未抓到任何 finding → 該條降選做;V2-13 若 ID 時鐘已修準（Phase II 失效格消失）→ 降級 | — |
| 對比判斷手冊（18 條，multi-stock-comparator references/judgment-playbook.md） | v1.9 (2026-07-08) | 6 份 MS 報告反萃取（對比特有邏輯:opportunity-cost 鏈/便宜法醫學/原版勝複製版等） | 同 playbook 逐條審計制（觸發後從未改變排序/推薦 → 降選做） | — |
| 供應鏈瓶頸兩層制（機械層＝替代難度×終端封鎖值 對帳 curated T0-T2;cartographer v1.1） | 2026-07-09 | 「最有價值最稀缺」缺跨鏈聚合＋小產業防偏誤（封鎖值用終端市場非節點規模） | 兩輪複審顯示機械提名 0 條被編輯層採納（純噪音）→ 機械段降為 console 輸出;或機械分與後續單點事件（斷供/認證突破）無相關 | — |
| macro §0 stance 三選一反騎牆＋§7 證偽表強制（macro-analyst v1.0） | 2026-07-08 | 生於短期轉折判死裁決後；防 macro 報告淪為不可證偽的騎牆散文 | stance 與後續 6M 風險資產實際方向連兩輪無相關（stance 無資訊量）→ 降為純敘事欄;或證偽表 kill metric 兩輪從未被查核（純儀式） | — |
| macro-analyst skill 本體（tool-level；描述器紀律＝禁擇時禁買賣指令） | 2026-07-08 | 系統缺總經深度研究層（描述器三頁只有資料層無敘事層） | 90 天內產出報告無任何 DD §11.5／ID／regime editorial／用戶決策討論實際引用 → skill 降級或砍（automatable ≠ valuable） | — |
| 宏觀投資時鐘機械層（G×I 兩軸七序列→象限，build_macro_clock.py，PREREG 凍結） | 2026-07-10 | 54 年雙窗驗證：唯一過時滯訊號＝滯脹象限傷股票（+0.7%／−2.2% vs 他象限 +8~14%）、次強＝過熱商品；四象限完整輪動不成立 | 下輪審計滯脹象限股票條件劣勢消失（時滯後滯脹股票 ≥ 他象限中位）→ 降回純編輯層；或機械針與編輯針連兩季同位（機械層零增量資訊）→ 擇一保留 | — |
| synthesis 退出分軌（長抱倉技術項降警訊、清倉只認 thesis 級；expectations-synthesis §退出） | 2026-07 (v1.1) | 動能紀律會把多倍長抱倉在半山腰（−40~60%回撤／跌破200MA／整年共識下修）洗下車，與 DD F2「不因波動砍倉」矛盾 | 長抱倉因分軌而未減碼、其後 thesis 級證偽命中且回撤 > 動能紀律版的案例 ≥2 → 收緊（分軌放太寬＝變不賣的藉口） | — |
| priced_in=high 上行閘（機器欄先讀：priced_in=high 且答不出未定價向量 → §Δ 不得偏多；expectations-synthesis Step 4） | 2026-07 (v1.1) | calibration_id：shortage×PhaseII 唯一系統性失效格；物理短缺為真但股價已 price 時偏多判讀最易默默失效 | 閘擋下的偏多判讀，3 個月後方向實證為對的比例 > 60% → 降級為警語（閘系統性壓對的偏多＝過嚴） | — |
| 賣方料等級聲明（格式類但影響判讀權重：等級 C 降 §6 深度可信度；expectations-synthesis 硬規則 12） | 2026-07 (v1.1) | AMD 教訓：公開報導被包裝成「賣方對照」誇大料源深度，讀者高估 §6 權重 | 等級 C 報告的方向命中率（synthesis_ledger）與等級 A 無差異 ≥2 輪（料源等級對判讀品質無資訊量）→ 簡化為腳注 | — |
| 衛星席時機路由＝cyclical-track 位置閘（核心席仍走 sop-funnel 板機；低熱名單外衛星席顯性標「未覆蓋」不猜；/cockpit/ 陣容表） | 2026-07-11 | sop population 品質閘系統性排除爆發/循環型（COHR 不在 25 檔 population）＝衛星席時機層無板機覆蓋，QC-42 mandate gap 在時機層重演 | 循環衛星按此閘執行的樣本連兩輪超額 < 0；或位置閘連續兩季令衛星席「有名單無時機」僵死（可執行時機 0 次）；或「未覆蓋」的結構型衛星（如 COHR）漏掉的時機事後顯著優於閘內樣本（＝該補結構型閘而非留白） | — |
| 正不對稱三級標記（◆ 好球帶／★★／★；描述器類，`build_dd_screener.py::compute_asym_flag`，注入 /research/＋/dd-screener/）。門檻：◆＝AR_live≥9 且 liveIRR≥13% 且 trap🟢 且 moat≠↓ 且裁決＝進場 且齡≤90 天；★★＝AR_live≥6 且 liveIRR≥12% 且 trap🟢 且 moat≠↓；★＝AR_live≥4 且 liveIRR≥10% 且 trap≠🔴 且 moat≠↓。**PREREG 凍結至 2026-10** | 2026-07-12 | AR≥4 資格閘 v14.6 被殺的教訓＝閘不可證偽（沒人知道它擋掉的名字後來怎樣，安穩活三個月）。本標記刻意設計為**描述器**（非閘、不改裁決）＋**現價驅動**（隨股價漂移重算）＋**可證偽**（亮燈組可對帳 forward return），是教條的反面 | ◆ 亮燈組 12M forward return 未跑贏「非◆的進場組」，或 ◆ 組出現一檔 thesis 級虧損 → 驗屍防呆（收緊 ◆ 門檻）或直接刪 ◆ 級；★★/★ 兩級與後續超額無單調關係連兩輪 → 併級或降為純資訊註記 | — |
| detective 複合規則 R1 股高位×信用背離×廣度走弱（`detective_rules.py`；紅、min_true 3、confirm 2；composite:R1 進狀態機） | 2026-07-15 | detective v2 Phase 3：單指標警報網缺跨指標聯合條件層，指數高位但信用與廣度未確認的內部背離需多訊號同現才捕捉 | fire 後 20 交易日對應資產回撤中位不劣於未 fire 基準，連兩輪審計 → 刪或降黃 | — |
| detective 複合規則 R2 波動結構三件套（`detective_rules.py`；2/3 黃 3/3 紅、min_true 2、confirm 1） | 2026-07-15 | detective v2 Phase 3：選擇權尾部／波動加速定價需 VIX 期限×偏斜×VVIX 同時偏貴才成立，單項高位噪音大 | fire 後 20 交易日對應資產回撤中位不劣於未 fire 基準，連兩輪審計 → 刪或降黃 | — |
| detective 複合規則 R3 流動性三管收縮（`detective_rules.py`；黃、min_true 3、confirm 1；連 5 日走 sustained 升級） | 2026-07-15 | detective v2 Phase 3：準備金邊際趨緊須準備金×TGA×SOFR-IORB 三管同向，單管易被季節性雜訊誤判 | fire 與後續 NFCI 走向無相關，連兩輪 → 刪 | — |
| detective 複合規則 R4 信用內部裂縫（`detective_rules.py`；紅、min_true 3、confirm 2） | 2026-07-15 | detective v2 Phase 3：低評級端裂縫須 CCC 擴×IG 按兵不動×HY/IG 走弱同現，捕捉尚未擴散至投資級的早期壓力 | fire 後 HY OAS 20 日續闊比率 <50%，連兩輪 → 降黃 | — |
| detective 複合規則 R5 避險同框（`detective_rules.py`；黃、min_true 3、confirm 1） | 2026-07-15 | detective v2 Phase 3：跨資產避險須黃金×美元×實質殖利率同日同向，單一資產走強常是特異因素非系統避險 | 兩輪 0 fire 或與跨資產後續波動無關 → 刪 | — |
| detective 複合規則 R6 擁擠×動能翻轉（`detective_rules.py`；黃、min_true 2、confirm 1；COT↔rotation join、對不上市場不評估） | 2026-07-15 | detective v2 Phase 3：擁擠部位與價格動能背離須 COT 5 年分位極端×同資產輪動轉弱 join，單看擁擠無 unwind 觸發訊號 | fire 資產 20 日回撤中位不劣於未 fire 極端 → 刪 | — |
| detective 複合規則 R7 窄領導（`detective_rules.py`；黃、min_true 2、confirm 2；subgroup 三取二） | 2026-07-15 | detective v2 Phase 3：少數權值撐盤須指數高位×｛小型／區域銀行／運輸｝三取二走弱，單一廣度比噪音大 | fire 後 20 交易日對應資產回撤中位不劣於未 fire 基準，連兩輪審計 → 刪或降黃 | — |
| detective 複合規則 R8 晚週期滯脹組合（`detective_rules.py`；黃、min_true 3、confirm 1；macro_clock 象限閘） | 2026-07-15 | detective v2 Phase 3：晚週期＋通膨黏性須時鐘象限×銅金比走弱×通膨預期偏高同現；承接宏觀時鐘滯脹象限傷股票的驗證 | 滯脹象限條件劣勢在時鐘審計消失 → 連動降級 | — |
| detective 複合規則 R9 自滿組合（`detective_rules.py`；黃、min_true 3、confirm 1；pc_equity〔internals〕分位≤5×SKEW 分位≥90×VIX 分位≤10；status dormant→active） | 2026-07-16 | options 資料層（internals.json pc_equity，309 交易日 backfill）上線後啟用 Phase 3 預留的自滿組合——選擇權與波動面同時反映極度自滿須三面同現才成立，單面低分位噪音大 | fire 後 20 交易日 SPX 回撤中位不劣於未 fire 基準，連兩輪審計 → 刪或降黃 | — |
| PM-QC-2 長抱賣出分軌（portfolio-manager v2.0；清倉建議必須指名 thesis 級觸發物，估值偏高/漲幅本身最多 trim 回目標倉、永不單獨清倉） | 2026-07-17 | v1.0 機械超漲止盈（>mid_target×1.2 → 減碼 30%）退役；calibration_legacy_dca_20260707 實證強勢段機械保守成本 ≈ 3× 其收益 | 兩輪校準顯示「thesis 級觸發前若機械止盈可保住的回吐」規模中位 > 「續抱多賺」（＝機械止盈其實在救人）；或 thesis 級觸發系統性太慢（觸發時已回吐超過機械止盈保住額的 2×）→ 恢復分級止盈 | — |
| PM-QC-1 direction override 禁止（portfolio-manager v2.0；PM 不得反 §14 裁決，L4 唯一出路＝重跑 DD；L1-L3 sizing/horizon/information 允許但強制 reversal condition） | 2026-07-17 | v1.0 override 4 級協議繼承；分工純粹（PM 不做單股研究）防組合層情緒繞過裁決鏈 | 出現 ≥3 例「新資訊明確、重跑 DD 的延遲造成實質錯失、且 L3 資訊通道未能補位」→ 開 PM 層條件式 direction override（附強制事後 DD 對帳）；或兩輪 L4 攔下的意圖事後全部正確（禁令在害人） | — |

| ID 研究引擎三件套（industry-analyst v3.0 Gate 15：五軸 fan-out〔含 Axis E 替代/圈外〕＋承重數字 3-skeptic 對抗查證＋completeness critic；僅新 ID／裁決級 refresh，措辭級免） | v3.0 (2026-07-20) | AIInferenceEconomics 整份漏中國 open-weight（寫手與自己 checklist 共享盲點，缺席偵測需獨立腦）；Kimi K3 案例證明承重數字第一印象方向會錯（開源便宜 vs 2.8T 硬體地板） | 逐件審計：兩輪內 completeness critic 零「補研究後改變 debate/裁決」實績 → critic 降選做；對抗查證兩輪內零「數字被 ≥2 票反駁且除名後影響結論」→ 降為抽查制；Axis E 兩輪掃描全部「無一階威脅」且無一次事後被打臉 → 降為 checklist 項 | — |
| ID 替代威脅 debate 席（industry-analyst v3.0 Gate 16：debates ≥1 張圈外/替代威脅卡，「已掃描無威脅＋判別訊號」為合法結論） | v3.0 (2026-07-20) | 同上中國模型盲點；結構保留席＝把「搜尋義務」變成版面必填格，成本最低的 forcing function | 兩輪校準內威脅卡全部流於「無威脅」樣板且無任一判別訊號後續被觸發 → 降為 Axis E 附屬輸出、撤 gate | — |

**登記規則**：新增判斷類規則 → 加一列（含 kill condition）＋提名一條既有規則候刪（寫進 PR/commit 訊息）；刪除規則 → 該列標 `KILLED @ 版本`（保留供 lineage，勿刪行）；每輪校準把審計結果回填最後一欄。

## 思考訓練工具使用對帳（2026-07-08 起）

工具比照判斷類規則治理：**不可證偽的存在就是膨脹**。下列 wiki 訓練介面各登記使用型 kill condition，審計日 **2026-08-07**（上線滿 30 天）；審計數據源＝道場「⬇ 備份全部訓練紀錄」匯出的 localStorage 統計＋`vault/notes/` 匯出筆記數。

| 工具 | 生日 | Kill condition（30 天審計） | 2026-08-07 審計 |
|---|---|---|---|
| wiki/munger.html 蒙格清單 | 2026-07-07 | 匯出筆記（notes/munger/）＝0 且無任一 ticker 有已存答案 → 砍或併入 gym | — |
| wiki/dojo.html 道場（盲測/對決/殺手） | 2026-07-07 | 盲測題數 < 20 → 砍掉低使用 mode，只留有人玩的 | — |
| wiki/gym.html 對照室＋時光機＋寫作間 | 2026-07-07 | 各 tab 產出（2×2 自評數/匯出數）＝0 → 逐 tab 砍 | — |
| wiki/gym.html 異常狩獵（用戶票選） | 2026-07-08 | 認領數 < 5 或對帳判定數 = 0（只認領不對帳＝評論家模式）→ 降級回靜態榜 | — |
| q.py --inbox / --falsifiers 回寫迴路 | 2026-07-08 | falsifiers.json 30 天後仍 0 條 → 回寫迴路失敗，重新設計而非硬推 | — |
| munger-mind 蒙格腦（定位＝掛蒙格清單的紅隊，非蒙格複製；語料薄／二手卡／出處洗白三風險已知） | 2026-07-08 | 30 天內對質報告無任何一條進入實際決策參考 → 降級為純語料檢索、撤第三隻錨席位。正面樣本 ×2：META（治理假說重安放進 pre-mortem）、NVDA（歷史倍數錨失效＋四傾向共振警報，用戶認可） | — |
