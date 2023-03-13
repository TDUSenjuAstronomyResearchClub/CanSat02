# -- coding: utf-8 --
import serial #Xbeeで送信する
import csv
import time
import datetime

import gps #gpsの緯度経度・海抜を求める
import DistanceAzimuth #ゴールとの直線距離を求める
import Distance #超音波距離センサで距離を求める
import NineAxisSensor #9軸センサで加速度・速度・角速度・地軸値を求める
import Temperature #温湿度気圧センサで温度・湿度・気圧を求める


#ポート設定
PORT = '/dev/ttyUSB0'      
#通信レート設定         
BAUD_RATE = 9600

#===機体に残すログ===
dt_start = datetime.datetime.now() #現在日時を取得する
filename = 'sending' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒') + '.csv'  #ファイル名を現在時刻にする

#表のインデックスを付ける
f = open(filename, 'a') 
writer = csv.writer(f, lineterminator='\n') 
index=['Times of Day','latitude','longitude','altitude','gps distance','ultrasound distance','acceleration(x axis)','acceleration(y axis)','acceleration(z axis)','speed(x axis)','speed(y axis)','speed(z axis)','angular velocity(x axis)','angular velocity(y axis)','angular velocity(z axis)','azimuth','temperature','barometric pressure','humidity','battery temperature','battery humidity']
writer.writerow(index)
f.close()

while True:
    #===センサから値を取得し、その都度地上局に送信する===
    ser = serial.Serial(PORT, BAUD_RATE)

    try:
        latitude = gps.gps_latitude()   #gpsから緯度の値を取得する
        lat=str(latitude)
        ser.write(b'latitude' + lat.encode('utf-8') + b'\n')    #gpsから緯度の値を送信する
    except  AttributeError :
        ser.write(b'Latitude value was not obtained correctly' + b'\n')

    try:
        longitude = gps.gps_longitude() #gpsから経度の値を取得する
        log=str(longitude)
        ser.write(b'longitude' + log.encode('utf-8') + b'\n')    #gpsから経度の値を送信する
    except AttributeError :
        ser.write(b'Longitude value was not obtained correctly' + b'\n')

    try:
        altitude = gps.gps_altitude()   #gpsから海抜の値を取得する
        alt=str(altitude)
        ser.write(b'altitude' + alt.encode('utf-8') + b'\n')    #gpsから海抜の値を送信する
    except AttributeError:
        ser.write(b'Altitude value was not obtained correctly' + b'\n')

    gps_distance = DistanceAzimuth.get_gpsdistance()  #ゴールとの直線距離を取得する
    gps=str(gps_distance)
    ser.write(b'direct distance' + gps.encode('utf-8') + b'\n')    #ゴールとの直線距離を送信する


    #超音波距離センサで障害物への距離を取得する
    ultrasound_distance = Distance.distance_result()   
    if ultrasound_distance == True:
        print('ultrasound distance type error') 
    else:
        ult=str(ultrasound_distance)
        ser.write(b'ultrasound distance' + ult.encode('utf-8') + b'\n')    #超音波距離センサで障害物への距離を送信する



    #9軸センサから加速度（x軸値、y軸値、z軸値）・速度（x軸値、y軸値、z軸値）を取得する
    acceleration_speed = NineAxisSensor.AccelerationSpeed() 
    if acceleration_speed == True:  #OS errerが発生した場合
        print('acceleration speed OS errer')
    else:
        speed=str(acceleration_speed)
        ser.write(b'acceleration(x axis,y axis,z axis),speed(x axis,y axis,z axis)' + speed.encode('utf-8') + b'\n')    #9軸センサから加速度のx軸値、y軸値、z軸値、速度のx軸値、y軸値、z軸値を送信する



    #===9軸センサから角速度のx軸値、y軸値、z軸値を取得する===
    angular_velocity = NineAxisSensor.AngularVelocity()  
    if angular_velocity == True:    #OS errerが発生した場合
        print('angular velocity OS errer')
    else:
        velocity=str(angular_velocity)
        ser.write(b'angular_velocity(x axis,y axis,z axis)' + velocity.encode('utf-8') + b'\n')    #9軸センサから角速度のx軸値、y軸値、z軸値を送信する


    #===9軸センサから地軸値のx軸値、y軸値、z軸値を取得する===
    Azimuth = NineAxisSensor.Azimuth()
    if Azimuth == True:   #OS errerが発生した場合
        print('azimuth OS errer')
    else:
        axis=str(Azimuth)
        ser.write(b'Azimuth' + axis.encode('utf-8') + b'\n')    #9軸センサから方位角を送信する
        


    #===外気用の温湿度気圧センサから温度・気圧・湿度の値を取得する===
    temperature = Temperature.Temperature_result() 
    if temperature == True:   #OS errerが発生した場合
        print('temperature OS errer')
    else:
        tem=str(temperature)
        ser.write(b'temperature,barometric pressure, humidity' + tem.encode('utf-8') + b'\n')    #温湿度気圧センサから温湿度・気圧の値を送信する

    #===バッテリー用の温湿度センサから温度・湿度の値を取得する===
    temperature = Temperature.Temperature_result() 
    if temperature == True:   #OS errerが発生した場合
        print('temperature OS errer')
    else:
        tem=str(temperature)
        ser.write(b'temperature,barometric pressure, humidity' + tem.encode('utf-8') + b'\n')    #温湿度気圧センサから温湿度・気圧の値を送信する



    ser.close() #シリアルポートを閉じる


    #===データの書き込みを行う===
    f = open(filename, 'a') 
    writer = csv.writer(f, lineterminator='\n') 
    dt_now = datetime.datetime.now() #現在日時を取得する

    #加速度・角速度・地軸のxyz追加
    send_data = (dt_now,latitude,longitude,altitude,gps_distance,ultrasound_distance,acceleration_speed[0],acceleration_speed[1],acceleration_speed[2],acceleration_speed[3],acceleration_speed[4],acceleration_speed[5],angular_velocity[0],angular_velocity[1],angular_velocity[2],Azimuth,temperature[0],temperature[1],temperature[2])#データをまとめる           
    
    writer.writerow(send_data)
    f.close()
    time.sleep(2)
