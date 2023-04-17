"""カメラモジュール

カメラモジュールを使って画像を撮影、地上局に送信するモジュール

使用しているライブラリ:
    open-cv

依存関係のあるライブラリ:
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-100
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev

他にnumpyのバージョンが古いとうまくいかないのでアプデを行うこと
sudo pip3 install -U numpy
"""

import datetime
import time

import cv2
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
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise CameraError("カメラを開けません")

    # 画像ファイルの作成
    now = datetime.datetime.now()
    d = now.strftime('%Y-%m-%d_%H-%M-%S')
    today = d + '.jpg'

    ret, frame = cap.read()
    if not ret:
        cap.release()
        raise CameraError("フレームを開けません")

    # ウィンドウをリサイズ
    window_size = (200, 200)
    frame = cv2.resize(frame, window_size)  # 画像サイズ
    cv2.imwrite(today, frame)  # 名前付け保存
    cap.release()

    ser = serial.Serial(PORT, 9600)  # XBeeシリアルポートを開く

    for i in range(5):
        with open(today, 'rb') as img:  # 画像ファイルをバイナリデータとして開く
            try:
                data = img.read()
                ser.write(data)  # XBeeに送信

                ser.close()  # XBeeシリアルポートを閉じる
                return

            except SerialException:
                time.sleep(1)

    return


class CameraError(Exception):
    """カメラ使用時のエラー
    """
    try:
        ser = serial.Serial(PORT, BAUD_RATE)
        exception = str(Exception)
        ser.write(exception.encode('utf-8') + b'\n')
        ser.close()      
    except SerialException:
        pass    #Runing.pyのログ用ファイルにエラーが起きたことを記入する
