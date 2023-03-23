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

    bool
        OSErrorが発生した場合はTrueを返す。
    """
    try:
        moisture = ss.moisture_read()
        sleep(0.1)  # Wait for 100 ms to allow the sensor to stabilize.
        return (100 - ((moisture / 65535.0) * 100))
    
    except OSError:
        return True


# Generate API documentation using pdoc.
pdoc.pdoc(get_soil_moisture)
