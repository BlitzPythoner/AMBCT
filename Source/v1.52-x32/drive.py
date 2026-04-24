import os

from globals import list_drives, get_folder_size
from errors import error_handler

def select_backup_drive():
    os.system("cls")
    print("=== SELECTING THE DRIVE TO BE BACKED UP ===\n")

    DRIVE = False

    drives = list_drives()
    if not drives:
        error_handler(4)

    for i, d in enumerate(drives, 1):
        print(f"[{i}] {d['drive']}:\\")
        print(f"Name: {d['name']}")
        print(f"Filesystem: {d['filesystem']}")
        print(f"Total: {d['total']} GB | Occupied: {d['occupied']} GB")
        print("-" * 40)
    
    print(f"[{len(drives)+1}] Enter custom path")
    while True:
        try:
            choice = int(input("\nSelect a drive number: "))
            if 1 <= choice <= len(drives):
                DRIVE = True
                selected = drives[choice - 1]
                source_drive = selected['drive']
                size = selected['occupied']
                return source_drive, size, DRIVE

            elif choice == len(drives)+1:
                while True: 
                    backup_path = input("\nType in a path to a Folder, what should be backed up: ")
                    if not os.path.exists(backup_path):
                        print("The path doesn't exist, make sure you typed the path correctly.")
                        continue
                    backup_size_folder = get_folder_size(backup_path)
                    return backup_path, backup_size_folder, DRIVE

            else:
                print("Invalid number, try again.")
                continue
        except ValueError:
            print("Please enter a valid number.")    
            continue

def select_save_drive():
    os.system("cls")
    print("=== SELECTING THE DRIVE WHERE THE BACKUP SHOULD BE STORED ===\n")

    drives = list_drives()
    if not drives:
        error_handler(4)

    for i, d in enumerate(drives, 1):
        print(f"[{i}] {d['drive']}:\\")
        print(f"Name: {d['name']}")
        print(f"Filesystem: {d['filesystem']}")
        print(f"Total: {d['total']} GB | Free: {d['free']} GB")
        print("-" * 40)
    while True:
        try:
            choice = int(input("\nSelect a drive number: "))
            if 1 <= choice <= len(drives):

                selected = drives[choice - 1]
                target_drive = selected['drive']
                target_free_space = selected['free']
                while True:
                    choice = input("\nDo you want also the specify a path in this drive, where the Backup should be stored? (Y/N): ").lower()
                    if choice == "y":
                        targetpath = input(f"Type in the path, letter is already included:\n{target_drive}:\\")
                        target_path = f"{target_drive}:\\{targetpath}"
                        if not os.path.exists(target_path):
                            print("The path doesn't exists, try again.")
                            continue
                        return target_path, target_free_space

                    elif choice == "n":
                        target_path = f"{target_drive}:\\"
                        return target_path, target_free_space

            else:
                print("Invalid number, try again.")
        except ValueError:
            print("Please enter a valid number.")    