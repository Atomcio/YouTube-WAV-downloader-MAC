# YTWAV - Smoke Tests

🧪 **Podstawowe testy funkcjonalności YTWAV**

Te testy sprawdzają czy wszystkie komponenty działają poprawnie. Uruchom je po instalacji lub po zmianach w kodzie.

## 📋 Lista kontrolna przed testami

- [ ] Python 3.7+ zainstalowany
- [ ] yt-dlp zainstalowany (`pip install yt-dlp`)
- [ ] FFmpeg zainstalowany i dostępny w PATH
- [ ] Połączenie internetowe aktywne
- [ ] Katalog projektu YTWAV dostępny

## 🔧 Test 1: Sprawdzenie środowiska

### Cel
Sprawdzenie czy wszystkie wymagane komponenty są zainstalowane.

### Kroki

#### macOS (Terminal)
```bash
# Test Python
python3 --version
# Oczekiwany wynik: Python 3.x.x

# Test yt-dlp
python3 -c "import yt_dlp; print('yt-dlp OK')"
# Oczekiwany wynik: yt-dlp OK
```

# Test FFmpeg
ffmpeg -version
# Oczekiwany wynik: ffmpeg version N-xxxxx...
```

#### macOS/Linux (Terminal)
```bash
# Test Python
python3 --version
# Oczekiwany wynik: Python 3.x.x

# Test yt-dlp
python3 -c "import yt_dlp; print('yt-dlp OK')"
# Oczekiwany wynik: yt-dlp OK

# Test FFmpeg
ffmpeg -version
# Oczekiwany wynik: ffmpeg version N-xxxxx...
```

### Kryteria sukcesu
- [ ] Python wyświetla wersję 3.7+
- [ ] yt-dlp importuje się bez błędów
- [ ] FFmpeg wyświetla informacje o wersji

---

## 🔧 Test 2: Podstawowa funkcjonalność

### Cel
Sprawdzenie czy YTWAV uruchamia się i wyświetla pomoc.

### Kroki

```bash
# Przejdź do katalogu projektu
cd /path/to/ytwav

# Test pomocy
python ytdl_wav.py --help

# Test wersji
python ytdl_wav.py --version
```

### Oczekiwane wyniki
- Pomoc wyświetla się bez błędów
- Wersja pokazuje "YTWAV 1.0.0"
- Brak komunikatów o błędach importu

### Kryteria sukcesu
- [ ] Pomoc wyświetla się poprawnie
- [ ] Wersja jest wyświetlana
- [ ] Brak błędów Python

---

## 🔧 Test 3: Pobieranie informacji o filmie

### Cel
Sprawdzenie czy YTWAV może pobrać metadane filmu bez pobierania audio.

### Kroki

```bash
# Test z popularnym filmem (Rick Roll - zawsze dostępny)
python ytdl_wav.py --info "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Oczekiwane wyniki
```
Pobieranie informacji o filmie...

Tytuł: Rick Astley - Never Gonna Give You Up (Official Video)
Autor: Rick Astley
Czas trwania: 03:32
Wyświetlenia: xxx,xxx,xxx
```

### Kryteria sukcesu
- [ ] Informacje o filmie są wyświetlane
- [ ] Tytuł, autor, czas trwania są poprawne
- [ ] Brak błędów pobierania
- [ ] Proces kończy się bez błędów

---

## 🔧 Test 4: Pobieranie audio (krótki film)

### Cel
Sprawdzenie pełnej funkcjonalności pobierania i konwersji do WAV.

### Przygotowanie
```bash
# Utwórz katalog testowy
mkdir test_output
cd test_output
```

### Kroki

```bash
# Pobierz krótki film testowy (10 sekund)
python ../ytdl_wav.py -f "test_audio" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Oczekiwane wyniki
- Proces pobierania rozpoczyna się
- FFmpeg konwertuje audio do WAV
- Plik `test_audio.wav` jest utworzony
- Komunikat sukcesu: "✅ Audio zostało pobrane i skonwertowane do WAV PCM!"

### Weryfikacja pliku

#### macOS
```bash
# Sprawdź czy plik istnieje
ls -la test_audio.wav

# Sprawdź właściwości audio (opcjonalnie)
ffprobe test_audio.wav
```

#### macOS/Linux
```bash
# Sprawdź czy plik istnieje
ls -la test_audio.wav

