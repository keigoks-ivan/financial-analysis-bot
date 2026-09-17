# 席位引擎 v4（2026-09-17）

## 為什麼要改

10 週對照組（7/4→9/17）：核心席 −3.8%、核心＋衛星 −8.4%，同期 SPY +1.2%；首批 buy&hold
組反而 +1.0%。10 週內 23 檔坐過 10 席——換手率遠高於「長抱倉」的定位。回頭看，週遲滯
（新席連 2 次過閘、現任連 4 次不過才下）在保護的是雜訊，不是訊號：一週的漲跌、一週的
上修雜音，都能讓席位換手。同時三月上修比 FY+1 單月更抗雜訊，過熱與頂點被混在同一個
「位置閘」裡也不對——過熱是短線動能滿檔該讓時機燈接手，頂點（賺得比五年均值快）其實
是健康訊號，NVDA、CLS 兩檔都頂點、卻穩居核心候選前 5，混在一起會誤殺好公司。

## 改了什麼

1. **成長閘**：三年期 Koyfin CAGR 仍是硬性必備，門檻 15%，但耐久（durable_5y）者放寬到
   10%——複利股基期已高，成長本該慢下來。
2. **上修否決**：改看三個月（FY 加權 0.2/0.3/0.5）EPS 上修 ≤ −5% 才否決，取代原本 FY+1
   單月 ≤ −10%；後者只在前者缺值時當備援。
3. **過熱／頂點分開**：過熱（12-1 個月動能 >150%，缺值退回 26 週漲幅 >80%）不再是資格
   閘，只排除核心候選（照樣能坐衛星）；頂點（roic_vs_5y_x ≥1.3）純顯示，不影響核心候選
   資格。
4. **排序**：own_score 改五個排名百分位（三月上修、12-1 月動能、成長封頂 30、品質、盈餘
   殖利率）在合格集合內互相比較後平均，需 ≥4/5 有值。品質＝FCF÷淨利與稀釋率百分位平均，
   但增量 ROIC ≥15%（投資有回報）的名字免計 FCF÷淨利。舊 own_score（v2 公式）保留一輪
   對照，存在 `own_v2`。
5. **新增硬否決**：體質淨評級「拒絕」、衰退燈號「⛔」、DD 迴避（180 天內）——後者是重新
   打開（9/16 曾關閉迴避否決，一天後這裡再打開，兩份拍板時間點都留在 commit 歷史）。
6. **無產業集中度上限**（持有人拍板：席位本來就沒幾席，硬性上限只會逼著湊數）。
7. **月頻輪動**取代週遲滯：每月第一次 `--ledger` 跑整批重選一次；期間只有六項硬否決
   （迴避／拒絕／⛔／三月上修 ≤−5／市值不足／連兩週跌破 52 週線）能讓現任下席，其餘軟性
   資格失守（比如成長掉出門檻）都先沿用到下個月，空位由下一名遞補。
8. **時機燈**（新）：把位置、RS、200 日線、階段收斂成一個燈號＋倉位建議——🟢可進·正常倉／
   🟡半倉／🟠過熱·半倉／🔴等板機·零倉／⚫不合格。這是週頻判斷，跟月頻的「值不值得擁有」
   刻意分開：CLS 耐久、不過熱，穩居核心候選，但距高 −31%、RS 33、跌破 200 日線，時機燈是
   紅的——核心席不代表現在該買，時機燈才回答這個問題。

## 陣容（本次跑，未帶 `--ledger`，即預覽）

| 席 | 核心 | 衛星 |
|---|---|---|
| 排名 | NVDA・LRCX・MRK・ASML・JBL | MU・WDC・DELL・STX・AMAT |

