"""電流センサの動作確認用モジュール"""
import sys
import time
from cansatapi import ina219

if __name__ == 'main':
    while True:
        try:
            print(f"バッテリー電圧{ina219.get_voltage()}[V]")
            time.sleep(1)

        except KeyboardInterrupt:
            sys.exit(0)
