import datetime
import time

from cansatapi.util import logger
from cansatapi.util.logger import Logger
from cansatapi.gps import get_gps_data
from cansatapi import *

# 本番前に記入
SAMPLE_LON: float = 0.0
SAMPLE_LAT: float = 0.0

GOAL_LON: float = 0.0
GOAL_LAT: float = 0.0


# gps.pyからサンプル取得地点の緯度経度値を取得する関数


def get_sample():
    # gps.pyの関数を呼び出してサンプル取得地点の緯度経度値を取得する処理を記述する
    # ここでは、仮の値として示すだけする
    # 要追記

    sample_latitude = 35.6789
    sample_longitude = 139.0123
    return sample_latitude, sample_longitude


# SeeValueに渡す緯度経度値を含む関数


def SeeValue():
    # gps.pyからサンプル取得地点の緯度経度値を取得
    sample_latitude, sample_longitude = get_sample()

    # ゴールの緯度経度値
    goal_let = []
    goal_let = get_gps_data()
    goal_latitude = goal_let[1]
    goal_longitude = goal_let[2]

    # ゴール地点とサンプル取得地点の値を表示
    print("ゴール地点の緯度経度値:", goal_latitude, goal_longitude)
    print("サンプル取得地点の緯度経度値:", sample_latitude, sample_longitude)

    # ゴール地点とサンプル取得地点の値を返す
    # 関数を呼び出せば求める値が返ってくる予定
    # ゴールの緯度経度、サンプル取得地点の緯度経度の順で返す
    return goal_latitude, goal_longitude, sample_latitude, sample_longitude


# 関数を呼び出して緯度経度値を表示


result = SeeValue()

# 結果の仮想処理 要削除
print("結果の仮想処理:")
goal_latitude, goal_longitude, sample_latitude, sample_longitude = result
# ここで結果を使った処理を行う
print("ゴール地点の緯度経度値:", goal_latitude, goal_longitude)
print("サンプル取得地点の緯度経度値:", sample_latitude, sample_longitude)


def FallJudgement():
    """落下判定をするまで待つ関数
    """


def LandingJudgement():
    """着地判定をするまで待つ関数"""


def detach_parachute(logger: Logger):
    """パラシュートの切り離しを行います
    """
    para_motor = dcmotor.DCMotor(9, 10)
    logger.msg("パラシュート切り離し開始")
    para_motor.forward()

    time.sleep(10)  # 10秒間巻取り

    para_motor.stop()
    para_motor.cleanup()
    logger.msg("パラシュート切り離し終了")


def main():
    """メインアルゴリズム
    """
    main_logger = Logger("Running" + datetime.datetime.now().strftime(logger.DATETIME_F))
    XBee.send_msg("Start running")

    FallJudgement()
    XBee.send_msg("Detect falling")

    LandingJudgement()
    XBee.send_msg("Landed")

    detach_parachute(main_logger)


if __name__ == "__main__":
    main()  # 実行