與持有人模擬預期的核心（NVDA／ASML／LRCX／CLS／MRK）有 4/5 重疊，JBL（排名分 63.5、
第 11 名）擠進第 5 席，CLS（61.7、第 13 名）差距僅 1.8 分——逐檔查過 pass／overheated／
durable 全部一致，是百分位排序的邊際差距，不是資格判定錯誤（原因：`fcf_ni_ratio` 這個
排序輸入原本沒有從 `compute_fundamental_gates()` 曝出去，本輪一併補上；補上前 JBL/CAT
排名更靠前，補上後 CLS 已回升到緊貼第 5 名）。衛星 5 席與模擬預期完全同組（僅順序不同）。
CLS 的時機燈驗證：🔴 等板機／零倉，why=「距高點 -31.5%、RS 33、vs 200 日線 -1.5%」，與
持有人給的驗收數字（距高 31%、RS 33、跌破 200 日線）逐項吻合。

## 證偽條件（12-10 月校準輪查核）

12 週席位中位報酬落後 SPY ≥5 個百分點、連兩次月度輪動 → 檢討排序公式或月頻節奏；
或月換手 > 5 檔連兩月 → 硬否決條件過鬆，收緊；或頂點不排除核心候選這條，若下一輪校準
顯示頂點組系統性跑輸非頂點核心組 ≥2 次 → 恢復「頂點排除核心候選」。

## 沒做/未驗證

品質×時機矩陣的警訊點只加在 imq-badge.js 前端顯示層，未回填任何既有清單或分數；
`_arena_body.html`（M5 對照組擂台頁）文案已同步更新到 v4 措辭，但欄位結構（核心表／
衛星表／擂台對戰表）本身沒有照 Step 3 新欄序重做——那張表是既有的「擂台」視角，
新欄序只落在 `_board_body.html`／`board.txt`。

## v4.1 追加（2026-09-17，同日第二輪）

Koyfin watchlist 同日再加兩欄（融券占流通股比、內部人淨買賣 3M），順勢把 DD 技能既有的
三條 DD-free 機械規則搬進引擎——皆非新創判準，登記見 `knowledge/rule_ledger.md`
「v4.1 融券比 >10% 只能衛星」與「v4.1 基期效應＋循環股守門」兩列。

**改了什麼**：

1. **融券高不是排序因子**：原規劃是把融券比當 own_score 第六個排名百分位，持有人拍板
   改向——高融券預測低報酬的學術證據集中在尾巴（>10-20% 流通股），大型優質股母體內
   1-3% 的差異是雜訊，硬塞進排序只會加雜訊。改為比照 `overheated` 的待遇：
   `short_interest_pct_float > 10` → `high_short_interest=True`，只排除核心候選資格
   （衛星照樣能坐），不進 `own_score_v4()` 排序、不是資格閘（`grp.grp_score()`／
   `build_arena.row_dict()` 的 `core_candidate`）。內部人買賣（`insider_net_buy_3m`／
   `insider_signal`）從頭到尾只是席位表的備註 badge，沒有考慮過進排序。
2. **基期效應**（`grp._base_effect_growth()`）：Koyfin 三年 FY1→FY3 CAGR 用幾何平均，
   若 FY1→FY2 因低基期跳增會把整段拉得虛高，蓋掉 FY2→FY3 才是穩態的事實。f1/f2/f3
   （`eps_fy_curr`/`eps_fy_next`/`eps_fy3`）皆為正值時，FY2/FY1 > 1.6x 且 FY2→FY3
   成長 < 20% → 改用 FY2→FY3 成長率取代，同時作用於成長閘（`grp_score` 的 `g`）與
   排序鍵（`own_raw` 的 `g`）；改用的仍是三年期 Koyfin 資料，不影響 `g_three_year`
   判定（不是退回單年 fallback）。
3. **循環股守門**（`own_raw()`／`own_score_v4()`）：毛利率（LTM/FY-1/FY-2/FY-3，需
   ≥3 點）跨距 >20pp 或資本支出佔營收 >15% → `cyclical`；`cyclical` 且 PEG（`live_peg`
   優先，fallback `peg`）<0.3 → `cycle_guard=True`——循環股在景氣高點常同時出現「爆量
   成長」與「PEG 低到可疑」，觸發時成長分位（`p_g`）與盈餘殖利率分位（`p_ey`）封頂
   50 再平均。`cyclical` 本身即使未觸發 guard 也照樣回傳，供純顯示用的「循環」備註。

