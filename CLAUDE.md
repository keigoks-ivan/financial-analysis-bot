# Repo-wide instructions

## Decision-time critic：思考產業 thesis 動部位前必先 spawn

當用戶討論以下任一情境，**必須先 spawn `industry-thesis-critic` sub-agent** 對相關 ID 跑冷讀，再給投資建議。這是 Boris verify-app pattern 在投資決策的翻譯 — 寫 ID 的 agent 與驗 thesis 的 agent 不同。

**觸發情境**（任一即觸發）：
- 「考慮加倉 / 減倉 / 新進 / 退出 X 產業 theme」
- 「{theme} thesis 還活著嗎」
- 「該不該對 {industry} 增加 / 降低曝險」
- 「{ID 主題} 現在還能 act 嗎」
- 用戶提及具體 ID 主題並表達決策意圖（不是純資訊查詢）

**Spawn 方式**：
```
Agent({
  description: "Cold review {theme} thesis",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "You are operating as the industry-thesis-critic sub-agent. Read spec at /Users/ivanchang/.claude/agents/industry-thesis-critic.md. ID: {path}. Intent: {user 意圖}. Save report to notes/site-internal/id/_critic_{Theme}_{YYYYMMDD}.md."
})
```

**並讀知識帳本**（2026-06 新增）：對決策涉及的每個 ticker，先跑 `python knowledge/q.py <TICKER>` 載入歷次裁決 / thesis 演進 / 已回填 outcome 再給建議——不要從零重推一個我可能早有定見的名字；產業層級用 `python knowledge/q.py --theme {關鍵字}` 看成員現裁決分布。帳本（我過去實際下的判斷）與 critic（事前冷讀）互補，是動部位前的另一隻錨。衍生物若不在則 `q.py` 會自動 rebuild；細節見 `knowledge/README.md`。

**並讀用戶自己的思考筆記**（2026-07-08 新增）：同時跑 `python knowledge/q.py --note <TICKER>` 撈該 ticker 的 usernote（用戶在蒙格清單/獵場/寫作間親手寫的裁決、殺手假設、費曼解釋——在 `knowledge/vault/notes/`），與 `--falsifiers` 看其未對帳假設。**用戶寫過的判斷是最高優先級的錨**：給建議時必須引用或明確反駁，不可無視；若其殺手假設已觸發，先指出這件事再談別的。

**蒙格腦（第三隻錨，2026-07-08 新增）**：用戶說「問蒙格」/「蒙格會怎麼看 {X}」/「用蒙格的方法檢查 {ticker}」時，spawn `munger-mind` sub-agent（spec：`~/.claude/agents/munger-mind.md`；語料在 `knowledge/munger/`，corpus 缺檔先跑 `python3 knowledge/munger/fetch_corpus.py`）。它執行蒙格的判斷程序（能力圈→四過濾器→反過來想→激勵→傾向掃描→與庫內裁決對質），輸出存 `notes/site-internal/munger/`。與 critic（產業冷讀）、q.py（用戶歷史）互補；「太難籃子」是合法輸出。動大部位時三隻錨並用。

**不觸發**（僅資訊查詢）：
- 「ID_X 寫了什麼」/「{theme} 是什麼」/「介紹一下 {industry}」 — 純解釋型問題，直接回答即可
- 寫稿過程中（that's a separate write-time critic, P2 未實作）

**例外**：用戶明確說「不用跑 critic」/「我自己看就好」可跳過。

## Site composition：4 repos 共同產生 docs/

公開站 `https://research.investmquest.com/` 由 4 個 repo 共同生成 `docs/` 內容。任何「整站樣板/頁首/頁尾」這類任務，第一步要先判斷該頁路徑屬於哪個 repo，再去對應 repo 改 generator template。

**速查**：
- `qgm/`、`qgm-tw/` → minervini-quality-backtest
- `briefing/YYYY-*`、`weekly/`、可能 `earnings/` 流程 → morning-briefing
- `backtest/`、可能 `six-state/` 報告檔 → v7-backtest
- 其餘（首頁、`earnings/`、`research/`、`pm/`、`dd/`、`id/`、`markets.html`、`sectors.html`、`screener*.html`、`how-to.html`、`briefing/index.html`、`six-state/index.html`）→ 本 repo

不確定時：`git -C <repo> log --oneline -- docs/<path>` 看哪個 repo 有歷史。改外部 repo 是新的 commit/push 範圍，**動手前先跟用戶確認**。

