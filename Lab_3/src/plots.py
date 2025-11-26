import matplotlib.pyplot as plt
from pathlib import Path
from utils import ensure_dir


def plot_series(x, y, xlabel, ylabel, title, out_path):
    ensure_dir(Path(out_path).parent)

    plt.figure(figsize=(10, 5))
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_raw_angles(df, out_dir):
    plot_series(
        x=df.index,
        y=df["heading_deg"],
        xlabel="Time (s)",
        ylabel="Heading (deg)",
        title="Heading vs Time",
        out_path=out_dir / "heading_raw.png"
    )

    plot_series(
        x=df.index,
        y=df["pitch_deg"],
        xlabel="Time (s)",
        ylabel="Pitch (deg)",
        title="Pitch vs Time",
        out_path=out_dir / "pitch_raw.png"
    )


def plot_smoothed(df10, df20, out_dir):
    plot_series(
        x=df10.index,
        y=df10["heading_deg"],
        xlabel="Time (s)",
        ylabel="Heading (deg)",
        title="Heading Avg (10 s)",
        out_path=out_dir / "heading_avg_10s.png"
    )

    plot_series(
        x=df10.index,
        y=df10["pitch_deg"],
        xlabel="Time (s)",
        ylabel="Pitch (deg)",
        title="Pitch Avg (10 s)",
        out_path=out_dir / "pitch_avg_10s.png"
    )

    plot_series(
        x=df20.index,
        y=df20["heading_deg"],
        xlabel="Time (s)",
        ylabel="Heading (deg)",
        title="Heading Avg (20 s)",
        out_path=out_dir / "heading_avg_20s.png"
    )

    plot_series(
        x=df20.index,
        y=df20["pitch_deg"],
        xlabel="Time (s)",
        ylabel="Pitch (deg)",
        title="Pitch Avg (20 s)",
        out_path=out_dir / "pitch_avg_20s.png"
    )
