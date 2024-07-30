#!/usr/bin/python3

# List of supported devices' types
# Strings used as default value to populate the PID dict

DEV_TYPE_SIM7600 = "SIM7600"


# List of supported dbus ifaces
# Strings used as default value to populate the PID dict

DEV_IFACE_SIM7600 = "com.waveshare.sim7600"


# Definitions for supported data types

SIM_STATUSES = {
    0: {'name': "Unknown", 'vals': []},
    1: {'name': "Ready", 'vals': ["READY"]},
    2: {'name': "Missing Config", 'vals': ["SIM PIN",
                                           "SIM PUK",
                                           "PH-SIM PIN",
                                           "SIM PIN2",
                                           "SIM PUK2",
                                           "PH-NET PIN"]},
}
SIM_STATUSES_UNKNOWN_KEY = 0
SIM_STATUSES_WORKING_KEY = 1