詳細 4-repo 表格 + 每個 repo 的 generator/workflow/commit author：見 `.claude/notes/site-composition.md`。

## Workflow: 每次 DD / DCA 必同步 research 頁（DD 組合快照）

任何 DD（`docs/dd/`）或 DCA（`docs/dca/`）的新增、修改、補 patch 後，**commit 前必跑** `python scripts/update_dd_index.py`，以同時更新：
- `docs/research/index.html` 主表（dd-tbody-v12 整段重生 from dd-meta JSON）
- DD 組合快照（DD_AUTO_STATS：訊號分布、最新 8 筆、PEG 便宜 top 5、5Y P/E 分位、2Y upside、X cohort 拆分、DCA Verdict 分布、護城河面板）
- 同跑 `DD_STALE_FRESH` / `PM_LAST_RUN` / `PM_HOLDINGS` / `PM_ACTIONS` 五段標記注入
- **自動觸發** `scripts/build_dd_screener.py`（rebuild `docs/dd-screener/latest.json`），讓 `/research/` 與 `/dd-screener/` 兩個頁面 universe 永遠一致。yfinance 失敗時 screener rebuild 會 warn 但不 abort research sync；要離線跑加 `--skip-dd-screener`。

把 `docs/research/index.html`、`docs/dd-screener/latest.json`、`docs/picks/candidates.json`（2026-07-05 起 update_dd_index 自動連鎖 build_picks.py，讓精選清單即時反映新裁決）、DD 新檔**併入同一 commit**，避免任一頁面滯後於底層報告。stock-analyst v13 skill 的 HTML 輸出協議已內建此步（step 3 跑 update_dd_index.py），但**手動 patch / 補 metadata / 改 legacy DCA Verdict** 這類 skill-外路徑也必須遵守此規則。v13 DD 的決策層欄位（dca_verdict 等）在 dd-meta JSON，下游 dual-read 直接讀。

## Workflow: push earnings / 發布財報

當用戶說「push earnings」/「發布財報」/「發佈財報」/「發布新財報」/「更新 earnings index」時，自動觸發 `push-earnings` skill（`.claude/skills/push-earnings/`），照其 9 個 steps 執行。

## Workflow: refresh DD screener with new EPS Excel

當用戶丟新 `DD_universe_EPS_estimates_YYYYMMDD.xlsx`（無論放 Downloads/ 或直接給路徑）並要 update，或說「update eps screener」/「更新 dd-screener」/「DD screener 更新 EPS」/「跑新 Excel 更新 screener」/「refresh EPS estimates」/「{path}.xlsx 更新表格」時，自動觸發 `refresh-eps-screener` skill（`.claude/skills/refresh-eps-screener/`），照其 8 個 steps 執行。

**核心**：同月內 5/20→5/25 這種 intra-month refresh，skill 會先 cp 舊 `{YYYY-MM}.json` snapshot 為 `{YYYY-MM}-DD.json` 保留 baseline（避免被新 snapshot 覆蓋抹掉），讓 build 撿到 prior baseline 算 FY1/FY2/FY3 EPS revision%。**Spot-check 對照 Excel Notes 第 8 列「Updated EPS vs YYYY-MM-DD」是 hard gate**，sanity 不過不要 commit。非美股 (TW/JP/HK/KS/CN/CH) FX 自動換算走既有 pipeline，不用手動處理。

## Workflow: 30 天財報統整 (earnings synthesis)

當用戶說「跑最近財報的統整」/「earnings 統整」/「30 天財報統整」/「月度財報統整」/「財報季統整」/「過去 30 天財報重點」/「earnings synthesis」/「earnings monthly recap」/「earnings 30-day recap」/「monthly earnings rollup」時，自動觸發 `earnings-synthesis` skill（`.claude/skills/earnings-synthesis/`）。

**定位**：消費端 skill — 假設 `docs/earnings/earnings_YYYY-MM-DD.html` 30 天日報已存在。重點是把 vertical 日報串成 horizontal sector-level 敘事 + investment implication，不重做 per-company 分析。

**輸出**：
- HTML：`docs/earnings/synthesis_YYYY-MM-DD.html`（同階層；prefix `synthesis_` 不與日報 regex 衝突，push-earnings 不會誤抓）
- 索引：`docs/earnings/index.html` 在 hero 之後 / 日報列表之前插入 `<section id="monthly-synthesis">` highlight card（CSS 已預備在 index.html `.synthesis-tag` / `.synthesis-list` 規則）

