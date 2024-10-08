#!/usr/bin/python3

# List of supported DBus objects' definitions
# Strings used as default value to populate the PID dict

DEV_DBUS_DESC_SIM7600 = '''<node>
  <interface name='{dbus_iface}'>
    <property name="manufacturer" type="s" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="model" type="s" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="serial_number" type="s" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="version_module" type="s" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="version_chip" type="s" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="version_firmware" type="s" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="network_signal_quality_rssi" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="network_signal_quality_ber" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="network_signal_quality" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="network_registration" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="network_searching" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="network_roaming" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="network_status_code" type="i" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="network_sim_status" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="network_sim_status_code" type="i" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="network_sim_provider" type="s" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    
    <property name="pos_gps_lat_dir" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gps_lat_degrees" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gps_log_dir" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gps_log_degrees" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gps_alt" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gps_speed" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gps_course" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    
    <property name="pos_gnss_lat_dir" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_lat_degrees" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_log_dir" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_log_degrees" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_alt" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_speed" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_course" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_pdop" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_hdop" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_vdop" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_mode" type="i" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_sat_count" type="i" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_sat_gps_count" type="i" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_sat_glonass_count" type="i" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <property name="pos_gnss_sat_beidou_count" type="i" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    
    <property name="power_module_state" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal"
       value="true"/>
    </property>
    <method name="power_module">
      <arg direction="in" name="value" type="b"/>
    </method>
    
  </interface>
</node>
'''
