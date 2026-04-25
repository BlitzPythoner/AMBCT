import os, subprocess, re

from globals import show_progressbar_small
from errors import error_handler

def check_backup(wimlib_path, wim_path):
        os.system("cls")
        print("=== VERIFYING BACKUP IMAGE ===\n")
        try:
            phase = ""
            command = [wimlib_path, "verify", wim_path]
            process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True,encoding="utf-8",errors="ignore")
            for raw_line in process.stdout:
                line = raw_line.strip()

                if "Verifying integrity of" in line:
                    if phase != "verify":
                        phase = "verify"
                        print("Verifying Integrity table of Backup...")
                    match = re.search(r"\((\d+)%\)", line)
                    if match:
                        percent = int(match.group(1))
                        show_progressbar_small(percent)
                    continue
                if "Verifying metadata for image" in line:
                    if phase != "verify-md":
                        phase = "verify-md"
                    match = re.search(r"Verifying metadata for image (\d+) of (\d+)", line)
                    if match:
                        current = int(match.group(1))
                        total = int(match.group(2))
                        print(f"\n\nVerifying metadata of index {current} of {total}:")
                if "Verifying file data" in line:
                    if phase != "verify":
                        phase = "verify"
                        print("\nVerifying file data of Backup...")
                    match = re.search(r"\((\d+)%\)", line)
                    if match:
                        percent = int(match.group(1))
                        show_progressbar_small(percent)

            process.wait()
        except Exception:
            error_handler(14)

        input(f"\n\nVerifying of {wim_path} was successful, no errors were found!\nPress Enter to continue...")
        return 