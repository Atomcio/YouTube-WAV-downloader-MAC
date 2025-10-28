#!/usr/bin/env bash
set -euo pipefail

# YTWAV macOS Self-Repair Script
# Fixes common environment issues: Python/pip, yt-dlp, ffmpeg, PATH, cache.

info() { echo "[INFO] $*"; }
warn() { echo "[WARN] $*"; }
err()  { echo "[ERROR] $*"; }

# 1) Python & pip
info "Checking Python3..."
if ! command -v python3 >/dev/null 2>&1; then
  err "python3 not found. Install via Homebrew: brew install python@3.11"
  exit 1
fi
python3 --version || true

info "Upgrading pip..."
python3 -m pip install --upgrade pip || warn "pip upgrade failed"

# 2) Dependencies
info "Installing/Upgrading yt-dlp from requirements.txt..."
pip3 install -r "$(dirname "$0")/../requirements.txt" || warn "requirements install failed"

info "Ensuring yt-dlp is up to date..."
pip3 install --upgrade yt-dlp || warn "yt-dlp upgrade failed"

# 3) FFmpeg
info "Checking ffmpeg..."
if ! command -v ffmpeg >/dev/null 2>&1; then
  warn "ffmpeg not found. Installing via Homebrew..."
  if command -v brew >/dev/null 2>&1; then
    brew install ffmpeg || err "Homebrew install failed. Try: brew doctor"
  else
    err "Homebrew not found. Install from https://brew.sh/ and re-run this script."
    exit 1
  fi
else
  info "ffmpeg found: $(which ffmpeg)"
  info "Upgrading ffmpeg via Homebrew (optional)..."
  if command -v brew >/dev/null 2>&1; then
    brew upgrade ffmpeg || warn "brew upgrade ffmpeg failed"
  fi
fi

# 4) PATH tips for Apple Silicon
if [[ "$(uname -m)" == "arm64" ]]; then
  if ! echo "$PATH" | grep -q "/opt/homebrew/bin"; then
    warn "PATH may miss /opt/homebrew/bin. Add this to your shell config (e.g., ~/.zshrc):"
    echo 'export PATH="/opt/homebrew/bin:$PATH"'
  fi
fi

# 5) Clear yt-dlp cache
info "Clearing yt-dlp cache..."
python3 -m yt_dlp --rm-cache-dir || warn "Could not clear yt-dlp cache"

# 6) Sanity checks
info "Verifying imports and versions..."
python3 - <<'PY'
try:
    import yt_dlp
    print("yt-dlp OK")
except Exception as e:
    print("yt-dlp import failed:", e)
PY

ffmpeg -version | head -n 1 || warn "ffmpeg check failed"

# 7) Optional quick test (no download)
info "Self-repair completed. If issues persist, run:"
echo "  python3 maintenance.py"

echo "You can also test CLI:"
echo "  python3 ytdl_wav.py \"https://youtube.com/watch?v=VIDEO_ID\" --sr 48000 --bit 16 --ch 2"

echo "Done."