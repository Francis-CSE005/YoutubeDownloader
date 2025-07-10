🎬 YouTube Downloader (GUI)

A sleek, beginner-friendly desktop app to download YouTube videos or MP3s using a stylish Python GUI built with customtkinter, powered by yt-dlp and ffmpeg.


🚀 Features
🎨 Modern GUI using customtkinter

🔗 Paste any valid YouTube URL

🎧 Download video (MP4) or audio (MP3)

📁 Select your own download folder

✅ Shows status updates ("Download Complete", "Cancelled", "Error")

❌ Cancel button to stop download mid-way

🖼️ App logo added

🌐 Converts downloaded audio to MP3 using ffmpeg

🛠 Requirements
Make sure the following are installed:

Python 3.10+

yt-dlp

ffmpeg (added to system PATH)

Python packages:
pip install customtkinter yt-dlp pillow

💻 How to Run
python Main.py

📦 Convert to .exe (Optional)
Use PyInstaller to create a standalone .exe:

pyinstaller --noconsole --onefile --add-data "logo.png;." Main.py


🧠 Learning Purpose
This project was built to learn:

GUI app development with Python

Handling subprocesses and threads

Using yt-dlp and ffmpeg

Making and publishing GitHub projects

Connecting with the dev community (LinkedIn-friendly 💼)
