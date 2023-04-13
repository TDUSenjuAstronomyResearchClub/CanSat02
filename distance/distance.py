"""
Module Name:<br> 
distance<br><br>
Description:<br> 
超音波距離センサを使い、機体前面にある物体と機体との距離を取得するプログラム<br><br>
"""

import RPi.GPIO as GPIO
import time
from ..temperature import temperature

# 測定環境温度
temp = temperature.temperature_result()  # 温湿度気圧センサから現在の温度値を呼び出す
TEMP = temp[0]

# GPIO設定
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN)



def distance_result():
    """
    超音波距離センサ(HC-SR04)を使って機体前面にある物体と機体との距離を取得するプログラム。

    Returns
    -------
    str
            str型で距離(cm)を返却する
    OSError
            OSErrorが発生した場合はエラー文を返す。
    """
    try:
        # トリガ信号出力
        GPIO.output(17, GPIO.HIGH)
        time.sleep(0.00001)

        GPIO.output(17, GPIO.LOW)

        # 返送HIGHレベル時間計測
        while GPIO.input(27) == GPIO.LOW:
            soff = time.time()  # LOWレベル終了時刻

        while GPIO.input(27) == GPIO.HIGH:
            son = time.time()  # HIGHレベル終了時刻

        # HIGHレベル期間の計算
        clc = son - soff

        # 時間から距離に変換(TEMPは測定環境温度)
        clc = clc * (331.50 + (0.6 * TEMP)) / 2 * 100


        return str(clc)
    except TypeError as e:
        return e
