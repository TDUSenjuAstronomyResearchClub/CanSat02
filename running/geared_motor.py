# 3秒間前進
import time

from cansatapi.dcmotor import DCMotor

# TODO: ピン番号は書き換えること
FIN = 0
RIN = 0


def StraightLine():
    # モータを初期化
    motor = DCMotor(FIN, RIN)

    # duty比を80と0にする
    motor.forward(80)
    time.sleep(3)

    # duty比を0と0にする
    motor.stop_motor()
    time.sleep(1)
