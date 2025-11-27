import csv
from pathlib import Path
from database import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent  # Lab_5/
DATA_DIR = BASE_DIR / "data"


def load_csv_to_table(csv_filename, table_name):
    csv_path = DATA_DIR / csv_filename

    if not csv_path.exists():
        raise FileNotFoundError(f"File not found: {csv_path}")

    conn = get_connection()
    cur = conn.cursor()

    with csv_path.open(encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)

        placeholders = ", ".join("?" for _ in headers)
        query = f"INSERT INTO {table_name} VALUES ({placeholders});"

        rows_loaded = 0
        for row in reader:
            if len(row) != len(headers):
                print(f"Warning: skipping row with wrong number of columns in {csv_filename}: {row}")
                continue
            cur.execute(query, row)
            rows_loaded += 1

    conn.commit()
    conn.close()
    print(f"Loaded {rows_loaded} rows into {table_name} from {csv_path}")


def load_all_data():
    load_csv_to_table("equipment.csv", "equipment")
    load_csv_to_table("workers.csv", "workers")
    load_csv_to_table("maintenance_operations.csv", "maintenance_operations")
    load_csv_to_table("materials_used.csv", "materials_used")

    print("Дані успішно завантажено!")
