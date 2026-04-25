import os, time

def c_select_options(storage_index):

    if not storage_index == None:
        if 1 < storage_index < 1.2:
            recommended_compression = "XPRESS"
        elif 0.85 < storage_index < 1:
            recommended_compression = "LZX"
        elif 0.75 < storage_index < 0.85:
            recommended_compression = "LZMS"

    os.system("cls")

    print("=== SELECTING COMPRESSION METHOD ===\n")
    print("Please select a compression method below:\n")
    print("[1] None - No Compression at all, is fast but needs just as much space")
    print("[2] XPRESS - Has light to medium compression, is also fast.")
    print("[3] LZX - Strong compression takes longer and requires moderate CPU power.")
    print("[4] LZMS - Strongest compression, lasts a long time, but saves a lot of space \n")
    print("If you need help, visit https://wimlib.net/compression.html for more detailed explainations.\n")
    if not storage_index == None and storage_index < 1.2:
        print(f"Based on your situation, we recommend using: {recommended_compression}")
    while True:
        choice = int(input("Select a number between 1 and 4 for compression selection: "))
        if choice == 1:
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
            time.sleep(2)
            continue

    os.system("cls")

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
            print("Your option is not available, there is 1, 2 and 3.")
            time.sleep(2)
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

    backup_name = input("\nGive a name for this backup: ")

    return compression, backup_name, CHECK, SOLID, SHUTDOWN

def a_select_options():
    os.system("cls")

    CHECK, SHUTDOWN = False, False
    print("=== SELECTING OTHER OPTIONS ===\n")
    print("You can add further options, select them below:\n")
    print("[0 - nothing] No other options, if you want it fast")
    print("[1 - check] Checks the integrety of the backup file at the end (recommended)")
    print("[2 - shutdown] Select it, if you want to shutdown your computer after the backup is created")
    print("Write your options like [12] or just 1, the program will detect it automatically.\n")
    while True:
        choice = input("Write your options here: ")

        if "0" not in choice and "1" not in choice and "2" not in choice:
            print("Your option is not available, there is 1 and 2.")
            time.sleep(2)
            continue
        if "0" in choice:
            break
        if "1" in choice:
            CHECK = True
        if "2" in choice:
            SHUTDOWN = True
        break

    backup_name = input("\nGive a name for this backup: ")

    return backup_name, CHECK, SHUTDOWN