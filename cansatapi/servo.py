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
    # 範囲変換式で±90°からデューティ比2.5~12[%]に収める
    if angle > 90:
        angle = 90
    elif angle < -90:
        angle = -90
    return conv_range(angle, -90, 90, 2.5, 12.0)


class Servo:
    def __init__(self, pin_number: int):
        """サーボを初期化するメソッド

        Args:
            pin_number: サーボのピン番号
        """
        self.servo_pin = pin_number
        # GPIOの番号指定モードをBCMに設定
        GPIO.setmode(GPIO.BCM)

        # SERVO_PINを出力モードに設定
        GPIO.setup(self.servo_pin, GPIO.OUT)

        # PWMの設定
        # SG90と同じように制御できるっぽい
        self.servo = GPIO.PWM(self.servo_pin, 50)

        # サーボの制御を開始する
        self.servo.start(0)

    def rotate_to_angle(self, angle: int):
        """サーボモーターを指定の角度[°]へ動かすメソッド

        範囲は±90°で指定してください。
        指定された角度が[-90, 90]の範囲を越えていた場合はこの範囲に収めます。

        Args:
            angle: 範囲[-90, 90]の角度[°]
        """
        self.servo.ChangeDutyCycle(calc_duty(angle))
        time.sleep(0.3)

    def stop(self):
        """サーボモーターを停止させるメソッド

        サーボモーター使用後は必ず呼び出すこと
        """
        self.servo.stop()
        GPIO.cleanup()
