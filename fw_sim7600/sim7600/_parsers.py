#!/usr/bin/python3


def props_parser_vin(raw_value: str) -> bool:
    try:
        if raw_value.upper() == "GOOD":
            return True
        elif raw_value.upper() == "NG":
            return False
        else:
            raise ValueError("Can't cast '{}' into {}, invalid value".format(raw_value, "float"))
    except Exception:
        raise ValueError("Can't cast '{}' into {}".format(raw_value, "float"))
