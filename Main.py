import os
import threading
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from yt_dlp import YoutubeDL

# App setup
app = ctk.CTk()
app.title("YouTube Downloader")
app.geometry("600x450")
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# Folder selection variable
folder_path = ctk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))

# Main frame
main_frame = ctk.CTkFrame(app)
main_frame.pack(pady=30, padx=30, fill="both", expand=True)

# Logo
logo_image = ctk.CTkImage(light_image=Image.open("logo.png"), size=(100, 100))
logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
logo_label.pack(pady=(10, 5))

# UI Elements
url_label = ctk.CTkLabel(main_frame, text="YouTube URL:", font=("Arial", 14))
url_label.pack(pady=(10, 5))

url_entry = ctk.CTkEntry(main_frame, width=500, font=("Arial", 13))
url_entry.pack(pady=5)

format_label = ctk.CTkLabel(main_frame, text="Choose Format:", font=("Arial", 14))
format_label.pack(pady=(15, 5))

format_opt = ctk.StringVar(value="MP4")
format_menu = ctk.CTkOptionMenu(main_frame, variable=format_opt, values=["MP4", "MP3"], font=("Arial", 13), width=150)
format_menu.pack(pady=5)

folder_button = ctk.CTkButton(main_frame, text="Select Download Folder", font=("Arial", 13),
                               command=lambda: folder_path.set(filedialog.askdirectory()))
folder_button.pack(pady=10)

folder_display = ctk.CTkLabel(main_frame, textvariable=folder_path, text_color="gray", font=("Arial", 12))
folder_display.pack(pady=2)

status_label = ctk.CTkLabel(main_frame, text="", text_color="red", font=("Arial", 13))
status_label.pack(pady=10)

def threaded_download():
    url = url_entry.get()
    folder = folder_path.get()
    format_choice = format_opt.get()

    if not url:
        status_label.configure(text="Please enter a valid YouTube URL ❗", text_color="red")
        return

    status_label.configure(text="Downloading...", text_color="orange")

    filename_template = os.path.join(folder, '%(title)s.%(ext)s')

    ydl_opts = {
        'outtmpl': filename_template,
        'no-mtime': True,
        'format': 'bestaudio/best' if format_choice == "MP3" else 'bestvideo+bestaudio',
        'merge_output_format': 'mp4',
    }

    if format_choice == "MP3":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_label.configure(text="Download Complete ✅", text_color="green")
    except Exception as e:
        status_label.configure(text=f"Error ❌: {e}", text_color="red")

def download_video():
    thread = threading.Thread(target=threaded_download)
    thread.start()

# Buttons
download_button = ctk.CTkButton(main_frame, text="Download", font=("Arial", 13), command=download_video)
download_button.pack(pady=10)

# Start the app
app.mainloop()



