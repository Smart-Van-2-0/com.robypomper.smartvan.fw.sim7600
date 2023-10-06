#!/usr/bin/python3

import os
import sys
import argparse
from datetime import datetime, timedelta
import time
import signal
from typing import Optional

from fw_sim7600.sim7600.device import Device
from fw_sim7600.sim7600.simulator import DeviceSimulator
from fw_sim7600.dbus.obj import DBusObject
from fw_sim7600.dbus.daemon import *
from fw_sim7600.sim7600.mappings import PROPS_CODES, CALC_PROPS_CODES

""" Name of the current script """
FW_NAME = "FW SIM7600"
""" Description of the current script """
FW_DESC = "Python script as {} firmware".format(FW_NAME)
""" Group of the current script """
FW_GROUP = "com.robypomper.smartvan.fw.sim7600"
""" Version of the current script """
FW_VERSION = "1.0.0-DEV"
""" Value to use as default serial port """
DEF_SERIAL_PORT = "/dev/ttyAMA0"
""" Value to use as default serial port speed """
DEF_SERIAL_SPEED = 115200
""" Value to use as default DBus name """
DEF_DBUS_NAME = "com.simcom"
""" Value to use as default DBus object path, if none  """
DEF_DBUS_OBJ_PATH = None
""" Value to use as default DBus object interface """
DEF_DBUS_IFACE = None
""" Maximum time a property can be stored on the cache before sending his value again. """
CACHE_TIME_TO_RESET = timedelta(hours=0, minutes=10, seconds=0)
""" Directory name where store log files """
LOGGER_FOLDER = "logs"
""" Log level for file messages """
LOGGER_FILE_LEVEL = logging.INFO
""" Format for logging messages """
LOGGER_FORMAT = "(%(asctime)s) [%(levelname)-7s] %(message)s"
""" Format for logging date"""
LOGGER_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
""" Format for logging messages on DEV mode"""
LOGGER_FORMAT_DEV = "[%(levelname)-7s] (%(asctime)s) %(filename)s::%(lineno)d %(message)s"
""" Format for logging date on DEV mode"""
LOGGER_DATE_FORMAT_DEV = "%H:%M:%S"
""" Seconds between each serial connection retry (on initialization but also on device disconnection """
CONN_RETRY = 5
""" Seconds that the main loop sleeps before next interation (print or update dbus object's value) """
LOOP_SLEEP = 1
""" Exit value on success (exit required by the user) """
EXIT_SUCCESS = 0
""" Exit value on initialization halted by the user because the serial device not available (required by the user) """
EXIT_INIT_TERMINATED = 1
""" Exit value on DBus initialization error """
EXIT_INIT_DBUS = 2

# default logger, used if _setup_logging() was not called
logger = logging.getLogger()
dev_global: Optional[Device] = None
must_shutdown = False
properties_cache = {}


def _full_version():
    """ Return a string containing the version, name and group from current script. """

    return "{} (Version: {})\n{}".format(FW_NAME, FW_VERSION, FW_GROUP)


def _cli_args():
    """ Configures, parses and returns arguments from cmd line. """

    parser = argparse.ArgumentParser(description=FW_DESC)
    group01 = parser.add_argument_group()
    group01.add_argument('--port', default=DEF_SERIAL_PORT,
                         help='Serial port')
    group01.add_argument('--speed', type=int, default=DEF_SERIAL_SPEED,
                         help='Serial port speed')
    group01.add_argument('--simulate', default=False, action="store_true", required=False,
                         help='Simulate a Device with id \'0xA060\'')

    group02 = parser.add_argument_group()
    group02.add_argument('--dbus-name', default=DEF_DBUS_NAME,
                         help='DBus name')
    group02.add_argument('--dbus-obj-path', default=DEF_DBUS_OBJ_PATH,
                         help='DBus object path (if None, the device type will be used, if empty nothing will be used)')
    group02.add_argument('--dbus-iface', default=DEF_DBUS_IFACE,
                         help='DBus object\'s interface')

    group03 = parser.add_argument_group()
    group03.add_argument("-v", "--version", action="store_true", required=False,
                         help="Show version and exit")

    group04 = parser.add_argument_group()
    group04.add_argument("--dev", action="store_true",
                         help="Enable development mode, increase logged messages info")
    group04.add_argument("--debug", action="store_true",
                         help="Set log level to debug")
    group04.add_argument("--quiet", action="store_true",
                         help="Set log level to error")

    return parser.parse_args()


