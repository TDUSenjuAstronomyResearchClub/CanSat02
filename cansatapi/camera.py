"""カメラモジュール

カメラモジュールを使って画像を撮影、地上局に送信するモジュール

使用しているライブラリ:
    picamera2
"""

import datetime

# from picamera2 import Picamera2

from .xbee import *


def photograph():
    """カメラモジュールを使って画像を撮影ができるプログラム

    Raises:
        CameraError: カメラに不具合があった際に発生
    """
    picam2 = Picamera2()

    # 画像サイズの設定
    preview_config = picam2.create_preview_configuration(main={"size": (200, 200)})
    picam2.configure(preview_config)

    # 画像ファイル名の作成
    date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = "./img/" + date + ".jpg"

    # 撮影
    picam2.start()
    picam2.capture_file(filename)
    picam2.close()

    with open(filename, 'rb') as img:  # 画像ファイルをバイナリデータとして開く
        data = img.read()
        send_pic(data.hex())


class CameraError(Exception):
    """カメラ使用時のエラー
    """
    pass    # TODO:仮で記入したため再考が必要
