def convert_coordinate(value_str, direction):
    """
    Конвертація формату ddmm.mmmm або dddmm.mmmm -> decimal degrees (float).
    """
    if not value_str:
        return None
    try:
        value = float(value_str)
    except ValueError:
        return None

    degrees = int(value // 100)
    minutes = value - degrees * 100
    decimal = degrees + minutes / 60.0

    if direction in ('S', 'W'):
        decimal = -decimal
    return decimal


def time_to_seconds(timestr):
    """
    timestr формат HHMMSS.ss -> seconds від початку доби (float).
    """
    if not timestr:
        return None
    try:
        hh = int(timestr[0:2])
        mm = int(timestr[2:4])
        ss = float(timestr[4:])
        total = hh * 3600 + mm * 60 + ss
        return total
    except Exception:
        return None
