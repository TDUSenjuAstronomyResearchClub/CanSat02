import json
import datetime

import serial

from ..gps import GPS
from ..nineAxisSensor.NineAxis import BMX055Sensor as NineAxis
from ..temperature import Temperature
from ..pressure import BarometricPress
from ..battery import Battery
from ..distance import Distance

import Runing #走行プログラムのソースファイル

# ポート設定
PORT = '/dev/ttyUSB0'

# 通信レート設定
BAUD_RATE = 9600

dt_start = datetime.datetime.now()
start_time = 'sending' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒')

while True:
    gps_data = GPS.get_gps_data()
    
    gps_distance = GPS.calculate_distance_bearing()
    nineAxis = NineAxis()
    bme280 = Temperature.Temperature_result()  # 温湿度気圧センサデータ
    lps25hb = BarometricPress.get_pressure_altitude_temperature()  # 気圧センサ
    data = {
        "gps": {
            "緯度": gps_data[0],
            "経度": gps_data[1],
            "海抜": gps_data[2],
            # todo 距離計算モジュールがどこにあるかわからない
            "サンプル": {
                "直線距離": 1,
                "方位角": 2
            },
            "ゴール": {
                "直線距離": 1,
                "方位角": 2
            }
        },
        "9軸": {
            "加速度": nineAxis.get_acceleration(),
            "角速度": nineAxis.get_gyroscope(),
            "方位角": nineAxis.get_magnetic_heading()
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
        "電池": Battery.get_battery_level(),
        "距離": Distance.distance_result()
    }

    datetime.datetime.now()
    'sending' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒')

    f = open(start_time, 'a')
    ser = serial.Serial(PORT, BAUD_RATE)

    # jsonとして書き込み
    json.dump(data, f, indent=4, ensure_ascii=False)

    # シリアルにjsonを書き込む
    ser.write(bytes(json.load(f), 'utf-8'))
    f.close()
