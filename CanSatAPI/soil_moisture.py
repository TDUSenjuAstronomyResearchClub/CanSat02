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


i2c_bus = busio.I2C(board.SCL, board.SDA)
ss = Seesaw(i2c_bus, addr=0x36)


def get_soil_moisture() -> float:
    """土壌水分センサ（Adafruit STEMMA Soil Sensor - I2C CapacitiveMoisture Sensor）から土壌水分率を取得します

    Returns:
        float: 0.0から100.0の間の土壌水分率

    Raises:
        OSError: I2C通信が正常に行えなかった際に発生
    """
    try:
        moisture = ss.moisture_read()
        sleep(0.1)  # センサが安定するまで 100 ms 待つ
        return 100 - ((moisture / 65535.0) * 100)
    
    except OSError:
        raise OSError
