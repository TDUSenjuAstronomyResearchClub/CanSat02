"""気圧・高度・気温取得モジュール

気圧センサ(AE-LPS25HB)を使って気圧、高度、気温を取得できるモジュール

使用しているライブラリ:
    smbus2
"""

import smbus2

# 気圧センサ(LPS25HB)のための定数を定義
LPS25HB_ADDRESS = 0x5C
CTRL_REG1 = 0x20
CMD_REG = 0x80
RES_CONF = 0x10
PRESS_OUT_XL = 0x28
PRESS_OUT_L = 0x29
PRESS_OUT_H = 0x2A
TEMP_OUT_L = 0x2B
TEMP_OUT_H = 0x2C


def byte_pressure_to_hpa(raw_byte: list) -> float:
    """生の気圧データをhPaに変換する関数

    Parameters:
        raw_byte (list):　LPS25HBから読み取った生の気圧データ

    Returns:
        float: 気圧(hpa)
    """
    # 参考: https://github.com/ControlEverythingCommunity/LPS25HB/blob/master/Python/LPS25HB.py
    return ((raw_byte[2] << 16) | (raw_byte[1] << 8) | raw_byte[0]) / 4096.0


def byte_temp_to_deg_c(raw_byte: list) -> float:
    """生の温度データを℃に変換する関数

    Args:
        raw_byte (list):　LPS25HBから読み取った生のデータ

    Returns:
        float: 温度(℃)
    """
    # 参考: https://garretlab.web.fc2.com/arduino/lab/barometer_and_temperature_sensor/
    return (raw_byte[1] << 8) | raw_byte[0] / 480 + 42.5


def calc_altitude(pressure: float, sea_level_pressure: float = 1013.25) -> float:
    """気圧[hPa]から高度[m]を計算する関数

    海面気圧に基づいて高度を計算するので低気圧接近時などにズレが生じます。
    絶対値として使うのではなく、相対値として(差分を計算して)使用してください。

    Args:
        pressure (float): 気圧[hPa]
        sea_level_pressure (float): 海面気圧[hPa]

    Returns:
        float: 計算された高度[m]
    """
    return 44330.0 * (1.0 - pow(pressure / sea_level_pressure, 0.1903))


class LPS25HB:
    """気圧センサ (AE-LPS25HB)を扱うクラス

    データシート: https://www.st.com/resource/en/datasheet/lps25hb.pdf
    """

    def __init__(self):
        """気圧センサ (AE-LPS25HB)を初期化する
        """
        # I2Cバスを初期化
        self.bus = smbus2.SMBus(1)
        # 気圧センサを設定
        self.bus.write_byte_data(LPS25HB_ADDRESS, CTRL_REG1, 0xC4)
        self.bus.write_byte_data(LPS25HB_ADDRESS, RES_CONF, 0x00)

    def get_pressure(self) -> float:
        """気圧を読み取るメソッド

        Returns:
            float: 気圧[hPa]
        """
        # PRESS_OUT_XL(0x28)からPRESS_OUT_H(0x2A)までの3つを読み取る
        # 参考: https://github.com/ControlEverythingCommunity/LPS25HB/blob/master/Python/LPS25HB.py
        press_out = self.bus.read_i2c_block_data(LPS25HB_ADDRESS, PRESS_OUT_XL | CMD_REG, 3)
        return byte_pressure_to_hpa(press_out)

    def get_temperature(self) -> float:
        """内蔵の温度計から温度を読み取るメソッド

        LPS25HBの内蔵温度計の公差は±2℃です。
        また、有効範囲は0℃から+65℃です。
        内蔵なので温度が気温よりすこし高めに出る傾向があります。

        Returns:
            float: 温度[℃]
        """
        temp_out = self.bus.read_i2c_block_data(LPS25HB_ADDRESS, TEMP_OUT_L | CMD_REG, 2)
        return byte_temp_to_deg_c(temp_out)

    def get_pressure_altitude_temperature(self) -> list[float]:
        """気圧・高度・気温を読み取るメソッド

        Deprecated:
            後方互換性のために残しています。

        Returns:
            list[float]: 現在の気圧[hPa], 現在の高度[m], 現在の気温[℃], をこの順番で要素とするリスト
        """
        # 生の気圧と気温データをセンサーから読み取る
        press_out_xl = self.bus.read_byte_data(LPS25HB_ADDRESS, PRESS_OUT_XL)
        press_out_l = self.bus.read_byte_data(LPS25HB_ADDRESS, PRESS_OUT_L)
        press_out_h = self.bus.read_byte_data(LPS25HB_ADDRESS, PRESS_OUT_H)
        temp_out_l = self.bus.read_byte_data(LPS25HB_ADDRESS, TEMP_OUT_L)
        temp_out_h = self.bus.read_byte_data(LPS25HB_ADDRESS, TEMP_OUT_H)

        # 生のデータを気圧(hPa) 気温(deg C)に変換
        raw_pressure = (press_out_h << 16) | (press_out_l << 8) | press_out_xl
        raw_pressure = raw_pressure >> 4
        pressure = raw_pressure / 4096.0

        raw_temperature = (temp_out_h << 8) | temp_out_l
        temperature = raw_temperature / 480.0 + 42.5

        # 気圧に基づいた高度を計算
        sea_level_pressure = 1013.25  # hPa
        altitude = 44330.0 * (1.0 - pow(pressure / sea_level_pressure, 0.1903))

        # 小数点以下2桁に数値を丸める
        pressure = round(pressure, 2)
        altitude = round(altitude, 2)
        temperature = round(temperature, 2)

        # リストにして返す
        return [pressure, altitude, temperature]
