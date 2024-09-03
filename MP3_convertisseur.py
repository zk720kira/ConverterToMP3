# ---Imports---
import yt_dlp
import os
import csv
from datetime import datetime

# Function to convert a YouTube link to a mp3 file
def convert_to_mp3(url):
    # ---Create folder to put the MP3---
    today = datetime.today().strftime("%Y-%m-%d")  # Get the date of today
    folder_path = os.path.join(os.path.expanduser("~"), "Downloads", f"Musique {today}")  # Build the folder path
    
    # If not exists create the folder
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    ydl_opts = {
        'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),  # Path to the Download folder
        'format': 'bestaudio/best',  # Download the best file
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'EmbedThumbnail'  # Add miniature
        }],
        'config_location': 'yt-dlp.conf',  # Path to the conf file
        'ffmpeg_location': 'C:\\ffmpeg\\ffmpeg-2024-08-28-git-b730defd52-essentials_build\\bin\\ffmpeg.exe',
        'writethumbnail': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Function to read a csv that contain YouTube link, foreach link download it to MP3
def read_csv(csv_file):
    data = []
    download_count = 0 # Counter for the number of downloads
    with open(csv_file, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['link_youtube']
            convert_to_mp3(url)
            data.append(row)
            download_count += 1 # Increment the download counter
            
            # Make a break to each 10 downloads
            if download_count == 10:
                print("Pause de 5 secondes...")
                time.sleep(5) # Sleep the program 5 secondes
                download_count = 0
    return data

# Get the YouTube link and call the converter function
if __name__ == "__main__":
    usage = input("Voulez-vous utiliser un lien (lien) ou un fichier csv qui contient plusieurs lien (csv) ? lien/csv : ")
    if usage == 'lien':
        url = input("Entrez le lien YouTube: ")
        convert_to_mp3(url)
    elif usage == 'csv':
        csv_file = input("Entrez le chemin du fichier csv: ")
        read_csv(csv_file)
    print("Conversion terminée !")