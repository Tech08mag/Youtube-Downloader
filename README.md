# Youtube-Downloader

(Es wird vorrausgesetzt, dass man Python installiert hat)

## Wie lasse ich den Code laufen?

1. Gebe 'pip install -r requirements.txt' ins Terminal ein.
   Diese installiert alles nötige, um den Code laufen zu lassen.
2. Führe die main.py aus
3. Gebe einen Link ein und die gewünschte Auflösung. Anschließend kannst du das Video in dem Ordner "Videos" finden.

## Wie erstelle ich eine .exe oder eine andere ausführbare Datei

1. installiere pyinstaller
2. Gebe das folgende ins Terminal ein:
   pyinstaller --onefile --add-data "youtube.ico:." --add-binary "PATH_TO_FFMPEG:." main.py -y -w -n="Youtube_downloader"
3. Die ausführbare Datei finden sie in dem ordner dist

[![Python][Python]][Python-url] [![ctk][ctk]][ctk-url] [![yt-dlp][yt-dlp]][yt-dlp-url]

# Funktionen

- [x] YouTube-Videos in der höchsten Auflösungen herunterladen
- [x] Grafisches Userinterface mit [custom tkinter](https://customtkinter.tomschimansky.com/)
- [x] Datei an einem beliebigen Ort im Dateisystem ablegen
- [x] Output file ist immer eine .mp4/.mp3
- [x] Enter downloadet das Video
- [x] Path in settings.json angeben

## Vorraussetzungen

- [ffmpeg](https://ffmpeg.org/download.html)
- [Python 3.8+](https://www.python.org/downloads/)

## Installation & Start

1. Repository klonen

```sh
git clone https://github.com/Tech08mag/Youtube-Downloader.git
```

2. Virtuelle Python-Environment erstellen

```sh
python -m venv venv
```

3. Environment aktivieren

```sh
# Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

4. Anghängigkeiten installieren

```sh
pip install -r requirements.txt
```

5. Führe die `main.py` aus

```sh
# Standart
python main.py
# Python 3
python3 main.py
```

## Script in auführbare Datei kompilieren

1. Python-Libary `pyinstaller` installieren

```sh
# Standart
pip install pyinstaller
# Python 3
pip3 install pyinstaller
```

2. Folgender command muss aus dem home-Verzeichnis des Projektes im Terminal ausgeführt werden:

```sh
pyinstaller --onefile --add-data "youtube.ico:." --add-binary "PATH_TO_ffmpeg.exe:." main.py -y -w -n="Youtube_downloader"
```

3. Die ausführbare Datei findet sich in dem Ordner `dist` wieder

## erstellt von tech08mag

<img src="https://github.com/Tech08mag/Tech08mag/blob/main/profile.jpeg" alt="Profile">

[Python]: https://img.shields.io/badge/Language-Python-green
[Python-url]: https://www.python.org/
[ctk]: https://img.shields.io/badge/Framework-custom--tkinter-blue
[ctk-url]: https://customtkinter.tomschimansky.com/
[yt-dlp]: https://img.shields.io/badge/Build--With-yt--dlp-blue
[yt-dlp-url]: https://github.com/yt-dlp/yt-dlp
