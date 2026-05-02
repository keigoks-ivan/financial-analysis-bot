# SEMI_EVIDENCE SPEC.md
# 半導體 ID 寫稿 evidence pool（PDF / 簡報 / 法說會錄音 / 技術論文）
# 版本：v1.0 | 日期：2026-05-02
# 目標：補足 `/id/` 報告寫稿時的 primary-source 資料層

---

## 0. 背景與動機

### 現況問題

寫 ID（Industry DD）時，現有資料來源以「網頁 HTML + earnings press release + 二手新聞轉述」為主，下列高價值來源**實際上拿不到**：

- **投資人日 / Capital Markets Day deck**（PDF，藏在 IR events 頁；WebFetch 抓回是 wrapper 不是內容）
- **法說會 Q&A 音訊**（webcast 錄影，沒有 PDF；音訊裡的 framing 訊號最高）
- **技術論文 / 會議簡報**（IEDM / ISSCC / VLSI / TSMC Tech Symposium，PDF 多在會議 archive）
- **券商產業報告**（GS / MS / Jefferies，須客戶門戶下載）
- **付費深度報告**（SemiAnalysis / Yole / TechInsights，paywall）

結果是 ID 引用的「primary 比例」實際上比表面看起來低，深度受限於可 render HTML 的來源。

### 本 spec 目標

建立 `evidence/` 目錄與 fetcher pipeline，做兩件事：

1. **自動 fetch**：寫 ID 時對相關 ticker 自動拉 EDGAR 8-K + IR deck + YouTube 法說會音訊 + arXiv paper
2. **手動 ingest**：使用者把券商報告 / 付費深度報告 upload 到 `evidence/inbox/`，下次寫 ID 時自動歸位

### 核心原則

- **不放 `docs/`**：`docs/` 整個 ship 到 `research.investmquest.com/`，把第三方 / NDA 內容放進去會違反著作權
- **本地讀取，零外部 API extraction**：用 Claude Code session 內建的 `Read` tool 讀 PDF（支援分頁），不另寫 vision extraction script、不呼叫 Anthropic API
- **Whitelist 自然成長**：不預先灌 100 家 ticker；寫到誰收誰，auto-discover + user confirm
- **慢的非阻塞**：YouTube 轉文字 30 分鐘/場，背景跑，不卡寫稿

---

## 1. 資料夾結構

```
~/financial-analysis-bot/evidence/         ← 整個 .gitignore（除 manifest）
├── ir_decks/                              ← 公司 IR / 投資人日 / earnings deck
│   ├── NVDA_2026Q1_earnings.pdf
│   ├── TSM_TechSymposium2026.pdf
│   └── ASML_CMD2024.pdf
├── tech_papers/                           ← arXiv + 會議論文
│   ├── arxiv_2603.12345_HBM4_thermal.pdf
│   └── IEDM2025_TSMC_N2_paper.pdf
├── transcripts/                           ← YouTube + whisper 產出
│   ├── raw/                               ← 原始 mp3
│   │   └── NVDA_GTC2026_keynote.mp3
│   └── txt/                               ← whisper 轉文字
│       └── NVDA_GTC2026_keynote.txt
├── broker_reports/                        ← user upload only
│   └── GS_Semis_2026Q1.pdf
├── industry_research/                     ← user upload（付費深度）
│   └── SemiAnalysis_AdvPackaging_2026.pdf
├── inbox/                                 ← user 拖檔，下次寫 ID 時自動歸位
└── manifest.jsonl                         ← 索引（git-tracked，不含原檔）
```

`.gitignore` 規則：

```
evidence/**
!evidence/manifest.jsonl
!evidence/.gitkeep
!evidence/tickers.json
```

---

## 2. Whitelist（`evidence/tickers.json`）

### Schema

```json
{
  "tickers": [
    {
      "ticker": "NVDA",
      "name": "NVIDIA Corporation",
      "cik": "0001045810",
      "ir_url": "https://investor.nvidia.com/financial-info/quarterly-results/",
      "ir_events_url": "https://investor.nvidia.com/events/",
      "youtube_channel": "NVIDIA",
      "industry": ["semi", "AI_accelerator"],
      "active": true,
      "added_at": "2026-05-02",
      "added_by": "manual_v1"
    }
  ]
}
```

