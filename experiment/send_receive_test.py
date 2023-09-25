"""地上局のテストモジュール
    地上局にセンサーの値を送り、地上局からのデータを受け取る
"""
import queue
from multiprocessing import Process

from cansatapi.xbee import *
from cansatapi import *

import sys

if __name__ == "__main__":

    parse_proc = Process(target=xbee.start)
    parse_proc.start()

    while True:
        try:
            receive_val = get_received_str()  # 地上局から受信した値を格納する
            print(receive_val)
            time.sleep(1)

        except queue.Empty:  # 地上局から受信した値がなければpass
            # print("debug comment:send message")
            send_msg("test_message")    # 地上局にメッセージを機体から送信
            time.sleep(3)   # センサーデータを送信する時間を作るため

            soilmois = soil_moisture.get_soil_moisture()    # 土壌水分値を取得
            send_soilmois_data(soilmois)    # 土壌水分値を地上局に送信
            time.sleep(3)   # センサーデータを送信する時間を作るため
            pass

        except KeyboardInterrupt:
            sys.exit(0)
