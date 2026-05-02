# scripts/evidence — Evidence Pool Fetchers

Fetches primary-source PDFs, earnings decks, arXiv papers, and YouTube transcripts for the `evidence/` directory, which backs the `/id/` Industry DD writing workflow.

## Install Prerequisites

```bash
# Python packages
pip install requests beautifulsoup4 arxiv

# yt-dlp (YouTube audio download)
brew install yt-dlp

# whisper.cpp (local speech-to-text)
brew install whisper-cpp

# Download Whisper models (run once after install)
# Models are stored in $(brew --prefix whisper-cpp)/share/whisper.cpp/models/

# Option A: multilingual (recommended — works for both English and Chinese earnings calls)
cd "$(brew --prefix whisper-cpp)/share/whisper.cpp/models"
bash download-ggml-model.sh medium

# Option B: English-only (~1.5x faster, use for NVDA/AMD/ASML/etc.)
bash download-ggml-model.sh medium.en
```

## Modules

| Module | Tier | What it does |
|---|---|---|
| `edgar_fetcher.py` | 1 | SEC EDGAR 8-K + EX-99.1/EX-99.2 PDFs via EDGAR JSON API |
| `ir_fetcher.py` | 2 | IR page scrape (NVDA + TSM fully implemented; others via generic fallback) |
| `youtube_transcript.py` | — | YouTube audio download (yt-dlp) + Whisper transcription |
| `arxiv_fetcher.py` | 3 | arXiv semiconductor papers (cs.AR / eess.SP) |
| `web_fallback.py` | 4 | WebSearch + WebFetch query builder (used inside Claude Code agent session) |
| `orchestrator.py` | all | Chains Tier 1→2→3→4; `fetch_for_ticker()` / `fetch_for_topic()` entry points |

## Quick Start

```bash
# Fetch EDGAR 8-K + IR decks for NVDA (dry run to see what's available)
python scripts/evidence/edgar_fetcher.py NVDA --dry-run

# Fetch and download 1 NVDA 8-K from past 90 days
python scripts/evidence/edgar_fetcher.py NVDA --days 90

# List NVDA + TSM IR PDFs without downloading
python scripts/evidence/ir_fetcher.py NVDA TSM --list-only

# Search arXiv for HBM papers (past 30 days)
python scripts/evidence/arxiv_fetcher.py --query "HBM" --days 30 --list-only

# Full prefetch for NVDA (Tier 1 + 2)
python scripts/evidence/orchestrator.py NVDA

# Full prefetch for all active tickers
python scripts/evidence/orchestrator.py --all

# Topic-based arXiv fetch
python scripts/evidence/orchestrator.py --topic "HBM" "CoWoS"

# Transcribe a YouTube earnings call
python scripts/evidence/youtube_transcript.py \
    --url https://www.youtube.com/watch?v=XXXX \
    --ticker NVDA \
    --event GTC2026_keynote \
    --model medium

# Verify youtube_transcript.py imports + tools available
python scripts/evidence/youtube_transcript.py --import-test
```

## Evidence Layout

```
evidence/
├── ir_decks/          ← EDGAR EX-99 + IR page PDFs
├── tech_papers/       ← arXiv + conference papers
├── transcripts/
│   ├── raw/           ← Downloaded mp3 audio
│   └── txt/           ← Whisper transcripts (.txt)
├── broker_reports/    ← User upload only (not fetched)
├── industry_research/ ← User upload only (not fetched)
├── inbox/             ← Drop any PDF here; inbox_classifier.py moves it
├── manifest.jsonl     ← Git-tracked index (no PDFs in git)
└── tickers.json       ← Whitelist of 10 semiconductor companies
```

## Manifest Format

One JSON line per downloaded file:

```json
{
  "path": "ir_decks/NVDA_20260226_EX-99_2_ex-99-2.pdf",
  "ticker": "NVDA",
  "source_type": "earnings_deck",
  "title": "NVDA 2026-02-26 EX-99.2",
  "date": "2026-02-26",
  "added_by": "edgar_fetcher",
  "fetched_from": "https://www.sec.gov/Archives/edgar/data/1045810/.../ex-99-2.pdf",
  "sha256": "abc123...",
  "tags": ["semi", "AI_accelerator"],
  "added_at": "2026-05-02T10:00:00+00:00",
  "page_count": null
}
```

`page_count` is populated when the Claude Code agent reads the PDF with the `Read` tool (it reports page count for PDFs).

## Adding a New Ticker

1. Add entry to `evidence/tickers.json` (verify CIK from [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany))
2. Add a recipe function `scrape_<TICKER>()` in `ir_fetcher.py` (or use the generic fallback)
3. Run `python scripts/evidence/orchestrator.py <TICKER>` to prefetch

## Notes on Whisper Models

- `medium` (multilingual): best for TSMC, SK Hynix calls with Chinese/Korean content
- `medium.en` (English-only): 1.5x faster; use for NVDA, AMD, ASML, Intel
- Runtime on Apple Silicon M-series: ~20-40 min per 1 hour of audio
- Models are large (~1.5 GB each); stored locally by brew, not in this repo

## Rate Limits

- SEC EDGAR: 10 requests/second max (edgar_fetcher.py sleeps 120ms between calls)
- arXiv: 3 second delay between requests (built into `arxiv` library client)
- IR pages: 300ms between requests (ir_fetcher.py)
