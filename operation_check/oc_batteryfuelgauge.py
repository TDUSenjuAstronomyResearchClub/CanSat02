"""電流センサの動作確認用モジュール"""
import sys
import time
from cansatapi import batteryfuelgauge

if __name__ == 'main':
    while True:
        try:
            print(f"バッテリー電圧{batteryfuelgauge.get_level()}[%]")
            time.sleep(1)

        except KeyboardInterrupt:
            sys.exit(0)
