import psutil, shutil, ctypes, os, sys
from datetime import datetime

from errors import error_handler

VERSION = 1.5
ARCH = 64

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

def show_progressbar(percent, eta=None):
    length = 40
    filled = int(length * percent / 100)
    bar = "#" * filled + "-" * (length - filled)
    if eta is not None:
        mins, secs = divmod(int(eta), 60)
        line = f"[{bar}] {percent:3d}%  ETA: {mins:02d}m {secs:02d}s"
    else:
        line = f"[{bar}] {percent:3d}%"
    sys.stdout.write("\r" + line + " " * 10)
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
