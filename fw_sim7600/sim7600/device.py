#!/usr/bin/python3
import logging
from typing import Optional
import serial
import time

try:
    import RPi.GPIO as GPIO

    _gpio_loaded = True
except:
    print("WARN: RPi.GPIO module disabled.")
    _gpio_loaded = False

from fw_sim7600.sim7600.mappings import *
from fw_sim7600.device_serial import DeviceSerial

logger = logging.getLogger()


class Device(DeviceSerial):
    """
    Device class for SIM7600 Pack devices communicating via Serial port
    """

    RETRY_TIMES = 5
    RETRY_TIME_SEC = 1.0
    RESPONSE_WAIT_TIME = 0.01
    AT_CMD_TIMEOUT = 1.0
    POWER_PIN = 6

    def __init__(self, device: str = '/dev/ttyAMA0', speed: int = 115200,
                 auto_refresh=True):
        super().__init__(device, speed, None, auto_refresh)

        self.cached_pid = None

        self._power_state = True

    def _get_data(self) -> [bytes]:
        """ Returns a PDU array, one entry per line."""
        if not self._power_state:
            return []

        data = []
        try:
            with serial.Serial(self.device, self.speed, timeout=1) as s:
                self._is_connected = True

                data += self._query_product_info(s)

                if len(data) == 0:
                    logger.debug("Error querying device, no data received")
                    self._is_connected = False
                    return []
                if not self._find_pid(data):
                    logger.debug("Error querying device, no PID received")
                    self._is_connected = False
                    return []

                data += self._query_gnss_info(s)
                if self._must_terminate:
                    self._is_connected = False

        except serial.serialutil.SerialException:
            self._is_connected = False

        return data

    def _query_product_info(self, s) -> [bytes]:
        data = []
        if not self._must_terminate:
            logger.debug('Query product info...')
            data.append(self.send_at(s, 'AT+CGMI', 'OK', self.AT_CMD_TIMEOUT))
            data.append(self.send_at(s, 'AT+CGMM', 'OK', self.AT_CMD_TIMEOUT))
            data.append(self.send_at(s, 'AT+CGSN', 'OK', self.AT_CMD_TIMEOUT))
            data.append(self.send_at(s, 'AT+CSUB', 'OK', self.AT_CMD_TIMEOUT))
            data.append(self.send_at(s, 'AT+CGMR', 'OK', self.AT_CMD_TIMEOUT))
            data.append(self.send_at(s, 'AT+CSQ', 'OK', self.AT_CMD_TIMEOUT))
            data.append(self.send_at(s, 'AT+CREG?', 'OK', self.AT_CMD_TIMEOUT))
            data.append(self.send_at(s, 'AT+CPIN?', 'OK', self.AT_CMD_TIMEOUT))
            data.append(self.send_at(s, 'AT+COPS?', 'OK', self.AT_CMD_TIMEOUT))
            res = []
            for val in data:
                if val is not None:
                    res.append(val)
            data = res
        return data

    def _query_gnss_info(self, s) -> [bytes]:
        data = []
        if not self._must_terminate:
            logger.debug('Start GPS session...')
            self.send_at(s, 'AT', 'OK', self.AT_CMD_TIMEOUT)
            self.send_at(s, 'AT+CGPS=1', 'OK', self.AT_CMD_TIMEOUT)

            # gps request
            gps_answer = None
            count = 0
            while gps_answer is None \
                    and count < self.RETRY_TIMES \
                    and not self._must_terminate:
                gps_answer = self.send_at(s,
                                          'AT+CGPSINFO',
                                          '+CGPSINFO: ',
                                          self.AT_CMD_TIMEOUT)
                if gps_answer is not None:
                    if gps_answer is not None and b',,,,,,' in gps_answer:
                        gps_answer = None
                        logger.debug("No data for GPS, attempt {}/{}"
                                     .format(count + 1, self.RETRY_TIMES))
                time.sleep(self.RETRY_TIME_SEC)
                count += 1
            if gps_answer is not None:
                data.append(gps_answer)

            # gnss request
            gnss_answer = None
            count = 0
            while gnss_answer is None \
                    and count < self.RETRY_TIMES \
                    and not self._must_terminate:
                gnss_answer = self.send_at(s,
                                           'AT+CGNSSINFO',
                                           '+CGNSSINFO: ',
                                           self.AT_CMD_TIMEOUT)
                if gnss_answer is not None and b',,,,,,' in gnss_answer:
                    gnss_answer = None
                time.sleep(self.RETRY_TIME_SEC)
                count += 1
            if gnss_answer is not None:
                data.append(gnss_answer)

            logger.debug('End GPS session...')
            (self.send_at(s,
                          'AT+CGPS=0',
                          'OK',
                          self.AT_CMD_TIMEOUT)
             .decode())
        return data

    @staticmethod
    def send_at(ser, command, back, timeout) -> Optional[bytes]:
        try:
            rec_buff = ''
            ser.write((command + '\r\n').encode())
            time.sleep(timeout)
            if ser.inWaiting():
                time.sleep(Device.RESPONSE_WAIT_TIME)
                rec_buff = ser.read(ser.inWaiting())

            if rec_buff == '':
                return None

            if back not in rec_buff.decode():
                logger.debug(
                    "AT command '{}' returned wrong response".format(command))
                logger.debug(rec_buff)
                return None

            return rec_buff

        except Exception as err:
            logger.warning(
                "Unknown exception sending '{}' AT command: {};"
                "print stacktrace:"
                .format(command, err))
            import traceback
            traceback.print_exc()
            return None

    def _parse_pdu(self, frames):
        """ AT commands responses, one per frame. """

        at_cpin_set = False
        count = 1
        for frame in frames:
            if b'AT+CGMI' in frame:
                # AT+CGMI\r\r\nSIMCOM INCORPORATED\r\n\r\nOK\r\n
                frame_lines = frame.decode().split("\r\n")
                self._data['AT+CGMI'] = frame_lines[1]

            elif b'AT+CGMM' in frame:
                # AT+CGMM\r\r\nSIMCOM_SIM7600E-H\r\n\r\nOK\r\n
                frame_lines = frame.decode().split("\r\n")
                self._data['AT+CGMM'] = frame_lines[1]

            elif b'AT+CGSN' in frame:
                # AT + CGSN\r\r\n860147054839863\r\n\r\nOK\r\n
                frame_lines = frame.decode().split("\r\n")
                self._data['AT+CGSN'] = frame_lines[1]

            elif b'AT+CSUB' in frame:
                # AT+CSUB\r\r\n+CSUB: B04V03\r\n+CSUB: MDM9x07_LE20_S_22_V1.03_210527\r\n\r\nOK\r\n
                frame_lines = frame.decode().split("\r\n")
                self._data['AT+CSUB'] = frame_lines[1][
                                        len("CSUB:") + 1:].strip()
                self._data['AT+CSUB_B'] = frame_lines[2][
                                          len("CSUB:") + 1:].strip()

            elif b'AT+CGMR' in frame:
                # AT+CGMR\r\r\n+CGMR: LE20B04SIM7600M22\r\n\r\nOK\r\n
                frame_lines = frame.decode().split("\r\n")
                self._data['AT+CGMR'] = frame_lines[1][
                                        len("CGMR:") + 1:].strip()

            elif b'AT+CSQ' in frame:
                # AT+CSQ\r\r\n+CSQ: 4,99\r\n\r\nOK\r\n
                frame_lines = frame.decode().split("\r\n")
                values = frame_lines[1][len("CSQ:") + 1:].strip().split(',')
                self._data['AT+CSQ_rssi'] = values[0]
                self._data['AT+CSQ_ber'] = values[1]

            elif b'AT+CREG' in frame:
                # AT+CREG...
                frame_lines = frame.decode().split("\r\n")
                self._data['AT+CREG'] = frame_lines[1]

            elif b'AT+CPIN' in frame:
                # AT+CPIN...
                frame_lines = frame.decode().split("\r\n")
                self._data['AT+CPIN'] = frame_lines[1]
                at_cpin_set = True

            elif b'AT+COPS' in frame:
                # AT+COPS...
                frame_lines = frame.decode().split("\r\n")
                self._data['AT+COPS'] = frame_lines[1]

            elif b'+CGPSINFO:' in frame:
                # {...}+CGPSINFO: 4629.830411,N,01120.202419,E,051023,185112.0,290.5,0.0,{...}
                frame_lines = frame.decode().split("\r\n")
                line: str
                for line in frame_lines:
                    if "+CGPSINFO:" in line:
                        line = line[len("+CGPSINFO:"):].strip()
                        values = line.split(",")
                        self._data['CGPSINFO_lat_degrees'] = values[0]
                        self._data['CGPSINFO_lat_dir'] = values[1]
                        self._data['CGPSINFO_log_degrees'] = values[2]
                        self._data['CGPSINFO_log_dir'] = values[3]
                        # self._data['CGPSINFO_date'] = values[4]
                        # self._data['CGPSINFO_utc_date'] = values[5]
                        self._data['CGPSINFO_alt'] = values[6]
                        self._data['CGPSINFO_speed'] = values[7]
                        self._data['CGPSINFO_course'] = values[8] if values[
                                                                         8] != "" else "-1"

            elif b'+CGNSSINFO:' in frame:
                # {...}+CGNSSINFO: 2,02,03,00,4629.822936,N,01120.199998,E,051023,194627.0,323.3,0.0,,2.0,1.7,1.0{...}
                frame_lines = frame.decode().split("\r\n")
                line: str
                for line in frame_lines:
                    if "+CGNSSINFO:" in line:
                        line = line[len("+CGNSSINFO:"):].strip()
                        values = line.split(",")
                        self._data['CGNSSINFO_mode'] = values[0]
                        self._data['CGNSSINFO_sat_gps_count'] = values[1]
                        self._data['CGNSSINFO_sat_glonass_count'] = values[2]
                        self._data['CGNSSINFO_sat_beidou_count'] = values[3]
                        self._data['CGNSSINFO_lat_degrees'] = values[4]
                        self._data['CGNSSINFO_lat_dir'] = values[5]
                        self._data['CGNSSINFO_log_degrees'] = values[6]
                        self._data['CGNSSINFO_log_dir'] = values[7]
                        # self._data['CGNSSINFO_date'] = values[8]
                        # self._data['CGNSSINFO_utc_date'] = values[9]
                        self._data['CGNSSINFO_alt'] = values[10]
                        self._data['CGNSSINFO_speed'] = values[11]
                        self._data['CGNSSINFO_course'] = values[12] if values[
                                                                           12] != "" else "-1"
                        self._data['CGNSSINFO_pdop'] = values[13]
                        self._data['CGNSSINFO_hdop'] = values[14]
                        self._data['CGNSSINFO_vdop'] = values[15]

            else:
                logger.debug("Unknown frame {}/{}:".format(count, len(frames)))
                logger.debug(frame)

            count += 1
        if not at_cpin_set:
            self._data['AT+CPIN'] = "NoSIM"
        self._data['power_module_state'] = str(self._power_state)

        # for k in self._data.keys():
        #     print("'{}': '{}',".format(k, self._data[k]))

    @property
    def device_pid(self) -> "str | None":
        """
        Returns the device PID, it can be used as index for the PID dict.
        In the SIM7600 case is the device's model (AT+CGMM).
        """

        if self.cached_pid is None:
            try:
                self.cached_pid = self._data['AT+CGMM']
            except KeyError as err:
                raise SystemError("Unknown PID from device") from err

        return self.cached_pid

    @property
    def device_type(self) -> str:
        """ Returns the device type """
        if self.cached_type is None:
            if self.device_pid is not None:
                try:
                    self.cached_type = PID[self.device_pid]['type']
                except KeyError as err:
                    raise SystemError("Unknown PID '{}' read from device".format(self.device_pid)) from err

        return self.cached_type \
            if self.cached_type is not None \
            else DEV_TYPE_UNKNOWN

    def power_module(self, value: bool):
        logger.info("EXECUTE power_module with {} val".format(value))
        if self._power_state == value:
            logger.debug(
                "power_module already power ".format("ON" if value else "OFF"))
            return

        if value:
            self._power_on()
        else:
            self._power_down()

    def _power_on(self):
        if _gpio_loaded:
            logger.debug('SIM7600X is starting:')
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.POWER_PIN, GPIO.OUT)
            time.sleep(0.1)
            GPIO.output(self.POWER_PIN, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(self.POWER_PIN, GPIO.LOW)
            time.sleep(20)
            with serial.Serial(self.device, self.speed, timeout=1) as s:
                s.flushInput()
            logger.debug('SIM7600X is ready')
            self._power_state = True

    def _power_down(self):
        if _gpio_loaded:
            logger.debug('SIM7600X is shutdown:')
            GPIO.output(self.POWER_PIN, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(self.POWER_PIN, GPIO.LOW)
            time.sleep(18)
            logger.debug('SIM7600X is down')
            self._power_state = True

    def _find_pid(self, data):
        for frame in data:
            if b'AT+CGMM' in frame:
                return True
        return False


if __name__ == '__main__':
    v = Device()
    print("{}# [{}CONNECTED]: {}".format(v.device_type,
                                         "" if v.is_connected else "NOT ",
                                         v.latest_data["V"]))
