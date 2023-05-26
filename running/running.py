import datetime
import time
from multiprocessing import Process

from cansatapi import *
from cansatapi.util import logging
from cansatapi.util.logging import Logger

# 本番前に記入
SAMPLE_LON: float = 0.0
SAMPLE_LAT: float = 0.0

GOAL_LON: float = 0.0
GOAL_LAT: float = 0.0

# 共有変数
receive_command = ''


def manual_mode():
    """手動制御を行う関数
    """


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


def angle_adjustment():
    """目的地と機体を一直線にする関数
    """


def go_to_goal():
    """ゴールまで直進する関数
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


if __name__ == "__main__":
    main()  # 実行
