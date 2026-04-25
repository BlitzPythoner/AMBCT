# Main Code for AMBCT

import os, time, webbrowser

from globals import VERSION, get_free_space, normalize_path
from load import load
from errors import error_handler
from drive import select_backup_drive, select_save_drive
from storage import check_storage
from options import c_select_options, a_select_options
from bench import benchmark
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
    if update == 1:
        print("[U] Visit website for update\n")
        print(f"A newer version of AMBCT is available. Current version: {VERSION}, Latest version: v{version}\n")
    if update == 2:
        print("You are using the newest version.\n")
    if update == 3:
        print("This version is currently under development.\n")
    if update == 4:
        print("It was not possible to check for updates.\n")
    print("[X] Exit AMBCT\n")

    while True:
        choice = input("Choose an option for what you'd like to do: ").lower()

        if choice == "1":
            # Create backup
            backup_path, backup_size, DRIVE = select_backup_drive()
            target_path, target_available_space = select_save_drive()
            storage_index = check_storage(backup_size, target_available_space, backup_path[0])
            compression, backup_name, CHECK, SOLID, SHUTDOWN = c_select_options(storage_index)
            cpu_speed, read_speed_source, write_speed_target = benchmark(wimlib_path, bench_path, normalize_path(backup_path), normalize_path(target_path), compression)
            c_pre_create_backup(backup_path, backup_size, DRIVE, target_path, target_available_space, compression, backup_name, CHECK, SOLID, SHUTDOWN, cpu_speed, read_speed_source, write_speed_target)
            create_backup(wimlib_path, normalize_path(backup_path), DRIVE, normalize_path(target_path), compression, backup_name, CHECK, SOLID, SHUTDOWN)
            thanks()

        elif choice == "2":
            # Append backup
            existing_backup_path, compression = select_existing_backup(wimlib_path)
            backup_path, backup_size, DRIVE = select_backup_drive()
            target_available_space = get_free_space(existing_backup_path[0])
            storage_index = check_storage(backup_size, target_available_space, backup_path[0])
            backup_name, CHECK, SHUTDOWN = a_select_options()
            cpu_speed, read_speed_source, write_speed_target = benchmark(wimlib_path, bench_path, normalize_path((backup_path)), normalize_path(existing_backup_path), compression)
            a_pre_create_backup(existing_backup_path, backup_path, backup_size, DRIVE, target_available_space, compression, backup_name, CHECK, SHUTDOWN, cpu_speed, read_speed_source, write_speed_target)
            append_backup(wimlib_path, normalize_path(existing_backup_path), normalize_path(backup_path), DRIVE, compression, backup_name, CHECK, SHUTDOWN)
            thanks()

        elif choice == "3":
            # Image Configurator
            return image_configurator(wimlib_path)
        
        elif choice == "4":
            # AMBCT Help
            return ambct_help()
        elif choice == "u" and update == 1:
            webbrowser.open("https://github.com/BlitzPythoner/AMBCT/releases/latest")
            return main()
        
        elif choice == "x":
            error_handler(-1)
        else:
            print("Please select one of the options listed above.\n")
            time.sleep(2)
            continue

code, update, wimlib_path, bench_path, version = load()
main()