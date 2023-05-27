"""超音波距離センサの動作確認用モジュール"""
import sys
import time

from cansatapi import distance

if __name__ == "__main__":
    while True:
        try:
            print(f"距離: {distance.distance_result()}[cm]")
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)
