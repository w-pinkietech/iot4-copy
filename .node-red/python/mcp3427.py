"""
ADCセンサーMCP3427通信処理

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
import subprocess
import time
from typing import Tuple

import smbus2
from MCP342x import MCP342x


def __parse_args() -> Tuple[int, float, int]:
    """実行時引数の解釈を行う

    Returns:
        Tuple[int, float, int]: I2Cアドレス, 出力間隔[sec], ゲイン
    """
    parser = argparse.ArgumentParser(description='ADCセンサーMCP3427通信処理')
    parser.add_argument('-a', '--address', type=int, choices=[0x6B, 0x6F, 0x68], required=True, help='I2Cアドレス')
    parser.add_argument('-i', '--interval', type=float, default=1.0, help='出力間隔[sec]')
    parser.add_argument('-g', '--gain', type=int, choices=[1, 2, 4, 8], default=1, help='ゲイン')
    args = parser.parse_args()
    return args.address, args.interval, args.gain


def __exit_if_started(address: int) -> None:
    """同一のプロセスが実行中である場合に強制終了する

    Args:
        address (int): I2Cアドレス
    """
    file_name = os.path.basename(__file__)
    with subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE) as p1:
        with subprocess.Popen(['grep', f'{file_name} -a {address}'], stdin=p1.stdout, stdout=subprocess.PIPE) as p2:
            with subprocess.Popen(['grep', 'python'], stdin=p2.stdout, stdout=subprocess.PIPE) as p3:
                with subprocess.Popen(['wc', '-l'], stdin=p3.stdout, stdout=subprocess.PIPE) as p4:
                    output = p4.communicate()[0].decode('utf8').replace('\n', '')
                    if int(output) != 1:
                        exit(1)


if __name__ == '__main__':
    address, interval, gain = __parse_args()
    __exit_if_started(address)
    mcp3427_ch0 = MCP342x(smbus2.SMBus(1), address, device='MCP3427', channel=0, gain=gain, resolution=16)
    mcp3427_ch1 = MCP342x(smbus2.SMBus(1), address, device='MCP3427', channel=1, gain=gain, resolution=16)
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    base_time = time.time()
    next_time = 0
    while True:
        now = datetime.datetime.now(JST)
        volt0 = mcp3427_ch0.convert_and_read()
        volt1 = mcp3427_ch1.convert_and_read()
        data = dict(
            time=int(now.timestamp()*1000),
            values=[volt0 * 1000.0, volt1 * 1000.0],
            address=address,
            sensorType=259)
        print(json.dumps(data))
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)
