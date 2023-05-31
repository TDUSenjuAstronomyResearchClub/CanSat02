import datetime
from enum import Enum
import time
from multiprocessing import Process

from cansatapi import *
from cansatapi.util import logging
from cansatapi.util.logging import Logger


class Mode(Enum):
    """制御モードを表すクラス
    """
    AUTO = 0
    MANUAL = 1


# 本番前に記入
SAMPLE_LON: float = 0.0
SAMPLE_LAT: float = 0.0

GOAL_LON: float = 0.0
GOAL_LAT: float = 0.0

DECLINATION: float = 0.0

# 共有変数
mode: Mode = Mode.AUTO


def manual_mode(cmd: str):
    """手動制御を行う関数

    Args:
        cmd(str): コマンド文字列
    """
    if cmd == "forward":
        dcmotor.Wheels.forward()
    elif cmd == "reverse":
        dcmotor.Wheels.reverse()
    elif cmd == "right":
        dcmotor.Wheels.r_pivot_fwd()
    elif cmd == "left":
        dcmotor.Wheels.l_pivot_fwd()

    time.sleep(3)
    dcmotor.Wheels.stop()


def FallJudgement() -> bool:
    """落下判定を返す関数
    """


def LandingJudgement() -> bool:
    """着地判定を返す関数
    """


def detach_parachute(logger: Logger):
    """パラシュートの切り離しを行います
    """
    para_motor = dcmotor.DCMotor(dcmotor.PARACHUTE_FIN, dcmotor.PARACHUTE_RIN)
    wheels = dcmotor.WheelController()
    logger.msg("パラシュート切り離し開始")
    para_motor.forward()
    wheels.forward()

    time.sleep(10)  # 10秒間巻取り&前進

    para_motor.stop()
    para_motor.cleanup()
    logger.msg("パラシュート切り離し終了")


def is_straight(lat: float, lon: float) -> bool:
    """指定された地点と機体が一定の範囲内に収まってたらTrueを返す関数

    Args:
        lat (float): 地点の緯度
        lon (float): 地点の経度
    """
    return gps.calculate_distance_bearing(lat, lon, DECLINATION)[0] - nineaxissensor\
        .nine_axis_sensor.get_magnetic_heading() < 30  # todo: ここの値は要確認


def angle_adjustment():
    """目的地と機体を一直線にする関数
    """


def is_goal() -> bool:
    """gps.calculate_distance_bearingの距離をもとにゴールについたか判定する関数
    """


def soil_moisture():
    """土壌水分量を測定する関数
    """


def sample_collection():
    """サンプルを採取する関数
    """


def parse_cmd(cmd: str):
    """受信したコマンドをもとに処理をする関数

    グローバル変数にモードとかを書き込むことを想定

    Args:
        cmd (str): 受信したコマンド
    """
    global mode
    mode = Mode.MANUAL
    if mode is Mode.AUTO:
        if cmd == "manual":
            mode = Mode.MANUAL
            return
    else:
        manual_mode(cmd)


def main():
    """メインアルゴリズム
    """
    # 受信を開始
    proc = Process(target=xbee.start, args=(parse_cmd,))
    proc.start()

    main_logger = Logger("Running" + datetime.datetime.now().strftime(logging.DATETIME_F))
    xbee.send_msg("走行開始")

    while not FallJudgement():
        time.sleep(0.1)

    xbee.send_msg("落下検知")

    while not LandingJudgement():
        time.sleep(0.1)

    xbee.send_msg("着地")

    detach_parachute(main_logger)

    go_to_sample = True
    while True:
        # 1行動ごとにループを回す
        if mode is Mode.AUTO:
            lat = SAMPLE_LAT if go_to_sample else GOAL_LAT
            lon = SAMPLE_LON if go_to_sample else GOAL_LON

            if is_straight(lat, lon):
                dcmotor.Wheels.forward()  # 方位角が範囲に収まっていれば3秒直進
                time.sleep(3)
                dcmotor.Wheels.stop()
            else:
                angle_adjustment()  # 収まっていなければ調整

            if is_goal() and go_to_sample:
                xbee.send_msg("サンプル地点到達")
                sample_collection()
                soil_moisture()
                go_to_sample = False
            elif is_goal() and not go_to_sample:
                xbee.send_msg("ゴール到達")
                xbee.send_msg("動作終了")
                break
        elif mode is Mode.MANUAL:
            manual_mode()


if __name__ == "__main__":
    main()  # 実行
