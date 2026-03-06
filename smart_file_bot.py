import os
import shutil
import re
import hashlib
import json
import time
import random
from datetime import datetime, timedelta

# ============================================================
# ✅ MASTER SMART FILE V7 PRO By ItsOkDev
# ============================================================
# ✅ TRIAL: 3 Days OR 20 Runs
# ✅ PRO: Lifetime
# ✅ Features:
# - License Gate (Activated / Trial / Expired)
# - Device ID + Copy
# - Pro Locked Popups (clean UI)
# - Daily Automation Settings (Job Scheduler)
# - Battery Optimization Guide
# - Full Menu + Back to License Screen (B)
# - Fix: Change Settings loops correctly
# - Fix: Rename format 4 FREE, 5-9 PRO
# ============================================================

# -----------------------
# DEFAULT PATHS
# -----------------------
DEFAULT_SOURCE = "/storage/emulated/0/Download"
DEFAULT_OUTPUT = "/storage/emulated/0/Organized"

# -----------------------
# PROTECTED PATH PARTS
# -----------------------
PROTECTED_PATH_PARTS = ["/Android/", "/System/", "/MIUI/"]

# -----------------------
# ORGANIZE RULES
# -----------------------
RULES = {
    "Images/JPG": [".jpg", ".jpeg"],
    "Images/PNG": [".png"],
    "Images/GIF": [".gif"],
    "Images/WEBP": [".webp"],

    "Videos/MP4": [".mp4"],
    "Videos/MKV": [".mkv"],
    "Videos/MOV": [".mov"],
    "Videos/AVI": [".avi"],

    "Documents/PDF": [".pdf"],
    "Documents/Word": [".doc", ".docx"],
    "Documents/Excel": [".xls", ".xlsx"],
    "Documents/PPT": [".ppt", ".pptx"],
    "Documents/TXT": [".txt"],

    "Music/MP3": [".mp3"],
    "Music/M4A": [".m4a"],
    "Music/WAV": [".wav"],

    "APK": [".apk"],
    "ZIP": [".zip", ".rar", ".7z"],
}

CAT_CODE = {
    "Images/JPG": "IMG",
    "Images/PNG": "PNG",
    "Images/GIF": "GIF",
    "Images/WEBP": "WEBP",

    "Videos/MP4": "VID",
    "Videos/MKV": "VID",
    "Videos/MOV": "VID",
    "Videos/AVI": "VID",

    "Documents/PDF": "PDF",
    "Documents/Word": "DOC",
    "Documents/Excel": "XLS",
    "Documents/PPT": "PPT",
    "Documents/TXT": "TXT",

    "Music/MP3": "MUS",
    "Music/M4A": "MUS",
    "Music/WAV": "MUS",

    "APK": "APK",
    "ZIP": "ZIP",
    "Others": "FILE",
}

# ============================================================
# 🎨 UI COLORS (ANSI)
# ============================================================
RESET = "\033[0m"
BOLD = "\033[1m"
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_MAGENTA = "\033[95m"
C_BLUE = "\033[94m"
C_WHITE = "\033[97m"
C_GRAY = "\033[90m"


def ui_title(text):
    print(f"{BOLD}{C_CYAN}{text}{RESET}")


def ui_good(text):
    print(f"{C_GREEN}{text}{RESET}")


def ui_warn(text):
    print(f"{C_YELLOW}{text}{RESET}")


def ui_bad(text):
    print(f"{C_RED}{text}{RESET}")


def ui_info(text):
    print(f"{C_MAGENTA}{text}{RESET}")


