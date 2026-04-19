import os, re, subprocess, time

from globals import format_bytes, show_progressbar_small
from errors import error_handler

def delete_backup(wimlib_path, wim_path):
        os.system("cls")
        print("=== DELETING A BACKUP ===")
        try:
            result = subprocess.run(
                [wimlib_path, "info", wim_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                check=True
            )
            wim_output = result.stdout
        except Exception:
            error_handler(11)
        
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
        print("-"*60)
        print("\n**NOTE**: Deleting an index cannot be undone, use at you own risk!")
        while True:
            sel_idx = input("\nChoose an index what do you want to delete: ")
            if not sel_idx.strip():
                return 
            if not sel_idx.isdigit():
                print("Please enter a valid number.")
                continue
            print("\nDeleting an index removes part of your backup. This action cannot be undone!")
            confirm = input("Type in 'sure' for confirmation: ").lower()
            if confirm == "sure":
                break
            else:
                print("Confirmation not successful!")
                continue
        try:
            phase = ""
            command = [wimlib_path, "delete", wim_path, sel_idx]
            process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True,encoding="utf-8",errors="ignore")
            for raw_line in process.stdout:
                line = raw_line.strip()

                if "Archiving file data:" in line:
                    if phase != "delete":
                        phase = "delete"
                        print(f"\nDeleting Backup Index {sel_idx}...")
                    match = re.search(r"\((\d+)%\)", line)
                    if match:
                        percent = int(match.group(1))
                        show_progressbar_small(percent)
                    continue
                if "Calculating integrity table" in line:
                    if phase != "verify":
                        phase = "verify"
                        print("\n\nVerifying Integrity table of Backup...")
                    match = re.search(r"\((\d+)%\)", line)
                    if match:
                        percent = int(match.group(1))
                        show_progressbar_small(percent)
                    continue

            process.wait()
        except Exception:
            error_handler(13)

        print(f"\n\nDeleting of index {sel_idx} in {wim_path} was successful.")
        time.sleep(2)
        return 