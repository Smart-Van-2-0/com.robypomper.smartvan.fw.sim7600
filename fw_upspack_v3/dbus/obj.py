#!/usr/bin/python3

import logging
from pydbus.generic import signal

from fw_upspack_v3.ups.mappings import *


logger = logging.getLogger()


class DBusObject:

    PropertiesChanged = signal()

    def __init__(self, dbus_name, pid, dbus_obj_path=None, dbus_iface=None, enable_cache=False):
        if pid not in PID:
            raise NotImplementedError("Device with '{}' DEV_ID not implemented."
                                      .format(pid))

        self._cached_properties = {} if enable_cache else None

        self.dbus_name = dbus_name
        self.dbus_obj_path = dbus_obj_path
        self.dbus_iface = dbus_iface if dbus_iface is not None else PID[pid]['dbus_iface']

        dbus_obj_definition = PID[pid]['dbus_desc']
        if dbus_obj_definition is None:
            raise NotImplementedError("Device model '{}' with '{}' PID not implemented."
                                      .format(PID[pid].model, pid))
        self.dbus_desc = dbus_obj_definition.format(dbus_iface=self.dbus_iface)

    def publish(self, dbus):
        logger.info(
            "Publish DBus '{}' interface on '{}' DBus and '{}' object path.".format(
                self.dbus_iface, self.dbus_name, self.dbus_obj_path if self.dbus_obj_path is not None else ""))
        dbus_obj_pub = self.dbus_obj_path, self, self.dbus_desc
        dbus.publish(self.dbus_name, dbus_obj_pub)

    def update_property(self, property_name, value):
        if self._cached_properties is not None:
            if property_name in self._cached_properties:
                if self._cached_properties[property_name] == value:
                    return
            self._cached_properties[property_name] = value

        logger.debug("Object '{}' property update '{}.{} = {}'."
                     .format(self.dbus_obj_path, self.dbus_iface, property_name, value))
        try:
            self.PropertiesChanged(self.dbus_iface, {property_name: value}, [])
        except KeyError as err:
            raise NameError("Property {} not registered on current DBUs iface".format(err)) from err
