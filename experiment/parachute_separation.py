"""機体とパラシュートが分離できるかのテストモジュール
パラシュートを付けた状態で機体をセットする
"""
from cansatapi import *
from cansatapi.servo import Servo
import time

# パラシュート分離用のgpioを指定
para_servo = Servo(23)

# 機体を前進させる
dcmotor.Wheels.forward()

start_time = time.time()

try:
    while True:
        para_servo.rotate_to_angle(90)
        # TODO: パラシュート分離にかかる時間を測定し，変更・反映させる
        """
        if time.time() - start_time >= 10:
            dcmotor.Wheels.stop()
            para_servo.rotate_to_angle(0)
            dcmotor.Wheels.cleanup()
            break
        """


except KeyboardInterrupt:
    dcmotor.Wheels.stop()
    para_servo.rotate_to_angle(0)

    dcmotor.Wheels.cleanup()

