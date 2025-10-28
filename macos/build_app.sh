#!/usr/bin/env bash
# Build macOS .app via py2app
set -euo pipefail

# Upgrade build tooling
python3 -m pip install --upgrade pip wheel setuptools

# Install py2app and app deps
python3 -m pip install py2app yt-dlp

# Build .app
python3 macos/setup.py py2app

echo "\nBuilt app at: dist/YTWAV.app"