import os, subprocess, re

from errors import error_handler

def write_test(target_path):
    letter = target_path[0]
    WR = False
    os.system("cls")
    print("=== MEASURING DISK SPEED ===\n")
    print("Measuring sequential disk write speed...")
    command = ["winsat", "disk", "-drive", letter, "-seq", "-write"]
    
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
            return write_speed, WR

        else:
            error_handler(6)
            return None, WR

    except Exception as e:
        return None, WR