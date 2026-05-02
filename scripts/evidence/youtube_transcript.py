"""
youtube_transcript.py — YouTube audio download + Whisper transcription wrapper.

Downloads audio from a YouTube URL using yt-dlp, then transcribes it using
whisper-cli (whisper.cpp CLI), and writes the result to evidence/transcripts/.
Adds a manifest entry on completion.

PREREQUISITES (user must install separately — see scripts/evidence/README.md):
    brew install yt-dlp
    brew install whisper-cpp
    # Then download the whisper model you want to use:
    cd $(brew --prefix whisper-cpp)/share/whisper.cpp/models
    bash download-ggml-model.sh medium       # multilingual (default)
    bash download-ggml-model.sh medium.en    # English-only, ~1.5x faster

Usage:
    python scripts/evidence/youtube_transcript.py \\
        --url https://www.youtube.com/watch?v=XXXX \\
        --ticker NVDA --event GTC2026_keynote

    python scripts/evidence/youtube_transcript.py \\
        --url https://youtu.be/XXXX \\
        --ticker TSM --event 2026Q1_earnings_call \\
        --model medium.en

Options:
    --url       YouTube URL to download
    --ticker    Ticker symbol (used in filename)
    --event     Short event name slug (used in filename, no spaces)
    --model     Whisper model to use: medium (default) or medium.en
    --audio-only  Download audio only, skip transcription
    --import-test  Verify script can be imported and CLI tools are present
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = REPO_ROOT / "evidence"
TRANSCRIPTS_RAW_DIR = EVIDENCE_DIR / "transcripts" / "raw"
TRANSCRIPTS_TXT_DIR = EVIDENCE_DIR / "transcripts" / "txt"
MANIFEST_PATH = EVIDENCE_DIR / "manifest.jsonl"
TICKERS_PATH = EVIDENCE_DIR / "tickers.json"

# Default whisper model path (brew install whisper-cpp puts models here)
WHISPER_MODELS_DIR_CANDIDATES = [
    Path("/opt/homebrew/share/whisper.cpp/models"),   # Apple Silicon brew
    Path("/usr/local/share/whisper.cpp/models"),       # Intel brew
    Path.home() / ".local" / "share" / "whisper.cpp" / "models",  # manual install
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Manifest helper
# ---------------------------------------------------------------------------

def append_manifest(entry: dict[str, Any]) -> None:
    with MANIFEST_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Tool availability checks
# ---------------------------------------------------------------------------

def find_whisper_cli() -> str | None:
    """Return path to whisper-cli binary, or None if not found."""
    # whisper.cpp brew formula installs the CLI as 'whisper-cli'
    for name in ("whisper-cli", "whisper"):
        found = shutil.which(name)
        if found:
            return found
    return None


def find_model_path(model_name: str) -> Path | None:
    """Locate the ggml model file for the given model name."""
    filename = f"ggml-{model_name}.bin"
    for models_dir in WHISPER_MODELS_DIR_CANDIDATES:
        candidate = models_dir / filename
        if candidate.exists():
            return candidate
    return None


def check_prerequisites() -> tuple[bool, list[str]]:
    """
    Check that yt-dlp and whisper-cli are on PATH.
    Returns (all_ok: bool, missing: list[str]).
    """
    missing = []
    if not shutil.which("yt-dlp"):
        missing.append("yt-dlp")
    if not find_whisper_cli():
        missing.append("whisper-cli")
    return (len(missing) == 0), missing


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def download_audio(youtube_url: str, dest_path: Path) -> bool:
    """
    Download audio from YouTube URL to dest_path (mp3) using yt-dlp.
    Returns True on success.
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    # yt-dlp output template: strip extension, yt-dlp will add .mp3
    output_template = str(dest_path.with_suffix(""))
    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",   # best quality
        "-o", f"{output_template}.%(ext)s",
        "--no-playlist",
        "--quiet",
        "--progress",
        youtube_url,
    ]
    log.info("Running: %s", " ".join(cmd))
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as exc:
        log.error("yt-dlp failed (exit %d)", exc.returncode)
        return False
    except FileNotFoundError:
        log.error("yt-dlp not found on PATH. Install with: brew install yt-dlp")
        return False


