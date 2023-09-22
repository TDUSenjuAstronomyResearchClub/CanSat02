"""JSONジェネレータモジュール

各型式のJSONを作成するモジュールです。
"""
from __future__ import annotations

import json

from .type import SensorJson, Gps, NineAxis, Bme280, Lps25Hb


def generate_json(
    data_type: str = None,
    time: float = 0.0,
    gps: Gps = 0.0,
    nine_axis: NineAxis = 0.0,
    bme280: Bme280 = 0.0,
    lps25hb: Lps25Hb = 0.0,
    battery: float = 0.0,
    distance: float = 0.0,
    camera: str = None,
    soil_moisture: float = 0.0,
    message: str = None,
) -> str:
    """JSONを生成する関数

    各引数に値を入れると対応するJSONデータを生成します。

    Args:
        data_type: sonファイルに何のデータが入っているか判定する
        time (float): データの送信時時間
        gps (Gps): GPSデータ
        nine_axis (NineAxis): 9軸データ
        bme280: BME280のデータ
        lps25hb: LPS25HBのデータ
        battery: バッテリー残量[%]
        distance: 距離
        camera: カメラのヘックスデータ
        soil_moisture: 土壌水分量[%]
        message: 任意のメッセージ

    Returns:
        str: 生成されたJSON文字列
    """

    sensor_json: SensorJson = {
        "data_type": data_type,
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
    return json.dumps(clean_nones(sensor_json))


def clean_nones(dict_data: dict) -> dict:
    """値がNoneの要素を再帰的に取り除く

    Args:
        dict_data (dict): 辞書型データ

    Returns:
        dict: Noneの要素が取り除かれたデータ
    """
    for key, value in list(dict_data.items()):
        if value is None:
            del dict_data[key]
        elif isinstance(value, dict):
            clean_nones(value)
    return dict_data
