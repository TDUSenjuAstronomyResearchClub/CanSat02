"""機体と地上局の通信を行うモジュール
"""

import json
import time
import datetime
import serial
from serial import SerialException

# ポート設定
PORT = '/dev/ttyUSB0'
# 通信レート設定
BAUD_RATE = 9600

# シリアルポート使用判定フラグ(使用中はTrue)
is_using_serial_port = False


def send(filename: str, json_data: str):
    """データ送信用関数

    Args:
        filename (str): ファイルネーム
        json_data (str): JSON形式のデータ
    """
    # ログ用ファイルをオープン
    f = open(filename, 'a')
    # jsonとして書き込み
    json.dump(json_data, f, indent=4, ensure_ascii=False)
    f.close()

    while True:
        global is_using_serial_port
        if not is_using_serial_port:  # シリアルポートは使用中ではないか
            # シリアルポート使用判定フラグを使用中にする
            is_using_serial_port = True

            try:
                ser = serial.Serial(PORT, BAUD_RATE)
                # シリアルにjsonを書き込む
                ser.write(json_data.encode('utf-8'))
                ser.close()

                is_using_serial_port = False
                break

            except SerialException:  # デバイスが見つからない、または構成できない場合
                is_using_serial_port = False
                break  # ここの処理について要件等

        else:
            time.sleep(0.5)

    return


def receive(filename: str) -> str:
    """データ送信用関数

    Returns:
        str: 受信した文字列

    Raises:
        SerialException: デバイスがみつからないときに発生します
        PortNotOpenError: ポートが空いていないときに発生します
    """
    global is_using_serial_port
    if not is_using_serial_port:
        # シリアルポート使用判定フラグを使用中にする
        is_using_serial_port = True

        try:
            now = datetime.datetime.now()  # センサ値取得開始日時の取得
            ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
            utf8_string = ser.read_all()  # 機体から値を受け取る
            ser.close()
            
            catch_value = {
                "time": now,
                "message":utf8_string
            }
            # ログ用ファイルをオープン
            f = open(filename, 'a')
            # jsonとして書き込み
            json.dump(catch_value, f, indent=4, ensure_ascii=False)
            f.close()

            is_using_serial_port = False
            return utf8_string

        except SerialException:  # デバイスが見つからない、または構成できない場合
            is_using_serial_port = False
            raise SerialException

    else:
        raise serial.PortNotOpenError
