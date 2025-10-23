#!/usr/bin/env python3
"""
YTWAV - YouTube Audio Downloader
Szybkie, bezpieczne CLI do pobierania audio z YouTube i zapisu jako WAV PCM w wysokiej jakości.

Wymagania:
- yt-dlp
- ffmpeg (systemowy)

Autor: Senior Python Developer
Licencja: MIT
"""

import argparse
import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime

try:
    import yt_dlp
except ImportError:
    print("Błąd: Brak modułu yt-dlp. Zainstaluj: pip install yt-dlp")
    sys.exit(1)


class YTWavDownloader:
    """Klasa do pobierania audio z YouTube i konwersji do WAV PCM."""
    
    def __init__(self, output_dir: str = "wav_out", sample_rate: int = 48000, 
                 channels: int = 2, bit_depth: int = 16, keep_source: bool = False,
                 retries: int = 5):
        self.output_dir = Path(output_dir)
        self.sample_rate = sample_rate
        self.channels = channels
        self.bit_depth = bit_depth
        self.keep_source = keep_source
        self.retries = retries
        self.output_dir.mkdir(exist_ok=True)
        
        # Konfiguracja loggingu
        self.setup_logging()
        
        # Hints engine
        self.show_hints()
        
    def setup_logging(self):
        """Konfiguruje logowanie z timestampem."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        
    def show_hints(self):
        """Hints engine - wyświetla ostrzeżenia i wskazówki."""
        if self.bit_depth == 24:
            self.logger.warning("Używasz 24-bit audio - pliki będą większe (około 50% więcej miejsca)")
        
        if self.channels == 1:
            self.logger.info("Wymuszasz mono audio (1 kanał)")
            
        self.logger.info(f"Konfiguracja: {self.sample_rate}Hz, {self.channels}ch, {self.bit_depth}bit")
        
    def check_ffmpeg(self) -> bool:
        """Sprawdza czy ffmpeg jest dostępny w systemie."""
        if not shutil.which("ffmpeg"):
            self.logger.error("FFmpeg nie jest zainstalowany lub niedostępny w PATH")
            self.logger.error("Instrukcje instalacji:")
            self.logger.error("  Windows: choco install ffmpeg lub zobacz scripts/win_install_ffmpeg.md")
            self.logger.error("  macOS: brew install ffmpeg")
            self.logger.error("  Linux: sudo apt install ffmpeg (Ubuntu/Debian)")
            return False
        return True
    
    def auto_update_ytdlp(self) -> bool:
        """Automatycznie aktualizuje yt-dlp do najnowszej wersji."""
        try:
            self.logger.info("Próbuję zaktualizować yt-dlp do najnowszej wersji...")
            import subprocess
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.logger.info("yt-dlp zaktualizowany pomyślnie!")
                return True
            else:
                self.logger.warning(f"Nie udało się zaktualizować yt-dlp: {result.stderr}")
                return False
        except Exception as e:
            self.logger.warning(f"Błąd podczas aktualizacji yt-dlp: {e}")
            return False
    
    def load_urls_from_file(self, file_path: Path) -> List[str]:
        """Ładuje URL-e z pliku tekstowego."""
        urls = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    # Pomijaj puste linie i komentarze
                    if line and not line.startswith('#'):
                        if self.is_valid_youtube_url(line):
                            urls.append(line)
                        else:
                            self.logger.warning(f"Linia {line_num}: Nieprawidłowy URL YouTube: {line}")
            self.logger.info(f"Załadowano {len(urls)} URL-ów z pliku {file_path}")
        except FileNotFoundError:
            self.logger.error(f"Nie znaleziono pliku: {file_path}")
        except Exception as e:
            self.logger.error(f"Błąd podczas czytania pliku {file_path}: {e}")
        return urls
    
    def load_all_urls(self, single_url: Optional[str], list_file: Optional[str]) -> List[str]:
        """Jednolity loader URL-ów - łączy single URL + --list."""
        urls = []
        
        # Załaduj z pojedynczego URL
        if single_url:
            if self.is_valid_youtube_url(single_url):
                urls.append(single_url)
            else:
                self.logger.error(f"Nieprawidłowy URL YouTube: {single_url}")
        
        # Załaduj z pliku listy
        if list_file:
            file_urls = self.load_urls_from_file(list_file)
            urls.extend(file_urls)
        
        return urls
    
    def is_valid_youtube_url(self, url: str) -> bool:
        """Sprawdza czy URL jest prawidłowym linkiem YouTube."""
        youtube_domains = ['youtube.com', 'youtu.be', 'm.youtube.com', 'www.youtube.com']
        return any(domain in url for domain in youtube_domains)
    
    def build_opts(self, out_dir: Path, sr: int, ch: int, bit: int, 
                   keep_src: bool, retries: int) -> dict:
        """Buduje opcje konfiguracyjne dla yt-dlp."""
        # Określenie formatu sample dla FFmpeg
        if bit == 16:
            sample_fmt = "s16"
        elif bit == 24:
            sample_fmt = "s32"  # FFmpeg bezpieczny 24-bit PCM w kontenerze WAV
        else:
            raise ValueError(f"Nieobsługiwana głębia bitowa: {bit}")
        
        opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best[height<=720]',
            'outtmpl': str(out_dir / '%(title).200B.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '0'
            }],
            'postprocessor_args': [
                '-ar', str(sr),
                '-ac', str(ch),
                '-sample_fmt', sample_fmt
            ],
            'retries': retries,
            'fragment_retries': retries,
            'ignoreerrors': 'only_download',
            'windowsfilenames': True,
            'consoletitle': True,
            'noprogress': False,
            'no_warnings': False,  # Włączam ostrzeżenia aby zobaczyć co się dzieje
            'sleep_interval': 1,  # Opóźnienie między requestami
            'max_sleep_interval': 5,  # Maksymalne opóźnienie
            'sleep_interval_subtitles': 0,
            'extractor_retries': 3,  # Dodatkowe próby dla extractora
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        }
        
        # Zachowaj plik źródłowy jeśli wymagane
        if not keep_src:
            opts['keepvideo'] = False
            
        return opts
    
    def sanitize_filename(self, filename: str) -> str:
        """Czyści nazwę pliku z niedozwolonych znaków."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:200]  # Ograniczenie długości
    
    def download_audio(self, url: str, output_filename: Optional[str] = None) -> bool:
        """Pobiera audio z YouTube i konwertuje do WAV PCM z inteligentnym retry."""
        
        if not self.check_ffmpeg():
            return False
        
        # Różne strategie retry przeciwko blokowaniu - zoptymalizowane na podstawie obserwacji
        retry_strategies = [
            {'sleep_interval': 2, 'user_agent_suffix': ''},
            {'sleep_interval': 5, 'user_agent_suffix': ' Edg/120.0.0.0'},
            {'sleep_interval': 8, 'user_agent_suffix': ' Firefox/120.0'},
            {'sleep_interval': 12, 'user_agent_suffix': ' Safari/537.36'},
            {'sleep_interval': 15, 'user_agent_suffix': ' Chrome/120.0.0.0'},
        ]
        
        for attempt, strategy in enumerate(retry_strategies, 1):
            try:
                self.logger.info(f"Próba {attempt}/{len(retry_strategies)}: {url}")
                
                # Budowanie opcji yt-dlp z aktualną strategią
                ydl_opts = self.build_opts(
                    out_dir=self.output_dir,
                    sr=self.sample_rate,
                    ch=self.channels,
                    bit=self.bit_depth,
                    keep_src=self.keep_source,
                    retries=self.retries
                )
                
                # Modyfikacja User-Agent dla różnych prób
                base_ua = ydl_opts['http_headers']['User-Agent']
                ydl_opts['http_headers']['User-Agent'] = base_ua + strategy['user_agent_suffix']
                ydl_opts['sleep_interval'] = strategy['sleep_interval']
                
                # Niestandardowa nazwa pliku
                if output_filename:
                    clean_filename = self.sanitize_filename(output_filename)
                    if not clean_filename.endswith('.wav'):
                        clean_filename += '.wav'
                    ydl_opts['outtmpl'] = str(self.output_dir / clean_filename.replace('.wav', '.%(ext)s'))
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    self.logger.info(f"Pobieranie audio z: {url}")
                    ydl.download([url])
                    self.logger.info("Pobieranie zakończone pomyślnie!")
                    return True
                    
            except yt_dlp.DownloadError as e:
                error_msg = str(e).lower()
                if 'http error 403' in error_msg or 'forbidden' in error_msg:
                    self.logger.warning(f"Próba {attempt} zablokowana (403). Czekam {strategy['sleep_interval']*2}s...")
                    import time
                    time.sleep(strategy['sleep_interval'] * 2)
                    if attempt < len(retry_strategies):
                        continue
                self.logger.error(f"Błąd pobierania {url}: {e}")
                if attempt == len(retry_strategies):
                    # Ostatnia próba - spróbuj zaktualizować yt-dlp
                    self.logger.warning("Wszystkie strategie retry zawiodły. Próbuję zaktualizować yt-dlp...")
                    if self.auto_update_ytdlp():
                        self.logger.info("Ponawiam pobieranie po aktualizacji yt-dlp...")
                        import time
                        time.sleep(3)
                        # Jedna dodatkowa próba po aktualizacji
                        try:
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                ydl.download([url])
                                self.logger.info("Pobieranie zakończone pomyślnie po aktualizacji!")
                                return True
                        except Exception as final_e:
                            self.logger.error(f"Pobieranie nie powiodło się nawet po aktualizacji: {final_e}")
                    return False
            except Exception as e:
                self.logger.error(f"Nieoczekiwany błąd dla {url}: {e}")
                if attempt == len(retry_strategies):
                    return False
        
        return False
    
    def get_video_info(self, url: str) -> Optional[dict]:
        """Pobiera informacje o filmie bez pobierania."""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Nieznany tytuł'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Nieznany autor'),
                    'view_count': info.get('view_count', 0)
                }
        except Exception as e:
            print(f"Błąd pobierania informacji: {e}")
            return None


