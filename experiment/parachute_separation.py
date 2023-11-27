"""機体とパラシュートが分離できるかのテストモジュール
パラシュートを付けた状態で機体をセットする
"""
from cansatapi import dcmotor
from cansatapi.servo import Servo
import time

# パラシュート分離用モーターのピン番号
para_pin = 23

# パラシュート分離線を巻き取り
para_servo = Servo(para_pin)
try:
    print("パラシュート分離線を巻き取り")
    para_servo.rotate_cw()
    time.sleep(10)
    para_servo.finish()

    time.sleep(1)

    # 機体を前進させる
    dcmotor.Wheels.stop()
    print("機体を20秒前進させる")
    dcmotor.Wheels.forward()
    time.sleep(20)
    dcmotor.Wheels.stop()
    dcmotor.Wheels.cleanup()

except KeyboardInterrupt:
    dcmotor.Wheels.stop()
    dcmotor.Wheels.cleanup()
    para_servo.finish()


