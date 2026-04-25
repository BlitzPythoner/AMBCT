import os, time

from errors import error_handler
from globals import normalize_path

def c_pre_create_backup(backup_path, backup_size, DRIVE, target_path, free_space, compression, backup_name, CHECK, SOLID, SHUTDOWN, cpu_speed, read_speed_source, write_speed_target):
    
    ETA = False
    commentary = "Unknown situation (logic gap)"

    if backup_size*0.75 < free_space < backup_size*0.85:
        commentary = "The target drive has just barely space for the backup"
    elif backup_size*0.85 < free_space < backup_size*1:
        commentary = "The target drive has just enough space for the backup"
    elif backup_size*1 <= free_space <= backup_size*1.2:
        commentary = "The target drive has sufficient space for the backup"
    elif backup_size*1.2 < free_space:
        commentary = "The target drive has more than enough space for the backup"
    
    if cpu_speed is not None and read_speed_source is not None and write_speed_target is not None:    
        ETA = True
        effective_speed = min(cpu_speed, read_speed_source, write_speed_target)

        eta_se = (backup_size * 1024) / effective_speed
        eta_h = int(eta_se // 3600)
        eta_m = int((eta_se % 3600) // 60)
        eta_s = int(eta_se % 60)

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
    if ETA:
        print("Advanced Information:\n")
        print(f"CPU Speed: {cpu_speed} MB/s")
        print(f"Read Source drive: {read_speed_source} MB/s")
        print(f"Write Target drive: {write_speed_target} MB/s")
        print(f"Effective Speed: {effective_speed} MB/s")
        print(f"Estimated Time for Backup Creation: {eta_h}h {eta_m}m {eta_s}s\n")
    else:
        print("No data regarding CPU speed and/or the drive could be measured.\n")
    while True:
        choice = input("Has all the information been entered correctly according to your wishes? (Y/N): ").lower()

        if choice == "y":
            return 
        elif choice == "n":
            while True:
                ch = input("Are you sure you want to close this program? (y/n): ").lower()
                if ch == "y":
                    error_handler(-1)
                elif ch == "n":
                    return 
                else:
                    print("Please enter Y or N.")
                    time.sleep(2)
                    continue
        else:
            print("Please enter Y or N.")
            time.sleep(2)
            continue

def a_pre_create_backup(existing_backup_path, backup_path, backup_size, DRIVE, free_space, compression, backup_name, CHECK, SHUTDOWN, cpu_speed, read_speed_source, write_speed_target):
    
    ETA = False
    commentary = "Unknown situation (logic gap)"

    if backup_size*0.75 < free_space < backup_size*0.85:
        commentary = "The target drive has just barely space for the backup"
    elif backup_size*0.85 < free_space < backup_size*1:
        commentary = "The target drive has just enough space for the backup"
    elif backup_size*1 <= free_space <= backup_size*1.2:
        commentary = "The target drive has sufficient space for the backup"
    elif backup_size*1.2 < free_space:
        commentary = "The target drive has more than enough space for the backup"
        
    if cpu_speed is not None and read_speed_source is not None and write_speed_target is not None:    
        ETA = True
        effective_speed = min(cpu_speed, read_speed_source, write_speed_target)

        eta_se = (backup_size * 1024) / effective_speed
        eta_h = int(eta_se // 3600)
        eta_m = int((eta_se % 3600) // 60)
        eta_s = int(eta_se % 60)

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
    if ETA:
        print("Advanced Information:\n")
        print(f"CPU Speed: {cpu_speed} MB/s")
        print(f"Read Source drive: {read_speed_source} MB/s")
        print(f"Write Target drive: {write_speed_target} MB/s")
        print(f"Effective Speed: {effective_speed} MB/s")
        print(f"Estimated Time for Backup Creation: {eta_h}h {eta_m}m {eta_s}s\n")
    else:
        print("No data regarding CPU speed and/or the drive could be measured.\n")
    while True:
        choice = input("Has all the information been entered correctly according to your wishes? (Y/N): ").lower()

        if choice == "y":
            return 
        elif choice == "n":
            while True:
                ch = input("Are you sure you want to close this program? (y/n): ").lower()
                if ch == "y":
                    error_handler(-1)
                elif ch == "n":
                    return 
                else:
                    print("Please enter Y or N.")
                    time.sleep(2)
                    continue
        else:
            print("Please enter Y or N.")
            time.sleep(2)
            continue