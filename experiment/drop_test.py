"""投下試験用のテストモジュール
"""
import time
import datetime
import math

from cansatapi.nineaxissensor import NineAxisSensor
from cansatapi.servo import Servo
from cansatapi import dcmotor
from cansatapi.util.logging import LoggerCSV
from cansatapi.util import logging

from cansatapi import *


def detach_parachute(logger: LoggerCSV):
    """パラシュートの切り離しを行います
    """
    logger.msg_csv("パラシュート切り離し開始")
    para_servo = Servo(servo.PARA_PIN)
    para_servo.rotate_cw()
    time.sleep(10)
    para_servo.rotate_stop()

    # 機体を前進させる
    dcmotor.Wheels.stop()
    logger.msg_csv("機体を20秒前進させる")
    dcmotor.Wheels.forward()
    time.sleep(20)
    dcmotor.Wheels.stop()
    dcmotor.Wheels.cleanup()
    logger.msg_csv("パラシュート切り離し終了")


if __name__ == "__main__":
    # ログ用ファイルの作成
    dt_start = datetime.datetime.now()  # 現在日時を取得する
    filename = 'drop_test' + dt_start.strftime(logging.FILE_NAME_FMT)  # ファイル名を現在時刻にする
    LOGGER = LoggerCSV(filename)

    LOGGER.msg_csv("初期化開始")
    nine_axis = NineAxisSensor()
    LOGGER.msg_csv("初期化完了")

    # 落下開始判定
    LOGGER.msg_csv("落下待機中")

    accel_abs_past = 0  # accel_abs_pastを初期化
    try:
        accel = nine_axis.get_acceleration()
        accel_abs_past = math.sqrt(accel[0] ** 2 + accel[1] ** 2 + accel[2] ** 2)  # 9軸から加速度の大きさを求める
        LOGGER.log_csv("加速度", accel_abs_past)  # ログを残す
    except OSError:
        LOGGER.error_csv("9軸センサでOSError")
    accel_abs = 0.0

    drop_start_s = time.time()  # 落下後経過時間を初期化
    drop_count = 0
    landing_count = 0

    while True:
        try:
            accel = nine_axis.get_acceleration()
            accel_abs = math.sqrt(accel[0] ** 2 + accel[1] ** 2 + accel[2] ** 2)  # 9軸から加速度の大きさを求める
            LOGGER.log_csv("加速度", accel_abs)  # ログを残す
        except OSError:
            LOGGER.error_csv("9軸センサでOSError")

        # todo: 落下開始判定を行う加速度の差の閾値を書き込む
        # 5回連続で加速度の差が0 m/s^2以上だったら落下開始判定とする
        if accel_abs - accel_abs_past > 0:
            drop_count += 1
            if drop_count >= 5:
                drop_start_s = time.time()
                LOGGER.msg_csv("落下開始判定が行われました")
                break
        else:
            drop_count = 0

        accel_abs_past = accel_abs

        time.sleep(0.1)

    # 着地判定
    while True:
        try:
            accel = nine_axis.get_acceleration()
            accel_abs = math.sqrt(accel[0] ** 2 + accel[1] ** 2 + accel[2] ** 2)  # 9軸から加速度の大きさを求める
            LOGGER.log_csv("加速度", accel_abs)  # ログを残す
        except OSError:
            LOGGER.error_csv("9軸センサでOSError")

        # todo: 着地判定の高度と加速度の閾値を書き込む
        # 5回連続で加速度が閾値よりも小さかったら着地判定とする
        if accel_abs < 1.406:
            landing_count += 1
            if landing_count >= 5:
                LOGGER.msg_csv("着地判定が行われました")
                break
        else:
            landing_count = 0

        # 降下開始から2分経過で強制的に着地判定とする
        if drop_start_s + 120 < time.time():
            LOGGER.msg_csv("時間経過で強制的に着地判定が行われました")
            break

        time.sleep(0.1)

    detach_parachute(LOGGER)
