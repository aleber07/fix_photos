import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import time

if len(sys.argv) < 2:
    print("Usage: python sistema_foto.py FOLDER_PATH")
    sys.exit(1)

cartella = " ".join(sys.argv[1:]).strip('"')

if not os.path.exists(cartella):
    print("Folder not found.")
    sys.exit(1)
prefisso = "DSC_"

def data_file(path):
    return datetime.fromtimestamp(os.path.getmtime(path))

def data_scatto(path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif:
            return data_file(path)
        for tag, val in exif.items():
            if TAGS.get(tag) == "DateTimeOriginal":
                return datetime.strptime(val, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return data_file(path)

file_media = []

for nome in os.listdir(cartella):
    if nome.lower().endswith((".jpg", ".jpeg", ".mov", ".avi", ".nef", ".heic", ".heif", ".mp4")):
        path = os.path.join(cartella, nome)
        data = data_scatto(path)
        estensione = os.path.splitext(nome)[1]  # leaves original extention
        file_media.append((path, data, estensione))

# Sort photos by date
file_media.sort(key=lambda x: x[1])

# --- STEP 1: temporal names ---
temp_files = []
for i, (path, _, estensione) in enumerate(file_media, start=1):
    temp_name = f"__temp__{i:04d}{estensione}"
    temp_path = os.path.join(cartella, temp_name)
    os.rename(path, temp_path)
    temp_files.append((temp_path, estensione))

# --- STEP 2: final names ---
print("Starting renaming...")
for i, (temp_path, estensione) in enumerate(temp_files, start=1):
    final_name = f"{prefisso}{i:04d}{estensione}"
    final_path = os.path.join(cartella, final_name)
    os.rename(temp_path, final_path)
    # print mapping 
    # print(f"{os.path.basename(temp_path)} → {final_name}")

time.sleep(1)
print(f"\nRenamed {len(temp_files)} files.")