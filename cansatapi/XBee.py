"""機体と地上局の通信を行うモジュール
"""

import json
import time
from datetime import datetime

import serial
from serial import PortNotOpenError
from serial import SerialException

# ポート設定
PORT = '/dev/ttyUSB0'
# 通信レート設定
BAUD_RATE = 9600


def send(msg: str):
    """データ送信用関数

    Args:
        msg (str): 送信するメッセージ

    Raises:
        PortNotOpenError: ポートが空いておらず、リトライにも失敗した場合発生します
        SerialException: デバイスがみつからないときに発生します
    """
    # ログ用ファイルをオープン
    f = open('send_data' + datetime.now().strftime('%Y年%m月%d日_%H時%M分%S秒') + '.json', 'a')
    # jsonとして書き込み
    json.dump(msg, f, indent=4, ensure_ascii=False)
    f.close()

    retry_c = 0
    while True:
        try:
            ser = serial.Serial(PORT, BAUD_RATE)
            # シリアルにjsonを書き込む
            ser.write(msg.encode('utf-8'))
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


async def receive() -> str:
    """データ受信用非同期関数

    XBeeでデータを受信するまで待つ関数です。
    処理を止めてしまうので非同期で実行するようにしてください。

    Examples:
        ブロッキング実行するサンプル

        ::

            asyncio.run(XBee.receive())

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
            receive_data: bytes = bytes()
            while len(receive_data) == 0:
                receive_data = ser.readline()

            ser.close()
            return receive_data.decode("utf-8")

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
