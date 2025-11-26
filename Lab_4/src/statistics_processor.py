import statistics
import pandas as pd


def load_dataset(path):
    return pd.read_csv(path)


def compute_statistics(data):
    return {
        "mean": statistics.mean(data),
        "median": statistics.median(data),
        "mode": _compute_mode_safe(data),
        "population_variance": statistics.pvariance(data),
        "sample_variance": statistics.variance(data),
        "population_std": statistics.pstdev(data),
        "sample_std": statistics.stdev(data)
    }


def _compute_mode_safe(data):
    try:
        return statistics.mode(data)
    except statistics.StatisticsError:
        return "No unique mode"
