#!/usr/bin/python3


# noinspection PyPropertyDefinition
class DeviceAbs:
    """
    Device base classes.
    """

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
        raise NotImplementedError()

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
