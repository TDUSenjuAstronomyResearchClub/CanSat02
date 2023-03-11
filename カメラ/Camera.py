"""
Module Name:<br> 
カメラモジュール<br><br>
Description:<br> 
カメラモジュールを使って画像を撮影、地上局に送信ができるプログラム。動作確認用実行ファイルはCameraTest.py<br><br>
Library:<br>
opencv<br>
sudo apt-get install python-opencv<br>
または<br>
pip install opencv-python<br>
または<br>
pip3 install opencv-python<br>
よりインストールする。<br><br>

依存関係のあるライブラリをインストールする。<br>
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-100<br>
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5<br>
sudo apt-get install libatlas-base-dev<br>
sudo apt-get install libjasper-dev<br><br>

他にnumpyのバージョンが古いとうまくいかないのでアプデを行うこと。<br>
sudo pip3 install -U numpy<br>
"""

from time import strftime
import cv2
import datetime
import numpy as np
import serial
import binascii

PORT = '/dev/ttyUSB0' 

def photograph():
    """
    カメラモジュールを使って画像を撮影、地上局に送信ができるプログラム。

    Returns
    -------
    なし(撮影が出来ないとCannot open cameraが出力される)

    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        

    #画像ファイルの作成
    now =datetime.datetime.now()
    d = now.strftime('%Y-%m-%d_%H-%M-%S')
    today = d + '.jpg' 

    ret, Frame = cap.read()
    if not ret:
        print("Cannot read frame")
        cap.release()
        
    
    #resize the window
    windowsize = (200, 200)
    frame = cv2.resize(Frame, windowsize)   #画像サイズ
    cv2.imwrite(today, frame)   #名前付け保存
    cap.release()

    ser = serial.Serial(PORT, 9600) # XBeeシリアルポートを開く

    with open(today, 'rb') as img: # 画像ファイルをバイナリデータとして開く
        data = img.read()
        ser.write(data) # XBeeに送信

    ser.close() # XBeeシリアルポートを閉じる
    return