**素材結構**：本地日報的 §2/§3/§4/§5 + lede + report-meta（複用 push-earnings 的 parsing 邏輯）+ **缺失交易日 web fill-gap**（mkt cap ≥ $50B 的當日 earnings，light WebFetch 取 EPS/rev/guidance/reaction）+ 中量 WebSearch / WebFetch（3-5 輪/主題）做趨勢深掘。Ticker → 子產業 mapping 走 `docs/id/ID_*.html` id-meta `related_tickers[]` 為主、`docs/dd/dd-meta` industry 補強、inline 硬表 fallback。本地深度料 vs web 補料在報告中**明確分色標示（`.source-local` 藍 vs `.source-webfill` 橘）+ 信心度註腳**，§6 add/cut/hold 建議只用本地深度料當主錨。

**Critic**：無強制 gate（v1 政策同 push-earnings）。用戶可在發布後手動跑 `id-review --mode synthesis`（未來 Phase 2 才有此 mode；現階段用一般 cold-review）。

**git flow**：commit 訊息格式 `Add earnings synthesis: window YYYY-MM-DD → YYYY-MM-DD`，直接 push main。

## Workflow: 個股深度報告（v13 DD，含決策層）— DCA 已併入

**2026-06-22 起 DCA 已併入 stock-analyst v13。** 個股深度研究與投資決策層整併成**單一報告** `docs/dd/DD_{TICKER}_{YYYYMMDD}.html`：Part I 基本面深度（§1-§11）+ Part II 決策層（§12 矛盾裁決 / §13 pre-mortem+Max DD / §14 統一裁決 / §15 複審），收斂為**一個人面對裁決：進場 / 觀望 / 迴避**。基本面評級 A+/A/B/C/X 降為 metadata（餵 screener），不再是並列 headline。

當用戶說「幫我跑 {ticker} dca」/「{ticker} 定見」/「conviction analysis {ticker}」/「最終判斷 {ticker}」/「該不該進場 {ticker}」/「買不買 {ticker}」/「個股分析 {ticker}」/「{ticker} DD」時，一律自動觸發 `stock-analyst` skill（v13，`.claude/skills/stock-analyst/`）。`deep-conviction-analyst` 已退役為 deprecation stub，dca/定見 觸發語改觸發 stock-analyst。

**輸出**：
- HTML：單一 `docs/dd/DD_{TICKER}_{YYYYMMDD}.html`（schema v13.0；§14 帶 `id="decision"` 錨點；**不再產獨立 `docs/dca/DCA_*.html`**）
- dd-meta v13：新增決策層欄位 `dca_verdict`/`dca_role`/`moat_trend`（權威）/`runway_post_y5`/`ev5y_pct`（+ 選填 `irr_base_pct`/`max_dd_pct`），下游聚合器直接讀
- Research 頁同步：跑 `python scripts/update_dd_index.py` 後，「定見」欄連到該 ticker v13 報告的 `/dd/DD_X.html#decision` 錨點

**Legacy**：343 份既有 `docs/dca/DCA_*.html` 凍結保留、仍在站上，下游以 dual-read 支援（v13 dd-meta 優先，讀不到才 fall back legacy DCA）。設計細節見 `docs/_handoff_v13_dd_design_20260621.md`。

## Workflow: 產業 DS（敘述型產業研究）— 【DEPRECATED 2026-06-11，已併入 industry-analyst v2.0】

`industry-ds`（DS 敘述報告）已於 2026-06-11 停用，**併入 `industry-analyst` v2.0**。v2.0 走「敘事為骨、表格為窗」單一架構，用 DS 的因果敘事弧當骨架、ID 的決策資產當器官嵌入，吸收了 DS 的敘事弧 / 因果閉合 / 推導鏈 / §末 aside 來源系統。

**觸發語轉向**：原 DS 觸發語（「{主題} ds」/「ds {主題}」/「{產業} 敘述報告」/「分析 {產業} 的供需循環」/「{產業} 歷史與未來」/「discourse {industry}」）現在一律觸發 `industry-analyst`（v2.0），輸出寫 `docs/id/`（不再寫 `docs/ds/`）。

