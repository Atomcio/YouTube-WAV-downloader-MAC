#!/usr/bin/env bash
# Przykładowe wywołanie ytdl_wav.py
# Pobiera audio z YouTube i konwertuje do WAV

echo "Uruchamianie ytdl_wav.py..."
echo

# Przejdź do katalogu głównego projektu
cd "$(dirname "$0")/.."

# Utwórz folder docelowy jeśli nie istnieje
mkdir -p wav_out

# Przykładowe wywołanie z URL YouTube
# Zmień URL na własny
python3 ytdl_wav.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o wav_out --sr 44100 --ch 2 --bit 16

echo
echo "Pobieranie zakończone! Sprawdź folder wav_out"
read -p "Naciśnij Enter aby kontynuować..."