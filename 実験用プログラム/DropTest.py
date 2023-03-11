import csv  #csv形式で出力する
import smbus #ダウンロードする9軸を動かすためのライブラリ
import time
import datetime
#import sys
import RPi.GPIO as GPIO
import serial


GPIO.setmode(GPIO.BCM)  # GPIO番号で、指定できるように設定
print("基板設定完了")

addressG = 0x6a
addressA = 0x6a
addressM = 0x1c
getG=0x18
getA=0x28
getM=0x28

CTRL_REG1_G  = 0x10
CTRL_REG4    = 0x1E
CTRL_REG5_XL = 0x1F
CTRL_REG3_M  = 0x22
#dev_addr = 0x39

#try:
bus = smbus.SMBus(1)
time.sleep(1)

bus.write_byte_data(addressG, CTRL_REG1_G, 0b00100000)   #gyro/accel odr and bw
bus.write_byte_data(addressG, CTRL_REG4, 0b00111000)     #enable gyro axis
bus.write_byte_data(addressA,CTRL_REG5_XL, 0b00111000)  #enable acceleromete
bus.write_byte_data(addressM, CTRL_REG3_M, 0b00000000)   #enable mag continuous]
#照度センサーの設定
#ret = bus.write_byte_data(dev_addr, 0x80|0x20|0x0F, 0x02)
#ret = bus.write_byte_data(dev_addr, 0x80|0x20|0x01, 0xF6)
#ret = bus.write_byte_data(dev_addr, 0x80|0x20|0x00, 0x02|0x01)

#ポート設定
PORT = '/dev/ttyUSB0'      
#通信レート設定         
BAUD_RATE = 9600
ser = serial.Serial(PORT, BAUD_RATE,timeout=0.1)

time.sleep(1)


dt_start = datetime.datetime.now() #現在日時を取得する
filename = 'log_' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒') + '.csv'  #ファイル名を現在時刻にする

#表のインデックスを付ける
f = open(filename, 'a') 
writer = csv.writer(f, lineterminator='\n') 
index=['時刻','x軸の加速度','y軸の加速度','z軸の加速度','x軸の速度','y軸の加速度','z軸の加速度','PCから受信した値']        #,'可視光と赤外光（Ch0）','赤外光（Ch1）'
print(index)
writer.writerow(index)
f.close()

time_start = time.time() #積分するための基準時間を作る

try:
        while True:
                #積分時間の始まりを取得
                integration_time1 = time.time() - time_start    
                # PWMをDuty比10で出力(負論理、かつ100がMAX)
                #pwm47.start(90)

                dataA = bus.read_i2c_block_data(addressA, getA,6)

                rawAX = ((dataA[1] * 256) + (dataA[0] & 0xF0)) / 16
                if (rawAX > 2047):
                        rawAX -= 4096
                rawAY = ((dataA[3] * 256) + (dataA[2] & 0xF0)) / 16
                if (rawAY > 2047):
                        rawAY -= 4096
                rawAZ = ((dataA[5] * 256) + (dataA[4] & 0xF0)) / 16
                if (rawAZ > 2047):
                        rawAZ -= 4096
                
                integration_time2 = time.time() - time_start 

                AX = rawAX * 0.0098 * 9.80665      #range = +/-2g  x軸の加速度（rawAXに0.0098をかけることで物理量(G)が求められる。それに9.80665をかけることで加速度がわかる）
                AY = rawAY * 0.0098 * 9.80665      #range = +/-2g  y軸の加速度（rawAYに0.0098をかけることで物理量(G)が求められる。それに9.80665をかけることで加速度がわかる）
                AZ = rawAZ * 0.0098 * 9.80665      #range = +/-2g  z軸の加速度（rawAZに0.0098をかけることで物理量(G)が求められる。それに9.80665をかけることで加速度がわかる）
                VX = AX * integration_time2 - AX * integration_time1    #x軸の速度
                VY = AY * integration_time2 - AY * integration_time1    #y軸の速度
                VZ = AZ * integration_time2 - AZ * integration_time1    #z軸の速度
                
                #データ読み込み
                #uv = bus.read_i2c_block_data(dev_addr, 0x80|0x20|0x14, 0x04)
        
                #データ変換
                #ch0 = uv[1] << 8 | uv[0]
                #ch1 = uv[3] << 8 | uv[2]
        
                #物理量（UV照度）に変換
                #ch0 = ch0 / 16 / 19.0
                #ch1 = ch1 / 16 / 10.8

                #Xbeeから値を受け取る
                time.sleep(0.1)
                xbee = ser.read_all()

                #Xbeeを使い値を送る
                ser = serial.Serial(PORT, BAUD_RATE)
                ser.write(b'OK')   #endをPCに送る
                
                #データの書き込みを行う
                f = open(filename, 'a') 
                writer = csv.writer(f, lineterminator='\n') 
                dt_now = datetime.datetime.now() #現在日時を取得する
                acceleration_now = [dt_now,AX,AY,AZ,VX,VY,VZ,xbee]   #,ch0,ch1

                writer.writerow(acceleration_now)
                print(acceleration_now)
                f.close()
                time.sleep(0.1)

except KeyboardInterrupt:
        ser.close()
        print('stop!')

        
        
