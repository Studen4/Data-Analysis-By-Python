from database import create_tables
from loader import load_all_data
from utils import save_results
import queries


def main():
    print("Створюємо таблиці...")
    create_tables()

    print("Завантажуємо CSV...")
    load_all_data()

    # Виконання запитів
    save_results("Простий SELECT", queries.simple_select())
    save_results("SELECT з умовою", queries.select_with_condition())
    save_results("Агрегатні дані", queries.select_aggregated())
    save_results("JOIN запит", queries.select_join())

    deleted = queries.delete_example()
    save_results("Видалені записи", [f"Видалено: {deleted} рядків"])

    print("Готово! Результати у output/results.txt")


if __name__ == "__main__":
    main()
