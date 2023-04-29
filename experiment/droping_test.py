import csv
import time
import datetime
import math

from cansatapi.barometer import Barometer
from cansatapi.nineaxissensor import NineAxisSensor

barometer = Barometer()
nine_axis = NineAxisSensor()


# ===logを残す関数　引数：log_type(この値が何の意味を持つのかの説明),value(変数値)　戻り値：なし===
def log(filename, log_type, value) -> None:
    dat_now = datetime.datetime.now()  # 現在日時を取得する
    explanation = log_type
    variable = value
    writer = csv.writer(f, lineterminator='\n')
    log_list = [dat_now, explanation, variable]  # リストに各値を挿入

    f = open(filename, 'a')
    writer.writerow(log_list)
    print(log_list)
    f.close()
    time.sleep(0.1)
    return


# ===ログ用ファイルの作成===
dt_start = datetime.datetime.now()  # 現在日時を取得する
filename = 'driving' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒') + '.csv'  # ファイル名を現在時刻にする

f = open(filename, 'a')
writer = csv.writer(f, lineterminator='\n')
index = ['Time of Day', 'Log type value', 'value']  # 表のインデックスを付ける
writer.writerow(index)
f.close()

# ===落下開始判定===
hight_past = -1  # 高度比較用に使用する過去の高度値を初期化する

while True:

    try:
        hight_temp = barometer.get_pressure_altitude_temperature()
        hight_now = hight_temp[0]  # 現在の高度を求める
        log(filename, "高度", hight_now)  # ログを残す
    except OSError:
        log("気圧センサOSエラー", None)

    if hight_past > hight_now:
        log(filename, "落下判定が行われました", None)
        break

    hight_past = hight_now

    time.sleep(0.5)

# ===着地判定===
while True:

    try:
        hight = barometer.get_pressure_altitude_temperature()
        log(filename, "高度", hight[0])  # ログを残す
    except OSError:
        log("気圧センサOSエラー", None)

    try:
        accel_tmp = nine_axis.get_acceleration()
        accel = math.sqrt(accel_tmp[0] ^ 2 + accel_tmp[1] ^ 2 + accel_tmp[2] ^ 2)  # 9軸から加速度の大きさを求める
        log(filename, "加速度の大きさ", accel)  # ログを残す
    except OSError:
        log("9軸センサOSエラー", None)

    # ===高度と加速度の着地判定の基準値を書き込む===
    if hight[0] < 0 or accel < 0:
        log(filename, "着地判定が行われました", None)
        break

    time.sleep(0.5)

# ===DCモータでパラシュートを分離させる===
# プログラム作成の必要あり
