import RPi.GPIO as GPIO
import time
import Temperature

#測定環境温度
temp = Temperature.Temperature_result() #温湿度気圧センサから現在の温度値を呼び出す
TEMP = temp[0]

#GPIO設定
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

#繰り返し
#while True:
def distance_result() :
    try:
        #トリガ信号出力
        GPIO.output(17, GPIO.HIGH)
        time.sleep(0.00001)
        
        GPIO.output(17, GPIO.LOW)
        
        #返送HIGHレベル時間計測
        while GPIO.input(27) == GPIO.LOW:
            soff = time.time()    #LOWレベル終了時刻
        
        while GPIO.input(27) == GPIO.HIGH:
            son = time.time()    #HIGHレベル終了時刻
        
        #HIGHレベル期間の計算
        clc = son - soff
        
        #時間から距離に変換(TEMPは測定環境温度)
        clc = clc * (331.50 + (0.6 * TEMP)) / 2 * 100
        
        #画面に表示
        #print(str(clc))
        #一時停止
        #time.sleep(0.1)
        return str(clc)
    except TypeError:
        return True