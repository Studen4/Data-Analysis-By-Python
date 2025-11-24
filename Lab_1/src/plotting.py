import matplotlib.pyplot as plt
from pathlib import Path


def ensure_dir(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)


def plot_altitude(df, out_path):
    ensure_dir(Path(out_path).parent)
    plt.figure()
    plt.plot(df['elapsed_time_s'], df['alt'].astype(float))
    plt.xlabel('Elapsed time (s)')
    plt.ylabel('Altitude (m)')
    plt.title('Altitude over time')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_hdop(df, out_path):
    ensure_dir(Path(out_path).parent)
    plt.figure()
    hdop = df['hdop'].apply(lambda x: float(x) if x not in (None, '', '0') else float('nan'))
    plt.plot(df['elapsed_time_s'], hdop)
    plt.xlabel('Elapsed time (s)')
    plt.ylabel('HDOP')
    plt.title('HDOP over time')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_trajectory(df, out_path):
    ensure_dir(Path(out_path).parent)
    plt.figure()
    plt.plot(df['lon'], df['lat'], marker='o', linestyle='-')
    plt.xlabel('Longitude (deg)')
    plt.ylabel('Latitude (deg)')
    plt.title('Trajectory')
    plt.axis('equal')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
