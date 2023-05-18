import datetime
import time

from cansatapi.gps import get_gps_data
from cansatapi.util import logging
from cansatapi.util.logging import Logger

# 本番前に記入
SAMPLE_LON: float = 0.0
SAMPLE_LAT: float = 0.0

GOAL_LON: float = 0.0
GOAL_LAT: float = 0.0


def get_sample():
    # gps.pyの関数を呼び出してサンプル取得地点の緯度経度値を取得する処理を記述する
    # ここでは、仮の値として示すだけする
    # 要追記
    sample_let = []
    sample_let = get_gps_data()
    sample_latitude = sample_let[1]
    sample_longitude = sample_let[2]
    return sample_latitude, sample_longitude

def LandingJudgement():
    """着地判定をするまで待つ関数"""


def SeeValue():
    # gps.pyからサンプル取得地点の緯度経度値を取得
    sample_latitude, sample_longitude = get_sample()

    # ゴールの緯度経度値
    goal_latitude = 35.6789
    goal_longitude = 139.0123

    FallJudgement()
    XBee.send_msg("Detect falling")

    LandingJudgement()
    XBee.send_msg("Landed")

    detach_parachute(main_logger)


if __name__ == "__main__":
    main()  # 実行
