import pandas as pd


def load_dualgps(path):

    rows = []
    with open(path, "r") as f:
        for line in f:
            if not line.startswith("#DUALANTENNAHEADINGA"):
                continue

            line = line.split("*")[0]
            line = line.replace(";", ",")
            parts = line.split(",")
            rows.append(parts)

    df = pd.DataFrame(rows)

    df = df.iloc[:, :20]
    df.columns = [f"col{i+1}" for i in range(df.shape[1])]

    df["time_s"] = pd.to_numeric(df["col7"], errors="coerce")
    df["heading_deg"] = pd.to_numeric(df["col13"], errors="coerce")
    df["pitch_deg"] = pd.to_numeric(df["col14"], errors="coerce")
    df = df.dropna(subset=["time_s", "heading_deg", "pitch_deg"])

    df = df.sort_values("time_s")
    df = df.set_index("time_s")
    df.index = pd.to_timedelta(df.index, unit="s")

    return df
