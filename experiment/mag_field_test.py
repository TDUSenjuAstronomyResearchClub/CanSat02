"""地磁気センサの楕円体のフィッティングと中心座標の導出をするためのテストモジュール
作成されたログファイルを使い地磁気センサのバイアス値を補正する
"""
import sys

from cansatapi.nineaxissensor import NineAxisSensor
import csv
import datetime
import time

# ログ用ファイルを作成
dt_start = datetime.datetime.now()  # 現在日時を取得する
filename = 'magnetic_field' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒')  # ファイル名を現在時刻にする
log_path = "./log/" + filename + ".csv"
file = open(log_path, 'a')
writer = csv.writer(file, lineterminator='\n')

# CSVにインデックスをつける
writer.writerow(['現在日時', 'x軸', 'y軸', 'z軸'])
file.close()

try:
    while True:
        # 9軸センサの地磁気値を読み取る
        nineaxissensor = NineAxisSensor()
        mag_data = nineaxissensor.get_magnetic_field_data()

        # 地磁気値をcsvファイルに書き込む
        file = open(log_path, 'a')
        writer = csv.writer(file, lineterminator='\n')
        dt_now = time.time()  # UNIX形式で現在日時を取得する
        log_list = [dt_now, mag_data[0], mag_data[1], mag_data[2]]  # リストに各値を挿入

        writer.writerow(log_list)
        file.close()
        time.sleep(0.1)
except KeyboardInterrupt:
    sys.exit(0)


