"""JSONジェネレータモジュール

各型式のJSONを作成するモジュールです。
"""
from __future__ import annotations

import json

from .type import SensorJson, Gps, NineAxis, Bme280, Lps25Hb


def generate_json(
    time: str = None,
    gps: Gps = None,
    nine_axis: NineAxis = None,
    bme280: Bme280 = None,
    lps25hb: Lps25Hb = None,
    battery: float = None,
    distance: float = None,
    camera: str = None,
    soil_moisture: float = None,
    message: str = None,
) -> str:
    """JSONを生成する関数

    各引数に値を入れると対応するJSONデータを生成します。

    Args:
        message: 任意のメッセージ
        soil_moisture: 土壌水分量[%]
        camera: カメラのヘックスデータ
        distance: 距離
        battery: バッテリー残量[%]
        lps25hb: LPS25HBのデータ
        bme280: BME280のデータ
        time (str): データの送信時時間
        gps (Gps): GPSデータ
        nine_axis (NineAxis): 9軸データ

    Returns:
        str: 生成されたJSON文字列
    """

    sensor_json: SensorJson = {
        "time": time,
        "gps": gps,
        "nine_axis": nine_axis,
        "bme280": bme280,
        "lps25hb": lps25hb,
        "battery": battery,
        "distance": distance,
        "camera": camera,
        "soil_moisture": soil_moisture,
        "message": message
    }

    return json.dumps(sensor_json)


