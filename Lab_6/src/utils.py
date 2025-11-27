import time
import json
from contextlib import contextmanager
from pathlib import Path

try:
    import psutil
except Exception:
    psutil = None


@contextmanager
def timer():
    t0 = time.perf_counter()
    try:
        yield lambda: time.perf_counter() - t0
    finally:
        pass


def now_s():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def ensure_dirs():
    root = Path(__file__).resolve().parent.parent
    (root / "output").mkdir(parents=True, exist_ok=True)
    (root / "output" / "results").mkdir(parents=True, exist_ok=True)
    (root / "output" / "plots").mkdir(parents=True, exist_ok=True)


def get_memory_info():
    """
    Returns resident set size in bytes (rss) if psutil is available, else None.
    """
    if psutil is None:
        return None
    p = psutil.Process()
    mem = p.memory_info().rss
    return mem


def save_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
