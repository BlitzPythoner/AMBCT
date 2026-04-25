import os, time, tempfile, shutil, subprocess

def _round(x):
    return max(128, int(round(x / 128) * 128))

def _run(wimlib, comp, size):
    t = tempfile.mkdtemp(prefix="ambct_")
    d = os.path.join(t, "d")
    os.makedirs(d)
    f = os.path.join(d, "t.bin")

    with open(f, "wb") as fp:
        fp.write(os.urandom(size * 1024 * 1024))

    out = os.path.join(t, "t.wim")

    s = time.time()
    subprocess.run([
        wimlib, "capture", d, out, "t",
        f"--compress={comp.lower()}",
        "--threads=0"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dur = time.time() - s

    shutil.rmtree(t, ignore_errors=True)

    return dur

def cpu_bench(wimlib, comp):
    size = 128

    for _ in range(3):
        d = _run(wimlib, comp, size)

        if 3 <= d <= 6:
            break

        scale = 4 / d
        size = _round(size * scale)

        if size > 1024:
            size = 1024
            break

    d = _run(wimlib, comp, size)
    return round(size / d, 1)