**實測數字（依據，見 rule_ledger 對應列）**：MRK（2.75→9.55→10.62）三年 CAGR 幾何平均
虛高，FY2→FY3 只有 +11.2%，基期校正後 g≈11.2%，只能靠 durable 10% 放寬過關；MU
（73.4→156.3→171.6）FY2→FY3 只有 +9.8%，校正後直接跌出成長閘（15% 門檻）；NVDA
（9.31→15.61→21.06，FY2→FY3 +34.9% ≥20%）未觸發，證明門檻方向正確——basis 是
「FY2→FY3 是否夠快」而非「FY1→FY2 是否夠快」。

**陣容（本次跑，未帶 `--ledger`，即預覽；模擬預期：核心 NVDA／LRCX／ASML／JBL／CAT，
衛星 WDC／DELL／STX／AMAT／TER，TSM ≈ 第 12 名、CLS ≈ 第 14 名、MRK ≈ 第 21 名、MU
不合格）**：實跑結果見任務報告（本檔僅記錄規則設計，逐檔數字與模擬預期的差異已在
報告內逐一核對）。

**證偽條件**：融券高組（衛星席）12 週中位報酬 ≥ 未標記席位連兩次月度輪動 → 撤回融券
旗標；基期校正組後續 12 個月 FY2→FY3 實際成長顯著優於校正值連兩輪 → 撤回基期效應、
復歸原始三年 CAGR；循環守門組 12 週中位報酬 ≥ 未觸發組連兩輪 → 撤回封頂邏輯。

**沒做/未驗證**：三條規則皆為 DD 技能既有機械規則的移植，未額外做獨立回測（回測依據
是任務給定的實際三檔數字，非樣本內外分離的統計檢定）；循環股守門的 PEG<0.3 門檻與
毛利跨距/資本支出雙路徑判準沿用 DD 技能既有數字，未在本引擎脈絡重新校準。

## 時機燈日更（2026-09-17）

**問題**：cockpit 席位表的時機燈（→倉位動作）原料——dd-screener `timing.*`／`ma.*`、
`docs/stages/data/lamp.json`——本來就每天跟著 `daily-taipei-morning.yml` 更新，但只有
`weekly-engine.yml` 的 `build_arena.py --ledger` 跑次會讀進來重算燈號，燈最多落後 6 天，
跟原料的更新頻率脫節。月頻輪動（值不值得擁有）跟時機燈（現在能不能買）本來就是刻意
分開的兩層判斷（見上「改了什麼」第 8 點），只是「讀」的頻率一直沒補上。

**改法**：`build_arena.py` 新增 `--lamp-only` 唯讀旗標——讀 `arena-ledger.json` 的
`roster`（缺則退回 `arena.json` 現有 `core_seats`／`sat_seats`）決定要刷新哪些席位／
候補，對每檔重讀 dd-screener／QGM 最新 `ma`／`timing` 與 `lamp.json` 階段，借用既有
`grp_score()` 的位置閘與 `timing_lamp()` 重算 P 閘欄位（`above_w52`／`p_label`／
`dist_hi`／`price`／`overheated`）與燈號／倉位，只覆寫這些欄位＋新增
`lamp_as_of`／`lamp_source`／`lamp_last_rotation_date` 三個戳記，`own_score`／排名／
席位組成一律原樣保留、不重算、不寫 `arena-ledger.json`。`board.txt`／
`_board_body.html` 只原地替換「目前席位」區塊（`_seat_section_lines()`／
`_seat_section_html()`，抽成獨立函式供全量重建與唯讀刷新共用同一份格式），全母體表／
DD 對照／候選佇列維持上次 `--ledger` 跑次內容不變。任何輸入缺失（`arena.json`／
`arena-ledger.json` 皆讀不到）一律印 warning、`exit 0`，不擋排程。掛進
`daily-taipei-morning.yml`（實際排程跑班次）與 `daily-non-fundamental-refresh.yml`
（已停用排程，僅手動 dispatch，同步加這步保持一致）Step 1 之後。

