"""サンプル採取機構が正しく動作するかのテストモジュール
"""
from cansatapi.servo import Servo
from cansatapi import *
import time

# サンプル採取機構のピン番号を指定
sample_motor_pin = 24


# サンプル採取機構を土と接触させる
print("サンプル採取機構を土と接触させる")
sample_servo = Servo(sample_motor_pin)
try:
    sample_servo.rotate_cw_or_ccw(11.5)
    time.sleep(0.2)
    sample_servo.stop()
except KeyboardInterrupt:
    sample_servo.stop()


# 機体を前進させ，土をサンプル採取機構の中に入れる
print("機体を前進")
dcmotor.Wheels.forward()
time.sleep(5)
dcmotor.Wheels.stop()
dcmotor.Wheels.cleanup()

# サンプル採取機構を機体に格納する
print("サンプル採取機構を機体に格納する")
sample_servo = Servo(sample_motor_pin)
try:
    sample_servo.rotate_cw_or_ccw(3.5)
    time.sleep(0.2)
    sample_servo.stop()
except KeyboardInterrupt:
    sample_servo.stop()