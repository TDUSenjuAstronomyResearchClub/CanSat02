"""サーボモーターの動作確認用モジュール
各サーボモーターの役割に伴った動作をさせる
"""
from cansatapi.servo import Servo
import time

para_servo = Servo(23)
sample_servo = Servo(24)
soil_servo = Servo(25)

# パラシュート分離用モーターにパラシュート分離の動作をさせる
para_start_time = time.time()
try:
    while True:
        para_servo.rotate_to_angle(90)
        if time.time() - para_start_time >= 20:
            para_servo.rotate_to_angle(0)
            break
except KeyboardInterrupt:
    para_servo.rotate_to_angle(0)

time.sleep(1)

# サンプル採取用モーターにサンプル採取機構を土と接触させる動作をさせる
print("サンプル採取機構を土と接触させる")
sample_start_time = time.time()
try:
    while True:
        sample_servo.rotate_to_angle(90)
        if time.time() - sample_start_time >= 5:
            sample_servo.rotate_to_angle(0)
            break
except KeyboardInterrupt:
    sample_servo.rotate_to_angle(0)

# サンプル採取機構を機体に格納する
print("サンプル採取機構を機体に格納する")
start_pull_out_time = time.time()
try:
    while True:
        sample_servo.rotate_to_angle(-90)
        if time.time() - start_pull_out_time >= 10:
            sample_servo.rotate_to_angle(0)
            break
except KeyboardInterrupt:
    sample_servo.rotate_to_angle(0)

time.sleep(1)

# 土壌水分量測定モータで土壌水分センサを土に挿し込む
print("土壌水分センサを土に挿し込む")
start_insert_time = time.time()
try:
    while True:
        soil_servo.rotate_to_angle(90)
        if time.time() - start_insert_time >= 10:
            soil_servo.rotate_to_angle(0)
            break
except KeyboardInterrupt:
    soil_servo.rotate_to_angle(0)

# 土壌水分センサを機体に格納する
print("土壌水分センサを機体に格納する")
start_pull_out_time = time.time()
try:
    while True:
        soil_servo.rotate_to_angle(-90)
        if time.time() - start_pull_out_time >= 10:
            soil_servo.rotate_to_angle(0)
            break
except KeyboardInterrupt:
    soil_servo.rotate_to_angle(0)

