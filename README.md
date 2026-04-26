# AMBCT – Automatic Manual Backup Creation Tool

**Author:** BlitzPythoner  
**Version:** v1.6+
**Language:** Python 3.6+  
**OS Support:** Windows Vista, 7, 8.x, 10, 11  
**Architecture:** x64 only (v1.6+)

---

## Description

AMBCT (Automatic Manual Backup Creation Tool) is a command-line based backup utility that uses **wimlib-imagex** for creating reliable and highly compressed system or file backups.

It combines **automation, performance analysis, and manual control** to deliver accurate and efficient backup creation — even on legacy systems without modern dependencies.

---

## Core Features

- **Native Disk Benchmark System**  
  → Measures real read/write speed using direct I/O (no OS cache influence)  

- **CPU Performance Benchmark**  
  → Determines realistic compression speed  

- **Dynamic ETA Calculation**  
  → Based on actual CPU, read, and write speeds  
  → Automatically detects bottlenecks  

- **Accurate Progress Tracking**  
  → Live progress bar with smoothed ETA  

- **Full Control Backup System**  
  → Supports drives, folders, and custom paths  

- **Offline Capability**  
  → Works fully without internet connection  

---

## Backup Creation Features

- Automatic drive detection with detailed information  
- Backup entire drives or custom folders  
- Flexible target selection  
- Smart storage validation system  
- Advanced compression methods:
  - `NONE`
  - `XPRESS`
  - `LZX`
  - `LZMS`
- Optional flags:
  - `check`
  - `solid`
  - `shutdown`
- VSS Snapshot support for system backups  
- Full logging system (`*_log.txt`)  
- Pre-check summary before execution  

---

## Backup Append Features

- Append backups to existing `.wim` files  
- Automatic compression detection  
- Pre- and post-verification of backups  
- Safe multi-index management  
- Logging for all append operations  

---

## Backup Configuration Features

- Inspect `.wim` images  
- View detailed metadata:
  - Compression
  - Size
  - Creation time
  - Windows version
- Modify:
  - Name
  - Display Name
  - Description  
- Delete individual backup indexes  
- Verify backup integrity  

---

## Performance System (v1.6+)

AMBCT uses a **multi-factor performance model**:

- CPU speed (compression)
- Source read speed
- Target write speed

The slowest component determines the **effective speed**:

This ensures realistic ETA predictions and optimal behavior across all systems.

---

## Requirements

- Administrator privileges  
- Windows Vista or later  
- wimlib-imagex (included)  
- No external tools required  

---

## How It Works

Visit my github page: https://blitzpythoner.github.io/AMBCT/ 

---

## Compatibility

AMBCT is designed to work on both modern and legacy systems:

- Windows Vista  
- Windows 7  
- Windows 8 / 8.1  
- Windows 10  
- Windows 11  

No modern APIs or online services required.

---

## Limitations

- VSS only works on NTFS drives  
- Performance depends on hardware  
- Requires sufficient disk space  

---

## Known Issues

- ETA may vary under heavy system load  
- Antivirus software may slow down operations  
- Benchmark may fail on restricted systems (handled safely)  

---

## Project Status

As of April 2026, AMBCT is still under active development. However, development may be suspended at any time for an indefinite period.
Future updates will focus on stability improvements and advanced backup features.

---

## License and Third-Party Software

Includes:

- **wimlib-imagex** (GPL v3)  
  https://wimlib.net/

---

## Credits

Created by BlitzPythoner  

---

## Disclaimer

This software is provided "as-is" without warranty.  
Use at your own risk.
