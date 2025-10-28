# 🎵 YTWAV - YouTube Audio Downloader
## Kompletna dokumentacja aplikacji

### 📋 SPIS TREŚCI
1. [Przegląd aplikacji](#przegląd-aplikacji)
2. [Architektura systemu](#architektura-systemu)
3. [Struktura plików](#struktura-plików)
4. [Główne komponenty](#główne-komponenty)
5. [Funkcjonalności](#funkcjonalności)
6. [Rozwiązania techniczne](#rozwiązania-techniczne)
7. [Konfiguracja i zależności](#konfiguracja-i-zależności)
8. [Interfejsy użytkownika](#interfejsy-użytkownika)
9. [System utrzymania](#system-utrzymania)
10. [Bezpieczeństwo i stabilność](#bezpieczeństwo-i-stabilność)

---

## 🎯 PRZEGLĄD APLIKACJI

**YTWAV** to zaawansowana aplikacja do pobierania audio z YouTube i konwersji do formatu WAV PCM w wysokiej jakości. Aplikacja oferuje zarówno interfejs graficzny (GUI) jak i interfejs wiersza poleceń (CLI).

### Główne cechy:
- **Wysokiej jakości audio**: WAV PCM 48kHz/16-bit domyślnie
- **Inteligentny system retry**: Automatyczne obchodzenie blokad YouTube
- **Dual interface**: GUI (Tkinter) + CLI (argparse)
- **Auto-maintenance**: Automatyczne aktualizacje i diagnostyka
- **macOS-only**: Dedykowane dla macOS
- **Minimalne zależności**: Tylko yt-dlp + systemowy FFmpeg

---

## 🏗️ ARCHITEKTURA SYSTEMU

```
┌─────────────────────────────────────────────────────────────┐
│                    YTWAV ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│  GUI Layer (ytwav_gui.py)     │  CLI Layer (ytdl_wav.py)   │
│  ┌─────────────────────────┐   │  ┌─────────────────────────┐ │
│  │ Tkinter Interface       │   │  │ Argparse CLI           │ │
│  │ - 400x120px window      │   │  │ - Batch processing     │ │
│  │ - URL input field       │   │  │ - File list support    │ │
│  │ - Download button       │   │  │ - Advanced options     │ │
│  └─────────────────────────┘   │  └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    CORE ENGINE                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ YTWavDownloader Class (ytdl_wav.py)                     │ │
│  │ - URL validation & processing                           │ │
│  │ - Multi-strategy retry system                           │ │
│  │ - Audio quality configuration                           │ │
│  │ - FFmpeg integration                                    │ │
│  │ - Intelligent error handling                            │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                 MAINTENANCE SYSTEM                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ YTDownloaderMaintenance Class (maintenance.py)          │ │
│  │ - Version checking & auto-updates                       │ │
│  │ - System diagnostics                                    │ │
│  │ - Success rate monitoring                               │ │
│  │ - FFmpeg validation                                     │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                 EXTERNAL DEPENDENCIES                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ yt-dlp (>=2023.12.30)  │  FFmpeg (system)              │ │
│  │ - YouTube extraction    │  - Audio conversion           │ │
│  │ - Format selection      │  - WAV PCM encoding           │ │
│  │ - Metadata handling     │  - Quality control            │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 STRUKTURA PLIKÓW

```
p_YT_downloader/
├── 🐍 GŁÓWNE PLIKI APLIKACJI
│   ├── ytdl_wav.py              # Główny moduł CLI + core engine
│   ├── ytwav_gui.py             # Interfejs graficzny (Tkinter)
│   └── maintenance.py           # System utrzymania i diagnostyki
│
├── ⚙️ KONFIGURACJA I SKRYPTY
│   ├── requirements.txt         # Zależności Python (yt-dlp)
│   ├── .gitignore               # Wzorce ignorowania Git
│   ├── urls.txt                 # Przykładowe URL-e do testów
│   └── macos/                   # Skrypty uruchomieniowe i pakowanie dla macOS
│
├── 📂 FOLDERY WYJŚCIOWE
│   ├── wav_out/                # Nowo pobrane pliki WAV
│   ├── wav_out_already/        # Archiwum pobranych plików
│   ├── interkontinentalbajern/ # Kolekcja muzyki elektronicznej
│   ├── test_cli/               # Testy interfejsu CLI
│   └── test_fix/               # Testy napraw i poprawek
│
├── 🛠️ NARZĘDZIA I SKRYPTY
│   └── macos/
│       ├── run_gui.command      # Launcher GUI dla macOS
│       ├── run_cli.sh           # Przykłady CLI dla macOS
│       ├── setup.py             # Konfiguracja py2app
│       └── build_app.sh         # Budowanie .app
│
├── 🧪 TESTY I DIAGNOSTYKA
│   ├── tests/
│   │   └── smoke_test.md       # Testy podstawowej funkcjonalności
│   ├── test_optimized_system.py # Testy wydajności systemu
│   └── maintenance.log         # Logi systemu utrzymania
│
└── 📚 DOKUMENTACJA
    ├── README.md               # Podstawowa dokumentacja
    ├── ZABEZPIECZENIA_YOUTUBE.md # Informacje o obchodzeniu blokad
    └── DOKUMENTACJA_APLIKACJI.md # Ten plik - pełna dokumentacja
```

---

## 🔧 GŁÓWNE KOMPONENTY

### 1. **YTWavDownloader Class** (ytdl_wav.py)
**Główny silnik aplikacji** - odpowiada za pobieranie i konwersję audio.

#### Kluczowe metody:
- `__init__()` - Konfiguracja parametrów audio (sample rate, kanały, bit depth)
- `download_audio()` - Główna metoda pobierania z inteligentnym retry
- `build_opts()` - Budowanie opcji yt-dlp z konfiguracją FFmpeg
- `auto_update_ytdlp()` - Automatyczne aktualizacje yt-dlp
- `check_ffmpeg()` - Walidacja dostępności FFmpeg
- `load_urls_from_file()` - Ładowanie URL-ów z pliku tekstowego

#### Parametry konfiguracyjne:
```python
sample_rate: int = 48000    # Częstotliwość próbkowania
channels: int = 2           # Liczba kanałów (1=mono, 2=stereo)
bit_depth: int = 16         # Głębia bitowa (16 lub 24)
keep_source: bool = False   # Zachowanie pliku źródłowego
retries: int = 5            # Liczba ponowień przy błędach
```

### 2. **YTWavGUI Class** (ytwav_gui.py)
**Minimalistyczny interfejs graficzny** - 400x120px, nierozszerzalne okno.

#### Komponenty UI:
- **Label**: "Wklej link YouTube:"
- **Entry**: Pole tekstowe na URL (width=50)
- **Button**: Przycisk "Pobierz" (15x1)
- **Bindings**: Enter key → download_audio()

#### Funkcjonalności:
- Walidacja URL YouTube przy starcie
- Sprawdzenie FFmpeg przy inicjalizacji
- Blokowanie przycisku podczas pobierania
- Automatyczne czyszczenie pola po sukcesie

### 3. **YTDownloaderMaintenance Class** (maintenance.py)
**System utrzymania i monitorowania** - automatyczna diagnostyka i aktualizacje.

#### Główne funkcje:
- `check_ytdlp_version()` - Porównanie z najnowszą wersją PyPI
- `update_ytdlp()` - Automatyczna aktualizacja yt-dlp
- `test_download_capability()` - Test pobierania z URL-ów testowych
- `check_ffmpeg()` - Walidacja FFmpeg i kodekow
- `show_success_statistics()` - Statystyki sukcesu/porażek

---

## ⚡ FUNKCJONALNOŚCI

### 🎵 **Pobieranie Audio**
- **Formaty wejściowe**: Wszystkie obsługiwane przez yt-dlp
- **Format wyjściowy**: WAV PCM (nieskompresowany)
- **Jakość**: Konfigurowana (domyślnie 48kHz/16-bit/stereo)
- **Źródła**: YouTube, YouTube Music, inne platformy obsługiwane przez yt-dlp

### 🔄 **Inteligentny System Retry**
Aplikacja implementuje zaawansowany system ponowień z różnymi strategiami:

```python
retry_strategies = [
    {'sleep_interval': 2, 'user_agent_suffix': ''},
    {'sleep_interval': 5, 'user_agent_suffix': ' Edg/120.0.0.0'},
    {'sleep_interval': 8, 'user_agent_suffix': ' Firefox/120.0'},
    {'sleep_interval': 12, 'user_agent_suffix': ' Safari/537.36'},
    {'sleep_interval': 15, 'user_agent_suffix': ' Chrome/120.0.0.0'},
]
```

**Mechanizmy obchodzenia blokad:**
1. **Rotacja User-Agent**: Symulacja różnych przeglądarek
2. **Progresywne opóźnienia**: Zwiększanie czasu oczekiwania
3. **Auto-update yt-dlp**: Aktualizacja przy niepowodzeniu
4. **Dodatkowa próba**: Po aktualizacji jedna dodatkowa próba

### 📁 **Przetwarzanie Wsadowe**
- **Pojedynczy URL**: Bezpośrednie podanie w CLI lub GUI
- **Lista URL-ów**: Plik tekstowy z URL-ami (jeden na linię)
- **Komentarze**: Linie zaczynające się od `#` są ignorowane
- **Walidacja**: Automatyczne sprawdzanie poprawności URL-ów YouTube

### 🎛️ **Konfiguracja Audio**
```bash
# Przykłady konfiguracji
python ytdl_wav.py URL --sr 44100 --ch 1 --bit 24    # 44.1kHz mono 24-bit
python ytdl_wav.py URL --sr 48000 --ch 2 --bit 16    # 48kHz stereo 16-bit (domyślne)
python ytdl_wav.py URL --keep-src                     # Zachowanie pliku źródłowego
```

---

## 🔬 ROZWIĄZANIA TECHNICZNE

### **1. Obchodzenie Blokad YouTube**
YouTube regularnie blokuje automatyczne pobieranie. Aplikacja implementuje:

- **Multi-strategy retry**: 5 różnych strategii z różnymi User-Agent
- **Progresywne opóźnienia**: Od 2 do 15 sekund między próbami
- **Auto-update mechanizm**: Automatyczna aktualizacja yt-dlp przy błędach
- **Intelligent error detection**: Rozpoznawanie błędów 403/Forbidden

### **2. Optymalizacja Jakości Audio**
```python
# Konfiguracja yt-dlp dla najwyższej jakości
'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'wav',
    'preferredquality': None,  # Bez kompresji
}]
```

### **3. Bezpieczne Nazwy Plików**
```python
def sanitize_filename(self, filename: str) -> str:
    # Usunięcie niebezpiecznych znaków
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    return filename[:200]  # Ograniczenie długości
```

### **4. Inteligentne Logowanie**
```python
# Konfiguracja z timestampem i wieloma handlerami
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('maintenance.log'),
        logging.StreamHandler()
    ]
)
```

### **5. macOS Compatibility**
- **macOS**: Shell scripts (.sh), Homebrew package manager
- **Python**: Pathlib dla ścieżek, shutil.which() dla sprawdzania programów

---

## 📦 KONFIGURACJA I ZALEŻNOŚCI

### **requirements.txt**
```
# Minimalne zależności
yt-dlp>=2023.12.30
```

### **Zależności systemowe**
- **FFmpeg**: Wymagany do konwersji audio
  - macOS: `brew install ffmpeg`

### **Struktura konfiguracji yt-dlp**
```python
ydl_opts = {
    'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
    'outtmpl': str(out_dir / '%(title)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': None,
    }, {
        'key': 'FFmpegMetadata',
        'add_metadata': True,
    }],
    'postprocessor_args': {
        'ffmpeg_i': ['-hide_banner', '-loglevel', 'error'],
        'ffmpeg_o': [
            '-ar', str(sr),           # Sample rate
            '-ac', str(ch),           # Channels
            '-sample_fmt', f's{bit}', # Bit depth
            '-f', 'wav'               # Format
        ]
    }
}
```

---

## 🖥️ INTERFEJSY UŻYTKOWNIKA

### **1. GUI (ytwav_gui.py)**
**Minimalistyczny interfejs Tkinter**

```
┌─────────────────────────────────────────┐
│           YT → WAV Downloader           │
├─────────────────────────────────────────┤
│                                         │
│        Wklej link YouTube:              │
│  ┌───────────────────────────────────┐   │
│  │ https://youtube.com/watch?v=...  │   │
│  └───────────────────────────────────┘   │
│                                         │
│            ┌─────────┐                  │
│            │ Pobierz │                  │
│            └─────────┘                  │
└─────────────────────────────────────────┘
```

**Cechy GUI:**
- Rozmiar: 400x120px (nierozszerzalne)
- Centrowanie na ekranie
- Walidacja URL w czasie rzeczywistym
- Blokowanie przycisku podczas pobierania
- Automatyczne czyszczenie po sukcesie

### **2. CLI (ytdl_wav.py)**
**Zaawansowany interfejs wiersza poleceń**

```bash
# Podstawowe użycie
python ytdl_wav.py "https://youtube.com/watch?v=VIDEO_ID"

# Zaawansowane opcje
python ytdl_wav.py URL --sr 44100 --ch 1 --bit 24 -o custom_dir

# Przetwarzanie wsadowe
python ytdl_wav.py --list urls.txt -o batch_output

# Pomoc
python ytdl_wav.py --help
```

**Dostępne parametry:**
- `url`: URL YouTube (opcjonalny z --list)
- `--list`: Plik z listą URL-ów
- `-o, --out`: Katalog wyjściowy
- `--sr`: Sample rate (domyślnie 48000)
- `--ch`: Kanały 1=mono, 2=stereo (domyślnie 2)
- `--bit`: Głębia bitowa 16/24 (domyślnie 16)
- `--keep-src`: Zachowanie pliku źródłowego
- `--retries`: Liczba ponowień (domyślnie 5)

---

## 🛠️ SYSTEM UTRZYMANIA

### **Automatyczne Utrzymanie (maintenance.py)**
System monitoruje i utrzymuje aplikację w optymalnym stanie.

#### **Funkcje diagnostyczne:**
1. **Sprawdzanie wersji yt-dlp**
   - Porównanie z najnowszą wersją PyPI
   - Automatyczne aktualizacje
   - Logowanie zmian wersji

2. **Test możliwości pobierania**
   - URL-e testowe (Rick Roll, Gangnam Style)
   - Walidacja bez pobierania (extract_info)
   - Monitoring sukcesu/porażek

3. **Walidacja FFmpeg**
   - Sprawdzenie dostępności w PATH
   - Test kodekow audio
   - Walidacja parametrów konwersji

4. **Statystyki wydajności**
   - Tracking success rate
   - Analiza typów błędów
   - Metryki czasowe

#### **Auto-maintenance (macOS)**
```bash
# Automatyczny skrypt utrzymania (macOS)
# Uruchom z katalogu projektu
python3 maintenance.py
```

**Zalecane uruchamianie**: Raz w tygodniu lub przed ważnymi sesjami pobierania.

---

## 🔒 BEZPIECZEŃSTWO I STABILNOŚĆ

### **1. Obsługa Błędów**
```python
# Wielopoziomowa obsługa błędów
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
except yt_dlp.DownloadError as e:
    # Specyficzne błędy yt-dlp
    if 'http error 403' in str(e).lower():
        # Retry z inną strategią
except Exception as e:
    # Ogólne błędy
    self.logger.error(f"Nieoczekiwany błąd: {e}")
```

### **2. Walidacja Danych**
- **URL validation**: Sprawdzanie domen YouTube
- **File path sanitization**: Bezpieczne nazwy plików
- **Input validation**: Walidacja parametrów CLI
- **FFmpeg validation**: Sprawdzenie dostępności przed użyciem

### **3. Resource Management**
- **Context managers**: Automatyczne zamykanie zasobów yt-dlp
- **Timeout handling**: Limity czasowe dla operacji sieciowych
- **Memory management**: Streaming processing dla dużych plików
- **Disk space**: Sprawdzanie dostępnego miejsca

### **4. Logging i Monitoring**
```python
# Strukturalne logowanie z timestampami
self.logger.info(f"[{i}/{total_count}] Przetwarzanie: {url}")
self.logger.warning(f"Próba {attempt} zablokowana (403)")
self.logger.error(f"Błąd pobierania {url}: {e}")
```

### **5. Graceful Degradation**
- **Fallback strategies**: Alternatywne metody przy błędach
- **Partial success handling**: Kontynuacja przy częściowych błędach
- **User feedback**: Informowanie o problemach i rozwiązaniach
- **Recovery mechanisms**: Automatyczne naprawy i aktualizacje

---

## 📊 METRYKI I WYDAJNOŚĆ

### **Obsługiwane formaty wejściowe:**
- YouTube (wszystkie jakości)
- YouTube Music
- YouTube Shorts
- Inne platformy obsługiwane przez yt-dlp

### **Parametry wyjściowe:**
- **Format**: WAV PCM (nieskompresowany)
- **Sample rates**: 8kHz - 192kHz (domyślnie 48kHz)
- **Bit depth**: 16-bit lub 24-bit
- **Kanały**: Mono lub Stereo
- **Rozmiar pliku**: ~10MB/minutę (48kHz/16-bit/stereo)

### **Wydajność:**
- **Pobieranie**: Zależne od prędkości internetu
- **Konwersja**: ~2-5x szybciej niż czas trwania (FFmpeg)
- **Retry system**: Maksymalnie 5 prób z progresywnymi opóźnieniami
- **Memory usage**: Minimalne dzięki streaming processing

---

## 🚀 ROZSZERZENIA I ROZWÓJ

### **Potencjalne ulepszenia:**
1. **Playlist support**: Pobieranie całych playlist YouTube
2. **Quality presets**: Predefiniowane ustawienia jakości
3. **Batch GUI**: Interfejs graficzny dla wielu URL-ów
4. **Progress bars**: Wizualne wskaźniki postępu
5. **Metadata editing**: Edycja tagów audio
6. **Format options**: Dodatkowe formaty wyjściowe (FLAC, MP3)
7. **Cloud integration**: Synchronizacja z chmurą
8. **Mobile app**: Aplikacja mobilna

### **Architektura modularna:**
Aplikacja jest zaprojektowana modularnie, co ułatwia:
- Dodawanie nowych formatów
- Integrację z innymi platformami
- Rozszerzanie interfejsów użytkownika
- Implementację nowych strategii retry

---

## 💰 MODEL SPRZEDAŻY I LICENCJONOWANIA

### **🛒 Platformy Sprzedaży (Minimalny Start)**

#### **1. Rozwiązania Proste (MVP)**
- **Gumroad / Payhip**
  - ✅ Szybkie, bezproblemowe wdrożenie
  - ✅ Obsługa jednorazowych sprzedaży
  - ✅ Licencje prostego typu (pliki do pobrania)
  - ✅ Idealne dla MVP i testowania rynku
  - 💰 Prowizja: 3.5-5% + opłaty płatności

#### **2. Rozwiązania Zaawansowane (SaaS)**
- **Paddle / FastSpring**
  - ✅ Pełne rozwiązanie SaaS
  - ✅ Automatyczna obsługa VAT
  - ✅ Generowanie faktur
  - ✅ Obsługa subskrypcji
  - ✅ Wsparcie międzynarodowe
  - 💰 Prowizja: 5-8% + opłaty płatności

#### **3. Rozwiązanie Własne (Pełna Kontrola)**
- **Stripe Checkout + Własny Serwer**
  - ✅ Pełna kontrola nad procesem
  - ✅ Niższe koszty długoterminowe
  - ✅ Własne generowanie kluczy/licencji
  - ⚠️ Wymaga więcej pracy technicznej
  - 💰 Prowizja Stripe: 2.9% + 0.30 USD

### **💵 Model Cenowy**

#### **Opcje Cenowe:**
```
🆓 DARMOWA WERSJA
├── Podstawowe pobieranie (1 URL na raz)
├── Jakość standardowa (48kHz/16-bit)
├── Brak wsadowego przetwarzania
└── Watermark w metadanych

💎 LICENCJA PRO - 15 USD
├── Pobieranie wsadowe (listy URL-ów)
├── Wszystkie jakości audio (do 192kHz/24-bit)
├── Playlist support
├── Zaawansowane opcje CLI
├── Brak watermarków
└── Dożywotnie aktualizacje

🚀 LICENCJA BUSINESS - 45 USD
├── Wszystkie funkcje PRO
├── Komercyjne użytkowanie
├── API dla integracji
├── Priorytetowe wsparcie
└── Białe etykiety (white-label)
```

#### **Model Freemium:**
- **Darmowa wersja**: Podstawowa funkcjonalność z ograniczeniami
- **PRO funkcje**: Zaawansowane opcje za opłatą
- **Konwersja**: 2-5% użytkowników przechodzi na wersję płatną

### **🔐 System Licencjonowania**

#### **1. Implementacja Prosta (Offline)**
```python
# Struktura licencji lokalnej
{
    "license_key": "YTWAV-PRO-XXXX-XXXX-XXXX",
    "user_email": "user@example.com",
    "license_type": "PRO",
    "issued_date": "2024-01-15",
    "signature": "RSA_DIGITAL_SIGNATURE"
}
```

**Proces weryfikacji:**
1. Klient otrzymuje plik licencji po zakupie
2. Aplikacja weryfikuje podpis cyfrowy (RSA)
3. Sprawdza ważność i typ licencji
4. Odblokowuje funkcje PRO

#### **2. Implementacja Bezpieczna (Online)**
```python
# API endpoint weryfikacji
POST /api/verify-license
{
    "license_key": "YTWAV-PRO-XXXX-XXXX-XXXX",
    "machine_id": "UNIQUE_MACHINE_HASH",
    "app_version": "1.2.0"
}

# Odpowiedź serwera
{
    "valid": true,
    "license_type": "PRO",
    "features_enabled": ["batch_download", "high_quality", "playlist"],
    "expires_at": null  # null = dożywotnia
}
```

**Proces weryfikacji online:**
1. Aplikacja wysyła klucz do API przy starcie
2. Serwer sprawdza w bazie danych
3. Zwraca status i dostępne funkcje
4. Aplikacja konfiguje się zgodnie z licencją

#### **3. Implementacja Minimalna (MVP)**

**Generowanie klucza:**
```python
import uuid
import hashlib

def generate_license_key(email, license_type):
    # Unikalny identyfikator
    unique_id = str(uuid.uuid4())
    
    # Hash z email + typ licencji
    data = f"{email}:{license_type}:{unique_id}"
    key_hash = hashlib.sha256(data.encode()).hexdigest()[:16]
    
    # Format klucza: YTWAV-TYPE-HASH
    return f"YTWAV-{license_type}-{key_hash.upper()}"
```

**Weryfikacja w aplikacji:**
```python
def verify_license_key(key, email):
    try:
        parts = key.split('-')
        if len(parts) != 3 or parts[0] != 'YTWAV':
            return False
            
        license_type = parts[1]
        provided_hash = parts[2]
        
        # Sprawdź czy hash się zgadza
        expected_data = f"{email}:{license_type}:*"
        # Weryfikacja przez API lub lokalnie
        
        return True
    except:
        return False
```

### **🛡️ Zabezpieczenia Licencji**

#### **Offline Licensing:**
- **Podpisy cyfrowe RSA**: Niemożliwość sfałszowania
- **Machine binding**: Powiązanie z konkretnym komputerem
- **Encrypted storage**: Szyfrowane przechowywanie lokalnie
- **Checksum validation**: Sprawdzanie integralności pliku

#### **Online Licensing:**
- **Server-side validation**: Weryfikacja po stronie serwera
- **Rate limiting**: Ograniczenie częstotliwości sprawdzeń
- **Machine fingerprinting**: Unikalny odcisk komputera
- **Revocation support**: Możliwość unieważnienia licencji

#### **Hybrid Approach:**
```python
def check_license():
    # 1. Sprawdź licencję lokalnie
    local_valid = verify_local_license()
    
    # 2. Co 7 dni sprawdź online (jeśli internet)
    if should_check_online():
        online_valid = verify_online_license()
        if online_valid != local_valid:
            handle_license_mismatch()
    
    return local_valid
```

### **📊 Metryki Biznesowe**

#### **KPI do śledzenia:**
- **Conversion rate**: % darmowych użytkowników → płatni
- **Customer Lifetime Value (CLV)**: Wartość klienta
- **Churn rate**: Wskaźnik rezygnacji
- **Support tickets**: Liczba zgłoszeń wsparcia
- **Feature usage**: Wykorzystanie funkcji PRO

#### **A/B Testing:**
- Różne ceny (10 USD vs 15 USD vs 20 USD)
- Modele licencji (jednorazowa vs subskrypcja)
- Funkcje w wersji darmowej
- Komunikaty o upgrade

### **🚀 Strategia Go-to-Market**

#### **Faza 1: MVP (Miesiące 1-3)**
1. Wdrożenie Gumroad/Payhip
2. Jedna cena: 15 USD
3. Podstawowe funkcje PRO
4. Społeczność Reddit/Discord

#### **Faza 2: Skalowanie (Miesiące 4-12)**
1. Przejście na Paddle/FastSpring
2. Wprowadzenie modelu Freemium
3. Rozszerzenie funkcji
4. Marketing content (YouTube, blogi)

#### **Faza 3: Ekspansja (Rok 2+)**
1. Własna platforma płatności
2. API dla deweloperów
3. Wersje enterprise
4. Partnerstwa strategiczne

---

---

## 📝 PODSUMOWANIE

**YTWAV** to profesjonalna, stabilna aplikacja do pobierania audio z YouTube z następującymi kluczowymi cechami:

✅ **Wysokiej jakości audio** - WAV PCM bez kompresji  
✅ **Inteligentny retry system** - Obchodzenie blokad YouTube  
✅ **Dual interface** - GUI + CLI dla różnych użytkowników  
✅ **Auto-maintenance** - Automatyczne utrzymanie i aktualizacje  
✅ **macOS-only** - Działa na macOS  
✅ **Minimalne zależności** - Tylko yt-dlp + FFmpeg  
✅ **Profesjonalne logowanie** - Pełna diagnostyka i monitoring  
✅ **Bezpieczna architektura** - Obsługa błędów i walidacja danych  

Aplikacja jest gotowa do użycia produkcyjnego i może być łatwo rozszerzona o dodatkowe funkcjonalności.

---

*Dokumentacja wygenerowana automatycznie na podstawie analizy kodu źródłowego.*  
*Ostatnia aktualizacja: 2024*

## ENGLISH GUIDE — macOS

YTWAV is a macOS-only tool to download YouTube audio and convert it to lossless WAV/PCM. It provides a simple GUI (Tkinter) and a flexible CLI, using `yt-dlp` to fetch media and `ffmpeg` for conversion.

- macOS-only
- GUI (Tkinter) + CLI
- Minimal dependencies: `yt-dlp` and system `ffmpeg`

### Features
- Download audio and convert to WAV/PCM (via FFmpeg)
- Resilient retries to handle HTTP errors (403/429)
- Batch mode via URL list file
- Configurable audio settings: sample rate, channels, bit depth
- Safe filename handling
- Optional maintenance/diagnostics script

### Requirements
- `python3` (3.11+ recommended)
- Homebrew
- `ffmpeg` installed via Homebrew

### Installation
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
- Make macOS launch scripts executable (optional):
  ```bash
  chmod +x macos/run_gui.command macos/run_cli.sh
  ```

### Quick Start (GUI)
- Launch the GUI:
  ```bash
  ./macos/run_gui.command
  ```
- Alternatively:
  ```bash
  python3 ytwav_gui.py
  ```

### Quick Start (CLI)
- Single URL:
  ```bash
  ./macos/run_cli.sh "https://youtube.com/watch?v=VIDEO_ID"
  ```
- Using Python directly:
  ```bash
  python3 ytdl_wav.py "https://youtube.com/watch?v=VIDEO_ID"
  ```

### CLI Options
The CLI exposes control over output quality and behavior:
- `--list <file>`: Path to a text file with one URL per line (lines starting with `#` are comments)
- `-o, --out <dir>`: Output directory (default: `wav_out`)
- `--sr <int>`: Sample rate (default: `48000`)
- `--ch <1|2>`: Channels: `1` mono or `2` stereo (default: `2`)
- `--bit <16|24>`: WAV bit depth (default: `16`)
- `--keep-src`: Keep the original downloaded audio file (e.g., `.m4a`)
- `--retries <int>`: Retry count for errors (default: `5`)

Examples:
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

### Self-Repair (macOS)
To automatically fix common environment issues:
```bash
chmod +x macos/self_repair.sh
./macos/self_repair.sh
```
What it does:
- Upgrades `pip` and `yt-dlp`
- Installs/upgrades `ffmpeg` via Homebrew
- Clears `yt-dlp` cache
- Suggests PATH fixes for Apple Silicon
- Verifies environment and prints guidance

If issues persist, run diagnostics:
```bash
python3 maintenance.py
```

### Troubleshooting
- `ffmpeg: command not found`
  - Install FFmpeg: `brew install ffmpeg`
  - Verify PATH: `which ffmpeg`
- Permission denied when running scripts
  - Grant execute permission: `chmod +x macos/run_gui.command macos/run_cli.sh`
- Update `yt-dlp` if you see HTTP or extraction issues:
  ```bash
  pip3 install --upgrade yt-dlp
  ```

### CLI Options
The CLI exposes control over output quality and behavior:
- `--list <file>`: Path to a text file with one URL per line (lines starting with `#` are comments)
- `-o, --out <dir>`: Output directory (default: `wav_out`)
- `--sr <int>`: Sample rate (default: `48000`)
- `--ch <1|2>`: Channels: `1` mono or `2` stereo (default: `2`)
- `--bit <16|24>`: WAV bit depth (default: `16`)
- `--keep-src`: Keep the original downloaded audio file (e.g., `.m4a`)
- `--retries <int>`: Retry count for errors (default: `5`)

Examples:
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

### Self-Repair (macOS)
To automatically fix common environment issues:
```bash
chmod +x macos/self_repair.sh
./macos/self_repair.sh
```
What it does:
- Upgrades `pip` and `yt-dlp`
- Installs/upgrades `ffmpeg` via Homebrew
- Clears `yt-dlp` cache
- Suggests PATH fixes for Apple Silicon
- Verifies environment and prints guidance

If issues persist, run diagnostics:
```bash
python3 maintenance.py
```

### Troubleshooting
- `ffmpeg: command not found`
  - Install FFmpeg: `brew install ffmpeg`
  - Verify PATH: `which ffmpeg`
- Permission denied when running scripts
  - Grant execute permission: `chmod +x macos/run_gui.command macos/run_cli.sh`
- Update `yt-dlp` if you see HTTP or extraction issues:
  ```bash
  pip3 install --upgrade yt-dlp
  ```

### CLI Options
The CLI exposes control over output quality and behavior:
- `--list <file>`: Path to a text file with one URL per line (lines starting with `#` are comments)
- `-o, --out <dir>`: Output directory (default: `wav_out`)
- `--sr <int>`: Sample rate (default: `48000`)
- `--ch <1|2>`: Channels: `1` mono or `2` stereo (default: `2`)
- `--bit <16|24>`: WAV bit depth (default: `16`)
- `--keep-src`: Keep the original downloaded audio file (e.g., `.m4a`)
- `--retries <int>`: Retry count for errors (default: `5`)

Examples:
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

### Self-Repair (macOS)
To automatically fix common environment issues:
```bash
chmod +x macos/self_repair.sh
./macos/self_repair.sh
```
What it does:
- Upgrades `pip` and `yt-dlp`
- Installs/upgrades `ffmpeg` via Homebrew
- Clears `yt-dlp` cache
- Suggests PATH fixes for Apple Silicon
- Verifies environment and prints guidance

If issues persist, run diagnostics:
```bash
python3 maintenance.py
```

### Troubleshooting
- `ffmpeg: command not found`
  - Install FFmpeg: `brew install ffmpeg`
  - Verify PATH: `which ffmpeg`
- Permission denied when running scripts
  - Grant execute permission: `chmod +x macos/run_gui.command macos/run_cli.sh`
- Update `yt-dlp` if you see HTTP or extraction issues:
  ```bash
  pip3 install --upgrade yt-dlp
  ```