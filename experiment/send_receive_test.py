"""地上局のテストモジュール
    地上局にセンサーの値を送り、地上局からのデータを受け取る
"""
from cansatapi import xbee
from multiprocessing import Process
from cansatapi.xbee import *
from cansatapi.util import logging

import datetime
import sys

if __name__ == "__main__":
    # ログ用ファイルの作成
    dt_start = datetime.datetime.now()  # 現在日時を取得する
    filename = 'send_data' + dt_start.strftime(logging.FILE_NAME_FMT)  # ファイル名を現在時刻にする
    LoggerJSON(filename)

    parse_proc = Process(target=xbee.start)
    parse_proc.start()

    while True:
        try:
            receive_val = get_received_str()  # 地上局から受信した値を格納する
            print(get_received_str())
            time.sleep(1)

        except queue.Empty:  # 地上局から受信した値がなければpass
            print("地上局から値を受信してない")
            pass

        except KeyboardInterrupt:
            sys.exit(0)
