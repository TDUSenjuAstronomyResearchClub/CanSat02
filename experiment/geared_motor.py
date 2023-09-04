"""DCモーターを使って機体を制御するモジュール
"""
import time
from cansatapi.dcmotor import DCMotor


def StraightLine():
    """3秒間前進させるための関数
    """

    # DCモータのインスタンスを生成
    motor_r = DCMotor(6, 5)
    motor_l = DCMotor(26, 19)

    # それぞれのモーターのデューティ比を80%に設定
    motor_r.forward(80)
    motor_l.forward(80)
    time.sleep(3)  # 3秒間前進

    # それぞれのモーターを停止
    motor_r.stop()
    motor_l.stop()
    time.sleep(1)  # 1秒間待つ

def Back():
    """3秒間後退させるための関数
    """

    # DCモータのインスタンスを生成
    motor_r = DCMotor(6, 5)
    motor_l = DCMotor(26, 19)

    # それぞれのモーターのデューティ比を80%に設定
    motor_r.reverseward(80)
    motor_l.reverseward(80)
    time.sleep(3)  # 3秒間後退

    # それぞれのモーターを停止
    motor_r.stop()
    motor_l.stop()
    time.sleep(1)  # 1秒間待つ

def TurnRight():
    """右旋回させるための関数
    """

    # DCモータのインスタンスを生成
    motor_r = DCMotor(6, 5)
    motor_l = DCMotor(26, 19)

    # 右のモーターのデューティ比を80%に設定
    motor_r.forward(80)
    motor_l.forward()

    # 右のモーターを停止
    motor_r.stop()
    motor_l.stop()
    time.sleep(1)  # 1秒間待つ

def TurnLeft():
    """左旋回させるための関数
    """

    # DCモータのインスタンスを生成
    motor_r = DCMotor(6, 5)
    motor_l = DCMotor(26, 19)

    # 左のモーターのデューティ比を80%に設定
    motor_r.reverse()
    motor_l.reverse(80)

    # 左のモーターを停止
    motor_r.stop()
    motor_l.stop()
    time.sleep(1)  # 1秒間待つ