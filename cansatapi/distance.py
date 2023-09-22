"""超音波距離センサを使い、機体前面にある物体と機体との距離を取得するプログラム

使用しているライブラリ:
    rpi.gpio
"""

import RPi.GPIO as GPIO
import time
from .bme280 import BME280

# 測定環境温度
try:
    temp = BME280().temperature_result()  # 温湿度気圧センサから現在の温度値を呼び出す
    TEMP = temp[0]
except OSError:  # OSErrorが発生した場合は、25度として計算をしていく
    TEMP = 25

# GPIO設定
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.IN)


def distance_result() -> float:
    """超音波距離センサ(HC-SR04)を使って機体前面にある物体と機体との距離を取得する

    Returns:
        float: 距離(cm)
    """
    # プログラム動作時間測定の基準
    start_time = time.time()

    # トリガ信号出力
    GPIO.output(5, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(5, GPIO.LOW)

    soff = time.time()  # 初期値の設定
    # 返送LOWレベル時間計測
    while GPIO.input(6) == GPIO.LOW:
        soff = time.time()  # LOWレベル終了時刻更新
        if soff - start_time > 5:   # 5秒よりも長くLOWレベルにならなかった場合は、0.0を返却する
            return 0.0

    son = time.time()  # 初期値の設定
    # 返送HIGHレベル時間計測
    while GPIO.input(6) == GPIO.HIGH:
        son = time.time()  # HIGHレベル終了時刻更新
        if son - start_time > 10:  # 10秒よりも長くHIGHレベルにならなかった場合は、0.0を返却する
            return 0.0

    # HIGHレベル期間の計算
    clc = son - soff

    # 時間から距離に変換(TEMPは測定環境温度)
    clc = clc * (331.50 + (0.6 * TEMP)) / 2 * 100

    return clc
