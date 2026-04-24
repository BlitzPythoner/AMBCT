import os, time, re, subprocess, psutil

from errors import error_handler

def check_storage(backup_size, free_space, letter):
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
    elif backup_size*0.75 < backup_size < backup_size*0.95:
        print("\nThe available free storage space is not sufficient for the recommended size. Errors may occur during the backup process due to insufficient storage space:\n")
        print(f"Recommended free space: {backup_size*0.95:.1f} GB")
        print(f"Free Space: {free_space:.1f} GB\n")
        while True:
            choice = input("Do you want to continue anyway? (y/n): ").lower()

            if choice == "y":
                break
            elif choice == "n":
                while True:
                    ch = input("Are you sure you want to close the program? (y/n): ")

                    if ch == "y":
                        error_handler(-1)
                    elif ch == "n":
                        break
                    else:
                        print("Please type y or n.")
                        time.sleep(2)
                        continue
            else:
                print("Please type y or n.")
                time.sleep(2)
                continue

    if letter == "C":
        used, allocated, max = check_vss()
        if used == None:
            return round(free_space/backup_size, 2)
        
        vss_percent = max
        vss_index = round((psutil.disk_usage("C:\\").total * (vss_percent / 100)) / (1024**3), 2)

        if vss_index < 9:
            if vss_index <= 1:
                warn = "Your VSS Storage is extremly low:"
                message = "Backing up your system drive will most likely fail. To increase the VSS storage, you need to free up space on your system drive."
            elif 1 < vss_index <= 2.5:
                warn = "Your VSS Storage is very low:"
                message = "The backup of your system drive will likely fail. To increase the VSS storage, you need to free up space on your system drive."
            elif 2.5 < vss_index <= 6:
                warn = "Your VSS Storage is low:"
                message = "Backing up your system drive may fail. To increase the VSS storage, you need to free up space on your system drive."
            elif 6 < vss_index < 9:
                warn = "Your VSS Storage is moderate:"
                message = "There is a small chance that the backup of your system drive may fail. To increase the VSS storage even further, you need to free up space on your system drive."
            
            print(f"{warn}\nVSS creates a temporary snapshot of your system so even locked files can be backed up safely while Windows is running.\n{message}\n")

            while True:
                choice = input("Are you sure you want to continue anyway? (y/n): ").lower()

                if choice == "y":
                    break
                elif choice == "n":
                    error_handler(-1)
                else:
                    print("\nPlease type y or n.\n")
                    time.sleep(2)
                    continue

    return round(free_space/backup_size, 2)

def check_vss():
    try:
        result = subprocess.run(
            ["vssadmin", "list", "shadowstorage"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            errors="ignore"
        )

        output = result.stdout

        matches = re.findall(r"\((\d+)\s*%\)", output)

        if not matches:
            return None

        percents = [int(p) for p in matches]

        used = percents[0] if len(percents) > 0 else None
        allocated = percents[1] if len(percents) > 1 else None
        maximum = percents[2] if len(percents) > 2 else None

        return used, allocated, maximum

    except Exception:
        error_handler(15)
        return None, None, None