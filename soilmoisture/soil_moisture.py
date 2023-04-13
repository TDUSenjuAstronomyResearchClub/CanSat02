"""
Module Name:<br> 
土壌水分量測定プログラム<br><br>
Description:<br> 
土壌水分センサを使って土壌水分率を取得できるプログラム<br><br>
Library:<br>
board<br>
pip install board<br><br>
busio<br>
pip install adafruit-blinka<br><br>
Seesaw<br>
pip install adafruit-circuitpython-seesaw<br><br>

"""
from time import sleep
import board
import busio
from adafruit_seesaw.seesaw import Seesaw
import pdoc


i2c_bus = busio.I2C(board.SCL, board.SDA)
ss = Seesaw(i2c_bus, addr=0x36)


def get_soil_moisture():
    """
    土壌水分センサ（Adafruit STEMMA Soil Sensor - I2C CapacitiveMoisture Sensor）から土壌水分率を取得します。

    Returns
    -------
    float
        0から100の間のfloat値としての土壌水分率

    OSError
        OSErrorが発生した場合はエラー文を返す。
    """
    try:
        moisture = ss.moisture_read()
        sleep(0.1)  # センサが安定するまで 100 ms 待つ
        return 100 - ((moisture / 65535.0) * 100)
    
    except OSError as e:
        return e


# Generate API documentation using pdoc.
pdoc.pdoc(get_soil_moisture)
