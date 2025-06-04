"""
差圧センサ(SDP810-500)通信クラス

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
import os
import struct
import subprocess
import time
from typing import List

import smbus2


class SDP810:

    """差圧センサSdp810-500との通信クラス"""

    def __init__(self, bus: int, address: int) -> None:
        """コンストラクタ

        Args:
            bus (int): I2Cバス
            address (int): 通信対象の照度センサのI2Cアドレス
        """
        # I2C device: /dev/i2c-x
        self._bus = smbus2.SMBus(bus)
        # OPT3001: slave address
        self._address = address
        # 初期化フラグ
        self._initialized = False

    def init(self) -> bool:
        """初期化を行う

        Returns:
            bool: 成否
        """
        self.__stop()
        if not self.__begin():
            return False
        self.__soft_reset()
        self.__start()
        self._initialized = True
        return True

    def __start(self) -> None:
        self._bus.write_i2c_block_data(self._address, 0x36, [0x15])
        time.sleep(0.05)

    def __stop(self) -> None:
        self._bus.write_i2c_block_data(self._address, 0x3F, [0xF9])
        time.sleep(0.05)

    def __soft_reset(self) -> None:
        self._bus.write_byte(0x00, 0x06)
        time.sleep(0.05)

    def get_pressure(self) -> float:
        if not self._initialized:
            return float('nan')
        data = self._bus.read_i2c_block_data(self._address, 0, 9)
        if self.__check_sum(data[:2]) != data[2]:
            return float('nan')
        if self.__check_sum(data[6:8]) != data[8]:
            return float('nan')
        dp = struct.unpack('>h', bytes(data[:2]))[0]
        scale_factor = struct.unpack('>h', bytes(data[6:8]))[0]
        return dp / scale_factor

    def __begin(self) -> bool:
        """接続先のセンサーがSDP810-500かどうかをチェックする

        Returns:
            bool: 成否
        """
        self._bus.write_i2c_block_data(self._address, 0x36, [0x7C])
        self._bus.write_i2c_block_data(self._address, 0xE1, [0x02])
        data = self._bus.read_i2c_block_data(self._address, 0, 6)
        if self.__check_sum(data[:2]) != data[2]:
            return False
        if self.__check_sum(data[3:5]) != data[5]:
            return False
        productNumber = struct.unpack('>I', bytes(data[:2]) + bytes(data[3:5]))[0]
        return productNumber == 0x03020A01

    @staticmethod
    def __check_sum(values: List[int]) -> int:
        crc = 0xFF
        for v in values:
            crc ^= (v & 0xFF)
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ 0x31) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc


def __exit_if_started() -> None:
    """同一のプロセスが実行中である場合に強制終了する
    """
    file_name = os.path.basename(__file__)
    with subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE) as p1:
        with subprocess.Popen(['grep', file_name], stdin=p1.stdout, stdout=subprocess.PIPE) as p2:
            with subprocess.Popen(['grep', 'python'], stdin=p2.stdout, stdout=subprocess.PIPE) as p3:
                with subprocess.Popen(['wc', '-l'], stdin=p3.stdout, stdout=subprocess.PIPE) as p4:
                    output = p4.communicate()[0].decode('utf8').replace('\n', '')
                    if int(output) != 1:
                        exit(1)


if __name__ == '__main__':
    __exit_if_started()
    address = 0x25
    sdp810 = SDP810(1, address)
    sdp810.init()
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    base_time = time.time()
    next_time = 0
    while True:
        now = datetime.datetime.now(JST)
        pressure = sdp810.get_pressure()
        data = dict(
            time=int(now.timestamp()*1000),
            values=[pressure],
            address=address,
            sensorType=263)
        print(json.dumps(data))
        next_time = ((base_time - time.time()) % 1.0) or 1.0
        time.sleep(next_time)
