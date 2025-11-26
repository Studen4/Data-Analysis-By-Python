from pathlib import Path
from parser import load_dualgps
from plots import plot_raw_angles, plot_smoothed
from processor import smooth_angles, compute_stats
from utils import ensure_dir


def main():

    data_path = Path("../data/dualgps_raw.txt")
    plots_dir = Path("../output/plots")
    results_dir = Path("../output/results")
    ensure_dir(plots_dir)
    ensure_dir(results_dir)

    # 1. Завантаження даних
    df = load_dualgps(data_path)

    # 2. Побудова графіків raw
    plot_raw_angles(df, plots_dir)

    # 3. Усереднення
    df10 = smooth_angles(df, 10)
    df20 = smooth_angles(df, 20)

    # 4. Побудова графіків усереднених даних
    plot_smoothed(df10, df20, plots_dir)

    # 5. Статистика
    stats = {
        "heading_stats": compute_stats(df["heading_deg"]),
        "pitch_stats": compute_stats(df["pitch_deg"])
    }

    # Запис у файл
    stats_path = results_dir / "statistics.txt"
    with open(stats_path, "w") as f:
        f.write("Statistics of DualGPS measurements\n\n")
        for key, value in stats.items():
            f.write(f"{key}:\n")
            for k2, v2 in value.items():
                f.write(f"  {k2}: {v2}\n")
            f.write("\n")

    print("Готово! Файли створено у output/")


if __name__ == "__main__":
    main()
