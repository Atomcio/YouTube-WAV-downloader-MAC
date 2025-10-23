#!/usr/bin/env python3
"""
YTWAV GUI - Minimalistyczny interfejs graficzny dla YouTube Audio Downloader
Retro-style Tkinter GUI (400x120px, nierozszerzalne)

Wymagania:
- tkinter (wbudowany w Python)
- ytdl_wav.py (logika pobierania)

Autor: Senior Python Developer
Licencja: MIT
"""

import tkinter as tk
from tkinter import messagebox
import shutil
import sys
import os

# Import funkcji pobierania z głównego modułu
try:
    from ytdl_wav import download_wav
except ImportError:
    messagebox.showerror("Błąd", "Nie można zaimportować ytdl_wav.py")
    sys.exit(1)


class YTWavGUI:
    """Minimalistyczny GUI dla pobierania audio z YouTube."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.check_ffmpeg_on_startup()
        
    def setup_window(self):
        """Konfiguruje główne okno aplikacji."""
        self.root.title("YT → WAV Downloader")
        self.root.geometry("400x120")
        self.root.resizable(False, False)
        
        # Centrowanie okna na ekranie
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (120 // 2)
        self.root.geometry(f"400x120+{x}+{y}")
        
    def create_widgets(self):
        """Tworzy elementy interfejsu."""
        # Etykieta
        label = tk.Label(
            self.root, 
            text="Wklej link YouTube:",
            font=("Arial", 10)
        )
        label.pack(pady=(15, 5))
        
        # Pole tekstowe na URL
        self.url_entry = tk.Entry(
            self.root,
            width=50,
            font=("Arial", 9)
        )
        self.url_entry.pack(pady=5)
        
        # Przycisk pobierania
        download_btn = tk.Button(
            self.root,
            text="Pobierz",
            command=self.download_audio,
            font=("Arial", 10, "bold"),
            width=15,
            height=1
        )
        download_btn.pack(pady=(10, 15))
        
        # Focus na pole tekstowe
        self.url_entry.focus()
        
        # Bind Enter key do pobierania
        self.root.bind('<Return>', lambda event: self.download_audio())
        
    def check_ffmpeg_on_startup(self):
        """Sprawdza dostępność FFmpeg przy starcie aplikacji."""
        if not shutil.which("ffmpeg"):
            messagebox.showerror(
                "Błąd FFmpeg",
                "FFmpeg nie jest zainstalowany lub niedostępny w PATH.\n\n"
                "Instrukcje instalacji:\n"
                "• Windows: choco install ffmpeg\n"
                "• macOS: brew install ffmpeg\n"
                "• Linux: sudo apt install ffmpeg"
            )
            self.root.destroy()
            sys.exit(1)
            
    def download_audio(self):
        """Handler przycisku pobierania."""
        url = self.url_entry.get().strip()
        
        # Sprawdzenie czy URL został podany
        if not url:
            messagebox.showwarning(
                "Brak linku",
                "Proszę wkleić link YouTube do pobrania."
            )
            return
            
        # Sprawdzenie czy to prawidłowy URL YouTube
        youtube_domains = ['youtube.com', 'youtu.be', 'm.youtube.com', 'www.youtube.com']
        if not any(domain in url for domain in youtube_domains):
            messagebox.showwarning(
                "Nieprawidłowy link",
                "To nie wygląda na prawidłowy link YouTube."
            )
            return
            
        # Wyłączenie przycisku podczas pobierania
        download_btn = None
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                download_btn = widget
                break
                
        if download_btn:
            download_btn.config(state="disabled", text="Pobieranie...")
            
        self.root.update()
        
        try:
            # Wywołanie funkcji pobierania
            success = download_wav(url, "wav_out")
            
            if success:
                messagebox.showinfo(
                    "Sukces",
                    "Audio zostało pomyślnie pobrane i zapisane jako WAV!\n\n"
                    "Lokalizacja: wav_out/"
                )
                # Wyczyść pole tekstowe po sukcesie
                self.url_entry.delete(0, tk.END)
            else:
                messagebox.showerror(
                    "Błąd pobierania",
                    "Nie udało się pobrać audio.\n\n"
                    "Sprawdź link YouTube i połączenie internetowe."
                )
                
        except Exception as e:
            messagebox.showerror(
                "Nieoczekiwany błąd",
                f"Wystąpił błąd podczas pobierania:\n\n{str(e)}"
            )
            
        finally:
            # Przywrócenie przycisku
            if download_btn:
                download_btn.config(state="normal", text="Pobierz")
                
    def run(self):
        """Uruchamia główną pętlę GUI."""
        self.root.mainloop()


def main():
    """Główna funkcja GUI."""
    try:
        app = YTWavGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nZamykanie aplikacji...")
    except Exception as e:
        messagebox.showerror("Błąd krytyczny", f"Nie można uruchomić aplikacji:\n\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()