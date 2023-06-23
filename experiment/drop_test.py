"""投下試験用のテストモジュール
"""
import time
import datetime
import math

from cansatapi.lps25hb import LPS25HB
from cansatapi.lps25hb import calc_altitude
from cansatapi.nineaxissensor import NineAxisSensor
from cansatapi.dcmotor import DCMotor
from cansatapi.util.logging import Logger


def detach_parachute(logger: Logger):
    """パラシュートの切り離しを行います
    """
    para_motor = DCMotor(9, 10)
    logger.msg("パラシュート切り離し開始")
    para_motor.forward()

    time.sleep(10)  # 10秒間巻取り

    para_motor.stop()
    para_motor.cleanup()
    logger.msg("パラシュート切り離し終了")


if __name__ == "__main__":
    # ログ用ファイルの作成
    dt_start = datetime.datetime.now()  # 現在日時を取得する
    filename = 'drop_test' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒')   # ファイル名を現在時刻にする
    LOGGER = Logger(filename)

    LOGGER.msg("初期化開始")
    barometer = LPS25HB()
    nine_axis = NineAxisSensor()
    LOGGER.msg("初期化完了")

    # 落下開始判定
    LOGGER.msg("落下待機中")

    try:
        accel = nine_axis.get_acceleration()
        accel_abs_past = math.sqrt(accel[0] ** 2 + accel[1] ** 2 + accel[2] ** 2)  # 9軸から加速度の大きさを求める
        LOGGER.log("加速度", accel_abs_past)  # ログを残す
    except OSError:
        LOGGER.error("9軸センサでOSError")
    accel_abs = 0.0 

    drop_start_s = time.time()  # 落下後経過時間を初期化
    drop_count = 0


    while True:

        try:
            accel = nine_axis.get_acceleration()
            accel_abs = math.sqrt(accel[0] ** 2 + accel[1] ** 2 + accel[2] ** 2)  # 9軸から加速度の大きさを求める
            LOGGER.log("加速度", accel_abs)  # ログを残す
        except OSError:
            LOGGER.error("9軸センサでOSError")

        # todo: 落下開始判定を行う加速度の差の閾値を書き込む
        # 5回連続で加速度の差が0 m/s^2以上だったら落下開始判定とする
        if accel_abs-accel_abs_past > 0:
            drop_count += 1
            if drop_count >= 5:
                drop_start_s = time.time()
                LOGGER.msg("落下開始判定が行われました")
                break
        else:
            drop_count = 0

        accel_abs_past = accel_abs

        time.sleep(0.5)

    # 着地判定
    pressure = 0.0
    altitude = 0.0
    while True:

        try:
            pressure = barometer.get_pressure()
            LOGGER.log("気圧", pressure)
            altitude = calc_altitude(pressure)
            LOGGER.log("高度", altitude)  # ログを残す
        except OSError:
            LOGGER.error("気圧センサでOSError")

        try:
            accel = nine_axis.get_acceleration()
            accel_abs = math.sqrt(accel[0] ** 2 + accel[1] ** 2 + accel[2] ** 2)  # 9軸から加速度の大きさを求める
            LOGGER.log("加速度", accel_abs)  # ログを残す
        except OSError:
            LOGGER.error("9軸センサでOSError")

        # todo: 着地判定の高度と加速度の閾値を書き込む
        if altitude < 0 or accel_abs < 0:
            LOGGER.msg("着地判定が行われました")
            break

        # 降下開始から2分経過で強制的に着地判定とする
        if drop_start_s + 120 < time.time():
            LOGGER.msg("時間経過で強制的に着地判定が行われました")
            break

        time.sleep(0.5)

    detach_parachute(LOGGER)