**Legacy DS 報告**：既有 8 份 `docs/ds/DS_*.html` 凍結為 legacy，檔案不動、不 retrofit、不遷移，仍在 `https://research.investmquest.com/ds/` 上站。需 review / patch / 驗證 legacy DS 時走 `id-review --mode ds`（DS-mode 8 條檢查清單仍在）；**不要用 industry-ds 生新 DS**。

**Plumbing（僅供 legacy DS 維護參考）**：`scripts/validate_ds_meta.py`（驗 `ds-meta`，pre-commit hook 仍跑）、`scripts/build_ds_category_pages.py`（重生 `docs/ds/cat-*.html`）、`scripts/init_ds_index.py`（一次性 bootstrap）。Taxonomy 與 ID 共用（`docs/id/taxonomy.md`）。

## Workflow: 多股對比（multi-stock comparator）

當用戶說「比較 {T1} {T2} 用 DCA」/「比較 {T1} {T2} {T3} 看 DD」/「多檔比較」/「同類對比」/「該選哪一家」/「DCA 對比分析」時，自動觸發 `multi-stock-comparator-v1` skill（`.claude/skills/multi-stock-comparator-v1/`）。

**定位**：消費端 skill — 假設目標 ticker 的個股報告已存在（v13 `docs/dd/DD_*.html`，內含基本面 + 決策層；或 legacy `docs/dca/` + `docs/dd/`），不自動觸發 `stock-analyst`。對 2-5 檔執行四層時間框架（<12M / 2-3Y / 3-5Y / 5-10Y）橫向打分，每層獨立排序 + 判斷邏輯，最後給推薦標的 + 不選其他檔的具體理由。**v13 注意**：新報告的決策層（裁決/IRR/Max DD/pattern match）已在 DD 檔 Part II，不再有獨立 DCA 檔——讀 v13 DD 即可；legacy ticker 才需讀 `docs/dca/`。

**輸出**：
- HTML：`docs/comparisons/MS_{T1}vs{T2}_{YYYYMMDD}.html`（4 檔以上用底線連接：`MS_T1_T2_T3_T4_YYYYMMDD.html`）
- 索引：`docs/comparisons/index.html`（skill 在 `<ul class="reports">` 最上方 insert `<li>` 卡片；首份報告產出後自動移除 `.empty-state` div）
- 上站路徑：`https://research.investmquest.com/comparisons/`

**股價來源**：固定走 `WebSearch`（`scripts/fetch_prices.py` 是 weekly GitHub Actions batch，不收 ticker 參數，無法 ad-hoc）。報告日 >3 天時重抓現價並重算 Fwd PE / PEG（v1.3 無痕呈現規則）。

**Plumbing**：無 pre-commit validator（與 DCA 同政策）；無 build script（listing 是 skill-appended，類似 `push-earnings` 模式）；目前無 `push-comparisons` skill，git flow 是手動 `add / commit / push`。

## Workflow: 期望落差綜合研判（expectations-synthesis）

當用戶說「{ticker} 期望綜合」/「{ticker} 綜合研判」/「{ticker} 趨勢期望」/「expectations synthesis {ticker}」，或丟下一個 `…/007美股/{ticker}/` 券商報告資料夾並要做綜合判讀時，自動觸發 `expectations-synthesis` skill（`.claude/skills/expectations-synthesis/`）。

**定位**：消費端 / 綜合層 skill — 假設目標 ticker 的 DD（`docs/dd/DD_*.html`）與相關 ID / 供應鏈已存在，**不重做基本面或競爭分析**。把站內深度料（ID / 供應鏈 / DD / 知識帳本）＋ 外部賣方報告（CLSA / Nomura / HSBC / UBS / Barclays…）＋ 法說與分析師會議逐字稿，收斂成單一投資判斷。骨架＝ A 趨勢定位（選股漏斗上游）＋ B 期望落差（市場對未來 EPS 的預估是否過高或過低）＋ 退出觸發，雙鏡頭依 mandate 取捨。與 `multi-stock-comparator-v1` 並列（皆消費端），與 `stock-analyst` 互補（後者做單檔 DD）。

**輸出**：
- HTML：`docs/research/synthesis/{TICKER}_{YYYYMMDD}.html`（noindex；模板 `.claude/skills/expectations-synthesis/template.html`）
- 索引：`docs/research/synthesis/index.html` 列表頁（skill append 卡片）；nav「研究 ▾ → 期望落差綜合研判」入口已建於 `scripts/site_nav.py`
- 上站路徑：`https://research.investmquest.com/research/synthesis/`

