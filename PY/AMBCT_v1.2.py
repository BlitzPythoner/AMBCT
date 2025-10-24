import os, subprocess, platform, re, time, sys, shutil, atexit, tempfile, ctypes
from datetime import datetime

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)#

def cleanup_temp():
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception as e:
        sys.exit(-1)

def welcome():
    os.system("cls")
    print(f"=== Automatic Manual Backup Creation Tool {__version__} ===\n")
    print("Welcome!\nWith this Tool you can create backups for your system or other files.\nWhat do you want to do?\n")
    print("[1] Create a new backup")
    print("[2] Configure a backup")
    print("[X] More will be soon!\n")
    while True:
        choice = input("Choose a path: ")

        if choice == "1":
            return select_backup_drive()
        
        if choice == "2":
            return config_backup_image()
        
        else:
            print("Invalid option, try again.")
            continue

def select_backup_drive():
    os.system("cls")
    print("=== SELECTING THE DRIVE TO BE BACKED UP ===")
    drives = {}
    
    try:
        command = ["wmic", "logicaldisk", "get", "caption,volumename,size,freespace"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        wmic_output = result.stdout
        
    except FileNotFoundError:
        print("Error: 'wmic' not found. Make sure you are running on a Windows system and have wmic installed.\nIf you have Windows 11, install it via:\nDISM /Online /Add-Capability /CapabilityName:WMIC~~~~\nPress Enter to restart the program...")
        input()
        return welcome()
    
    lines = wmic_output.strip().split('\n')
    for line in lines[1:]:
        parts = line.strip().split()
        if not parts:
            continue

        caption = parts[0].strip(':')
        volume_name = "No Label"
        size_gb = "Unknown"
        free_gb = "Unknown"

        try:
            if len(parts) >= 4:
                free_bytes = int(parts[1])
                size_bytes = int(parts[2])
                volume_name = " ".join(parts[3:])
            elif len(parts) == 3:
                free_bytes = int(parts[1])
                size_bytes = int(parts[2])
            else:
                continue
            
            size_gb = round(size_bytes / (1024**3), 2)
            free_gb = round(free_bytes / (1024**3), 2)
            
        except ValueError:
            print(f"Error while parsing line: {line}")
            continue
        if caption:
            drives[caption] = {
                "name": volume_name,
                "size": f"{size_gb} GB",
                "free_space": f"{free_gb} GB"
            }

    if not drives:
        input("No drives were found. Plug in your storage media or create a partition and press Enter to restart the program...")
        return welcome()
        
    while True:
        print("\nSelect the drive you want to back up:\n")
        drive_list = list(drives.keys())
        
        for i, drive in enumerate(drive_list, 1):
            info = drives[drive]
            print(f"[{i}]")
            print(f"Name: {info['name']}")
            print(f"Size: {info['size']}")
            print(f"Free Space: {info['free_space']}")
            print(f"Drive Letter: {drive}:")
            print("-" * 20)
        try:
            selection = int(input(f"Enter the number of the drive, or type {i+1} to select a path. Press Enter to refresh: "))
            if 1 <= selection <= len(drive_list):
                global source_drive, size, free_space, DRIVE
                source_drive = drive_list[selection - 1]
                info = drives[source_drive]
                full_size = float(info["size"].split()[0].replace(",", "."))
                free_space = float(info["free_space"].split()[0].replace(",", "."))
                size = full_size - free_space
                DRIVE = True
                return select_backup_save_drive()
            elif selection == i+1:
                global backup_path
                while True: 
                    backup_path = input("\nType in a path to a Folder, what should be backed up: ")
                    if not os.path.exists(backup_path):
                        print("The path doesn't exist, make sure you typed the path correctly.")
                        continue
                    global backup_size_folder
                    backup_size_folder = get_folder_size(backup_path)
                    DRIVE = False
                    return select_backup_save_drive()

            else:
                print("Invalid selection. Please enter a valid number.")

        except ValueError:
            return select_backup_drive()

def config_backup_image():
    os.system("cls")
    print("=== SELECTING BACKUP IMAGE ===\n")
    while True:
        wim_path = input("Please enter the path to the backup image you want to configure: ")
        ending = os.path.splitext(wim_path)[1].lower()
        
        if not os.path.isfile(wim_path):
            print("The path you specified, doesn't lead to a file.\n")
            continue

        if ending != ".wim":
            print("The path to file you specified, isn't a backup image file.\n")
            continue
        
        break
    os.system("cls")
    try:
        result = subprocess.run(
            [wimlib_path, "info", wim_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            check=True
        )
        wim_output = result.stdout
    except Exception as e:
        input(f"Error while executing wimlib-imagex: {e}\nPress any key to go back to main menu...")
        return welcome()

    def format_bytes(num):
        num = float(num)
        if num >= 1024**4:
            return f"{num / (1024**4):.2f} TB"
        elif num >= 1024**3:
            return f"{num / (1024**3):.2f} GB"
        elif num >= 1024**2:
            return f"{num / (1024**2):.2f} MB"
        else:
            return f"{num:.0f} bytes"

    print("=== WIM INFORMATION ===")

    compression = re.search(r"Compression:\s+(.+)", wim_output)
    chunk_size = re.search(r"Chunk Size:\s+(.+)", wim_output)
    file_size_bytes = os.path.getsize(wim_path)
    file_size_gb = format_bytes(file_size_bytes)

    if compression:
        print(f"Compression: {compression.group(1)}")
    if chunk_size:
        print(f"Chunk Size: {chunk_size.group(1)}")
    print(f"Size: {file_size_gb}")

    print("\n=== IMAGE INFORMATION ===")

    images = [i.strip() for i in re.split(r"\n(?=Index:\s+\d+)", wim_output) if i.strip()]

    for img in images:
        index = re.search(r"Index:\s+(\d+)", img)
        if not index:
            continue
        if index.group(1) == "0":
            continue
        name = re.search(r"Name:\s+(.+)", img)
        display_name = re.search(r"Display Name:\s+(.+)", img)
        display_desc = re.search(r"Display Description:\s+(.+)", img)
        total_bytes = re.search(r"Total Bytes:\s+([\d]+)", img)
        creation_time = re.search(r"Creation Time:\s+(.+)", img)
        mod_time = re.search(r"Last Modification Time:\s+(.+)", img)
        arch = re.search(r"Architecture:\s+(.+)", img)
        major = re.search(r"Major Version:\s+(\d+)", img)
        minor = re.search(r"Minor Version:\s+(\d+)", img)
        build = re.search(r"Build:\s+(\d+)", img)

        print("-" * 60)
        print(f"Index: {index.group(1)}")
        if name:
            print(f"Name: {name.group(1)}")
        if display_name:
            print(f"Display Name: {display_name.group(1)}")
        if display_desc:
            print(f"Display Description: {display_desc.group(1)}")
        if total_bytes:
            print(f"Total Size: {format_bytes(total_bytes.group(1))}")
        if creation_time:
            print(f"Created: {creation_time.group(1)}")
        if mod_time:
            print(f"Modified: {mod_time.group(1)}")
        if arch:
            print(f"Architecture: {arch.group(1)}")

        if major and minor:
            major_v = int(major.group(1))
            minor_v = int(minor.group(1))
            version = "Unknown"
            if major_v == 10 and minor_v == 0:
                version = "Windows 10 / 11"
            elif major_v == 6 and minor_v == 3:
                version = "Windows 8.1"
            elif major_v == 6 and minor_v == 2:
                version = "Windows 8"
            elif major_v == 6 and minor_v == 1:
                version = "Windows 7"
            elif major_v == 6 and minor_v == 0:
                version = "Windows Vista"
            elif major_v == 5 and minor_v == 1:
                version = "Windows XP"
            print(f"Windows Version: {version}")

        if build:
            print(f"Build: {build.group(1)}")

    while True:
        sel_idx = input("\nChoose an index where you want to change something "
                        "or press Enter to go back to main menu: ")
        if not sel_idx.strip():
            return welcome()
        if not sel_idx.isdigit():
            print("Please enter a valid number.")
            continue
        break

    os.system("cls")
    print("=== MODIFY IMAGE PROPERTIES ===\n")
    print("What do you want to change?\n")
    print("[1] Name")
    print("[2] Display Name")
    print("[3] Display Description\n")

    while True:
        choice = input("Choose a number between 1 and 3: ").strip()
        if choice not in ["1", "2", "3"]:
            print("Please select a number between 1 and 3.")
            continue
        break

    prop_map = {
        "1": "NAME",
        "2": "DISPLAYNAME",
        "3": "DISPLAYDESCRIPTION"
    }
    prop_name = prop_map[choice]

    while True:
        new_value = input(f"Type in the new value for {prop_name}: ").strip()
        if not new_value:
            print("No value entered, please try again.")
            continue
        break
    try:
        command = [
            wimlib_path, "info", wim_path, sel_idx,
            "--image-property", f"{prop_name}={new_value}"
        ]
        print(f"Changing {prop_name}... This may take a while depending on the size of your backup.")
        subprocess.run(command, check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print(f"\n{prop_name} was successfully set to: {new_value}")
    except Exception as e:
        input(f"\nError while changing value on backup image:\n{e}\n"
            "Press Enter to go back to main menu...")
        return welcome()

    time.sleep(3)
    return welcome()

def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp) and os.path.exists(fp):
                try:
                    total_size += os.path.getsize(fp)
                    print(f"\rDiscovering files... [{round(total_size/1024**3, 1)} GB]  ", end="", flush=True)
                except (OSError, PermissionError):
                    pass
    return round(total_size / (1024**3), 2)

def select_backup_save_drive():
    os.system("cls")
    print("=== SELECTING THE DRIVE WHERE THE BACKUP SHOULD BE STORED ===\n")

    try:
        result = subprocess.run(
            ["wmic", "logicaldisk", "get", "caption,volumename,size,freespace"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, check=True
        )
    except Exception as e:
        print(f"Error: {e}")
        return -1

    drives = {}
    for line in result.stdout.strip().split("\n")[1:]:
        parts = line.split()
        if len(parts) < 3:
            continue

        caption = parts[0]
        free = parts[1]
        size = parts[2]
        name = " ".join(parts[3:]) if len(parts) > 3 else "No Label"

        try:
            drives[caption] = {
                "name": name,
                "size": round(int(size) / (1024**3), 2),
                "free": round(int(free) / (1024**3), 2)
            }
        except ValueError:
            continue

    if not drives:
        input("No drives found. Press Enter to exit...")
        return

    for i, (d, info) in enumerate(drives.items(), 1):
        print(f"[{i}] {d}\nName: {info['name']}\nFree: {info['free']:.1f} GB\nSize: {info['size']:.1f} GB")
        print("-"*40)

    while True:
        try:
            sel = int(input("\nSelect drive where the backup should be stored: "))
            if 1 <= sel <= len(drives):
                chosen = list(drives.keys())[sel - 1]
                global target_path, target_size, target_free_space, target_drive
                target_drive = chosen.replace(":", "")  
                target_size = drives[chosen]["size"]
                target_free_space = drives[chosen]["free"]

                while True:
                    choice = input("\nDo you want also the specify a path in this drive, where the Backup should be stored? (Y/N): ").lower()

                    if choice == "y":
                        targetpath = input(f"Type in the path, letter is already included:\n{target_drive}:\\")
                        target_path = f"{target_drive}:\\{targetpath}"
                        if not os.path.exists(target_path):
                            print("The path doesn't exists, try again.")
                            continue
                        return check_storage()
                    elif choice == "n":
                        target_path = f"{target_drive}:\\"
                        return check_storage()
                    else:
                        print("Invalid choice, try again.")
                        continue
        except ValueError:
            pass
        print("Invalid selection.")

def check_storage():
    os.system("cls")
    print("=== CHECKING AVAILABLE STORAGE ===\n")
    if DRIVE == True:
        space = size
    else:
        space = backup_size_folder

    if space*(0.6 if DRIVE == True else 0.8) >= target_free_space:
        print("We detected that your target drive has not enough Free Space and the backup cannot be created on your target drive:\n")
        print(f"Free Space on target drive: {target_free_space} GB")
        print(f"Recommended free space: min. {space*(0.6 if DRIVE == True else 0.8):.1f} GB, optimal: {space+5:.1f} GB\n")
        input("Press Enter to close this program...")
        cleanup_temp()
        sys.exit(-1)
    elif space*(0.6 if DRIVE == True else 0.8) < target_free_space < space+5:
        print("We detected that your target drive doesn't meet the optimal requirement for backup creation:\n")
        print(f"Free Space on target drive: {target_free_space} GB")
        print(f"Optimal Free Space (e.g without compression): {space+5:.1f} GB.")
        print(f"**NOTE**: With compression your target drive meets the optimal requirement.\n")
        while True: 
            choice = input(f"Do you want to continue anyways? (Y/N): ").lower()

            if choice == "n":
                return welcome()
            elif choice == "y":
                break
            else:
                print("Invalid option, try again.")
                continue
    return select_compression()

def select_compression():
    os.system("cls")
    print("=== SELECTING COMPRESSION METHOD ===\n")
    print("Please select a compression method below:\n")
    print("[1] None - No Compression at all, is fast but needs just as much space")
    print("[2] XPRESS - Has light to medium compression, is also fast.")
    print("[3] LZX - Strong compression takes longer and requires moderate CPU power.")
    print("[4] LZMS - Strongest compression, lasts a long time, but saves a lot of space ")
    print("If you need help, visit https://wimlib.net/compression.html for more detailed explainations.\n")
    while True:
        choice = int(input("Select a number between 1 and 4 for compression selection: "))
        if choice == 1:
            global compression 
            compression = "NONE"
            break
        elif choice == 2:
            compression = "XPRESS"
            break
        elif choice == 3:
            compression = "LZX"
            break
        elif choice == 4:
            compression = "LZMS"
            break
        else:
            print("Invalid choice, try again.")
            continue
    return select_other_options()

def select_other_options():
    os.system("cls")
    global CHECK, SOLID, SHUTDOWN
    CHECK, SOLID, SHUTDOWN = False, False, False
    print("=== SELECTING OTHER OPTIONS ===\n")
    print("You can add further options, select them below:\n")
    print("[0 - nothing] No other options, if you want it fast")
    print("[1 - check] Checks the integrety of the backup file at the end (recommended)")
    print("[2 - solid] Stores backups in blocks, increases compression, but access to individual files is not possible quickly")
    print("[3 - shutdown] Select it, if you want to shutdown your computer after the backup is created")
    print("Write your options like [12] or just 1, the program will detect it automatically.\n")
    while True:
        choice = input("Write your options here: ")

        if "0" not in choice and "1" not in choice and "2" not in choice and "3" not in choice:
            print("Your option is not available, there is 1 and 2 only yet.")
            continue
        if "0" in choice:
            break
        if "1" in choice:
            CHECK = True
        if "2" in choice:
            SOLID = True 
        if "3" in choice:
            SHUTDOWN = True
        break
    global backup_name
    backup_name = input("Please enter the name for the backup, that will be created: ")
    return write_test()

def write_test():
    global WR 
    WR = False
    os.system("cls")
    print("=== MEASURING DISK SPEED ===\n")
    print("Measuring sequential disk write speed...")
    command = ["winsat", "disk", "-drive", target_drive, "-seq", "-write"]
    
    try:
        result = subprocess.run(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding="mbcs",
                                universal_newlines=True,
                                errors="ignore",
                                check=True)
        winsat_output = result.stdout

        pattern = re.compile(r"(Sequential|Sequentiell)\s+64\.0\s+(Write|Schreiben)\s+([\d\.,]+)\s+MB/s")

        match = pattern.search(winsat_output)
        if match:
            speed_str = match.group(3).replace(",", ".")
            write_speed_mbps = float(speed_str)
            global write_speed
            write_speed = write_speed_mbps
            WR = True 
            pre_create_backup()

        else:
            input("Error while measuring write speed, press any key to continue anyways...")
            pre_create_backup()

    except Exception as e:
        print(f"Error while measuring speed test... {e}\nPress Enter to restart the program...")
        input()
        return welcome()

def pre_create_backup():
    global source_path
    if DRIVE:
        space = size
        source_path = source_drive
    else:
        space = backup_size_folder
        source_path = backup_path

    if space*0.7 < target_free_space < space*0.9:
        commentary = "The target drive has just barely space for the backup"
    elif space*0.9 < target_free_space < space*1.1:
        commentary = "The target drive has just enough space for the backup"
    elif space*1.1 < target_free_space:
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

        raw_eta = (space*1024)/comp 
        eta_m = int(raw_eta // 60)
        eta_s = int(raw_eta % 60)

    os.system("cls")
    print("=== CHECK YOUR INFOS ===\n")
    print("That's all infos we need, please check them below:\n")
    print(f"Name of the backup: '{backup_name}' ")
    print(f"Source drive/path: {normalize_source_path(source_path)} ")
    print(f"Backup size (without compression): {space:.1f} GB ")
    print(f"Target Drive/path: {target_path}")
    print(f"Free Space of target drive: {target_free_space:.1f} GB")
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
            return create_backup()
        elif choice == "n":
            return welcome()
        else:
            print("Please enter Y or N.")
            continue

def normalize_source_path(path):
        if re.fullmatch(r"[A-Za-z]:?", path.strip()):
            return f"{path.rstrip(':')}:\\"
        return path.rstrip("\\/")

def create_backup():
    os.system("cls")

    def is_ntfs(drive_letter):
        return os.path.exists(f"\\\\.\\{drive_letter.rstrip(':')}:\\$Extend")

    def is_removable(drive_letter):
        path = f"{drive_letter.rstrip(':')}:\\"  
        drive_type = ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(path))
        return drive_type == 2

    def show_progressbar(percent, eta=None):
        length = 40
        filled = int(length * percent / 100)
        bar = "#" * filled + "-" * (length - filled)
        if eta is not None:
            mins, secs = divmod(int(eta), 60)
            line = f"[{bar}] {percent:3d}%  ETA: {mins:02d}m {secs:02d}s"
        else:
            line = f"[{bar}] {percent:3d}%"
        sys.stdout.write("\r" + line + " " * 10)
        sys.stdout.flush()
    
    def log_event(log_file, message):
        timestamp = datetime.now().strftime("%H:%M:%S, %d.%m.%Y")
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"{message} at {timestamp}\n")
    
    log_file = os.path.join(target_path, f"{backup_name}_log.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        log.write("=== AMBCT LOG START ===\n\n")
        start_time = datetime.now().strftime("%H:%M:%S, %d.%m.%Y")
        log.write(f"Backup Creation started at: {start_time}\n")
        log.write("------------------------------------------------\n")

    output_file = os.path.join(target_path, f"{backup_name}.wim")
    args = [
        wimlib_path, "capture",
        normalize_source_path(source_path),
        output_file,
        f"{backup_name}",
        f"--compress={compression.lower()}",
        "--snapshot"
    ]

    if CHECK:
        args.append("--check")
    if SOLID:
        args.append("--solid")

    enable_snapshot = False
    if DRIVE:
        if is_ntfs(source_drive) and not is_removable(source_drive):
            enable_snapshot = True

    if not enable_snapshot and "--snapshot" in args:
        args.remove("--snapshot")

    print("=== CREATING BACKUP ===\n")

    start_time = time.time()
    last_percent = 0
    smoothed_eta = 0
    phase = None

    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding="utf-8",
        errors="ignore"
    )

    try:
        for raw_line in process.stdout:
            line = raw_line.strip()

            if "scanned" in line and "Archiving" not in line:
                if phase != "scan":
                    log_event(log_file, "Scanning started")
                    print(f"Scanning \"{normalize_source_path(source_path)}\"...")
                    phase = "scan"
                match = re.search(r"([\d\.]+)\s+([KMGT]i?B)\s+scanned", line)
                if match:
                    scanned_value = match.group(1)
                    scanned_unit = match.group(2)
                    sys.stdout.write(f"\rScanned: {scanned_value} {scanned_unit}... ")
                    sys.stdout.flush()
                continue

            if "Archiving file data:" in line:
                if phase != "backup":
                    log_event(log_file, f"Successfully scanned {scanned_value} {scanned_unit}")
                    with open(log_file, "a", encoding="utf-8") as log:
                        log.write("------------------------------------------------\n")
                    log_event(log_file, "Creation of Backup started")
                    print(f"\n\nSaving Backup in \"{target_path}\"... This can take a while!\n")
                    phase = "backup"

                match = re.search(r"Archiving file data:.*?\((\d+)%\)", line, re.IGNORECASE)
                if match:
                    percent = int(match.group(1))
                    if percent > last_percent:
                        delta = time.time() - start_time
                        eta = (100 - percent) * (delta / max(1, percent - last_percent))
                        smoothed_eta = smoothed_eta * 0.7 + eta * 0.3 if smoothed_eta else eta
                        last_percent = percent
                    show_progressbar(percent, smoothed_eta)
                continue

            if "Calculating integrity table" in line or "Verifying" in line:
                if phase != "check":
                    log_event(log_file, "Backup Creation was successful")
                    with open(log_file, "a", encoding="utf-8") as log:
                        log.write("------------------------------------------------\n")
                    log_event(log_file, "Verifying started")
                    print("\n\nVerifying backup integrity...\n")
                    phase = "check"
                match = re.search(r"\((\d+)%\)", line)
                if match:
                    percent = int(match.group(1))
                    show_progressbar(percent)
                continue

        process.wait()
        total_time = time.time() - start_time
        mins, secs = divmod(int(total_time), 60)

        with open(log_file, "a", encoding="utf-8") as log:
            log.write("------------------------------------------------\n")
            if process.returncode == 0:
                if CHECK:
                    log_event(log_file, "Verifying was successful")
                if SHUTDOWN:
                    log_event(log_file, "Shutdown of Computer was successful")
                log_event(log_file,"AMBCT was successful in Creating Backup")
                log.write("\n=== AMBCT LOG END ===\n")
            else:
                log_event(log_file, f"Backup failed (Exit code {process.returncode})")
                log.write("\n=== AMBCT LOG END ===\n")

        if process.returncode == 0:
            print(f"\n\nBackup completed successfully. Total time: {mins}m {secs:02d}s")
            if SHUTDOWN:
                print("System will shutdown in 10 seconds...")
                os.system("shutdown /s /t 10")
            input("\nBackup was created successfully, press Enter to continue!")
            try:
                subprocess.run(["notepad.exe", log_file])
            except Exception as e:
                pass
            return thanks()
        else:
            input(f"\n\nBackup failed (Exit code {process.returncode}).\nPress Enter to go back to main menu...")
            return welcome()

    except KeyboardInterrupt:
        log_event(log_file, "Backup cancelled by user")
        print("\nBackup cancelled by user.")
        process.terminate()

    except Exception as e:
        log_event(log_file, f"Unexpected error: {e}")
        print(f"\nUnexpected error during backup: {e}")
        process.terminate()

def thanks():
    os.system("cls")
    print(f"Thank you for using AMBCT - Automatic Manual Backup Creation Tool\nfor Backup-Creation!\nMore updates will come soon, stay tuned\nAMBCT {__version__} - by BlitzPythoner.\n")
    input("Press any key to get back to main menu...")
    return welcome()

os.system("cls")
__version__ = "v1.2"
arch = platform.machine()

temp_dir = os.path.join(tempfile.gettempdir(), "ambct_temp")
os.makedirs(temp_dir, exist_ok=True)

required_files = ["sources/wimlib-imagex.exe", "sources/libwim-15.dll"]

temp_paths = {}
for file in required_files:
    src = resource_path(file)
    if not os.path.exists(src):
        print(f"Required file missing: {file}")
        input("Press Enter to exit...")
        sys.exit(0)

    print(f"Loading {file}...")
    dest = os.path.join(temp_dir, os.path.basename(file))
    shutil.copy(src, dest)
    temp_paths[file] = dest

global wimlib_path
wimlib_path = temp_paths["sources/wimlib-imagex.exe"] 

atexit.register(cleanup_temp)
print("\nFiles were successfully loaded.")

time.sleep(1)
welcome()