def main():
    """Główna funkcja CLI."""
    parser = argparse.ArgumentParser(
        description="Pobierz audio z YouTube i konwertuj do WAV PCM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  %(prog)s "https://youtube.com/watch?v=VIDEO_ID"
  %(prog)s --list urls.txt -o custom_dir
  %(prog)s "https://youtube.com/watch?v=VIDEO_ID" --sr 44100 --ch 1 --bit 24
        """
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        help="URL do filmu YouTube (opcjonalnie jeśli używasz --list)"
    )
    
    parser.add_argument(
        "--list",
        help="Plik .txt z URL-ami (po jednym na linię, # = komentarz)"
    )
    
    parser.add_argument(
        "-o", "--out",
        default="wav_out",
        help="Katalog wyjściowy (domyślnie: wav_out)"
    )
    
    parser.add_argument(
        "--sr",
        type=int,
        default=48000,
        help="Sample rate (domyślnie: 48000)"
    )
    
    parser.add_argument(
        "--ch",
        type=int,
        choices=[1, 2],
        default=2,
        help="Liczba kanałów: 1=mono, 2=stereo (domyślnie: 2)"
    )
    
    parser.add_argument(
        "--bit",
        type=int,
        choices=[16, 24],
        default=16,
        help="Głębia bitowa WAV: 16 lub 24 (domyślnie: 16)"
    )
    
    parser.add_argument(
        "--keep-src",
        action="store_true",
        help="Zachowaj plik źródłowy audio (np. .m4a)"
    )
    
    parser.add_argument(
        "--retries",
        type=int,
        default=5,
        help="Liczba ponowień przy błędach (domyślnie: 5)"
    )
    
    args = parser.parse_args()
    
    # Tworzenie downloadera
    downloader = YTWavDownloader(
        output_dir=args.out,
        sample_rate=args.sr,
        channels=args.ch,
        bit_depth=args.bit,
        keep_source=args.keep_src,
        retries=args.retries
    )
    
    # Wyświetl hinty
    downloader.show_hints()
    
    # Jednolity loader URL-ów
    urls = downloader.load_all_urls(args.url, args.list)
    
    # Sprawdź czy są jakiekolwiek URL-e
    if not urls:
        if not args.url and not args.list:
            downloader.logger.error("Musisz podać URL lub plik z listą URL-ów (--list)")
        else:
            downloader.logger.error("Nie znaleziono prawidłowych URL-ów")
        sys.exit(2)  # Exit code 2 dla braku URL-ów
    
    # Pobieranie audio
    success_count = 0
    total_count = len(urls)
    
    downloader.logger.info(f"Rozpoczynam pobieranie {total_count} plików...")
    
    for i, url in enumerate(urls, 1):
        downloader.logger.info(f"[{i}/{total_count}] Przetwarzanie: {url}")
        if downloader.download_audio(url):
            success_count += 1
    
    # Podsumowanie
    downloader.logger.info(f"Zakończono: {success_count}/{total_count} plików pobrano pomyślnie")
    
    if success_count == total_count:
        downloader.logger.info("✅ Wszystkie operacje zakończone pomyślnie!")
        sys.exit(0)
    elif success_count > 0:
        downloader.logger.warning(f"⚠️ Częściowy sukces: {success_count}/{total_count}")
        sys.exit(0)
    else:
        downloader.logger.error("❌ Wszystkie operacje zakończone niepowodzeniem!")
        sys.exit(1)


def download_wav(url: str, output_dir: str = "wav_out") -> bool:
    """
    Prosta funkcja do pobierania audio z YouTube i konwersji do WAV PCM.
    Używana przez GUI i CLI.
    
    Args:
        url: URL YouTube do pobrania
        output_dir: Katalog wyjściowy (domyślnie: wav_out)
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        downloader = YTWavDownloader(
            output_dir=output_dir,
            sample_rate=48000,
            channels=2,
            bit_depth=16,
            keep_source=False,
            retries=5
        )
        
        return downloader.download_audio(url)
        
    except Exception as e:
        print(f"Błąd podczas pobierania: {e}")
        return False


if __name__ == "__main__":
    main()