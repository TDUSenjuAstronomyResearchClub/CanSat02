"""
Module Name:<br> 
nineAxisSensor<br><br>
Description:<br> 
加速度・角速度・方位角を求めるプログラム。動作確認用実行ファイルはNineAxisSensorTest.py<br><br>
Library:<br>
BMX055<br>
pip install bmx055<br><br>
"""

import BMX055
import math
from gps import gps


class BMX055Sensor:
    """
    BMX055センサを制御し、加速度・角速度・方位角を求めるクラス。
    """

    def __init__(self, declination=0):
        """
        BMX055センサを初期化する。

        :param declination: 地磁気偏角（単位：度）。省略時はゼロを指定する。
        """
        self.bmx055 = BMX055.BMX055()
        self.declination = declination

    def get_acceleration(self):
        """
        加速度を取得する。
        Returns

        -------
        list
             加速度（x, y, z）（単位:m/s^2）
        bool
            OSErrorが発生した場合はTrueを返す。
        """
        try:
            raw_accel = self.bmx055.get_accel_data()
            return [x / 1000 for x in raw_accel]
        except OSError:
            return True

    def get_gyroscope(self):
        """
        角速度を取得する。

        Returns
        -------
        list
                角速度（x, y, z）（単位:rad/s）
        bool
            OSErrorが発生した場合はTrueを返す。
        """
        try:
            raw_gyro = self.bmx055.get_gyro_data()
            return [math.radians(x) for x in raw_gyro]
        except OSError:
            return True

    def get_magnetic_heading(self):
        """
        地磁気センサから方位角を計算する。

        Returns
        -------
        list
                方位角（単位：度）
        bool
            OSErrorが発生した場合はTrueを返す。
        """
        try:
            raw_mag = self.bmx055.get_mag_data()
            gps_date = gps.get_gps_data()

            # 地磁気偏角を適用する
            declination = self.calculate_declination(gps_date[0], gps_date[1])
            heading = math.atan2(raw_mag[1], raw_mag[0]) + math.radians(declination)

            # 方位角を0から360度の範囲にする
            heading = math.degrees(heading)
            if heading < 0:
                heading += 360.0

            return heading
        except OSError:
            return True
