import logging

class Settings:

    # Group of the current script (default: None)
    FW_GROUP = "fw_group"
    # Version of the current script (default: None)
    FW_NAME = "fw_name"
    # Description of the current script (default: None)
    FW_VERSION = "fw_version"
    # Name of the current script (default: None)
    FW_DESC = "fw_desc"

    # Value to use as default serial port (default: "/dev/ttyS0")
    PARAM_SERIAL_PORT = "param_serial_port"
    # Value to use as default serial port speed (default: 115200)
    PARAM_SERIAL_SPEED = "param_serial_speed"
    # Value to use as default DBus name (default: "com.fw_dbus")
    PARAM_DBUS_NAME = "param_dbus_name"
    # Value to use as default DBus object path (default: None)
    PARAM_DBUS_OBJ_PATH = "param_dbus_obj_path"
    # Value to use as default DBus object interface (default: None)
    PARAM_DBUS_IFACE = "param_dbus_iface"

    # Enable local cache for properties (default: True)
    CACHE_ENABLE = "cache_enable"
    # Maximum time a property can be stored on the cache before sending his value again. (default: 300)
    CACHE_TIME_TO_RESET = "cache_time_to_reset"

    # Log level for console messages (default: logging.WARN)
    LOGGER_CONSOLE_LEVEL = "logger_console_level"
    # Format for logging messages on console (default: "(%(asctime)s) [%(levelname)-7s] %(message)s")
    LOGGER_CONSOLE_FORMAT = "logger_console_format"
    # Format for logging date on console (default: "%Y-%m-%d %H:%M:%S")
    LOGGER_CONSOLE_DATE_FORMAT = "logger_console_format_date"
    # Format for logging messages on DEV mode (default: "[%(levelname)-7s] (%(asctime)s) %(filename)s::%(lineno)d %(message)s")
    LOGGER_CONSOLE_DEV_FORMAT = "logger_console_dev_format"
    # Format for logging date on DEV mode (default: "%H:%M:%S")
    LOGGER_CONSOLE_DEV_DATE_FORMAT = "logger_console_dev_format_date"
    # Directory name where store log files (default: "logs/")
    LOGGER_FILE_FOLDER = "logger_file_folder"
    # Log level for file messages (default: logging.INFO)
    LOGGER_FILE_LEVEL = "logger_file_level"
    # Format for logging messages on file (default: "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    LOGGER_FILE_FORMAT = "logger_file_format"
    # Format for logging date on file (default: "%Y-%m-%d %H:%M:%S")
    LOGGER_FILE_DATE_FORMAT = "logger_file_format_date"

    # Seconds between each device connection retry (default: 5)
    DEV_CONN_RETRY = "dev_connection_retry"
    # Seconds between each publish retry (default: 30)
    DEV_PUBLISH_RETRY_SLEEP = "dev_publish_retry_sleep"

    # Seconds between each main loop iteration (default: 10)
    MAIN_LOOP_SLEEP = "main_loop_sleep"

    # Exit code for success (default: 0)
    EXIT_SUCCESS = "exit_success"
    # Exit code for termination during initialization (default: 1)
    EXIT_INIT_TERMINATED = "exit_init_terminated"
    # Exit code for initialization error (default: 2)
    EXIT_INIT_ERROR_DEV = "exit_init_error_dev"
    # Exit code for DBus initialization error (default: 3)
    EXIT_INIT_ERROR_DBUS = "exit_init_error_dbus"

    def __init__(self, values: dict):
        self.custom_vals = values
        self.default_vals = DEFAULT_SETTINGS

    def _get_setting(self, key):
        val = self.custom_vals.get(key, self.default_vals.get(key, None))
        if val is None:
            raise ValueError("Option '{}' not found".format(key))
        return val

    def __getattr__(self, name):
        if name.startswith("get_"):
            key = name[4:].upper()
            if hasattr(self, key):
                return self._get_setting(getattr(self, key))
        raise AttributeError(f"'Settings' object has no attribute '{name}'")


DEFAULT_SETTINGS = {
    Settings.FW_GROUP: None,
    Settings.FW_NAME: None,
    Settings.FW_VERSION: None,
    Settings.FW_DESC: None,

    Settings.PARAM_SERIAL_PORT: "/dev/ttyS0",
    Settings.PARAM_SERIAL_SPEED: 115200,
    Settings.PARAM_DBUS_NAME: "com.fw_dbus",
    Settings.PARAM_DBUS_OBJ_PATH: None,
    Settings.PARAM_DBUS_IFACE: None,

    Settings.CACHE_ENABLE: True,
    Settings.CACHE_TIME_TO_RESET: 300,

    Settings.LOGGER_CONSOLE_LEVEL: logging.WARN,
    Settings.LOGGER_CONSOLE_FORMAT: "(%(asctime)s) [%(levelname)-7s] %(message)s",
    Settings.LOGGER_CONSOLE_DATE_FORMAT: "%Y-%m-%d %H:%M:%S",
    Settings.LOGGER_CONSOLE_DEV_FORMAT: "[%(levelname)-7s] (%(asctime)s) %(filename)s::%(lineno)d %(message)s",
    Settings.LOGGER_CONSOLE_DEV_DATE_FORMAT: "%H:%M:%S",
    Settings.LOGGER_FILE_FOLDER: "logs/",
    Settings.LOGGER_FILE_LEVEL: logging.INFO,
    Settings.LOGGER_FILE_FORMAT: "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    Settings.LOGGER_FILE_DATE_FORMAT: "%Y-%m-%d %H:%M:%S",

    Settings.DEV_CONN_RETRY: 5,
    Settings.DEV_PUBLISH_RETRY_SLEEP: 30,

    Settings.MAIN_LOOP_SLEEP: 10,

    Settings.EXIT_SUCCESS: 0,
    Settings.EXIT_INIT_TERMINATED: 1,
    Settings.EXIT_INIT_ERROR_DEV: 2,
    Settings.EXIT_INIT_ERROR_DBUS: 3
}