### v1 初始名單（10 家半導體）

```
NVDA / TSM / ASML / AMD / AVGO / INTC / MU / AMAT / LRCX / KLAC
```

CIK 與 IR URL 在動手 Step 2 時逐家 verify，不依賴本 spec 的估值。

### 必要欄位

- `ticker`、`name`、`cik`、`ir_url`、`industry`、`active` 是 required
- `ir_events_url`、`youtube_channel` 是 optional（沒有則對應 fetcher 跳過）
- `deprecated_reason`、`absorbed_into` 是 inactive 條目用

---

## 3. Fetchers（6 個 module）

| # | 模組 | 來源 | 範圍 | 依賴 | Critical |
|---|---|---|---|---|---|
| 1 | `edgar_fetcher.py` | SEC EDGAR API | 8-K + EX-99 PDFs，過去 4 季 | `requests`，免 key | ✅ |
| 2 | `ir_fetcher.py` | per-ticker IR 頁面 | 投資人日 / CMD / quarterly + events 雙頁面 | `requests` + `bs4` | ✅ |
| 3 | `youtube_transcript.py` | YouTube webcast | audio → transcript | `yt-dlp` + `whisper.cpp` | ✅ |
| 4 | `arxiv_fetcher.py` | arXiv API | 半導體相關 paper，過去 180 天 | `arxiv` package | |
| 5 | `web_fallback.py` | WebSearch + WebFetch | Tier 1-4 沒命中時補一刀 | 無 | |
| 6 | `inbox_classifier.py` | inbox/ 自動歸位 | 開檔識別 → 移檔 → 寫 manifest | in-session `Read` 即可 | |

### IR Fetcher 雙頁面

每筆 ticker 抓 2 個 URL：

- `ir_url`（quarterly results）→ 抓最近 4 季 earnings deck
- `ir_events_url`（events / presentations）→ 抓投資人日 / CMD / 會議 keynote

### EDGAR 範圍

- Forms: `8-K`
- Lookback: 過去 90 天（≈ 1 季 + 緩衝）
- Exhibits filter: `EX-99.1` (press release)、`EX-99.2` (deck)
- 解析方式: 走 `data.sec.gov/submissions/CIK<NNN>.json` → filter forms → fetch index → grep EX-99 PDFs

### Web Fallback 觸發條件

僅在 Tier 1-3 全部 miss 時觸發。query pattern:

```
"<company> investor day 2026 filetype:pdf site:investor.<domain>"
"<ticker> earnings call presentation 2026Q1 filetype:pdf"
```

---

## 4. Manifest Schema（`manifest.jsonl`）

每行一筆 JSON：

```json
{
  "path": "ir_decks/NVDA_2026Q1_earnings.pdf",
  "ticker": "NVDA",
  "source_type": "earnings_deck",
  "title": "NVIDIA Q1 FY26 Earnings Presentation",
  "date": "2026-02-26",
  "added_by": "edgar_fetcher",
  "fetched_from": "https://www.sec.gov/Archives/edgar/data/1045810/.../ex-99-2.pdf",
  "sha256": "abc...",
  "tags": ["AI_accelerator", "Blackwell"],
  "added_at": "2026-05-02T...",
  "page_count": 28
}
```

### Enums

- `source_type`：`earnings_deck` / `investor_day` / `capital_markets_day` / `tech_paper` / `conference_keynote` / `transcript_audio` / `broker_report` / `industry_research` / `whitepaper` / `other`
- `added_by`：`edgar_fetcher` / `ir_fetcher` / `youtube_transcript` / `arxiv_fetcher` / `web_fallback` / `user_upload` / `inbox_classifier`

---

## 5. YouTube 轉文字流程

### 依賴安裝

```bash
brew install yt-dlp whisper-cpp
# whisper.cpp model（兩個都裝，按場合切）
sh ./models/download-ggml-model.sh medium.en      # 英文 webcast
sh ./models/download-ggml-model.sh medium         # multilingual（TSMC 中文法說會）
```

