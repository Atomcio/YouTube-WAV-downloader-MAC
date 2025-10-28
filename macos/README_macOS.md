# YTWAV — macOS Guide

## Overview
This folder provides macOS-specific usage notes, launch scripts, and optional packaging instructions for the YTWAV app.

- Runs with Python 3.11+ and system `ffmpeg`
- GUI via Tkinter, CLI via `ytdl_wav.py`
- Uses `yt-dlp` for retrieval and `ffmpeg` for conversion

## Requirements
- Install Python 3.11+ (via python.org or `brew install python@3.11`)
- Install FFmpeg:
  ```bash
  brew install ffmpeg
  ```
- Install Python dependencies (from project root):
  ```bash
  pip3 install -r requirements.txt
  ```

## Preinstallation (macOS)
If Homebrew is not installed yet:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then ensure `python3` and `pip3` are available. If not:
```bash
brew install python
```

## Run GUI
- Double-click or run:
  ```bash
  ./macos/run_gui.command
  ```
- Alternatively from the project root:
  ```bash
  python3 ytwav_gui.py
  ```

## Run CLI
Examples:
```bash
# Single URL
python3 ytdl_wav.py --url "https://youtu.be/..." --sr 48000 --bit_depth 16 --channels 2

# Batch from list
python3 ytdl_wav.py --list urls.txt --out wav_out
```

## Optional: Create a macOS .app (py2app)
1. Install build tools:
   ```bash
   pip3 install --upgrade pip wheel setuptools
   pip3 install py2app yt-dlp
   ```
2. Build the app:
   ```bash
   python3 macos/setup.py py2app
   ```
3. Output:
   - App bundle: `dist/YTWAV.app`
   - Requires `ffmpeg` to be available on PATH (via Homebrew)

### Gatekeeper note
If macOS blocks the app, right-click the app and choose "Open" the first time.

## Self-Repair
Run the automated fix script:
```bash
chmod +x macos/self_repair.sh
./macos/self_repair.sh
```
It will:
- Upgrade `pip` and `yt-dlp`
- Install/upgrade `ffmpeg` via Homebrew
- Clear `yt-dlp` cache
- Suggest PATH fixes for Apple Silicon
- Verify environment and print guidance

## Troubleshooting
- `ffmpeg: command not found` → `brew install ffmpeg`
- `ModuleNotFoundError: yt_dlp` → `pip3 install -r requirements.txt`
- Permission issues on `run_gui.command` → `chmod +x macos/run_gui.command`