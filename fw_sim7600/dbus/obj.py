#!/usr/bin/python3

import logging
from pydbus.generic import signal


logger = logging.getLogger()


class DBusObject:

    PropertiesChanged = signal()

    def __init__(self, main_obj, dbus_name, dbus_obj_path, dbus_iface, dbus_obj_definition, enable_cache=False):
        self._obj = main_obj
        self.dbus_name = dbus_name
        self.dbus_obj_path = dbus_obj_path
        self.dbus_iface = dbus_iface
        self.dbus_obj_definition = dbus_obj_definition
        self._cached_properties = {} if enable_cache else None

    def publish(self, dbus):
        logger.info(
            "Publish DBus '{}' interface on '{}' DBus and '{}' object path.".format(
                self.dbus_iface, self.dbus_name, self.dbus_obj_path if self.dbus_obj_path is not None else ""))
        dbus_obj_pub = self.dbus_obj_path, self, self.dbus_obj_definition
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

    def __getattr__(self, attr):
        if attr not in self.__dict__:
            return getattr(self._obj, attr)
        return super().__getattr__(attr)