def _init_logging(dev, debug, quiet):
    """ Init and configure logging system. """

    logger_format = LOGGER_FORMAT if not dev else LOGGER_FORMAT_DEV
    logger_date_format = LOGGER_DATE_FORMAT if not dev else LOGGER_DATE_FORMAT_DEV
    name_code = FW_NAME.lower().replace(' ', '_')
    now_date_time = datetime.today().strftime('%Y%m%d_%H%M%S')

    if not os.path.exists(LOGGER_FOLDER):
        os.mkdir(LOGGER_FOLDER)
    logging.basicConfig(level=LOGGER_FILE_LEVEL,
                        format=logger_format,
                        datefmt=logger_date_format,
                        filename=f'{LOGGER_FOLDER}/{name_code}-{now_date_time}.log')

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(logger_format)
    handler.setFormatter(formatter)
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    elif quiet:
        logging.getLogger().setLevel(logging.ERROR)
        handler.setLevel(logging.ERROR)

    logger.info(_full_version())
    logger.info("Execution mode: " + ("QUIET" if quiet else
                                      "DEV" if dev else
                                      "DEBUG" if debug else "NORMAL"))
    logger.info("Execution args: " + str(sys.argv[1:]))

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    return root_logger


def _init_device(port, speed, wait_connection=True, simulate_dev=False) -> Device:
    """ Init and configure Device. """

    global must_shutdown, dev_global

    if simulate_dev:
        logger.debug("Simulate device '{} at {}'...".format(port, speed))
        return DeviceSimulator(port, speed)

    logger.info("Connecting to '{} at {}'...".format(port, speed))
    dev = Device(port, speed, False)
    dev_global = dev
    logger.debug("Read first data from device at '{}' port...".format(port))
    dev.refresh()

    if must_shutdown:
        logger.warning("Received terminate signal during Device initialization, exit.")
    elif not dev.is_connected and wait_connection:
        logger.warning("Port '{}' not available, retry in {} seconds. Press (Ctrl+C) to exit.".format(port, CONN_RETRY))
        try:
            must_shutdown = False
            while not dev.is_connected and not must_shutdown:
                time.sleep(CONN_RETRY)
                dev.refresh()
                if not dev.is_connected:
                    logger.debug("Port '{}' still not available, retry in {} seconds.".format(port, CONN_RETRY))
        except KeyboardInterrupt:
            logger.info("Terminating required by the user.")
            exit(EXIT_INIT_TERMINATED)

    if dev.is_connected:
        logger.info("Connected to {} device model '{}'.".format("SIM7600", dev.device_pid))
    else:
        logger.info("Initialized Device at port '{}', but not connected.".format(port))
    return dev


def _init_dbus_object(dbus_name, dev_id, dbus_obj_path, dbus_iface) -> DBusObject:
    """ Init and configure DBus object. """

    try:
        return DBusObject(dbus_name, dev_id, dbus_obj_path, dbus_iface)
    except NotImplementedError as err:
        logger.fatal("Error initializing DBus object: {}".format(err))
        exit(EXIT_INIT_DBUS)


def _main_loop(dev, dbus_obj):
    """ Current script's main loop. """

    global must_shutdown

    # Main thread loop
    logger.info("Start {} Main Loop. Press (Ctrl+C) to quit.".format(FW_NAME))
    must_shutdown = False
    while not must_shutdown:
        try:
            dev.refresh(True)
            # print("{}/{}# [{}CONNECTED]: {}".format(dev.device_model, dev.device_serial,
            #                                        "" if dev.is_connected else "NOT ", dev.battery_volts))

            if len(dev.latest_data) == 0:
                logger.warning("No data read, nothing to update")
            else:
                for property_code in dev.latest_data:
                    _process_property(dev, dbus_obj, property_code)

        except KeyboardInterrupt:
            logger.info("Terminating required by the user.")
            must_shutdown = True
        except Exception as unknown_error:
            logger.error("Unknown error on Main Loop: {}".format(unknown_error))
            import traceback
            traceback.print_exc()

        try:
            time.sleep(LOOP_SLEEP if dev.is_connected else CONN_RETRY)

        except KeyboardInterrupt:
            logger.info("Terminating required by the user.")
            must_shutdown = True

    logger.info(FW_NAME + " Main Loop terminated.")


