"""サーボモーターの動作確認用モジュール
各サーボモーターの役割に伴った動作をさせる
"""
from cansatapi.servo import Servo
import time

para_servo = Servo(23)
sample_servo = Servo(24)
soil_servo = Servo(25)


# パラシュート分離用モーターにパラシュート分離の動作をさせる
print("パラシュート分離用モーターを動かす")
try:
    for _ in range(20):
        para_servo.rotate_cw_or_ccw(3.5)
        time.sleep(2)
except KeyboardInterrupt:
    para_servo.rotate_cw_or_ccw(7.5)
    para_servo.stop()

para_servo.stop()
time.sleep(1)

# サンプル採取用モーターにサンプル採取機構を土と接触させる動作をさせる
print("サンプル採取機構を土と接触させる")
try:

    sample_servo.rotate_cw_or_ccw(3.5)
    time.sleep(10)
except KeyboardInterrupt:
    sample_servo.rotate_cw_or_ccw(7.5)

# サンプル採取機構を機体に格納する
print("サンプル採取機構を機体に格納する")
try:
    sample_servo.rotate_cw_or_ccw(11.5)
    time.sleep(10)
except KeyboardInterrupt:
    sample_servo.rotate_cw_or_ccw(7.5)

sample_servo.stop()
time.sleep(1)

# 土壌水分量測定モータで土壌水分センサを土に挿し込む
print("土壌水分センサを土に挿し込む")
try:
    soil_servo.rotate_cw_or_ccw(3.5)
    time.sleep(10)
except KeyboardInterrupt:
    soil_servo.rotate_cw_or_ccw(7.5)

# 土壌水分センサを機体に格納する
print("土壌水分センサを機体に格納する")
try:
    soil_servo.rotate_cw_or_ccw(11.5)
    time.sleep(10)
except KeyboardInterrupt:
    soil_servo.rotate_cw_or_ccw(7.5)

soil_servo.stop()
