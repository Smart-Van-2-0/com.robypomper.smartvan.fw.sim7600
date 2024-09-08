#!/usr/bin/python3
import os
import sys
import argparse
from datetime import datetime
import time
import logging

from fw_sim7600.base.settings import Settings
from fw_sim7600.base.device import DeviceAbs
from fw_sim7600.dbus.obj import DBusObject
from fw_sim7600.dbus.daemon import *

logger = logging.getLogger()


class DeviceRunner:

    def __init__(self, init_device_physical_method, init_device_simulator_method,
                 options: dict,
                 device_pids, properties_codes: list[dict], properties_calculated: list[dict]):
        self._init_device_physical = init_device_physical_method
        self._init_device_simulator = init_device_simulator_method
        self.settings = Settings(options)
        self.dev = None
        self.device_pids = device_pids
        self.properties_codes = properties_codes
        self.properties_calculated = properties_calculated
        self.properties_cache = {}

    @property
    def fw_name(self):
        """ Return the version from current script. """

        return self.settings.get_fw_name


    @property
    def fw_version(self):
        """ Return the version from current script. """

        return self.settings.get_fw_version


    @property
    def fw_full_version(self):
        """ Return a string containing the version, name and group from current script. """

        return "{}:{} (Version: {})".format(self.settings.get_fw_group,
                                            self.settings.get_fw_name,
                                            self.settings.get_fw_version)


    def cli_args(self):
        """ Configures, parses and returns arguments from cmd line. """

        parser = argparse.ArgumentParser(description=self.settings.get_fw_desc)
        group01 = parser.add_argument_group()
        group01.add_argument("--port", default=self.settings.get_param_serial_port,
                             help="Serial port name "
                                  "(default: {})".format(self.settings.get_param_serial_port))
        group01.add_argument("--speed", type=int, default=self.settings.get_param_serial_speed,
                             help="Serial port speed "
                                  "(default: {})".format(self.settings.get_param_serial_speed))
        group01.add_argument("--simulate", default=False,
                             action="store_true", required=False,
                             help="Simulate a UPS Pack V3 Device "
                                  "(default: False)")

        group02 = parser.add_argument_group()
        group02.add_argument("--dbus-name", default=self.settings.get_param_dbus_name,
                             help="DBus name to connect to "
                                  "(default: {})".format(self.settings.get_param_dbus_name))
        group02.add_argument("--dbus-obj-path", default=self.settings.get_param_dbus_obj_path,
                             help="DBus object path to use for object publication "
                                  "(Default: current device's `device_type_code`)")
        group02.add_argument("--dbus-iface", default=self.settings.get_param_dbus_iface,
                             help="DBus object\'s interface "
                                  "(Default: current device's `dbus_iface`)")

        group03 = parser.add_argument_group()
        group03.add_argument("-v", "--version", action="store_true", required=False,
                             help="Show version and exit")

        group04 = parser.add_argument_group()
        group04.add_argument("--dev", action="store_true",
                             help="Enable development mode, increase log messages")
        group04.add_argument("--debug", action="store_true",
                             help="Set log level to debug")
        group04.add_argument("--quiet", action="store_true",
                             help="Set log level to error")

        return parser.parse_args()


    def init_logging(self, dev, debug, quiet):
        """ Init and configure logging system. """

        fw_name = self.settings.get_fw_name
        fw_name_code = fw_name.lower().replace(' ', '_')
        now_date_time = datetime.today().strftime('%Y%m%d_%H%M%S')

        # setup logging file directory
        logger_file_folder = self.settings.get_logger_file_folder
        if not os.path.exists(logger_file_folder):
            os.mkdir(logger_file_folder)

        # setup logging file
        logging.basicConfig(level=self.settings.get_logger_file_level,
                            format=self.settings.get_logger_file_format,
                            datefmt=self.settings.get_logger_file_date_format,
                            filename=f'{logger_file_folder}/{fw_name_code}-{now_date_time}.log')

        logger_console_level = self.settings.get_logger_console_level if not debug and not quiet else logging.DEBUG if debug else logging.ERROR
        logger_console_format = self.settings.get_logger_console_format if not dev else self.settings.get_logger_console_dev_format
        logger_console_date_format = self.settings.get_logger_console_date_format if not dev else self.settings.get_logger_console_dev_date_format

        # setup logging console
        formatter = logging.Formatter(logger_console_format, datefmt=logger_console_date_format)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logger_console_level)
        handler.setFormatter(formatter)
        root_logger = logging.getLogger()
        root_logger.setLevel(logger_console_level)
        root_logger.addHandler(handler)

        logger.info(self.fw_full_version)
        logger.debug("Execution mode: " + ("QUIET" if quiet else
                                          "DEV" if dev else
                                          "DEBUG" if debug else "NORMAL"))
        logger.debug("Execution args: " + str(sys.argv[1:]))

        return root_logger


    def _init_device(self, wait_connection=True, simulate_dev=False) -> DeviceAbs:
        """ Init and configure Device. """

        #port = self.settings.get_param_serial_port
        #speed = self.settings.get_param_serial_speed

        if simulate_dev:
            logger.debug("Simulate device")
            #return DeviceSimulator(port, speed)
            return self._init_device_simulator()

        logger.info("Connecting to {} device...".format(self.fw_name))
        #dev = Device(port, speed, False)
        dev = self._init_device_physical()
        logger.debug("Read first data from device...")
        dev.refresh()

        if dev.must_terminate:
            logger.warning("Received terminate signal during Device initialization, exit.")
        elif not dev.is_connected and wait_connection:
            conn_retry = self.settings.get_dev_conn_retry
            logger.warning("Device not available, retry in {} seconds. Press (Ctrl+C) to exit.".format(conn_retry))
            try:
                while True:
                    time.sleep(conn_retry)
                    dev.refresh()
                    if not dev.is_connected and not dev.must_terminate:
                        logger.debug("Device still not available, retry in {} seconds.".format(conn_retry))
                    else:
                        break
            except KeyboardInterrupt:
                logger.info("Terminating required by the user.")
                exit(self.settings.get_exit_init_terminated)

        if dev.must_terminate:
            logger.warning("Terminating required by the user")
        elif dev.is_connected:
            logger.info("Connected to Device '{}'.".format(dev.device_pid))
        else:
            logger.info("Initialized Device, but not connected.")

        return dev


    @property
    def _device_pid_info(self):
        assert self.dev is not None
        assert self.dev.device_pid is not None
        dev_pid_info = self.device_pids[self.dev.device_pid]
        if dev_pid_info is None:
            raise NotImplementedError("Device PID '{}' not recognized".format(self.dev.device_pid))
        return dev_pid_info


    def _init_dbus_object(self) -> DBusObject:
        """ Init and configure DBus object. """

        assert self.dev is not None

        dbus_name = self.settings.get_param_dbus_name
        assert dbus_name != ""
        dev_id = self.dev.device_pid
        assert dev_id is not None
        dbus_obj_path = self.settings.get_param_dbus_obj_path
        dbus_obj_path = dbus_obj_path if dbus_obj_path != "" else "/" + self.dev.device_type_code
        dbus_iface = self.settings.get_param_dbus_iface
        dbus_iface = dbus_iface if dbus_iface != "" else self._device_pid_info['dbus_iface']
        dbus_obj_definition = self._device_pid_info['dbus_desc']
        if dbus_obj_definition is None:
            raise NotImplementedError("Device model '{}' with '{}' PID not implemented.".format(self._device_pid_info['model'], dev_id))
        dbus_obj_definition = dbus_obj_definition.format(dbus_iface=dbus_iface)

        try:
            return DBusObject(self.dev, dbus_name, dbus_obj_path, dbus_iface, dbus_obj_definition)
        except NotImplementedError as err:
            logger.fatal("Error initializing DBus object: {}".format(err))
            exit(self.settings.get_exit_init_error_dbus)


    def _publish_dbus_object(self, dbus, dbus_obj):
        assert self.dev is not None
        
        while not self.dev.must_terminate:
            try:
                dbus_obj.publish(dbus)
                break

            except Exception as err:
                if str(err).find("An object is already exported") == 0:
                    publish_retry_sleep = self.settings.get_dev_publish_retry_sleep
                    logger.debug("Object already published on DBus, retry in {} seconds.".format(publish_retry_sleep))
                    time.sleep(publish_retry_sleep)
                else:
                    raise RuntimeError("Can't publish the object on DBus") from err

        if self.dev.must_terminate:
            logger.warning("Received terminate signal during Object publication on DBus, exit.")


    def _internal_loop(self, dev, dbus_obj, development=False):
        """ Current script's main loop. """

        assert self.dev is not None

        # Main thread loop
        fw_name = self.settings.get_fw_name
        loop_sleep = self.settings.get_main_loop_sleep
        conn_retry = self.settings.get_dev_conn_retry
        logger.info("Start {} Main Loop. Press (Ctrl+C) to quit.".format(fw_name))
        while not self.dev.must_terminate:
            if loop_sleep > 0:
                logger.info("  ==== ==== ==== ====")
            logger.debug("Start fetch/pull device")

            try:
                dev.refresh(True)
                # print("{}/{}# [{}CONNECTED]: {}".format(dev.device_model, dev.device_serial,
                #                                        "" if dev.is_connected else "NOT ", dev.battery_volts))

                if len(dev.latest_data) == 0:
                    logger.warning("No data read, nothing to update")
                else:
                    for property_code in dev.latest_data:
                        self._process_property(dev, dbus_obj, property_code, development)

            except KeyboardInterrupt:
                logger.info("Terminating required by the user.")
                self.dev.terminate()
            except Exception as unknown_error:
                logger.error("Unknown error on Main Loop: {}, retry later".format(unknown_error))
                if development is True:
                    import traceback
                    traceback.print_exc()

            logger.debug("End fetch/pull device")

            sleepTime = loop_sleep if dev.is_connected else conn_retry
            try:
                for i in range(sleepTime):
                    if self.dev.must_terminate:
                        break
                    time.sleep(1)

            except KeyboardInterrupt:
                logger.info("Terminating required by the user.")
                self.dev.terminate()

        logger.info(fw_name + " Main Loop terminated.")


    def _process_property(self, dev, dbus_obj, property_code, development=False):
        """
        Get and parse the Device's property and, if it used to elaborate a
        calculated value, the calculated value will be refreshed.
        """

        property_value_raw = dev.latest_data[property_code]
        if property_value_raw is None:
            logger.warning("Property '{}' <raw value: {}> not available, skipped.".format(property_code, property_value_raw))
            return

        try:
            property_name = self.properties_codes[property_code]['name']
            property_parser = self.properties_codes[property_code]['parser']
        except KeyError:
            logger.warning("Read unknown property code '{}' <raw value: {}>, skipped.".format(property_code, property_value_raw))
            return

        try:
            cache_enable = self.settings.get_cache_enable
            cache_time_to_reset = self.settings.get_cache_time_to_reset
            property_value = property_parser(property_value_raw)

            # check if value is the same and it can be skipped
            if cache_enable \
                    and property_name in self.properties_cache \
                    and self.properties_cache[property_name]['value'] == property_value \
                    and (datetime.now() - self.properties_cache[property_name]['time']).total_seconds() < cache_time_to_reset:
                return

            self.properties_cache[property_name] = {
                'name': property_name,
                'value': property_value,
                'time': datetime.now()
            }
            dbus_obj.update_property(property_name, property_value)
            logger.info("R ==> {:<16} = '{}'".format(property_name, str(property_value)))
            self._update_property_derivatives(dbus_obj, property_name, development)

        except ValueError:
            logger.warning("Property '{}' <{}> raw value malformed, skipped.".format(property_name, property_value_raw))
            if development is True:
                import traceback
                traceback.print_exc()
        except TypeError:
            logger.warning("DBus property '{}' <{}> malformed, skipped.".format(property_name, property_value_raw))
            if development is True:
                import traceback
                traceback.print_exc()
        except KeyError:
            logger.warning("Property '{}' not used by current DBus object definition, skipped.".format(property_name))
            if development is True:
                import traceback
                traceback.print_exc()
        except KeyboardInterrupt as err:
            raise err
        except Exception as err:
            logger.warning("Unknown error on parsing and updating property '{}': [raw value: {}] {}"
                           .format(property_name, type(err), str(err)))
            if development is True:
                import traceback
                traceback.print_exc()


    def _update_property_derivatives(self, dbus_obj, property_name, development=False):
        """ Get and parse the Device's property and notify his update on DBus. """

        cache_enable = self.settings.get_cache_enable
        cache_time_to_reset = self.settings.get_cache_time_to_reset

        for c_property_name in self.properties_calculated:
            try:
                if property_name in self.properties_calculated[c_property_name]['depends_on']:
                    c_property_value = self.properties_calculated[c_property_name]['calculator'](self.properties_cache)
                    if c_property_value is None:
                        logger.debug("No value calculated for '{}', skipped".format(c_property_name))
                        continue

                    # Check cached value
                    if cache_enable \
                            and c_property_name in self.properties_cache \
                            and self.properties_cache[c_property_name]['value'] == c_property_value \
                            and (datetime.now() - self.properties_cache[c_property_name]['time']).total_seconds() < cache_time_to_reset:
                        logger.debug("Value cached for '{}' <{}>".format(c_property_name, c_property_value))
                        continue

                    # Update property's value
                    self.properties_cache[c_property_name] = {
                        'name': c_property_name,
                        'value': c_property_value,
                        'time': datetime.now()
                    }
                    # Update property
                    dbus_obj.update_property(c_property_name, c_property_value)
                    logger.info("C ==> {:<16} = '{}'".format(c_property_name, str(c_property_value)))
                    self._update_property_derivatives(dbus_obj, c_property_name)

            except Exception as err:
                logger.warning("Error calculating '{}' property: {}".format(c_property_name, err))
                if development is True:
                    import traceback
                    traceback.print_exc()


    def run(self, simulate_dev=False, development=False):
        """ Initialize a Device to read data and a DBus Object to share collected data. """
        
        if self.dev is not None:
            raise RuntimeError("Device {} already initialized" % self.dev.settings.get_fw_name)

        # Init Device
        try:
            self.dev = self._init_device(True, simulate_dev)
            if not self.dev.is_connected and self.dev.must_terminate:
                exit(0)
            if self.dev.device_type_code == "":
                logger.warning("Device not recognized, exit.")
                exit(-1)
        except Exception as err:
            logger.warning("Error on initializing Device: " + str(err))
            if development is True:
                import traceback
                traceback.print_exc()
            exit(-1)

        # Init DBus Object
        try:
            dbus_obj = self._init_dbus_object()
        except Exception as err:
            logger.warning("Error on initializing DBus Object: " + str(err))
            if development is True:
                import traceback
                traceback.print_exc()
            exit(-1)

        # Publish on init DBus
        try:
            os.environ['DISPLAY'] = "0.0"
            dbus = get_dbus()
        except Exception as err:
            logger.warning("Error on init DBus: " + str(err))
            import traceback
            traceback.print_exc()
            exit(-1)

        start_dbus_thread()

        # Publish on DBus
        try:
            self._publish_dbus_object(dbus, dbus_obj)
        except Exception as err:
            logger.warning("Error on publish DBus Object: " + str(err))
            try:
                stop_dbus_thread()
            except:
                pass
            import traceback
            traceback.print_exc()
            exit(-1)

        try:
            self._internal_loop(self.dev, dbus_obj, development)
        except Exception as err:
            logger.warning("Error on main thread: " + str(err))
            exit(-1)

        try:
            stop_dbus_thread()
        except Exception as err:
            logger.warning("Error on stopping DBus threads: " + str(err))
