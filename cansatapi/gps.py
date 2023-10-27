"""緯度経度・海抜・磁気偏角・直線距離・方位角取得モジュール

GPSから緯度経度・海抜・磁気偏角を取得し、そこから2地点間の距離を計算します

使用しているライブラリ:
    pyserial
"""
import time
from math import radians, sin, cos, atan2, sqrt, pi

import serial


def get_gps_data() -> tuple[float, float, float]:
    """GPSデータを取得する関数

    Returns:
        list[float]: 緯度(ddmm.mm), 経度(dddmm.mm), 海抜(m)

    Raises:
        SerialError: シリアル通信時に発生する可能性がある
    """

    ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
    ser.flush()
    # type.pyでfloatとして扱っているので初期値を0.0にする
    lat = 0.0
    lon = 0.0
    alt = 0.0
    start_time = time.time()

    while time.time() - start_time < 5:  # 5秒後にタイムアウトします
        if ser.in_waiting > 0:
            line = ser.readline().decode("ASCII").rstrip()
            if line.startswith("GGA", 2):
                # 時刻・位置・GPS関連情報
                data = line.split(",")
                if data[6] != '0':  # データが有効かチェック
                    lat = lat_conv_deg_min_to_decimal(data[2], data[3])
                    lon = lon_conv_deg_min_to_decimal(data[4], data[5])
                    alt = float(data[10])
            elif line.startswith("GPGGA", 2):
                # 時刻や位置とGPS関連の情報
                data = line.split(",")
                if data[6] != '0':  # データが有効かチェック
                    lat = lat_conv_deg_min_to_decimal(data[2], data[3])
                    lon = lon_conv_deg_min_to_decimal(data[4], data[5])
                    alt = float(data[10])

            elif line.startswith("RMC", 2):
                # 衛星情報
                data = line.split(",")
                if data[2] == 'A':
                    lat = lat_conv_deg_min_to_decimal(data[3], data[4])
                    lon = lon_conv_deg_min_to_decimal(data[5], data[6])
            elif line.startswith("GPRMC", 2):
                # 衛星情報
                data = line.split(",")
                if data[2] == 'A':
                    lat = lat_conv_deg_min_to_decimal(data[3], data[4])
                    lon = lon_conv_deg_min_to_decimal(data[5], data[6])

            elif line.startswith("GPGLL", 2):
                # 地理的位置を取得
                data = line.split(",")
                if data[6] == 'A':
                    lat = lat_conv_deg_min_to_decimal(data[1], data[2])
                    lon = lat_conv_deg_min_to_decimal(data[3], data[4])
            break

    ser.close()
    return lat, lon, alt


def lat_conv_deg_min_to_decimal(lat: str, direction: str) -> float:
    """緯度を度分形式から10進数形式に変換する関数

    GPGGA緯度フォーマット: ddmm.mm
    https://gpsd.gitlab.io/gpsd/NMEA.html#_gga_global_positioning_system_fix_data

    Args:
        lat (str): 度分形式の緯度
        direction (str): 方向（N, Sのどちらか）

    Returns:
        float: 10進数形式の経度
    """
    d = float(lat[:2])
    m = float(lat[2:])
    decimal = d + m / 60

    if direction == "S":
        decimal *= -1

    return decimal


def lon_conv_deg_min_to_decimal(lon: str, direction: str) -> float:
    """経度を度分形式から10進数形式に変換する関数

    GPGGA経度フォーマット: dddmm.mm
    https://gpsd.gitlab.io/gpsd/NMEA.html#_gga_global_positioning_system_fix_data

    Args:
        lon (str): 度分形式の経度
        direction (str): 方向（E, Wのいずれか）

    Returns:
        float: 10進数形式の経度
    """
    d = float(lon[:3])
    m = float(lon[3:])
    decimal = d + m / 60

    if direction == "W":
        decimal *= -1

    return decimal


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
