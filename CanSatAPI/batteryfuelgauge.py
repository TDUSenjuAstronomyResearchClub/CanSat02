"""電池残量計を使ってバッテリーガスゲージから電池残量を取得するモジュール.

使用するにはI2Cが有効になっている必要があります

使用しているライブラリ:
    smbus2
"""

import smbus2

# 定数
DEVICE_ADDRESS = 0x36  # I2Cデバイスのアドレス
COMMAND = 0xB4  # 電池残量を測定するコマンド


class BatteryFuelGauge:
    """電池残量計(SKU 8806)を扱うクラス

    データシート: https://cdn.sparkfun.com/datasheets/Prototyping/MAX17043-MAX17044.pdf
    """

    def __init__(self):
        self.bus = smbus2.SMBus(1)

    def get_level(self) -> int:
        """電池残量(%)を取得するメソッド

        Returns:
            int: 電池残量(%)を返却する（0-100の範囲で表される整数）

        Raises:
            OSError: I2C通信が正常に行えなかった際に発生
        """
        # 電池残量を測定するコマンドを送信
        self.bus.write_byte_data(DEVICE_ADDRESS, 0x00, COMMAND)
        # 電池残量を取得
        return self.bus.read_byte_data(DEVICE_ADDRESS, 0x00)
