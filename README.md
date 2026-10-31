# fix_photos.py

Renames photos and videos in a folder to a sequential format (`DSC_0001.jpg`, `DSC_0002.mov`, ...), ordered by the date each file was taken.

---

## Table of contents

- [How it works](#how-it-works)
- [Supported formats](#supported-formats)
- [Requirements](#requirements)
- [Usage](#usage)
- [Important](#important)
- [Known limitations](#known-limitations)
- [License](#license)

---

## How it works

1. Scans the folder for supported media files.
2. Reads the capture date from the EXIF `DateTimeOriginal` tag. If the tag is missing or unreadable, it uses the file's last-modified date.
3. Sorts all files by that date.
4. Renames them in two passes: first to temporary names, then to the final names. This avoids collisions during the rename.

The original file extension is preserved (`.JPG` stays `.JPG`, `.mov` stays `.mov`).

---

## Supported formats

| Type  | Extensions                                     |
| ----- | ---------------------------------------------- |
| Photo | `.jpg`, `.jpeg`, `.heic`, `.nef`               |
| Video | `.mov`, `.avi`, `.mp4`                         |

Matching is case-insensitive.

---

## Requirements

- Python 3.6 or newer
- [Pillow](https://pypi.org/project/Pillow/)

```bash
pip install pillow
```

---

## Usage

```bash
python fix_photos.py "/path/to/folder"
```

Quotes are recommended for paths containing spaces. Unquoted paths also work, since all arguments after the script name are joined.

**Windows example:**

```bash
python fix_photos.py "C:\Users\me\Pictures\Trip 2025"
```

**Output:**
- Started renaming...
- Renamed 128 files


---

## Important

> **Warning:** the script renames files in place and cannot be undone. Back up the folder before running it.

Only file names change. Contents and EXIF metadata are not modified.

---

## Known limitations

- EXIF date reading uses `Image._getexif()`, which works for JPEG files. For HEIC, NEF, and video files, the date usually falls back to the modification time, which may not match the capture date.
- Files with identical timestamps have an arbitrary relative order.
- Subfolders are not processed. Only files directly inside the given folder are renamed.
- Existing files named `DSC_NNNN.ext` in the folder will be overwritten.

---

## License

MIT
