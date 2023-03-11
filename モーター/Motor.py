import RPi.GPIO as GPIO # RPi.GPIOモジュールを使用
import time

#moterの配線
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

#進行方向に機体を置き、後ろから見た時の右モーター
p2 = GPIO.PWM(5, 50) #50Hz
p1 = GPIO.PWM(6, 50) #50Hz

#進行方向に機体を置き、後ろから見た時の左モーター
p3 = GPIO.PWM(19, 50) #50Hz
p4 = GPIO.PWM(26, 50) #50Hz

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

#３秒間直進して、停止する
print("３秒間直進")
p1.ChangeDutyCycle(80) #duty比（moterで動かすための値）
p2.ChangeDutyCycle(0)
p3.ChangeDutyCycle(80) #duty比（moterで動かすための値）
p4.ChangeDutyCycle(0)
time.sleep(3)
print("停止")
p1.ChangeDutyCycle(0)
p2.ChangeDutyCycle(0)
p3.ChangeDutyCycle(0)
p4.ChangeDutyCycle(0)
print("[３秒間直進して、停止する]終了")
time.sleep(2)

#機体を右に旋回する
print("機体を右に旋回する")
p1.ChangeDutyCycle(100) #duty比（moterで動かすための値）
p2.ChangeDutyCycle(0)
time.sleep(1)   
print("停止")
p1.ChangeDutyCycle(0)
p2.ChangeDutyCycle(0)
print("[機体を右に旋回する]終了")
time.sleep(1) 

