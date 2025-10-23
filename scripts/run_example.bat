@echo off
REM Przykładowe wywołanie ytdl_wav.py
REM Pobiera audio z YouTube i konwertuje do WAV

echo Uruchamianie ytdl_wav.py...
echo.

REM Przejdź do katalogu głównego projektu
cd /d "%~dp0.."

REM Utwórz folder docelowy jeśli nie istnieje
if not exist "wav_out" mkdir wav_out

REM Przykładowe wywołanie z URL YouTube
REM Zmień URL na własny
python ytdl_wav.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o wav_out --sr 44100 --ch 2 --bit 16

echo.
echo Pobieranie zakończone! Sprawdź folder wav_out
pause