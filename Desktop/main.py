import customtkinter, yt_dlp
from messages import Error, Success, Finished
from tkinter import filedialog
from pathlib import Path
import os, sys, shutil, filefix as filefix, ffmpeg

LOG_STATES = {
    'debug': False,
    'info': False,
    'warning': True,
    'error': True
}

def format_selector_mp4(ctx):
    """ Select the best video and the best audio that won't result in an mkv.
    NOTE: This is just an example and does not handle all cases """

    # formats are already sorted worst to best
    formats = ctx.get('formats')[::-1]

    # acodec='none' means there is no audio
    best_video = next(f for f in formats
                      if f['vcodec'] != 'none' and f['acodec'] == 'none')

    # find compatible audio extension
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    # vcodec='none' means there is no video
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    # These are the minimum required fields for a merged format
    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        # Must be + separated list of protocols
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }

def format_selector_mp3(ctx):
    """ Select the best audio that won't result in an mkv.
    NOTE: This is just an example and does not handle all cases """

    # formats are already sorted worst to best
    formats = ctx.get('formats')[::-1]

    # acodec='none' means there is no audio
    best_video = next(f for f in formats
                      if f['vcodec'] != 'none' and f['acodec'] == 'none')

    # find compatible audio extension
    audio_ext = {'mp3': 'm3a', 'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    # vcodec='none' means there is no video
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    # These are the minimum required fields for a merged format
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

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Youtube downloader")
        self.geometry("500x400")
        self.resizable(True, True)
        self.toplevel_window = None
        self.value_storage = ["You need to input a link"]

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(padx=10, pady=10, fill='x', expand=True)

        self.entry = customtkinter.CTkEntry(self.main_frame, placeholder_text="Youtube link", fg_color="transparent")
        self.entry.pack(padx=10, pady=10, fill='x', expand=True)
        self.entry.bind(sequence="<Return>", command=lambda _: self.load_resolutions())

        self.check_var = customtkinter.StringVar(value="off")
        self.checkbox = customtkinter.CTkCheckBox(self.main_frame, text="Only Audio",
                                     variable=self.check_var, onvalue="on", offvalue="off")
        self.checkbox.pack(padx=10, pady=10, fill='x')

        self.path_var = customtkinter.StringVar(value="on")
        self.path_check = customtkinter.CTkCheckBox(self.main_frame, text="Download to Path",
                                 variable=self.path_var, onvalue="on", offvalue="off")
        self.path_check.pack(padx=10, pady=10, fill='x')

        self.optionmenu_var = customtkinter.StringVar(value=self.value_storage[0])
        self.optionmenu = customtkinter.CTkOptionMenu(self.main_frame, values=self.value_storage, variable=self.optionmenu_var)
        self.optionmenu.pack(padx=10, pady=10, fill='x', expand=True)

        self.button = customtkinter.CTkButton(self.main_frame, text="download", command=self.button_callback)
        self.button.pack(padx=10, pady=10, fill='x', expand=True)

    def open_Error(self):
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = Error(self) 
            else:
                self.toplevel_window.focus()

    def open_Sucess(self):
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = Success(self)
            else:
                self.toplevel_window.focus()
    
    def open_Finished(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Finished(self) 
        else:
            self.toplevel_window.focus()

    def load_resolutions(self):
        URL = self.entry.get()
        if URL == "":
            self.open_Error()

        yd_opts = {
            # 'listformats': True,
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ignoreerrors': True,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(yd_opts) as ydl:
            info = ydl.extract_info(URL, download=False)
            formats = info.get('formats', [])
            # filter only video formats and get the resolutions
            video_formats = [f for f in formats if f.get('vcodec') != 'none']
            resolutions = set([f.get('resolution') for f in video_formats])
            # update the option menu
            self.optionmenu_var.set(next(iter(resolutions)) if resolutions else "No video formats found")
            self.optionmenu.configure(values=resolutions)

    def button_callback(self):
        URL = self.entry.get()
        if str(URL) == "":
            self.open_Error()
        else:
            if self.check_var.get() == "on" and self.path_var.get() == "on":
                self.open_Sucess()
                data = open("settings.txt", "r")
                path = data.read()
                ydl_opts = {
                    'format': format_selector_mp3,
                    'progress_hooks': [progress_hook],
                    'logger': Logger(LOG_STATES),
                     'ignoreerrors': True,
                      'noplaylist': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(URL, download=True)

                    video_url = info_dict.get("url", None)
                    video_id = info_dict.get("id", None)
                    video_title = info_dict.get('title', None)
                    chars = filefix.get_ending(link=URL)
                    video_title_path = f"{Path.cwd()}\\{video_title}.mp3"

                    try:
                        (
	                    ffmpeg.input(f"{video_title} [{chars}].mp4")
	                    .output(f"{video_title}.mp3")
	                    .run()
                        )

                    except Exception:
                        (
	                    ffmpeg.input(f"{video_title} [{chars}].webm")
	                    .output(f"{video_title}.mp3")
	                    .run()
                        )

                    if os.path.exists(Path.cwd()) and os.path.isfile(f"{video_title}.mp3") == True:
                        shutil.move(video_title_path, path)
                    data.close()
            
            elif self.path_var.get() == "on":
                self.open_Sucess()
                data = open("settings.txt", "r")
                path = data.read()
                ydl_opts = {
                    'format': format_selector_mp4,
                    'progress_hooks': [progress_hook],
                    'logger': Logger(LOG_STATES),
                    'ignoreerrors': True,
                    'noplaylist': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(URL, download=True)

                    video_url = info_dict.get("url", None)
                    video_id = info_dict.get("id", None)
                    video_title = info_dict.get('title', None)
                    chars = filefix.get_ending(link=URL)

                    try:
                        (
	                    ffmpeg.input(f"{video_title} [{chars}].webm")
	                    .output(f"{video_title}.mp4")
	                    .run()
                        )
                    except Exception:
                            os.rename(f"{Path.cwd()}\\{video_title} [{chars}].mp4", f"{Path.cwd()}\\{video_title}.mp4")
                            video_title_path = f"{Path.cwd()}\\{video_title}.mp4"

                    if os.path.exists(Path.cwd()) and os.path.isfile(f"{video_title}.mp4") == True:
                        shutil.move(video_title_path, path)
                data.close()
                self.open_Finished()

            elif self.check_var.get() == "on":
                self.open_Sucess()
                ydl_opts = {
                    'format': format_selector_mp3,
                    'progress_hooks': [progress_hook],
                    'logger': Logger(LOG_STATES),
                    'ignoreerrors': True,
                    'noplaylist': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(URL, download=True)

                    video_url = info_dict.get("url", None)
                    video_id = info_dict.get("id", None)
                    video_title = info_dict.get('title', None)
                    print(video_title)
                    chars = filefix.get_ending(link=URL)
                    video_title_path = f"{Path.cwd()}\\{video_title}.mp3"

                    try:
                        (ffmpeg.input(f"{video_title} [{chars}].mp4")
                         .output(f"{video_title}.mp3")
                         .run())
                    except Exception:
                        (
	                    ffmpeg.input(f"{video_title} [{chars}].webm")
	                    .output(f"{video_title}.mp3")
	                    .run()
                        )
                if os.path.exists(Path.cwd()) and os.path.isfile(f"{video_title}.mp3") == True:
                    save_path = filedialog.asksaveasfilename(title="Save", filetypes=[("Mp3 Files", ".mp3")], defaultextension=".mp3",
                        initialdir=Path(sys.executable), initialfile=video_title)
                    shutil.move(video_title_path, save_path)
            else:
                self.open_Sucess()
                ydl_opts = {
                    'format': format_selector_mp4,
                    'progress_hooks': [progress_hook],
                    'logger': Logger(LOG_STATES),
                    'ignoreerrors': True,
                    'noplaylist': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(URL, download=True)

                    video_url = info_dict.get("url", None)
                    video_id = info_dict.get("id", None)
                    video_title = info_dict.get('title', None)
                    chars = filefix.get_ending(link=URL)

                    try:
                        (
	                    ffmpeg.input(f"{video_title} [{chars}].webm")
	                    .output(f"{video_title}.mp4")
	                    .run()
                        )
                    except Exception:
                            os.rename(f"{Path.cwd()}\\{video_title} [{chars}].mp4", f"{Path.cwd()}\\{video_title}.mp4")
                            video_title_path = f"{Path.cwd()}\\{video_title}.mp4"

                    if os.path.exists(Path.cwd()) and os.path.isfile(f"{video_title}.mp4") == True:
                        save_path = filedialog.asksaveasfilename(title="Save", filetypes=[("Mp4 Files", ".mp4")], defaultextension=".mp4",
                            initialdir=Path(sys.executable), initialfile=video_title)
                        shutil.move(video_title_path, save_path)
                self.open_Finished()


if __name__ == '__main__':
    app = App()
    app.mainloop()