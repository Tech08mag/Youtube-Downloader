import ffmpeg, os, shutil,sys
from pathlib import Path
from tkinter import filedialog

def convert_to_mp3(video_title: str, chars: str):
    try:
        (
	    ffmpeg.input(f'{video_title} [{chars}].webm')
	    .output(f"{video_title}.mp4")
	    .run()
        )
    except Exception:
        os.rename(f"{Path.cwd()}\\{video_title} [{chars}].mp4", f"{Path.cwd()}\\{video_title}.mp4")
        video_title_path = f"{Path.cwd()}\\{video_title}.mp3"

    if os.path.exists(Path.cwd()) and os.path.isfile(f"{video_title}.mp3") == True:
                    save_path = filedialog.asksaveasfilename(title="Save", filetypes=[("Mp3 Files", ".mp3")], defaultextension=".mp3",
                        initialdir=Path(sys.executable), initialfile=video_title)
                    shutil.move(video_title_path, save_path)


def convert_to_mp4(video_title: str, chars: str):
    try:
        (
	    ffmpeg.input(f'{video_title} [{chars}].webm')
	    .output(f"{video_title}.mp4")
	    .run()
        )
    except Exception:
            os.rename(f"{Path.cwd()}\\{video_title} [{chars}].mp4", f"{Path.cwd()}\\{video_title}.mp4")
            video_title_path = f"{Path.cwd()}\\{video_title}.mp4"
    if os.path.exists(Path.cwd()) and os.path.isfile(f"{video_title}.mp4") == True:
                    save_path = filedialog.asksaveasfilename(title="Save", filetypes=[("Mp3 Files", ".mp4")], defaultextension=".mp3",
                        initialdir=Path(sys.executable), initialfile=video_title)
                    shutil.move(video_title_path, save_path)