def _process_property(dev, dbus_obj, property_code):
    """
    Get and parse the Device's property and, if it used to elaborate a
    calculated value, the calculated value will be refreshed.
    """

    property_value_raw = dev.latest_data[property_code]
    try:
        property_name = PROPS_CODES[property_code]['name']
        property_parser = PROPS_CODES[property_code]['parser']
    except KeyError:
        logger.warning("Read unknown property code '{}' <{}>, skipped.".format(property_code, property_value_raw))
        return

    try:
        property_value = property_parser(property_value_raw)
        if property_name in properties_cache \
                and properties_cache[property_name]['value'] == property_value \
                and properties_cache[property_name]['time'] > datetime.now() - CACHE_TIME_TO_RESET:
            return
        properties_cache[property_name] = {
            'name': property_name,
            'value': property_value,
            'time': datetime.now()
        }
        dbus_obj.update_property(property_name, property_value)
        _update_property_derivatives(dbus_obj, property_name)

    except ValueError:
        logger.warning("Property '{}' <{}> raw value malformed, skipped.".format(property_name, property_value_raw))
    except TypeError:
        logger.warning("DBus property '{}' <{}> malformed, skipped.".format(property_name, property_value_raw))
    except KeyError:
        logger.warning("Property '{}' not used by current DBus object definition, skipped.".format(property_name))
    except KeyboardInterrupt as err:
        raise err
    except Exception as err:
        logger.warning("Unknown error on parsing and updating property '{}': [{}] {}"
                       .format(property_name, type(err), str(err)))
        import traceback
        traceback.print_exc()


def _update_property_derivatives(dbus_obj, property_name):
    """ Get and parse the Device's property and notify his update on DBus. """

    for c_property_name in CALC_PROPS_CODES:
        try:
            if property_name in CALC_PROPS_CODES[c_property_name]['depends_on']:
                c_property_value = CALC_PROPS_CODES[c_property_name]['calculator'](properties_cache)
                if c_property_value is None:
                    logger.debug("No value calculated for '{}', skipped".format(c_property_name))
                    continue

                # Check cached value
                if c_property_name in properties_cache \
                        and properties_cache[c_property_name]['value'] == c_property_value \
                        and properties_cache[c_property_name]['time'] > datetime.now() - CACHE_TIME_TO_RESET:
                    logger.debug("Value cached for '{}' <{}>".format(c_property_name, c_property_value))
                    continue

                # Update property's value
                properties_cache[c_property_name] = {
                    'name': c_property_name,
                    'value': c_property_value,
                    'time': datetime.now()
                }
                # Update property
                dbus_obj.update_property(c_property_name, c_property_value)
                _update_property_derivatives(dbus_obj, c_property_name)

        except Exception as err:
            logger.warning("Error calculating '{}' property: {}".format(c_property_name, err))
            # uncomment for calculators development
            # print("###################################")
            # import traceback
            # traceback.print_exc()
            # print("###################################")


def _register_kill_signals():
    signal.signal(signal.SIGINT, __handle_kill_signals)
    signal.signal(signal.SIGTERM, __handle_kill_signals)


def __handle_kill_signals(signo, _stack_frame):
    global must_shutdown

    logger.info("Received `{}` signal. Shutting down...".format(signo))
    # SIGINT    2   <= Ctrl+C
    # SIGTERM   15  <= kill PID
    if dev_global is not None:
        dev_global.terminate()
    must_shutdown = True


def main(port, speed, dbus_name, obj_path=None, dbus_iface=None, simulate_dev=False):
    """ Initialize a Device to read data and a DBus Object to share collected data. """
    _register_kill_signals()

    # Init Device
    try:
        dev = _init_device(port, speed, True, simulate_dev)
        if not dev.is_connected and must_shutdown:
            exit(0)
    except Exception as err:
        logger.warning("Error on initializing Device: " + str(err))
        import traceback
        traceback.print_exc()
        exit(-1)

    # Init DBus Object
    try:
        obj_path = obj_path if obj_path is not None else "/" + dev.device_type_code
        dev_id = dev.device_pid
        dbus_obj = _init_dbus_object(dbus_name, dev_id, obj_path, dbus_iface)
    except Exception as err:
        logger.warning("Error on initializing DBus Object: " + str(err))
        import traceback
        traceback.print_exc()
        exit(-1)

    # Publish on DBus
    try:
        os.environ['DISPLAY'] = "0.0"
        dbus = get_dbus()
    except Exception as err:
        logger.warning("Error on publish DBus Object: " + str(err))
        try:
            stop_dbus_thread()
        except:
            pass
        import traceback
        traceback.print_exc()
        exit(-1)

    start_dbus_thread()
    dbus_obj.publish(dbus)

    try:
        _main_loop(dev, dbus_obj)
    except Exception as err:
        logger.warning("Error on main thread: " + str(err))
        exit(-1)

    try:
        stop_dbus_thread()
    except Exception as err:
        logger.warning("Error on stopping DBus threads: " + str(err))


if __name__ == '__main__':
    args = _cli_args()

    if args.version:
        if args.quiet:
            print(FW_VERSION)
        else:
            print(_full_version())
        exit(EXIT_SUCCESS)

    if args.dev:
        args.debug = True
        args.quiet = False

    logger = _init_logging(args.dev, args.debug, args.quiet)
    main(args.port, args.speed, args.dbus_name, args.dbus_obj_path, args.dbus_iface, args.simulate)
    exit(EXIT_SUCCESS)
