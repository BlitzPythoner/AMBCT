# AMBCT v1.0 – Automatic Manual Backup Creation Tool

**Author:** BlitzPythoner  
**Version:** 1.0 
**Language:** Python 3.6+  
**OS Support:** Windows Vista, 7, 8.x, 10, 11  
**Architecture:** x64 (x86 support planned)  

---

## Description

AMBCT (Automatic Manual Backup Creation Tool) is a command-line based backup utility that uses **wimlib-imagex** for creating reliable and highly compressed system or file backups.  
It allows users to select drives or folders, define a target location, choose compression methods, and manage advanced options like integrity checks or automatic shutdown.

This tool combines automation and manual control – perfect for users who want efficiency **without losing control** over how their backups are created.

---

## Main Features

- **Automatic Drive Detection:** Lists all connected drives with names, sizes, and available space.  
- **Flexible Source Selection:** Back up entire drives or specific folders.  
- **Destination Selection:** Choose where the backup should be stored, with optional path specification.  
- **Storage Check:** Warns when the destination drive doesn’t have enough free space.  
- **Compression Options:**  
  - `NONE` – No compression, fastest.  
  - `XPRESS` – Light/medium compression, balanced speed.  
  - `LZX` – Strong compression, slower but efficient.  
  - `LZMS` – Maximum compression, slowest but smallest result.  
- **Additional Options:**  
  - `check` – Verifies the integrity of the resulting backup.  
  - `solid` – Combines file data into solid blocks for higher compression.  
  - `shutdown` – Shuts down the system after backup creation.  
- **Write Speed Test:** Measures sequential write speed using **WinSAT** before starting the backup.  
- **ETA Calculation:** Estimates backup duration based on detected drive performance.  
- **Progress Bar:** Real-time display of progress and estimated time remaining.  
- **Snapshot Support:** Uses Volume Shadow Copy (VSS) on NTFS drives to capture files safely.  
- **Error Handling:** Detects missing dependencies, insufficient space, or permission issues.  
- **Automatic Cleanup:** Removes temporary files on exit.  
- **Detailed Summary:** Displays all chosen settings and backup details before execution.

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

1. The program starts by detecting all available drives.  
2. The user selects the source (drive or folder).  
3. The target destination for the backup is chosen.  
4. AMBCT checks the available space and compression settings.  
5. A write-speed benchmark (WinSAT) is performed.  
6. The user reviews all settings before starting.  
7. The backup is created using **wimlib-imagex**, with live progress updates.  
8. Optional post-process actions (verification, shutdown) are executed.  

---

## Limitations

- Currently supports only **x64 systems**.  
- **x86 version** is planned for a later release.  
- Only **NTFS drives** support Volume Shadow Copy (snapshot).  
- Requires sufficient free space for temporary and output files.  
- Write-speed testing may fail on Windows versions without WinSAT.  

---

## Known Issues

- On Windows 10 21H2 and up "wmic" may be missing, please install it via: 'DISM /Online /Add-Capability /CapabilityName:WMIC~~~~' as Admin.
- Antivirus software might delay or interfere with file operations.  
- Progress bar timing (ETA) may vary depending on system load.  
- In rare cases, shadow copy creation might fail on removable drives.  

Bug reports and feature requests are welcome via the project’s GitHub Issues page.

---
## Releases
- v1.0 Main Release [21-10-2025]
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

