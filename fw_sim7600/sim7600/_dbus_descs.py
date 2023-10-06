#!/usr/bin/python3

# List of supported DBus objects' definitions
# Strings used as default value to populate the PID dict

DEV_DBUS_DESC_UPSSmart = '''<node>
  <interface name='{dbus_iface}'>
    <property name="firmware_version" type="s" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="state_operation" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="battery_capacity" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="voltage_out" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    
  </interface>
</node>
'''
