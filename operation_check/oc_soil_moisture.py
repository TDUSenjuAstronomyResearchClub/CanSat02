"""土壌水分量センサの動作確認モジュール"""

import sys
import time

from cansatapi.soil_moisture import SoilMoistureSensor

if __name__ == "__main__":
    sensor = SoilMoistureSensor()
    while True:
        try:
            print(f"{sensor.get_soil_moisture()}[%]")
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)
