"""DCモーター制御用モジュール
"""
import RPi.GPIO as GPIO


class DCMotor:
    """DCモーターを制御するクラス
    """

    def __init__(self, pin: int, freq: int = 100):
        """DCモーターを初期化するメソッド

        Args:
            pin (int): PWM制御用のピン
            freq (int): PWMの周波数[Hz]
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, freq)

    def start_motor(self, duty: int = 50):
        """モーターを回転させるメソッド

        Args:
            duty (int): デューティ比[%] デフォルトは50%
        """
        self.pwm.start(0)
        self.pwm.ChangeDutyCycle(duty)

    def change_duty(self, duty: int):
        """モーターのデューティ比を変更するメソッド

        Args:
            duty (int): デューティ比[%]
        """
        self.pwm.ChangeDutyCycle(duty)

    def stop_motor(self):
        """モーターを停止させるメソッド
        """
        self.pwm.ChangeDutyCycle(0)  # 停止

    def cleanup(self):
        """モーターの使用後に呼び出すメソッド

        GPIOのクリーンアップを行います。
        DCモーター使用後は必ず呼び出して下さい。
        """
        self.stop_motor()
        self.pwm.stop()
        GPIO.cleanup()
