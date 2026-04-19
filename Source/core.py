import os, time, sys, subprocess, re
from datetime import datetime

from errors import error_handler
from globals import is_ntfs, is_removable, show_progressbar, log_event

def create_backup(wimlib_path, backup_path, DRIVE, target_path, compression, backup_name, CHECK, SOLID, SHUTDOWN, write_speed, WR, eta_m, eta_s):
    os.system("cls")
    
    log_file = os.path.join(target_path, f"{backup_name}_log.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        log.write("=== AMBCT LOG START ===\n\n")
        start_time = datetime.now().strftime("%H:%M:%S, %d.%m.%Y")
        log.write(f"Backup Creation started at: {start_time}\n")
        log.write("------------------------------------------------\n")

    output_file = os.path.join(target_path, f"{backup_name}.wim")
    args = [
        wimlib_path, "capture",
        backup_path,
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
        if is_ntfs(backup_path) and not is_removable(backup_path):
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
                    print(f"Scanning \"{backup_path}\"...")
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
                else:
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
            return 
        else:
            error_handler(7)

    except KeyboardInterrupt:
        log_event(log_file, "Backup cancelled by user")
        process.terminate()
        error_handler(-1)

    except Exception as e:
        log_event(log_file, f"Unexpected error: {e}")
        process.terminate()
        error_handler(8)

def append_backup(wimlib_path, existing_backup_path, backup_path, DRIVE, compression, backup_name, CHECK, SHUTDOWN, write_speed, WR):
    os.system("cls")
    
    log_file = os.path.join(os.path.dirname(existing_backup_path), f"{backup_name}_log.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        log.write("=== AMBCT LOG START ===\n\n")
        start_time = datetime.now().strftime("%H:%M:%S, %d.%m.%Y")
        log.write(f"Backup Creation started at: {start_time}\n")
        log.write("------------------------------------------------\n")

    
    args = [
            wimlib_path, "append",
            backup_path,
            existing_backup_path,
            f"{backup_name}",
            f"--compress={compression.lower()}",
            "--snapshot"
        ]
    if CHECK:
        args.append("--check")

    enable_snapshot = False
    if DRIVE:
        if is_ntfs(backup_path) and not is_removable(backup_path):
            enable_snapshot = True

    if not enable_snapshot and "--snapshot" in args:
        args.remove("--snapshot")

    print("=== APPENDING BACKUP ===\n")

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

                if "Verifying integrity of" in line:
                    if phase != "verify_existing":
                        log_event(log_file, "Verifying existing backup before appending")
                        print("Verifying integrity of existing backup...")
                        phase = "verify_existing"
                    match = re.search(r"\((\d+)%\)", line)
                    if match:
                        percent = int(match.group(1))
                        show_progressbar(percent)
                    continue

                if "scanned" in line and "Archiving" not in line:
                    if phase != "scan":
                        log_event(log_file, "Scanning started")
                        print(f"\n\nScanning \"{backup_path}\"...")
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
                        log_event(log_file, "Appending new backup image started")
                        print(f"\n\nAppending new backup image to \"{existing_backup_path}\"... This can take a while!\n")
                        phase = "backup"
                    match = re.search(r"Archiving file data:.*?\((\d+)%\)", line, re.IGNORECASE)
                    if match:
                        percent = int(match.group(1))
                        if percent > last_percent:
                            delta = time.time() - start_time
                            eta = (100 - percent) * (delta / max(1, percent - last_percent))
                            smoothed_eta = smoothed_eta * 0.8 + eta * 0.2 if smoothed_eta else eta
                            start_time = time.time() 
                            last_percent = percent
                        show_progressbar(percent, smoothed_eta)
                    continue

                if "Calculating integrity table" in line or "Verifying" in line:
                    if phase != "check":
                        log_event(log_file, "Append operation was successful")
                        with open(log_file, "a", encoding="utf-8") as log:
                            log.write("------------------------------------------------\n")
                        log_event(log_file, "Verifying new backup integrity")
                        print("\n\nVerifying appended backup integrity...\n")
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
                else:
                    log_event(log_file, "AMBCT was successful in Appending Backup")
                log.write("\n=== AMBCT LOG END ===\n")
            else:
                log_event(log_file, f"Backup failed (Exit code {process.returncode})")
                log.write("\n=== AMBCT LOG END ===\n")

        if process.returncode == 0:
            print(f"\n\nBackup completed successfully. Total time: {mins}m {secs:02d}s")
            if SHUTDOWN:
                print("System will shutdown in 10 seconds...")
                os.system("shutdown /s /t 10")
            input("\nBackup was appended successfully, press Enter to continue!")
            try:
                subprocess.run(["notepad.exe", log_file])
            except Exception as e:
                pass
            return 
        else:
            error_handler(7)

    except KeyboardInterrupt:
        log_event(log_file, "Backup cancelled by user")
        process.terminate()
        error_handler(-1)

    except Exception as e:
        log_event(log_file, f"Unexpected error: {e}")
        process.terminate()
        error_handler(8)