# Sprawdź właściwości audio
ffprobe test_audio.wav
```

### Oczekiwane właściwości audio
- Format: WAV (PCM)
- Kodek: pcm_s16le
- Częstotliwość: 44100 Hz
- Kanały: 2 (stereo)
- Rozmiar pliku: > 0 bajtów

### Kryteria sukcesu
- [ ] Plik WAV został utworzony
- [ ] Plik ma poprawne właściwości audio
- [ ] Rozmiar pliku jest sensowny (> 100KB dla 10s)
- [ ] Brak błędów podczas procesu

---

## 🔧 Test 5: Obsługa błędów

### Cel
Sprawdzenie czy YTWAV poprawnie obsługuje błędne dane wejściowe.

### Test 5.1: Nieprawidłowy URL
```bash
python ytdl_wav.py "https://example.com/fake-video"
```

**Oczekiwany wynik**: Komunikat błędu o nieprawidłowym URL YouTube

### Test 5.2: Nieistniejący film
```bash
python ytdl_wav.py "https://www.youtube.com/watch?v=nieistniejacy123"
```

**Oczekiwany wynik**: Komunikat błędu pobierania

### Test 5.3: Brak argumentów
```bash
python ytdl_wav.py
```

**Oczekiwany wynik**: Komunikat błędu o wymaganym argumencie URL

### Kryteria sukcesu
- [ ] Błędy są obsługiwane gracefully
- [ ] Komunikaty błędów są czytelne
- [ ] Program nie crashuje
- [ ] Kody wyjścia są odpowiednie (≠ 0)

---

## 🔧 Test 6: Różne opcje CLI

### Test 6.1: Niestandardowy katalog wyjściowy
```bash
mkdir custom_output
python ytdl_wav.py -o "custom_output" --info "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Test 6.2: Kombinacja opcji
```bash
python ytdl_wav.py -o "test_dir" -f "custom_name" --info "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Kryteria sukcesu
- [ ] Opcje są poprawnie parsowane
- [ ] Katalogi są tworzone automatycznie
- [ ] Kombinacje opcji działają

---

## 🔧 Test 7: Performance i stabilność

### Cel
Sprawdzenie wydajności i stabilności przy różnych scenariuszach.

### Test 7.1: Długi film (opcjonalny)
```bash
# UWAGA: Ten test pobiera duży plik - uruchom tylko jeśli masz czas i miejsce
python ytdl_wav.py --info "https://www.youtube.com/watch?v=[długi-film]"
```

### Test 7.2: Specjalne znaki w tytule
```bash
# Film z nietypowymi znakami w tytule
python ytdl_wav.py --info "https://www.youtube.com/watch?v=[film-ze-specjalnymi-znakami]"
```

### Kryteria sukcesu
- [ ] Długie filmy są obsługiwane
- [ ] Specjalne znaki w nazwach plików są sanityzowane
- [ ] Brak wycieków pamięci

---

## 📊 Podsumowanie testów

### Checklist końcowy

#### Testy podstawowe (wymagane)
- [ ] Test 1: Środowisko ✓
- [ ] Test 2: Podstawowa funkcjonalność ✓
- [ ] Test 3: Pobieranie informacji ✓
- [ ] Test 4: Pobieranie audio ✓
- [ ] Test 5: Obsługa błędów ✓

#### Testy zaawansowane (opcjonalne)
- [ ] Test 6: Opcje CLI ✓
- [ ] Test 7: Performance ✓

### Kryteria akceptacji

**Minimum do przejścia**: Testy 1-5 muszą przejść bez błędów

**Pełna funkcjonalność**: Wszystkie testy przechodzą

---

## 🐛 Rozwiązywanie problemów testowych

### Problem: "ModuleNotFoundError: No module named 'yt_dlp'"
**Rozwiązanie**:
```bash
pip install yt-dlp
# lub
pip3 install yt-dlp
```

### Problem: "ffmpeg: command not found"
**Rozwiązanie**:
- macOS: `brew install ffmpeg`

### Problem: "HTTP Error 403: Forbidden"
**Rozwiązanie**:
```bash
# Aktualizuj yt-dlp
pip install --upgrade yt-dlp
```

### Problem: Powolne pobieranie
**Przyczyny**:
- Wolne połączenie internetowe
- Ograniczenia YouTube
- Duży rozmiar pliku audio

**Rozwiązanie**: To normalne, poczekaj na zakończenie

---

## 📝 Raportowanie błędów

Jeśli któryś test nie przechodzi:

1. **Zapisz pełny output błędu**
2. **Sprawdź wersje**:
   ```bash
   python --version
   pip show yt-dlp
   ffmpeg -version
   ```
3. **Sprawdź połączenie internetowe**
4. **Spróbuj z innym filmem YouTube**
5. **Zgłoś issue z pełnymi informacjami**

---

**Ostatnia aktualizacja**: 2024-01-XX  
**Wersja testów**: 1.0.0  
**Kompatybilność**: YTWAV 1.0.0