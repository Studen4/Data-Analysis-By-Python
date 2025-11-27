import time
from pathlib import Path
from dask_worker import run_dask_basic
from polars_worker import run_polars_eager, run_polars_lazy
from utils import ensure_dirs, save_json

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "results"


def run_all(npartitions=None):
    ensure_dirs()
    results = {"runs": [], "started_at": time.time()}

    print("Running Polars (eager)...")
    p_eager = run_polars_eager()
    results["runs"].append(p_eager)

    print("Running Polars (lazy)...")
    p_lazy = run_polars_lazy()
    results["runs"].append(p_lazy)

    print("Running Dask...")
    d = run_dask_basic(npartitions=npartitions)
    results["runs"].append(d)

    results["finished_at"] = time.time()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    save_json(OUTPUT / "all_metrics.json", results)
    print("All runs completed, metrics saved to output/results/all_metrics.json")
    return results
