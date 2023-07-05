"""電圧測定モジュール

使用するにはI2Cが有効になっている必要があります

使用しているライブラリ:
    board
    adafruit_circuitpython_ina219
"""

import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

i2c_bus = board.I2C()  # INA219 が接続されている I2C バス。
ina219 = INA219(i2c_bus, 0x41)  # バス上の INA219 のアドレス（0x40）

# バス電圧とシャント電圧の両方に 32 サンプルの平均化を使用するように構成を変更
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
# 電圧範囲を 16V に変更
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V


def get_voltage() -> float:
    """電圧を取得する関数

    Returns:
        float :バッテリーのシャント電圧

    """

    return ina219.shunt_voltage
