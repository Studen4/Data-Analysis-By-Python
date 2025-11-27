from database import get_connection


def simple_select():
    """1. Простий SELECT — список працівників."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT first_name, last_name, position FROM workers;")
    rows = cur.fetchall()
    conn.close()
    return rows


def select_with_condition():
    """2. Обладнання, придбане після 2019 року."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, type, purchase_year
        FROM equipment
        WHERE purchase_year > 2019;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def select_aggregated():
    """3. Агрегат: кількість операцій ТО по кожному працівнику."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT workers.first_name, workers.last_name, COUNT(*)
        FROM maintenance_operations
        JOIN workers ON workers.worker_id = maintenance_operations.worker_id
        GROUP BY workers.worker_id;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def select_join():
    """4. JOIN: коли і яке обладнання проходило ТО."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT maintenance_operations.date,
               equipment.name,
               workers.first_name || ' ' || workers.last_name,
               maintenance_operations.description
        FROM maintenance_operations
        JOIN equipment ON equipment.equipment_id = maintenance_operations.equipment_id
        JOIN workers ON workers.worker_id = maintenance_operations.worker_id;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_example():
    """5. Видалення: видаляємо матеріали з кількістю < 2"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM materials_used WHERE quantity < 2;")
    affected = cur.rowcount

    conn.commit()
    conn.close()
    return affected
