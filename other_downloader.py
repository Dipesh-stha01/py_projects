import tkinter as tk
from tkinter import messagebox
import yt_dlp
import requests
from bs4 import BeautifulSoup

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("500x250")

        # URL Entry
        self.url_label = tk.Label(root, text="Video URL:")
        self.url_label.pack(pady=10)
        self.url_entry = tk.Entry(root, width=60)
        self.url_entry.pack(pady=5)

        # Download Button
        self.download_button = tk.Button(root, text="Download Video", command=self.download_video)
        self.download_button.pack(pady=20)

    def download_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a video URL.")
            return

        try:
            # Download video using yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_title = info_dict.get('title', 'video')
                messagebox.showinfo("Success", f"Video '{video_title}' downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
