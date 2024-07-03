# FW SIM 7600 - Values Mapping

The properties exposed on the DBus vary depending on
the [type of device](supported_devices.md). A description of the
DBus object to be exposed is defined for each type of device. The DBus object
definitions are specified in the
[_dbus_descs.py](/fw_sensehat/sense/_dbus_descs.py) file.

During the `main_loop`, this script refresh the device's data and parse any
property found, if the property value is update the script sends the property
update to the DBus. To parse the property it uses the info contained into
the`PROPS_CODE` table. Sometime, it can trigger an exception because the updated
property is not present into the DBus object definitions. In this case add the
property to the DBus object definitions or fix the `PROPS_CODES` table.

## DBus properties

Exposed properties can be of two types: direct or calculated. Direct properties
are exported as they come from the device. Calculated properties are the result
of an elaboration.

### Direct

Direct properties are defined into the `PROPS_CODES` table into
the [mappings.py](/fw_victron/mappings.py) file.

For each property are defined following fields:

* `KEY`: property name on device side
* `name`: property name on DBus
* `desc`: human-readable description of the property
* `parser`: the method to use to parse the value read from the device

| Prop.'s KEY                   | Prop.'s Name on DBus          | Description                                                   | Parser method        |
|-------------------------------|-------------------------------|---------------------------------------------------------------|----------------------|
| `AT+CGMI`                     | `manufacturer`                | Product's manufacturer                                        | `props_parser_str`   |
| `AT+CGMM`                     | `model`                       | Product's model                                               | `props_parser_str`   |
| `AT+CGSN`                     | `serial_number`               | Product's serial number                                       | `props_parser_str`   |
| `AT+CSUB`                     | `version_module`              | Product's module version                                      | `props_parser_str`   |
| `AT+CSUB_B`                   | `version_chip`                | Product's chip version                                        | `props_parser_str`   |
| `AT+CGMR`                     | `version_firmware`            | Product's firmware version                                    | `props_parser_str`   |
| `AT+CSQ_rssi`                 | `network_signal_quality_rssi` | Cellular network quality as signal strength indication <rssi> | `props_parser_int`   |
| `AT+CSQ_ber`                  | `network_signal_quality_ber`  | Cellular network quality as .channel bit error rate <ber>     | `props_parser_int`   |
| `AT+CPIN`                     | `network_sim_status`          | SIM status                                                    | `props_parser_str`   |
| `CGPSINFO_lat_dir`            | `pos_gps_lat_dir`             | GPS latitude (N/S)"                                           | `props_parser_str`   |
| `CGPSINFO_lat_degrees`        | `pos_gps_lat_degrees`         | GPS latitude degrees                                          | `props_parser_float` |
| `CGPSINFO_log_dir`            | `pos_gps_log_dir`             | GPS longitude (E/W)                                           | `props_parser_str`   |
| `CGPSINFO_log_degrees`        | `pos_gps_log_degrees`         | GPS longitude degrees                                         | `props_parser_float` |
| `CGPSINFO_alt`                | `pos_gps_alt`                 | GPS position MSL Altitude. Unit is meters.                    | `props_parser_float` |
| `CGPSINFO_speed`              | `pos_gps_speed`               | GPS position Speed Over Ground. Unit is knots.                | `props_parser_float` |
| `CGPSINFO_course`             | `pos_gps_course`              | GPS position course in degrees                                | `props_parser_float` |
| `CGNSSINFO_lat_dir`           | `pos_gnss_lat_dir`            | GNSS latitude (N/S)                                           | `props_parser_str`   |
| `CGNSSINFO_lat_degrees`       | `pos_gnss_lat_degrees`        | GNSS latitude degrees                                         | `props_parser_float` |
| `CGNSSINFO_log_dir`           | `pos_gnss_log_dir`            | GNSS longitude (E/W)                                          | `props_parser_str`   |
| `CGNSSINFO_log_degrees`       | `pos_gnss_log_degrees`        | GNSS longitude degrees                                        | `props_parser_float` |
| `CGNSSINFO_alt`               | `pos_gnss_alt`                | GNSS position MSL Altitude. Unit is meters.                   | `props_parser_float` |
| `CGNSSINFO_speed`             | `pos_gnss_speed`              | GNSS position Speed Over Ground. Unit is knots.               | `props_parser_float` |
| `CGNSSINFO_course`            | `pos_gnss_course`             | GNSS position course in degrees.                              | `props_parser_float` |
| `CGNSSINFO_pdop`              | `pos_gnss_pdop`               | Position Dilution Of Precision.                               | `props_parser_float` |
| `CGNSSINFO_hdop`              | `pos_gnss_hdop`               | Horizontal Dilution Of Precision.                             | `props_parser_float` |
| `CGNSSINFO_vdop`              | `pos_gnss_vdop`               | Vertical Dilution Of Precision.                               | `props_parser_float` |
| `CGNSSINFO_mode`              | `pos_gnss_mode`               | Fix mode 2=2D fix 3=3D fix                                    | `props_parser_int`   |
| `CGNSSINFO_sat_gps_count`     | `pos_gnss_sat_gps_count`      | GPS satellite valid numbers scope: 00-12                      | `props_parser_int`   |
| `CGNSSINFO_sat_glonass_count` | `pos_gnss_sat_glonass_count`  | GLONASS satellite valid numbers scope: 00-12                  | `props_parser_int`   |
| `CGNSSINFO_sat_beidou_count`  | `pos_gnss_sat_beidou_count`   | BEIDOU satellite valid numbers scope: 00-12                   | `props_parser_int`   |
| `power_module_state`          | `power_module_state`          | State of the module: true is power on, otherwise is power off | `props_parser_bool`  |

