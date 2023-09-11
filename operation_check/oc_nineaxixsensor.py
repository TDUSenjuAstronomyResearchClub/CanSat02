"""9軸センサ(BMX055)用の動作確認モジュール
"""
from cansatapi.nineaxissensor import NineAxisSensor
import sys
import time
import math

if __name__ == "__main__":
    nineaxis = NineAxisSensor()
    while True:
        try:
            acc = nineaxis.get_acceleration()
            accel_abs = math.sqrt(acc[0] ** 2 + acc[1] ** 2 + acc[2] ** 2)  # 9軸から加速度の大きさを求める
            print(f'加速度 X: {acc[0]}, Y: {acc[1]}, Z: {acc[2]},絶対値{accel_abs}')

            ang_rate = nineaxis.get_angular_rate()
            print(f'角速度 X: {ang_rate[0]}, Y: {ang_rate[1]}, Z: {ang_rate[2]}')

            heading = nineaxis.get_magnetic_heading()
            print(f'方位角: {heading}')

            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)
        except OSError as e:
            print(e)
