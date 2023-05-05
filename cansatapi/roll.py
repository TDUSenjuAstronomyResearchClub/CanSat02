"""DCモーター制御用モジュール
"""
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


def start_motor():
    """モーターを回転させる関数
    """
    pwm.start(0)
    pwm.ChangeDutyCycle(50)  # 50%のデューティ比で回転


def stop_motor():
    """モーターを停止させる関数
    """
    pwm.ChangeDutyCycle(0)  # 停止


def cleanup():
    """モーターの使用後に呼び出す関数

    GPIOのクリーンアップを行います。
    DCモーター使用後は必ず呼び出して下さい。
    """
    stop_motor()
    pwm.stop()
    GPIO.cleanup()
