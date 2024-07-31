#!/usr/bin/python3
import logging

from fw_sim7600.sim7600.device import Device
from fw_sim7600.sim7600.mappings import *
from fw_sim7600.commons import regenerateValueMaxMin


logger = logging.getLogger()


class DeviceSimulator(Device):

    def __init__(self, device: str = '/dev/ttyAMA0', speed: int = 9600):
        super().__init__(device, speed, False)
        self._data = {
            'AT+CGMI': 'SIMCOM INCORPORATED',
            'AT+CGMM': 'SIMCOM_SIM7600E-H',
            'AT+CGSN': '860147054839863',
            'AT+CSUB': 'B04V03',
            'AT+CSUB_B': 'MDM9x07_LE20_S_22_V1.03_210527',
            'AT+CGMR': 'LE20B04SIM7600M22',
            'AT+CSQ_rssi': '2',
            'AT+CSQ_ber': '50',
            'AT+CPIN': '+CPIN: READY',
            'AT+COPS': '+COPS: 0,0,"China Mobile Com",0',
            'AT+CREG': '+CREG: 0, 0',
            'CGPSINFO_lat_degrees': '4629.837756',
            'CGPSINFO_lat_dir': 'N',
            'CGPSINFO_log_degrees': '01120.203911',
            'CGPSINFO_log_dir': 'E',
            'CGPSINFO_alt': '276.8',
            'CGPSINFO_speed': '0.0',
            'CGPSINFO_course': '-1',
            'CGNSSINFO_mode': '2',
            'CGNSSINFO_sat_gps_count': '06',
            'CGNSSINFO_sat_glonass_count': '04',
            'CGNSSINFO_sat_beidou_count': '00',
            'CGNSSINFO_lat_degrees': '4629.837221',       # 46°17'54.1"N
            'CGNSSINFO_lat_dir': 'N',
            'CGNSSINFO_log_degrees': '01120.204242',      # 11°12'15.3"E
            'CGNSSINFO_log_dir': 'E',
            'CGNSSINFO_alt': '274.9',
            'CGNSSINFO_speed': '0.0',
            'CGNSSINFO_course': '-1',
            'CGNSSINFO_pdop': '1.3',
            'CGNSSINFO_hdop': '1.0',
            'CGNSSINFO_vdop': '0.8',
            'power_module_state': str(self._power_state),
        }

    def refresh(self, reset_data=False) -> bool:
        if not self._power_state:
            return False

        self._data = {
            'AT+CGMI': 'SIMCOM INCORPORATED',
            'AT+CGMM': 'SIMCOM_SIM7600E-H',
            'AT+CGSN': '860147054839863',
            'AT+CSUB': 'B04V03',
            'AT+CSUB_B': 'MDM9x07_LE20_S_22_V1.03_210527',
            'AT+CGMR': 'LE20B04SIM7600M22',
            'AT+CSQ_rssi': regenerateValueMaxMin(self._data['AT+CSQ_rssi'], 1, 0, 199),
            'AT+CSQ_ber': regenerateValueMaxMin(self._data['AT+CSQ_ber'], 1, 0, 99),
            'AT+CPIN': '+CPIN: READY',
            'AT+COPS': '+COPS: 0,0,"China Mobile Com",0',
            'AT+CREG': '+CREG: 0, 0',
            'CGPSINFO_lat_degrees': regenerateValueMaxMin(self._data['CGPSINFO_lat_degrees'], 0.01, 0, 9000),
            'CGPSINFO_lat_dir': 'N',    # 'S' or "N" if random.randint(0, 1) else "N",
            'CGPSINFO_log_degrees': regenerateValueMaxMin(self._data['CGPSINFO_log_degrees'], 0.01, 0, 18000),
            'CGPSINFO_log_dir': 'E',    # 'W' or "E" if random.randint(0, 1) else "W",
            'CGPSINFO_alt': regenerateValueMaxMin(self._data['CGPSINFO_alt'], 0.1, 0, 500),
            'CGPSINFO_speed': regenerateValueMaxMin(self._data['CGPSINFO_speed'], 0.1, 0, 20),
            'CGPSINFO_course': regenerateValueMaxMin(self._data['CGPSINFO_course'], 0.1, 0, 360),
            'CGNSSINFO_mode': '2',      # '3' or "2" if random.randint(0, 1) else "3",
            'CGNSSINFO_sat_gps_count': regenerateValueMaxMin(self._data['CGNSSINFO_sat_gps_count'], 1, 0, 12),
            'CGNSSINFO_sat_glonass_count': regenerateValueMaxMin(self._data['CGNSSINFO_sat_glonass_count'], 1, 0, 12),
            'CGNSSINFO_sat_beidou_count': regenerateValueMaxMin(self._data['CGNSSINFO_sat_beidou_count'], 1, 0, 12),
            'CGNSSINFO_lat_degrees': regenerateValueMaxMin(self._data['CGNSSINFO_lat_degrees'], 0.01, 0, 9000),
            'CGNSSINFO_lat_dir': 'N',   # 'S' or "N" if random.randint(0, 1) else "N",
            'CGNSSINFO_log_degrees': regenerateValueMaxMin(self._data['CGNSSINFO_log_degrees'], 0.01, 0, 18000),
            'CGNSSINFO_log_dir': 'E',   # 'W' or "E" if random.randint(0, 1) else "W",
            'CGNSSINFO_alt': regenerateValueMaxMin(self._data['CGNSSINFO_alt'], 0.1, 0, 500),
            'CGNSSINFO_speed': regenerateValueMaxMin(self._data['CGNSSINFO_speed'], 0.1, 0, 20),
            'CGNSSINFO_course': regenerateValueMaxMin(self._data['CGNSSINFO_course'], 0.1, 0, 360),
            'CGNSSINFO_pdop': regenerateValueMaxMin(self._data['CGNSSINFO_pdop'], 0.1, 0, 4),
            'CGNSSINFO_hdop': regenerateValueMaxMin(self._data['CGNSSINFO_hdop'], 0.1, 0, 4),
            'CGNSSINFO_vdop': regenerateValueMaxMin(self._data['CGNSSINFO_vdop'], 0.1, 0, 4),
            'power_module_state': str(self._power_state),
        }
        return True

    def power_module(self, value: bool):
        logger.info("EXECUTE power_module with {} val".format(value))
        if self._power_state == value:
            logger.debug("power_module already power ".format("ON" if value else "OFF"))
            return

        self._power_state = value
        if self._power_state:
            logger.debug('SIM7600X is ready')
        else:
            logger.debug('SIM7600X is down')


if __name__ == '__main__':
    v = DeviceSimulator()
    print("{}# [{}CONNECTED]: {}".format(v.device_type,
                                         "" if v.is_connected else "NOT ",
                                         v.latest_data["V"]))
