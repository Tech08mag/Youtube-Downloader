import yt_dlp
import ctypes
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
import os
import sys

# For information see also:
#
# - [General Doc](https://pypi.org/project/yt-dlp/)
# - [Code relevant doc](https://pypi.org/project/yt-dlp/#embedding-yt-dlp)
# - [GitHub](https://github.com/yt-dlp/yt-dlp)

myappid = u'youtube.downloader.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
root = tk.Tk()
root.geometry("500x300")
root.resizable(True, True)
root.title('Youtube downloader')

# store youtube link and resulotion
youtube_link = tk.StringVar()
resolution = tk.IntVar()
# URL can alo be a list of URLs
#https://www.youtube.com/watch?v=lxRj81GiCqM
URL = ""

# Define which log messages should be printed (refers to logs of the yt-dlp logger)
LOG_STATES = {
    'debug': False,
    'info': False,
    'warning': True,
    'error': True
}

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Load the icon image
# root.iconphoto(False, tk.PhotoImage(file="youtube.png"))
# Load the icon image using PIL
icon = Image.open(resource_path("youtube.ico"))
icon = ImageTk.PhotoImage(icon)

# Set the taskbar icon
root.iconphoto(True, icon)
        

def format_selector(ctx):
    """ Select the best video and the best audio that won't result in an mkv.
    NOTE: This is just an example and does not handle all cases """

    # Reverse the formats list to start from the best quality
    formats = ctx.get('formats')[::-1]

    # acodec='none' means there is no audio
    best_video = next(
        f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none')

    print(f"\033[92m[INFO]:\033[00m Best video picked: {best_video['format_note']}")

    # find compatible audio extension
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}.get(best_video['ext'], None)

    if audio_ext is None:
        print('\033[91m[ERROR]:\033[00m No compatible audio extension found!')
        return

    # vcodec='none' means there is no video
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    # minimum required fields for a merged format
    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        # Must be + separated list of protocols
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }


def progress_hook(d):
    """ Custom hook to print download progress """
    # see help(yt_dlp.YoutubeDL) for all available fields and more information

    # helper function to convert bytes to human readable format
    def sizeof_fmt(num, suffix='B'):
        if not isinstance(num, (int, float)):
            return "unkown size"

        for unit in ['', 'Ki', 'Mi', 'Gi']:
            if abs(num) < 1024.0:
                return "%3.1f %s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f %s%s" % (num, 'Ti', suffix)

    # helper function to convert seconds to human readable format
    def seconds_to_hms(seconds):
        if not isinstance(seconds, (int, float)):
            return "--:--:-- " + str(seconds)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:.0f}:{m:02.0f}:{s:02.0f}"

    if d['status'] == 'finished':
        print(f"\n\033[92m[INFO]:\033[00m Done downloading! "
              f"({sizeof_fmt(d['total_bytes'])} in {seconds_to_hms(d['elapsed'])})\n")

    if d['status'] == 'downloading':
        # use carriage return to overwrite the previous line (dynmic output)
        # see: https://stackoverflow.com/questions/2122385/dynamic-terminal-printing-with-python
        print(
            "({percentage}) {amount} of {total} at {speed} | Time: {elapsed} - ETA: {eta}{offset}".format(
                percentage=d.get('_percent_str', '(\033[94m0.0%\033[00m)'),
                amount=sizeof_fmt(d.get('downloaded_bytes')),
                total=sizeof_fmt(d.get('total_bytes')),
                speed=sizeof_fmt(d.get('speed')) + '/s',
                elapsed=seconds_to_hms(d.get('elapsed')),
                eta=seconds_to_hms(d.get('eta')),
                offset=' ' * 20 # if previous line was longer than the current
            ), end='\r')

    if d['status'] == 'error':
        print(f"\033[91m[ERROR]:\033[00m {d['error']}\n")


class Logger:
    """ Custom logger to colorize and filter messages """

    def __init__(self, LOG_STATES):
        self.log_states = LOG_STATES

    def debug(self, msg):
        if msg.startswith('[debug] ') and self.log_states['debug']:
            print(f"\033[94m[DEBUG]:\033[00m {msg}")
        else:
            self.info(msg)

    def info(self, msg):
        if msg.startswith('[download] ') and msg.endswith(' has already been downloaded'):
            print("\033[92m[INFO]:\033[00m Video already downloaded")

        elif msg.startswith('[download] '):
            return

        elif self.log_states['info']:
            print(f"\033[92m[INFO]:\033[00m {msg}")

    def warning(self, msg):
        if self.log_states['warning']:
            print(f"\033[93m[WARN]:\033[00m {msg}")

    def error(self, msg):
        if self.log_states['error']:
            print(f"\033[91m[ERROR]:\033[00m {msg}")
            


def get_input():
       yt_link = youtube_link.get()
       if str(yt_link) == "":
            msg = 'Gib einen Link ein!'
            showinfo(
            title='Fehlermeldung',
            message=msg
            )

       else:
            msg = 'Die Anfrage wird gerade verarbeitet'
            showinfo(
            title='Status',
            message=msg
            )
            ydl_opts = {
                'format': format_selector,
                'progress_hooks': [progress_hook],
                'logger': Logger(LOG_STATES),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # get information about the video -> see https://pypi.org/project/yt-dlp/#extracting-information

            # import json
            # info = ydl.extract_info(URL, download=False)
            # print(json.dumps(ydl.sanitize_info(info), indent=4))
        
        
            # download the actual video, you can also pass a list of URLs
            # def for the Button

                ydl.download(yt_link)

# Youtube in frame
youtube_frame = ttk.Frame(root)
youtube_frame.pack(padx=10, pady=10, fill='x', expand=True)


# Youtube Link 
youtube_link_label = ttk.Label(youtube_frame, text="Youtube Link: ")
youtube_link_label.pack(fill='x', expand=True)

youtube_link_entry = ttk.Entry(youtube_frame, textvariable=youtube_link)
youtube_link_entry.pack(fill='x', expand=True)
youtube_link_entry.focus()


# submit button
submit_button = ttk.Button(youtube_frame, text="Submit", command=get_input)
submit_button.pack(fill='x', expand=True, pady=10)


root.mainloop()