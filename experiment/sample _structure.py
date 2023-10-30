"""サンプル採取機構が正しく動作するかのテストモジュール
"""
from cansatapi.servo import Servo
from cansatapi import *
import time

# サンプル採取用サーボモーターのgpioを指定
sample_servo = Servo(24)

start_hang_down_time = time.time()

# サンプル採取機構を土と接触させる
print("サンプル採取機構を土と接触させる")
try:
    while True:
        sample_servo.rotate_to_angle(90)
        # TODO: サンプル採取機構が土と接触するのにかかる時間を測定し，変更・反映させる
        if time.time() - start_hang_down_time >= 5:
            sample_servo.rotate_to_angle(0)
            break
except KeyboardInterrupt:
    sample_servo.rotate_to_angle(0)

# 機体を前進させ，土をサンプル採取機構の中に入れる
dcmotor.Wheels.forward()
time.sleep(3)
dcmotor.Wheels.stop()
dcmotor.Wheels.cleanup()

# サンプル採取機構を機体に格納する
start_pull_out_time = time.time()
try:
    while True:
        sample_servo.rotate_to_angle(-90)
        # TODO: サンプル採取機構が機体に格納されるのにかかる時間を測定し，変更・反映させる
        if time.time() - start_pull_out_time >= 10:
            sample_servo.rotate_to_angle(0)
            break
except KeyboardInterrupt:
    sample_servo.rotate_to_angle(0)

