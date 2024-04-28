import ffmpeg, os
from pytube import YouTube

video_url = input("Gege: ")

# Initialize YouTube object
yt = YouTube(video_url)

# Get the highest resolution progressive video stream
video_stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()

def clean_filename(filename):
    replacements = {
        " ": "_",
        "ö": "o",
        "ü": "u",
        "ä": "a",
        "ß": "ss",
        "!": "."
    }
    for old, new in replacements.items():
        filename = filename.replace(old, new)
    return filename

# Download the video
video_name = clean_filename(f"{yt.title}_video.mp4")
video_stream.download(filename=video_name)

# Get the highest quality audio stream
audio_stream = yt.streams.get_audio_only()

# Download the audio
audio_name = clean_filename(f"{yt.title}_audio.mp3")
audio_stream.download(filename=audio_name)

# https://www.youtube.com/watch?v=lxRj81GiCqM
cwd = os.path.realpath(os.path.dirname(__file__))
video_fname = f'{cwd}\\{video_name}'
audio_fname = f'{cwd}\\{audio_name}'
print(f'{video_fname=}, {audio_fname=}')

input_video = ffmpeg.input(video_fname)
input_audio = ffmpeg.input(audio_fname)


ffmpeg.concat(input_video, input_audio, v=1, a=1).output(cwd + '/Videos').run()