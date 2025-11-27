# src/main.py
from pathlib import Path
import subprocess
import sys
from compare import run_all
from visualize import run_visuals

ROOT = Path(__file__).resolve().parent.parent
DATA_CSV = ROOT / "data" / "sales_2023.csv"
GENERATOR = ROOT / "data" / "generate_data.py"


def ensure_data(n_rows=1_000_000):
    if DATA_CSV.exists():
        print("Data file exists:", DATA_CSV, "size:", DATA_CSV.stat().st_size / (1024*1024), "MB")
        return
    print("Data file not found. Generating with data/generate_data.py ...")
    cmd = [sys.executable, str(GENERATOR), str(n_rows)]
    subprocess.check_call(cmd)
    print("Generation finished.")


def main():
    # default number of rows
    N_ROWS = 1_000_000

    # ensure data
    ensure_data(N_ROWS)

    # run comparisons
    run_all()

    # visualize
    run_visuals()
    print("Done. Check output/results and output/plots.")


if __name__ == "__main__":
    main()
