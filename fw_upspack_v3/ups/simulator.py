#!/usr/bin/python3

from .device import Device
from .mappings import *
from ..commons import regenerateValue


class DeviceSimulator(Device):

    def __init__(self, device: str = '/dev/ttyAMA0', speed: int = 9600):
        super().__init__(device, speed, False)
        self._data = {
            'SmartUPS': 'V3.2P',
            'Vin': 'GOOD',
            'BATCAP': "100",
            'Vout': '5250'
        }

    def refresh(self, reset_data=False) -> bool:
        self._data = {
            'SmartUPS': 'V3.2P',
            'Vin': 'GOOD' if random.randint(0, 1) else "NG",
            'BATCAP': max(min(regenerateValue(self._data['BATCAP'], 1), 100), 0),
            'Vout': max(min(regenerateValue(self._data['Vout'], 10), 5400), 5100),
        }
        return True


if __name__ == '__main__':
    v = DeviceSimulator()
    print("{}# [{}CONNECTED]: {}".format(v.device_type,
                                         "" if v.is_connected else "NOT ",
                                         v.latest_data["V"]))
