# ラズパイから各種センサの値を一定時間ごとに取得し、json形式のデータを作成するプログラム。
# json形式のデータを地上局に送信するのはsend_recive.pyのsend関数の中で行う。
import json
import sys
import time

import running  # 走行プログラムのソースファイル
import send_receive  # 地上局と値を送受信するプログラム

from serial import SerialException
import datetime

from cansatapi.nineaxissensor import NineAxisSensor
from cansatapi.barometer import Barometer
from cansatapi.batteryfuelgauge import BatteryFuelGauge
from cansatapi import distance as distance_sensor
from cansatapi import gps
from cansatapi.temperature import Temperature

nine_axis = NineAxisSensor()
barometer = Barometer()
battery_fuel_gauge = BatteryFuelGauge()
temperature = Temperature()

# ログファイルのファイル名を作成
dt_start = datetime.datetime.now()
start_time = 'send_sensor_data' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒')

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

    now = datetime.datetime.now()  # センサ値取得開始日時の取得

    try:
        gps_data = gps.get_gps_data()
        lat_lon = running.SeeValue()  # 走行プログラムに定義されているサンプル採取地点とゴール地点の緯度経度値を持ってくる
        sample_distance = gps.calculate_distance_bearing(lat_lon[0], lat_lon[1])
        goal_distance = gps.calculate_distance_bearing(lat_lon[2], lat_lon[3])
    except SerialException:
        print("Error: GPSとのシリアル通信でエラーが発生しました", file=sys.stderr)

    try:
        acc = nine_axis.get_acceleration()
        ang_velo = nine_axis.get_angular_rate()
        azimuth = nine_axis.get_magnetic_heading()
    except OSError:
        print("Error: 9軸センサと正常に通信できません", file=sys.stderr)

    try:
        bme280 = temperature.temperature_result()  # 温湿度気圧センサデータ
    except OSError:
        print("Error: 温湿度気圧センサと正常に通信できません", file=sys.stderr)

    try:
        lps25hb = barometer.get_pressure_altitude_temperature()  # 気圧センサ
    except OSError:
        print("Error: 気圧センサと正常に通信できません", file=sys.stderr)

    try:
        battery_level = battery_fuel_gauge.get_level()
    except OSError:
        print("Error: 電池残量計と正常に通信できません", file=sys.stderr)

    try:
        distance = distance_sensor.distance_result()
    except TypeError:
        print("Error: 超音波センサと正常に通信できません", file=sys.stderr)

    data = {
        "時間": now,
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

    send_receive.send(start_time, json.dumps(data))  # json形式のデータを送信する
    time.sleep(5)
