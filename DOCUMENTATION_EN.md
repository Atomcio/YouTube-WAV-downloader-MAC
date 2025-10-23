# YTWAV — Application Documentation (EN)

## Overview
YTWAV is a lightweight YouTube audio downloader that converts streams to lossless WAV/PCM. It offers both a simple GUI (Tkinter) and a robust CLI, with configurable audio parameters, resilient retries against transient errors (403/429), batch processing via URL lists, and safe filename handling.

- Platforms: Windows-first, cross-platform where `yt-dlp` and `ffmpeg` are available
- Core tools: `yt-dlp` for retrieval, `ffmpeg` for conversion
- Use responsibly: comply with YouTube Terms of Service and copyright law

## System Architecture
- Retrieval: `yt-dlp` fetches the best available audio stream and metadata
- Transcode: `ffmpeg` converts the source audio to WAV/PCM
- Orchestration: Python layers handle CLI/GUI, retries, sanitization, logging

## Project Structure
- `ytdl_wav.py` — core CLI and downloader utilities
- `ytwav_gui.py` — minimal Tkinter GUI
- `maintenance.py` — maintenance tasks: version checks and updates for `yt-dlp`
- `scripts/` — example runners and Windows FFmpeg installation guide
- `urls.txt` — example list of URLs for batch processing
- `wav_out/`, `wav_out_already/` — output directories (do not commit large `.wav`)
- `DOKUMENTACJA_APLIKACJI.md` — full documentation (PL)

## Core Components
- `YTWavDownloader` (in `ytdl_wav.py`):
  - `setup_logging`, `show_hints`, `check_ffmpeg`, `auto_update_ytdlp`
  - `is_valid_youtube_url`, `load_urls_from_file`, `load_all_urls`
  - `build_opts` (yt-dlp options), `sanitize_filename`
  - `download_audio` with resilient retry (rotating User-Agent, backoff, 403 handling, optional yt-dlp update)
  - `get_video_info` for metadata-only inspection
  - `download_wav` convenience wrapper (used by GUI and CLI)
- `YTWavGUI` (in `ytwav_gui.py`):
  - Fixed-size window, URL input, download button
  - FFmpeg availability check on startup
  - Calls `download_wav`, shows success/error messages
- `YTDownloaderMaintenance` (in `maintenance.py`):
  - Compares local `yt-dlp` version with PyPI
  - Auto-update via pip
  - Safe title formatting, test info extraction

## Key Features
- Lossless WAV/PCM conversion via `ffmpeg`
- Audio controls: `sample_rate`, `channels`, `bit_depth`
- Batch downloads via `--list` file
- Safe Windows-compatible filenames
- Retry strategy for network/HTTP issues
- Metadata-only mode for inspection

## CLI Usage
Examples:
- Single URL:
  ```powershell
  python ytdl_wav.py --url "https://youtu.be/…" --sr 48000 --bit_depth 16 --channels 2
  ```
- Batch list:
  ```powershell
  python ytdl_wav.py --list urls.txt --out wav_out
  ```
- Common options:
  - `--url` YouTube URL
  - `--list` Path to text file with URLs (one per line, `#` as comment)
  - `--out` Output directory (default: `wav_out`)
  - `--sr` Sample rate (e.g., 48000)
  - `--channels` 1=mono, 2=stereo (default: 2)
  - `--bit_depth` 16 or 24 (default: 16)
  - `--keep_src` Keep original downloaded source file
  - `--retries` Retry attempts on failure

## GUI Usage (Windows)
- Run `YT_downloader_wav.bat` or `python ytwav_gui.py`
- Paste a valid YouTube URL and click Download
- The app validates FFmpeg and shows clear error/success messages

## Configuration & Requirements
- Python: 3.11+
- Dependencies: install `yt-dlp` via `requirements.txt`
- FFmpeg: install system-wide; see `scripts/win_install_ffmpeg.md`

## Maintenance
- `maintenance.py` checks current `yt-dlp` version against PyPI
- Updates `yt-dlp` via pip when needed
- `auto_maintenance.bat` automates running maintenance and handling the exit code

## Error Handling & Logging
- Structured logging with timestamps and clear messages
- User hints for common scenarios (e.g., 24-bit size implications, mono forcing)
- Robust handling of 403/429 via retry and User-Agent rotation
- Graceful handling of invalid URLs and download failures

## Security & Compliance
- No telemetry; minimal permissions
- Input validation and safe filename generation
- Respect YouTube Terms of Service and copyright

## Performance Notes
- Minimal dependencies: `yt-dlp` + system `ffmpeg`
- Retry/backoff prevents unnecessary failures
- Batch mode reduces manual steps for large lists

## Licensing & Commercialization (Optional)
- Sales platforms: Gumroad/Payhip (MVP), Paddle/FastSpring (SaaS), Stripe Checkout + own backend (full control)
- Pricing model: Free (basic), Pro (advanced features), Business (commercial use)
- Licensing:
  - Offline: local license file + digital signature (RSA)
  - Online: server-side verification via API, machine binding
  - Hybrid: local verification with periodic online checks

## Future Work
- Playlist support and richer progress indicators
- Metadata editing and additional output formats (FLAC/MP3)
- Cloud sync and advanced batch GUI

## Installation (Quick)
```powershell
# Install dependencies
pip install -r requirements.txt

# Windows FFmpeg guidance
# See: scripts/win_install_ffmpeg.md

# Run GUI
python ytwav_gui.py

# Run CLI (single URL)
python ytdl_wav.py --url "https://youtu.be/…"
```