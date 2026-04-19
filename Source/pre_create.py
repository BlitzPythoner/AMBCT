import os, time

from errors import error_handler

def c_pre_create_backup(backup_path, backup_size, DRIVE, target_path, free_space, compression, backup_name, CHECK, SOLID, SHUTDOWN, write_speed, WR):
    global source_path
    
    if backup_size*0.75 < free_space < backup_size*0.85:
        commentary = "The target drive has just barely space for the backup"
    elif backup_size*0.85 < free_space < backup_size*1:
        commentary = "The target drive has just enough space for the backup"
    elif backup_size*1.2 < free_space:
        commentary = "The target drive has enough space for the backup"
    if WR:
        if compression == "NONE":
            comp = write_speed*0.9
        elif compression == "XPRESS":
            comp = write_speed*0.4
        elif compression == "LZX":
            comp = write_speed*0.12
        elif compression == "LZMS":
            comp = write_speed*0.05
        else:
            comp = 250*0.4

        raw_eta = (backup_size*1024)/comp 
        eta_m = int(raw_eta // 60)
        eta_s = int(raw_eta % 60)
    else:
        eta_m = 0
        eta_s = 0

    os.system("cls")
    print("=== CHECK YOUR INFOS ===\n")
    print("That's all information we need, please check them below:\n")
    print(f"Mode: Creating Backup")
    print(f"Name of the backup: '{backup_name}' ")
    if DRIVE:
        print(f"Source drive/path: {backup_path}:\\ ")
    else:
        print(f"Source drive/path: {backup_path} ")
    print(f"Backup size (without compression): {backup_size:.1f} GB ")
    print(f"Target Drive/path: {target_path}")
    print(f"Free Space of target drive: {free_space:.1f} GB")
    print(f"Commentary: {commentary}")
    print("-"*80)
    print(f"Compression-Method: {compression}")
    print(f"CHECK = {CHECK}")
    print(f"SOLID = {SOLID}")
    print(f"SHUTDOWN = {SHUTDOWN}")
    print("-"*80)
    if WR:
        print(f"Write Speed, sequential: {write_speed:.1f} MB/s")
        print(f"Approximate backup time: {eta_m}m {eta_s}s")
        print("**NOTE** The time was only roughly calculated, only using the sequential write speed on your target drive.\nExact values depend on your computer hardware.\n")
    else:
        print("Write Speed was not successful recorded, additional infos are not avaiable\n")
    while True:
        choice = input("Has all the information been entered correctly according to your wishes? (Y/N): ").lower()

        if choice == "y":
            return eta_m, eta_s
        elif choice == "n":
            while True:
                ch = input("Are you sure you want to close this program? (y/n): ").lower()
                if ch == "y":
                    error_handler(-1)
                elif ch == "n":
                    return eta_m, eta_s
                else:
                    print("Please enter Y or N.")
                    time.sleep(2)
                    continue
        else:
            print("Please enter Y or N.")
            time.sleep(2)
            continue

def a_pre_create_backup(existing_backup_path, backup_path, backup_size, DRIVE, free_space, compression, backup_name, CHECK, SHUTDOWN, write_speed, WR):
    global source_path
    
    if backup_size*0.75 < free_space < backup_size*0.85:
        commentary = "The target drive has just barely space for the backup"
    elif backup_size*0.85 < free_space < backup_size*1:
        commentary = "The target drive has just enough space for the backup"
    elif backup_size*1.2 < free_space:
        commentary = "The target drive has enough space for the backup"
    if WR:
        if compression == "NONE":
            comp = write_speed*0.9
        elif compression == "XPRESS":
            comp = write_speed*0.4
        elif compression == "LZX":
            comp = write_speed*0.12
        elif compression == "LZMS":
            comp = write_speed*0.05
        else:
            comp = 250*0.4

        raw_eta = (backup_size*1024)/comp 
        eta_m = int(raw_eta // 60)
        eta_s = int(raw_eta % 60)
    else:
        eta_m = 0
        eta_s = 0

    os.system("cls")
    print("=== CHECK YOUR INFOS ===\n")
    print("That's all information we need, please check them below:\n")
    print(f"Mode: Appending Backup")
    print(f"Name of the backup: '{backup_name}' ")
    if DRIVE:
        print(f"Source drive/path: {backup_path}:\\ ")
    else:
        print(f"Source drive/path: {backup_path} ")
    print(f"Backup size (without compression): {backup_size:.1f} GB ")
    print(f"Target Drive/path: {existing_backup_path}")
    print(f"Free Space of target drive: {free_space:.1f} GB")
    print(f"Commentary: {commentary}")
    print("-"*80)
    print(f"Compression-Method: {compression}")
    print(f"CHECK = {CHECK}")
    print(f"SHUTDOWN = {SHUTDOWN}")
    print("-"*80)
    if WR:
        print(f"Write Speed, sequential: {write_speed:.1f} MB/s")
        print(f"Approximate backup time: {eta_m}m {eta_s}s")
        print("**NOTE** The time was only roughly calculated, only using the sequential write speed on your target drive.\nExact values depend on your computer hardware.\n")
    else:
        print("Write Speed was not successful recorded, additional infos are not avaiable\n")
    while True:
        choice = input("Has all the information been entered correctly according to your wishes? (Y/N): ").lower()

        if choice == "y":
            return eta_m, eta_s
        elif choice == "n":
            while True:
                ch = input("Are you sure you want to close this program? (y/n): ").lower()
                if ch == "y":
                    error_handler(-1)
                elif ch == "n":
                    return eta_m, eta_s
                else:
                    print("Please enter Y or N.")
                    time.sleep(2)
                    continue
        else:
            print("Please enter Y or N.")
            time.sleep(2)
            continue