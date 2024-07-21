from pytube import YouTube

def download_video(url,path):
    yt = YouTube(url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(path)
    print(f"Video downloaded to {path}")


url = "https://www.youtube.com/watch?v=BPpDrWeUpzY&list=RDBPpDrWeUpzY&index=1"
path = "C:/Users/zheer/Desktop/"

download_video(url, path)