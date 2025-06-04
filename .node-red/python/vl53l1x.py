"""
距離センサ(VL53l1X)通信処理

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

from qwiic_vl53l1x import QwiicVL53L1X


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
    parser = argparse.ArgumentParser(description='距離センサ(VL53l1X)通信')
    parser.add_argument('-i', '--interval', type=int, default=1000, help='出力間隔[ms]')
    return parser.parse_args().interval / 1000


if __name__ == '__main__':
    interval = __parse_args()
    __exit_if_started()
    address = 0x29
    vl53l1x = QwiicVL53L1X()

    if vl53l1x.init_sensor(address) == 0:
        exit(1)

    if vl53l1x.set_distance_mode(1) == 0:
        exit(1)

    while not vl53l1x.check_for_data_ready():
        time.sleep(.005)

    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    base_time = time.time()
    next_time = 0
    while True:
        now = datetime.datetime.now(JST)
        vl53l1x.start_ranging()
        time.sleep(.005)
        distance = vl53l1x.get_distance()
        time.sleep(.005)
        vl53l1x.stop_ranging()
        if distance != 0:
            values = [min(distance, 2000)]
        else:
            values = []
        data = dict(time=int(now.timestamp()*1000),
                    values=values,
                    address=address,
                    sensorType=260)
        print(json.dumps(data))
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)
