"""2023/5/6の投下試験用のテストモジュール
"""
import csv
import sys
import time
import datetime
import math

from cansatapi.barometer import Barometer
from cansatapi.barometer import calc_altitude
from cansatapi.nineaxissensor import NineAxisSensor


class Logger:
    """ロガークラス

    CSV形式でロギングを行います。
    """

    def __init__(self, file_name: str):
        """ロガーのコンストラクタ

        CSV形式でロギングを行います。

        Args:
            file_name: ログファイルの名前
        """
        self.file = open(file_name, 'a')
        self.writer = csv.writer(self.file, lineterminator='\n')

        # CSVにインデックスをつける
        self.writer.writerow(['現在日時', '説明', '内容'])
        self.file.close()

    def log(self, description: str, content: str | float):
        """ロギング用のプライベートメソッド

        Args:
            description (str): ログの説明文
            content (str): ログメッセージ
        """
        self.file = open(self.file.name, 'a')
        dt_now = datetime.datetime.now()  # 現在日時を取得する
        log_list = [dt_now, description, content]  # リストに各値を挿入

        self.writer.writerow(log_list)
        self.file.close()
        time.sleep(0.1)

    def msg(self, msg: str):
        """メッセージロギング用メソッド

        Args:
            msg (str): メッセージ
        """
        self.log("[LOG]", msg)
        print(msg, file=sys.stdout)

    def error(self, msg: str):
        """エラーロギング用のメソッド

        Args:
            msg (str): エラーメッセージ
        """
        self.log("[ERROR]", msg)
        print(msg, file=sys.stderr)


if __name__ == "__main__":
    barometer = Barometer()
    nine_axis = NineAxisSensor()

    # ログ用ファイルの作成
    dt_start = datetime.datetime.now()  # 現在日時を取得する
    filename = 'driving' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒') + '.csv'  # ファイル名を現在時刻にする
    logger = Logger(filename)

    # 落下開始判定
    altitude_past = -1  # 高度比較用に使用する過去の高度値を初期化する
    altitude_now = 0
    while True:

        try:
            altitude_now = calc_altitude(barometer.get_pressure())
            logger.log("[高度]", altitude_now)  # ログを残す
        except OSError:
            logger.error("気圧センサーでOSError")

        if altitude_past > altitude_now:
            logger.msg("落下判定が行われました")
            break

        altitude_past = altitude_now

        time.sleep(0.5)

    # 着地判定
    altitude = 0
    accel_abs = 0
    while True:

        try:
            altitude = calc_altitude(barometer.get_pressure())
            logger.log("[高度]", altitude)  # ログを残す
        except OSError:
            logger.error("気圧センサでOSError")

        try:
            accel = nine_axis.get_acceleration()
            accel_abs = math.sqrt(accel[0] ** 2 + accel[1] ** 2 + accel[2] ** 2)  # 9軸から加速度の大きさを求める
            logger.log("[加速度]", accel_abs)  # ログを残す
        except OSError:
            logger.error("9軸センサでOSError")

        # 高度と加速度の着地判定の基準値を書き込む
        if altitude < 0 or accel_abs < 0:
            logger.msg("着地判定が行われました")
            break

        time.sleep(0.5)

# DCモータでパラシュートを分離させる
# プログラム作成の必要あり
