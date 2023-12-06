"""サーボモーターの動作確認用モジュール
各サーボモーターの役割に伴った動作をさせる
"""
from cansatapi.servo import Servo
import time


para_servo = Servo(23)
# パラシュート分離用モーターにパラシュート分離の動作をさせる
print("パラシュート分離用モーターを動かす")
try:
    para_servo.rotate_cw()
    time.sleep(10)
    para_servo.finish()
except KeyboardInterrupt:
    para_servo.finish()

time.sleep(1)


sample_servo = Servo(25)
# サンプル採取用モーターにサンプル採取機構を土と接触させる動作をさせる
print("サンプル採取機構を土と接触させる")
try:
    sample_servo.rotate_ccw()
    time.sleep(0.2)
    sample_servo.rotate_stop()
except KeyboardInterrupt:
    sample_servo.finish()

time.sleep(1)

# サンプル採取機構を機体に格納する
print("サンプル採取機構を機体に格納する")
try:
    sample_servo.rotate_cw()
    time.sleep(0.2)
    sample_servo.finish()
except KeyboardInterrupt:
    sample_servo.finish()
time.sleep(1)


soil_servo = Servo(24)
# 土壌水分量測定モータで土壌水分センサを土に挿し込む
print("土壌水分センサを土に挿し込む")
try:
    soil_servo.rotate_cw()
    time.sleep(10)
    soil_servo.rotate_stop()
except KeyboardInterrupt:
    soil_servo.finish()

time.sleep(1)

# 土壌水分センサを機体に格納する
print("土壌水分センサを機体に格納する")
try:
    soil_servo.rotate_ccw()
    time.sleep(10)
    soil_servo.finish()
except KeyboardInterrupt:
    soil_servo.finish()
