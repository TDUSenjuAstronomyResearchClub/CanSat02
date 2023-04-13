"""
Module Name:<br> 
battery<br><br>
Description:<br> 
電池残量計を使ってバッテリーガスゲージから電池残量を取得するプログラム。<br><br>
Library:<br>
smbus<br>
「sudo apt-get install python3-smbus2」を実行し、smbusをインストールする必要があります。<br>
また、sudo raspi-configから、Interface Optionを選択し、I2Cから、「はい」または「Yes」をEnterで確定して、I2C通信を有効にする必要があります。<br>
※確定後の再起動は必要ありません。<br><br>
"""

import smbus2

# 定数
DEVICE_ADDRESS = 0x36  # I2Cデバイスのアドレス
COMMAND = 0xB4  # 電池残量を測定するコマンド

# バスを初期化
bus = smbus2.SMBus(1)


# 電池残量を取得する関数
def get_battery_level():
    """
    電池残量計(SKU 8806)を使って電池残量を取得するプログラム。

    Returns
    -------
    int
            int型で電池残量を返却する（0-100の範囲で表される整数）
    bool
            OSErrorが発生した場合はTrueを返す。
    """
    try:
        # 電池残量を測定するコマンドを送信
        bus.write_byte_data(DEVICE_ADDRESS, 0x00, COMMAND)
        # 電池残量を取得
        level = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
        return level
    except OSError:
        return True  # OSErrorが発生したか否かを判断する（Trueが出たらエラーが発生した判定）


# テスト用の関数呼び出し
print(get_battery_level())
