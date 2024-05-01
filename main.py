from pytube import YouTube
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
import ctypes
import os
import sys

myappid = u'youtube.downloader.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# os path
cwd = os.path.realpath(os.path.dirname(__file__))

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# root window
root = tk.Tk()

# Load the icon image
# root.iconphoto(False, tk.PhotoImage(file="youtube.png"))
# Load the icon image using PIL
icon = Image.open(resource_path("youtube.ico"))
icon = ImageTk.PhotoImage(icon)

# Set the taskbar icon
root.iconphoto(True, icon)


root.geometry("500x300")
root.resizable(True, True)
root.title('Youtube downloader')

# store youtube link and resulotion
youtube_link = tk.StringVar()
resolution = tk.IntVar()

# def for the Button
def get_input():
    Boolean = True
    while Boolean == True:
       yt_link = youtube_link.get()
       res_usr = resolution.get()
       if str(yt_link) == "":
            msg = 'Gib einen Link ein!'
            showinfo(
            title='Fehlermeldung',
            message=msg
            )
            Boolean = False
       else:
        try:
           yt = YouTube(str(yt_link))
           yt.streams.get_by_resolution(res_usr).download()
           msg = f'Das Video {yt.title} wurde erfolgreich gedownloadet'
           showinfo(
           title='Info',
           message=msg
           )
           yt_link = ""
           res_usr = 0
           Boolean = False


        except Exception:
            msg = 'Der Download ist gescheitert'
            showinfo(
            title='Fehlermeldung',
            message=msg
            )
            Boolean = False


# Youtube in frame
youtube_frame = ttk.Frame(root)
youtube_frame.pack(padx=10, pady=10, fill='x', expand=True)


# Youtube Link 
youtube_link_label = ttk.Label(youtube_frame, text="Youtube Link: ")
youtube_link_label.pack(fill='x', expand=True)

youtube_link_entry = ttk.Entry(youtube_frame, textvariable=youtube_link)
youtube_link_entry.pack(fill='x', expand=True)
youtube_link_entry.focus()

# Resolution
resolution_label = ttk.Label(youtube_frame, text="Auflösung: ")
resolution_label.pack(fill='x', expand=True)

resolution_entry = ttk.Entry(youtube_frame, textvariable=resolution)
resolution_entry.pack(fill='x', expand=True)

# submit button
submit_button = ttk.Button(youtube_frame, text="Submit", command=get_input)
submit_button.pack(fill='x', expand=True, pady=10)


root.mainloop()