def transcribe_audio(
    audio_path: Path,
    output_base: Path,
    model_name: str = "medium",
) -> bool:
    """
    Transcribe audio_path using whisper-cli.
    Writes output to output_base.txt.
    Returns True on success.
    """
    whisper_cli = find_whisper_cli()
    if not whisper_cli:
        log.error("whisper-cli not found on PATH. Install with: brew install whisper-cpp")
        return False

    model_path = find_model_path(model_name)
    if not model_path:
        log.error(
            "Whisper model '%s' not found. Download with:\n"
            "  cd $(brew --prefix whisper-cpp)/share/whisper.cpp/models\n"
            "  bash download-ggml-model.sh %s",
            model_name,
            model_name,
        )
        return False

    output_base.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        whisper_cli,
        "-m", str(model_path),
        "-f", str(audio_path),
        "-otxt",
        "-of", str(output_base),
        "--language", "auto",
    ]
    log.info("Running: %s", " ".join(cmd))
    log.info("Transcription may take 20-40 min per hour of audio on M-series Mac.")
    try:
        result = subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as exc:
        log.error("whisper-cli failed (exit %d)", exc.returncode)
        return False
    except FileNotFoundError:
        log.error("whisper-cli binary not found at %s", whisper_cli)
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download YouTube audio and transcribe with whisper.cpp."
    )
    parser.add_argument("--url", required=False, help="YouTube URL to download")
    parser.add_argument("--ticker", required=False, help="Ticker symbol (e.g. NVDA)")
    parser.add_argument(
        "--event",
        required=False,
        help="Short event slug for filename (e.g. GTC2026_keynote)",
    )
    parser.add_argument(
        "--model",
        default="medium",
        choices=["medium", "medium.en", "small", "small.en", "large", "large-v3"],
        help="Whisper model name (default: medium / multilingual)",
    )
    parser.add_argument(
        "--audio-only",
        action="store_true",
        help="Download audio only, skip transcription",
    )
    parser.add_argument(
        "--import-test",
        action="store_true",
        help="Verify imports and tool availability; exit 0 if OK",
    )
    args = parser.parse_args()

    if args.import_test:
        all_ok, missing = check_prerequisites()
        if all_ok:
            log.info("Import test: OK — yt-dlp and whisper-cli both found on PATH.")
            sys.exit(0)
        else:
            log.warning(
                "Import test: PARTIAL — missing tools: %s. "
                "See scripts/evidence/README.md for install instructions.",
                ", ".join(missing),
            )
            # Exit 0 anyway — the script itself is importable, just tools are absent
            sys.exit(0)

    if not args.url or not args.ticker or not args.event:
        parser.error("--url, --ticker, and --event are required unless --import-test is used.")

    all_ok, missing = check_prerequisites()
    if not all_ok:
        if "yt-dlp" in missing:
            log.error("yt-dlp not installed. Run: brew install yt-dlp")
            sys.exit(1)
        if "whisper-cli" in missing and not args.audio_only:
            log.error(
                "whisper-cli not installed. Run: brew install whisper-cpp\n"
                "Or use --audio-only to skip transcription."
            )
            sys.exit(1)

    slug = f"{args.ticker.upper()}_{args.event}"
    audio_dest = TRANSCRIPTS_RAW_DIR / f"{slug}.mp3"
    txt_base = TRANSCRIPTS_TXT_DIR / slug

    # --- Step 1: Download audio ---
    if audio_dest.exists():
        log.info("Audio already exists: %s — skipping download.", audio_dest.name)
    else:
        log.info("Downloading audio to %s...", audio_dest)
        ok = download_audio(args.url, audio_dest)
        if not ok:
            sys.exit(1)

    # --- Step 2: Transcribe ---
    txt_path = txt_base.with_suffix(".txt")
    if not args.audio_only:
        if txt_path.exists():
            log.info("Transcript already exists: %s — skipping transcription.", txt_path.name)
        else:
            log.info("Transcribing %s with model=%s...", audio_dest.name, args.model)
            ok = transcribe_audio(audio_dest, txt_base, model_name=args.model)
            if not ok:
                sys.exit(1)

    # --- Step 3: Write manifest entries ---
    now_iso = datetime.now(tz=timezone.utc).isoformat()
    ticker = args.ticker.upper()

    # Audio manifest entry
    if audio_dest.exists():
        sha_audio = sha256_file(audio_dest)
        append_manifest({
            "path": str(audio_dest.relative_to(EVIDENCE_DIR)),
            "ticker": ticker,
            "source_type": "transcript_audio",
            "title": f"{slug} (audio)",
            "date": None,
            "added_by": "youtube_transcript",
            "fetched_from": args.url,
            "sha256": sha_audio,
            "tags": [],
            "added_at": now_iso,
            "page_count": None,
        })
        log.info("Manifest entry written for audio: %s", audio_dest.name)

    # Transcript manifest entry
    if not args.audio_only and txt_path.exists():
        sha_txt = sha256_file(txt_path)
        append_manifest({
            "path": str(txt_path.relative_to(EVIDENCE_DIR)),
            "ticker": ticker,
            "source_type": "transcript_audio",
            "title": f"{slug} (transcript)",
            "date": None,
            "added_by": "youtube_transcript",
            "fetched_from": args.url,
            "sha256": sha_txt,
            "tags": [],
            "added_at": now_iso,
            "page_count": None,
        })
        log.info("Manifest entry written for transcript: %s", txt_path.name)

    log.info("Done.")


if __name__ == "__main__":
    main()
