# src/visualize.py
from pathlib import Path
import matplotlib.pyplot as plt
import json
from utils import ensure_dirs
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "output" / "results"
PLOTS = ROOT / "output" / "plots"


def load_metrics():
    p = RESULTS / "all_metrics.json"
    if not p.exists():
        raise FileNotFoundError(p)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def plot_times(metrics, out_path=None):
    ensure_dirs()
    runs = metrics["runs"]
    labels = [r["method"] for r in runs]
    # attempt to get a representative time for each run
    times = []
    for r in runs:
        # prefer sum of main phases
        t = 0.0
        for k in ("read_time_s", "collect_time_s", "scan_time_s", "by_region_time_s", "total_rev_time_s"):
            t += float(r.get(k, 0.0))
        times.append(t)

    x = np.arange(len(labels))
    plt.figure(figsize=(8, 4))
    plt.bar(x, times)
    plt.xticks(x, labels)
    plt.ylabel("Approx. time (s)")
    plt.title("Comparison: approximate total time by method")
    out = (PLOTS / "time_comparison.png") if out_path is None else out_path
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    print("Saved time chart to", out)


def plot_memory(metrics, out_path=None):
    ensure_dirs()
    runs = metrics["runs"]
    labels = [r["method"] for r in runs]
    mems = []
    for r in runs:
        before = r.get("mem_before_bytes") or 0
        after = r.get("mem_after_bytes") or 0
        peak = max(before, after)
        mems.append(peak / (1024 * 1024))  # MB

    x = np.arange(len(labels))
    plt.figure(figsize=(8, 4))
    plt.bar(x, mems)
    plt.xticks(x, labels)
    plt.ylabel("Memory (MB) - approx")
    plt.title("Comparison: memory (rss) by method")
    out = (PLOTS / "memory_comparison.png") if out_path is None else out_path
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    print("Saved memory chart to", out)


def run_visuals():
    metrics = load_metrics()
    plot_times(metrics)
    plot_memory(metrics)
    print("Visualizations saved to output/plots/")