### Pipeline

```bash
yt-dlp -x --audio-format mp3 \
  -o "evidence/transcripts/raw/<ticker>_<event>.mp3" <youtube_url>

whisper-cli -m models/ggml-medium[.en].bin \
  -f "evidence/transcripts/raw/<ticker>_<event>.mp3" \
  -otxt -of "evidence/transcripts/txt/<ticker>_<event>"
```

### 模型策略

- 預設 `ggml-medium`（multilingual） — 適用所有場合
- 若確定純英文 webcast，可指定 `ggml-medium.en` 加速 1.5x
- 1 小時 webcast 約跑 20-40 分鐘（Mac M 系列）

### 觸發條件

不對所有 ticker 全跑 — 只挑 ID 主題最相關的 **top 3-5 ticker** 的最近一場 earnings call 或 investor day。

---

## 6. Prefetch 策略（Hybrid，prefetch 為主）

### Phase 0a：Candidate ticker（~10 秒）

ID 主題敲定 → 我列出候選 ticker（10-15 家寬鬆名單） → 對每家 grep `manifest.jsonl`，30 天內已有則 skip

### Phase 0b：Fast fetchers（~2 分鐘，平行）

對 missing ticker 同時跑：
- `edgar_fetcher` 過去 4 季 8-K + EX-99
- `ir_fetcher` 雙頁面（quarterly + events）
- `arxiv_fetcher`（針對 ID 主題 keyword 而非 ticker）

平行 10 家 ticker，總時 < 2 分鐘

### Phase 0c：Slow transcripts（背景非阻塞）

對 top 3-5 ticker 跑 `youtube_transcript`，背景 30 分鐘內完成。**不阻塞 Phase 1 寫稿**。

### Phase 1：研究 + 寫稿 §1-§9

我用已 fetch 完的 evidence + WebSearch + WebFetch 寫稿。背景 transcript 完成後可被 §10/§11 引用。

### Phase 2：§11 ticker list 確認

最終 ticker list 中若有 Phase 0a 沒列到的（晚加的） → lazy fetch 該 ticker（單家通常 < 30 秒）

### 例外：單家 ID

若 ID 主題只關 1 家公司（如 ASML High-NA EUV 專題），prefetch 退化成單家撈 — 沒分階段意義，直接撈完開寫。

---

## 7. industry-analyst Skill 整合點

### Hook 1：§0 開場（pre-research）

```
1. 列出 ID 預計涵蓋的 candidate ticker（10-15 家）
2. fetch_chain(ticker) for each
   → grep manifest → EDGAR → IR → YouTube (background)
3. 列「missing 清單」給使用者：哪些 ticker 抓不到，請補 upload
4. 進 Phase 1 開始研究
```

### Hook 2：§11 關聯個股清單（write-time）

```
For each ticker in §11:
  hits = grep_manifest(ticker)
  for hit in hits:
    Read(hit.path)  ← 分頁讀，session 內結構化
  cite as: [evidence: <hit.path> p.<N>]
```

### Hook 3：§3 / §5 主題層 reading

```
For topic keywords (e.g., "HBM", "CoWoS"):
  hits = grep_manifest_by_tag(topic)
  Read(hit.path) for relevant ones
```

### Citation 規範

引用 evidence 的句子在 footnote 寫：

```
[evidence: ir_decks/NVDA_GTC2026.pdf p.23]
[evidence: transcripts/txt/TSM_2025Q4_call.txt L.412-428]
```

方便 `id-review` skill / critic agent 回查驗證。

---

## 8. Whitelist 擴充策略

### 情境 A：同產業加新 ticker（最常見）

例：寫 ID 涵蓋 MRVL / NXPI / ON / TXN / SK Hynix / Samsung / TEL / Disco / SMIC / UMC

**機制：auto-discover with user confirm**

寫 ID Phase 0a 列候選 ticker，發現 `tickers.json` 沒有的條目時：

