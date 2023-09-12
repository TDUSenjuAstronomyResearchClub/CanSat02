"""地上局のテストモジュール
    地上局にセンサーの値を送り、地上局からのデータを受け取る
"""
from cansatapi import xbee
from multiprocessing import Process
from cansatapi.xbee import *

import sys

if __name__ == "__main__":
    try:
        parse_proc = Process(target=xbee.start)
        parse_proc.start()

        receive_val = get_received_str()
        if receive_val != 'Null':
            print(get_received_str())

    except KeyboardInterrupt:
        sys.exit(0)
