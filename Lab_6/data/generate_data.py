import polars as pl
import numpy as np
from datetime import datetime, timedelta
import time
import os


def generate_data(output_path: str = "sales_2023.csv", n_rows: int = 1_000_000):
    start_time = time.time()

    print(f"Генеруємо {n_rows:,} рядків...")
    order_id = np.arange(1, n_rows + 1)

    start_date = datetime(2023, 1, 1)
    order_date = [
        (start_date + timedelta(days=int(x))).strftime("%Y-%m-%d")
        for x in np.random.randint(0, 365, n_rows)
    ]

    regions = np.random.choice(
        ["Europe", "Asia", "North America", "South America", "Africa"], n_rows
    )
    categories = np.random.choice(
        ["Electronics", "Furniture", "Clothes", "Toys"], n_rows
    )
    sub_categories = np.random.choice(
        ["Phones", "TVs", "Sofas", "Chairs", "Shirts", "Pants", "Dolls"], n_rows
    )

    price = np.round(np.random.uniform(5, 5000, n_rows), 2)
    quantity = np.random.randint(1, 20, n_rows)
    discount = np.round(np.random.uniform(0, 0.5, n_rows), 2)

    df = pl.DataFrame({
        "order_id": order_id,
        "order_date": order_date,
        "region": regions,
        "category": categories,
        "sub_category": sub_categories,
        "price": price,
        "quantity": quantity,
        "discount": discount
    })

    df.write_csv(output_path)

    duration = time.time() - start_time
    size_mb = os.path.getsize(output_path) / (1024 * 1024)

    print(f"Файл згенеровано: {output_path}")
    print(f"Розмір файлу: {size_mb:.2f} MB")
    print(f"Час генерації: {duration:.2f} сек")

    return {
        "n_rows": n_rows,
        "file_size_mb": size_mb,
        "generation_time_s": duration
    }


if __name__ == "__main__":
    generate_data()