```
1. 自動解析 CIK
   → SEC EDGAR company search API
   → 抽 10 位 CIK

2. 自動猜 IR URL（試 5 種 pattern）
   - investor.<domain>
   - <domain>/investors
   - <domain>/en/investors
   - ir.<domain>
   - <domain>/investor-relations
   → HEAD request 第一個回 200 的當 ir_url

3. 自動搜 YouTube channel
   → WebSearch "<company> official YouTube channel"
   → 抽 channel handle

4. 全綠 → 列出來給使用者 confirm 一次
   "NEW: MRVL → CIK 0001835632, IR https://..., YT @MarvellTech, OK?"
   → confirm 後 append tickers.json
   → 不 confirm / 抓不到 → 標 incomplete，跳過 fetcher，留給使用者手動填
```

**關鍵**：tickers.json 不預先大量灌，**寫 ID 時遇到誰，誰就被收進來**，自然成長。

### 情境 B：新產業（非半導體）

例：之後寫 GLP-1 ID、核融合 ID

**機制：per-industry recipe pack**

`tickers.json` 每筆 entry 加 `industry` 標籤（陣列，可多分類）。但 fetchers 結構要分層：

```
fetchers/
├── common/                              ← 全產業共用
│   ├── edgar_fetcher.py
│   ├── ir_fetcher.py
│   └── youtube_transcript.py
└── industry/
    ├── semi/                            ← v1
    │   ├── arxiv_filters.py             ← cs.AR / eess.SP
    │   └── conferences.py                ← IEDM / ISSCC / VLSI / TSMC TS
    ├── biotech/                         ← v2 才加
    │   ├── clinicaltrials_fetcher.py
    │   └── conferences.py                ← ASCO / AHA / AACR / ESMO
    └── energy/                          ← v3 ...
```

**寫第一份非半導體 ID 時才補對應 industry pack**，不要預先寫空殼。

### 情境 C：條目腐敗（deprecation）

公司被併、下市、改名、CIK 換了 → 標 inactive 不刪除：

```json
{
  "ticker": "XLNX",
  "active": false,
  "deprecated_reason": "acquired by AMD 2022",
  "absorbed_into": "AMD"
}
```

保留歷史 ID 引用的可追溯性，fetcher 跳過。

### 維護工具（v2 視需要）

- `validate_tickers.py` — 跑全表，檢查 CIK / IR URL / YouTube 還活著，產 broken list
- `dedupe_tickers.py` — 同公司不同 ticker（class A/B、ADR vs 本地）合併
- CI weekly 跑一次 validator，broken 開 issue 給 review

### 實際擴充路徑（時間軸）

```
Now (v1)                          → 10 家半導體 hard-coded
寫第 12-15 份 semi ID 之後        → 自然成長到 25-40 家半導體
寫第一份 biotech ID 時            → 補 fetchers/industry/biotech/，加 8-15 家
寫第一份 consumer / fin ID 時     → 補對應 industry pack
```

---

## 9. 各種來源品質定位

### 訊號深度排序（從高到低）

```
Q&A audio transcript (whisper)    ← 最高訊號，最難取得
  ↓
Investor Day / CMD deck            ← 多年 strategic roadmap
  ↓
Earnings deck (8-K EX-99.2)        ← 季度量化錨
  ↓
Earnings press release (EX-99.1)   ← 法律精確但 sanitized
  ↓
News article 二手轉述              ← 雜訊比高
```

### EDGAR 8-K vs Investor Day deck 對比

| 維度 | EDGAR 8-K + EX-99 | Investor Day / CMD |
|---|---|---|
| 取得難度 | 極低（API 結構化） | 高（IR events 頁，要爬） |
| 頻率 | 4x/年/家（必發） | 1-3 年一次 |
| 頁數 | 15-30 頁 | 60-150 頁 |
| 內容 | 季度量化 + 1Q 短 guidance | 多年 roadmap + capacity ramp |
| Sanitize 程度 | 高（10b 法律審閱） | 中 |
| Q&A | ❌ 沒有 | ❌ 沒有 |
| 適合 ID 章節 | §6 財務 / §10 catalyst | §3 roadmap / §5 value chain / §10.5 |

**兩者互補不互替** — 寫一份好 ID 兩者都要。

---

## 10. 實作順序（v1）

