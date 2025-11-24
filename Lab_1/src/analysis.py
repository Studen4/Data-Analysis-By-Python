import math


def haversine_m(lat1, lon1, lat2, lon2):
    """
    Haversine distance in meters between two decimal-degree points.
    Вхід: градуси (float). Повертає м (float).
    """
    if None in (lat1, lon1, lat2, lon2):
        return 0.0

    R = 6371000.0  # радіус Землі в метрах
    # конвертація градусів у радіани
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def compute_intervals(df):
    n = len(df)
    delta_t = [0.0] * n
    elapsed = [0.0] * n
    dist = [0.0] * n
    cum = [0.0] * n
    speed = [0.0] * n

    prev_time = None
    prev_lat = None
    prev_lon = None
    cum_dist = 0.0
    start_time = None

    for i in range(n):
        lat = df.at[i, 'lat']
        lon = df.at[i, 'lon']
        t = df.at[i, 'raw_time_seconds']
        if start_time is None and t is not None:
            start_time = t

        if prev_time is None:
            dt = 0.0
        else:
            dt = t - prev_time
            if dt < 0:
                dt += 24 * 3600

        if prev_lat is None or prev_lon is None:
            d = 0.0
        else:
            d = haversine_m(prev_lat, prev_lon, lat, lon)

        cum_dist += d
        sp = 0.0 if dt == 0 else d / dt

        delta_t[i] = dt
        elapsed[i] = 0.0 if start_time is None or t is None else (
            t - start_time if t >= start_time else t - start_time + 24 * 3600)
        dist[i] = d
        cum[i] = cum_dist
        speed[i] = sp

        prev_time = t
        prev_lat = lat
        prev_lon = lon

    # присвоїмо у DataFrame
    df['delta_time_s'] = delta_t
    df['elapsed_time_s'] = elapsed
    df['distance_m'] = dist
    df['cum_distance_m'] = cum
    df['speed_m_s'] = speed

    return df


def compute_aggregates(df):
    total_length_m = float(df['distance_m'].sum())
    total_time_s = float(df['delta_time_s'].sum())

    avg_speed_m_s = total_length_m / total_time_s if total_time_s > 0 else 0.0

    max_alt = None
    min_alt = None
    if 'alt' in df.columns:
        alt_series = df['alt'].dropna().astype(float)
        if len(alt_series) > 0:
            max_alt = float(alt_series.max())
            min_alt = float(alt_series.min())

    speeds_moving = df.loc[df['delta_time_s'] > 0, 'speed_m_s'].dropna().astype(float)

    if len(speeds_moving) > 0:
        max_speed = float(speeds_moving.max())
        min_speed = float(speeds_moving.min())
    else:
        max_speed = None
        min_speed = None

    return {
        "total_length_m": total_length_m,
        "avg_speed_m_s": avg_speed_m_s,
        "max_alt_m": max_alt,
        "min_alt_m": min_alt,
        "max_speed_m_s": max_speed,
        "min_speed_m_s": min_speed,
        "total_time_s": total_time_s
    }
