#################################################################################
#           TDU CanSat 02 Main Program                                          #
#           (C) 2022-2023 TokyoDenkiUniversity-AstronomyClub-CansatTeam         #
#           coding by YamashitaTaichi,                                          #
#           KashiwagiMizuki, KatoRikuo, YamazakiYuma,                           #
#           and IshiharaRioto.                                                  #
#################################################################################

import serial
import datetime
import csv
import time
import RPi.GPIO as GPIO # RPi.GPIOモジュールを使用

import SoilMoisture #土壌水分センサ
#import Camera



#===logを残す関数　引数：log_type(この値が何の意味を持つのかの説明),value(変数値),filename(グローバルで定義したファイル名)　戻り値：なし===
def log(log_type,value,filename):
    f = open(filename,'a')
    dat_now = datetime.datetime.now()   #現在日時を取得する
    writer = csv.writer(f, lineterminator='\n') 
    log_list = (dat_now,log_type,value)   #リストに各値を挿入

    writer.writerow(log_list)
    print(log_list)
    f.close()
    time.sleep(0.1)
    return

# ===GPIO番号指定の準備===
GPIO.setmode(GPIO.BCM)

#===溶断回路の設定(ピン番号変わる可能性あり)===
soil_moisture_spring = 24
GPIO.setup(soil_moisture_spring, GPIO.OUT)


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

def manual_mode():

    #===ポート設定===
    PORT = '/dev/ttyUSB0'      
    #===通信レート設定===       
    BAUD_RATE = 9600

#===ログ用ファイルの作成===
    dt_start = datetime.datetime.now() #現在日時を取得する
    filename = 'Running' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒') + '.csv'  #ファイル名を現在時刻にする

    f = open(filename, 'a')     
    writer = csv.writer(f, lineterminator='\n') 
    index=('Time of Day','Log type value','value')  #表のインデックスを付ける
    writer.writerow(index)
    f.close()

    #===メインプログラム===
    #---機体をゴールまで進ませる---
    ser = serial.Serial(PORT, BAUD_RATE)
    ser.write(b'manual operation start')
    log('manual operation start','none',filename)    #関数logにマニュアル運転がスタートしたと残す

    while True:
        #Camera.photograph()#カメラを起動し地上局に送信する

        command = ser.read_all()
        log('manual operation',command,filename) #関数ログに値を渡す
        ser.write(b'receive')   #地上局に受け取った値を戻す
        ser.write(command.encode('utf-8'))

        if command == b'end':    #地上局から「end」を受け取ったらManualControlを終了する
            ser.write(b'manual operation finish')
            log('manual operation finish',None,filename)
            ser.close()
            break
        elif command == b'w':    #地上局から「w」を受け取ったら3秒間直進する
                log('went straight',None,filename)   #前進したというログを残す
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
        elif command == b'd':    #地上局から「d」を受け取ったら右旋回する
                log('turn right',None,filename)   #右旋回したというログを残す
                p1.ChangeDutyCycle(100) #duty比（moterで動かすための値）
                p2.ChangeDutyCycle(0)
                time.sleep(1)   
                p1.ChangeDutyCycle(0)
                p2.ChangeDutyCycle(0)
                time.sleep(1)
        elif command == b'a':    #地上局から「a」を受け取ったら左旋回する
                log('turn left',None,filename)   #左旋回したというログを残す
                p3.ChangeDutyCycle(100) #duty比（moterで動かすための値）
                p4.ChangeDutyCycle(0)
                time.sleep(1)   
                p3.ChangeDutyCycle(0)
                p4.ChangeDutyCycle(0)
                time.sleep(1)
        elif command == b's':    #地上局から「s」を受け取ったら3秒間後退する
                log('went back',None,filename)   #後退したというログを残す
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
        elif command == b'':
            pass
        else:   #どの条件分岐にも当てはまらなかったら地上局に文字が違うと送る
            ser.write(b'Wrong character.Send the correct letters.')
        ser.close()


    #---溶断回路を動かす（土壌水分センサのバネ開放）---
    ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)
    ser.write(b'fusing circuit start(soil moisture)')  #溶断回路を動かすと地上局に伝える
    ser.close()

    log('using circuit start(soil moisture)',None,filename)

    GPIO.output(soil_moisture_spring, 1)    # 溶断開始
    time.sleep(10)               # 10秒待機
    GPIO.output(soil_moisture_spring, 0) #溶断停止

    log('using circuit end(soil moisture)',None,filename)

    ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)
    ser.write(b'fusing circuit end(soil moisture)')  #溶断回路を動かすと地上局に伝える
    ser.close()

    #---土壌水分センサを動かす---
    ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)
    ser.write(b'soil moisture start')  #土壌水分センサを動かすと地上局に伝える
    ser.close()

    resistance = SoilMoisture.SoilMois_result()
    if resistance == True:
        ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)
        ser.write(b'soil moisture errer program finish')
        ser.close()
        log('soil moisture errer',None,filename)
        GPIO.cleanup
    else:     
        log('soil moisture',resistance,filename)

        ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)
        resistance_result = str(resistance)
        ser.write(resistance_result.encode('utf-8'))    #土壌水分センサの抵抗値を測る
        ser.write(b'goal now')  #土壌水分センサを動かすと地上局に伝える
        ser.close()
        log('goal now',None,filename)
        GPIO.cleanup()