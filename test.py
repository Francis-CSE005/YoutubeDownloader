import os
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog

# App setup
app = ctk.CTk()
app.title("YouTube Downloader")
app.geometry("550x400")

# Global variables
download_process = None

# Folder selection variable
folder_path = ctk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))

# UI Elements
url_label = ctk.CTkLabel(app, text="YouTube URL:")
url_label.pack(pady=5)

url_entry = ctk.CTkEntry(app, width=450)
url_entry.pack(pady=5)

format_label = ctk.CTkLabel(app, text="Choose Format:")
format_label.pack(pady=5)

format_opt = ctk.StringVar(value="MP4")
format_menu = ctk.CTkOptionMenu(app, variable=format_opt, values=["MP4", "MP3"])
format_menu.pack(pady=5)

folder_button = ctk.CTkButton(app, text="Select Download Folder", command=lambda: folder_path.set(filedialog.askdirectory()))
folder_button.pack(pady=5)

folder_display = ctk.CTkLabel(app, textvariable=folder_path, text_color="gray")
folder_display.pack(pady=2)

status_label = ctk.CTkLabel(app, text="", text_color="gray")
status_label.pack(pady=10)

progress_bar = ctk.CTkProgressBar(app, width=450)
progress_bar.set(0)
progress_bar.pack_forget()  # Hide initially

def threaded_download():
    global download_process
    url = url_entry.get()
    folder = folder_path.get()
    format_choice = format_opt.get()

    if not url:
        status_label.configure(text="Please enter a valid YouTube URL ❗", text_color="red")
        return

    progress_bar.pack(pady=5)  # Show progress bar when download starts
    status_label.configure(text="Downloading...", text_color="orange")
    progress_bar.set(0.2)

    filename_template = os.path.join(folder, '%(title)s.%(ext)s')

    if format_choice == "MP3":
        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "192K",
            "--no-mtime",
            "-o", filename_template,
            url
        ]
    else:
        cmd = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio",
            "--merge-output-format", "mp4",
            "--no-mtime",
            "-o", filename_template,
            url
        ]

    try:
        download_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = download_process.communicate()

        if download_process.returncode == 0:
            progress_bar.set(1.0)
            status_label.configure(text="Download Complete ✅", text_color="green")
        else:
            status_label.configure(text="Error ❌", text_color="red")
            print(stderr.decode())
    except Exception as e:
        status_label.configure(text=f"Error ❌: {e}", text_color="red")
        progress_bar.set(0)

def download_video():
    thread = threading.Thread(target=threaded_download)
    thread.start()

def cancel_download():
    global download_process
    if download_process and download_process.poll() is None:
        download_process.terminate()
        status_label.configure(text="Download Cancelled ❌", text_color="red")
        progress_bar.set(0)

# Buttons
download_button = ctk.CTkButton(app, text="Download", command=download_video)
download_button.pack(pady=10)

cancel_button = ctk.CTkButton(app, text="Cancel", command=cancel_download)
cancel_button.pack(pady=5)

# Start the app
app.mainloop()