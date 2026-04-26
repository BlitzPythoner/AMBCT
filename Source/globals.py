import psutil, shutil, ctypes, os, sys, time, subprocess, re
from datetime import datetime
from tkinter import Tk, filedialog

from errors import error_handler

VERSION = 1.62
ARCH = 64
start_time = None
_last_eta_update = 0
_cached_eta = None

def get_volume_label(drive_letter):
    buf = ctypes.create_unicode_buffer(1024)
    try:
        ctypes.windll.kernel32.GetVolumeInformationW(
            ctypes.c_wchar_p(f"{drive_letter}:\\"),
            buf, 1024, None, None, None, None, 0
        )
    except Exception:
        return "No Label"
    return buf.value or "No Label"

def list_drives():
    drives = []
    for part in psutil.disk_partitions(all=False):
        drive_letter = part.device.replace("\\", "").rstrip(":")
        try:
            usage = shutil.disk_usage(part.mountpoint)
            drives.append({
                "drive": drive_letter,
                "name": get_volume_label(drive_letter),
                "filesystem": part.fstype,
                "total": round(usage.total / 1024**3, 2),
                "free": round(usage.free / 1024**3, 2),
                "occupied": round((usage.total - usage.free) / 1024**3, 2)
            })
        except (PermissionError, OSError):
            continue
    return drives

def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp) and os.path.exists(fp):
                try:
                    total_size += os.path.getsize(fp)
                    print(f"\rDiscovering files... [{round(total_size/1024**3, 1)} GB]  ", end="", flush=True)
                except (OSError, PermissionError):
                    pass
    return round(total_size / (1024**3), 2)

def is_ntfs(drive_letter):
        return os.path.exists(f"\\\\.\\{drive_letter.rstrip(':')}:\\$Extend")

def is_removable(drive_letter):
    path = f"{drive_letter.rstrip(':')}:\\"  
    drive_type = ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(path))
    return drive_type == 2

def show_progressbar(percent):
    global start_time, _last_eta_update, _cached_eta

    if start_time is None:
        start_time = time.time()
    
    if percent >= 100:
        _cached_eta = 0

    elapsed = time.time() - start_time

    length = 40
    filled = int(length * percent / 100)
    bar = "#" * filled + "-" * (length - filled)

    if percent >= 3:
        total = elapsed / (percent / 100)
        eta = total - elapsed

        now = time.time()

        if _cached_eta is None:
            _cached_eta = eta
            _last_eta_update = now
        elif now - _last_eta_update >= 1:
            alpha = 0.3
            _cached_eta = alpha * eta + (1 - alpha) * _cached_eta
            _last_eta_update = now

        eta_display = int(_cached_eta)

        h, r = divmod(eta_display, 3600)
        m, s = divmod(r, 60)

        eta_str = f"{h:02d}h {m:02d}m {s:02d}s"
        line = f"[{bar}] {percent:3d}%  ETA: {eta_str}"
    else:
        line = f"[{bar}] {percent:3d}%  ETA: calculating..."

    sys.stdout.write("\r" + line + " " * 5)
    sys.stdout.flush()

def log_event(log_file, message):
        timestamp = datetime.now().strftime("%H:%M:%S, %d.%m.%Y")
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"{message} at {timestamp}\n")

def get_free_space(drive_letter):
    drive_letter = drive_letter.upper().replace(":", "").strip()
    drives = list_drives()
    
    for d in drives:
        if d['drive'].upper() == drive_letter:
            return d['free']
            
    error_handler(10)
    return None

def format_bytes(num):
        num = float(num)
        if num >= 1024**4:
            return f"{num / (1024**4):.2f} TB"
        elif num >= 1024**3:
            return f"{num / (1024**3):.2f} GB"
        elif num >= 1024**2:
            return f"{num / (1024**2):.2f} MB"
        else:
            return f"{num:.0f} bytes"
        
def show_progressbar_small(percent):
        length = 40
        filled = int(length * percent / 100)
        bar = "#" * filled + "-" * (length - filled)
        sys.stdout.write(f"\r[{bar}] {percent:3d}%")
        sys.stdout.flush()

def normalize_path(path):

    path = str(path).strip()

    path = path.replace("/", "\\")

    if len(path) == 1 and path.isalpha():
        return f"{path}:\\"

    if len(path) == 2 and path[1] == ":":
        return f"{path}\\"

    return os.path.normpath(path)

def ask_path_gui(mode="folder", title="Select path", filetypes=None, default_ext=None):
    root = Tk()
    root.withdraw()

    path = None

    if mode == "folder":
        path = filedialog.askdirectory(title=title)

    elif mode == "file":
        path = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes or [("All files", "*.*")]
        )

    elif mode == "save":
        path = filedialog.asksaveasfilename(
            title=title,
            defaultextension=default_ext or "",
            filetypes=filetypes or [("All files", "*.*")]
        )

    root.destroy()
    return path

def get_drive_root(path):
    drive = os.path.splitdrive(path)[0]
    if not drive:
        return None
    return drive + "\\"

def get_file_size(path):
    try:
        if not os.path.isfile(path):
            return None

        size_bytes = os.path.getsize(path)
        size_gb = round(size_bytes / (1024**3), 2)

        return size_gb

    except (OSError, PermissionError):
        return None
    
def get_compression(wimlib_path, wim_path):
    try:
        result = subprocess.run(
            [wimlib_path, "info", wim_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            check=True
        )
        wim_output = result.stdout
        raw_compression = re.search(r"Compression:\s+(.+)", wim_output)
        existing_backup_compression = raw_compression.group(1)
    except Exception:
        error_handler(9)
    
    return existing_backup_compression

def get_compression_factor(old_comp, new_comp):
    rank = {
        "NONE": 1,
        "XPRESS": 2,
        "LZX": 3,
        "LZMS": 4
    }

    old = rank.get(old_comp.upper())
    new = rank.get(new_comp.upper())

    if old is None or new is None:
        return None, None

    diff = new - old

    if diff == 0:
        min_factor = 1.0
        rec_factor = 1.1

    elif diff == 1:
        min_factor = 0.85
        rec_factor = 0.95

    elif diff == 2:
        min_factor = 0.7
        rec_factor = 0.85

    elif diff >= 3:
        min_factor = 0.6
        rec_factor = 0.8

    elif diff == -1:
        min_factor = 1.1
        rec_factor = 1.25

    elif diff == -2:
        min_factor = 1.25
        rec_factor = 1.5

    elif diff <= -3:
        min_factor = 1.5
        rec_factor = 1.8

    return min_factor, rec_factor
