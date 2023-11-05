"""サーボモーターの動作確認用モジュール
各サーボモーターの役割に伴った動作をさせる
"""
from cansatapi.servo import Servo
import time


# パラシュート分離用モーターにパラシュート分離の動作をさせる
print("パラシュート分離用モーターを動かす")
para_servo = Servo(23)
try:
    para_servo.rotate_cw_or_ccw(3.5)
    time.sleep(10)
except KeyboardInterrupt:
    para_servo.rotate_cw_or_ccw(7.5)
    para_servo.stop()
para_servo.stop()
time.sleep(1)


# サンプル採取用モーターにサンプル採取機構を土と接触させる動作をさせる
print("サンプル採取機構を土と接触させる")
sample_servo = Servo(24)
try:
    sample_servo.rotate_cw_or_ccw(11.5)
    time.sleep(0.3)
except KeyboardInterrupt:
    sample_servo.rotate_cw_or_ccw(7.5)
sample_servo.stop()
time.sleep(1)

# サンプル採取機構を機体に格納する
print("サンプル採取機構を機体に格納する")
sample_servo = Servo(24)
try:
    sample_servo.rotate_cw_or_ccw(3.5)
    time.sleep(0.3)
except KeyboardInterrupt:
    sample_servo.rotate_cw_or_ccw(7.5)
sample_servo.stop()
time.sleep(1)


# 土壌水分量測定モータで土壌水分センサを土に挿し込む
print("土壌水分センサを土に挿し込む")
soil_servo = Servo(25)
try:
    soil_servo.rotate_cw_or_ccw(3.5)
    time.sleep(0.5)
except KeyboardInterrupt:
    soil_servo.rotate_cw_or_ccw(7.5)
soil_servo.stop()
time.sleep(1)

# 土壌水分センサを機体に格納する
print("土壌水分センサを機体に格納する")
soil_servo = Servo(25)
try:
    soil_servo.rotate_cw_or_ccw(11.5)
    time.sleep(0.5)
except KeyboardInterrupt:
    soil_servo.rotate_cw_or_ccw(7.5)
soil_servo.stop()
