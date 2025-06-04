"""
温度センサ(mcp9600)通信クラス

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
import math
import os
import struct
import subprocess
import time
from enum import IntEnum
from typing import List, Tuple

import smbus2


class ThermocoupleType(IntEnum):

    """熱電対種別"""

    K = 0
    J = 1
    T = 2
    N = 3
    S = 4
    E = 5
    B = 6
    R = 7

    @classmethod
    def names(cls) -> List[str]:
        """熱電対の名称一覧を取得する

        Returns:
            List[str]: 熱電対の名称一覧
        """
        return [x.name for x in cls.__members__.values()]

    @classmethod
    def get_by_name(cls, name: str) -> IntEnum:
        """指定した名称から熱電対種別を取得する

        Args:
            name (str): 名称

        Returns:
            IntEnum: 熱電対種別
        """
        for t in cls.__members__.values():
            if t.name == name:
                return t
        return ThermocoupleType.K

    @classmethod
    def get_by_value(cls, value: int) -> IntEnum:
        """指定した値から熱電対種別を取得する

        Args:
            value (int): 値

        Returns:
            IntEnum: 熱電対種別
        """
        for t in cls.__members__.values():
            if t.value == value:
                return t
        return ThermocoupleType.K


class Mcp9600:

    """温度センサmcp9600との通信クラス"""

    WRITE_COMMAND = 0b11000000
    READ_COMMAND = 0b11000001

    REG_HOT_JUNCTION = 0x00
    REG_STATUS = 0x04
    REG_SENSOR_CONFIGURATION = 0x05
    REG_DEVICE_ID = 0x20

    TYPE_K = 0x00
    TYPE_J = 0x01
    TYPE_T = 0x02
    TYPE_N = 0x03
    TYPE_S = 0x04
    TYPE_E = 0x05
    TYPE_B = 0x06
    TYPE_R = 0x07

    def __init__(self, bus: int, address: int) -> None:
        """コンストラクタ

        Args:
            bus (int): I2Cバス
            address (int): 通信対象の温度センサのI2Cアドレス
        """
        # I2C device: /dev/i2c-x
        self._bus = smbus2.SMBus(bus)
        # MCP9600: slave address
        self._address = address
        # 初期化フラグ
        self._initialized = False

    def init(self, thermocouple_type: int) -> bool:
        """初期化を行う

        Args:
            thermocouple_type (int): 熱電対種別

        Returns:
            bool: 成否
        """
        if not self.__begin():
            return False
        self.__set_thermocouple_type(thermocouple_type)
        self._initialized = True
        return True

    def get_temperature(self) -> float:
        """温度を取得する

        Returns:
            float: 温度データ
        """
        if not self._initialized:
            return float('nan')
        block = self._bus.read_i2c_block_data(self._address, self.REG_HOT_JUNCTION, 2)
        return struct.unpack('>h', bytes(block))[0] * 0.0625

    def __send_write_command(self) -> None:
        self._bus.write_byte(self._address, self.WRITE_COMMAND)

    def __send_read_command(self) -> None:
        self._bus.write_byte(self._address, self.READ_COMMAND)

    def __begin(self) -> bool:
        """接続先のセンサーがMPC9600かどうかをチェックする

        Returns:
            bool: 成否
        """
        self.__send_read_command()
        values = self._bus.read_i2c_block_data(self._address, self.REG_DEVICE_ID, 2)
        device_id = values[0]
        return device_id == 0x40

    def __set_thermocouple_type(self, thermocouple_type: int) -> None:
        """熱電対種別を設定する

        Args:
            thermocouple_type (int): 熱電対種別
        """
        self.__send_write_command()
        self._bus.write_byte_data(self._address, self.REG_SENSOR_CONFIGURATION, thermocouple_type << 4)
        time.sleep(0.5)
        self.__send_read_command()


def __exit_if_started(address: int) -> None:
    """同一のプロセスが実行中である場合に強制終了する

    Args:
        address (int): I2Cアドレス
    """
    file_name = os.path.basename(__file__)
    with subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE) as p1:
        with subprocess.Popen(['grep', f'{file_name} -a {address} -t'], stdin=p1.stdout, stdout=subprocess.PIPE) as p2:
            with subprocess.Popen(['grep', 'python'], stdin=p2.stdout, stdout=subprocess.PIPE) as p3:
                with subprocess.Popen(['wc', '-l'], stdin=p3.stdout, stdout=subprocess.PIPE) as p4:
                    output = p4.communicate()[0].decode('utf8').replace('\n', '')
                    if int(output) != 1:
                        exit(1)


def __parse_args() -> Tuple[int, ThermocoupleType, float]:
    """実行時引数の解釈を行う

    Returns:
        Tuple[int, ThermocoupleType]: I2Cアドレス, 熱電対種別
    """

    parser = argparse.ArgumentParser(description='温度センサーMCP9600通信処理')
    parser.add_argument('-a', '--address', type=int, choices=[0x62, 0x61, 0x63, 0x65], required=True, help='I2Cアドレス')
    parser.add_argument('-t', '--thermocouple', choices=ThermocoupleType.names(), required=True, help='熱電対タイプ')
    parser.add_argument('-i', '--interval', type=int, default=1000, help='出力間隔[ms]')
    args = parser.parse_args()
    return args.address, ThermocoupleType.get_by_name(args.thermocouple), args.interval / 1000


if __name__ == '__main__':
    address, thermocouple, interval = __parse_args()
    __exit_if_started(address)
    mcp9600 = Mcp9600(1, address)
    mcp9600.init(thermocouple.value)
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    base_time = time.time()
    next_time = 0
    while True:
        now = datetime.datetime.now(JST)
        temp = mcp9600.get_temperature()
        if math.isnan(temp):
            values = []
        else:
            values = [temp]
        data = dict(
            time=int(now.timestamp()*1000),
            values=values,
            address=address,
            sensorType=261)
        print(json.dumps(data))
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)
