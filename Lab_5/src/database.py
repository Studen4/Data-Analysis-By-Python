import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "maintenance.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Таблиця обладнання
    cur.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            equipment_id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            purchase_year INTEGER
        );
    """)

    # Таблиця працівників
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            worker_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            position TEXT
        );
    """)

    # Таблиця операцій ТО
    cur.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_operations (
            operation_id INTEGER PRIMARY KEY,
            equipment_id INTEGER,
            worker_id INTEGER,
            date TEXT,
            description TEXT,
            FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id),
            FOREIGN KEY (worker_id) REFERENCES workers(worker_id)
        );
    """)

    # Таблиця використаних матеріалів
    cur.execute("""
        CREATE TABLE IF NOT EXISTS materials_used (
            material_id INTEGER PRIMARY KEY,
            operation_id INTEGER,
            name TEXT,
            quantity INTEGER,
            FOREIGN KEY (operation_id) REFERENCES maintenance_operations(operation_id)
        );
    """)

    conn.commit()
    conn.close()
