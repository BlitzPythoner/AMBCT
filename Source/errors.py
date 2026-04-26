import sys

def error_handler(code):
    if code == -1: # User-initiated program closure
        sys.exit(-1)
    if code == 1: # Serious error
        input("\nError 1: The architecture of this program does not match that of your processor. Please download the correct version of this program.\nPlease press any key to exit this program...")
        sys.exit(1)
    elif code == 2: # Serious error
        input("\nError 2: The files required for this program were not found. Please reinstall this program.\nPlease press any key to exit this program...")
        sys.exit(2)
    elif code == 3: # Minor error
        input("\nError 3: An internet connection could not be established to check for updates.\nPress any key continue anyway...")
        return
    elif code == 4: # Moderate error
        input("\nError 4: No drives were detected. Please connect a drive and restart the program. \nPress any key to close the program...")
        sys.exit(4)
    elif code == 5: # Special case: The error message is displayed in `check_storage()` for illustrative purposes.
        sys.exit(5)
    elif code == 6: # Minor error
        input("\nError 6: An error occurred while measuring the speed of your target drive. \nPress any key to skip this measurement...")
        return
    elif code == 7: # Moderate error
        input("\nError 7: The backup failed. Please restart the program, and if you encounter any further issues, please report them on my GitHub page. \nPress any key to close this program...")
        sys.exit(7)
    elif code == 8: # Moderate error
        input("\nError 8: An unexpected error occurred while creating or appending the backup. See the log for more information. \nPress any key to exit the program...")
        sys.exit(8)
    elif code == 9: # Moderate error
        input("\nError 9: An error occurred while reading the existing backup image. Please use a different backup image. \nPress any key to exit the program...")
        sys.exit(9)
    elif code == 10: # Minor error
        input("\nError 10: The available space on the drive where the existing backup file is located could not be determined. This may cause the backup to fail due to insufficient space. \nPress any key to continue anyway...")
        return
    elif code == 11: # Moderate error
        input("\nError 11: An error occurred while reading the backup file. Please use a different image and try again. \nPress any key to restart the program...")
        from main import main
        return main()
    elif code == 12: # Moderate error
        input("\nError 12: An error occurred while configuring the backup image. This image may be corrupted. Please use a different one or try again. \nPress any key to restart the program...")
        from main import main
        return main()
    elif code == 13: # Moderate error
        input("\nError 13: An error occurred while deleting a backup in the backup image. Please select a different backup image. \nPress any key to restart the program...")
        from main import main
        return main()
    elif code == 14: # Moderate error
        input("\nAn error occurred while verifying the backup. Please try again or use a different backup image. \nPress any key to restart the program...")
        from main import main
        return main()
    elif code == 15: # Minor error
        input("\nError 15: An error occurred while measuring CPU performance. The compression benchmark could not be completed.\nPress any key to continue anyway...")
        return
    elif code == 16: # Minor error
        input("\nError 16: An error occurred while measuring disk performance. The read or write speed test failed.\nPress any key to continue anyway...")
        return
    elif code == 17: # Minor error
        input("\nError 17: Low-level disk access failed during performance testing. Direct I/O could not be executed.\nPress any key to close this program...")
        sys.exit(17)
    elif code == 18: # Minor error
        input("\nError 18: The benchmark test file could not be created or accessed. The test file is missing or invalid.\nPress any key to continue anyway...")
        return
    elif code == 19: # Moderate error
        input("\nError 19: The size of the specified backup image could not be calculated. Please try again or select a different backup image to optimize. \nPress any key to restart the program...")
        from main import main
        return main()
    elif code == 20: # Moderate error
        input("\nError 20: An error occurred while optimizing the backup image. Please try again. If you encounter further errors, please visit my GitHub page. \nPress any key to close the program...")
        sys.exit(20)
        