"""機体と地上局の通信を行うモジュール
"""

import time
from datetime import datetime

import serial
from serial import PortNotOpenError
from serial import SerialException

from .util.logging import json_log, DATETIME_F
from .message import jsonGenerator

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
    json_log(msg)  # ローカルにJSONを保存
    retry_c = 0
    while True:
        try:
            ser = serial.Serial(PORT, BAUD_RATE)
            # シリアルにjsonを書き込む
            ser.write(msg.encode('utf-8'))
            ser.write(0x04)  # EOTを末尾に書き込む
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


def send_msg(msg: str):
    """任意のメッセージを地上に送信する関数

    Args:
        msg: 任意のメッセージ
    """
    send(jsonGenerator.generate_json(time=datetime.now().strftime(DATETIME_F), message=msg))


def send_pic(pic_hex: str):
    """写真データを地上に送信する関数

    Args:
        pic_hex: 写真データ(16進数)
    """
    send(jsonGenerator.generate_json(time=datetime.now().strftime(DATETIME_F), camera=pic_hex))


def receive() -> str:
    """データ受信用関数

    XBeeでデータを受信するまで待つ関数です。

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
