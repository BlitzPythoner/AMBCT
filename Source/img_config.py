import os, time

from globals import ask_path_gui, normalize_path
from config import config_backup_image
from delete import delete_backup
from check import check_backup

def image_configurator(wimlib_path):
    os.system("cls")
    print("=== IMAGE CONFIGURATOR ===\n")
    while True:
        wim_path = normalize_path(ask_path_gui("file", "Select the backup image you want to configure.", [("Backup Image files", "*.wim")]))
        
        if not wim_path:
            print("No path selected!\n")
            continue

        break

    while True:
        os.system("cls")
        print("=== IMAGE CONFIGURATOR ===\n")
        print(f"What do you want to do with your backup image?\nUsing: {wim_path}\n")
        print("[1] Change properties of the backup")
        print("[2] Delete a backup")
        print("[3] Check a backup")
        print("[X] Back to main menu\n")
        choice = input("Choose an action: ").lower()
        
        if choice == "1":
            config_backup_image(wimlib_path, wim_path)
        elif choice == "2":
            delete_backup(wimlib_path, wim_path)
        elif choice == "3":
            check_backup(wimlib_path, wim_path)
        elif choice == "x":
            from main import main
            return main()
        else:
            print("Invalid choice, try again.\n")
            time.sleep(2)
            continue
    
    