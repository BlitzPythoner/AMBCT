# Main Code for AMBCT

import os, time, webbrowser

from globals import VERSION, get_free_space
from load import load
from errors import error_handler
from drive import select_backup_drive, select_save_drive
from storage import check_storage
from options import c_select_options, a_select_options
from write import write_test
from pre_create import c_pre_create_backup, a_pre_create_backup
from core import create_backup, append_backup
from thanks import thanks
from adrive import select_existing_backup
from img_config import image_configurator
from help import ambct_help

def main():
    os.system("cls")
    print(f"=== Automatic Manual Backup Creation Tool v{VERSION} === \n")
    print("Welcome to AMBCT. What do you want to do?\n")
    print("[1] Create a new backup")
    print("[2] Append an existing backup")
    print("[3] Configure an existing backup")
    print("[4] How to use this program properly\n")
    if update == 2:
        print("You are using the newest version.\n\nThis is most likely the last version of AMBCT x32. Starting with v1.6 and beyond, only x64 versions will be developed and released. If you want to use the latest updates for AMBCT, download the x64 version or upgrade your system.\n")
        print("[U] Visit website for newest version")
        print("[H] What if I can't upgrade?")
    print("[X] Exit AMBCT\n")

    while True:
        choice = input("Choose an option for what you'd like to do: ").lower()

        if choice == "1":
            # Create backup
            backup_path, backup_size, DRIVE = select_backup_drive()
            target_path, target_available_space = select_save_drive()
            storage_index = check_storage(backup_size, target_available_space, backup_path[0])
            compression, backup_name, CHECK, SOLID, SHUTDOWN = c_select_options(storage_index)
            # write_speed, WR = write_test(target_path)
            c_pre_create_backup(backup_path, backup_size, DRIVE, target_path, target_available_space, compression, backup_name, CHECK, SOLID, SHUTDOWN)
            create_backup(wimlib_path, backup_path, DRIVE, target_path, compression, backup_name, CHECK, SOLID, SHUTDOWN)
            thanks()

        elif choice == "2":
            # Append backup
            existing_backup_path, compression = select_existing_backup(wimlib_path)
            backup_path, backup_size, DRIVE = select_backup_drive()
            target_available_space = get_free_space(existing_backup_path[0])
            storage_index = check_storage(backup_size, target_available_space, backup_path[0])
            backup_name, CHECK, SHUTDOWN = a_select_options()
            # write_speed, WR = write_test(existing_backup_path)
            a_pre_create_backup(existing_backup_path, backup_path, backup_size, DRIVE, target_available_space, compression, backup_name, CHECK, SHUTDOWN)
            append_backup(wimlib_path, existing_backup_path, backup_path, DRIVE, compression, backup_name, CHECK, SHUTDOWN)
            thanks()

        elif choice == "3":
            # Image Configurator
            return image_configurator(wimlib_path)
        
        elif choice == "4":
            # AMBCT Help
            return ambct_help()
        
        elif choice == "u":
            webbrowser.open("https://github.com/BlitzPythoner/AMBCT/releases/latest")
            return main()
        
        elif choice == "h":
            print("\nYou can continue to use this version of AMBCT; as of April 2026, it is still up to date. However, no new bug fixes or features will be released for this architecture. This version is expected to be the last version for x32 AMBCT.")
            time.sleep(10)
            return main()
        
        elif choice == "x":
            error_handler(-1)
        else:
            print("Please select one of the options listed above.\n")
            time.sleep(2)
            continue

code, update, wimlib_path, version = load()
main()