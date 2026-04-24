import os, subprocess, re

from errors import error_handler
from globals import list_drives, get_folder_size

def select_existing_backup(wimlib_path):
    os.system("cls")
    global existing_backup_path
    print("=== APPENDING AN EXISTING BACKUP ===\n")
    while True:
        existing_backup_path = input("Type in the path to the existing backup file: ")
        ending = os.path.splitext(existing_backup_path)[1].lower()
        
        if not os.path.isfile(existing_backup_path):
            print("The path you specified, doesn't lead to a file.\n")
            continue

        if ending != ".wim":
            print("The path to file you specified, isn't a backup image file.\n")
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
