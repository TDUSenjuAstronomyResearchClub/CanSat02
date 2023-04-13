"""電池残量計を使ってバッテリーガスゲージから電池残量を取得するモジュール.

使用するにはI2Cが有効になっている必要があります

使用しているライブラリ:
    smbus2
"""

import smbus2

# 定数
DEVICE_ADDRESS = 0x36  # I2Cデバイスのアドレス
COMMAND = 0xB4  # 電池残量を測定するコマンド

# バスを初期化
bus = smbus2.SMBus(1)


# 電池残量を取得する関数
def get_battery_level():
    """電池残量計(SKU 8806)を使って電池残量を取得するプログラム

    Returns:
        int: 電池残量を返却する（0-100の範囲で表される整数）

    Raises:
        OSError: I2C通信が正常に行えなかった際に発生
    """
    # 電池残量を測定するコマンドを送信
    bus.write_byte_data(DEVICE_ADDRESS, 0x00, COMMAND)
    # 電池残量を取得
    level = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
    return level
