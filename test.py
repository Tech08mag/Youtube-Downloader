from tkinter import filedialog
import yt_dlp
from pathlib import Path
from cleanname import clean_filename
import os, sys, shutil

LOG_STATES = {
    'debug': False,
    'info': False,
    'warning': True,
    'error': True
}

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
    audio_ext = {'mp4': 'm4a'}.get(best_video['ext'], None)

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
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}',
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

ydl_opts = {
                'format': format_selector,
                'progress_hooks': [progress_hook],
                'logger': Logger(LOG_STATES),
                'restrictfilenames': True
            }

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info("https://www.youtube.com/watch?v=RCk4b9X8LYI", download=True)
    
    video_url = info_dict.get("url", None)
    video_id = info_dict.get("id", None)
    video_title = info_dict.get('title', None)

    print(os.path.exists(f"{Path.cwd()}"))
    print(os.path.isfile(f"{video_title}"))
    print(f"{video_title}")

    if os.path.exists(f"{Path.cwd()}") and os.path.isfile(f"{video_title}"):
        save_path = filedialog.asksaveasfilename(title="Save", filetypes=[("Mp4 Files", ".mp4")], defaultextension=".mp4",
            initialdir=Path(sys.executable), initialfile=video_title)
        shutil.move(video_title, save_path)
