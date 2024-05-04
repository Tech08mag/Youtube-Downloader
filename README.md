# Youtube-Downloader

(Es wird vorrausgesetzt, dass man Python installiert hat)
## Wie lasse ich den Code laufen?
1. Gebe 'pip install -r requirements.txt' ins Terminal ein.
Diese installiert alles nötige, um den Code laufen zu lassen
2. Führe die main.py aus
3. Gebe einen Link ein und die gewünschte Auflösung. Anschließend kannst du das Video in dem Ordner "Videos" finden.

## Wie erstelle ich eine .exe oder eine andere ausführbare Datei
1. installiere pyinstaller
2. Gebe das folgende ins Terminal ein:
pyinstaller --onefile --add-data "youtube.ico;." main.py -y -w -n="Youtube_downloader"
3. Die ausführbare Datei finden sie in dem ordner dist

## erstellt von tech08mag 