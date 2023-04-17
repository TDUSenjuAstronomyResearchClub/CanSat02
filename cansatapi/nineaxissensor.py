"""加速度・角速度・方位角を求めるモジュール

使用しているライブラリ:
    bmx055
"""

# todo: BMX055は存在しない
import BMX055
import math
from . import gps


class NineAxisSensor:
    """BMX055センサを制御し、加速度・角速度・方位角を求めるクラス

    データシート: https://akizukidenshi.com/download/ds/bosch/BST-BMX055-DS000.pdf
    """

    def __init__(self, declination: float = 0):
        """BMX055センサを初期化する

        Args:
            declination (float): 地磁気偏角（単位：度）。省略時はゼロを指定する。
        """
        self.bmx055 = BMX055.BMX055()
        self.declination = declination

    def get_acceleration(self) -> list[float]:
        """加速度を取得する
        Returns:
            list[float]: 加速度（x, y, z）（単位:m/s^2）

        Raises:
        OSError: I2C通信が正常に行えなかった際に発生
        """
        raw_accel = self.bmx055.get_accel_data()
        return [x / 1000 for x in raw_accel]

    def get_gyroscope(self) -> list[float]:
        """角速度を取得する

        Returns:
            list[float]: 角速度（x, y, z）（単位:rad/s）
        
        Raises:
        OSError: I2C通信が正常に行えなかった際に発生
        """
        raw_gyro = self.bmx055.get_gyro_data()
        return [math.radians(x) for x in raw_gyro]

    def get_magnetic_heading(self) -> float:
        """地磁気センサから方位角を計算する

        Returns:
            float: 方位角（単位：度）

        Raises:
        OSError: I2C通信が正常に行えなかった際に発生
        """
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
