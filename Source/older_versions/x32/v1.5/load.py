# Prepare files, set paths

import sys, os, platform, tempfile, shutil, urllib.request
from globals import VERSION, ARCH
from errors import error_handler

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def update(current_version):
    version_url = "https://raw.githubusercontent.com/BlitzPythoner/AMBCT/main/version.txt"

    try:
        with urllib.request.urlopen(version_url, timeout=5) as response:
            online_version = response.read().decode().strip()
    except Exception:
        error_handler(3)

    local = current_version
    remote = float(online_version.strip())

    if local < remote:
        return 1, online_version
    elif local > remote:
        return 3, None
    else:
        return 2, None  

def load():
    print("\nChecking Architecture...\n")
    arch = platform.machine()
    if not str(ARCH) in arch:
        error_handler(1)

    temp_dir = os.path.join(tempfile.gettempdir(), "ambct_temp")
    os.makedirs(temp_dir, exist_ok=True)

    required_files = ["sources/wimlib-imagex.exe", "sources/libwim-15.dll"]

    temp_paths = {}
    for file in required_files:
        src = resource_path(file)
        if not os.path.exists(src):
            error_handler(2)

        print(f"Loading {file}...")
        dest = os.path.join(temp_dir, os.path.basename(file))
        shutil.copy(src, dest)
        temp_paths[file] = dest

    wimlib_path = temp_paths["sources/wimlib-imagex.exe"] 
    print("Files were successfully loaded!\n")
    
    print("Checking for updates...\n")
    upd_code, version = update(VERSION)

    return 0, upd_code, wimlib_path, version
