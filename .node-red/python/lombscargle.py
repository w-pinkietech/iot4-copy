"""
Lomb-Scargleピリオドグラムによる加速度周波数解析クラス

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

import concurrent.futures
import datetime
import json
import math
import os
import queue
import subprocess
import time
from typing import List

import numpy as np
import scipy.signal
from lis2duxs12 import LIS2DUXS12


class Lombscargle:

    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

    def __init__(self, bus: int, addresses: List[int]) -> None:
        self.queue = queue.Queue()
        self.addresses = addresses
        self.bus = bus

    def init(self) -> bool:
        for address in self.addresses:
            try:
                acc = LIS2DUXS12(self.bus, address)
                if acc.init():
                    self.acc = acc
                    return True
            except OSError:
                pass
        return False

    def accelerator(self) -> None:
        while True:
            now = datetime.datetime.now(self.JST)
            acc = self.acc.get_acc()
            values = [v/1000.0 for v in acc]
            values.append(int(now.timestamp()*1000))
            self.queue.put(values)

    def lombscargle(self) -> None:
        base_time = time.time()
        next_time = 0

        # 出力間隔[sec]
        interval = 1.0

        while True:

            # 周波数解析データ用
            delta = np.array([])
            vibrate = np.array([])
            accdata = np.array([[], [], [], []])
            last = None

            while not self.queue.empty():
                x, y, z, dt = self.queue.get()
                comp = math.sqrt(x**2 + y**2 + z**2)
                vibrate = np.append(vibrate, comp)
                accdata = np.append(accdata, [[x], [y], [z], [abs(comp-1)]], axis=1)
                delta = np.append(delta, dt)
                last = (x, y, x, dt)

            if last is None:
                next_time = ((base_time - time.time()) % interval) or interval
                time.sleep(next_time)
                continue

            # 加速度の平均値を計算
            vibmeans = accdata.mean(axis=1)

            # 加速度データ作成
            data = dict(
                time=last[3],
                values=list(vibmeans),
                address=self.acc._address,
                sensorType=262,
                tag='accelerator')

            # 加速度データ出力
            print(json.dumps(data))

            # スペクトログラムが必要な場合は以下コメントアウトを解除
            delta = [dt/1000.0 for dt in (delta - delta[0])]

            # 直流成分を除去
            vibrate = vibrate - np.mean(vibrate)
            # Lomb-Scargle法で使用する周波数分解能
            f = np.linspace(1e-12, 200.0*2.0*np.pi, 200, endpoint=False)
            # Lomb-Scargle法により周波数変換
            pgram = scipy.signal.lombscargle(delta, vibrate, f, normalize=False)

            # パワー合計値
            sumpower = np.dot(vibrate, vibrate)
            # パワーリスト
            pgram = pgram * 2.0 / sumpower

            # ヒストグラム格納先
            data = dict(
                time=last[3],
                values=list(pgram),
                sensorType=262,
                address=self.acc._address,
                sumpower=sumpower,
                tag='spectrogram')

            # 周波数解析結果出力
            print(json.dumps(data))

            next_time = ((base_time - time.time()) % interval) or interval
            time.sleep(next_time)


def __exit_if_started() -> None:
    file_name = os.path.basename(__file__)
    with subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE) as p1:
        with subprocess.Popen(['grep', file_name], stdin=p1.stdout, stdout=subprocess.PIPE) as p2:
            with subprocess.Popen(['grep', 'python'], stdin=p2.stdout, stdout=subprocess.PIPE) as p3:
                with subprocess.Popen(['wc', '-l'], stdin=p3.stdout, stdout=subprocess.PIPE) as p4:
                    output = p4.communicate()[0].decode('utf8').replace('\n', '')
                    if int(output) != 1:
                        exit(1)


if __name__ == '__main__':

    # 起動済みなら終了
    __exit_if_started()

    # メインプログラム
    lombscargle = Lombscargle(1, [0x18, 0x19])
    if not lombscargle.init():
        exit()

    # スレッドでメソッドを実行する
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(lombscargle.accelerator)
        executor.submit(lombscargle.lombscargle)
        try:
            while True:
                time.sleep(1)
        except:
            executor.shutdown()