def ui_line():
    print(f"{C_GRAY}{'-' * 58}{RESET}")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def safe_input(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return "0"


def press_enter(msg="Press ENTER to continue..."):
    input(f"\n{C_GRAY}{msg}{RESET}")


# ============================================================
# 🔐 LICENSE + TRIAL + PRO SYSTEM
# ============================================================
LICENSE_FILE = os.path.expanduser("~/.msf_v7_license.json")
SECRET_SALT = "ItsOkDev_MSFV7_2026_SECRET"  # 🔥 keep private

TRIAL_DAYS = 3
TRIAL_RUNS = 20


def get_device_id():
    home = os.path.expanduser("~")
    return "MSF-" + hashlib.md5(home.encode()).hexdigest()[:8].upper()


def make_license_key(device_id: str) -> str:
    raw = f"{device_id}:{SECRET_SALT}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_dt(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except:
        return None


def load_license():
    if not os.path.exists(LICENSE_FILE):
        return None
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


def save_license(data: dict):
    try:
        with open(LICENSE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except:
        pass


def init_trial_if_missing():
    device_id = get_device_id()
    data = load_license()

    if not data:
        data = {
            "device_id": device_id,
            "plan": "TRIAL",  # TRIAL / PRO
            "created_at": now_str(),
            "runs_used": 0,
            "activated": False,
            "license_key": "",
            "automation": {
                "enabled": False,
                "time": "09:00"
            }
        }
        save_license(data)

    if "automation" not in data:
        data["automation"] = {"enabled": False, "time": "09:00"}
        save_license(data)

    return data


def trial_status(data: dict):
    if data.get("plan") == "PRO" and data.get("activated") is True:
        return "PRO", 999, 999

    created = parse_dt(data.get("created_at", ""))
    if not created:
        created = datetime.now()

    days_used = (datetime.now() - created).days
    days_left = max(0, TRIAL_DAYS - days_used)

    runs_used = int(data.get("runs_used", 0))
    runs_left = max(0, TRIAL_RUNS - runs_used)

    if days_left <= 0 or runs_left <= 0:
        return "TRIAL_EXPIRED", days_left, runs_left

    return "TRIAL_ACTIVE", days_left, runs_left


def inc_run_counter_if_needed(data: dict):
    if data.get("plan") == "PRO" and data.get("activated") is True:
        return data
    data["runs_used"] = int(data.get("runs_used", 0)) + 1
    save_license(data)
    return data


def copy_to_clipboard(text: str):
    try:
        os.system(f'echo "{text}" | termux-clipboard-set')
        return True
    except:
        return False


# ============================================================
# 🔒 PRO LOCK POPUPS (V7 FIXED)
# ============================================================
def pro_locked_popup(feature="This Feature", reason_lines=None, price="$7"):
    clear_screen()
    ui_title("🔒 PRO FEATURE LOCKED")
    ui_line()

    ui_bad(f"{feature} is PRO only.")
    print("")

    ui_info("✅ Why this is PRO:")
    if not reason_lines:
        reason_lines = [
            "Advanced controls for power users",
            "Safer and more professional automation",
            "Extra reports + restore features"
        ]

    for line in reason_lines:
        print(f"• {line}")

    print("")
    ui_good(f"💎 Unlock PRO Lifetime for {price}")
    ui_warn("Main Menu → B) Back to License Screen → Activate Pro")
    ui_line()
    input("\nPress ENTER to continue...")


def lock_rename_popup():
    pro_locked_popup(
        feature="Advanced Rename Formats (5–9)",
        reason_lines=[
            "Includes TIME / SIZE / RANDOM naming options",
            "Perfect for privacy + backups + clean naming",
            "Best for creators & heavy users"
        ]
    )


def lock_md5_popup():
    pro_locked_popup(
        feature="Accurate Duplicate Finder (MD5 Hash)",
        reason_lines=[
            "Finds true duplicates even if file names differ",
            "Most accurate duplicate detection",
            "Best for cleaning storage safely"
        ]
    )


def lock_undo_popup():
    pro_locked_popup(
        feature="Undo History (Restore Files)",
        reason_lines=[
            "Undo moves and renames anytime",
            "Safe mode for confident cleaning",
            "Best for automation power users"
        ]
    )


def lock_profiles_popup():
    pro_locked_popup(
        feature="Profiles (Save / Load / Delete)",
        reason_lines=[
            "Save your favorite settings once",
            "Run same configuration again instantly",
            "Perfect for daily cleanup profiles"
        ]
    )


def lock_exclude_popup():
    pro_locked_popup(
        feature="Exclude List (Skip Important Files)",
        reason_lines=[
            "Protect important files from moving/renaming",
            "Best for work documents and personal folders",
            "More control and safety"
        ]
    )


def lock_report_popup():
    pro_locked_popup(
        feature="Large Files Report",
        reason_lines=[
            "Shows top biggest files",
            "Helps you free storage quickly",
            "Professional report output"
        ]
    )


def lock_date_mode_popup():
    pro_locked_popup(
        feature="Organize by Date Mode",
        reason_lines=[
            "Best for Photos/Videos cleanup",
            "Creates year/month folder structure",
            "Perfect for timeline backups"
        ]
    )


def lock_dashboard_popup():
    pro_locked_popup(
        feature="Summary Dashboard",
        reason_lines=[
            "Full statistics after run",
            "Largest files + total size + time report",
            "Premium end-screen results"
        ]
    )


def lock_automation_popup():
    pro_locked_popup(
        feature="Daily Automation (Auto Run)",
        reason_lines=[
            "Automatically runs daily cleanup",
            "No manual effort needed",
            "Best set-and-forget feature"
        ]
    )


# ============================================================
# 🔋 Battery Guide
# ============================================================
def show_battery_guide():
    clear_screen()
    ui_title("🔋 Battery Optimization Guide (Important)")
    ui_line()
    ui_warn("Android may STOP your daily automation if battery saving is ON.")
    print("")
    ui_info("✅ Fix Steps:")
    print(f"{C_WHITE}1){RESET} Settings → Apps → Termux → Battery")
    print(f"   Select: {C_GREEN}Unrestricted / Don't optimize{RESET}")
    print("")
    print(f"{C_WHITE}2){RESET} Allow Background Activity for Termux")
    print("")
    print(f"{C_WHITE}3){RESET} Vivo/Oppo/Realme/MIUI:")
    print("   Enable AutoStart + No Restrictions for Termux")
    print("")
    ui_info("✅ Helpful command:")
    print(f"{C_GRAY}termux-wake-lock{RESET}")
    ui_line()
    press_enter()


def require_pro(is_pro: bool, feature_name="This Feature"):
    if is_pro:
        return True
    pro_locked_popup(feature_name)
    return False


# ============================================================
# 🕒 DAILY AUTOMATION (Termux Job Scheduler)
# ============================================================
def set_daily_time_input(current="09:00"):
    clear_screen()
    ui_title("🕒 Set Daily Automation Time")
    ui_line()
    ui_info("Enter time in 24-hour format HH:MM")
    ui_warn("Example: 09:30 | 18:45 | 00:15")
    ui_line()

    t = safe_input(f"Time ({current}): ").strip()
    if not t:
        return current

    if not re.match(r"^\d{2}:\d{2}$", t):
        ui_bad("❌ Invalid format. Use HH:MM")
        press_enter()
        return current

    hh, mm = t.split(":")
    hh = int(hh)
    mm = int(mm)

    if not (0 <= hh <= 23 and 0 <= mm <= 59):
        ui_bad("❌ Invalid time range.")
        press_enter()
        return current

    return f"{hh:02d}:{mm:02d}"


def schedule_daily_job():
    script_path = os.path.abspath(__file__)
    os.system("termux-job-scheduler --cancel --job-id 101 >/dev/null 2>&1")

    cmd = (
        f'termux-job-scheduler --job-id 101 '
        f'--period-ms 86400000 --persisted true '
        f'--script "{script_path}"'
    )
    os.system(cmd)


def disable_daily_job():
    os.system("termux-job-scheduler --cancel --job-id 101 >/dev/null 2>&1")


def daily_automation_menu(data: dict, is_pro: bool):
    while True:
        clear_screen()
        ui_title("🕒 Daily Automation Settings")
        ui_line()

        enabled = data.get("automation", {}).get("enabled", False)
        t = data.get("automation", {}).get("time", "09:00")

        print(f"{C_WHITE}Status:{RESET} {C_GREEN if enabled else C_RED}{'ENABLED' if enabled else 'DISABLED'}{RESET}")
        print(f"{C_WHITE}Daily Time:{RESET} {C_YELLOW}{t}{RESET}")
        ui_line()

        print(f"{C_YELLOW}1){RESET} Enable Daily Automation ✅  {C_RED}[PRO]{RESET}")
        print(f"{C_YELLOW}2){RESET} Set Daily Time 🕒")
        print(f"{C_YELLOW}3){RESET} Disable Daily Automation ❌")
        print(f"{C_MAGENTA}4){RESET} Show Battery Fix Guide 🔋")
        print(f"{C_BLUE}B){RESET} Back")
        ui_line()

        ch = safe_input("Select: ").strip().upper()

        if ch == "1":
            if not is_pro:
                lock_automation_popup()
                continue

            data["automation"]["enabled"] = True
            save_license(data)
            schedule_daily_job()

            ui_good("✅ Daily Automation Enabled!")
            ui_warn("⚠️ If it stops, fix battery optimization for Termux.")
            press_enter()

        elif ch == "2":
            new_time = set_daily_time_input(t)
            data["automation"]["time"] = new_time
            save_license(data)
            ui_good(f"✅ Daily Time Updated: {new_time}")
            press_enter()

        elif ch == "3":
            data["automation"]["enabled"] = False
            save_license(data)
            disable_daily_job()
            ui_good("✅ Daily Automation Disabled.")
            press_enter()

        elif ch == "4":
            show_battery_guide()

        elif ch == "B":
            return


# ============================================================
# ✅ LICENSE GATE SCREEN (FIRST SCREEN)
# ============================================================
def screen_license_gate():
    data = init_trial_if_missing()
    device_id = data.get("device_id", get_device_id())
    valid_key = make_license_key(device_id)

    while True:
        clear_screen()
        ui_title("✅ MASTER SMART FILE V7 PRO By ItsOkDev")
        ui_line()

        status, days_left, runs_left = trial_status(data)

        print(f"{C_WHITE}📱 Device ID:{RESET} {C_GREEN}{device_id}{RESET}")

        if status == "PRO":
            ui_good("💎 Status: ACTIVATED (PRO LIFETIME)")
        elif status == "TRIAL_ACTIVE":
            ui_warn(f"🟡 Status: TRIAL ACTIVE | Days Left: {days_left} | Runs Left: {runs_left}")
        else:
            ui_bad("🔴 Status: TRIAL EXPIRED (Activation Required)")

        ui_line()
        print(f"{C_YELLOW}1){RESET} Copy Device ID 📋")
        print(f"{C_GREEN}2){RESET} Activate Pro (Enter License Key) 🔑")
        print(f"{C_BLUE}3){RESET} Battery Fix Guide 🔋")
        print(f"{C_MAGENTA}4){RESET} Daily Automation Settings 🕒")
        print(f"{C_WHITE}5){RESET} Continue ▶️")
        print(f"{C_RED}0){RESET} Exit")
        ui_line()

        ch = safe_input("Select: ").strip()

        if ch == "1":
            ok = copy_to_clipboard(device_id)
            if ok:
                ui_good("✅ Device ID copied to clipboard!")
            else:
                ui_warn("⚠️ Clipboard copy failed.")
                ui_info("Install Termux API:")
                print("pkg install termux-api")
            press_enter()

        elif ch == "2":
            clear_screen()
            ui_title("🔑 Activate PRO Lifetime")
            ui_line()
            print(f"{C_WHITE}Device ID:{RESET} {C_GREEN}{device_id}{RESET}")
            print(f"{C_GRAY}(Send this ID to ItsOkDev to get your key){RESET}")
            ui_line()

            key = safe_input("Enter License Key: ").strip().upper()
            if key == valid_key:
                data["plan"] = "PRO"
                data["activated"] = True
                data["license_key"] = key
                save_license(data)
                ui_good("✅ Activated Successfully! PRO Unlocked 🔥")
                press_enter()
            else:
                ui_bad("❌ Invalid Key! Please enter correct Pro key.")
                press_enter()

        elif ch == "3":
            show_battery_guide()

        elif ch == "4":
            is_pro = (data.get("plan") == "PRO" and data.get("activated") is True)
            daily_automation_menu(data, is_pro)

        elif ch == "5":
            if status == "TRIAL_EXPIRED":
                ui_bad("❌ Trial Expired. Activate Pro to continue.")
                press_enter()
                continue

            data = inc_run_counter_if_needed(data)
            status2, _, _ = trial_status(data)
            if status2 == "TRIAL_EXPIRED":
                ui_bad("❌ Trial limit reached now. Activate Pro to continue.")
                press_enter()
                continue

            is_pro = (data.get("plan") == "PRO" and data.get("activated") is True)
            return is_pro, data

        elif ch == "0":
            exit()


# ============================================================
# ✅ CORE UTILS
# ============================================================
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def is_protected_path(path: str) -> bool:
    p = path.replace("\\", "/")
    return any(part in p for part in PROTECTED_PATH_PARTS)


def get_ext(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()


def name_without_ext(filename: str) -> str:
    return os.path.splitext(filename)[0]


def clean_text(text: str, max_len: int = 18) -> str:
    text = text.strip()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^A-Za-z0-9_-]+", "_", text)
    text = re.sub(r"_+", "_", text)
    text = text.strip("_")
    if len(text) > max_len:
        text = text[:max_len]
    return text or "file"


def safe_unique_path(path: str) -> str:
    if not os.path.exists(path):
        return path
    folder = os.path.dirname(path)
    base = os.path.basename(path)
    name, ext = os.path.splitext(base)
    return os.path.join(folder, f"{name}_{int(datetime.now().timestamp())}{ext}")


def file_modified_date(path: str) -> datetime:
    return datetime.fromtimestamp(os.path.getmtime(path))


def bytes_to_mb(n: int) -> float:
    return round(n / (1024 * 1024), 2)


def size_tag(path: str) -> str:
    try:
        mb = bytes_to_mb(os.path.getsize(path))
        mb_int = max(1, int(round(mb)))
        return f"{mb_int}MB"
    except:
        return "0MB"


def folder_total_size_mb(file_paths):
    total = 0
    for p in file_paths:
        try:
            total += os.path.getsize(p)
        except:
            pass
    return bytes_to_mb(total)


def get_target_rel_folder(filename: str) -> str:
    ext = get_ext(filename)
    for folder, exts in RULES.items():
        if ext in exts:
            return folder
    return "Others"


def get_main_category(target_rel: str) -> str:
    return target_rel.split("/")[0] if "/" in target_rel else target_rel


def top_largest_files(file_paths, top_n=5):
    sizes = []
    for p in file_paths:
        try:
            sizes.append((p, os.path.getsize(p)))
        except:
            pass
    sizes.sort(key=lambda x: x[1], reverse=True)
    return sizes[:top_n]


# ============================================================
# ✅ PATHS (LOGS / UNDO / PROFILES)
# ============================================================
def get_paths(output_base: str):
    logs_dir = os.path.join(output_base, "logs")
    undo_dir = os.path.join(logs_dir, "undo")
    profiles_dir = os.path.join(logs_dir, "profiles")

    ensure_dir(logs_dir)
    ensure_dir(undo_dir)
    ensure_dir(profiles_dir)

    return {
        "logs_dir": logs_dir,
        "log_txt": os.path.join(logs_dir, "master_log.txt"),
        "large_report": os.path.join(logs_dir, "large_report.txt"),
        "undo_dir": undo_dir,
        "profiles_dir": profiles_dir,
        "exclude_list": os.path.join(logs_dir, "exclude.txt"),
    }


def log_write(log_file: str, msg: str):
    ensure_dir(os.path.dirname(log_file))
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


# ============================================================
# ✅ DUPLICATES
# ============================================================
def md5_hash(path: str, chunk=1024 * 1024) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def find_duplicates_fast(file_paths):
    seen = {}
    dups = []
    for p in file_paths:
        try:
            key = (os.path.basename(p).lower(), os.path.getsize(p))
            if key in seen:
                dups.append(p)
            else:
                seen[key] = p
        except:
            pass
    return dups


def find_duplicates_accurate(file_paths, is_pro=False):
    if not is_pro:
        return "LOCKED", []
    seen = {}
    dups = []
    for p in file_paths:
        try:
            h = md5_hash(p)
            if h in seen:
                dups.append(p)
            else:
                seen[h] = p
        except:
            pass
    return "OK", dups


# ============================================================
# ✅ EXCLUDE LIST
# ============================================================
def load_exclude_list(exclude_file: str, is_pro=False, enabled=False):
    if enabled and not is_pro:
        return "LOCKED", set()

    if not enabled:
        return "OFF", set()

    if not os.path.exists(exclude_file):
        return "OK", set()

    out = set()
    with open(exclude_file, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s:
                out.add(s)
    return "OK", out


# ============================================================
# ✅ RENAME ENGINE
# ============================================================
def build_new_name(option: str, cat: str, original_base: str, counter: int, ext: str, sep: str, path_for_size: str):
    ddmonyy = datetime.now().strftime("%d%b%y").upper()
    ymd = datetime.now().strftime("%Y-%m-%d")
    hm = datetime.now().strftime("%H%M")
    original_short = clean_text(original_base, max_len=18)
    rand = str(random.randint(100, 999))
    sz = size_tag(path_for_size)

    if option == "1":
        return f"{cat}{sep}{ddmonyy}{sep}{counter:03d}{ext}"
    if option == "2":
        return f"{ddmonyy}{sep}{cat}{sep}{counter:03d}{ext}"
    if option == "3":
        return f"{cat}{sep}{ymd}{sep}{counter:03d}{ext}"
    if option == "4":
        return f"{cat}{sep}{ddmonyy}{sep}{original_short}{sep}{counter:03d}{ext}"  # ✅ FREE
    if option == "5":
        return f"{original_short}{sep}{counter:03d}{ext}"
    if option == "6":
        return f"{cat}{sep}{counter:03d}{sep}{ddmonyy}{ext}"
    if option == "7":
        return f"{cat}{sep}{ddmonyy}{sep}{hm}{sep}{counter:03d}{ext}"
    if option == "8":
        return f"{cat}{sep}{ddmonyy}{sep}{sz}{sep}{counter:03d}{ext}"
    if option == "9":
        return f"{cat}{sep}{ddmonyy}{sep}{rand}{sep}{counter:03d}{ext}"

    return f"{cat}{sep}{ddmonyy}{sep}{counter:03d}{ext}"


# ============================================================
# ✅ ORGANIZE MODES
# ============================================================
def dest_folder_by_mode(output_base: str, target_rel: str, mode: str, src_path: str, is_pro=False):
    if mode == "1":
        return os.path.join(output_base, target_rel)

    if mode == "2":
        ext = get_ext(src_path).replace(".", "").upper() or "NOEXT"
        return os.path.join(output_base, "ByExtension", ext)

    if mode == "3":
        if not is_pro:
            return "LOCKED"
        dt = file_modified_date(src_path)
        return os.path.join(output_base, "ByDate", str(dt.year), f"{dt.month:02d}", target_rel)

    return os.path.join(output_base, target_rel)


# ============================================================
# ✅ PROGRESS BAR
# ============================================================
def progress_bar(current, total, width=28):
    if total <= 0:
        total = 1
    ratio = current / total
    done = int(ratio * width)
    bar = "#" * done + "-" * (width - done)
    pct = int(ratio * 100)
    return f"[{bar}] {pct:3d}% ({current}/{total})"


# ============================================================
# ✅ FILE OPS + UNDO ACTIONS
# ============================================================
def rename_file(path: str, new_filename: str, dry_run: bool, undo_actions: list, log_file: str):
    folder = os.path.dirname(path)
    new_path = os.path.join(folder, new_filename)
    new_path = safe_unique_path(new_path)
    log_write(log_file, f"RENAME: {path} -> {new_path}")

    if dry_run:
        return new_path

    os.rename(path, new_path)
    undo_actions.append({"type": "rename", "from": new_path, "to": path})
    return new_path


def move_file(path: str, dest_folder: str, dry_run: bool, undo_actions: list, log_file: str):
    ensure_dir(dest_folder)
    dest_path = os.path.join(dest_folder, os.path.basename(path))
    dest_path = safe_unique_path(dest_path)
    log_write(log_file, f"MOVE: {path} -> {dest_path}")

    if dry_run:
        return dest_path

    shutil.move(path, dest_path)
    undo_actions.append({"type": "move", "from": dest_path, "to": path})
    return dest_path


# ============================================================
# ✅ SCAN + REPORTS
# ============================================================
def scan_files(source_folder: str, older_than_days: int, exclude_set: set):
    out = []
    if not os.path.exists(source_folder):
        return out

    for name in os.listdir(source_folder):
        full = os.path.join(source_folder, name)
        if os.path.isfile(full):
            if is_protected_path(full):
                continue
            if name in exclude_set:
                continue
            if older_than_days > 0:
                dt = file_modified_date(full)
                if dt > (datetime.now() - timedelta(days=older_than_days)):
                    continue
            out.append(full)
    return out


def generate_large_report(file_paths, report_file, is_pro=False):
    if not is_pro:
        return "LOCKED", []

    ensure_dir(os.path.dirname(report_file))
    sizes = []
    for p in file_paths:
        try:
            sizes.append((p, os.path.getsize(p)))
        except:
            pass
    sizes.sort(key=lambda x: x[1], reverse=True)
    top = sizes[:20]

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("TOP LARGE FILES REPORT\n")
        f.write("======================\n")
        for i, (p, s) in enumerate(top, start=1):
            f.write(f"{i}. {bytes_to_mb(s)} MB -> {os.path.basename(p)}\n")

    return "OK", top


# ============================================================
# ✅ DUPLICATE PREVIEW + CONFIRM
# ============================================================
def duplicate_preview_and_confirm(dups, limit=15):
    clear_screen()
    ui_title("🧠 Duplicate Preview + Confirm")
    ui_line()

    ui_info(f"Duplicates Found: {len(dups)}")

    if not dups:
        ui_good("No duplicates ✅")
        press_enter()
        return "SKIP"

    ui_warn("\nPreview List:")
    for p in dups[:limit]:
        print(f"📌 {os.path.basename(p)}")

    if len(dups) > limit:
        ui_warn(f"... +{len(dups) - limit} more")

    ui_line()
    print(f"{C_GREEN}1){RESET} Move ALL duplicates ✅")
    print(f"{C_YELLOW}2){RESET} Skip duplicates ❌")
    print(f"{C_MAGENTA}3){RESET} Show FULL list 📄")
    print(f"{C_RED}0){RESET} Abort")
    ui_line()

    ch = safe_input("Select: ").strip()
    if ch == "1":
        return "MOVE"
    if ch == "2":
        return "SKIP"
    if ch == "3":
        clear_screen()
        ui_title("📄 FULL DUPLICATE LIST")
        ui_line()
        for p in dups:
            print(p)
        press_enter()
        return duplicate_preview_and_confirm(dups, limit=limit)

    return "ABORT"


# ============================================================
# ✅ DASHBOARD (Trial -> Mini summary only)
# ============================================================
def show_dashboard(summary: dict, is_pro=False):
    if not is_pro:
        clear_screen()
        ui_title("✅ Run Completed (Trial Mode)")
        ui_line()
        ui_warn("🔒 Full Summary Dashboard is PRO only.")
        ui_info(f"Scanned: {summary.get('scanned', 0)}")
        ui_info(f"Moved  : {summary.get('moved', 0)}")
        ui_info(f"Renamed: {summary.get('renamed', 0)}")
        ui_line()
        press_enter()
        return

    clear_screen()
    ui_title("📊 SUMMARY DASHBOARD")
    ui_line()

    print(f"{C_WHITE}Scanned Files:{RESET} {C_GREEN}{summary.get('scanned', 0)}{RESET}")
    print(f"{C_WHITE}Renamed Files:{RESET} {C_GREEN}{summary.get('renamed', 0)}{RESET}")
    print(f"{C_WHITE}Moved Files  :{RESET} {C_GREEN}{summary.get('moved', 0)}{RESET}")
    print(f"{C_WHITE}Duplicates   :{RESET} {C_GREEN}{summary.get('duplicates', 0)}{RESET}")
    print(f"{C_WHITE}Total Size   :{RESET} {C_GREEN}{summary.get('total_mb', 0)} MB{RESET}")
    print(f"{C_WHITE}Time Taken   :{RESET} {C_GREEN}{summary.get('time', 0)} sec{RESET}")
    print("")

    ui_info("Top Largest Files:")
    largest = summary.get("largest", [])
    if not largest:
        print("None")
    else:
        for i, (p, s) in enumerate(largest, start=1):
            print(f"{i}) {os.path.basename(p)} - {bytes_to_mb(s)} MB")

    ui_line()
    ui_info(f"Output Folder: {summary.get('output')}")
    ui_info(f"Log File     : {summary.get('log_file')}")
    ui_line()
    press_enter()


# ============================================================
# ✅ UNDO HISTORY
# ============================================================
def list_undo_files(undo_dir: str):
    if not os.path.exists(undo_dir):
        return []
    files = [f for f in os.listdir(undo_dir) if f.endswith(".json")]
    files.sort(reverse=True)
    return files


def undo_preview(undo_file_path: str):
    try:
        with open(undo_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        actions = data.get("actions", [])
        created = data.get("created", "unknown")
        moves = sum(1 for a in actions if a.get("type") == "move")
        renames = sum(1 for a in actions if a.get("type") == "rename")
        return {"created": created, "total": len(actions), "moves": moves, "renames": renames}
    except:
        return {"created": "unknown", "total": 0, "moves": 0, "renames": 0}


def apply_undo(undo_file_path: str):
    if not os.path.exists(undo_file_path):
        return False, "Undo file not found."

    try:
        with open(undo_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        actions = data.get("actions", [])
        actions.reverse()

        undone = 0
        total = len(actions)

        for i, act in enumerate(actions, start=1):
            t = act.get("type")
            src = act.get("from")
            dst = act.get("to")

            print(f"\r{C_YELLOW}UNDO {progress_bar(i, total)}{RESET}", end="")

            if not src or not dst:
                continue

            ensure_dir(os.path.dirname(dst))

            if t == "move":
                if os.path.exists(src):
                    shutil.move(src, dst)
                    undone += 1
            elif t == "rename":
                if os.path.exists(src):
                    os.rename(src, dst)
                    undone += 1

        print("")
        return True, f"Undo complete ✅ Actions undone: {undone}"

    except Exception as e:
        return False, f"Undo failed: {e}"


# ============================================================
# ✅ PROFILES
# ============================================================
def profile_path(profiles_dir: str, name: str):
    safe = clean_text(name, max_len=30)
    return os.path.join(profiles_dir, f"{safe}.json")


def save_profile(profiles_dir: str, profile_name: str, settings: dict):
    ensure_dir(profiles_dir)
    p = profile_path(profiles_dir, profile_name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
    return p


def load_profile(profiles_dir: str, profile_name: str):
    p = profile_path(profiles_dir, profile_name)
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def list_profiles(profiles_dir: str):
    if not os.path.exists(profiles_dir):
        return []
    files = [f for f in os.listdir(profiles_dir) if f.endswith(".json")]
    files.sort()
    return files


def delete_profile(profiles_dir: str, profile_file: str):
    p = os.path.join(profiles_dir, profile_file)
    if os.path.exists(p):
        os.remove(p)
        return True
    return False


# ============================================================
# ✅ MENUS / SCREENS
# ============================================================
def screen_main_menu():
    clear_screen()
    ui_title("✅ MASTER SMART FILE V7 PRO By ItsOkDev")
    ui_line()
    print(f"{C_YELLOW}1){RESET} Dry Run Preview ✅")
    print(f"{C_YELLOW}2){RESET} Run Real ✅")
    print(f"{C_YELLOW}3){RESET} Profiles (Save/Load/Delete) 👤 {C_RED}[PRO]{RESET}")
    print(f"{C_YELLOW}4){RESET} Duplicate Tools 🧠 {C_RED}[PRO]{RESET}")
    print(f"{C_YELLOW}5){RESET} Undo History 🔁 {C_RED}[PRO]{RESET}")
    print(f"{C_YELLOW}6){RESET} Daily Automation Settings 🕒 {C_RED}[PRO]{RESET}")
    print(f"{C_BLUE}B){RESET} Back to License Screen 🔙")
    print(f"{C_RED}0){RESET} Exit")
    ui_line()
    return safe_input("Select option: ").strip().upper()


def screen_select_folder(title="Select Source Folder"):
    clear_screen()
    ui_title(f"📂 {title}")
    ui_line()
    print(f"{C_YELLOW}1){RESET} Download")
    print(f"{C_YELLOW}2){RESET} DCIM / Camera")
    print(f"{C_YELLOW}3){RESET} WhatsApp Media")
    print(f"{C_YELLOW}4){RESET} Documents")
    print(f"{C_YELLOW}5){RESET} Custom Path")
    print(f"{C_BLUE}B){RESET} Back")
    print(f"{C_RED}0){RESET} Abort")
    ui_line()
    return safe_input("Select: ").upper()


def resolve_folder(choice: str):
    if choice == "1":
        return DEFAULT_SOURCE
    if choice == "2":
        return "/storage/emulated/0/DCIM/Camera"
    if choice == "3":
        return "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media"
    if choice == "4":
        return "/storage/emulated/0/Documents"
    if choice == "5":
        return safe_input("Enter custom path: ")
    return None


def screen_action_menu():
    clear_screen()
    ui_title("⚙️ Choose Action")
    ui_line()
    print(f"{C_YELLOW}1){RESET} Organize")
    print(f"{C_YELLOW}2){RESET} Rename")
    print(f"{C_YELLOW}3){RESET} Organize + Rename ✅")
    print(f"{C_BLUE}B){RESET} Back")
    print(f"{C_RED}0){RESET} Abort")
    ui_line()
    return safe_input("Select: ").upper()


def screen_separator_menu():
    clear_screen()
    ui_title("🔧 Choose Rename Separator")
    ui_line()
    print(f"{C_YELLOW}1){RESET} __  (double underscore) ✅")
    print(f"   Example: IMG__19JAN26__001.jpg\n")
    print(f"{C_YELLOW}2){RESET} _   (single underscore)")
    print(f"   Example: IMG_19JAN26_001.jpg\n")
    print(f"{C_YELLOW}3){RESET} -   (dash)")
    print(f"   Example: IMG-19JAN26-001.jpg\n")
    print(f"{C_YELLOW}4){RESET} .   (dot)")
    print(f"   Example: IMG.19JAN26.001.jpg\n")
    print(f"{C_YELLOW}5){RESET} Custom Separator")
    print(f"   Example: IMG|19JAN26|001.jpg\n")
    print(f"{C_BLUE}B){RESET} Back")
    print(f"{C_RED}0){RESET} Abort")
    ui_line()
    return safe_input("Select: ").upper()


def resolve_separator(choice: str):
    if choice == "1":
        return "__"
    if choice == "2":
        return "_"
    if choice == "3":
        return "-"
    if choice == "4":
        return "."
    if choice == "5":
        s = safe_input("Enter custom separator: ")
        return s if s else "__"
    return "__"


def screen_rename_format_menu(sep="__"):
    clear_screen()
    ui_title("✏️ Rename Format Options")
    ui_line()
    ui_info(f"Example file: download(7).pdf | CAT=PDF | sep='{sep}'\n")
    print(f"{C_YELLOW}1){RESET} PDF{sep}19JAN26{sep}001.pdf ✅")
    print(f"{C_YELLOW}2){RESET} 19JAN26{sep}PDF{sep}001.pdf")
    print(f"{C_YELLOW}3){RESET} PDF{sep}2026-01-19{sep}001.pdf")
    print(f"{C_YELLOW}4){RESET} PDF{sep}19JAN26{sep}download_7{sep}001.pdf ✅ (FREE)")
    print(f"{C_YELLOW}5){RESET} download_7{sep}001.pdf {C_RED}[PRO]{RESET}")
    print(f"{C_YELLOW}6){RESET} PDF{sep}001{sep}19JAN26.pdf {C_RED}[PRO]{RESET}")
    print(f"{C_YELLOW}7){RESET} PDF{sep}19JAN26{sep}2315{sep}001.pdf {C_RED}[PRO]{RESET}")
    print(f"{C_YELLOW}8){RESET} PDF{sep}19JAN26{sep}3MB{sep}001.pdf {C_RED}[PRO]{RESET}")
    print(f"{C_YELLOW}9){RESET} PDF{sep}19JAN26{sep}777{sep}001.pdf {C_RED}[PRO]{RESET}")
    print("")
    print(f"{C_BLUE}B){RESET} Back")
    print(f"{C_RED}0){RESET} Abort")
    ui_line()
    return safe_input("Select (1-9): ").upper()


def screen_toggle_types(state: dict):
    clear_screen()
    ui_title("✅ Rename Which Types? (Toggle ON/OFF)")
    ui_line()

    def flag(v):
        return f"{C_GREEN}ON{RESET}" if v else f"{C_RED}OFF{RESET}"

    print(f"{C_YELLOW}1){RESET} Images     [ {flag(state['Images'])} ]")
    print(f"{C_YELLOW}2){RESET} Videos     [ {flag(state['Videos'])} ]")
    print(f"{C_YELLOW}3){RESET} Documents  [ {flag(state['Documents'])} ]")
    print(f"{C_YELLOW}4){RESET} APK        [ {flag(state['APK'])} ]")
    print(f"{C_YELLOW}5){RESET} ZIP        [ {flag(state['ZIP'])} ]")
    print(f"{C_YELLOW}6){RESET} Music      [ {flag(state['Music'])} ]")
    print(f"{C_YELLOW}7){RESET} Others     [ {flag(state['Others'])} ]")
    print("")
    print(f"{C_GREEN}A){RESET} Select All")
    print(f"{C_MAGENTA}N){RESET} Select None")
    print(f"{C_GREEN}S){RESET} Save & Continue ✅")
    print(f"{C_BLUE}B){RESET} Back")
    print(f"{C_RED}0){RESET} Abort")
    ui_line()
    return safe_input("Select: ").upper()


def screen_organize_mode(is_pro=False):
    clear_screen()
    ui_title("📦 Organize Mode")
    ui_line()
    print(f"{C_YELLOW}1){RESET} Normal folders")
    print(f"{C_YELLOW}2){RESET} Extension folders")
    print(f"{C_YELLOW}3){RESET} Date folders {C_RED}[PRO]{RESET}")
    if not is_pro:
        ui_warn("   🔒 PRO Required for Date mode")
    print("")
    print(f"{C_BLUE}B){RESET} Back")
    print(f"{C_RED}0){RESET} Abort")
    ui_line()
    return safe_input("Select (1-3): ").upper()


def screen_extras_menu(extras):
    clear_screen()
    ui_title("🧠 Extra Features")
    ui_line()

    def onoff(v):
        return f"{C_GREEN}ON{RESET}" if v else f"{C_RED}OFF{RESET}"

    print(f"{C_YELLOW}1){RESET} Large Files Report      [ {onoff(extras['large_report'])} ]")
    print(f"{C_YELLOW}2){RESET} Duplicate Finder Mode   [ {C_MAGENTA}{extras['dup_mode']}{RESET} ]  (OFF/FAST/ACCURATE)")
    print(f"{C_YELLOW}3){RESET} Only older than days    [ {C_MAGENTA}{extras['older_than_days']}{RESET} ]  (0/7/30)")
    print(f"{C_YELLOW}4){RESET} Exclude List Enabled    [ {onoff(extras['exclude_enabled'])} ]")
    print(f"{C_YELLOW}5){RESET} Undo Support            [ {onoff(extras['undo_enabled'])} ]")
    print("")
    print(f"{C_GREEN}S){RESET} Save & Continue ✅")
    print(f"{C_BLUE}B){RESET} Back")
    print(f"{C_RED}0){RESET} Abort")
    ui_line()
    return safe_input("Select: ").upper()


def screen_preview(rename_list, move_list, extras, log_file):
    clear_screen()
    ui_title("✅ DRY RUN PREVIEW (NO CHANGES)")
    ui_line()

    if rename_list:
        ui_info("[RENAME PREVIEW]")
        for a, b in rename_list[:10]:
            print(f"{C_WHITE}{a}{RESET}  {C_GRAY}--> {RESET}{C_GREEN}{b}{RESET}")
        if len(rename_list) > 10:
            ui_warn(f"... +{len(rename_list) - 10} more")
        print("")

    if move_list:
        ui_info("[MOVE PREVIEW]")
        for a, b in move_list[:10]:
            print(f"{C_WHITE}{a}{RESET}  {C_GRAY}--> {RESET}{C_GREEN}{b}{RESET}")
        if len(move_list) > 10:
            ui_warn(f"... +{len(move_list) - 10} more")
        print("")

    ui_info("[EXTRAS]")
    print(f"Large Report: {'ON' if extras['large_report'] else 'OFF'}")
    print(f"Duplicate Mode: {extras['dup_mode']}")
    print(f"Older Than Days: {extras['older_than_days']}")
    print(f"Exclude List: {'ON' if extras['exclude_enabled'] else 'OFF'}")
    print(f"Undo Support: {'ON' if extras['undo_enabled'] else 'OFF'}")

    ui_line()
    ui_info(f"📄 Log: {log_file}")
    ui_line()
    print(f"{C_GREEN}1){RESET} Confirm Real Run ✅")
    print(f"{C_YELLOW}2){RESET} Change Settings")
    print(f"{C_RED}0){RESET} Abort")
    ui_line()
    return safe_input("Select: ").strip()


# ============================================================
# ✅ CONFIG FLOW (with locks)
# ============================================================
def configure_flow(is_pro=False):
    src_choice = screen_select_folder("Select Source Folder")
    if src_choice == "0":
        return None
    if src_choice == "B":
        return "BACK"

    source_folder = resolve_folder(src_choice)
    if not source_folder or not os.path.exists(source_folder):
        ui_bad("Source folder not found.")
        press_enter()
        return None

    act = screen_action_menu()
    if act == "0":
        return None
    if act == "B":
        return "BACK"

    do_organize = act in ["1", "3"]
    do_rename = act in ["2", "3"]

    sep = "__"
    rename_format = "1"
    rename_types = {k: False for k in ["Images", "Videos", "Documents", "APK", "ZIP", "Music", "Others"]}
    organize_mode = "1"

    if do_rename:
        sp = screen_separator_menu()
        if sp == "0":
            return None
        if sp == "B":
            return "BACK"

        sep = resolve_separator(sp)
        ui_info(f"\n✅ Example separator output: PDF{sep}19JAN26{sep}001.pdf")
        press_enter()

        rf = screen_rename_format_menu(sep=sep)
        if rf == "0":
            return None
        if rf == "B":
            return "BACK"

        # ✅ PRO LOCK: only 5-9 locked (4 is FREE)
        if rf in ["5", "6", "7", "8", "9"] and not is_pro:
            lock_rename_popup()
            rf = "1"

        if rf not in [str(i) for i in range(1, 10)]:
            rf = "1"

        rename_format = rf
        press_enter("Rename format selected ✅")

        while True:
            t = screen_toggle_types(rename_types)
            if t == "0":
                return None
            if t == "B":
                return "BACK"
            if t == "A":
                for k in rename_types:
                    rename_types[k] = True
            elif t == "N":
                for k in rename_types:
                    rename_types[k] = False
            elif t == "S":
                break
            elif t in ["1", "2", "3", "4", "5", "6", "7"]:
                m = {"1": "Images", "2": "Videos", "3": "Documents", "4": "APK", "5": "ZIP", "6": "Music", "7": "Others"}
                key = m[t]
                rename_types[key] = not rename_types[key]

    if do_organize:
        om = screen_organize_mode(is_pro=is_pro)
        if om == "0":
            return None
        if om == "B":
            return "BACK"

        if om == "3" and not is_pro:
            lock_date_mode_popup()
            om = "1"

        if om in ["1", "2", "3"]:
            organize_mode = om

        press_enter("Organize mode selected ✅")

    extras = {
        "large_report": False,
        "dup_mode": "OFF",
        "older_than_days": 0,
        "exclude_enabled": False,
        "undo_enabled": False
    }

    while True:
        ex = screen_extras_menu(extras)
        if ex == "0":
            return None
        if ex == "B":
            break
        if ex == "S":
            break

        if ex == "1":
            if not is_pro:
                lock_report_popup()
                continue
            extras["large_report"] = not extras["large_report"]

        elif ex == "2":
            if not is_pro:
                lock_md5_popup()
                continue
            if extras["dup_mode"] == "OFF":
                extras["dup_mode"] = "FAST"
            elif extras["dup_mode"] == "FAST":
                extras["dup_mode"] = "ACCURATE"
            else:
                extras["dup_mode"] = "OFF"

        elif ex == "3":
            if extras["older_than_days"] == 0:
                extras["older_than_days"] = 7
            elif extras["older_than_days"] == 7:
                extras["older_than_days"] = 30
            else:
                extras["older_than_days"] = 0

        elif ex == "4":
            if not is_pro:
                lock_exclude_popup()
                continue
            extras["exclude_enabled"] = not extras["exclude_enabled"]

        elif ex == "5":
            if not is_pro:
                lock_undo_popup()
                continue
            extras["undo_enabled"] = not extras["undo_enabled"]

    return {
        "source_folder": source_folder,
        "output_base": DEFAULT_OUTPUT,
        "do_organize": do_organize,
        "do_rename": do_rename,
        "sep": sep,
        "rename_format": rename_format,
        "rename_types": rename_types,
        "organize_mode": organize_mode,
        "extras": extras
    }


# ============================================================
# ✅ EXECUTION ENGINE
# ============================================================
def run_pipeline(settings: dict, dry_run=True, is_pro=False):
    source_folder = settings["source_folder"]
    output_base = settings["output_base"]
    do_organize = settings["do_organize"]
    do_rename = settings["do_rename"]
    rename_format = settings["rename_format"]
    sep = settings["sep"]
    rename_types = settings["rename_types"]
    organize_mode = settings["organize_mode"]
    extras = settings["extras"]

    paths = get_paths(output_base)
    log_file = paths["log_txt"]

    # ✅ EXCLUDE LIST
    ex_status, exclude_set = load_exclude_list(paths["exclude_list"], is_pro=is_pro, enabled=extras["exclude_enabled"])
    if ex_status == "LOCKED":
        exclude_set = set()
        extras["exclude_enabled"] = False

    file_paths = scan_files(source_folder, extras["older_than_days"], exclude_set)
    scanned = len(file_paths)
    total_mb = folder_total_size_mb(file_paths)
    largest = top_largest_files(file_paths, top_n=5)

    rename_preview = []
    move_preview = []
    counters = {}

    for p in file_paths:
        fname = os.path.basename(p)
        target_rel = get_target_rel_folder(fname)
        main_cat = get_main_category(target_rel)
        cat = CAT_CODE.get(target_rel, "FILE")

        counters.setdefault(cat, 0)
        counters[cat] += 1

        final_name = fname
        if do_rename and rename_types.get(main_cat, False):
            new_name = build_new_name(rename_format, cat, name_without_ext(fname), counters[cat], get_ext(fname), sep, p)
            rename_preview.append((fname, new_name))
            final_name = new_name

        if do_organize:
            dest = dest_folder_by_mode(output_base, target_rel, organize_mode, p, is_pro=is_pro)
            if dest == "LOCKED":
                dest = os.path.join(output_base, target_rel)
            move_preview.append((final_name, dest))

    if dry_run:
        return {
            "rename_preview": rename_preview,
            "move_preview": move_preview,
            "log_file": log_file,
            "scanned": scanned,
            "total_mb": total_mb
        }

    moved = 0
    renamed = 0
    duplicates_moved = 0
    undo_actions = []
    start = time.time()

    total = len(file_paths)
    counters = {}

    for idx, p in enumerate(file_paths, start=1):
        try:
            fname = os.path.basename(p)
            target_rel = get_target_rel_folder(fname)
            main_cat = get_main_category(target_rel)
            cat = CAT_CODE.get(target_rel, "FILE")

            counters.setdefault(cat, 0)
            counters[cat] += 1

            current = p

            if do_rename and rename_types.get(main_cat, False):
                new_name = build_new_name(rename_format, cat, name_without_ext(fname), counters[cat], get_ext(fname), sep, p)
                current = rename_file(current, new_name, False, undo_actions, log_file)
                renamed += 1

            if do_organize:
                dest = dest_folder_by_mode(output_base, target_rel, organize_mode, p, is_pro=is_pro)
                if dest == "LOCKED":
                    dest = os.path.join(output_base, target_rel)
                move_file(current, dest, False, undo_actions, log_file)
                moved += 1

            print(f"\r{C_YELLOW}{progress_bar(idx, total)}{RESET} {C_GREEN}OK{RESET}", end="")

        except Exception as e:
            log_write(log_file, f"ERROR: {p} -> {e}")
            print(f"\r{C_YELLOW}{progress_bar(idx, total)}{RESET} {C_RED}ERR{RESET}", end="")

    print("")

    # ✅ Large report (PRO)
    if extras["large_report"]:
        st, _ = generate_large_report(file_paths, paths["large_report"], is_pro=is_pro)
        if st == "OK":
            log_write(log_file, f"Large report saved: {paths['large_report']}")

    # ✅ Duplicates (PRO)
    if extras["dup_mode"] != "OFF":
        if not is_pro:
            lock_md5_popup()
        else:
            ui_warn("\nDuplicate scan running...")

            if extras["dup_mode"] == "FAST":
                dups = find_duplicates_fast(file_paths)
            else:
                st, dups = find_duplicates_accurate(file_paths, is_pro=is_pro)
                if st == "LOCKED":
                    dups = []

            action = duplicate_preview_and_confirm(dups)

            if action == "MOVE":
                dup_folder = os.path.join(output_base, "Duplicates")
                ensure_dir(dup_folder)

                total_d = len(dups)
                for i, d in enumerate(dups, start=1):
                    try:
                        dest = safe_unique_path(os.path.join(dup_folder, os.path.basename(d)))
                        shutil.move(d, dest)
                        undo_actions.append({"type": "move", "from": dest, "to": d})
                        duplicates_moved += 1
                        print(f"\r{C_YELLOW}{progress_bar(i, total_d)}{RESET} moving duplicates...", end="")
                    except:
                        pass
                print("")
                ui_good(f"Duplicates moved: {duplicates_moved}")

    # ✅ Save undo (PRO)
    if extras["undo_enabled"] and is_pro:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        undo_file = os.path.join(paths["undo_dir"], f"undo_{timestamp}.json")
        with open(undo_file, "w", encoding="utf-8") as f:
            json.dump({"created": str(datetime.now()), "actions": undo_actions}, f, indent=2)
        log_write(log_file, f"UNDO file saved: {undo_file}")

    elapsed = round(time.time() - start, 2)

    summary = {
        "scanned": scanned,
        "renamed": renamed,
        "moved": moved,
        "duplicates": duplicates_moved,
        "total_mb": total_mb,
        "time": elapsed,
        "largest": largest,
        "output": output_base,
        "log_file": log_file,
    }

    show_dashboard(summary, is_pro=is_pro)
    return summary


# ============================================================
# ✅ PROFILES MENU (PRO Version only)
# ============================================================
def profiles_menu(is_pro=False):
    if not is_pro:
        lock_profiles_popup()
        return

    paths = get_paths(DEFAULT_OUTPUT)
    prof_dir = paths["profiles_dir"]

    while True:
        clear_screen()
        ui_title("👤 PROFILES MENU")
        ui_line()
        print(f"{C_YELLOW}1){RESET} Create Profile")
        print(f"{C_YELLOW}2){RESET} Load Profile")
        print(f"{C_YELLOW}3){RESET} Delete Profile")
        print(f"{C_YELLOW}4){RESET} List Profiles")
        print(f"{C_BLUE}B){RESET} Back")
        print(f"{C_RED}0){RESET} Abort")
        ui_line()

        pc = safe_input("Select: ").upper()
        if pc == "0":
            return "ABORT"
        if pc == "B":
            return None

        profs = list_profiles(prof_dir)

        if pc == "4":
            ui_info("\nSaved Profiles:")
            if not profs:
                ui_warn("No profiles saved.")
            else:
                for p in profs:
                    print(f"✅ {p}")
            press_enter()

        elif pc == "1":
            settings = configure_flow(is_pro=is_pro)
            if settings in [None, "BACK"]:
                continue

            name = safe_input("Enter Profile Name (example: DailyClean): ")
            if not name:
                ui_bad("Profile name required.")
                press_enter()
                continue

            saved_path = save_profile(prof_dir, name, settings)
            ui_good(f"Profile saved ✅ {saved_path}")
            press_enter()

        elif pc == "2":
            if not profs:
                ui_warn("No profiles available.")
                press_enter()
                continue

            ui_info("\nProfiles:")
            for i, p in enumerate(profs, start=1):
                print(f"{i}) {p}")

            idx = safe_input("Select profile number: ")
            if idx.isdigit():
                n = int(idx)
                if 1 <= n <= len(profs):
                    profile_file = profs[n - 1]
                    profile_name = profile_file.replace(".json", "")
                    settings = load_profile(prof_dir, profile_name)

                    if not settings:
                        ui_bad("Failed to load profile.")
                        press_enter()
                        continue

                    ui_good(f"Loaded: {profile_file}")
                    press_enter()

                    while True:
                        prev = run_pipeline(settings, dry_run=True, is_pro=is_pro)
                        go = screen_preview(prev["rename_preview"], prev["move_preview"], settings["extras"], prev["log_file"])

                        if go == "1":
                            run_pipeline(settings, dry_run=False, is_pro=is_pro)
                            break
                        elif go == "2":
                            settings = configure_flow(is_pro=is_pro)
                            if settings in ["BACK", None]:
                                break
                            continue
                        else:
                            ui_warn("Aborted ❌")
                            press_enter()
                            break

        elif pc == "3":
            if not profs:
                ui_warn("No profiles to delete.")
                press_enter()
                continue

            ui_info("\nProfiles:")
            for i, p in enumerate(profs, start=1):
                print(f"{i}) {p}")

            idx = safe_input("Select profile number to delete: ")
            if idx.isdigit():
                n = int(idx)
                if 1 <= n <= len(profs):
                    ok = delete_profile(prof_dir, profs[n - 1])
                    if ok:
                        ui_good("Profile deleted ✅")
                    else:
                        ui_bad("Delete failed ❌")
                    press_enter()


# ============================================================
# ✅ DUPLICATE TOOLS MENU (PRO)
# ============================================================
def duplicate_tools_menu(is_pro=False):
    if not is_pro:
        lock_md5_popup()
        return

    while True:
        clear_screen()
        ui_title("🧠 DUPLICATE TOOLS")
        ui_line()
        print(f"{C_YELLOW}1){RESET} Scan FAST (name+size)")
        print(f"{C_YELLOW}2){RESET} Scan ACCURATE (hash) ⚠️ slow")
        print(f"{C_YELLOW}3){RESET} Move duplicates (FAST) with preview+confirm")
        print(f"{C_BLUE}B){RESET} Back")
        print(f"{C_RED}0){RESET} Abort")
        ui_line()

        ch = safe_input("Select: ").upper()
        if ch == "0":
            return "ABORT"
        if ch == "B":
            return None

        folder_choice = screen_select_folder("Select folder for duplicate scan")
        if folder_choice == "0":
            return "ABORT"
        if folder_choice == "B":
            continue

        folder = resolve_folder(folder_choice)
        if not folder or not os.path.exists(folder):
            ui_bad("Folder not found.")
            press_enter()
            continue

        files = scan_files(folder, 0, set())

        if ch == "1":
            dups = find_duplicates_fast(files)
            duplicate_preview_and_confirm(dups)
            ui_info(f"FAST duplicates count: {len(dups)}")
            press_enter()

        elif ch == "2":
            ui_warn("Accurate scan can be slow...")
            st, dups = find_duplicates_accurate(files, is_pro=is_pro)
            if st == "LOCKED":
                ui_bad("🔒 Accurate scan locked.")
                press_enter()
                continue
            duplicate_preview_and_confirm(dups)
            ui_info(f"ACCURATE duplicates count: {len(dups)}")
            press_enter()

        elif ch == "3":
            dups = find_duplicates_fast(files)
            action = duplicate_preview_and_confirm(dups)

            if action == "MOVE":
                dup_folder = os.path.join(DEFAULT_OUTPUT, "Duplicates")
                ensure_dir(dup_folder)
                moved = 0
                total = len(dups)
                for i, d in enumerate(dups, start=1):
                    try:
                        dest = safe_unique_path(os.path.join(dup_folder, os.path.basename(d)))
                        shutil.move(d, dest)
                        moved += 1
                        print(f"\r{C_YELLOW}{progress_bar(i, total)}{RESET} moving...", end="")
                    except:
                        pass
                print("")
                ui_good(f"Moved duplicates: {moved}")
                press_enter()
            else:
                ui_warn("Skipped duplicates.")
                press_enter()


# ============================================================
# ✅ UNDO MENU (PRO Version Only)
# ============================================================
def undo_menu(is_pro=False):
    if not is_pro:
        lock_undo_popup()
        return

    paths = get_paths(DEFAULT_OUTPUT)
    undo_files = list_undo_files(paths["undo_dir"])

    clear_screen()
    ui_title("🔁 UNDO HISTORY")
    ui_line()

    if not undo_files:
        ui_bad("No undo history found.")
        press_enter()
        return

    for i, f in enumerate(undo_files, start=1):
        print(f"{C_YELLOW}{i}){RESET} {f}")

    print(f"\n{C_BLUE}B){RESET} Back")
    print(f"{C_RED}0){RESET} Abort")
    ui_line()

    ch = safe_input("Select undo file: ").upper()
    if ch in ["0"]:
        return
    if ch == "B":
        return

    if ch.isdigit():
        idx = int(ch)
        if 1 <= idx <= len(undo_files):
            undo_file = os.path.join(paths["undo_dir"], undo_files[idx - 1])

            info = undo_preview(undo_file)
            ui_warn("\nUNDO PREVIEW ✅")
            ui_line()
            ui_info(f"Created: {info['created']}")
            ui_info(f"Total actions: {info['total']}")
            ui_info(f"Moves: {info['moves']}")
            ui_info(f"Renames: {info['renames']}")
            ui_line()

            confirm = safe_input("Type YES to apply UNDO: ").upper()
            if confirm == "YES":
                ok, msg = apply_undo(undo_file)
                if ok:
                    ui_good(msg)
                else:
                    ui_bad(msg)
                press_enter()
            return


# ============================================================
# ✅ MAIN APP 
# ============================================================
def main():
    IS_PRO, license_data = screen_license_gate()

    while True:
        ch = screen_main_menu()

        if ch == "0":
            ui_good("Bye bro ✅")
            break

        if ch == "B":
            IS_PRO, license_data = screen_license_gate()
            continue

        if ch == "3":
            profiles_menu(is_pro=IS_PRO)
            continue

        if ch == "4":
            duplicate_tools_menu(is_pro=IS_PRO)
            continue

        if ch == "5":
            undo_menu(is_pro=IS_PRO)
            continue

        if ch == "6":
            daily_automation_menu(license_data, IS_PRO)
            continue

        if ch in ["1", "2"]:
            settings = configure_flow(is_pro=IS_PRO)
            if settings in ["BACK", None]:
                continue

            # ✅ FIXED: Change Settings loops properly
            while True:
                prev = run_pipeline(settings, dry_run=True, is_pro=IS_PRO)

                go = screen_preview(
                    prev["rename_previews"],
                    prev["move_preview"],
                    settings["extras"],
                    prev["log_file"]
                )

                if go == "1":
                    if ch == "1":
                        ui_good("\nDry Run completed ✅ No changes made.")
                        press_enter()
                    else:
                        ui_warn("Starting REAL RUN...")
                        run_pipeline(settings, dry_run=False, is_pro=IS_PRO)
                    break

                elif go == "2":
                    settings = configure_flow(is_pro=IS_PRO)
                    if settings in ["BACK", None]:
                        break
                    continue

                else:
                    ui_warn("Aborted ❌")
                    press_enter()
                    break

            continue

# Finally, run the main app loop
if __name__ == "__main__":
    main()