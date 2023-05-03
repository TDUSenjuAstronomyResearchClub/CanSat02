import RPi.GPIO as GPIO

# GPIOピンの設定
PWM_PIN = 18

# PWM周波数の設定
PWM_FREQ = 100

# 初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)

# PWMオブジェクトの作成
pwm = GPIO.PWM(PWM_PIN, PWM_FREQ)

# モーターを回転させる関数


def start_motor():
    pwm.start(0)
    pwm.ChangeDutyCycle(50)  # 50%のデューティ比で回転


def stop_motor():
    pwm.ChangeDutyCycle(0)   # 停止

# 終了処理


def cleanup():
    stop_motor()
    pwm.stop()
    GPIO.cleanup()