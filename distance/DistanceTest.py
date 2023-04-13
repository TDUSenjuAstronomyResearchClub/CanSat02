# -- coding: utf-8 --
#Distance.pyの動作確認をするための実行プログラム
import distance
import time

while True:
    ultrasound_distance = Distance.distance_result()
    if ultrasound_distance == True:
        print('ultrasound distance type error') 
    else:
        print(ultrasound_distance)
    time.sleep(1)
