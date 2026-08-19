# scripts/intel/ — 情報監視器 Phase 1（市場層）

對應設計文件：`notes/site-internal/intel/DESIGN.md`。全部四段（抓取 →
haiku 分類 → sonnet 摘要／早報／儀表 → render）都在同一條 GHA workflow
`.github/workflows/intel-daily.yml` 裡跑（§10 2026-08-19 改判：claude.ai
Routine 推不上 GitHub，LLM 步驟改用 Claude Code CLI headless `claude -p`）。

## 這裡跑什麼

`fetch.py` 是唯一入口，全程零 LLM：

1. 讀 `sources.yml`，逐一抓取（RSS／FRED CSV／Polymarket JSON／少數純健康
   檢查用的 JSON），每個來源記一筆健康狀態。
2. 讀站內既有的 `docs/monitor|regime|rotation|crowding|detective/data/*.json`
   （已存在的日更數字骨幹），只在「今日新穿越門檻」或「狀態與昨天不同」時
   產生數字卡——不是每個序列每天都發卡。
3. 正規化成卡片（schema 見 DESIGN.md §11 的子集）、去重（URL 精確比對＋
   標題 token Jaccard ≥0.85 近重複合併）、丟棄 36 小時前的新聞（`data` 卡
   不受此限）、關鍵字 deny-list 過濾、依 tier／交叉印證數／新鮮度排序後
   截斷至 ≤200 條、對排名前 60 條做連結存活檢查。
4. 寫出兩個檔案。

## 輸入 / 輸出

| 檔案 | 角色 |
|---|---|
| `sources.yml` | 輸入：來源白名單（誰／怎麼抓／哪個維度／T1-T4） |
| `docs/monitor\|regime\|rotation\|crowding\|detective/data/*.json` | 輸入：站內既有數字骨幹（唯讀，本目錄不寫這些檔） |
| `docs/intel/pending/YYYY-MM-DD.json` | 輸出：候選卡片＋當日統計，餵給下一步 haiku/sonnet |
| `docs/intel/data/sources_health.json` | 輸出：每個來源本次抓取的 ok/latency/item_count/error |
| `docs/intel/data/state.json` | 輸出：跨日狀態（regime 標籤／輪動領先象限／擁擠極端集合／kill-watch near-set／Polymarket 前日機率），用來判斷「有沒有變」 |

## 怎麼加一個來源

1. 用真實 HTTP fetch 核實 URL（10 秒 timeout），確認回傳的是可解析的
   RSS/Atom 或 JSON，不是轉址回首頁的 HTML。
2. 在 `sources.yml` 加一筆，欄位說明見該檔開頭註解；`category` 必須是
   DESIGN.md §3 十三維度 key 之一。
3. `kind: rss` 直接吃 `fetch_rss_source`；`kind: csv` 只給 FRED 系列用
   （fetch.py 靠 `fred_` id 前綴＋URL 裡的 `id=` 參數辨識）；新的結構化
   JSON 來源（非 FRED、非 Polymarket）預設走 `fetch_json_healthcheck_source`
   （只健康檢查、不產卡）——要讓它產卡，得照 FRED／Polymarket 的模式在
   `dispatch_source()` 加專屬分支。
4. 抓不到的來源設 `enabled: false` 並在 `note` 寫清楚失敗原因（不要用猜的）。

## 本機怎麼跑

```bash
# 全量抓取（正式寫檔）
python3 scripts/intel/fetch.py --date 2026-08-19

# 只跑其中一個來源（除錯用）
python3 scripts/intel/fetch.py --date 2026-08-19 --only fed_press_all

# 只跑站內數字卡（不打任何外部 HTTP）
python3 scripts/intel/fetch.py --date 2026-08-19 --only onsite

# 乾跑，不寫檔（印統計即可，state.json 也不會被更新）
python3 scripts/intel/fetch.py --date 2026-08-19 --dry-run
```

依賴：`requests`／`feedparser`／`pyyaml`（皆為純 Python、無編譯依賴，GHA
安裝一行 `pip install requests feedparser pyyaml` 即可，不需要金鑰）。

