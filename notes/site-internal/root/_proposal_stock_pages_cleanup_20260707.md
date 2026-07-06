# 建議書：選股頁面整理（2026-07-07）

狀態：**提案，未執行**。持有人看過、裁決分岔項後才動手。
範圍：本 repo `docs/` 內所有選股相關頁面（含子頁面）＋餵它們的 cron／script。
已預先裁決（2026-07-07）：執行層 entry-state ＋ entry-state-backtest ＋ state-machine 三頁**封存成 stub**（比照 alpha-rank／flow 模式）。

---

## 0. 問題定性

選股聚合層在 **2026-07-02 → 07-05 四天內**由不同 session 連續搭了五個收斂面：

| 建置日 | 頁面 | 一句話 |
|---|---|---|
| 07-02 | `dd-screener/targets.html` 標的產生器 | 三發現層壓平、六燈火力集中 |
| 07-03 | `dd-screener/pipeline.html` 漏斗總覽 | 三軌架構權威頁（handoff Task 4） |
| 07-04 | `/engine/` 決策引擎 ×5 頁 | GRP 排序、L0–L4 席位系統 |
| 07-05 | `/cockpit/` 選股駕駛艙 | 純前端四區聚合、首頁頂卡 |
| 07-05 | `/picks/` 精選清單 | 正式榜（規則自動＋veto）＋十倍軌 |

沒有一頁資料斷更（全掛在現行 cron 上），但職能重疊嚴重：**漏斗講了兩套**（pipeline 三軌 vs engine L0–L4）、**發現層講了三套**（targets／radar／cockpit 漏斗區）、**最終名單講了兩套**（picks 正式榜 vs engine arena 席位）。這是整併債，不是棄置債。

---

## 1. 收斂判準（建議）

> **一個入口、一份對外名單、漏斗雙系統明確分工、latest.json 脊椎不動、5 月世代訊號頁收斂。**

- 入口 ＝ `/cockpit/`（首頁頂卡已是它；純前端零管線，維護成本最低）。
- 對外名單 ＝ `/picks/`（07-05 拍板的「規則自動上榜＋持有人 veto」治理是最新決策；十倍軌唯一載體）。
- 漏斗：`pipeline`（三軌流程＋板機＋回看鏡）與 `engine`（GRP 排序＋席位）**並存但分工**——見 §4 裁決項 D1。
- 真正的資料底座只有 `latest.json`（＋cyclical-track＋sop-funnel）——聚合層四群（pipeline／picks／cockpit／engine）**只吃這三份**。5 月世代的四個 timing 訊號頁（bottom-out／breakout／earnings-acceleration／entry-state）的 JSON **沒有任何下游消費者**，是純觀看頁，可收斂（見 §2-A2）。

---

## 2. 每頁去留總表

圖例：✅留　🔻降級／併　📦封存 stub　⛔停 cron　🚫不動（範圍外）

### A. 聚合層（本次整理主體）

| 頁面 | 建議 | 理由 |
|---|---|---|
| `/cockpit/` | ✅ 留（唯一日常入口） | 首頁頂卡、零管線、消費端 superset（fetch dd-screener＋engine＋momentum-5＋risk cache） |
| `/picks/` | ✅ 留（唯一對外精選名單） | veto 治理 07-05 拍板；tenbagger v0.1 唯一載體；週六 cron 活 |
| `dd-screener/pipeline.html` | ✅ 留（漏斗流程權威） | 07-03 handoff Task 4 產物；獨有內容：板機現況、回看鏡（發現力稽核）、觀望複審隊列——engine 沒有這三塊 |
| `/engine/` ×5 | ✅ 留（排序室），定位收窄 | GRP mandate（07-04 拍板「建議一律用 GRP 語言」）的唯一載體；arena.json 餵 cockpit 記分板；邏輯已凍結進維運 |
| `dd-screener/targets.html` | 📦 **封存**（見裁決項 D2） | 「給我名字」職能被 radar（全市場 GRP）＋ pipeline 潛力榜（DD 宇宙）雙面覆蓋；六燈≥2 同意的概念可移植成 pipeline 潛力榜的一欄 |

分工聲明（執行時落地）：pipeline 頁首加「排序與席位見 /engine/」、engine/index 加「流程與板機見 pipeline」、picks 頁首加「本頁＝對外正式榜；席位擂台是研究層」。三句話把職能邊界寫死，杜絕下一個 session 再蓋第六個收斂面。

### A2. 訊號層（5 月世代 timing screeners，2026-07-07 補充）

背景：quality-entry／bottom-out／breakout／earnings-acceleration／entry-state 五頁是 **05-18～05-20 三天內**建的上一世代平行 screener，比七月架構早一個半月。下游盤點結論：**四個 timing 頁的 JSON 零下游消費者**（聚合層只吃 latest.json＋cyclical-track＋sop-funnel）；唯一例外是 quality-entry.json 被 build_earnings_acceleration（取 universe）與 build_entry_state（將封存）讀。

七月架構已逐一取代它們的職能：

