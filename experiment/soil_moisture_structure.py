"""土壌水分量測定の構造が正しく動作するかのテストモジュール
"""

from cansatapi.servo import Servo
from cansatapi.soil_moisture import SoilMoistureSensor
import time

# 土壌水分センサ差し込み用モータのgpioを指定
soil_servo = Servo(25)

sensor = SoilMoistureSensor()

# 土壌水分センサを土に挿し込む
start_insert_time = time.time()
try:
    while True:
        soil_servo.rotate_to_angle(90)
        # TODO: 土壌水分センサが土に挿入するのにかかる時間を測定し，変更・反映させる
        if time.time() - start_insert_time >= 10:
            soil_servo.rotate_to_angle(0)
            break
except KeyboardInterrupt:
    soil_servo.rotate_to_angle(0)

# 土壌水分量を出力
print(f"{sensor.get_soil_moisture()}")

# 土壌水分センサを機体に格納する
start_pull_out_time = time.time()
try:
    while True:
        soil_servo.rotate_to_angle(-90)
        # TODO: 土壌水分センサが機体に格納されるのにかかる時間を測定し，変更・反映させる
        if time.time() - start_pull_out_time >= 10:
            soil_servo.rotate_to_angle(0)
            break
except KeyboardInterrupt:
    soil_servo.rotate_to_angle(0)

