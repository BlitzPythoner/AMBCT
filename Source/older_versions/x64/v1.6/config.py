import os, subprocess, re, time

from globals import format_bytes
from errors import error_handler

def config_backup_image(wimlib_path, wim_path):
        os.system("cls")
        print("Please wait...")
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

        os.system("cls")
        print("== WIM INFORMATION ==")

        compression = re.search(r"Compression:\s+(.+)", wim_output)
        chunk_size = re.search(r"Chunk Size:\s+(.+)", wim_output)
        file_size_bytes = os.path.getsize(wim_path)
        file_size_gb = format_bytes(file_size_bytes)

        if compression:
            print(f"Compression: {compression.group(1)}")
        if chunk_size:
            print(f"Chunk Size: {chunk_size.group(1)}")
        print(f"Size: {file_size_gb}")

        print("\n== IMAGE INFORMATION ==")

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
                            "or press Enter to go back to menu: ")
            if not sel_idx.strip():
                return 
            if not sel_idx.isdigit():
                print("Please enter a valid number.")
                continue
            break

        print("\n=== MODIFY IMAGE PROPERTIES ===\n")
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
            time.sleep(2)
            return 
        
        except Exception:
            error_handler(12)
            return 