| 5 月頁 | 職能 | 七月接替者 |
|---|---|---|
| `breakout.html` 突破動能 | 突破時機 | sop-funnel 板機（A1 突破型，含 email 警報） |
| `bottom-out.html` 深回檔逆向 | 低位進場 | cyclical-track（循環底部×上修提名） |
| `earnings-acceleration.html` EPS 加速 | 上修動能 | GRP 的 R 閘（engine/radar）＋ cyclical-track 上修條件 |
| `entry-state.html` MA 五態 | 進場狀態 | 已裁決封存（sop-funnel 是現行執行層） |
| `quality-entry.html` 品質×進場 | 資格閘明細 | **無取代者**——pipeline 資格閘只列名單，這頁是唯一逐檔評分明細視圖 |

**建議**：📦 封存 bottom-out／breakout／earnings-acceleration 三頁（比照 alpha-rank stub 模式），daily workflow Step 4/5/6 移除，snapshots（合計 ~3.2M）凍結保留供未來回測；✅ 留 quality-entry（資格閘明細視圖，daily Step 3 續跑）＋ cyclical-track（三軌之一）。見 §4 裁決項 D5。

替代案（較保守）：三頁併成單一「timing 訊號」頁做分頁籤，build script 續跑——保留所有視圖但工程較大，且與「太多了」的整理初衷相悖。

收斂後 dd-screener 區從 14 頁 → **6 頁**：總覽／pipeline／quality-entry／cyclical-track／sop-funnel／sop-funnel 回測（＋封存 stub 若干）。

### B. 執行層（已裁決：封存）

| 頁面 | 建議 | 附帶動作 |
|---|---|---|
| `dd-screener/entry-state.html` | 📦 封存 stub | ⛔ `daily-non-fundamental-refresh.yml` Step 7（`build_entry_state.py`）移除；`entry-state-snapshots/`（2.1M）凍結保留不再增長 |
| `dd-screener/entry-state-backtest.html` | 📦 封存 stub | 資料本就是 6/10 一次性回測，無 cron 要停；回測 JSON（542KB）保留 |
| `dd-screener/state-machine/` | 📦 封存 stub | `run_daily.py` 本來就沒 cron（daily.json 停在 06-10，實質孤兒）；**Step 8 `write_daily_close.py`（態④研究寬表）建議保留**——append-only 研究資料、成本近零、與頁面無關（見裁決項 D3） |
| `dd-screener/sop-funnel.html` ＋ `sop-funnel-backtest.html` | ✅ 留 | 現行板機系統（態②C 冷卻觀察期中，memory 明示勿動）；daily cron＋email 板機活躍 |

### C. 殭屍 cron／半殭屍（無爭議，建議即刻處理)

| 項目 | 建議 | 理由 |
|---|---|---|
| `.github/workflows/update_six_state.yml` | ⛔ **移除 schedule（留 workflow_dispatch）** | 六態機 07-04 已退役，但 cron 仍排每週五 21:46 UTC——**07-10（本週五）會再 fire**，繼續重生已退役頁面並 commit。最急的一項 |
| `dd_alpha_ranker.py`（daily Step 2 momentum ＋ weekly fundamental/jensen 兩層） | ⛔ 停跑（執行時先 grep 確認 `alpha-rank.json` 無下游消費者） | 頁面已封存（HTML 有 ARCHIVED guard），但每日仍白算並 commit 48KB JSON＋`alpha-rank-snapshots/`（5.4M）持續累積 |
| `alpha-rank-snapshots/` | 凍結 | 同上 |

### D. nav 瘦身（無爭議）

- dd-screener 子選單現 13 項，其中 `alpha-rank`（已封存）被 **14 個頁面**的 subnav 連著。封存執行層三頁＋targets＋timing 三頁（D5）後，子選單瘦身為：總覽／🧭 Pipeline／Quality-Entry／循環軌／SOP Funnel／SOP 回測（6 項）。
- 改 `scripts/site_nav.py` 的 `DD_SCREENER_SUBNAV` 後全站 re-inject（沿用 07-06 crossasset commit 的做法，排除外部樹）。

### E. 不動區（明確劃界，本次不碰）

| 資產 | 為什麼不動 |
|---|---|
| `latest.json`／`build_dd_screener.py` | 全站脊椎——所有聚合面的真正輸入 |
| quality-entry／cyclical-track 兩頁 | 資格閘明細視圖＋三軌之一；cyclical-track 有掛 weekly cron（探查初判「半孤兒」是誤判——snapshot 少是因為週更且 07-03 才建）。其餘三個 timing 頁改列 §2-A2 收斂對象 |
| 區域 RS＋VCP screener ×4（us/tw/jp/my） | 獨立 daily cron 資產，與 DD 宇宙選股是平行系統；要整併是另一個 plan |
| `/qgm/`＋`/qgm-tw/`（含 ~130 份 archive） | 外部 repo（minervini-quality-backtest）bot push，本 repo 零依賴；動它要去外部 repo，範圍外 |
| `/long-track-smh/`（＋leverage）／`/long-track-tw/`／`/turtle-sleeve/` | 部位狀態頁不是選股頁；各自 cron＋email 訊號活躍 |
| `/research/momentum-5/` | GRP 站外對照組，PREREG 凍結中，動了對照就失效 |
| `/tools/`、`/flow/`（stub）、`/six-state/`（redirect stub） | 已封存或純工具，只有 six-state 的殭屍 cron 要停（見 C） |

