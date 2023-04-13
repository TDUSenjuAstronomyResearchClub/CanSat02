# Distance.pyの動作確認をするための実行プログラム
from distance import distance
import time

if __name__ == "__main__":
    while True:
        ultrasound_distance = distance.distance_result()
        if ultrasound_distance:
            print('ultrasound distance type error')
        else:
            print(ultrasound_distance)
        time.sleep(1)
