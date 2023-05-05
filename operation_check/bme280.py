"""BME280の動作確認用モジュール
"""
import sys
import time

from cansatapi.bme280 import BME280

if __name__ == "__main__":
    temp = BME280()
    while True:
        try:
            print(f"温度: {temp.get_temperature()}")
            print(f"湿度: {temp.get_humidity()}")
            print(f"気圧: {temp.get_pressure()}")
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)

