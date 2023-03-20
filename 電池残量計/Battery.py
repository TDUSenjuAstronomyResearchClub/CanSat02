"""
Module Name:<br> 
電池残量計<br><br>
Description:<br> 
電池残量計を使って温度、湿度、気圧の値を取得できるプログラム。<br><br>
Library:<br>
smbus<br>
「sudo apt-get install python3-smbus」を実行し、smbusをインストールする必要があります。<br>
また、sudo raspi-configから、Interface Optionを選択し、I2Cから、「はい」または「Yes」をEnterで確定して、I2C通信を有効にする必要があります。<br>
※確定後の再起動は必要ありません。<br><br>
"""

import smbus

# 定数
DEVICE_ADDRESS = 0x36 # I2Cデバイスのアドレス
COMMAND = 0xB4 # 電池残量を測定するコマンド

# バスを初期化
bus = smbus.SMBus(1)

# 電池残量を取得する関数
def get_battery_level():
    # 電池残量を測定するコマンドを送信
    bus.write_byte_data(DEVICE_ADDRESS, 0x00, COMMAND)
    # 電池残量を取得
    level = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
    return level

# テスト用の関数呼び出し
print(get_battery_level())
