"""DCモーターを使って機体を制御するモジュール
"""
import time
from cansatapi.dcmotor import DCMotor

FIN = 0
RIN = 0

def StraightLine():
    """3秒間前進させるための関数
    """

    # DCモータのインスタンスを生成
    motor_r = DCMotor(6, 5)
    motor_l = DCMotor(26, 19)

    # それぞれのモーターのデューティ比を80%に設定
    motor_r.forward(80)
    motor_l.forward(80)
    time.sleep(3)  # 三秒間前進

    # それぞれのモーターを停止
    motor_r.stop()
    motor_l.stop()
    time.sleep(1)
