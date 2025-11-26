def smooth_angles(df, step_s):
    return df[["heading_deg", "pitch_deg"]].resample(f"{step_s}s").mean()


def compute_stats(series):
    mean_val = series.mean()
    std_val = series.std()
    max_dev = (series - mean_val).abs().max()

    return {
        "mean": float(mean_val),
        "std": float(std_val),
        "max_deviation": float(max_dev)
    }
