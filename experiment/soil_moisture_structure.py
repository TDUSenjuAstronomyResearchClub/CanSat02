"""土壌水分量測定の構造が正しく動作するかのテストモジュール
"""

from cansatapi.servo import Servo
from cansatapi.soil_moisture import SoilMoistureSensor
import time

# 土壌水分センサ差し込み用モータのpin番号を指定
soil_motor_pin = 25

# サーボモーターと土壌水分センサのインスタンスを宣言
soil_servo = Servo(soil_motor_pin)
sensor = SoilMoistureSensor()

try:
    print("土壌水分センサを土に挿し込む")
    soil_servo.rotate_ccw()
    time.sleep(0.5)
    soil_servo.rotate_stop()
except KeyboardInterrupt:
    soil_servo.finish()

# 土壌水分量を出力
print(f"{sensor.get_soil_moisture()}")

# 土壌水分センサを機体に格納する
try:
    print("土壌水分センサを機体に格納する")
    soil_servo.rotate_cw()
    time.sleep(0.5)
    soil_servo.finish()
except KeyboardInterrupt:
    soil_servo.finish()

