# 🚀 Smart File Organizer

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Automation](https://img.shields.io/badge/Automation-File%20Management-green)
![Status](https://img.shields.io/badge/Version-V2-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A Python automation tool that automatically organizes files in the **Downloads folder** by file type and renames them using timestamps for better file management.

This project was created to solve the common problem of **messy download folders** by automatically categorizing and organizing files.

---

# Features

### 📂 Automatic File Organization

Automatically detects file extensions and moves them into categorized folders.

### 🏷 Smart File Renaming

Files are renamed using a **date + counter format** to prevent overwriting.

Example:

```
2026-03-06_01_invoice.pdf
```

### 🧪 Dry Run Mode

Preview changes before actually moving files.

### 📊 Execution Summary

After running the script, a summary report is displayed.

Example:

```
Total Files Scanned : 32
Files Organized     : 29
Files Skipped       : 3
```

### 📝 Logging System

All actions are logged for tracking and debugging.

Log file:

```
Downloads/automation.log
```

---

# 📁 Supported File Categories

| File Extension      | Category Folder |
| ------------------- | --------------- |
| .pdf                | PDF             |
| .jpg / .jpeg / .png | Images          |
| .csv / .xlsx        | Data            |
| .txt                | Text            |
| .mp3 / .wav         | Audio           |
| .mp4 / .mov         | Videos          |
| .zip / .rar         | Archives        |
| .exe                | Executables     |
| Others              | Misc            |

---

# ⚙️ How It Works

1️⃣ The script scans the **Downloads folder**

2️⃣ Detects file extensions

3️⃣ Maps the extension to a category folder

4️⃣ Renames the file using:

```
YYYY-MM-DD_counter_filename
```

5️⃣ Moves the file into the correct folder

---

# 📊 Example

### Before Running Script

```
Downloads/
invoice.pdf
photo.jpg
song.mp3
video.mp4
report.xlsx
```

### After Running Script

```
Downloads/

PDF/
2026-03-06_01_invoice.pdf

Images/
2026-03-06_01_photo.jpg

Audio/
2026-03-06_01_song.mp3

Videos/
2026-03-06_01_video.mp4

Data/
2026-03-06_01_report.xlsx
```

---

# 🛠 Technologies Used

* Python
* OS Module
* shutil Module
* logging Module
* datetime Module

---

# 📦 Project Structure

```
smart-file-organizer
│
├ organizer_v1.py
├ organizer_v2.py
└ README.md
```

---

# 📈 Project Evolution

### Version 1

Basic automation script

* File organization
* File renaming
* Logging

### Version 2

Improved automation system

* Dry run mode
* Summary report
* File size logging
* Better error handling

---

# 🔮 Future Improvements

Planned features for upcoming versions:

* Duplicate file detection
* Recursive folder scanning
* Command-line interface
* Configuration file support
* Automated scheduling

---

# 👨‍💻 Author

**Devesh Pawar**
Python Developer

GitHub: https://github.com/itsOkDev