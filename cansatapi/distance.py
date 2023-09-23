"""超音波距離センサを使い、機体前面にある物体と機体との距離を取得するプログラム

使用しているライブラリ:
    rpi.gpio
"""

import RPi.GPIO as GPIO
import time
from .bme280 import BME280

# ポート番号の定義
TRIG = 5  # 変数"Trig"に27を代入
ECHO = 6  # 変数"Echo"に18を代入

# GPIO設定
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# 測定環境温度
try:
    temp = BME280().temperature_result()  # 温湿度気圧センサから現在の温度値を呼び出す
    TEMP = temp[0]
except OSError:  # OSErrorが発生した場合は、25度として計算をしていく
    TEMP = 25


def distance_result() -> float:
    """超音波距離センサ(HC-SR04)を使って機体前面にある物体と機体との距離を取得する

    Returns:
        float: 距離(cm)
    """
    time.sleep(0.1)  # センサーの安定を待つ

    # トリガ信号出力
    GPIO.output(TRIG, GPIO.HIGH)  # GPIO5の出力をHigh(3.3V)にする
    time.sleep(0.00001)  # 10μ秒間待つ
    GPIO.output(TRIG, GPIO.LOW)  # GPIO5の出力をLow(0V)にする

    sig_off = time.time()  # 初期値の設定
    timeout = time.time() + 0.02  # タイムアウトを0.02秒に設定

    while GPIO.input(ECHO) == GPIO.LOW and time.time() < timeout:  # 返送LOWレベル時間計測
        sig_off = time.time()  # LOWレベル終了時刻更新
        print(f"デバック用 sig_off: {sig_off}")

    sig_on = time.time()  # 初期値の設定
    timeout = time.time() + 0.02  # タイムアウトを0.02秒に設定
    print(f"デバック用 echo timeout: {timeout}")

    while GPIO.input(ECHO) == GPIO.HIGH and time.time() < timeout:  # 返送HIGHレベル時間計測
        sig_on = time.time()  # HIGHレベル終了時刻更新
        print(f"デバック用 sig_on: {sig_on}")

    # HIGHレベル期間の計算
    elapsed = sig_on - sig_off
    print(f"デバック用 elapsed: {elapsed}")

    speed = 331.50 + 0.6 * TEMP     # 音速を求める(TEMPは測定環境温度)
    duration = elapsed * speed / 2 * 100     # elapsedは経過時間（秒）、最後に100をかけてメートルからセンチメートルに変換

    return duration
