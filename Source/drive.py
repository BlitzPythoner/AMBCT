import os

from globals import list_drives, get_folder_size, ask_path_gui, get_free_space
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
                    backup_path = ask_path_gui("folder", "Select the folder you want to be backed up.", None, None)
                    if not backup_path:
                        print("No path selected!\n")
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

    print(f"[{len(drives)+1}] Enter custom path")

    while True:
        try:
            choice = int(input("\nSelect a drive number: "))
            if 1 <= choice <= len(drives):

                selected = drives[choice - 1]
                target_drive = selected['drive']
                target_free_space = selected['free']
                target_path = f"{target_drive}:\\"
                return target_path, target_free_space

            elif choice == len(drives)+1:
                while True:
                    target_path = ask_path_gui("folder", ...)
                    if not target_path:
                        print("No path selected!\n")
                        continue
                    break

                drive_letter = target_path[0]  
                target_free_space = get_free_space(drive_letter)

                return target_path, target_free_space
            
            else:
                print("Invalid number, try again.")
        except ValueError:
            print("Please enter a valid number.")    