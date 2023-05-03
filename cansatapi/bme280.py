"""温湿度気圧センサモジュール

温湿度気圧センサを使って温度、湿度、気圧の値を取得できるモジュール

使用するにはI2Cが有効になっている必要があります

使用しているライブラリ:
    bme280
"""

from bme280 import bme280, bme280_i2c

BUS_NUMBER = 1
I2C_ADDRESS = 0x76


class BME280:

    def __init__(self):

        bme280_i2c.set_default_i2c_address(I2C_ADDRESS)
        bme280_i2c.set_default_bus(BUS_NUMBER)
        bme280.setup()

    def temperature_result(self) -> list:
        """温湿度気圧センサ(AE-BME280)を使って温度、湿度、気圧の値を返却します

        Deprecated:
            後方互換性のために残しています

        Returns:
            list: [温度[℃], 湿度[%], 気圧[hPa]]
        """
        return [bme280.read_temperature(), bme280.read_humidity(), bme280.read_pressure()]

    def get_temperature(self) -> float:
        """温度[℃]を取得します

        Returns:
            float: 温度[℃]
        """
        return bme280.read_temperature()

    def get_humidity(self) -> float:
        """湿度[%]を取得します

        Returns:
            float: 湿度[%]
        """
        return bme280.read_humidity()

    def get_pressure(self) -> float:
        """気圧[hPa]を取得します

        Returns:
            float: 気圧[hPa]
        """
        return bme280.read_pressure()
