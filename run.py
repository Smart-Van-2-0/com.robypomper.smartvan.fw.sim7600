#!/usr/bin/python3

import logging

from fw_sim7600.sim7600.device import Device
from fw_sim7600.sim7600.mappings import PID, PROPS_CODES, CALC_PROPS_CODES


from fw_sim7600.base.runner import DeviceRunner
from fw_sim7600.base.settings import Settings
from fw_sim7600.sim7600.simulator import DeviceSimulator

# default logger, used if _setup_logging() was not called
logger = logging.getLogger()

FW_SETTINGS = {
    # Group of the current script (default: None)
    Settings.FW_GROUP: "com.robypomper.smartvan.fw.sim7600",
    # Version of the current script (default: None)
    Settings.FW_VERSION: "1.0.2-DEV",
    # Description of the current script (default: None)
    Settings.FW_DESC: "Python script as FW SIM7600",
    # Name of the current script (default: None)
    Settings.FW_NAME: "FW SIM7600",

    # Value to use as default serial port (default: "/dev/ttyS0")
    Settings.PARAM_SERIAL_PORT: "/dev/ttyAMA0",
    # Value to use as default serial port speed (default: 115200)
    Settings.PARAM_SERIAL_SPEED: 115200,
    # Value to use as default DBus name (default: "com.fw_dbus")
    Settings.PARAM_DBUS_NAME: "com.waveshare.sim7600",
    # Value to use as default DBus object path (default: None)
    Settings.PARAM_DBUS_OBJ_PATH: "",
    # Value to use as default DBus object interface (default: None)
    Settings.PARAM_DBUS_IFACE: "",

    # Enable local cache for properties (default: True)
    Settings.CACHE_ENABLE: True,
    # Maximum time a property can be stored on the cache before sending his value again. (default: 300)
    Settings.CACHE_TIME_TO_RESET: 10 * 60,

    # Log level for console messages (default: logging.WARN)
    Settings.LOGGER_CONSOLE_LEVEL: logging.INFO,
    # Format for logging messages on console (default: "(%(asctime)s) [%(levelname)-7s] %(message)s")
    #Settings.LOGGER_CONSOLE_FORMAT: "(%(asctime)s) [%(levelname)-7s] %(message)s",
    # Format for logging date on console (default: "%Y-%m-%d %H:%M:%S")
    #Settings.LOGGER_CONSOLE_DATE_FORMAT: "%Y-%m-%d %H:%M:%S",
    # Format for logging messages on DEV mode (default: "[%(levelname)-7s] (%(asctime)s) %(filename)s::%(lineno)d %(message)s")
    #Settings.LOGGER_CONSOLE_DEV_FORMAT: "[%(levelname)-7s] (%(asctime)s) %(filename)s::%(lineno)d %(message)s",
    # Format for logging date on DEV mode (default: "%H:%M:%S")
    #Settings.LOGGER_CONSOLE_DEV_DATE_FORMAT: "%H:%M:%S",
    # Directory name where store log files (default: "logs/")
    #Settings.LOGGER_FILE_FOLDER: "logs",
    # Log level for file messages (default: logging.INFO)
    #Settings.LOGGER_FILE_LEVEL: logging.INFO,
    # Format for logging messages on file (default: "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    #Settings.LOGGER_FILE_FORMAT: "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # Format for logging date on file (default: "%Y-%m-%d %H:%M:%S")
    #Settings.LOGGER_FILE_DATE_FORMAT: "%Y-%m-%d %H:%M:%S",

    # Seconds between each device connection retry (default: 5)
    #Settings.DEV_CONN_RETRY: 5,
    # Seconds between each publish retry (default: 30)
    #Settings.DEV_PUBLISH_RETRY_SLEEP: 30,

    # Seconds that the main loop sleeps before next iteration (default: 10)
    #Settings.MAIN_LOOP_SLEEP: 10,

    # Exit value on success (default: 0)
    #Settings.EXIT_SUCCESS: 0,
    # Exit value on initialization halted by the user because the serial device not available (default: 1)
    #Settings.EXIT_INIT_TERMINATED: 1,
    # Exit value on Device initialization error (default: 2)
    #Settings.EXIT_INIT_ERROR_DEV: 2,
    # Exit value on DBus initialization error (default: 3)
    #Settings.EXIT_INIT_ERROR_DBUS: 3,
}

if __name__ == '__main__':

    def init_device_physical(device, speed, auto_refresh):
        return Device(device, speed, auto_refresh)


    def init_device_simulator(device, speed, auto_refresh):
        return DeviceSimulator(device, speed)


    r = DeviceRunner(init_device_physical, init_device_simulator,
                       FW_SETTINGS,
                       PID, PROPS_CODES, CALC_PROPS_CODES)
    args = r.cli_args()

    if args.version:
        if args.quiet:
            print(r.fw_version)
        else:
            print(r.fw_full_version)
        exit(0)

    if args.dev:
        args.debug = True
        args.quiet = False
    logger = r.init_logging(args.dev, args.debug, args.quiet)

    FW_SETTINGS[Settings.PARAM_DBUS_NAME] = args.dbus_name
    FW_SETTINGS[Settings.PARAM_DBUS_OBJ_PATH] = args.dbus_obj_path
    FW_SETTINGS[Settings.PARAM_DBUS_IFACE] = args.dbus_iface
    FW_SETTINGS[Settings.PARAM_SERIAL_PORT] = args.port
    FW_SETTINGS[Settings.PARAM_SERIAL_SPEED] = args.speed

    r.run(args.simulate, args.dev)
    exit(0)
