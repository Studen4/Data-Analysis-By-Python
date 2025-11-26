from pathlib import Path
from generator import generate_random_int_data, generate_triangular_data
from statistics_processor import load_dataset, compute_statistics
from utils import ensure_dir

OUTPUT_FILE = Path("../output/results.txt")
DATASET_PATH = Path("../data/dataset_variant.csv")


def write_results(title, stats, file):
    file.write(f"{title}\n")
    for key, value in stats.items():
        file.write(f"{key}: {value}\n")
    file.write("\n\n")


def main():
    ensure_dir(Path("../output"))

    with open(OUTPUT_FILE, "w") as out:
        out.write("=== Демонстраційні приклади ===\n\n")
        demo1 = generate_random_int_data()
        demo1_stats = compute_statistics(demo1)
        write_results("Випадкові int дані", demo1_stats, out)
        demo2 = generate_triangular_data()
        demo2_stats = compute_statistics(demo2)
        write_results("Трикутний розподіл", demo2_stats, out)

        out.write("=== Статистика для набору даних ===\n\n")
        df = load_dataset(DATASET_PATH)
        student_data = df["speed_kmh"].tolist()
        student_stats = compute_statistics(student_data)
        write_results("Набір за варіантом — speed_kmh", student_stats, out)
        course_data = df["course_deg"].tolist()
        course_stats = compute_statistics(course_data)
        write_results("Набір за варіантом — course_deg", course_stats, out)

    print("Готово! Результати у output/results.txt")


if __name__ == "__main__":
    main()
