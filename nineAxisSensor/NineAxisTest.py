import nineAxisSensor
import time

while True:
    sensor = nineAxisSensor.BMX055Sensor(declination=7.8) # 磁気偏角（2021年時点で秋田県能代市の磁気偏角は7.8度とされている）

    acceleration = sensor.get_acceleration()
    print(f"Acceleration: {acceleration} m/s^2")

    gyroscope = sensor.get_gyroscope()
    print(f"Gyroscope: {gyroscope} rad/s")

    magnetic_heading = sensor.get_magnetic_heading()
    print(f"Magnetic heading: {magnetic_heading} degrees")

    time.sleep(1)