from pathlib import Path


def load_raw_data(path):
    p = Path(path)
    with p.open('r', encoding='utf-8') as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    return lines


def _strip_checksum(line):
    if '*' in line:
        return line.split('*')[0]
    return line


def parse_gpgga_line(line):
    """
    Повертає dict з полями raw: time, raw_lat, lat_dir, raw_lon, lon_dir, fix, sat, hdop, alt
    Якщо рядок не GPGGA — повертає None.
    """
    line = _strip_checksum(line)
    if 'GPGGA' not in line:
        return None
    parts = line.split(',')
    try:
        return {
            "raw_time": parts[1],
            "raw_lat": parts[2],
            "lat_dir": parts[3],
            "raw_lon": parts[4],
            "lon_dir": parts[5],
            "fix": parts[6],
            "sat": parts[7],
            "hdop": parts[8],
            "alt": parts[9]
        }
    except IndexError:
        return None


def parse_all(lines):
    parsed = []
    for ln in lines:
        row = parse_gpgga_line(ln)
        if row is not None:
            parsed.append(row)
    return parsed