### F. 週邊債（低優先，P3）

- **snapshot 無 retention**：六個活層 snapshot 目錄每日 append 無 pruning，總量 ~21MB、`quality-entry-snapshots/` +230KB/日。建議之後加 90 天保留窗——但**先確認無回測腳本依賴 snapshot 全史**（entry-state-backtest 一類）再動，本次只凍結封存層。
- engine 5 頁本身偏多（cards 與 arena 都在講席位），可考慮日後併頁；邏輯已凍結，純呈現整併，不急。

---

## 3. 執行順序（裁決後）

1. **P0 今週內**：停 `update_six_state.yml` schedule（趕在 07-10 週五 fire 之前）。
2. **P1 封存批**：執行層三頁封存 stub＋Step 7 移除＋targets 封存（若 D2 通過）＋timing 三頁封存（若 D5 通過，daily Step 4/5/6 移除）＋alpha-rank 停算＋subnav 瘦身＋全站 re-inject。一個 commit 群完成，逐項可逆。**注意**：`scripts/update_dd_index.py` 內建的 screener 連鎖 rebuild（quality-entry→bottom-out→breakout→EA→entry-state）要同步修剪成只剩 quality-entry，否則每次 DD 同步會把封存頁重生回來。
3. **P2 分工聲明**：pipeline／engine／picks 三頁頁首互指定位句（改 generator template，不是改烘焙 HTML）。
4. **P3 之後另議**：snapshot retention、engine 併頁。

執行紀律：比照 CLAUDE.md「Parallel-session git hygiene」四步自檢；封存 stub 沿用 alpha-rank／flow 現成模板（noindex＋原檔搬 `_archived/`）；改 workflow 一律留 workflow_dispatch 可逆。

---

## 4. 需要持有人裁決的分岔

| # | 分岔 | 我的建議 | 更激進的替代案 |
|---|---|---|---|
| **D1** | pipeline 與 engine 兩套漏斗長期並存？ | **並存但分工**：pipeline＝流程與板機（三軌、回看鏡、觀望複審），engine＝排序與席位（GRP）。兩者資料源與方法論本來就不同，砍任一都會丟獨有內容 | 砍 pipeline、把回看鏡／板機區塊移植進 engine——省一頁但要動已凍結的 engine build 鏈，工程不小 |
| **D2** | targets.html 封存？ | **封存**，六燈≥2 同意概念移植成 pipeline 潛力榜一欄 | 保留但從 subnav 降級（頁面白留著，下個 session 又會有人往上疊） |
| **D3** | state-machine 封存後，Step 8 態④研究寬表（`write_daily_close.py`）續跑？ | **續跑**——append-only 研究資料、與頁面無關、C 冷卻觀察期可能用得到 | 一起停，state-machine 樹整個凍結 |
| **D4** | picks 正式榜 vs engine arena 席位，兩套「名單」並存？ | **並存**：arena＝機器排序擂台（研究層），picks＝人工治理對外榜（決策層）。用 P2 分工聲明固定 | 砍 arena 對外呈現、只留 JSON 餵 cockpit——動 engine 呈現層，收益低 |
| **D5** | 5 月世代 timing 三頁（bottom-out／breakout／earnings-acceleration）封存？ | **封存**：JSON 零下游、職能被 sop-funnel 板機／cyclical-track／GRP-R 取代；snapshots 凍結保留 | 併成單一 timing 頁做分頁籤（保留視圖但工程較大）；或只降 nav 不封存（頁面白留，繼續每日重生） |

---

## 附錄：cron ↔ 頁面對照速查

| workflow | cron（UTC） | 餵哪些選股頁 | 本提案動作 |
|---|---|---|---|
| `daily-non-fundamental-refresh.yml` | 週二–六 01:00 | latest.json＋五訊號層＋sop-funnel＋alpha JSON＋entry-state | 移除 Step 7（entry-state）；Step 4/5/6（bottom-out／breakout／EA）依 D5 移除；Step 2（alpha momentum）停；Step 8 依 D3；留 Step 1（latest.json）／Step 3（quality-entry）／Step 9（sop-funnel） |
| `weekly-fundamental-refresh.yml` | 週日 18:00 | targets＋cyclical-track＋pipeline＋alpha fundamental/jensen | targets step 依 D2 移除；alpha 兩層停 |
| `weekly-engine.yml` | 週日 20:00 | /engine/ 五頁 | 不動 |
| `weekly-market-update.yml` | 週六 00:08 | picks（candidates＋tenbagger）＋momentum-5 | 不動 |
| `update_six_state.yml` | 週五 21:46 | 已退役 six-state 狀態頁 | **移除 schedule** |
| `daily-screener-{us,tw,jp,my}.yml` | 各自每日 | 區域 RS＋VCP ×4 | 不動 |
| （外部 repo bot） | — | /qgm/、/qgm-tw/ | 不動 |
