import random


def generate_random_int_data(n=1000, low=1, high=100):
    """Генерує список випадкових цілих чисел."""
    return [random.randint(low, high) for _ in range(n)]


def generate_triangular_data(n=1000, low=1, high=100, mode=80):
    """Генерує список чисел із трикутним розподілом."""
    return [random.triangular(low, high, mode) for _ in range(n)]
