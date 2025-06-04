# -*- coding: utf-8 -*
"""
加速度センサー(LIS2DUXS12)通信処理

Copyright (c) 2023 Fukuoka Industrial Technology Center

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import datetime
import json
import math
import struct
import time
from typing import List, Tuple

import smbus2


class LIS2DUXS12:

    REG_WHO_AM_I = 0x0F
    REG_CTRL1 = 0x10
    REG_CTRL2 = 0x11
    REG_CTRL3 = 0x12
    REG_CTRL4 = 0x13
    REG_CTRL5 = 0x14
    REG_OUT = 0x28
    SLEEP = 0.01

    def __init__(self, bus, address):
        self._bus = smbus2.SMBus(bus)
        self._address = address

    def __write_reg(self, register: int, data: int) -> None:
        self._bus.write_i2c_block_data(self._address, register, [data])

    def __read_reg(self, register: int) -> int:
        self._bus.write_byte(self._address, register)
        time.sleep(self.SLEEP)
        return self._bus.read_byte(self._address)

    def __read_block_reg(self, register: int, length: int) -> List[int]:
        return self._bus.read_i2c_block_data(self._address, register, length)

    def begin(self) -> bool:
        identifier = self.__read_reg(self.REG_WHO_AM_I)
        return identifier == 0x47

    def soft_reset(self) -> None:
        value = self.__read_reg(self.REG_CTRL1)
        value |= 0b0010_0000
        self.__write_reg(self.REG_CTRL1, value)

    def set_range_8g(self) -> None:
        value = self.__read_reg(self.REG_CTRL5)
        value &= 0b1111_1100
        value |= 0b1111_1110
        self.__write_reg(self.REG_CTRL5, value)

    def set_rate_800hz(self) -> None:
        value = self.__read_reg(self.REG_CTRL5)
        value &= 0b0000_1111
        value |= 0b1011_0000
        self.__write_reg(self.REG_CTRL5, value)

    def set_filter_bandwidth_as_odr2(self) -> None:
        value = self.__read_reg(self.REG_CTRL5)
        value &= 0b1111_0011
        self.__write_reg(self.REG_CTRL5, value)

    def set_high_performance_mode(self) -> None:
        value = self.__read_reg(self.REG_CTRL3)
        value |= 0b0000_0100
        self.__write_reg(self.REG_CTRL3, value)

    def power_up(self) -> None:
        try:
            self.begin()
        except OSError:
            time.sleep(0.3)

    def init(self) -> bool:
        self.power_up()
        if not self.begin():
            return False
        self.soft_reset()
        self.set_range_8g()
        self.set_filter_bandwidth_as_odr2()
        self.set_high_performance_mode()
        self.set_rate_800hz()
        return True

    def get_acc(self) -> Tuple[float, float, float]:
        values = self.__read_block_reg(self.REG_OUT, 6)
        x, y, z = struct.unpack('<hhh', bytes(values))
        return x * 0.244, y * 0.244, z * 0.244


if __name__ == '__main__':
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    i2c_address = 0x19
    lis2duxs12 = LIS2DUXS12(1, i2c_address)
    if not lis2duxs12.init():
        exit()
    base_time = time.time()
    next_time = 0
    while True:
        now = datetime.datetime.now(JST)
        acc = lis2duxs12.get_acc()
        values = [v/1000.0 for v in acc]
        values.append(abs(math.sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2)/1000.0-1.0))
        data = dict(
            time=now.strftime('%Y-%m-%d %H:%M:%S.%f'),
            values=values,
            address=i2c_address,
            sensorType=262,
            tag='accelerator')
        print(json.dumps(data))
        next_time = ((base_time - time.time()) % 1.0) or 1.0
        time.sleep(next_time)
