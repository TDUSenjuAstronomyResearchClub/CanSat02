import serial
from PIL import Imaged
import datetime
import time
import json

#ポート設定
PORT = '/dev/ttyUSB0'      
#通信レート設定         
BAUD_RATE = 9600

while True:
    ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)
    utf8_string = ser.read_all()    #機体から値を受け取る
    first_byte = utf8_string[0]     # バイト列から先頭バイトを取得する
    first_char = chr(first_byte)    # 先頭バイトを文字列に変換する

    if first_char == 'a':   #ソーラーパネルについての値
        solar = utf8_string[1:].decode("utf-8") # バイト列から先頭バイトを取り除いた文字列を取得する
        with open('./receive.json','a') as f:
            json.dump(solar,f)
    
    if first_char == 'b':   #温湿度気圧センサについての値
        temp = utf8_string[1:].decode("utf-8") # バイト列から先頭バイトを取り除いた文字列を取得する
        with open('./receive.json','b') as f:
            json.dump(solar,f)

    if first_char == 'c':   #9軸センサについての値
        NineAxis = utf8_string[1:].decode("utf-8") # バイト列から先頭バイトを取り除いた文字列を取得する
        with open('./receive.json','c') as f:
            json.dump(solar,f)

    if first_char == 'd':   #距離センサについての値
        distance = utf8_string[1:].decode("utf-8") # バイト列から先頭バイトを取り除いた文字列を取得する
        with open('./receive.json','d') as f:
            json.dump(solar,f)

    if first_char == 'e':   #ゴールとの直線距離と方位角についての値
        DistanceAzimuth = utf8_string[1:].decode("utf-8") # バイト列から先頭バイトを取り除いた文字列を取得する
        with open('./receive.json','e') as f:
            json.dump(solar,f)

    if first_char == 'f':   #gpsについての値
        DistanceAzimuth = utf8_string[1:].decode("utf-8") # バイト列から先頭バイトを取り除いた文字列を取得する
        with open('./receive.json','f') as f:
            json.dump(solar,f)

    if first_char == 'g':   #カメラについての値
        camera = utf8_string[1:].decode("utf-8") # バイト列から先頭バイトを取り除いた文字列を取得する

        now =datetime.datetime.now()
        d = now.strftime('%Y-%m-%d_%H-%M-%S')
        file_name = d + '.jpg'  # 受信データを保存するファイル名
        file = open(file_name, "wb")    # ファイルを開く
        file.write(camera)
        file.close()    #ファイルを閉じる

    if first_char == 'h':   #土壌水分センサについての値
        soil = utf8_string[1:].decode("utf-8") # バイト列から先頭バイトを取り除いた文字列を取得する
        with open('./receive.json','h') as f:
            json.dump(solar,f)
    
    time. sleep(0.1)