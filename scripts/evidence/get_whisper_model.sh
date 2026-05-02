#!/usr/bin/env bash
# Download a whisper.cpp ggml model to ~/.local/share/whisper.cpp/models/
# Usage:
#   bash scripts/evidence/get_whisper_model.sh           # default: medium (multilingual, ~1.5GB)
#   bash scripts/evidence/get_whisper_model.sh medium.en # English-only, ~1.5GB, faster
#   bash scripts/evidence/get_whisper_model.sh base.en   # smaller, ~150MB, lower quality
#   bash scripts/evidence/get_whisper_model.sh large-v3  # best quality, ~3GB
set -euo pipefail

MODEL="${1:-medium}"
DEST_DIR="${HOME}/.local/share/whisper.cpp/models"
DEST_FILE="${DEST_DIR}/ggml-${MODEL}.bin"
URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-${MODEL}.bin"

mkdir -p "$DEST_DIR"

if [[ -f "$DEST_FILE" ]]; then
  echo "[OK] Already exists: $DEST_FILE"
  ls -lh "$DEST_FILE"
  exit 0
fi

echo "[*] Downloading ggml-${MODEL}.bin → $DEST_FILE"
echo "[*] Source: $URL"
curl -L --fail --progress-bar "$URL" -o "$DEST_FILE.partial"
mv "$DEST_FILE.partial" "$DEST_FILE"

echo "[OK] Downloaded:"
ls -lh "$DEST_FILE"
