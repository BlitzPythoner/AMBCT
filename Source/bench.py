import os, time

from bench_cpu import cpu_bench
from bench_disk import disk_bench

from errors import error_handler
from globals import get_drive_root


def benchmark(wimlib_path, bench_path, source_path, target_path, compression):
    os.system("cls")

    print("=== BENCHMARK TEST ===")

    try:
        print(f"\nAnalyzing CPU performance ({compression})...")
        cpu_speed = cpu_bench(wimlib_path, compression)
    except Exception:
        error_handler(15)
        cpu_speed = None

    print("\nTesting disk performance...")

    read_speed_source, write_speed_target = disk_bench (bench_path, source_path, target_path)

    if read_speed_source is None or write_speed_target is None:
        error_handler(16)

    return cpu_speed, read_speed_source, write_speed_target