## 2026-08-19 補充（orchestrator 驗收後修正）

- FRED 規則 1 改為「20 日變化 vs 近一年 20 日變化的 2σ」（原本對日變化 σ 比，10 條裡 6 條天天觸發）；新增規則 2「一年水位進出前／後 5% 分位」，只在換帶那天發卡（`state.json.fred_bands`）。
- 沒有時間戳的新聞（Nikkei Asia RSS）改用 `state.json.seen_news` 判新舊：首跑全收，之後只留第一次出現的，7 天後遺忘。
- `udn_money` 的 RSS 回 200 但零條，換成鉅亨網頭條 `cnyes_headline`（有日期、40 條）。

## Stage 1（haiku 分類）／Stage 2（sonnet 摘要）／orchestrator（2026-08-19 新增）

對應 DESIGN.md §6（最省資源六原則）／§7（正確性五道）／§10（每天怎麼跑）／
§11（卡片 schema）。四個新檔：

| 檔案 | 角色 |
|---|---|
| `llm.py` | Claude Code CLI headless 呼叫封裝（`run_claude(system, user, model, label, ledger, card_count)`），照抄 `morning-briefing/briefing/ai_processor.py::_call_claude_code` 已驗證過的模式：`claude -p --output-format json --model <m> --system-prompt … --allowed-tools ""`、stdin=user prompt、解析 envelope、重試 ×3（帶「上次不是 JSON」guard）、`MAX_THINKING_TOKENS=0`、子行程 env 一律拿掉 `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_BASE_URL`（否則 CLI 會改用 API key 計費，見同檔 2026-08-17 事故記載）。內建 `Ledger`：依 DESIGN §6 模型表的**卡片數**硬上限（haiku ≤200／日、sonnet ≤60／日，不是 token 上限）擋下超額呼叫，記 `capped:true`，寧可漏不爆額度。 |
| `common.py` | 共用常數／路徑／小工具：13 維度 key 與中文 label、`source_id → 人類可讀名稱`（`sources.yml` ＋ onsite/FRED 特判）、JSON 讀寫。 |
| `classify.py` | Stage 1（haiku）：`kind=="data"` 的卡片（onsite monitor/regime/rotation/crowding/kill-watch、FRED）**全程零 LLM**，Python 直接判 `relevant/level/category/importance_guess`；其餘卡片 batch ~25 條送 haiku，回 `relevant/level/category/tickers/themes/headline_ok/is_rumor/importance_guess`。Python 決定性後規則（非模型判斷）：**T4-only ⇒ importance_guess 上限 2**；`headline_ok=false ⇒ checks.headline_mismatch=true`。選 ≤60 條進 stage 2，依 `(importance_guess desc, tier asc, corroboration desc, recency desc)` 排序，log 被丟掉的張數。 |
| `summarize.py` | Stage 2（sonnet）：對選出的 ≤60 張卡逐張補 `summary_zh`/`why_zh`/`importance`/`forecast`（`kind=="data"` 一樣零 LLM，直接從 title 產生）；**`importance==3`（🔴）在 Python 端強制檢查 corroboration≥2 或 source_tier=="T1"，不合格降到 2**（DESIGN §7 規則 3／§8 T4 單獨不得 🔴，不管 LLM 說了什麼）。另有一次 sonnet 呼叫產出 `gauges`（13 維度儀表，`_canonicalize_gauges()` 只信任模型的 `status/value/delta`，`category`/`label` 一律由 Python 覆寫，保證順序與字面正確）／`brief_zh`（5–8 段早報，寫完跑 `sanitize_brief_html()` allow-list，只留 `<a href>`/`<b>`/`<span class="n">`）／`flags`（轉折提醒，候選由 `build_flag_candidates()` 在 Python 端從 kill-watch near/breached、regime 標籤變化算好，LLM 只負責把候選寫成中文句子，不得新增）。`build_calendar()` 完全不經 LLM：讀 `docs/monitor/data/macro_calendar.json` ＋ `docs/catalyst/calendar.json` 未來 7 天的事件合併。 |
| `run_daily.py` | Orchestrator：`fetch.py`（可 `--skip-fetch`）→ `classify()` → `summarize_cards()`＋`build_digest()`＋`build_calendar()` → 寫 `docs/intel/data/{date}.json` → `render.py --date {date}`（若已存在；尚未存在時印警告不擋）。**`CLAUDE_CODE_OAUTH_TOKEN` 沒設就整段跳過 LLM**，只保留 `kind=="data"` 卡片＋日曆，輸出 `"llm":"unavailable"`，仍 exit 0（頁面照樣能更新）。只有真的連 JSON 都寫不出來才回非 0。 |

