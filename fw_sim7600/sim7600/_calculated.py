#!/usr/bin/python3

from fw_sim7600.sim7600._definitions import *


# Calculation defaults and constants

# N/A


# Calculation methods

# SIM and Network

def calc_network_registration(property_cache) -> bool:
    try:
        status_code = property_cache['network_status_code']['value']
    except KeyError as err:
        raise ValueError("Missing required property: {}".format(err))
    return status_code == 1 or status_code == 5


def calc_network_searching(property_cache) -> bool:
    try:
        status_code = property_cache['network_status_code']['value']
    except KeyError as err:
        raise ValueError("Missing required property: {}".format(err))
    return status_code == 2


def calc_network_roaming(property_cache) -> bool:
    try:
        status_code = property_cache['network_status_code']['value']
    except KeyError as err:
        raise ValueError("Missing required property: {}".format(err))
    return status_code == 5


def calc_network_signal_quality(property_cache) -> float:
    try:
        rssi = property_cache['network_signal_quality_rssi']['value']
        ber = property_cache['network_signal_quality_ber']['value']
    except KeyError as err:
        raise ValueError("Missing required property: {}".format(err))

    # Default values from SIM7600
    # RSSI_MIN = -116
    # RSSI_MAX = -25
    # BER_MIN = 0
    # BER_MAX = 10

    # Adjusted constants on 2G/3G and LTE requirements
    RSSI_MIN = -100
    RSSI_MAX = -60
    BER_MIN = 0
    BER_MAX = 10

    if rssi == 0:
        return -1   # Invalid
    if rssi <= RSSI_MIN:
        return 0.0    # No signal
    if rssi >= RSSI_MAX:
        rssi = RSSI_MAX
    rssi_percent = min((rssi - RSSI_MIN) / (RSSI_MAX - RSSI_MIN), 100.0)

    if ber == -1:
        return round(rssi_percent * 100, 2)
    if ber <= BER_MIN:
        return round(rssi_percent * 100, 2)
    if ber >= BER_MAX:
        ber = BER_MAX
    ber_percent = (ber - BER_MIN) / (BER_MAX - BER_MIN)
    ber_weight = -0.2
    signal_quality = rssi_percent + (ber_percent * ber_weight)
    return max(0.0, round(signal_quality * 100, 2))


def calc_network_sim_status(property_cache) -> bool:
    status_code = property_cache['network_sim_status_code']['value']
    return status_code == SIM_STATUSES_WORKING_KEY


# GNSS

def calc_pos_gnss_sat_count(property_cache):
    try:
        return property_cache['pos_gnss_sat_gps_count']['value']
    except KeyError as err:
        raise ValueError("Missing required property: {}".format(err))
