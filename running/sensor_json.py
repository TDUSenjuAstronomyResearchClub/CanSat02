""" ラズパイから各種センサの値を一定時間ごとに取得し、JSON形式のデータを作成するモジュール

JSON形式のデータを地上局に送信するのはsend_receive.pyのsend関数の中で行う。
"""
import json
import sys
import time

import running  # 走行プログラムのソースファイル
from cansatapi.xbee import XBee  # 地上局と値を送受信するプログラム

from serial import SerialException
import datetime

from cansatapi.nineaxissensor import NineAxisSensor
from cansatapi.lps25hb import LPS25HB
from cansatapi.batteryfuelgauge import BatteryFuelGauge
from cansatapi import distance as distance_sensor
from cansatapi import gps
from cansatapi.bme280 import BME280

nine_axis = NineAxisSensor()
barometer = LPS25HB()
battery_fuel_gauge = BatteryFuelGauge()
temperature = BME280()

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
        "time": now,
        "gps": {
            "latitude": gps_data[0],
            "longitude": gps_data[1],
            "altitude": gps_data[2],

            "distance": {
                "sample": {
                    "description": sample_distance[0],
                },
                "goal": {
                    "description": goal_distance[0],
                }
            },
            "azimuth": {
                "sample": {
                    "description": sample_distance[1]
                },
                "goal": {
                    "description": goal_distance[1]
                }
            }
        },

        "nine-axis": {
            "acceleration": {
                "X": acc[0],
                "Y": acc[1],
                "Z": acc[2]
            },
            "angular-velocity": {
                "X": ang_velo[0],
                "Y": ang_velo[1],
                "Z": ang_velo[2]
            },
            "azimuth": azimuth
        },

        "bme280": {
            "temperature": bme280[0],
            "humidity": bme280[1],
            "pressure": bme280[2]
        },

        "lps25hb": {
            "temperature": lps25hb[2],
            "pressure": lps25hb[0],
            "altitude": lps25hb[1]
        },
        "battery": battery_level,
        "distance": distance
    }

    XBee.send(json.dumps(data))  # json形式のデータを送信する
    time.sleep(5)