Parser methods are defined into [_parsers.py](/fw_sensehat/sense/_parsers.py)
file. Depending on which DBus property's they are mapped for, they can return
different value's types.<br/>
Custom types are defined into
the [_definitions.py](/fw_sensehat/sense/_definitions.py) file.

### Calculated

Calculated properties are special values that can be elaborated starting from
other properties (also other calculated properties). When a property is updated,
the script checks if there is some calculated property that depends on it. If
any, then the script calculate the dependant property.

For each calculated property are defined following fields:

* `KEY`: calculated property name on DBus
* `name`: calculated property name (not used)
* `desc`: human-readable description of the property
* `depends_on`: the list of properties on which the current property depends
* `calculator`: the method to use to elaborate the property

| Prop.'s Name on DBus | Description | Depends on | Calculator method |
|----------------------|-------------|------------|-------------------|
| --                   | --          | --         | --                |

**No calculated properties are used from this script. **

All methods used to elaborate the properties, receives the properties cache as
param. So they can use that list to get all properties read from the device (
also other calculated properties).

## Properties by DBus Object description

This is the table containing all properties handled by this script. For each
property, the table define if it will be exported by the column's device type.

| Prop.'s Name on DBus          | Type   | SIM7600 |
|-------------------------------|--------|---------|
| `manufacturer`                | string | Yes     |
| `model`                       | string | Yes     |
| `serial_number`               | string | Yes     |
| `version_module`              | string | Yes     |
| `version_chip`                | string | Yes     |
| `version_firmware`            | string | Yes     |
| `network_signal_quality_rssi` | int    | Yes     |
| `network_signal_quality_ber`  | int    | Yes     |
| `network_sim_status`          | string | Yes     |
| `pos_gps_lat_dir`             | string | Yes     |
| `pos_gps_lat_degrees`         | double | Yes     |
| `pos_gps_log_dir`             | string | Yes     |
| `pos_gps_log_degrees`         | double | Yes     |
| `pos_gps_alt`                 | double | Yes     |
| `pos_gps_speed`               | double | Yes     |
| `pos_gps_course`              | double | Yes     |
| `pos_gnss_lat_dir`            | string | Yes     |
| `pos_gnss_lat_degrees`        | double | Yes     |
| `pos_gnss_log_dir`            | string | Yes     |
| `pos_gnss_log_degrees`        | double | Yes     |
| `pos_gnss_alt`                | double | Yes     |
| `pos_gnss_speed`              | double | Yes     |
| `pos_gnss_course`             | double | Yes     |
| `pos_gnss_pdop`               | double | Yes     |
| `pos_gnss_hdop`               | double | Yes     |
| `pos_gnss_vdop`               | double | Yes     |
| `pos_gnss_mode`               | int    | Yes     |
| `pos_gnss_sat_gps_count`      | int    | Yes     |
| `pos_gnss_sat_glonass_count`  | int    | Yes     |
| `pos_gnss_sat_beidou_count`   | int    | Yes     |
| `power_module_state`          | bool   | Yes     |

## DBus methods

This script exposes the following methods on the DBus:

| Method's Name on DBus | Description                | Type | SIM7600 |
|-----------------------|----------------------------|------|---------|
| `power_module`        | Power on or off the module | void | Yes     |
