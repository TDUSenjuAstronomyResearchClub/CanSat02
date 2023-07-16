"""土壌水分量測定モジュール

土壌水分センサを使って土壌水分率を取得するモジュール

使用しているライブラリ:
    Adafruit-Blinka
    adafruit-circuitpython-seesaw
"""
from adafruit_blinka.board.raspberrypi.raspi_40pin import *
import busio
from adafruit_seesaw.seesaw import Seesaw


class SoilMoistureSensor:
    """土壌水分センサ(Adafruit STEMMA Soil Sensor - I2C CapacitiveMoisture Sensor)を扱うクラス

    製品ページ: https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor
    """
    def __init__(self):
        i2c_bus = busio.I2C(SCL, SDA)
        self.seesaw = Seesaw(i2c_bus, addr=0x36)

    def get_soil_moisture(self) -> float:
        """土壌水分量を取得します

        200(非常に乾いた状態)から2000(非常に湿った状態)までの値を取得できます

        Returns:
            float: 土壌水分量
        """
        return self.seesaw.moisture_read()
