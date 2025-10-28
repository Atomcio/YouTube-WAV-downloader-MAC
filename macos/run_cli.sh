#!/usr/bin/env bash
# YTWAV macOS CLI helper
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Ensure ffmpeg
command -v ffmpeg >/dev/null 2>&1 || { echo "Install FFmpeg: brew install ffmpeg"; exit 1; }

# Examples
cat <<'TXT'
Examples:

# Single URL (stereo, 48kHz, 16-bit)
python3 ytdl_wav.py --url "https://youtu.be/..." --sr 48000 --bit_depth 16 --channels 2

# Batch from urls.txt into wav_out/
python3 ytdl_wav.py --list urls.txt --out wav_out

# High-quality (96kHz, 24-bit)
python3 ytdl_wav.py --url "https://youtu.be/..." --sr 96000 --bit_depth 24 --channels 2

# Mono, keep source file, 10 retries
python3 ytdl_wav.py --url "https://youtu.be/..." --channels 1 --keep_src --retries 10
TXT