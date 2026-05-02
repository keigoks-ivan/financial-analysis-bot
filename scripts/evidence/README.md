# scripts/evidence — Evidence Pool Fetchers

> **🚫 DEPRECATED 2026-05-02** — `industry-analyst` skill v1.12 reverted the v1.11 evidence-pool hooks after same-day end-to-end validation failed. The fetchers below are kept as **dead code** (not invoked from any skill). Full post-mortem in `SEMI_EVIDENCE_SPEC.md` deprecation banner.
>
> **Standalone modules that are still occasionally useful**:
> - `arxiv_fetcher.py` — pull recent papers for a topic keyword. Can be called manually for narrow tech-deep ID work.
> - `get_whisper_model.sh` — bootstrap whisper.cpp model on a fresh machine. Independent of the rest.
> - `youtube_transcript.py` — transcribe a single known webcast URL when needed. Independent of manifest system.
>
> **Don't use the orchestrator / manifest / tickers.json system for new ID work** — that's what failed validation.

Fetches primary-source PDFs, earnings decks, arXiv papers, and YouTube transcripts for the `evidence/` directory, which backs the `/id/` Industry DD writing workflow.

## Install Prerequisites

```bash
# Python packages (use pip3 if `pip` is not on PATH)
pip3 install requests beautifulsoup4 arxiv

# yt-dlp (YouTube audio download)
brew install yt-dlp

# whisper.cpp (local speech-to-text)
brew install whisper-cpp
```

### Whisper model

The brew `whisper-cpp` formula (≥ 1.8.x) **no longer ships** the `download-ggml-model.sh` helper or pre-staged model files. Use the bundled helper script in this repo, which downloads from HuggingFace into `~/.local/share/whisper.cpp/models/` (where `youtube_transcript.py` looks):

```bash
# Default: medium (multilingual, ~1.5 GB) — works for TSMC/SK Hynix Chinese/Korean calls
bash scripts/evidence/get_whisper_model.sh

# Or explicit:
bash scripts/evidence/get_whisper_model.sh medium       # multilingual (default)
bash scripts/evidence/get_whisper_model.sh medium.en    # English-only, ~1.5x faster
bash scripts/evidence/get_whisper_model.sh base.en      # ~150 MB, lower quality
bash scripts/evidence/get_whisper_model.sh large-v3     # ~3 GB, best quality
```

The script is idempotent: re-running with an existing model is a no-op.

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
- Models are large (~1.5 GB each); stored in `~/.local/share/whisper.cpp/models/`, **not** in this repo (brew `whisper-cpp` ≥ 1.8.x ships only the binary, no models)
- `youtube_transcript.py` searches `/opt/homebrew/share/whisper.cpp/models/`, `/usr/local/share/whisper.cpp/models/`, and `~/.local/share/whisper.cpp/models/` in that order

## Rate Limits

- SEC EDGAR: 10 requests/second max (edgar_fetcher.py sleeps 120ms between calls)
- arXiv: 3 second delay between requests (built into `arxiv` library client)
- IR pages: 300ms between requests (ir_fetcher.py)
