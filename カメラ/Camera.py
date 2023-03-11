from time import strftime
import cv2
import datetime
import numpy as np
import serial
import binascii

PORT = '/dev/ttyUSB0' 

def photograph():
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



