"""サーボモーターを制御するモジュール
"""
import time

import RPi.GPIO as GPIO

from cansatapi.util.convert import conv_range


def calc_duty(angle: float) -> float:
    """指定の角度からデューティ比を求める関数

    Args:
        angle (float): 角度[°]

    Returns:

    """
    # 範囲変換式で±90°からパルス幅1~2msに収める
    if angle > 90:
        angle = 90
    elif angle < -90:
        angle = -90
    return conv_range(angle, -90, 90, 1, 2)


class Servo:
    def __init__(self, pin_number: int):
        """サーボを初期化するメソッド

        Args:
            pin_number: サーボのピン番号
        """
        self.servo_pin = pin_number
        # GPIOの番号指定モードをBOARDに設定(ボードの番号と一致するモード)
        GPIO.setmode(GPIO.BOARD)

        # SERVO_PINを出力モードに設定
        GPIO.setup(self.servo_pin, GPIO.OUT)

        # PWMの設定
        # 周波数指定がよくわからないのでいったん50Hzで試してみる
        # SG90と特性が似ているっぽいので恐らくPWMの周波数は20ms
        self.servo = GPIO.PWM(self.servo_pin, 50)

        # サーボの制御を開始する
        self.servo.start(0)

    def angle(self, angle: int):
        """サーボモーターを指定の角度へ動かすメソッド

        範囲は±90°

        Args:
            angle: 範囲[-90, 90]の角度[°]
        """
        self.servo.ChangeDutyCycle(calc_duty(angle))
        time.sleep(0.3)
