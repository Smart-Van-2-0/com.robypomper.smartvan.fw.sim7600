#!/usr/bin/python3

from fw_sim7600.sim7600._definitions import *


def props_parser_sim_status_code(raw_value: str) -> int:
    try:
        # remove the '+CPIN: ' prefix
        raw_code = raw_value.split(': ')[1]
        for key, status in SIM_STATUSES.items():
            if raw_code in status['vals']:
                return key
        return SIM_STATUSES_UNKNOWN_KEY
    except Exception:
        raise ValueError("Can't find {} mapped value for '{}' code".format("SIM_STATUSES", raw_value))


def calc_network_sim_status(property_cache):
    status_code = property_cache['network_sim_status_code']['value']
    return status_code is SIM_STATUSES_WORKING_KEY


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


# North -> True, South -> False
def props_parser_lat(raw_value: str) -> bool:
    if raw_value.upper() in ['N', 'NORTH']:
        return True
    return False


# West -> True, East -> False
def props_parser_lon(raw_value: str) -> bool:
    if raw_value.upper() in ['W', 'WEST']:
        return True
    return False


def calc_pos_gnss_sat_count(property_cache):
    return property_cache['pos_gnss_sat_gps_count']['value']
