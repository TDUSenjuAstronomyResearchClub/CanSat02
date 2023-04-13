"""
Module Name:<br> 
気圧・高度・気温取得プログラム<br><br>
Description:<br> 
気圧センサを使って気圧、高度、気温を取得できるプログラム<br><br>
Library:<br>
smbus2<br>
pip install smbus2<br><br>
"""

import smbus2
import time

# Define constants for the LPS25HB pressure sensor
LPS25HB_ADDRESS = 0x5C
LPS25HB_CTRL_REG1 = 0x20
LPS25HB_RES_CONF = 0x10
LPS25HB_PRESS_OUT_XL = 0x28
LPS25HB_PRESS_OUT_L = 0x29
LPS25HB_PRESS_OUT_H = 0x2A
LPS25HB_TEMP_OUT_L = 0x2B
LPS25HB_TEMP_OUT_H = 0x2C

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Configure the LPS25HB pressure sensor
bus.write_byte_data(LPS25HB_ADDRESS, LPS25HB_CTRL_REG1, 0xC4)
bus.write_byte_data(LPS25HB_ADDRESS, LPS25HB_RES_CONF, 0x00)

def get_pressure_altitude_temperature():
    """
    pressure（AE-LPS25HB）から気圧、高度、気温を読み取ります。

    Returns
    -------
    list
        現在の気圧（hPa）、現在の高度（m）、現在の気温（deg C）をこの順番で要素とするリストが返されます。
        処理が正常に終了した場合は、要素数3のリストが返されます。

    bool
        OSErrorが発生した場合はエラー文を返す。
    """
    try:
        # Read raw pressure and temperature data from the sensor
        press_out_xl = bus.read_byte_data(LPS25HB_ADDRESS, LPS25HB_PRESS_OUT_XL)
        press_out_l = bus.read_byte_data(LPS25HB_ADDRESS, LPS25HB_PRESS_OUT_L)
        press_out_h = bus.read_byte_data(LPS25HB_ADDRESS, LPS25HB_PRESS_OUT_H)
        temp_out_l = bus.read_byte_data(LPS25HB_ADDRESS, LPS25HB_TEMP_OUT_L)
        temp_out_h = bus.read_byte_data(LPS25HB_ADDRESS, LPS25HB_TEMP_OUT_H)

        # Convert raw data to pressure (hPa) and temperature (deg C)
        raw_pressure = (press_out_h << 16) | (press_out_l << 8) | press_out_xl
        raw_pressure = raw_pressure >> 4
        pressure = raw_pressure / 4096.0

        raw_temperature = (temp_out_h << 8) | temp_out_l
        temperature = raw_temperature / 480.0 + 42.5

        # Calculate altitude based on pressure and temperature
        sea_level_pressure = 1013.25  # hPa
        altitude = 44330.0 * (1.0 - pow(pressure / sea_level_pressure, 0.1903))

        # Round values to two decimal places
        pressure = round(pressure, 2)
        altitude = round(altitude, 2)
        temperature = round(temperature, 2)

        # Create list with results
        results = [pressure, altitude, temperature]

        return results
    except OSError as e:
        return [e,e,e]
