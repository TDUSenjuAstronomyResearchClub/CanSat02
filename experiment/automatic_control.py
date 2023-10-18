"""機体が目的地に向かって進むかのテストモジュール
"""

import time

from cansatapi import *

# ToDo:試験前に記入
GOAL_LON: float = 35.758660
GOAL_LAT: float = 139.817332
DECLINATION: float = 7.78  # 磁気偏角値


def is_straight(lat: float, lon: float) -> bool:
    """指定された地点と機体が一定の範囲内に収まってたらTrueを返す関数

    Args:
        lat (float): 地点の緯度
        lon (float): 地点の経度
    """
    return gps.calculate_distance_bearing(lat, lon, DECLINATION)[0] - nineaxissensor \
        .nine_axis_sensor.get_magnetic_heading() < 30  # todo: ここの値は要確認


def angle_adjustment(lat: float, lon: float):
    """目的地と機体を一直線にする関数

    Args:
        lat (float): 地点の緯度
        lon (float): 地点の経度
    """
    gps_temp = gps.calculate_distance_bearing(lat, lon, DECLINATION)
    difference = gps_temp[1] - nineaxissensor.nine_axis_sensor.get_magnetic_heading()
    if difference >= 0:
        dcmotor.Wheels.r_pivot_fwd()
    else:
        dcmotor.Wheels.l_pivot_fwd()

    return


def main():
    """メインアルゴリズム
    """

    while True:
        # 1行動ごとにループを回す

        if is_straight(GOAL_LAT, GOAL_LON):
            dcmotor.Wheels.forward()  # 方位角が範囲に収まっていれば3秒直進
            time.sleep(3)
            dcmotor.Wheels.stop()
        else:
            angle_adjustment(GOAL_LAT, GOAL_LON)  # 収まっていなければ調整


if __name__ == "__main__":
    isAuto = True
    main()  # 実行
