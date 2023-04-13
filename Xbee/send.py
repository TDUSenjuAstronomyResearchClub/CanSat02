import json
import datetime

import serial
import time

from ..gps import gps
from ..nineAxisSensor.nine_axis import BMX055Sensor as NineAxis
from ..temperature import temperature
from ..pressure import barometric_press
from ..battery import battery
from ..distance import distance

import Running  # 走行プログラムのソースファイル

# ポート設定
PORT = '/dev/ttyUSB0'

# 通信レート設定
BAUD_RATE = 9600

nine_axis = NineAxis()

while True:
    gps_data = gps.get_gps_data()
    lat_lon = Running.SeeValue()    # 走行プログラムに定義されているサンプル採取地点とゴール地点の緯度経度値を持ってくる
    sample_distance = gps.calculate_distance_bearing(lat_lon[0], lat_lon[1])
    goal_distance = gps.calculate_distance_bearing(lat_lon[2], lat_lon[3])

    acc = nine_axis.get_acceleration()
    ang_velo = nine_axis.get_gyroscope()
    azimuth = nine_axis.get_magnetic_heading()

    bme280 = temperature.temperature_result()  # 温湿度気圧センサデータ
    lps25hb = barometric_press.get_pressure_altitude_temperature()  # 気圧センサ

    data = {
        "gps": {
            "緯度": gps_data[0],
            "経度": gps_data[1],
            "海抜": gps_data[2],

            "サンプル": {
                "直線距離": sample_distance[0],
                "方位角": sample_distance[1]
            },
            "ゴール": {
                "直線距離": goal_distance[0],
                "方位角": goal_distance[1]
            }
        },
        "9軸": {
            "加速度": {
                "X": acc[0],
                "Y": acc[1],
                "Z": acc[2]
            },
            "角速度": {
                "X": ang_velo[0],
                "Y": ang_velo[1],
                "Z": ang_velo[2]
            },
            "方位角": {
                "X": azimuth[0],
                "Y": azimuth[1],
                "Z": azimuth[2]
            }
        },
        "温湿度気圧": {
            "温度": bme280[0],
            "湿度": bme280[1],
            "気圧": bme280[2]
        },
        "気圧": {
            "気圧": lps25hb[0],
            "高度": lps25hb[1],
            "温度": lps25hb[2]
        },
        "電池": battery.get_battery_level(),
        "距離": distance.distance_result()
    }

    dt_start = datetime.datetime.now()
    start_time = 'sending' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒')

    f = open(start_time, 'a')

    # jsonとして書き込み
    json.dump(data, f, indent=4, ensure_ascii=False)

    ser = serial.Serial(PORT, BAUD_RATE)
    # シリアルにjsonを書き込む
    ser.write(bytes(json.load(f), 'utf-8'))
    ser.close()
    f.close()

    time.sleep(1)
