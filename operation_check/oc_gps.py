"""GPSの動作確認用モジュール
"""
import sys

from cansatapi.gps import *

if __name__ == "__main__":
    while True:
        try:
            # GPSデータの取得
            latitude, longitude, altitude = get_gps_data()

            # 結果の表示
            print("緯度：", latitude)
            print("経度：", longitude)
            print("海抜：", altitude)
            # 目的地の緯度経度
            dest_lat = 35.681236
            dest_lon = 139.767125

            # 現在地と目的地の距離と方位角を計算
            # 2020年の能代の磁気偏差は9°10'
            distance, bearing = calculate_distance_bearing(dest_lat, dest_lon, 9.167)

            # 結果の表示
            print("目的地までの距離：", distance, "m")
            print("方位角：", bearing, "°")
        except KeyboardInterrupt:
            sys.exit(0)
