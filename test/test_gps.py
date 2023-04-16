import math
import unittest
from cansatapi.gps import *

if __name__ == "__main__":
    # GPSデータの取得
    latitude, longitude, altitude, declination = get_gps_data()

    # 結果の表示
    print("緯度：", latitude)
    print("経度：", longitude)
    print("海抜：", altitude)
    print("磁器偏角値：", declination)

    # 目的地の緯度経度
    dest_lat = 35.681236
    dest_lon = 139.767125

    # 現在地と目的地の距離と方位角を計算
    distance, bearing = calculate_distance_bearing(dest_lat, dest_lon)

    # 結果の表示
    print("目的地までの距離：", distance, "m")
    print("方位角：", bearing, "°")


class TestGPSMethods(unittest.TestCase):

    def test_lat_conv_deg_min_to_decimal(self):
        lat_deg_min = "3544.92"
        direction = "N"

        expect = 35.74866667
        decimal = lat_conv_deg_min_to_decimal(lat_deg_min, direction)

        # 浮動小数点のチェックなので、近似しているかどうかを検証する
        self.assertTrue(math.isclose(expect, decimal))

    def test_lan_conv_deg_min_to_decimal(self):
        lon_deg_min = "13948.38"
        direction = "E"

        expect = 139.80633333
        decimal = lon_conv_deg_min_to_decimal(lon_deg_min, direction)

        self.assertTrue(math.isclose(expect, decimal))
