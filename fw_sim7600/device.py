#!/usr/bin/python3

import signal


# noinspection PyPropertyDefinition
class DeviceAbs:
    """
    Device base classes.
    """

    def __init__(self):
        self._must_terminate = False
        self._register_kill_signals()

    def refresh(self, reset_data=False):
        """
        Refresh latest data querying them to the device, if `reset_data` is true,
        then default-Zero values are set.
        """
        raise NotImplementedError()

    @property
    def is_connected(self) -> bool:
        """ Returns True if at last refresh attempt the serial device was available. """
        raise NotImplementedError()

    @property
    def is_reading(self) -> bool:
        """ Returns the local device (eg: '/dev/ttyUSB0') used to connect to the serial device """
        raise NotImplementedError()

    def terminate(self):
        """
        Send the terminate signal to all device process and loops.
        """
        self._must_terminate = True

    @property
    def must_terminate(self) -> bool:
        """ Returns True if the device must terminate the current operation and disconnect """
        return self._must_terminate

    def _register_kill_signals(self):
        signal.signal(signal.SIGINT, self.__handle_kill_signals)
        signal.signal(signal.SIGTERM, self.__handle_kill_signals)

    def __handle_kill_signals(self, signo, _stack_frame):
        print("Device received `{}` signal. Shutdown device...".format(signo))
        # SIGINT    2   <= Ctrl+C
        # SIGTERM   15  <= kill PID
        self.terminate()

    @property
    def device_pid(self) -> "str | None":
        """
        Returns the device PID, it can be used as index for the PID dict.
        """
        raise NotImplementedError()

    @property
    def device_type(self) -> str:
        """ Returns the device type """
        raise NotImplementedError()

    @property
    def device_type_code(self) -> str:
        """ Returns the device type as a code string"""
        raise NotImplementedError()

    @property
    def latest_data(self) -> dict:
        raise NotImplementedError()
