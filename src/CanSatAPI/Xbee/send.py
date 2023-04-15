import json
import datetime
import sys

import serial
from serial import SerialException
import time

from src.CanSatAPI.gps import gps
from src.CanSatAPI.nineAxisSensor.nine_axis import BMX055Sensor as NineAxis
from src.CanSatAPI.temperature import temperature
from src.CanSatAPI.pressure import barometric_press
from src.CanSatAPI.battery import battery as battery_gauge
from src.CanSatAPI.distance import distance as distance_sensor

import Running  # 走行プログラムのソースファイル

# ポート設定
PORT = '/dev/ttyUSB0'

# 通信レート設定
BAUD_RATE = 9600

nine_axis = NineAxis()

while True:
    # ここで初期化することで、エラーが出たときにNoneで値を送れる
    gps_data: list[float] | None = None
    lat_lon = None
    sample_distance: list[float] | None = None
    goal_distance: list[float] | None = None
    acc: list[float] | None = None
    ang_velo: list[float] | None = None
    azimuth: float | None = None
    bme280: list | None = None
    lps25hb: list[float] | None = None
    battery_level: int | None = None
    distance: float | None = None

    try:
        gps_data = gps.get_gps_data()
        lat_lon = Running.SeeValue()    # 走行プログラムに定義されているサンプル採取地点とゴール地点の緯度経度値を持ってくる
        sample_distance = gps.calculate_distance_bearing(lat_lon[0], lat_lon[1])
        goal_distance = gps.calculate_distance_bearing(lat_lon[2], lat_lon[3])
    except SerialException:
        print("Error: GPSとのシリアル通信でエラーが発生しました", file=sys.stderr)

    try:
        acc = nine_axis.get_acceleration()
        ang_velo = nine_axis.get_gyroscope()
        azimuth = nine_axis.get_magnetic_heading()
    except OSError:
        print("Error: 9軸センサと正常に通信できません", file=sys.stderr)

    try:
        bme280 = temperature.temperature_result()  # 温湿度気圧センサデータ
    except OSError:
        print("Error: 温湿度気圧センサと正常に通信できません", file=sys.stderr)

    try:
        lps25hb = barometric_press.get_pressure_altitude_temperature()  # 気圧センサ
    except OSError:
        print("Error: 気圧センサと正常に通信できません", file=sys.stderr)

    try:
        battery_level = battery_gauge.get_battery_level()
    except OSError:
        print("Error: 電池残量計と正常に通信できません", file=sys.stderr)

    try:
        distance = distance_sensor.distance_result()
    except TypeError:
        print("Error: 超音波センサと正常に通信できません", file=sys.stderr)

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
            "方位角": azimuth
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
        "電池": battery_level,
        "距離": distance
    }

    dt_start = datetime.datetime.now()
    start_time = 'sending' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒')

    f = open(start_time, 'a')

    # jsonとして書き込み
    json.dump(data, f, indent=4, ensure_ascii=False)

    try:
        ser = serial.Serial(PORT, BAUD_RATE)
        # シリアルにjsonを書き込む
        ser.write(bytes(json.load(f), 'utf-8'))
        ser.close()
    except SerialException as msg:
        # todo: 地上局にエラーを送信
        print('Error: シリアルポートでエラーが発生しました', file=sys.stderr)

    f.close()

    time.sleep(1)
