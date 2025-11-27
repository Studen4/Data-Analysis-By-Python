from pathlib import Path
import time
from utils import ensure_dirs, get_memory_info, save_json
import dask.dataframe as dd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "sales_2023.csv"
OUTPUT = ROOT / "output" / "results"


def run_dask_basic(npartitions=None):
    ensure_dirs()
    metrics = {"method": "dask", "start": time.time()}

    mem_before = get_memory_info()
    t0 = time.perf_counter()
    if npartitions:
        ddf = dd.read_csv(str(DATA_PATH), blocksize=None).repartition(npartitions=npartitions)
    else:
        ddf = dd.read_csv(str(DATA_PATH))
    metrics["read_time_s"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    ddf["price"] = ddf["price"].astype(float)
    ddf["quantity"] = ddf["quantity"].astype(int)
    ddf["discount"] = ddf["discount"].astype(float)
    cast_time = time.perf_counter() - t0
    metrics["cast_time_s"] = cast_time

    t0 = time.perf_counter()
    ddf = ddf.assign(revenue=ddf["price"] * ddf["quantity"] * (1 - ddf["discount"]))
    assign_time = time.perf_counter() - t0
    metrics["assign_time_s"] = assign_time

    t0 = time.perf_counter()
    total_rev = ddf["revenue"].sum().compute()
    metrics["total_rev"] = float(total_rev)
    metrics["total_rev_time_s"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    by_region = ddf.groupby("region")["revenue"].sum().compute()
    by_region_time = time.perf_counter() - t0
    metrics["by_region_time_s"] = by_region_time

    mem_after = get_memory_info()
    metrics["mem_before_bytes"] = mem_before
    metrics["mem_after_bytes"] = mem_after

    OUTPUT.mkdir(parents=True, exist_ok=True)
    out_csv = OUTPUT / "dask_by_region.csv"
    by_region.to_csv(out_csv)

    metrics["finished_at"] = time.time()
    save_json(OUTPUT / "dask_metrics.json", metrics)
    return metrics
