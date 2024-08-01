#!/usr/bin/python3

import random


""" Default device type for unknown devices """
DEV_TYPE_UNKNOWN = "Unknown Device Type"


# Default properties' parsers

def props_parser_none(raw_value):
    return raw_value


def props_parser_str(raw_value: str) -> str:
    try:
        return str(raw_value)
    except Exception:
        raise ValueError("Can't cast '{}' into {}".format(raw_value, "str"))


def props_parser_bool(raw_value: str) -> bool:
    try:
        return bool(raw_value)
    except Exception:
        raise ValueError("Can't cast '{}' into {}".format(raw_value, "bool"))


def props_parser_int(raw_value: str) -> int:
    try:
        return int(raw_value)
    except Exception:
        raise ValueError("Can't cast '{}' into {}".format(raw_value, "int"))


def props_parser_float(raw_value: str) -> float:
    try:
        return float(raw_value)
    except Exception:
        raise ValueError("Can't cast '{}' into {}".format(raw_value, "float"))


# Firmware utility methods

def dev_type_to_code(device_type) -> str:
    """ make given string lower case and replace whitespaces with '_' """
    return device_type.lower().replace(' ', '_')


def regenerateValueMaxMin(str_value, range_value, min_val, max_val):
    return max(min(regenerateValue(str_value, range_value), max_val), min_val)


def regenerateValue(str_value, range_value):
    prev_value = props_parser_float(str_value)
    if type(range_value) == int:
        inc = random.randint(0, range_value) - (range_value / 2)
    elif type(range_value) == float:
        range_value_multi = range_value * 10000
        inc = random.randint(0, range_value_multi) - (range_value_multi / 2)
        inc = inc / 10000
    else:
        inc = range_value
    return prev_value + inc
