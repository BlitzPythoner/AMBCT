import os

from globals import VERSION

def ambct_help():
    os.system("cls")
    print("=== AMBCT HELP ===\n")
    print("1. Create a new Backup:\nIf you want to make a new backup for your system, specific folders, or external drives.\n")
    print("2. Appending an existing backup:\nIf you want to extend an existing backup image, a file can contain multiple backups.\n")
    print("3. Image Configurator:\n   3.1. Change properties of a backup:\n   This allows you to change the name, display name, or display description of a backup.\n\n   3.2. Delete a backup:\n   This allows you to delete individual backups in a backup image.\n\n   3.3. Check a backup:\n   This allows you to check your backup for integrity and errors.\n")
    print(f"AMBCT v{VERSION}:\nAMBCT is a command line-based tool that uses wimlib-imagex to create backups for entire systems, specific folders, or external drives. It is very easy to use. For more help, visit: https://blitzpythoner.github.io/AMBCT/\n")
    input("Press enter to get back to main menu...")
    from main import main
    return main()