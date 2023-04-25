"""サーボモーター制御モジュール
"""
import time

import RPi.GPIO as GPIO

from cansatapi.util.convert import conv_range

# ピン番号は適切に変えること
SERVO_PIN = 18


def calc_duty(angle: float) -> float:
    """指定の角度からデューティ比を求める関数

    Args:
        angle (float): 角度[°]

    Returns:

    """
    # 範囲変換式で±90°からパルス幅1~2msに収める
    return conv_range(angle, -90, 90, 1, 2)


class Servo:
    def __init__(self):
        # GPIOの番号指定モードをBOARDに設定(ボードの番号と一致するモード)
        GPIO.setmode(GPIO.BOARD)

        # SERVO_PINを出力モードに設定
        GPIO.setup(SERVO_PIN, GPIO.OUT)

        # PWMの設定
        # 周波数指定がよくわからないのでいったん50Hzで試してみる
        # SG90と特性が似ているっぽいので恐らくPWMの周波数は20ms
        self.servo = GPIO.PWM(SERVO_PIN, 50)

        # サーボの制御を開始する
        self.servo.start(0)

    def angle(self, angle: int):
        """サーボモーターを指定の角度へ動かすメソッド

        Args:
            angle: 角度[°]
        """
        self.servo.ChangeDutyCycle(calc_duty(angle))
        time.sleep(0.3)
