"""
Module Name: <br>
緯度経度・海抜・磁器偏角・直線距離・方位角取得プログラム<br><br>
Description:<br>
gps.pyから緯度経度、海抜、磁器偏角を取得し、ゴールと機体との直線距離と方位角を求めるプログラム<br><br>

Library:<br>
serial<br>
「pip install --upgrade pip」を行いpipを最新版にします<br>
「pip install pyserial」このコマンドを打つことでpyserialを導入できます<br>
"""

import serial
import time
from math import radians, sin, cos, atan2, sqrt, pi


def get_gps_data():
    """
    GPSデータを取得する関数

    Returns
    -------
    lat : float
            度分形式の緯度
    lon : float
            度分形式の経度
    alt : float
            海抜
    declination : float
            磁気偏角(度)
    """

    ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
    ser.flush()
    lat = None
    lon = None
    alt = None
    declination = None
    start_time = time.time()

    while time.time() - start_time < 5:  # 5秒後にタイムアウトします
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").rstrip()
                if line.startswith("$GPGGA"):
                    # 時刻・位置・GPS関連情報
                    data = line.split(",")
                    lat = lat_conv_deg_min_to_decimal(data[1], data[2])
                    lon = lon_conv_deg_min_to_decimal(data[3], data[4])
                    alt = float(data[9])
                elif line.startswith("$GPRMC"):
                    # 衛星情報
                    data = line.split(",")
                    lat = lat_conv_deg_min_to_decimal(data[2], data[3])
                    lon = lon_conv_deg_min_to_decimal(data[4], data[5])

                    # 磁気偏差
                    declination = float(data[11])
                    break
        except Exception as e:
            print(e)
            continue

    ser.close()
    return lat, lon, alt, declination


def lat_conv_deg_min_to_decimal(lat, direction):
    """
    緯度を度分形式から10進数形式に変換する関数

    GPGGA緯度フォーマット: ddmm.mm
    https://gpsd.gitlab.io/gpsd/NMEA.html#_gga_global_positioning_system_fix_data
    Args
    -------
    lat : str
            度分形式の緯度
    direction : str
            方向（N, Sのどちらか）

    Returns
    -------
    degree : float
            10進数形式の経度
    """
    d = float(lat[:2])
    m = float(lat[2:])
    degree = d + m / 60

    if direction == "S":
        degree *= -1

    return degree


def lon_conv_deg_min_to_decimal(lon, direction):
    """
    経度を度分形式から10進数形式に変換する関数

    GPGGA経度フォーマット: dddmm.mm
    https://gpsd.gitlab.io/gpsd/NMEA.html#_gga_global_positioning_system_fix_data
    Args
    -------
    lon : str
            度分形式の経度
    direction : str
            方向（E, Wのいずれか）

    Returns
    -------
    degree : float
            10進数形式の経度
    """
    d = float(lon[:3])
    m = float(lon[3:])
    degree = d + m / 60

    if direction == "W":
        degree *= -1

    return degree


def calculate_distance_bearing(lat2, lon2):
    """
    2地点の緯度経度から直線距離と方位角を計算する関数

    Args
    -------
    lat2 : float
            目的地の緯度
    lon2 : float
            方向（N, E, S, Wのいずれか）

    Returns
    -------
    distance(float)
            2地点間の直線距離 
    bearing(float)
            2地点間の方位角 
    """
    r = 6371  # 地球の半径（km）
    try:
        # gpsの緯度経度・磁器偏角値を取得
        gps_date = get_gps_data()
        lat1 = gps_date[0]
        lon1 = gps_date[1]
        declination = gps_date[3]

        # 緯度経度をラジアンに変換
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # 2地点間の距離
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = r * c * 1000

        # 方位角
        y = sin(lon2 - lon1) * cos(lat2)
        x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1)
        bearing = (atan2(y, x) * 180 / pi + 360) % 360

        # 磁気偏角の補正
        bearing = (bearing + declination) % 360

        return distance, bearing
    except TypeError:
        distance = None
        bearing = None
        return distance, bearing
