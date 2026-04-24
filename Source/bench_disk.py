import subprocess, re, os

def disk_bench(bench_path, source_path, target_path):
    try:
        if os.path.isfile(target_path):
            target_path = os.path.dirname(target_path)

        result = subprocess.run(
            [bench_path, source_path, target_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        output = result.stdout

        match = re.search(
            r"Read:\s*([\d\.]+)\s*MB/s,\s*Write:\s*([\d\.]+)\s*MB/s",
            output
        )

        if not match:
            return None, None

        read_speed = float(match.group(1))
        write_speed = float(match.group(2))

        return read_speed, write_speed

    except Exception as e:
        return None, None


