from yt_dlp import YoutubeDL
from moviepy.editor import *
import os
import shutil
import yaml

yaml_path = '/root/opt/option/output.yaml'
with open(yaml_path) as file:
    yml = yaml.safe_load(file)
    
mp3_output = yml['youtube']['mp3']
mp4_output = yml['youtube']['mp4']

def download_mp3(url):
    ydl_video_opts = {
        'outtmpl': mp3_output,
        'format': 'bestaudio'
    }
    with YoutubeDL(ydl_video_opts) as ydl:
        result = ydl.download([url])
        
def download_mp4(url):
    #映像をダウンロード  
    ydl_video_opts = {
        'outtmpl': mp4_output,
        'format': 'bestvideo/best'
    }
    with YoutubeDL(ydl_video_opts) as ydl:
        result = ydl.download([url])
        
    #メタデータ取得
    with YoutubeDL() as ydl:
        res = ydl.extract_info(url, download=False)

    #動画取得
    ydl_video_opts = {
        'outtmpl': 'video.mp4',
        'format': 'bestvideo/best'
    }
    with YoutubeDL(ydl_video_opts) as ydl:
        ydl.download([url])

    #音声取得
    ydl_audio_opts = {
        'outtmpl': 'audio.mp3',
        'format': 'bestaudio/best'
    }
    with YoutubeDL(ydl_audio_opts) as ydl:
        ydl.download([url])

    #動画・音声結合＆出力
    videoclip = VideoFileClip("video.mp4")
    audioclip = AudioFileClip("audio.mp3")
    output_video = videoclip.set_audio(audioclip)
    output_video.write_videofile('result.mp4')
    output = os.path.join(os.path.dirname(mp4_output),res['title']+'.mp4')
    shutil.copyfile('result.mp4',output)

    #一時ファイルの削除
    os.remove('video.mp4')
    os.remove('audio.mp3')
    os.remove('result.mp4')