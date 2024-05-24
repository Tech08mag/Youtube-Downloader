
import yt_dlp
import ctypes
import customtkinter as ctk
import messages
import helper
# from resolutions import

# For information see also:
#
# - [General Doc](https://pypi.org/project/yt-dlp/)
# - [Code relevant doc](https://pypi.org/project/yt-dlp/#embedding-yt-dlp)
# - [GitHub](https://github.com/yt-dlp/yt-dlp)

myappid = u'youtube.downloader.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


# URL can alo be a list of URLs
#https://www.youtube.com/watch?v=lxRj81GiCqM
URL = ""
value_storage = ["You need to input a link"]
formats = ("640x360", "640x480", "1280x720", "1920x1080", "2560x1440", "2048x1080", "3840x2160", "7680x4320")


# Define which log messages should be printed (refers to logs of the yt-dlp logger)
LOG_STATES = {
    'debug': False,
    'info': False,
    'warning': True,
    'error': True
}

def format_selector_audio(ctx):
    """ Select the best video and the best audio that won't result in an mkv.
    NOTE: This is just an example and does not handle all cases """

    # Reverse the formats list to start from the best quality
    formats = ctx.get('formats')[::-1]

    # acodec='none' means there is no audio
    best_video = next(
        f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none')

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
        'format_id': f'{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_audio],
        # Must be + separated list of protocols
        'protocol': f'{best_audio["protocol"]}'
    }


def format_selector_video(ctx):
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

class Mainwindow(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")
        #customtkinter default settings
        self.resizable(True, True)
        self.title('Youtube downloader')
        self.iconbitmap(default=helper.resource_path() + "/youtube.ico")


        self.Messagebox_success = None
        self.Messagebox_fail = None
        self.onlyAudio = ctk.StringVar()
        self.Author = ctk.StringVar()
        self.best_res_var = ctk.StringVar()


        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=10, pady=10, fill='x', expand=True)
        
        # Youtube Link 
        self.youtube_link_label = ctk.CTkLabel(self.main_frame, text="Youtube Link: ")
        self.youtube_link_label.pack(padx=10, pady=10, fill='x', expand=True)
        
        youtube_link = ctk.StringVar()
        youtube_link.trace("w", lambda name, index, mode, sv=youtube_link: Mainwindow.callback(youtube_link))
        youtube_link_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Youtube Link", textvariable=youtube_link)
        youtube_link_entry.pack(padx=10, pady=10, fill='x', expand=True)


        self.checkbox = ctk.CTkCheckBox(self.main_frame, text="only Audio",
                                     variable=self.onlyAudio, onvalue="on", offvalue="off")
        self.checkbox.pack(padx=10, pady=10, fill='x', expand=True)

        self.checkbox = ctk.CTkCheckBox(self.main_frame, text="every Video from the auther",
                                     variable=self.Author, onvalue="on", offvalue="off")
        self.checkbox.pack(padx=10, pady=10, fill='x', expand=True)

        self.checkbox = ctk.CTkCheckBox(self.main_frame, text="highest resolution",
                                     variable=self.best_res_var, onvalue="on", offvalue="off")
        self.checkbox.pack(padx=10, pady=10, fill='x', expand=True)

        self.optionmenu_var = ctk.StringVar(value=value_storage[0])
        self.optionmenu = ctk.CTkOptionMenu(self.main_frame,values=value_storage,
                                         variable=self.optionmenu_var)
        self.optionmenu.pack(padx=10, pady=10, fill='x', expand=True)

        self.button = ctk.CTkButton(self.main_frame, text="downloaden", command=self.get_input(youtube_link))
        self.button.pack(padx=10, pady=10, fill='x', expand=True)

    def callback(youtube_link):
        print("Ausgelöst")
        # ylink = self.youtube_link.get()
        youtube_link = youtube_link.get()
        if youtube_link.startswith("https://www.youtube.com/watch?v="):
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_link, download=False)
                formats = info.get('formats')[::-1]
    
                try:
                    aviable_formats = next(f for f in formats if f['resolution'] == '')
                    value_storage.pop(0)
                    value_storage.append(aviable_formats)
                    print(aviable_formats)
    
                except Exception:
                    messages.fail_to_load_formats()
        else:
            messages.Error_Message()

    def get_input(self, youtube_link):
        yt_link = youtube_link.get()
        if yt_link.startswith("https://www.youtube.com/watch?v=") and self.onlyAudio.get() == "on":

            ydl_opts = {
                'format': format_selector_audio,
                'progress_hooks': [progress_hook],
                'logger': Logger(LOG_STATES)
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # get information about the video -> see https://pypi.org/project/yt-dlp/#extracting-information
                # import json
                # info = ydl.extract_info(URL, download=False)
                # print(json.dumps(ydl.sanitize_info(info), indent=4))
                # download the actual video, you can also pass a list of URLs
                # def for the Button
                ydl.download(yt_link)
                messages.Finish_Message()

        elif yt_link.startswith("https://www.youtube.com/watch?v=") and self.best_res_var.get() == "on":
            ydl_opts = {
                'format': format_selector_video,
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
                messages.Finish_Message()
        else:
            messages.Error_Message()


if __name__ == '__main__':
    app = Mainwindow()
    app.mainloop()