**驗證**：對真實資料跑 `--lamp-only`，因當天輸入未變，15 檔席位/候補燈號逐一比對
前後完全一致；`arena.json` 的 `core_seats`/`sat_seats`/`bench_seats` 除
`lamp`/`action`/`r26`/`r52`/`grp.above_w52`/`grp.p_label`/`grp.dist_hi`/
`grp.price`/`grp.overheated` 外零欄位差異，`own_board`/`duels`/`rotation`/
`concentration` 等其餘欄位逐位元組相同；`arena-ledger.json` md5／mtime 皆未變。
`board.txt`／`_board_body.html` 只有「目前席位」區塊新增兩行新鮮度戳記＋DOWN
異動列原因退化成「不在母體」（因唯讀模式不重建全母體 `rows`，此為刻意降級，
待下次 `--ledger` 跑次自然恢復完整原因），其餘全母體表／DD 對照／候選佇列
逐位元組相同。

**沒做/未驗證**：目前 repo 內 `arena-ledger.json` 尚未跑過 v4 `--ledger`（`roster`
仍是 `None`，最近一筆 snapshot 是 2026-09-12 的 v3 陣容），`--lamp-only` 因此走的是
「退回 `arena.json` 現有席位」那條 fallback 路徑——`roster` 非空時的主路徑要等下次
`weekly-engine.yml --ledger` 跑過後才有真實資料可驗；DOWN 列因唯讀模式拿不到全母體
`rows` 而降級成「不在母體」的行為只在這次的資料錯位下被觸發到，正常狀態（ledger 與
`arena.json` 同步）下 DOWN 列理論上應為空，未在乾淨狀態下驗證過。

## 財報錨定上修（2026-09-17）

**問題**：`eps_rev_3m_pct`（`build_dd_screener.py::_compute_eps_rev_3m`）拿今天的
共識跟 ~90 天前的月度 baseline snapshot 比——是一個「日曆錨」，對報告日期分散的
母體不公平：7 月初就發財報的名字，上修動能一個月後就因為日曆理由過期出窗；還沒
發財報的名字反而卡在接近零，兩者不是同一把尺。

**改法**：每檔改認自己的財報日，不認共用的日曆窗。

1. **每檔財報日曆**——`get_earnings_calendar()`（`build_dd_screener.py`）用
   `yf.Ticker(t).get_earnings_dates(limit=12)` 一次拿到最近一次已公布財報日
   （`last_earnings_date`，篩 `Reported EPS` 非空）與下次財報日（`next_earnings_date`，
   最近一筆未來列），持久快取在新檔 `data/earnings_calendar_cache.json`（3 天內不
   重抓，同一 ticker/yf_ticker 鍵，thread-safe，同 `eps_fx_normalize.py` reporting-
   currency cache 的寫法）。查過 repo 既有的財報日來源：`data/flowmap_earnings_cache.json`
   （`build_flowmap.py`）只覆蓋 SP100 前 100 大市值、只存 next_earnings_date，缺
   ASML/TER/JBL/CLS/CAH/DELL/STX 等中小型 DD 名字且沒有 last_earnings_date；
   `dd_numbers_extra.py::compute_price_and_earnings_recency()` 與
   `build_momentum5.py` 的 `report_date` 欄用同一套 `get_earnings_dates()` 手法但
   都是單檔即時查、無持久快取——沿用同一手法、新建一個涵蓋全 DD-screener 母體的
   持久快取，而非硬套現成但覆蓋不足的快取。
2. **baseline picker**——`pick_strictly_before_baseline()`（純函式）在
   `docs/dd-screener/eps-estimates-snapshots/*.json` 的**canonical 月度快照**
   （`{YYYY-MM}.json`，不含 intra-month `{YYYY-MM}-DD.json`，與既有
   `_load_eps_rev_3m_baseline()`/`_load_eps_fy1_baselines()` 同一慣例）中，挑
   snapshot_date **嚴格早於**該檔 `last_earnings_date` 的最新一筆——「財報前市場
   怎麼看」而非「財報後已經反映修正的市場怎麼看」。查無合格快照（尚未進入本輪
   財報季、或所有快照都晚於財報日）回傳 `None`，呼叫端退回 `eps_rev_3m_pct`。
