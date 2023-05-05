"""2023/5/6の投下試験用のテストモジュール
"""
import time
import datetime
import math

from cansatapi.lps25hb import LPS25HB
from cansatapi.lps25hb import calc_altitude
from cansatapi.nineaxissensor import NineAxisSensor
from cansatapi.dcmotor import DCMotor
from cansatapi.util.logger import Logger


def detach_parachute(logger: Logger):
    """パラシュートの切り離しを行います
    """
    para_motor = DCMotor(9, 10)
    logger.msg("パラシュート切り離し開始")
    para_motor.forward()

    time.sleep(10)  # 10秒間巻取り

    para_motor.stop_motor()
    para_motor.cleanup()
    logger.msg("パラシュート切り離し終了")


if __name__ == "__main__":
    barometer = LPS25HB()
    nine_axis = NineAxisSensor()

    # ログ用ファイルの作成
    dt_start = datetime.datetime.now()  # 現在日時を取得する
    filename = 'driving' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒') + '.csv'  # ファイル名を現在時刻にする
    LOGGER = Logger(filename)

    # 落下開始判定
    altitude_past = -1  # 高度比較用に使用する過去の高度値を初期化する
    altitude_now = 0
    drop_start = time.time()
    while True:

        try:
            altitude_now = calc_altitude(barometer.get_pressure())
            LOGGER.log("高度", altitude_now)  # ログを残す
        except OSError:
            LOGGER.error("気圧センサーでOSError")

        if altitude_past > altitude_now:
            LOGGER.msg("落下判定が行われました")
            break

        altitude_past = altitude_now

        time.sleep(0.5)

    # 着地判定
    pressure = 0.0
    altitude = 0.0
    accel_abs = 0.0
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
        if drop_start + 120 < time.time():
            LOGGER.msg("時間経過で強制的に着地判定が行われました")
            break

        time.sleep(0.5)

    detach_parachute(LOGGER)
