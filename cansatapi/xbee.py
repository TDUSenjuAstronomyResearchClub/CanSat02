"""機体と地上局の通信を行うモジュール
"""
import multiprocessing
import time
from datetime import datetime

import serial
from serial import PortNotOpenError
from serial import SerialException

from .message import jsonGenerator
from .util.logging import json_log, DATETIME_FMT

# ポート設定
PORT = '/dev/ttyUSB0'
# 通信レート設定
BAUD_RATE = 9600

_send_queue = multiprocessing.Queue()
_receive_queue = multiprocessing.Queue()


def start():
    """XBeeモジュールの待機動作を開始する関数
    """
    while True:
        while _send_queue.empty():
            _receive(1)  # 1秒間待機する
        _send()


def _send():
    """キューからメッセージを送信する関数
    """
    msg = _send_queue.get_nowait()
    if msg is None:
        return

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


def send(msg: str):
    """データ送信用関数

    Args:
        msg (str): 送信するメッセージ
    """
    json_log(msg)  # ローカルにJSONを保存
    _send_queue.put_nowait(msg)


def send_msg(msg: str):
    """任意のメッセージを地上に送信する関数

    Args:
        msg: 任意のメッセージ
    """
    send(jsonGenerator.generate_json(time=datetime.now().strftime(DATETIME_FMT), message=msg))


def send_pic(pic_hex: str):
    """写真データを地上に送信する関数

    Args:
        pic_hex: 写真データ(16進数)
    """
    send(jsonGenerator.generate_json(time=datetime.now().strftime(DATETIME_FMT), camera=pic_hex))


def _receive(sec: float, retry: int = 5, retry_wait: float = 0.5) -> bool:
    """データを地上から受信する関数

    データを受信するとキューにデータを格納します。

    Args:
        retry_wait (float): リトライ時に待機する秒数
        sec (float): 待機する時間
        retry (int): ポートが使用中だった際のリトライ回数

    Returns:
        bool: データを受信したかどうか
    """
    st = time.time()
    ret = 0
    while time.time() - st < sec:
        try:
            ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
            receive_data = ser.readline().removesuffix(bytes(0x04))
            ser.close()
            if len(receive_data) != 0:
                data_utf8 = receive_data.decode("utf-8")
                json_log(data_utf8)  # ロギング
                _receive_queue.put_nowait(data_utf8)  # キューに受信したデータを追加

            return len(receive_data) != 0

        except PortNotOpenError:
            # 5回リトライに失敗したらエラーを吐く
            if ret >= retry:
                raise PortNotOpenError
            else:
                time.sleep(retry_wait)
                continue
        except SerialException:  # デバイスが見つからない、または構成できない場合
            raise SerialException


def get_received_str() -> str:
    """受信した文字列を返す関数

    Returns:
        str: 受信した文字列
    """
    return _receive_queue.get_nowait()
