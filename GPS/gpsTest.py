# -- coding: utf-8 --
import gps
import serial
import micropyGPS
import threading
import time


while True:
    latitude = gps.gps_latitude()
    longitude = gps.gps_longitude()
    altitude = gps.gps_altitude()
    if latitude == True or longitude == True or altitude:
        print('gps index error')

    else:
        print('緯度,経度,海抜')
        print(latitude, longitude, altitude)
        time.sleep(1)
