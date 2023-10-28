"""緯度経度・海抜・磁気偏角・直線距離・方位角取得モジュール

GPSから緯度経度・海抜・磁気偏角を取得し、そこから2地点間の距離を計算します

使用しているライブラリ:
    pyserial
    micropyGPS
"""
import time
from math import radians, sin, cos, atan2, sqrt, pi
from micropyGPS import MicropyGPS

import serial


def get_gps_data() -> tuple[float, float, float]:
    """GPSデータを取得する関数

    Returns:
        list[float]: 緯度(ddmm.mm), 経度(dddmm.mm), 海抜(m)

    Raises:
        SerialError: シリアル通信時に発生する可能性がある
    """
    # シリアル通信設定
    ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
    ser.flush()  # 送信バッファをクリア

    # gpsの設定(UTCとのタイムゾーン差が日本は9時間, 10進数形式で値を取り出す）
    my_gps = MicropyGPS(9, 'dd')

    # 緯度経度・海抜の変数初期化
    lat = 0.0
    lon = 0.0
    alt = 0.0

    sentence = ser.readline()
    # シリアル通信で受信しているか
    if len(sentence) > 0:
        for x in sentence:
            if 10 <= x <= 126:  # 文字列の長さの正弦がupdateにはあるため
                stat = my_gps.update(chr(x))
                if stat:
                    lat = my_gps.latitude[0]
                    lon = my_gps.longitude[0]
                    alt = my_gps.altitude
    ser.close()
    return lat, lon, alt


def calculate_distance_bearing(lat: float, lon: float, declination: float) -> tuple[float, float]:
    """機体の現在地点から指定された地点の緯度経度までの直線距離と方位角を計算する関数

    Args:
        lat (float): 目的地の緯度
        lon (float): 目的地の経度
        declination (float): 磁気偏差

    Returns:
        tuple[Optional[float], Optional[float]]: 2地点間の直線距離, 現在地点から見た方位角
    """
    # gpsの緯度経度・磁器偏角値を取得
    gps_data = get_gps_data()

    # 初期値をNoneから0.0に変更したのでコメントアウト
    # if (gps_data[0] is None) or (gps_data[1] is None):
    # return 0.0, 0.0
    return calc_distance_between_two_points(gps_data[0], gps_data[1], lat, lon, declination)


def calc_distance_between_two_points(from_lat: float, from_lon: float,
                                     dest_lat: float, dest_lon, declination: float) -> tuple[float, float]:
    """指定された2地点間の距離と始点からの方位角を返す関数

    Args:
        from_lat (float): 始点の緯度
        from_lon (float): 始点の経度
        dest_lat (float): 終点の緯度
        dest_lon (float): 終点の緯度
        declination (float): 補正に使う磁気偏差

    Returns:
        tuple[Optional[float], Optional[float]]: 2地点間の直線距離, 始点から見た方位角
    """
    from_lat, from_lon, dest_lat, dest_lon = map(radians, [from_lat, from_lon, dest_lat, dest_lon])

    r = 6371  # 地球の半径（km
    # 2地点間の距離
    dlat = dest_lat - from_lat
    dlon = dest_lon - from_lon
    a = sin(dlat / 2) ** 2 + cos(from_lat) * cos(dest_lat) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c * 1000

    # 方位角
    y = sin(dest_lon - from_lon) * cos(dest_lat)
    x = cos(from_lat) * sin(dest_lat) - sin(from_lat) * cos(dest_lat) * cos(dest_lon - from_lon)
    bearing = (atan2(y, x) * 180 / pi + 360) % 360

    # 磁気偏角の補正
    bearing = (bearing + declination) % 360

    return distance, bearing
