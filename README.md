# YTWAV — YouTube WAV Downloader

Lekki downloader audio z YouTube do bezstratnego WAV/PCM z GUI i CLI. Wspiera konwersję przez FFmpeg, retry na błędy (403/429), batch przez plik URL-i i szczegółową konfigurację jakości.

English summary: Lightweight YouTube audio downloader to lossless WAV/PCM with GUI and CLI, FFmpeg-based conversion, resilient retries, batch via URL list, and detailed audio settings.

## Funkcje
- Pobieranie audio i konwersja do WAV/PCM (FFmpeg)
- Retry z różnymi User-Agent (radzi sobie z 403/429)
- GUI w Tkinter + pełny CLI
- Lista URL-i (batch) i metadane bez pobierania
- Konfigurowalne: `sample_rate`, `channels`, `bit_depth`

## Wymagania
- Python 3.11+
- `yt-dlp` (z `requirements.txt`)
- FFmpeg (zainstaluj przez Homebrew: `brew install ffmpeg`)

## Szybki start
- GUI (macOS): uruchom `./macos/run_gui.command` lub `python3 ytwav_gui.py`
- CLI (pojedynczy URL):
  ```bash
  python3 ytdl_wav.py --url "https://youtu.be/…" --sr 48000 --bit_depth 16 --channels 2
  ```
- CLI (lista):
  ```bash
  python3 ytdl_wav.py --list urls.txt --out wav_out
  ```

## Struktura
- Główne skrypty: `ytdl_wav.py`, `ytwav_gui.py`
- Utrzymanie: `maintenance.py`
- macOS: `macos/run_gui.command`, `macos/run_cli.sh`
- Przykłady: `urls.txt`
- Wyjścia audio: `wav_out/`, `wav_out_already/`

## Dokumentacja
Pełny opis architektury, funkcji i decyzji: `DOKUMENTACJA_APLIKACJI.md`.

## Uwaga dot. repozytorium
Nie commituj ciężkich plików `.wav`. Dodaj do `.gitignore`:
```
wav_out/
wav_out_already/
interkontinentalbajern/
test_cli/*.wav
test_fix/*.wav
```
Alternatywnie użyj Git LFS dla dużych plików.

## Licencja
Sugerowana licencja: MIT (dodaj plik `LICENSE`).

## Zastrzeżenia
Korzystaj zgodnie z regulaminem YouTube i prawem autorskim. Narzędzie przeznaczone do użytku zgodnego z licencjami treści.