**硬規則**（詳見 SKILL.md）：§2+§3 都要寫且 §Δ 必須收斂兩面、§5 只連出 DD/ID/供應鏈不複製、專業賣方口吻無 slang/自我對話、**每份報告獨立成立不跨檔對照**、股價＝最新收盤、大 PDF 一律先 `pdftotext`。內建**決策時 critic**（spawn `industry-thesis-critic`，存 `notes/site-internal/id/_critic_{TICKER}_*.md`）。

**Plumbing**：無 pre-commit validator（同 comparisons / DCA 政策）；列表卡片 skill-appended（同 push-earnings）。**預設停下複審**，用戶說 push 才走 3 檔 commit（synthesis 頁 + `research/synthesis/index.html` + critic md），push 前先 `git pull --rebase`。參考實作：`docs/research/synthesis/GLW_20260625.html`、`TSM_20260625.html`。

## Workflow: 產業供應鏈互動地圖（supply-chain map）

當用戶說「跑 {topic} 供應鏈地圖」/「{topic} 供應鏈」/「畫 {topic} 供應鏈」/「supply-chain {topic}」/「{topic} supply chain map」時，自動觸發 `supply-chain-cartographer` skill（`.claude/skills/supply-chain-cartographer/`）。

**定位**：與 industry-analyst v2.0（敘事為骨、表格為窗的產業深度報告，含供需循環敘事 + 決策層）並列的**另一種產業視角** — 互動式節點圖，看「製程節點上誰是脆弱依賴點」。同 theme 可與 ID 並存。

**輸出**：
- JSON：`docs/supply-chain/data/{topic}.json`（節點圖資料，schema 見 SKILL.md）
- HTML：`docs/supply-chain/{topic}.html`（thin template，~60 行，load engine.js）
- Manifest：把 `docs/supply-chain/data/topics.json` 該 topic 的 `active` 翻成 `true`
- 上站路徑：`https://research.investmquest.com/supply-chain/{topic}.html`

**Row 數彈性**：3-6 列由產業敘事決定（半導體製造 3 列 / 光電混合 5 列 / IC 設計 5 列 / 機器人 6 列）— 引擎不強制。

**核心規則**：
- 每個 ⚑（客戶獨家／關鍵單點）必須 ≥2 來源、信心度標註（high/med + 條件文字）
- TW 中文源（TechNews / Money Weekly / 工商時報 / 鉅亨 / 法說 vocus）至少 30%
- ⚑ 子類用 4-bucket 框架（近乎獨佔 / 客戶獨家 / 鎖喉點 / 封裝級單點）
- 禁止 stingtao voice 殘留（「本版補齊」「先前漏掉」等）

**Plumbing**：
- `scripts/validate_supply_chain_meta.py`：驗 `docs/supply-chain/data/*.json`（pre-commit hook 會跑、staged-only；validator 自身變動時 full-sweep 全部 topic）
- `scripts/build_supply_chain_dd_index.py`：scan docs/dd/ 重建 `dd_links.json`。**已掛 update_dd_index.py 自動鏈** — 跑 DD/DCA 同步時會自動 rebuild 一次，不需手動。
- engine 完全抽離（`assets/engine.{css,js}`），新 topic 不需動 code

**現況**：CoWoS（31 nodes 3 列）+ CPO（19 nodes 5 列）兩個 topic 上線；剩下 13 個 topic 在 manifest 中標 `active: false`（HBM / 先進製程 / 矽光子 / 面板級封裝 / IC 設計 / 半導體材料 / ASIC / IC 基板 / 電源散熱 / AI 伺服器 ODM / 機器人 / 低軌衛星 / 軍工國防）。

## Workflow: 擁擠交易監測（crowding monitor）

當用戶說「跑擁擠交易監測」/「crowding monitor」/「擁擠交易月報」/「新一期 crowding」/「positioning monitor」時，自動觸發 `crowding-monitor` skill（`.claude/skills/crowding-monitor/`）。

**定位**：消費端 skill — 產出新一期 `docs/crowding/CROWDING_YYYYMMDD.html`，把週更資料層＋情緒/資金流 web 掃描（FMS／Flow Show／GS positioning／AAII／VIX-SKEW）收斂成三層代理三角測量。**與首頁風險儀表同家族——描述器（describer）非擇時訊號**，衡量部位集中與下方緩衝、放大回撤與相關性，不預測轉折時點。

