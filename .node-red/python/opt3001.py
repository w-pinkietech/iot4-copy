"""
照度センサ(OPT3001)通信クラス

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

import argparse
import datetime
import json
import os
import struct
import subprocess
import time

import smbus2


class Opt3001:

    """照度センサOpt3001との通信クラス"""

    REG_RESULT = 0x00
    REG_CONFIG = 0x01
    REG_DEVICE_ID = 0x7F

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
        if not self.__begin():
            return False
        self._bus.write_word_data(self._address, self.REG_CONFIG, 0x10CC)
        self._initialized = True
        return True

    def get_illuminance(self) -> float:
        """輝度値(lux)を取得する

        Returns:
            float: 輝度値(lux)
        """
        if not self._initialized:
            return float('nan')
        raw = self._bus.read_word_data(self._address, self.REG_RESULT)
        exponent = (raw & 0x00F0) >> 4
        fractional = ((raw & 0xFF00) >> 8) + ((raw & 0x000F) << 8)
        lux = (2 ** exponent) * fractional * 0.01
        return lux

    def __begin(self) -> bool:
        """接続先のセンサーがOPT3001かどうかをチェックする

        Returns:
            bool: 成否
        """
        data = self._bus.read_i2c_block_data(self._address, self.REG_DEVICE_ID, 2)
        identifier = struct.unpack('>H', bytes(data))[0]
        return identifier == 0x3001


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


def __parse_args() -> float:
    """実行時引数の解釈を行う

    Returns:
        float: 出力間隔[sec]
    """
    parser = argparse.ArgumentParser(description='照度センサ(OPT3001)通信')
    parser.add_argument('-i', '--interval', type=int, default=1000, help='出力間隔[ms]')
    return parser.parse_args().interval / 1000


if __name__ == '__main__':
    interval = __parse_args()
    __exit_if_started()
    address = 0x44
    opt3001 = Opt3001(1, address)
    opt3001.init()
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    base_time = time.time()
    next_time = 0
    while True:
        now = datetime.datetime.now(JST)
        lux = opt3001.get_illuminance()
        data = dict(
            time=int(now.timestamp()*1000),
            values=[round(lux)],
            address=address,
            sensorType=264)
        print(json.dumps(data))
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)
