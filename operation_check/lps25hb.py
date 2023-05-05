"""LPS25HBの動作確認用モジュール
"""
import sys
import time

from cansatapi.lps25hb import LPS25HB
from cansatapi.lps25hb import calc_altitude

if __name__ == "__main__":
    lps25hb = LPS25HB()

    while True:
        try:
            print(f"気圧: {lps25hb.get_pressure()}")
            print(f"温度: {lps25hb.get_temperature()}")
            print(f"高度: {calc_altitude(lps25hb.get_pressure())}")
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)
