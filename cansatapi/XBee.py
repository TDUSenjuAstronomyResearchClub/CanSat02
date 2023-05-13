"""機体と地上局の通信を行うモジュール
"""

from datetime import datetime
import json
import time

import serial
from serial import SerialException
from serial import PortNotOpenError

# ポート設定
PORT = '/dev/ttyUSB0'
# 通信レート設定
BAUD_RATE = 9600


def send(json_data: str):
    """データ送信用関数

    Args:
        json_data (str): JSON形式のデータ

    Raises:
        PortNotOpenError: ポートが空いておらず、リトライにも失敗した場合発生します
        SerialException: デバイスがみつからないときに発生します
    """
    # ログ用ファイルをオープン
    f = open('send_data' + datetime.now().strftime('%Y年%m月%d日_%H時%M分%S秒') + '.json', 'a')
    # jsonとして書き込み
    json.dump(json_data, f, indent=4, ensure_ascii=False)
    f.close()

    retry_c = 0
    while True:
        try:
            ser = serial.Serial(PORT, BAUD_RATE)
            # シリアルにjsonを書き込む
            ser.write(json_data.encode('utf-8'))
            ser.close()
            return

        except PortNotOpenError:
            # 5回リトライに失敗したらエラーを吐く
            retry_c += 1
            if retry_c > 5:
                raise PortNotOpenError
            else:
                time.sleep(0.5)
                continue
        except SerialException:
            raise SerialException  # ここの処理について要件等


def receive() -> str:
    """データ受信用関数

    Returns:
        str: 受信した文字列

    Raises:
        SerialException: デバイスがみつからないときに発生します
        PortNotOpenError: ポートが空いておらず、リトライにも失敗した場合発生します
    """
    retry_c = 0
    while True:
        try:
            ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
            receive_data = ser.read_all()  # 機体から値を受け取る
            ser.close()

            catch_value = {
                "time": datetime.now(),
                "message": receive_data
            }
            # ログ用ファイルをオープン
            f = open('receive_data' + datetime.now().strftime('%Y年%m月%d日_%H時%M分%S秒') + '.json', 'a')
            # jsonとして書き込み
            json.dump(catch_value, f, indent=4, ensure_ascii=False)
            f.close()
            return receive_data

        except PortNotOpenError:
            # 5回リトライに失敗したらエラーを吐く
            retry_c += 1
            if retry_c > 5:
                raise PortNotOpenError
            else:
                time.sleep(0.5)
                continue
        except SerialException:  # デバイスが見つからない、または構成できない場合
            raise SerialException