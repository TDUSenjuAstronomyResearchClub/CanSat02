"""超音波距離センサを使い、機体前面にある物体と機体との距離を取得するプログラム
"""

import digitalio
import board
import time
from .bme280 import BME280

# 測定環境温度
try:
    temp = BME280().temperature_result()  # 温湿度気圧センサから現在の温度値を呼び出す
    TEMP = temp[0]
except OSError:  # OSErrorが発生した場合は、25度として計算をしていく
    TEMP = 25

# GPIO設定
OUT = digitalio.DigitalInOut(board.D17)
IN = digitalio.DigitalInOut(board.D27)


def distance_result() -> float:
    """超音波距離センサ(HC-SR04)を使って機体前面にある物体と機体との距離を取得する

    Returns:
        float: 距離(cm)
    """

    # トリガ信号出力
    OUT.value = True
    time.sleep(0.00001)
    OUT.value = False

    # 返送HIGHレベル時間計測
    while not IN.value:
        soff = time.time()  # LOWレベル終了時刻

    start = time.time()
    while IN.value:
        son = time.time()  # HIGHレベル終了時刻

        if son - start > 10:  # 10秒よりも長くHIGHレベルにならなかった場合は、Noneを返却する
            return None

    # HIGHレベル期間の計算
    clc = son - soff

    # 時間から距離に変換(TEMPは測定環境温度)
    clc = clc * (331.50 + (0.6 * TEMP)) / 2 * 100

    return clc
