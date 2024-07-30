#!/usr/bin/python3

def props_parser_gpsinfo_coordinates(raw_value: str) -> int:
    try:
        return convert_to_decimal_degrees(raw_value)

    except Exception:
        return 0


# https://www.earthpoint.us/convert.aspx
def convert_to_decimal_degrees(raw_value: str) -> float:
    """ Convert a string in `dddmm.mmmmmm` format to decimal degrees """
    if len(raw_value) < 7:  # Ensure the string is long enough
        raise ValueError("Invalid format for degrees")
    point_index = raw_value.index('.')
    degrees = int(raw_value[:point_index-2])
    minutes = float(raw_value[point_index-2:])
    decimal_degrees = degrees + minutes / 60
    return decimal_degrees


def convert_to_degrees_minutes_seconds(decimal_degrees: float) -> tuple:
    degrees = int(decimal_degrees)
    minutes_decimal = abs(decimal_degrees - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60
    return degrees, minutes, seconds
