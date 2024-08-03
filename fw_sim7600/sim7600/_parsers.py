#!/usr/bin/python3

from fw_sim7600.sim7600._definitions import *


def props_parser_network_status_code(raw_value: str) -> int:
    try:
        # remove the '+CREG: 0,' prefix
        return int(raw_value.split(',')[1])
    except Exception:
        raise ValueError("Can't cast '{}' into {}".format(raw_value, "network_status_code"))


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


def props_parser_sim_provider(raw_value: str) -> str:
    try:
        if '"' not in raw_value:
            return "-- Unknown Provider --"

        # extract text in apex from the '+COPS: 0,0,"vodafone IT",0' format
        provider = raw_value.split('"')[1]
        if provider == "":
            return "-- Unknown Provider --"
        return provider

    except Exception:
        raise ValueError("Can't extract provider name from '{}' response".format(raw_value))


def calc_network_registration(property_cache) -> bool:
    status_code = property_cache['network_status_code']['value']
    return status_code == 1 or status_code == 5


def calc_network_searching(property_cache) -> bool:
    status_code = property_cache['network_status_code']['value']
    return status_code == 2


def calc_network_roaming(property_cache) -> bool:
    status_code = property_cache['network_status_code']['value']
    return status_code == 5


def parse_network_signal_quality_rssi(raw_value: str) -> int:
    """
    From https://www.waveshare.com/w/upload/a/af/SIM7500_SIM7600_Series_AT_Command_Manual_V3.00.pdf
    Page 65 - AT+CSQ

    0 – - 113 dBm or less
    1 – - 111 dBm
    2...30 – - 109... - 53 dBm                  56 dBm / 28 levels = 2 dBm/level
    31 – - 51 dBm or greater
    99 – not known or not detectable
    100 – - 116 dBm or less
    101 – - 115 dBm
    102…191 – - 114... - 26dBm                  88 dBm / 90 levels = 0.98 dBm/level
    191 – - 25 dBm or greater
    199 – not known or not detectable
    100…199 – expand to TDSCDMA, indicate RSCPreceived
    """

    try:
        raw_int = int(raw_value)
    except Exception:
        raise ValueError("Can't cast '{}' into {}".format(raw_value, "int"))

    if raw_int == 0:
        return -113
    elif raw_int == 1:
        return -111
    elif 2 <= raw_int <= 30:
        return -109 + (raw_int * 2)
    elif raw_int == 31:
        return -51
    elif raw_int == 99:
        return 0
    elif raw_int == 100:
        return -116
    elif raw_int == 101:
        return -115
    elif 102 <= raw_int <= 191:
        return -114 + (raw_int * 0.98)
    elif raw_int == 199:
        return 0

    raise ValueError("Invalid value for RSSI: {}".format(raw_value))


def parse_network_signal_quality_ber(raw_value: str) -> float:
    """
    From https://www.waveshare.com/w/upload/a/af/SIM7500_SIM7600_Series_AT_Command_Manual_V3.00.pdf
    Page 65 - AT+CSQ

    0 – <0.01%
    1 – 0.01% --- 0.1%
    2 – 0.1% --- 0.5%
    3 – 0.5% --- 1.0%
    4 – 1.0% --- 2.0%
    5 – 2.0% --- 4.0%
    6 – 4.0% --- 8.0%
    7 – >=8.0%
    99 – not known or not detectable
    """

    try:
        raw_int = int(raw_value)
    except Exception:
        raise ValueError("Can't cast '{}' into {}".format(raw_value, "int"))

    if raw_int == 0:
        return 0.0
    elif raw_int == 1:
        return 0.05
    elif raw_int == 2:
        return 0.25
    elif raw_int == 3:
        return 0.75
    elif raw_int == 4:
        return 1.5
    elif raw_int == 5:
        return 3.0
    elif raw_int == 6:
        return 6.0
    elif raw_int == 7:
        return 10.0
    elif raw_int == 99:
        return -1.0

    raise ValueError("Invalid value for BER: {}".format(raw_value))


def calc_network_signal_quality(property_cache) -> float:
    rssi = property_cache['network_signal_quality_rssi']['value']
    ber = property_cache['network_signal_quality_ber']['value']
    return _calculate_signal_quality(rssi, ber)


def _normalize_rssi(rssi):
    if rssi == 99 or rssi == 199:
        return 0  # Not known or not detectable
    elif rssi <= 31:
        return (rssi - 0) / (31 - 0)  # Normalize 0-31 to 0-1
    elif rssi >= 100 and rssi <= 191:
        return (rssi - 100) / (191 - 100)  # Normalize 100-191 to 0-1
    else:
        return 0  # Out of range values


def _normalize_ber(ber):
    if ber == 99:
        return 0  # Not known or not detectable
    else:
        return (7 - ber) / 7  # Invert and normalize 0-7 to 0-1


def _calculate_signal_quality(rssi, ber):
    normalized_rssi = _normalize_rssi(rssi)
    normalized_ber = _normalize_ber(ber)

    # Assign weights (e.g., 80% for RSSI and 20% for BER)
    rssi_weight = 0.8
    ber_weight = 0.2

    # Calculate the signal quality as a weighted average
    signal_quality = (normalized_rssi * rssi_weight) + (normalized_ber * ber_weight)

    # Convert to percentage
    signal_quality_percentage = signal_quality * 100

    return signal_quality_percentage



def calc_network_sim_status(property_cache) -> bool:
    status_code = property_cache['network_sim_status_code']['value']
    return status_code == SIM_STATUSES_WORKING_KEY


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
