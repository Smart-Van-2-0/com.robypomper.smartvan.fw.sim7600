# FW SIM 7600 - TODOs

[README](README.md) | [CHANGELOG](CHANGELOG.md) | [TODOs](TODOs.md) | [LICENCE](LICENCE.md)

* Optimize power consumption switching ON/OFF the module when not in use
* Add a DBUS method to select the default GNSS system (GPS, GLONASS, GALILEO, BEIDOU)
  At the same time it must expose GNSS agnostic properties (like `pos_lat` insted of `pos_gps_lat`)
