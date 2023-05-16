"""カメラモジュール

カメラモジュールを使って画像を撮影、地上局に送信するモジュール

使用しているライブラリ:
    py
"""

import datetime
import json
import time

from picamera2 import Picamera2
import serial
from serial import SerialException

# ポート設定
PORT = '/dev/ttyUSB0'

# 通信レート設定
BAUD_RATE = 9600


def photograph():
    """カメラモジュールを使って画像を撮影、地上局に送信ができるプログラム

    Raises:
        CameraError: カメラに不具合があった際に発生
    """
    picam2 = Picamera2()

    # 画像サイズの設定
    preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    picam2.configure(preview_config)

    # 画像ファイル名の作成
    date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = date + ".jpg"

    # 撮影
    picam2.start()
    picam2.capture_file(filename)
    picam2.close()

    ser = serial.Serial(PORT, 9600)  # XBeeシリアルポートを開く

    for i in range(5):
        with open(filename, 'rb') as img:  # 画像ファイルをバイナリデータとして開く
            try:
                data = img.read()
                camera_data = data.hex()
                json_data = json.dumps({"camera": camera_data, "time": date})

                ser.write(json_data.encode("UTF-8"))  # XBeeに送信

                ser.close()  # XBeeシリアルポートを閉じる
                return

            except SerialException:
                time.sleep(1)

    return


class CameraError(Exception):
    """カメラ使用時のエラー
    """
