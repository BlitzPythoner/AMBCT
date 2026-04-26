import os, subprocess, re

from globals import ask_path_gui, get_compression

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

    return existing_backup_path, get_compression(wimlib_path, existing_backup_path)
