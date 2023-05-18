import datetime
import time

from cansatapi import *
from cansatapi.util import logging
from cansatapi.util.logging import Logger

# 本番前に記入
SAMPLE_LON: float = 0.0
SAMPLE_LAT: float = 0.0

GOAL_LON: float = 0.0
GOAL_LAT: float = 0.0


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
    main_logger = Logger("Running" + datetime.datetime.now().strftime(logging.DATETIME_F))
    XBee.send_msg("Start running")

    FallJudgement()
    XBee.send_msg("Detect falling")

    LandingJudgement()
    XBee.send_msg("Landed")

    detach_parachute(main_logger)


if __name__ == "__main__":
    main()  # 実行
