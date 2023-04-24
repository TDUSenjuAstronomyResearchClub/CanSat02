"""土壌水分量測定モジュール

土壌水分センサを使って土壌水分率を取得するモジュール

使用しているライブラリ:
    Adafruit-Blinka
    adafruit-circuitpython-seesaw
"""
from time import sleep
import board
import busio
from adafruit_seesaw.seesaw import Seesaw


class SoilMoistureSensor:
    """土壌水分センサ(Adafruit STEMMA Soil Sensor - I2C CapacitiveMoisture Sensor)を扱うクラス

    製品ページ: https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor
    """
    def __init__(self):
        i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.seesaw = Seesaw(i2c_bus, addr=0x36)

    def get_soil_moisture(self) -> float:
        """土壌水分率(%)を取得します

        Returns:
            float: 0.0から100.0の間の土壌水分率(%)
        """
        moisture = self.seesaw.moisture_read()
        sleep(0.1)  # センサが安定するまで 100 ms 待つ
        return 100 - ((moisture / 65535.0) * 100)

