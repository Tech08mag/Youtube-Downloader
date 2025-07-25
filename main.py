# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "customtkinter>=5.2.2",
#     "ffmpeg-python>=0.2.0",
#     "tk>=0.1.0",
#     "yt-dlp>=2025.7.21",
# ]
# ///
import customtkinter
import yt_dlp
from messages import Error, Succes, Finished
import filefix
import formatselector
import logfuc
import convert

LOG_STATES = {
    'debug': False,
    'info': False,
    'warning': True,
    'error': True
}

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

        self.playlist = customtkinter.StringVar(value="off")
        self.playlist_check = customtkinter.CTkCheckBox(self.main_frame, text="Download the Playlist",
                                                        onvalue="on", offvalue="off")
        self.playlist_check.pack(padx=10, pady=10, fill='x')

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
                self.toplevel_window = Succes(self)
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
            'ignoreerrors': True
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
            if self.playlist.get() == "on" and self.check_var.get() == "on":
                self.open_Sucess()
                ydl_opts = {
                    'format': formatselector.format_selector_mp3,
                    'progress_hooks': [logfuc.progress_hook],
                    'logger': logfuc.Logger(LOG_STATES),
                    'ignoreerrors': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(URL, download=True)
                    video_title = info_dict.get('title', None)
                    chars = filefix.get_ending(link=URL)

            elif self.playlist.get() == "on":
                self.open_Sucess()
                ydl_opts = {
                    'format': formatselector.format_selector_mp4,
                    'progress_hooks': [logfuc.progress_hook],
                    'logger': logfuc.Logger(LOG_STATES),
                    'ignoreerrors': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(URL, download=True)
                    video_title = info_dict.get('title', None)
                    chars = filefix.get_ending(link=URL)

            elif self.check_var.get() == "on":
                self.open_Sucess()
                ydl_opts = {
                    'format': formatselector.format_selector_mp3,
                    'progress_hooks': [logfuc.progress_hook],
                    'logger': logfuc.Logger(LOG_STATES),
                    'ignoreerrors': True,
                    'noplaylist': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(URL, download=True)

                    video_title = info_dict.get('title', None)
                    chars = filefix.get_ending(link=URL)


                    convert.convert_to_mp3(video_title=video_title, chars=chars)

            elif self.check_var.get() == "on":
                self.open_Sucess()
                ydl_opts = {
                    'format': formatselector.format_selector_mp3,
                    'progress_hooks': [logfuc.progress_hook],
                    'logger': logfuc.Logger(LOG_STATES),
                    'ignoreerrors': True,
                    'noplaylist': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(URL, download=True)
                    video_title = info_dict.get('title', None)
                    print(video_title)
                    chars = filefix.get_ending(link=URL)

                    convert.convert_to_mp3(video_title=video_title, chars=chars)
            else:
                self.open_Sucess()
                ydl_opts = {
                    'format': formatselector.format_selector_mp4,
                    'progress_hooks': [logfuc.progress_hook],
                    'logger': logfuc.Logger(LOG_STATES),
                    'ignoreerrors': True,
                    'noplaylist': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(URL, download=True)
                    video_title = info_dict.get('title', None)
                    chars = filefix.get_ending(link=URL)
                self.open_Finished()

if __name__ == '__main__':
    app = App()
    app.mainloop()