3. **算法**——`_compute_eps_rev_since_earnings()` 拿到 baseline 後，逐字重用
   `_compute_fy_eps_revision()`（ADR 換算＋FX 正規化）與新抽出的
   `_fold_eps_rev_fy_weighted()`（0.2/0.3/0.5 FY 加權，从 `_compute_eps_rev_3m()`
   拆出來給兩邊共用，不重寫 FX/ADR 邏輯）。輸出 `eps_rev_since_earnings_pct` /
   `eps_rev_since_earnings_baseline_date` / `eps_rev_anchor`
   （`"earnings"|"calendar_3m"`）/ `eps_rev_since_earnings_days`（基準快照日距今
   天數，退回三個月時仍算，反映該退回值本身有多舊）。`eps_rev_3m_pct` 本身不動、
   繼續保留供對照（見 `enrich_ticker()` 呼叫處）。
4. **席位引擎**——`grp._revision_anchor()`（新函式）統一決定 `own_raw()` 的 `rev`
   欄與 `grp_score()` 的上修否決要用哪個值：`eps_rev_since_earnings_pct` 優先，
   缺值退回 `eps_rev_3m_pct`（第二層 fallback，只在極舊快照或手測 fixture 完全沒有
   新欄位時才會用到——screener 本身已經把「查無財報錨定」的情況折算進
   `eps_rev_since_earnings_pct`）。`grp_score()` 回傳新增 `rev_used_pct` /
   `rev_anchor` / `rev_baseline_date` / `days_to_next_earnings` 四個欄位供
   `build_arena.py` 渲染。`EPS_REV_3M_VETO=-5.0` 否決線本身不動。
5. **顯示層**——`build_arena.py` 的席位表欄位「三月上修%」改標「財報後上修%」
   （tooltip 標基準快照日＋錨定方式），新增「下次財報」欄（天數，≤7 天橘色 pill
   標記——分數是財報前快照）；board.txt legend、`_arena_body.html` 擂台頁說明、
   `arena.json` 的 `method` 字串同步改文案。`docs/dd-screener/index.html` 的
   「成長」欄 CAGR tooltip（`_renderLiveEPSCell`）加兩行：「財報後 +X%（基準
   YYYY-MM-DD）」與「下次財報 N 天」，不新增欄位。

**Sanity 驗證（14 檔，見任務報告逐檔數字）**：既有月度 canonical 快照只有
`2026-05.json`（`snapshot_date` 帶說明字尾「2026-05-26 (incremental updates over
2026-05-25 base)」，只取前 10 碼）、`2026-06.json`（2026-06-23）、`2026-07.json`
（2026-07-30）、`2026-08.json`（2026-08-28）四份。NVDA 財報日 2026-08-26 早於
2026-08 快照的 2026-08-28（快照反而晚 2 天，若採用會混進財報後的修正）——picker
正確跳過 2026-08、退回 2026-07，驗證「只有嚴格早於財報日」這條規則真的擋下了會
汙染量測的快照；DELL 財報日 2026-09-01 晚於 2026-08-28，picker 正確採用 2026-08。
這兩個邊界案例合起來覆蓋了 sanity 檢查要求的兩種情境。

**證偽條件**：兩輪月頻輪動下來，若拿舊制日曆三個月排序重算會產生更好的 12 週
席位報酬（即財報錨定反而是雜訊，不是訊號）→ 撤回本條，`own_raw()`/`grp_score()`
的上修輸入退回 `eps_rev_3m_pct`；或財報錨定組（`rev_anchor=="earnings"` 的席位）
12 週中位報酬顯著落後日曆錨組，連兩輪 → 同上撤回。

**沒做/未驗證**：`get_earnings_calendar()` 對台股/日股等非美 yfinance 代碼
（`.T`/`.TW` 等）的 `get_earnings_dates()` 覆蓋率未逐檔驗證——目前席位引擎母體
本就排除 `.TW`（2026-09-02 拍板），實際受影響面小；財報日快取的 3 天 TTL 是沿用
`build_flowmap.py` 7 天 TTL 縮短的估計值，未做「多久算太舊」的專門校準。
