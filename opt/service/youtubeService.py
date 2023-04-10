import sys
sys.path.append('../utils')
sys.path.append('../model')
import youtubeModel

def download_mp3(url):
    youtubeModel.download_mp3(url)
    
def download_mp4(url):
    youtubeModel.download_mp4(url)