**輸出**：
- HTML：`docs/crowding/CROWDING_{YYYYMMDD}.html`（noindex；規格對齊創刊號 `CROWDING_20260705.html`：Exhibit 編號制、named trades 含 unwind 觸發器、COT 儀表、主題熱力圖、§7 組合 read-through 用 GRP／三軌語言禁 IRR 排序禁買賣指令、反向掃描、方法論血統與 gaps）
- 索引：`docs/crowding/index.html` 期刊列表最上方 insert 卡片（不動 `<!-- CROWDING_AUTO_DASH_*-->` 標記間內容）
- 上站路徑：`https://research.investmquest.com/crowding/`

**週更 pipeline（另一 owner，skill 唯讀）**：`scripts/build_crowding.py`＋`.github/workflows/crowding-weekly.yml` cron 每週產 `docs/crowding/data/latest.json`（COT 15 市場＋64+ 主題分數＋15 檔 ETF＋gaps），並替換 index.html 的 AUTO_DASH 標記間即時儀表。**skill 不改 pipeline／data/／workflow。**

**硬規則**：中文標點全形；描述器定位禁買賣指令句；§7 GRP／三軌語言禁 IRR 排序；COT as-of 與各層時效必標；低信心數據掛 lo、未取得數值進 gaps 不捏造；無鷹架語言；發布前 self-review gate（三重檢查）；git flow＝預設停下複審、持有人說 push 才 commit（比照 expectations-synthesis）。

## Workflow: 總經深度報告（macro-analyst）

當用戶說「總經研究 {主題}」/「macro {topic}」/「{主題} 總經報告」/「總體經濟分析 {主題}」/「宏觀分析 {主題}」/「{主題} 宏觀傳導」時，自動觸發 `macro-analyst` skill（v1.0，`.claude/skills/macro-analyst/`）。

**定位**：與 industry-analyst（產業 ID）平行的**總經深度研究層**——輸入跨資產／政策／利率／匯率／財政／流動性層級主題，四軸 web 研究（歷史 base rate／政策與流動性／盈餘傳導／市場定價），輸出「機制 → base rate → 數據錨 → 傳導鏈 → 情境樹 → 證偽表 → 組合 read-through」HTML。**描述器紀律＝憲法**（生於 2026-07-08 短期轉折判死裁決之後）：環境判讀與情境準備，禁擇時結論、禁買賣指令。主題有明確產業供需錨 → 走 industry-analyst，不觸發本 skill。

**輸出**：`docs/macro/MACRO_{Slug}_{YYYYMMDD}.html`（macro-meta JSON schema=macro-v1）＋ `docs/macro/index.html` insert 卡片＋critic 報告 `notes/site-internal/macro/`；上站 `https://research.investmquest.com/macro/`。低頻深度層（每月 0-2 份，不做週期性自動產出）。

**硬規則**：中文標點全形；T1（Fed/FRED/Treasury/BLS/IMF/BIS 一手）floor 45%；每數字帶來源＋as-of；寫稿後強制 cold-review critic（7 條 checklist）；判斷類規則已登記 rule_ledger（stance 反騎牆＋證偽表強制＋tool-level 90 天引用 kill）；git flow＝預設停下複審、用戶說 push 才 commit。

## Report 篇幅 floor（depth gate，非灌水目標）

DD 報告有 size floor，但**這是深度閘門，不是 byte 目標** — 達標的正道永遠是「真量化模組 × sourced 數字」，反灌水鐵律不變（skill：「寧可 105KB 全自算，不要 125KB 注水」）。v13 單檔含基本面 Part I + 決策層 Part II，floor 上修；下列 floor 留足餘裕，只攔真正偷懶的薄報告：

| 類型 | hard floor（commit 擋下） | soft warn（放行但提示） | skill 目標 |
|---|---|---|---|
| **v13 DD**（`"schema":"v13`，含決策層） | < 110KB | < 125KB | ~110–125KB（Part I 基本面 ≥ 60%；Part II 決策層淨增深度） |
| legacy v12 DD（`docs/dd/DD_*.html`） | < 80KB | < 90KB | ~90–100KB（§5+§8+§9+§10+§11+§12 ≥ 60%） |
| legacy DCA（`docs/dca/DCA_*.html`，已退役不再新增） | < 50KB | < 55KB | — |

