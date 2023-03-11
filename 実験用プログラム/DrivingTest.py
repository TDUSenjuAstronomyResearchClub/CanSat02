import serial
import datetime
import csv
import time
import RPi.GPIO as GPIO # RPi.GPIOモジュールを使用

import Camera   #カメラモジュール
import NineAxisSensor   #9軸センサ
import DistanceAzimuth  #GPSからゴールとの直線距離と方位角を求める
import Distance     #超音波距離センサ
import SoilMoisture #土壌水分センサ


#===3秒間前進する関数　引数：なし　戻り値：なし===
def StraightLine():
    p1.ChangeDutyCycle(80) #duty比（moterで動かすための値）
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(80) #duty比（moterで動かすための値）
    p4.ChangeDutyCycle(0)
    time.sleep(3)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)
    time.sleep(1)
    return

#===3秒間後退する関数　引数：なし　戻り値：なし===
def Back():
    p1.ChangeDutyCycle(0) #duty比（moterで動かすための値）
    p2.ChangeDutyCycle(80)
    p3.ChangeDutyCycle(0) #duty比（moterで動かすための値）
    p4.ChangeDutyCycle(80)
    time.sleep(3)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)
    time.sleep(1)
    return

#===右旋回する関数　引数：なし　戻り値：なし===
def TurnRight():
    p1.ChangeDutyCycle(100) #duty比（moterで動かすための値）
    p2.ChangeDutyCycle(0)
    time.sleep(1)   
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    time.sleep(1)
    return

#===左旋回する関数　引数：なし　戻り値：なし===
def TurnLeft():
    p3.ChangeDutyCycle(100) #duty比（moterで動かすための値）
    p4.ChangeDutyCycle(0)
    time.sleep(1)   
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)
    time.sleep(1)
    return

#===地上局から手動で運転する関数　引数：なし　戻り値：なし===
def ManualControl():
    ser = serial.Serial(PORT, BAUD_RATE)
    ser.write(b'manual operation start')
    log('manual operation start','none')    #関数logにマニュアル運転がスタートしたと残す

    while True:
        Camera.photograph() #カメラの写真を送信
        command = ser.read_all()
        log('manual operation',command) #関数ログに値を渡す
        ser.write(b'receive')   #地上局に受け取った値を戻す
        ser.write(command.encode('utf-8'))

        if command == b'end':    #地上局から「end」を受け取ったらManualControlを終了する
            break
        elif command == b'w':    #地上局から「w」を受け取ったら3秒間直進する
            StraightLine()
        elif command == b'd':    #地上局から「d」を受け取ったら右旋回する
            TurnRight()
        elif command == b'a':    #地上局から「a」を受け取ったら左旋回する
            TurnLeft()
        elif command == b's':    #地上局から「s」を受け取ったら3秒間後退する
            Back()
        else:   #どの条件分岐にも当てはまらなかったら地上局に文字が違うと送る
            ser.write(b'Wrong character.Send the correct letters.')

    ser.close()
    return 

#===logを残す関数　引数：log_type(この値が何の意味を持つのかの説明),value(変数値)　戻り値：なし===
def log(log_type,value):
    dat_now = datetime.datetime.now()   #現在日時を取得する
    explanation = log_type
    variable = value
    writer = csv.writer(f, lineterminator='\n') 
    log_list = [dat_now,explanation,variable]   #リストに各値を挿入

    f = open(filename,'a')
    writer.writerow(log_list)
    print(log_list)
    f.close()
    time.sleep(0.1)
    return

#===ゴールと機体の正面が一直線になるように機体の角度を調節する関数　引数：なし　戻り値：なし===
def AngleAdjustment():
    ser = serial.Serial(PORT, BAUD_RATE)
    ser.write(b'angle adjustment start')    #ゴールと機体の正面が一直線になるように機体の角度を調節するフェーズになったと地上局に送る

    while True:
        heading = NineAxisSensor.Azimuth()    #9軸センサの地磁気値を呼び出す関数名が変更になる可能性大　地磁気から求めた磁方位角を格納する
        log('Orientation of CanSat',heading)

        distination_heading = DistanceAzimuth.get_azimuth() #緯度経度から求めた方位角を格納する
        log('destination heading',distination_heading)

        difference = distination_heading - heading

        if difference>30:   #ここの値の調節は走行試験で行う
            if difference>=0:
                TurnLeft()
            else:
                TurnRight()
        else:
            ser.write(b'angle adjustment finish')
            break
        time.sleep(1)

    ser.close()
    return 


