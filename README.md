# Youtube-Downloader
(Die Software ffmpeg wird vorausgesetzt.)
https://ffmpeg.org/download.html
(Es wird vorrausgesetzt, dass man Python installiert hat)
## Wie lasse ich den Code laufen?
1. Gebe 'pip3 install -r requirements.txt' ins Terminal ein.
Diese installiert alles nötige, um den Code laufen zu lassen.
2. Führe die main.py aus

## Wie erstelle ich eine .exe oder eine andere ausführbare Datei
1. installiere pyinstaller
2. Gebe das folgende ins Terminal ein:
pyinstaller --onefile --add-data "youtube.ico:." --add-binary "PATH_TO_ffmpeg.exe:." main.py -y -w -n="Youtube_downloader"
3. Die ausführbare Datei finden sie in dem ordner dist

## erstellt von tech08mag 