**只對「新增」檔生效**（`git diff --cached --diff-filter=A`）— 全新報告永遠是新 `*_YYYYMMDD.html`（Add），對 legacy 報告補 metadata 是 Modify，不會被擋。gate 寫在 `scripts/hooks/pre-commit`（v13 floor 對 `"schema":"v13` 檔生效，legacy v12 維持 80KB），真要放行 lean-but-complete 報告用 `git commit --no-verify`。

## 規則治理：判斷類規則的加與刪（2026-07-07 起）

任何 skill 中**會影響裁決輸出的規則**（veto / gate / 救援 / critic / hysteresis 這類「判斷類」；純 sourcing/格式/防灌水不在此列）適用三條治理鐵律：

1. **無 kill condition 不准新增**——新規則必須同時登記進 `knowledge/rule_ledger.md`，寫明「什麼數據出現就該刪或降級」。說不出 kill condition 的規則是教條，不是紀律。
2. **加一提刪一**——新增判斷類規則時，必須在 commit 訊息提名一條既有規則作候刪審查對象（可以審後保留，但必須過一次審視）。
3. **每輪裁決校準附規則審計**——校準（下輪 2026-10，三份：legacy DCA / v13 DD / ID）同時回填 ledger 審計欄：零救援實績或誤傷 > 救援的規則直接 KILL，不辯護。
4. **改判斷類閘的標準程序（2026-07-07 校準輪固化）**——(a) **回溯考卷**：先組已知答案案例組（miss 組＋save 組，如 ALAB/AMAT/SEZL/DELL vs GLW/FORM/AXTI/RKLB），新閘必須乾淨分開兩組才可上線；(b) **資料命中率檢查**：資格條件先驗其變數在實檔的可得性與觸發率——0 命中的閘是裝飾不是紀律（AR≥4 教訓）；(c) 門檻數字上線即 PREREG 凍結至下輪校準，期間不因單一案例動門檻。

WHY：2026-07 全鏈驗屍證實，五月那批僵化閘（MA Soft Veto / AR≥4 / 動能過熱）的共同點是**不可證偽**——沒人知道它們擋掉的名字後來怎樣，所以安穩活了三個月，錯過尾 3× 躲掉尾。教條與紀律的分界＝可證偽性。另：skill 結構膨脹時優先「核心＋references/ 條件載入」拆分（stock-analyst v14.7 模式），不要讓 always-on context 無限長大。

## Parallel-session git hygiene（commit 前自檢）

常同時跑多個 session 對同一 working tree，歷史上多次被並行 session 清空 `_build`、catalog 掉條目、wrong-cwd commit、untracked sibling 被廣域 `git add` 掃進來（見 memory `feedback_supply_chain_precommit_sweeps_untracked` / `feedback_no_fixtures_in_docs`）。**commit 前固定四步**：

1. 確認 cwd 是對的 repo（4-repo 同站，改錯 repo 是真風險）。
2. `git status` 看 `??` 區 — 確認沒有別的 session 留下的 orphan 檔會被一起 commit；只 `git add` 你這次真的要動的檔，**不要盲 `git add -A`**。
3. push 前重查 `docs/research/index.html` / `docs/dd-screener/latest.json` / 相關 catalog 沒被並行 session 覆蓋掉你剛產的條目。
4. 驗證 fixture 一律放 `/tmp`，**不要放 `docs/` 追蹤目錄**（並行 cron/session 會掃上線）。

## Git pre-commit hook

Repo 有 pre-commit hook（`core.hooksPath=scripts/hooks`，已啟用）跑：dd/id-meta validator、cache schema、supply-chain schema、`.nojekyll` guard、supply-chain hub rollup，以及 **DD/DCA size-floor gate（added-only，見上）**。新 clone 啟用方式（`bash scripts/install_hooks.sh`）與 bypass 細節（`--no-verify`）：見 `scripts/README.md`。

標準 ticker pipeline（一句指令跑完，v13）：`stock-analyst`（v13 單一 DD，含決策層 + 統一裁決）→ `python scripts/update_dd_index.py`（同步 research 頁 + screener）→ commit/push。**DCA 已併入 v13，無獨立 DCA 步驟。** 給單一 ticker 時可順帶自動偵測同產業 peer 一起跑（如 KLAC → ASML / LRCX），但**動部位前先按 repo 頂部「Decision-time critic」規則 spawn `industry-thesis-critic`**。`/ddreport` skill（v2.0）把這條鏈固化。
