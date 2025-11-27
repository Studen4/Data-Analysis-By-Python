import time
from pathlib import Path

import polars as pl

from utils import get_memory_info, ensure_dirs, save_json

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "sales_2023.csv"
OUTPUT = ROOT / "output" / "results"


def run_polars_eager(n_head=5):
    ensure_dirs()
    metrics = {"method": "polars_eager", "start": time.time()}

    mem_before = get_memory_info()
    t0 = time.perf_counter()
    df = pl.read_csv(str(DATA_PATH))
    read_time = time.perf_counter() - t0

    metrics["read_time_s"] = read_time
    metrics["rows"], metrics["cols"] = df.shape

    t0 = time.perf_counter()
    df = df.with_columns(
        (pl.col("price") * pl.col("quantity") * (1 - pl.col("discount"))).alias("revenue")
    )
    revenue_time = time.perf_counter() - t0
    metrics["revenue_time_s"] = revenue_time

    t0 = time.perf_counter()
    total_rev = df.select(pl.sum("revenue")).to_series()[0]
    total_time = time.perf_counter() - t0
    metrics["total_rev"] = float(total_rev)
    metrics["total_rev_time_s"] = total_time

    t0 = time.perf_counter()
    by_region = df.group_by("region").agg(pl.sum("revenue").alias("total_revenue"))
    by_region = by_region.sort("total_revenue", descending=True)
    by_region_time = time.perf_counter() - t0
    metrics["by_region_time_s"] = by_region_time

    mem_after = get_memory_info()
    metrics["mem_before_bytes"] = mem_before
    metrics["mem_after_bytes"] = mem_after

    OUTPUT.mkdir(parents=True, exist_ok=True)
    out_csv = OUTPUT / "polars_by_region_eager.csv"
    by_region.write_csv(out_csv)

    metrics["head"] = df.head(n_head).to_dicts()

    metrics["duration_s"] = time.perf_counter() - t0
    metrics["finished_at"] = time.time()
    save_json(OUTPUT / "polars_eager_metrics.json", metrics)
    return metrics


def run_polars_lazy():
    ensure_dirs()
    metrics = {"method": "polars_lazy", "start": time.time()}

    mem_before = get_memory_info()
    t0 = time.perf_counter()
    lazy = pl.scan_csv(str(DATA_PATH))
    read_time = time.perf_counter() - t0
    metrics["scan_time_s"] = read_time

    t0 = time.perf_counter()
    result = (
        lazy
        .with_columns(
            (pl.col("price") * pl.col("quantity") * (1 - pl.col("discount"))).alias("revenue")
        )
        .group_by(["region", "category"])
        .agg([
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("order_id").count().alias("orders_count")
        ])
        .sort("total_revenue", descending=True)
    )
    build_time = time.perf_counter() - t0
    metrics["build_graph_time_s"] = build_time

    t0 = time.perf_counter()
    final = result.collect()
    collect_time = time.perf_counter() - t0
    metrics["collect_time_s"] = collect_time
    metrics["rows_result"] = final.shape[0]

    mem_after = get_memory_info()
    metrics["mem_before_bytes"] = mem_before
    metrics["mem_after_bytes"] = mem_after

    OUTPUT.mkdir(parents=True, exist_ok=True)
    out_csv = OUTPUT / "polars_by_region_lazy.csv"
    final.write_csv(out_csv)

    metrics["finished_at"] = time.time()
    save_json(OUTPUT / "polars_lazy_metrics.json", metrics)
    return metrics
