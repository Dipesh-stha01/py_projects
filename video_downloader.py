import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import yt_dlp
import os
import threading

def download_video(url, output_path='.', progress_callback=None):
    def hook(d):
        if d['status'] == 'finished':
            print(f"\nDone downloading video: {d['filename']}")
        elif d['status'] == 'downloading':
            if progress_callback:
                percent = d.get('percent', 0)
                progress_callback(percent)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',  # Merge audio and video into mp4 format
        'progress_hooks': [hook],
        'noplaylist': True,
    }

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def on_download():
    url = url_entry.get()
    output_path = output_entry.get()

    if not url.startswith('https://www.youtube.com/watch'):
        messagebox.showerror("Error", "Invalid URL. Please enter a valid YouTube video URL.")
        return

    if not output_path:
        output_path = '.'

    # Start download in a new thread to keep the GUI responsive
    def download_thread():
        try:
            download_video(url, output_path, progress_callback=update_progress)
            progress_bar['value'] = 100
            messagebox.showinfo("Success", "Download complete!")
            # Clear fields after successful download
            url_entry.delete(0, tk.END)
            output_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    progress_bar['value'] = 0
    threading.Thread(target=download_thread).start()

def update_progress(percent):
    progress_bar['value'] = percent
    app.update_idletasks()

def browse_directory():
    folder_selected = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_selected)

# Create the main application window
app = tk.Tk()
app.title("YouTube Video Downloader")

# Create and place the widgets
tk.Label(app, text="YouTube Video URL:").pack(padx=10, pady=5)
url_entry = tk.Entry(app, width=50)
url_entry.pack(padx=10, pady=5)

tk.Label(app, text="Output Directory:").pack(padx=10, pady=5)
output_frame = tk.Frame(app)
output_frame.pack(padx=10, pady=5)
output_entry = tk.Entry(output_frame, width=40)
output_entry.pack(side=tk.LEFT)
browse_button = tk.Button(output_frame, text="Browse", command=browse_directory)
browse_button.pack(side=tk.RIGHT)

tk.Label(app, text="Download Progress:").pack(padx=10, pady=5)
progress_bar = ttk.Progressbar(app, orient='horizontal', length=400, mode='determinate')
progress_bar.pack(padx=10, pady=10)

download_button = tk.Button(app, text="Download", command=on_download)
download_button.pack(padx=10, pady=20)

# Run the application
app.mainloop()
