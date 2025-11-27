from pathlib import Path


def save_results(title, data, output_path="output/results.txt"):
    Path("output").mkdir(exist_ok=True)

    with open(output_path, "a", encoding="utf-8") as file:
        file.write(f"\n=== {title} ===\n")
        for row in data:
            file.write(str(row) + "\n")
