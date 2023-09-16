"""サンプル採取地点とゴール地点の緯度経度、磁気偏角値が挿入されているモジュール
"""

SAMPLE_LON: float = 0.0
SAMPLE_LAT: float = 0.0
GOAL_LON: float = 0.0
GOAL_LAT: float = 0.0
DECLINATION: float = 0.0  # 磁気偏角値


def get_lon_lat_decl():
    """サンプル採取地点とゴール地点の緯度経度を取得する関数

    Returns:
            list:[サンプル地点経度、サンプル地点緯度、ゴール地点経度、ゴール地点緯度、磁気偏角値]
    """
    return [SAMPLE_LON, SAMPLE_LAT, GOAL_LON, GOAL_LAT, DECLINATION]
