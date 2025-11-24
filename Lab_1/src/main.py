import pandas as pd
from pathlib import Path

from parser import load_raw_data, parse_all
from converter import convert_coordinate, time_to_seconds
from analysis import compute_intervals, compute_aggregates
from plotting import plot_altitude, plot_hdop, plot_trajectory

DATA_IN = Path(__file__).resolve().parents[1] / 'data' / 'gps_raw.txt'
PROCESSED_OUT = Path(__file__).resolve().parents[1] / 'data' / 'processed.csv'
FIGURES_DIR = Path(__file__).resolve().parents[1] / 'reports' / 'figures'


def build_dataframe(parsed_rows):
    rows = []
    for r in parsed_rows:
        lat = convert_coordinate(r.get('raw_lat'), r.get('lat_dir'))
        lon = convert_coordinate(r.get('raw_lon'), r.get('lon_dir'))
        try:
            alt = float(r.get('alt')) if r.get('alt') not in (None, '') else None
        except Exception:
            alt = None
        t_seconds = time_to_seconds(r.get('raw_time'))
        rows.append({
            'raw_time': r.get('raw_time'),
            'raw_time_seconds': t_seconds,
            'lat': lat,
            'lon': lon,
            'alt': alt,
            'sat': r.get('sat'),
            'hdop': r.get('hdop')
        })
    df = pd.DataFrame(rows)
    return df


def format_table1(df):
    """
    Формуємо Таблицю 1:
    Columns: №, широта, довгота, distance (м) [від попередньої], Час польоту (elapsed s), швидкість (m/s)
    """
    t1 = df[['lat', 'lon', 'distance_m', 'elapsed_time_s', 'speed_m_s']].copy()
    t1.index = (t1.index + 1)  # нумерація з 1
    t1 = t1.reset_index().rename(columns={'index': '№'})
    # форматування колонок (необов'язково) — тут лишаємо числа
    return t1


def format_table2(aggs):
    """
    Таблиця 2 — словник -> DataFrame з трьома колонками: №, Параметр, Значення, Одиниця
    """
    rows = [
        (1, 'Сумарна довжина маршруту польоту', aggs['total_length_m'], 'm'),
        (2, 'Середня швидкість польоту', aggs['avg_speed_m_s'], 'm/s'),
        (3, 'Макс. Висота польоту', aggs['max_alt_m'], 'm'),
        (4, 'Мін. Висота польоту', aggs['min_alt_m'], 'm'),
        (5, 'Макс. швидкість польоту', aggs['max_speed_m_s'], 'm/s'),
        (6, 'Мін. швидкість польоту', aggs['min_speed_m_s'], 'm/s'),
        (7, 'Загальний час польоту', aggs['total_time_s'], 's'),
    ]
    df2 = pd.DataFrame(rows, columns=['№ з/п', 'Параметр', 'Значення', 'Одиниця виміру'])
    return df2


def main():
    print("Loading raw data from:", DATA_IN)
    lines = load_raw_data(DATA_IN)
    parsed = parse_all(lines)
    df = build_dataframe(parsed)

    df = compute_intervals(df)

    PROCESSED_OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_OUT, index=False)
    print("Processed data saved to:", PROCESSED_OUT)

    # Таблиця 1
    table1 = format_table1(df)
    print("\n=== Таблиця 1 (перші 20 рядків) ===")
    print(table1.to_string(index=False))

    # Таблиця 2
    aggs = compute_aggregates(df)
    table2 = format_table2(aggs)
    print("\n=== Таблиця 2 ===")
    print(table2.to_string(index=False))

    # графіки
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plot_altitude(df, FIGURES_DIR / 'altitude.png')
    plot_hdop(df, FIGURES_DIR / 'hdop.png')
    plot_trajectory(df, FIGURES_DIR / 'trajectory.png')
    print("\nFigures saved to:", FIGURES_DIR)


if __name__ == '__main__':
    main()
