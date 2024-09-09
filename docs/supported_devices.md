# FW SIM 7600 - Supported devices

This firmware works with all SIM7600 series devices.

During the device initialization, this script uses the response of the `AT+CGMM`
command as the **product PID of the connected device**.
The **device information is then retrieved from the PID mapping** in the
[mappings.py](/fw_sim7600/sim7600/mappings.py) file, this file is based on
the [Devices by MODEL](#devices-by-model) tables.<br/>
Then, those info are used to initialize the DBus object with the correspondent
DBus iface and description. Both, the iface and the object description are
defined into the `PID` mapping.

* `model`: human-readable name of the exact model
* `type`: devices code to group similar devices
  from [_definitions.py](/fw_sim7600/sim7600/_definitions.py) as `DEV_TYPE_*`
* `dbus_iface`: a string defining the DBus iface<br/>
  from [_definitions.py](/fw_sim7600/sim7600/_definitions.py) as `DEV_IFACE_*`
* `dbus_desc`: a string defining the DBus object's description<br/>
  [dbus_definitions.py](/fw_sim7600/sim7600/_dbus_descs.py) as `DEV_DBUS_DESC_*`

## Device types

Here, you can find the list of all devices types available. Any product MODEL
from [Devices by MODEL](#devices-by-model) section is mapped into a device type
using the `PID` table from the [mappings.py](/fw_sim7600/sim7600/mappings.py)
file.
More details on DBus definitions and their properties can be found on
the [Values Mapping](values_mapping.md#properties-by-dbus-object-description)
page.

| Type's Constant    | Type's Name | DBus's Iface          | DBus's Description      |
|--------------------|-------------|-----------------------|-------------------------|
| `DEV_TYPE_SIM7600` | SIM7600     | com.waveshare.sim7600 | `DEV_DBUS_DESC_SIM7600` |

## Devices by MODEL

At the current version, any `SIMCOM_SIM7600E-H` model is supported. To support
more models, please update the `PID` table into
the [mappings.py](/fw_sim7600/sim7600/mappings.py) file.
