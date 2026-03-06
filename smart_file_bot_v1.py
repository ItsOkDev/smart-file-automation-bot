import os
import shutil
import logging
from datetime import datetime

BASE_DIR = os.path.expanduser("~/Downloads")

FOLDER_MAP = {
    ".pdf": "PDF",
    ".jpg": "Images",
    ".png": "Images",
    ".csv": "Data",
    ".xlsx": "Data",
    ".txt": "Text",
    ".mp3": "Audio",
    ".mp4": "Videos",
    ".zip": "Archives",
    ".exe": "Executables",
}

LOG_FILE = os.path.join(BASE_DIR, "automation.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def organize_files():
    logging.info("Automation started")

    try:
        files = os.listdir(BASE_DIR)

        for file in files:
            file_path = os.path.join(BASE_DIR, file)

            if os.path.isfile(file_path) and file != "automation.log":
                ext = os.path.splitext(file)[1].lower()
                folder_name = FOLDER_MAP.get(ext, "Misc")

                target_folder = os.path.join(BASE_DIR, folder_name)
                os.makedirs(target_folder, exist_ok=True)

                date_str = datetime.now().strftime("%Y-%m-%d")
                counter = 1
                new_name = f"{date_str}_{counter:02d}_{file}"

                while os.path.exists(os.path.join(target_folder, new_name)):
                    counter += 1
                    new_name = f"{date_str}_{counter:02d}_{file}"

                shutil.move(file_path, os.path.join(target_folder, new_name))

                logging.info(f"Moved & renamed: {file} -> {folder_name}/{new_name}")

    except Exception as e:
        logging.error(f"Automation failed: {e}")

    logging.info("Automation completed")


# ========================
# ENTRY POINT
# ========================
if __name__ == "__main__":
    organize_files()