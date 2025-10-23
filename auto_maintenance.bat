@echo off
REM Automatyczne utrzymanie systemu YT Downloader
REM Uruchom ten skrypt regularnie (np. raz w tygodniu)

echo ========================================
echo    YT Downloader - Auto Maintenance
echo ========================================
echo.

REM Przejdź do katalogu skryptu
cd /d "%~dp0"

REM Aktywuj środowisko wirtualne jeśli istnieje
if exist "venv\Scripts\activate.bat" (
    echo Aktywuję środowisko wirtualne...
    call venv\Scripts\activate.bat
)

REM Uruchom pełne utrzymanie
echo Uruchamiam pełne utrzymanie systemu...
python maintenance.py

REM Sprawdź kod wyjścia
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Utrzymanie zakończone pomyślnie!
    echo System jest gotowy do pracy.
) else (
    echo.
    echo [WARNING] Wykryto problemy podczas utrzymania.
    echo Sprawdź logi w pliku maintenance.log
    echo.
    echo Naciśnij dowolny klawisz aby kontynuować...
    pause >nul
)

echo.
echo Utrzymanie zakończone.
echo ========================================