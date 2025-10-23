#!/usr/bin/env python3
"""
🧪 Test zoptymalizowanego systemu obronnego
Testuje nowe strategie retry i zbiera metryki
"""

import sys
import time
from pathlib import Path
from ytdl_wav import YTDownloader
from maintenance import YTDownloaderMaintenance

def test_optimized_defense():
    """Testuje zoptymalizowany system obronny."""
    
    print("🧪 TESTOWANIE ZOPTYMALIZOWANEGO SYSTEMU OBRONNEGO")
    print("=" * 60)
    
    # Inicjalizacja
    downloader = YTDownloader()
    maintenance = YTDownloaderMaintenance()
    
    # URLs do testowania (różne poziomy trudności)
    test_cases = [
        {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "description": "Rick Roll - standardowy test",
            "expected_difficulty": "łatwy"
        },
        {
            "url": "https://www.youtube.com/watch?v=9bZkp7q19f0", 
            "description": "Gangnam Style - test z znakami specjalnymi",
            "expected_difficulty": "średni"
        },
        {
            "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
            "description": "Despacito - popularny film",
            "expected_difficulty": "trudny"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{len(test_cases)}: {test_case['description']}")
        print(f"🔗 URL: {test_case['url']}")
        print(f"🎯 Oczekiwana trudność: {test_case['expected_difficulty']}")
        
        start_time = time.time()
        
        try:
            # Próba pobrania
            success = downloader.download_audio(test_case['url'])
            end_time = time.time()
            duration = end_time - start_time
            
            result = {
                'test_case': test_case,
                'success': success,
                'duration': duration,
                'error_type': None
            }
            
            if success:
                print(f"✅ SUKCES w {duration:.1f}s")
                maintenance.update_success_metrics(True)
            else:
                print(f"❌ NIEPOWODZENIE po {duration:.1f}s")
                maintenance.update_success_metrics(False, "download_failed")
                result['error_type'] = "download_failed"
                
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            error_type = type(e).__name__
            
            print(f"💥 BŁĄD: {error_type} po {duration:.1f}s")
            print(f"   Szczegóły: {str(e)}")
            
            maintenance.update_success_metrics(False, error_type)
            
            result = {
                'test_case': test_case,
                'success': False,
                'duration': duration,
                'error_type': error_type,
                'error_message': str(e)
            }
        
        results.append(result)
        
        # Przerwa między testami
        if i < len(test_cases):
            print("⏳ Przerwa 5s między testami...")
            time.sleep(5)
    
    # Podsumowanie
    print("\n" + "=" * 60)
    print("📊 PODSUMOWANIE TESTÓW")
    print("=" * 60)
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    success_rate = (successful / total) * 100 if total > 0 else 0
    
    print(f"✅ Udane testy: {successful}/{total}")
    print(f"📈 Wskaźnik sukcesu: {success_rate:.1f}%")
    
    avg_duration = sum(r['duration'] for r in results) / len(results)
    print(f"⏱️  Średni czas: {avg_duration:.1f}s")
    
    # Analiza błędów
    error_types = {}
    for result in results:
        if not result['success'] and result['error_type']:
            error_types[result['error_type']] = error_types.get(result['error_type'], 0) + 1
    
    if error_types:
        print("\n🔍 Analiza błędów:")
        for error_type, count in error_types.items():
            print(f"   - {error_type}: {count}")
    
    # Pokaż ogólne statystyki
    print("\n📈 OGÓLNE STATYSTYKI SYSTEMU:")
    maintenance.show_success_statistics()
    
    return results

if __name__ == "__main__":
    try:
        results = test_optimized_defense()
        print("\n🎉 Test zakończony pomyślnie!")
        
        # Zapisz wyniki do pliku
        import json
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        print("💾 Wyniki zapisane do test_results.json")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test przerwany przez użytkownika")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Błąd krytyczny: {e}")
        sys.exit(1)