#===溶断回路の設定(ピン番号変わる可能性あり)===
soil_moisture_spring = 23
carrier = 24

# ===GPIO番号指定の準備===
GPIO.setmode(GPIO.BCM)

# ===溶断回路の配線===
GPIO.setup(soil_moisture_spring, GPIO.OUT)
GPIO.setup(carrier, GPIO.OUT)


#===moterの配線===
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

#===進行方向に機体を置き、後ろから見た時の右モーター===
p2 = GPIO.PWM(5, 50) #50Hz
p1 = GPIO.PWM(6, 50) #50Hz

#===進行方向に機体を置き、後ろから見た時の左モーター===
p3 = GPIO.PWM(19, 50) #50Hz
p4 = GPIO.PWM(26, 50) #50Hz

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

#プログラムの処理時間を求めるための基準値
start_time = time.time()

#===ポート設定===
PORT = '/dev/ttyUSB0'      
#===通信レート設定===       
BAUD_RATE = 9600

#===ログ用ファイルの作成===
dt_start = datetime.datetime.now() #現在日時を取得する
filename = 'Running' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒') + '.csv'  #ファイル名を現在時刻にする

f = open(filename, 'a')     
writer = csv.writer(f, lineterminator='\n') 
index=['Time of Day','Log type value','value']  #表のインデックスを付ける
writer.writerow(index)
f.close()

#===メインプログラム===
#---機体をゴールまで進ませる---

log('photo shoot',None)
    
Camera.photograph() #写真を撮って地上局に伝える

AngleAdjustment()   #ゴールと機体の向きを一直線にする
    
#--直進する--
p1.ChangeDutyCycle(80) #duty比（moterで動かすための値）
p2.ChangeDutyCycle(0)
p3.ChangeDutyCycle(80) #duty比（moterで動かすための値）
p4.ChangeDutyCycle(0)

while True:
    close_distance = Distance.distance_result() #障害物との距離を調べる
    log('ultrasonic distance sensor',close_distance)

    gps_distance = DistanceAzimuth.get_gpsdistance()    #gpsセンサでゴールとの直線距離を求める
    log('gps distance',gps_distance)

    if close_distance<=30 or gps_distance<=0.3: #障害物に近づくかゴールに近づいたかどうか
        #--停止--
        p1.ChangeDutyCycle(0) #duty比（moterで動かすための値）
        p2.ChangeDutyCycle(0)
        p3.ChangeDutyCycle(0) #duty比（moterで動かすための値）
        p4.ChangeDutyCycle(0)

        ManualControl() #手動運転に切り替える

        gps_distance = DistanceAzimuth.get_gpsdistance()    #gpsセンサでゴールとの直線距離を求める
        log('gps distance',gps_distance)

        if gps_distance <=0.3:
            break
    
    time.sleep(0.5)

#---溶断回路を動かす（土壌水分センサのバネ開放）---
ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)
ser.write(b'fusing circuit start(soil moisture)')  #溶断回路を動かすと地上局に伝える
ser.close()

log('using circuit start(soil moisture)',None)

GPIO.output(soil_moisture_spring, 1)    # 溶断開始
time.sleep(10)               # 10秒待機
GPIO.output(soil_moisture_spring, 0) #溶断停止

log('using circuit end(soil moisture)',None)

ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)
ser.write(b'fusing circuit end(soil moisture)')  #溶断回路を動かすと地上局に伝える
ser.close()

#---土壌水分センサを動かす---
ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)
ser.write(b'soil moisture start')  #土壌水分センサを動かすと地上局に伝える
ser.close()

resistance = SoilMoisture.SoilMois_result()
log('soil moisture',resistance)

ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)
resistance_result = str(resistance)
ser.write(resistance_result.encode('utf-8'))    #土壌水分センサの抵抗値を測る
ser.write(b'goal now')  #土壌水分センサを動かすと地上局に伝える
ser.close()
log('goal now',None)