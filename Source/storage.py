import os, time

from errors import error_handler

def check_storage(backup_size, free_space):
    os.system("cls")

    if free_space == None or backup_size == None:
        return None
    
    print("=== CHECKING AVAILABLE STORAGE ===\n")
    
    if free_space < backup_size*0.75:
        print("\nError 5: The target drive does not have enough storage space for the backup you are trying to perform. Free up space on the destination drive or reduce the size of the backup:\n")
        print(f"Minimum required storage: {backup_size*0.75:.1f} GB")
        print(f"Free Space: {free_space:.1f} GB\n")
        input("Press any key to close this program...")
        error_handler(5)
    elif backup_size*0.95 < backup_size < backup_size*0.75:
        print("\nThe available free storage space is not sufficient for the recommended size. Errors may occur during the backup process due to insufficient storage space:\n")
        print(f"Recommended free space: {backup_size*0.95:.1f} GB")
        print(f"Free Space: {free_space:.1f} GB\n")
        while True:
            choice = input("Do you want to continue anyway? (y/n): ").lower()

            if choice == "y":
                return round(free_space/backup_size, 2)
            elif choice == "n":
                while True:
                    ch = input("Are you sure you want to close the program? (y/n): ")

                    if ch == "y":
                        error_handler(-1)
                    elif ch == "n":
                        return round(free_space/backup_size, 2)
                    else:
                        print("Please type y or n.")
                        time.sleep(2)
                        continue
            else:
                print("Please type y or n.")
                time.sleep(2)
                continue

    return round(free_space/backup_size, 2)