```
Step 1: 建 evidence/ 結構 + .gitignore + 空 manifest + tickers.json    ← 5 分鐘
Step 2: 寫 edgar_fetcher.py，verify 10 家 CIK，dry-run               ← 1 hr
Step 3: 寫 ir_fetcher.py（先做 NVDA + TSM 兩家當 template）           ← 1.5 hr
Step 4: 寫 youtube_transcript.py + 裝 whisper.cpp + 跑一場 NVDA GTC   ← 2 hr
Step 5: 寫 arxiv_fetcher.py                                          ← 30 min
Step 6: 寫 web_fallback.py                                           ← 30 min
Step 7: 串 fetch_for_ticker() / fetch_for_topic() orchestrator       ← 1 hr
Step 8: 改 industry-analyst skill 加 hook（§0/§3/§5/§11）             ← 30 min
Step 9: 用一份未寫過的產業 ID end-to-end 驗收                          ← 半天
```

**總時 ~7-8 小時**。Critical path 是 Step 1-4（~5 hr），完成後就能驗證核心價值。

---

## 11. 驗收標準

- [ ] EDGAR fetcher 對 10 家 ticker 正確抓 8-K + EX-99，PDF 可開啟
- [ ] IR fetcher 對 NVDA + TSM 雙頁面正確抓投資人日 deck
- [ ] YouTube transcript 對 1 場 NVDA GTC 完成轉文字（多語言模型 OK）
- [ ] arXiv fetcher 對 "HBM" / "CoWoS" 正確抓過去 180 天 paper
- [ ] manifest.jsonl 每筆有完整必要欄位
- [ ] inbox 裡 user upload PDF，下次寫 ID 時自動歸位、寫 manifest
- [ ] industry-analyst skill 寫一份新 ID 時：Phase 0a/0b 觸發、§11 寫稿時 cite evidence path
- [ ] `.gitignore` 確實排除 evidence/，但保留 manifest.jsonl

---

## 12. 邊界（不做）

- ❌ Vision LLM extraction（pdftotext + Sonnet API）— 改用 in-session `Read` tool
- ❌ Supabase / 任何 DB — JSON manifest in repo 即可
- ❌ Cron 自動 fetch — 使用者觸發 / ID 寫稿觸發
- ❌ Tier 分級 quality gate（spec v0 的 S/A/B/C/X）— whitelist + 用途分類即可
- ❌ Frontend 展示頁面（`/semi-intel/`）— 這是寫稿 evidence pool，不是公開展示
- ❌ Cross-industry fetcher（biotech / energy）— v2 視第一份非半導體 ID 需求再補
- ❌ 付費 paywall 突破 — SemiAnalysis / IEEE / 券商門戶都靠 user upload

---

## 13. 與既有 SEMI_INTEL_SPEC 的關係

`/Users/ivanchang/Documents/SEMI_INTEL_SPEC.md`（2026-05-02 較早版本）目標是建一套 RSS-driven daily news pipeline 餵 morning-briefing。

本 spec **不取代它**，但 scope 限縮：

| 維度 | SEMI_INTEL_SPEC | SEMI_EVIDENCE_SPEC（本檔） |
|---|---|---|
| 主用途 | 取代 morning-briefing 的 Tavily 雜訊 | 補 ID 寫稿的 primary-source 深度 |
| 節奏 | Daily（6h RSS poll） | 寫稿觸發 / user upload |
| 內容 | RSS summary + 8-K headline | 完整 PDF + audio transcript |
| 儲存 | Supabase | 本地 evidence/ + jsonl manifest |
| 抽取 | Haiku classifier | 無（in-session Read） |
| 成本 | ~$1.5/月 | ~$0/月（whisper 本地，無 API） |
| 受益方 | morning-briefing | `/id/` |

兩者**正交不衝突**。SEMI_INTEL 適合做 morning-briefing 的升級；SEMI_EVIDENCE 適合做 ID 寫稿的深度補強。先做哪個看哪個痛點優先。

---

*本 SPEC 基於 2026-05-02 與使用者的對話整理。*
*v1 scope 限定半導體產業；biotech / energy / 其他產業擴充屬 v2+。*
*動工前最後審閱：作者確認 → 才進入 Step 1。*
