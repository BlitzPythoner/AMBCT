import os, subprocess, re, time

from globals import ask_path_gui, get_free_space, get_file_size, get_compression, get_compression_factor, show_progressbar, normalize_path
from errors import error_handler

from options import o_select_options

def optimize_backup(wimlib_path, wim_path):
    os.system("cls")

    print("=== OPTIMIZE A BACKUP ===\n")

    while True:
        target_path = ask_path_gui("save", "Select the path where the optimized backup image file should be saved.", [("Backup image files", "*.wim")], ".wim")
        if not target_path:
            print("No path selected!\n")
            continue

        if normalize_path(wim_path) == normalize_path(target_path):
            print("You can't replace the old backup image with the new one right away. Select a different path or change the name of the backup.")
            continue

        break
    
    result = get_file_size(wim_path)
    if result == None:
        error_handler(19)
    wim_size = result
    free_space = get_free_space(target_path[0])

    used_compression = get_compression(wimlib_path, wim_path)

    os.system("cls")
    print("=== OPTIMIZE A BACKUP ===\n")

    CHANGE_COMPRESSION = False
    compression = used_compression

    done = False

    while not done:
        choice = input("Would you like to change the compression method for your backup image? (y/n): ").lower()

        if choice == "y":
            comp_map = {
                "1": "NONE",
                "2": "XPRESS",
                "3": "LZX",
                "4": "LZMS"
            }
            print("\n== SELECTING COMPRESSION METHOD ==\n")
            print("Please select a compression method below:\n")
            print("[1] None - No Compression at all, is fast but needs just as much space")
            print("[2] XPRESS - Has light to medium compression, is also fast.")
            print("[3] LZX - Strong compression takes longer and requires moderate CPU power.")
            print("[4] LZMS - Strongest compression, lasts a long time, but saves a lot of space \n")
            print("If you need help, visit https://wimlib.net/compression.html for more detailed explainations.\n")
            print(f"You are currentl using: {used_compression}\n")

            while True:
                c_choice = input("Select compression: ")

                comp = comp_map.get(c_choice)
                if comp is None:
                    print("Invalid input")
                    continue

                compression = comp
                if comp != used_compression:
                    CHANGE_COMPRESSION = True

                done = True
                break

        elif choice == "n":
            compression = used_compression
            done = True

        else:
            print("Please type y or n.")
    
    break_all = False
    min_factor, rec_factor = 1, 1.1
    if CHANGE_COMPRESSION:
        min_factor, rec_factor = get_compression_factor(used_compression, compression)
    
    min_free_space = wim_size*min_factor
    rec_free_space = wim_size*rec_factor

    if free_space <= min_free_space:
        print("\nError 5: The target drive does not have enough storage space to optimize the backup image. Change the drive or increase the compression level so that the optimized backup image fits on your drive:\n")
        print(f"Minimum required storage: {min_free_space+1:.1f} GB")
        print(f"Free Space: {free_space:.1f} GB\n")
        input("Press any key to close this program...")
        error_handler(5)
    elif min_free_space < free_space < rec_free_space:
        print("\nThe available free storage space is not sufficient for the recommended size. Errors may occur during the backup process due to insufficient storage space:\n")
        print(f"Recommended free space: {rec_free_space:.1f} GB")
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
                        break_all = True
                        break
                    else:
                        print("Please type y or n.")
                        time.sleep(2)
                        continue

            elif break_all == True:
                break

            else:
                print("Please type y or n.")
                time.sleep(2)
                continue
    
    CHECK, SHUTDOWN = o_select_options()

    start_time = time.time()

    args = [
        wimlib_path, "export",
        wim_path,
        "all",
        target_path,
    ]
    if CHANGE_COMPRESSION:
        args.extend([
        f"--compress={compression.lower()}",
        "--recompress"
        ])
    if CHECK:
        args.append("--check")
    
    try:
        process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding="utf-8",
        errors="ignore"
        )

        phase = None

        for raw_line in process.stdout:
            line = raw_line.strip()

            if "Verifying integrity of" in line:
                if phase != "precheck":
                    print("\nVerifying existing image...")
                    phase = "precheck"

                match = re.search(r"\((\d+)%\)", line)
                if match:
                    percent = int(match.group(1))
                    show_progressbar(percent)

            elif "Archiving file data:" in line:
                if phase != "export":
                    print("\n\nOptimizing backup...\n")
                    phase = "export"

                match = re.search(r"\((\d+)%\)", line)
                if match:
                    percent = int(match.group(1))
                    show_progressbar(percent)

            elif "Calculating integrity table" in line:
                if phase != "postcheck":
                    print("\n\nFinalizing...\n")
                    phase = "postcheck"

                match = re.search(r"\((\d+)%\)", line)
                if match:
                    percent = int(match.group(1))
                    show_progressbar(percent)
        
        process.wait()
        total_time = time.time() - start_time
        mins, secs = divmod(int(total_time), 60)
        
        if process.returncode == 0:
            print(f"\n\nBackup optimized successfully. Total time: {mins}m {secs:02d}s")
            if SHUTDOWN:
                print("System will shutdown in 10 seconds...")
                os.system("shutdown /s /t 10")

            input("\nBackup was optimized successfully, press Enter to continue!")
            return
        
        else:
            error_handler(20)
    
    except KeyboardInterrupt:
        process.terminate()
        input("\nOptimizing backup was cancelled, program will automatically close in 5 seconds...")
        time.sleep(5)
    
    except Exception:
        process.terminate()
        error_handler(20)
    
