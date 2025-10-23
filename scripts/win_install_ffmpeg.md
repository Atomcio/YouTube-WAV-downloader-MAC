# Instalacja FFmpeg na Windows

## Opcja 1: Winget (Windows 10/11)

```powershell
winget install Gyan.FFmpeg
```

## Opcja 2: Chocolatey

```powershell
# Instalacja Chocolatey (jeśli nie masz)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalacja FFmpeg
choco install ffmpeg
```

## Weryfikacja instalacji

```powershell
ffmpeg -version
```

Powinno wyświetlić informacje o wersji FFmpeg. Jeśli komenda nie jest rozpoznana, uruchom ponownie terminal lub dodaj FFmpeg do PATH ręcznie.

## Rozwiązywanie problemów

- **Komenda nie znaleziona**: Uruchom ponownie PowerShell/CMD jako administrator
- **PATH**: FFmpeg powinien być automatycznie dodany do PATH przez winget/chocolatey
- **Uprawnienia**: Upewnij się, że uruchamiasz terminal jako administrator