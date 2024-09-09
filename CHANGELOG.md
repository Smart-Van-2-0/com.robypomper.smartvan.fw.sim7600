# FW SIM 7600 - Changelog

[README](README.md) | [CHANGELOG](CHANGELOG.md) | [TODOs](TODOs.md) | [LICENCE](LICENCE.md)


## Version 1.0.1

* Fixed wrong links in docs
* Updated base firmware: repoSync
* Fixed properties: pos_gps_lat_degrees,  pos_gps_lat_dir
* Added property: pos_gnss_sat_count
* Fixed property: network_sim_status
* Added properties: network_sim_provider, network_status_code (reg/search/roaming), network_signal_quality
* Added all SIM7600 series models to the mappings
* Various fixes on simulator and parsers
* Fixed HALT signal handling

You can find the logs of this version into the [docs/logs](docs/logs) folder.

## Version 1.0.0

* Copied files from the [com.robypomper.smartvan.fw.upspack_v3](https://github.com/Smart-Van-2-0/com.robypomper.smartvan.fw.upspack_v3) repo
* Implemented Device class for SIM 7600 over serial (UART)
