import os, subprocess, re

from errors import error_handler
from globals import ask_path_gui

def select_existing_backup(wimlib_path):
    os.system("cls")
    global existing_backup_path
    print("=== APPENDING AN EXISTING BACKUP ===\n")
    while True:
        existing_backup_path = ask_path_gui("file", "Select the existing backup image file.", [("Backup image files", "*.wim")], ".wim")
        
        if not existing_backup_path:
            print("No path selected!\n")
            continue
        break
    try:
        result = subprocess.run(
            [wimlib_path, "info", existing_backup_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            check=True
        )
        wim_output = result.stdout
        raw_compression = re.search(r"Compression:\s+(.+)", wim_output)
        global existing_backup_compression
        existing_backup_compression = raw_compression.group(1)
    except Exception as e:
        error_handler(9)

    return existing_backup_path, existing_backup_compression
