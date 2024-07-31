#!/usr/bin/python3

from fw_sim7600.commons import *
from fw_sim7600.sim7600._definitions import *
from fw_sim7600.sim7600._dbus_descs import *
from fw_sim7600.sim7600._parsers import *

# Given an PID, this object returns all his info and meta-data
PID = {
    "SIMCOM_SIM7600E-H": {"model": "SIM7600E-H", "type": DEV_TYPE_SIM7600,
                          "dbus_iface": DEV_IFACE_SIM7600,
                          "dbus_desc": DEV_DBUS_DESC_SIM7600},
}

# Other models
# SIMCOM_SIM7600A-H     Cat-4
# SIMCOM_SIM7600E-H     Cat-4
# SIMCOM_SIM7600E       Cat-1
# A_7670E               Cat-1
# A_7600E               Cat-1
# SIMCOM_SIM7600SA-H    Cat-4
# SIMCOM_SIM7600CE      Cat-4
# SIMCOM_SIM7600CE-CNSE Cat-4
# SIMCOM_SIM7600CE-JT1S Cat-4
# A_7600C1              Cat-1
# SIMCOM_SIM7600G-H     Cat-4

PROPS_CODES = {
    "AT+CGMI": {"name": "manufacturer", "desc": "Product's manufacturer",
                "parser": props_parser_str},
    "AT+CGMM": {"name": "model", "desc": "Product's model",
                "parser": props_parser_str},
    "AT+CGSN": {"name": "serial_number", "desc": "Product's serial number",
                "parser": props_parser_str},
    "AT+CSUB": {"name": "version_module", "desc": "Product's module version",
                "parser": props_parser_str},
    "AT+CSUB_B": {"name": "version_chip", "desc": "Product's chip version",
                  "parser": props_parser_str},
    "AT+CGMR": {"name": "version_firmware",
                "desc": "Product's firmware version",
                "parser": props_parser_str},
    "AT+CSQ_rssi": {"name": "network_signal_quality_rssi",
                    "desc": "Cellular network quality as signal strength "
                            "indication <rssi>",
                    "parser": props_parser_int},
    "AT+CSQ_ber": {"name": "network_signal_quality_ber",
                   "desc": "Cellular network quality as channel bit error "
                           "rate <ber>",
                   "parser": props_parser_int},
    "AT+CREG": {"name": "network_status_code", "desc": "Network status code",
                "parser": props_parser_network_status_code},
    "AT+CPIN": {"name": "network_sim_status_code", "desc": "SIM status code",
                "parser": props_parser_sim_status_code},
    "AT+COPS": {"name": "network_sim_provider", "desc": "SIM provider",
                "parser": props_parser_sim_provider},

    "CGPSINFO_lat_dir": {"name": "pos_gps_lat_dir",
                         "desc": "GPS latitude (N/S)",
                         "parser": props_parser_lat},
    "CGPSINFO_lat_degrees": {"name": "pos_gps_lat_degrees",
                             "desc": "GPS latitude in decimal degrees",
                             "parser": props_parser_gpsinfo_coordinates},
    "CGPSINFO_log_dir": {"name": "pos_gps_log_dir",
                         "desc": "GPS longitude (E/W)",
                         "parser": props_parser_lon},
    "CGPSINFO_log_degrees": {"name": "pos_gps_log_degrees",
                             "desc": "GPS longitude in decimal degrees",
                             "parser": props_parser_gpsinfo_coordinates},
    "CGPSINFO_alt": {"name": "pos_gps_alt",
                     "desc": "GPS position MSL Altitude. Unit is meters.",
                     "parser": props_parser_float},
    "CGPSINFO_speed": {"name": "pos_gps_speed",
                       "desc": "GPS position Speed Over Ground. Unit is knots.",
                       "parser": props_parser_float},
    "CGPSINFO_course": {"name": "pos_gps_course",
                        "desc": "GPS position course in degrees",
                        "parser": props_parser_float},

    "CGNSSINFO_lat_dir": {"name": "pos_gnss_lat_dir",
                          "desc": "GNSS latitude (N/S)",
                          "parser": props_parser_lat},
    "CGNSSINFO_lat_degrees": {"name": "pos_gnss_lat_degrees",
                              "desc": "GNSS latitude in decimal degrees",
                              "parser": props_parser_gpsinfo_coordinates},
    "CGNSSINFO_log_dir": {"name": "pos_gnss_log_dir",
                          "desc": "GNSS longitude (E/W)",
                          "parser": props_parser_lon},
    "CGNSSINFO_log_degrees": {"name": "pos_gnss_log_degrees",
                              "desc": "GNSS longitude in decimal degrees",
                              "parser": props_parser_gpsinfo_coordinates},
    "CGNSSINFO_alt": {"name": "pos_gnss_alt",
                      "desc": "GNSS position MSL Altitude. Unit is meters.",
                      "parser": props_parser_float},
    "CGNSSINFO_speed": {"name": "pos_gnss_speed",
                        "desc": "GNSS position Speed Over Ground. Unit is "
                                "knots.",
                        "parser": props_parser_float},
    "CGNSSINFO_course": {"name": "pos_gnss_course",
                         "desc": "GNSS position course in degrees.",
                         "parser": props_parser_float},

    "CGNSSINFO_pdop": {"name": "pos_gnss_pdop",
                       "desc": "Position Dilution Of Precision.",
                       "parser": props_parser_float},
    "CGNSSINFO_hdop": {"name": "pos_gnss_hdop",
                       "desc": "Horizontal Dilution Of Precision.",
                       "parser": props_parser_float},
    "CGNSSINFO_vdop": {"name": "pos_gnss_vdop",
                       "desc": "Vertical Dilution Of Precision.",
                       "parser": props_parser_float},

    "CGNSSINFO_mode": {"name": "pos_gnss_mode",
                       "desc": "Fix mode 2=2D fix 3=3D fix",
                       "parser": props_parser_int},
    "CGNSSINFO_sat_gps_count": {"name": "pos_gnss_sat_gps_count",
                                "desc": "GPS satellite valid numbers scope: "
                                        "00-12",
                                "parser": props_parser_int},
    "CGNSSINFO_sat_glonass_count": {"name": "pos_gnss_sat_glonass_count",
                                    "desc": "GLONASS satellite valid numbers "
                                            "scope: 00-12",
                                    "parser": props_parser_int},
    "CGNSSINFO_sat_beidou_count": {"name": "pos_gnss_sat_beidou_count",
                                   "desc": "BEIDOU satellite valid numbers "
                                           "scope: 00-12",
                                   "parser": props_parser_int},

    "power_module_state": {"name": "power_module_state",
                           "desc": "State of the module: true is power on, "
                                   "otherwise is power off",
                           "parser": props_parser_bool},
}

CALC_PROPS_CODES = {
    # N/A
    "network_registration": {"depends_on": "network_status_code",
                "calculator": calc_network_registration},
    "network_searching": {"depends_on": "network_status_code",
                "calculator": calc_network_searching},
    "network_roaming": {"depends_on": "network_status_code",
                "calculator": calc_network_roaming},
    "network_sim_status": {"depends_on": "network_sim_status_code",
                "calculator": calc_network_sim_status},
    "pos_gnss_sat_count": {"depends_on": "pos_gnss_sat_gps_count",
                "calculator": calc_pos_gnss_sat_count},
}
