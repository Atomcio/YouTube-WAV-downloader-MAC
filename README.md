# YTWAV — YouTube WAV Downloader (macOS)

YTWAV is a lightweight macOS-only tool for downloading YouTube audio and converting it to lossless WAV/PCM. It offers a simple GUI (Tkinter) and a flexible CLI, uses `yt-dlp` for retrieval, and `ffmpeg` for audio conversion.

- macOS-only
- GUI (Tkinter) + CLI
- Minimal dependencies: `yt-dlp` and system `ffmpeg`

## Features
- Download audio and convert to WAV/PCM (via FFmpeg)
- Resilient retries to handle errors (e.g., 403/429)
- Batch mode via URL list file
- Configurable audio settings: sample rate, channels, bit depth
- Safe filename handling
- Optional maintenance/diagnostics script

## Requirements
- `python3` (3.11+ recommended)
- Homebrew
- `ffmpeg` installed via Homebrew

## Preinstallation (macOS)
If your system is fresh and Homebrew is not installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then verify `python3` and `pip3`. If they are missing or not working, install Python:
```bash
brew install python
```

## Installation
- Clone the repository:
  ```bash
  git clone https://github.com/Atomcio/YouTube-WAV-downloader-MAC.git
  cd YouTube-WAV-downloader-MAC
  ```
- Install Python dependencies:
  ```bash
  pip3 install -r requirements.txt
  ```
- Install FFmpeg:
  ```bash
  brew install ffmpeg
  ```
- Make macOS launch scripts executable (optional but convenient):
  ```bash
  chmod +x macos/run_gui.command macos/run_cli.sh
  ```

## Quick Start (GUI)
- Launch the GUI:
  ```bash
  ./macos/run_gui.command
  ```
- Alternatively:
  ```bash
  python3 ytwav_gui.py
  ```

## Quick Start (CLI)
- Single URL:
  ```bash
  ./macos/run_cli.sh "https://youtube.com/watch?v=VIDEO_ID"
  ```
- Using Python directly:
  ```bash
  python3 ytdl_wav.py "https://youtube.com/watch?v=VIDEO_ID"
  ```

## CLI Options
The CLI exposes fine-grained control over output quality and behavior:
- `--list <file>`: Path to a text file with one URL per line (lines starting with `#` are treated as comments)
- `-o, --out <dir>`: Output directory (default: `wav_out`)
- `--sr <int>`: Sample rate (default: `48000`)
- `--ch <1|2>`: Channels: `1` mono or `2` stereo (default: `2`)
- `--bit <16|24>`: WAV bit depth (default: `16`)
- `--keep-src`: Keep the original downloaded audio file (e.g., `.m4a`)
- `--retries <int>`: Retry count for errors (default: `5`)

### Examples
- Single video to a custom directory, 44.1 kHz mono, 24-bit:
  ```bash
  python3 ytdl_wav.py "https://youtube.com/watch?v=VIDEO_ID" -o my_wavs --sr 44100 --ch 1 --bit 24
  ```
- Batch from file:
  ```bash
  python3 ytdl_wav.py --list urls.txt --out batch_wavs
  ```
- Keep source file:
  ```bash
  python3 ytdl_wav.py "https://youtube.com/watch?v=VIDEO_ID" --keep-src
  ```

## Project Structure
- Main scripts: `ytdl_wav.py`, `ytwav_gui.py`
- Maintenance: `maintenance.py`
- macOS helpers: `macos/run_gui.command`, `macos/run_cli.sh`, `macos/build_app.sh`, `macos/setup.py`, `macos/README_macOS.md`
- Examples: `urls.txt`
- Outputs: `wav_out/`, `wav_out_already/`

## Maintenance & Diagnostics
- Run maintenance checks and logging:
  ```bash
  python3 maintenance.py
  ```
- This verifies `yt-dlp` and `ffmpeg`, can run a test download, and logs into `maintenance.log`.

## Troubleshooting
- `ffmpeg: command not found`
  - Install FFmpeg: `brew install ffmpeg`
  - Verify PATH: `which ffmpeg`
- Permission denied when running scripts
  - Grant execute permission: `chmod +x macos/run_gui.command macos/run_cli.sh`
- Update `yt-dlp` if you see HTTP or extraction issues:
  ```bash
  pip3 install --upgrade yt-dlp
  ```

## Self-Repair (macOS)
- Run automated fix script:
  ```bash
  chmod +x macos/self_repair.sh
  ./macos/self_repair.sh
  ```
- What it does:
  - Upgrades `pip` and `yt-dlp`
  - Installs/upgrades `ffmpeg` via Homebrew
  - Clears `yt-dlp` cache
  - Suggests PATH fixes for Apple Silicon
  - Verifies environment and prints guidance
- If issues persist, run diagnostics:
  ```bash
  python3 maintenance.py
  ```

## License
Recommended license: MIT (add a `LICENSE` file if desired).

## Disclaimer
Use in accordance with YouTube’s Terms of Service and applicable copyright laws. This tool is intended for lawful, licensed content usage.