#!/bin/bash
# YTWAV macOS launcher (GUI)
# Double-clickable from Finder

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 not found. Install via Homebrew or python.org." >&2
  exit 1
fi

# Check FFmpeg
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "FFmpeg not found. Install via: brew install ffmpeg" >&2
  exit 1
fi

# Check yt-dlp
python3 - <<'PY'
try:
    import yt_dlp  # noqa
    print("yt-dlp OK")
except Exception as e:
    print("yt-dlp not installed. Run: pip3 install -r requirements.txt")
    raise
PY

# Run GUI
exec python3 ytwav_gui.py