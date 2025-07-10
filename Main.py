import os #For Managing files
import subprocess #For Cancel function
import threading #For separating the downloading process
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

# App setup
app = ctk.CTk()
app.title("YouTube Downloader")
app.geometry("600x450")
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


# Global variables
download_process = None

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

folder_button = ctk.CTkButton(main_frame, text="Select Download Folder", font=("Arial", 13), command=lambda: folder_path.set(filedialog.askdirectory()))
folder_button.pack(pady=10)

folder_display = ctk.CTkLabel(main_frame, textvariable=folder_path, text_color="gray", font=("Arial", 12))
folder_display.pack(pady=2)

status_label = ctk.CTkLabel(main_frame, text="", text_color="red", font=("Arial", 13))
status_label.pack(pady=10)

def threaded_download():
    global download_process
    url = url_entry.get() #URL Input
    folder = folder_path.get() #Downloaded File Path
    format_choice = format_opt.get() #Selecting the format

    if not url: #if URL is not Entered
        status_label.configure(text="Please enter a valid YouTube URL ❗", text_color="red")
        return

    status_label.configure(text="Downloading...", text_color="orange")

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
            status_label.configure(text="Download Complete ✅", text_color="green")
        else:
            status_label.configure(text="Error ❌", text_color="red")
            print(stderr.decode())
    except Exception as e:
        status_label.configure(text=f"Error ❌: {e}", text_color="red")

def download_video():
    thread = threading.Thread(target=threaded_download)
    thread.start()

def cancel_download():
    global download_process
    if download_process and download_process.poll() is None:
        download_process.terminate()
        status_label.configure(text="Download Cancelled ❌", text_color="red")

# Buttons
download_button = ctk.CTkButton(main_frame, text="Download", font=("Arial", 13), command=download_video)
download_button.pack(pady=10)

cancel_button = ctk.CTkButton(main_frame, text="Cancel", font=("Arial", 13), command=cancel_download)
cancel_button.pack(pady=5)

# Start the app and keeps it running until closed by the user
app.mainloop()


