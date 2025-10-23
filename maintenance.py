#!/usr/bin/env python3
"""
🛠️ Skrypt utrzymania systemu YT Downloader
Automatyczne monitorowanie, aktualizacje i diagnostyka
"""

import subprocess
import sys
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import yt_dlp
import requests

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('maintenance.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YTDownloaderMaintenance:
    def __init__(self):
        self.logger = logger  # Przypisanie globalnego loggera
        self.test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll - zawsze dostępny
            "https://www.youtube.com/watch?v=9bZkp7q19f0",  # Gangnam Style
        ]
        self.status_file = Path("maintenance_status.json")
    
    def safe_title(self, title):
        """Bezpieczne formatowanie tytułu dla Windows console"""
        if not title:
            return "Nieznany tytuł"
        # Usuń znaki, które mogą powodować problemy z kodowaniem
        safe = title.encode('ascii', errors='ignore').decode('ascii')
        return safe if safe else "Tytuł z znakami specjalnymi"
        
    def check_ytdlp_version(self):
        """Sprawdza aktualną i najnowszą wersję yt-dlp"""
        try:
            # Aktualna wersja
            current = yt_dlp.version.__version__
            
            # Najnowsza wersja z PyPI
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
            latest = response.json()["info"]["version"]
            
            logger.info(f"yt-dlp: aktualna={current}, najnowsza={latest}")
            
            return {
                "current": current,
                "latest": latest,
                "needs_update": current != latest
            }
        except Exception as e:
            logger.error(f"Błąd sprawdzania wersji yt-dlp: {e}")
            return None
    
    def update_ytdlp(self):
        """Aktualizuje yt-dlp do najnowszej wersji"""
        try:
            logger.info("Aktualizuję yt-dlp...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("[OK] yt-dlp zaktualizowany pomyślnie")
                return True
            else:
                logger.error(f"[ERROR] Błąd aktualizacji yt-dlp: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"[ERROR] Wyjątek podczas aktualizacji: {e}")
            return False
    
    def test_download_capability(self):
        """Testuje możliwość pobierania z YouTube"""
        success_count = 0
        total_tests = len(self.test_urls)
        
        for i, url in enumerate(self.test_urls, 1):
            logger.info(f"Test {i}/{total_tests}: {url}")
            
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,
                    'skip_download': True,  # Tylko test, bez pobierania
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    if info and info.get('title'):
                        safe_title = self.safe_title(info.get('title'))
                        logger.info(f"[OK] Test {i} OK: {safe_title}")
                        success_count += 1
                    else:
                        logger.warning(f"[WARN] Test {i} - brak informacji o filmie")
                        
            except Exception as e:
                logger.error(f"[ERROR] Test {i} nieudany: {e}")
        
        success_rate = (success_count / total_tests) * 100
        logger.info(f"Wynik testów: {success_count}/{total_tests} ({success_rate:.1f}%)")
        
        return {
            "success_count": success_count,
            "total_tests": total_tests,
            "success_rate": success_rate,
            "status": "OK" if success_rate >= 80 else "PROBLEM"
        }
    
    def check_ffmpeg(self):
        """Sprawdza dostępność FFmpeg"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                logger.info(f"[OK] FFmpeg OK: {version_line}")
                return {"status": "OK", "version": version_line}
            else:
                logger.error("[ERROR] FFmpeg nie odpowiada")
                return {"status": "ERROR", "error": "No response"}
        except FileNotFoundError:
            logger.error("[ERROR] FFmpeg nie znaleziony")
            return {"status": "NOT_FOUND", "error": "FFmpeg not installed"}
        except Exception as e:
            logger.error(f"[ERROR] Błąd sprawdzania FFmpeg: {e}")
            return {"status": "ERROR", "error": str(e)}
    
    def save_status(self, status_data):
        """Zapisuje status do pliku JSON"""
        try:
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Błąd zapisu statusu: {e}")
    
    def load_status(self):
        """Ładuje poprzedni status"""
        try:
            if self.status_file.exists():
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Błąd odczytu statusu: {e}")
        return {}
    
    def update_success_metrics(self, success: bool, error_type: str = None):
        """Aktualizuje metryki sukcesu pobierania."""
        status = self.load_status()
        
        if 'metrics' not in status:
            status['metrics'] = {
                'total_attempts': 0,
                'successful_downloads': 0,
                'failed_downloads': 0,
                'error_types': {},
                'success_rate': 0.0
            }
        
        metrics = status['metrics']
        metrics['total_attempts'] += 1
        
        if success:
            metrics['successful_downloads'] += 1
        else:
            metrics['failed_downloads'] += 1
            if error_type:
                metrics['error_types'][error_type] = metrics['error_types'].get(error_type, 0) + 1
        
        # Oblicz wskaźnik sukcesu
        if metrics['total_attempts'] > 0:
            metrics['success_rate'] = (metrics['successful_downloads'] / metrics['total_attempts']) * 100
        
        metrics['last_updated'] = datetime.now().isoformat()
        self.save_status(status)
        
        return metrics

    def show_success_statistics(self):
        """Wyświetla statystyki sukcesu pobierania."""
        status = self.load_status()
        
        if 'metrics' not in status:
            self.logger.info("Brak danych statystycznych")
            return
        
        metrics = status['metrics']
        self.logger.info("=== STATYSTYKI SUKCESU POBIERANIA ===")
        self.logger.info(f"Łączna liczba prób: {metrics['total_attempts']}")
        self.logger.info(f"Udane pobierania: {metrics['successful_downloads']}")
        self.logger.info(f"Nieudane pobierania: {metrics['failed_downloads']}")
        self.logger.info(f"Wskaźnik sukcesu: {metrics['success_rate']:.1f}%")
        
        if metrics['error_types']:
            self.logger.info("Typy błędów:")
            for error_type, count in metrics['error_types'].items():
                self.logger.info(f"  - {error_type}: {count}")
        
        if 'last_updated' in metrics:
            self.logger.info(f"Ostatnia aktualizacja: {metrics['last_updated']}")

    def run_maintenance(self, auto_update=True):
        """Główna funkcja utrzymania systemu"""
        logger.info("[MAINTENANCE] Rozpoczynam utrzymanie systemu YT Downloader")
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # 1. Sprawdź wersję yt-dlp
        logger.info("[1/4] Sprawdzam wersję yt-dlp...")
        ytdlp_info = self.check_ytdlp_version()
        status["checks"]["ytdlp_version"] = ytdlp_info
        
        # 2. Aktualizuj jeśli potrzeba
        if auto_update and ytdlp_info and ytdlp_info.get("needs_update"):
            logger.info("[2/4] Aktualizuję yt-dlp...")
            update_success = self.update_ytdlp()
            status["checks"]["ytdlp_update"] = {"success": update_success}
        
        # 3. Sprawdź FFmpeg
        logger.info("[3/4] Sprawdzam FFmpeg...")
        ffmpeg_status = self.check_ffmpeg()
        status["checks"]["ffmpeg"] = ffmpeg_status
        
        # 4. Testuj pobieranie
        logger.info("[4/4] Testuję pobieranie z YouTube...")
        download_test = self.test_download_capability()
        status["checks"]["download_test"] = download_test
        
        # 5. Zapisz status
        self.save_status(status)
        
        # 6. Podsumowanie
        logger.info("[SUMMARY] PODSUMOWANIE UTRZYMANIA:")
        logger.info(f"   yt-dlp: {ytdlp_info.get('current', 'nieznana') if ytdlp_info else 'błąd'}")
        logger.info(f"   FFmpeg: {ffmpeg_status['status']}")
        logger.info(f"   Testy pobierania: {download_test['status']} ({download_test['success_rate']:.1f}%)")
        
        # Zwróć ogólny status
        overall_status = "OK"
        if ffmpeg_status["status"] != "OK":
            overall_status = "FFMPEG_PROBLEM"
        elif download_test["status"] != "OK":
            overall_status = "DOWNLOAD_PROBLEM"
        
        logger.info(f"[RESULT] Status ogólny: {overall_status}")
        return overall_status

def main():
    """Główna funkcja skryptu"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Utrzymanie systemu YT Downloader")
    parser.add_argument("--no-update", action="store_true", 
                       help="Nie aktualizuj automatycznie yt-dlp")
    parser.add_argument("--test-only", action="store_true",
                       help="Tylko testy, bez aktualizacji")
    parser.add_argument("--stats", action="store_true",
                       help="Pokaż statystyki sukcesu")
    
    args = parser.parse_args()
    
    maintenance = YTDownloaderMaintenance()
    
    if args.stats:
        # Pokaż statystyki
        print("=== STATYSTYKI SYSTEMU ===")
        maintenance.show_success_statistics()
    elif args.test_only:
        # Tylko testy
        download_test = maintenance.test_download_capability()
        ffmpeg_status = maintenance.check_ffmpeg()
        print(f"Testy pobierania: {download_test['status']}")
        print(f"FFmpeg: {ffmpeg_status['status']}")
    else:
        # Pełne utrzymanie
        auto_update = not args.no_update
        status = maintenance.run_maintenance(auto_update=auto_update)
        sys.exit(0 if status == "OK" else 1)

if __name__ == "__main__":
    main()