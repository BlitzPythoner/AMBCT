# AMBCT – Automatic Manual Backup Creation Tool

**Author:** BlitzPythoner  
**Version:** 1.2
**Language:** Python 3.6+  
**OS Support:** Windows Vista, 7, 8.x, 10, 11  
**Architecture:** x64 and x86 (x32)  

---

## Description

AMBCT (Automatic Manual Backup Creation Tool) is a command-line based backup utility that uses **wimlib-imagex** for creating reliable and highly compressed system or file backups.  
It allows users to select drives or folders, define a target location, choose compression methods, and manage advanced options like integrity checks or automatic shutdown.

This tool combines automation and manual control – perfect for users who want efficiency **without losing control** over how their backups are created.

---

## Backup Creation Features

- **Automatic Drive Detection:** Automatically lists all connected drives with volume names, sizes, and available space.  
- **Flexible Backup Sources:** Create backups from entire drives or custom folders.  
- **Custom Destination Paths:** Select any target drive or specify a subfolder for storing backups.  
- **Smart Storage Check:** Warns if the destination has insufficient free space and suggests optimal requirements.  
- **Advanced Compression Methods:**  
  - `NONE` – No compression, fastest speed.  
  - `XPRESS` – Balanced performance and size.  
  - `LZX` – High compression, moderate CPU load.  
  - `LZMS` – Maximum compression, minimal size, longest time.  
- **Optional Backup Flags:**  
  - `check` – Verifies backup integrity after completion.  
  - `solid` – Increases compression by combining file data into solid blocks.  
  - `shutdown` – Powers off the system automatically after the process finishes.  
- **Write Speed Benchmark:** Runs a **WinSAT** test to measure target drive performance before backup.  
- **ETA Prediction:** Calculates approximate backup time using real write speed data.  
- **Dynamic Progress Bar:** Displays live percentage and time estimation during the backup.  
- **VSS Snapshot Support:** Uses Windows Volume Shadow Copy on NTFS drives to ensure safe captures of active systems.  
- **Robust Error Handling:** Detects missing dependencies, permission issues, and low-space conditions.  
- **Automatic Cleanup:** Removes temporary files and restores system state on exit.  
- **Detailed Overview:** Shows all user selections and settings for confirmation before starting the backup.
- - **Backup Logging:** Automatically creates a detailed `*_log.txt` file with timestamps for each backup process. 

---

## Backup Configuration Features

- **WIM Image Management:** Open and inspect existing `.wim` backup files.  
- **Detailed Metadata View:** Displays compression type, chunk size, file size, creation time, and Windows build info.  
- **Edit Backup Information:**  
  - Change **Name**  
  - Change **Display Name**  
  - Change **Display Description**  
- **Multi-Index Support:** View and modify multiple images within one WIM file.  
- **Safe Editing:** Uses `wimlib-imagex` with direct property modification — no data extraction required.  
- **Version Detection:** Automatically identifies Windows versions (XP → 11) inside captured images.

---

## Requirements

- **Administrator privileges** (required for disk and shadow copy access)  
- **Python 3.6 or higher**  
- **Windows Vista or later**  
- **wimlib-imagex** and **libwim-15.dll** (included in `sources/` folder)  
- **WinSAT** (included in most Windows versions)  
- If you using the .exe all you need is to execute the program (:

---

## How It Works

1. **Drive Detection:**  
   AMBCT scans and lists all available drives with names, sizes, and free space.  

2. **Source Selection:**  
   The user selects either an entire drive or a specific folder to back up.  

3. **Destination Selection:**  
   A target drive (and optional subfolder) is chosen as the backup destination.  

4. **Storage & Compression Check:**  
   AMBCT verifies available space and prompts the user to choose a compression method.  

5. **Performance Benchmark:**  
   A write-speed test using **WinSAT** measures target drive performance to improve ETA accuracy.  

6. **Pre-Backup Summary:**  
   All chosen settings are displayed for final user confirmation.  

7. **Backup Creation:**  
   The program uses **wimlib-imagex** to capture the selected source into a `.wim` file, showing live progress and ETA.  

8. **Post-Processing:**  
   If selected, AMBCT performs integrity verification (`--check`) and/or shuts down the system automatically after completion.
 
For more info, visit https://blitzpythoner.github.io/AMBCT/ -> My custom Github page!
---

## Limitations
 
- Only **NTFS drives** support Volume Shadow Copy (snapshot).  
- Requires sufficient free space for temporary and output files.  
- Write-speed testing may fail on Windows versions without WinSAT.
    - If it fails, it can be skipped. 

---

## Known Issues

- On Windows 10 21H2 and up "wmic" may be missing, please install it via: 'DISM /Online /Add-Capability /CapabilityName:WMIC~~~~' as Admin.
- Antivirus software might delay or interfere with file operations.  
- Progress bar timing (ETA) may vary depending on system load.  
- In rare cases, shadow copy creation might fail on removable drives.  

Bug reports and feature requests are welcome via the project’s GitHub Issues page.

---
## Releases

- **v1.0** *(21.10.2025)*  
  First public release of AMBCT (x64).  
  Includes core backup creation, compression options, WinSAT speed test, and VSS snapshot support.

- **v1.0.1** *(22.10.2025)*  
  Bugfix release improving ETA calculation and handling failed WinSAT tests.

- **v1.1** *(22.10.2025)*  
  Major update with **x86 support** (now available as x64 and x86 builds).  
  Added new *Configure Backup* mode to edit existing `.wim` images (name, description, etc.).  
  Minor UI and stability improvements.
---

## Project Duration

Development Period: **13.10.2025 – 21.10.2025**

---

## License and Third-Party Software

This project is distributed under a custom permissive license.  
See `LICENSE.txt` for full details.

This tool includes the following third-party software:

- **wimlib-imagex** (by Eric Biggers) – Licensed under GNU GPL v3 or later  
  Source: https://wimlib.net/downloads/

I do not modify or recompile this tool; it is included in its original binary form.

---

## Credits

**Created by:** BlitzPythoner  
Special thanks to the open-source community and contributors of **wimlib**.  

---

## Disclaimer

This software is provided *"as-is"*, without warranty of any kind.  
Use at your own risk. The author is not responsible for data loss or hardware damage caused by misuse of this tool.

---