### 怎麼獨立跑 / 除錯

```bash
# stage 1：對前 10 張 pending 卡跑 haiku（本機已登入 claude 時可用 CLAUDE_CODE_USE_LOCAL_AUTH=1 代替 OAuth token）
CLAUDE_CODE_USE_LOCAL_AUTH=1 python3 scripts/intel/classify.py --date 2026-08-19 --limit 10 --out /tmp/classify-debug.json

# stage 2：對 classify.py 輸出的 selected 卡跑 sonnet
CLAUDE_CODE_USE_LOCAL_AUTH=1 python3 scripts/intel/summarize.py --date 2026-08-19 --selected /tmp/classify-debug.json --out /tmp/summarize-debug.json

# 全流程（GHA 用這個）
CLAUDE_CODE_OAUTH_TOKEN=xxx python3 scripts/intel/run_daily.py --date 2026-08-19 --skip-fetch
```

`classify.py`/`summarize.py` 的 CLI 只寫到 `--out` 指定的除錯路徑，不會動
`docs/intel/data/{date}.json`（那是 `run_daily.py` 唯一的寫入者）。

### 成本與額度（95 條候選卡的實測估算，2026-08-19）

- haiku 一批 25 條實測 ≈28k input token（含 CLI 固定開銷與 system prompt cache
  creation，同一 batch 內第一次呼叫較貴，後續 batch 若命中 prompt cache 會更
  便宜）／~600 output token；95 條候選中約 70 條非 data 卡需要 haiku，分 3 批
  ≈ 80–90k token／日，遠低於 haiku ≤200 卡／日的硬上限（卡片數上限先於 token
  量觸發保護）。
- sonnet 一批 10 條實測 ≈35k input／1.4k output token；≤60 條分 6 批
  ≈ 210k token／日；加上一次 digest 呼叫（gauges/brief_zh/flags）
  ≈ 39k input／2.2k output ≈ 41k；合計 sonnet ≈ 250k token／日。
- `Ledger.to_status_dict()` 把上述數字寫進當日 JSON 的 `status.tokens`（實際
  token，不是估算值），`status.capped` 標示今天是否撞到卡片數硬上限。
- Claude Code CLI 走 `CLAUDE_CODE_OAUTH_TOKEN`（`claude setup-token` 產生的
  長效 token）＝ Max/Pro 訂閱月租，不計 API 額度；GitHub secret 名稱固定
  `CLAUDE_CODE_OAUTH_TOKEN`，workflow 絕不能同時帶 `ANTHROPIC_API_KEY`（否則
  CLI 會改用 API key 計費，`llm.py::_cli_env()` 已從子行程 env 拿掉，
  workflow 裡也額外 `unset` 一次雙保險）。

### GHA workflow

`.github/workflows/intel-daily.yml`：cron `0 22 * * 0-4` UTC（＝06:00 TPE
週一到週五）＋ `workflow_dispatch`；`concurrency: intel-daily`；
`permissions: contents: write`；`timeout-minutes: 25`。步驟＝checkout →
`pip install feedparser pyyaml requests` → 算 TPE 日期 → `fetch.py` →
`npm install -g @anthropic-ai/claude-code`（`continue-on-error: true`，裝不
起來就讓 LLM 步驟自然降級，不擋 pipeline）→ `run_daily.py --skip-fetch`
（帶 `CLAUDE_CODE_OAUTH_TOKEN` secret）→ commit＋push `docs/intel/`（照抄
`monitor-daily.yml` 的 rebase-retry push idiom 與 bot author，未裝 pre-commit
hook 的 GHA 環境不需要 `--no-verify`）。
