"""DCモーター制御用モジュール
"""
import RPi.GPIO as GPIO


class DCMotor:
    """DCモーターをTB67H450FNGを通して制御するクラス
    """

    def __init__(self, in1: int, in2: int, freq: int = 100):
        """DCモーターを初期化するメソッド

        Args:
            in1 (int): PWM制御用のピン1
            in2 (int): PWM制御用のピン2
            freq (int): PWMの周波数[Hz]
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        self.in1 = GPIO.PWM(in1, freq)
        self.in2 = GPIO.PWM(in2, freq)

        # デューティ比0を指定しLOWにしてモーターをスタンバイモードに入れる
        self.in1 = GPIO.start(0)
        self.in2 = GPIO.start(0)

    def forward(self, duty: int = 50):
        """モーターを正転させます

        Args:
            duty (int): デューティ比[%]
        """
        self.in1.ChangeDutyCycle(duty)
        self.in2.ChangeDutyCycle(0)

    def backward(self, duty: int = 50):
        """モーターを逆転させます

        Args:
            duty (int): デューティ比[%]
        """
        self.in1.ChangeDutyCycle(0)
        self.in2.ChangeDutyCycle(duty)

    def stop_motor(self):
        """モーターを停止させるメソッド

        モーターは停止から1[ms]経過後にスタンバイモードに入ります。
        """
        # 両方がLOWになる
        self.in1.ChangeDutyCycle(0)
        self.in2.ChangeDutyCycle(0)

    def cleanup(self):
        """モーターの使用後に呼び出すメソッド

        GPIOのクリーンアップを行います。
        DCモーター使用後は必ず呼び出して下さい。
        """
        self.stop_motor()
        self.in1.stop()
        self.in2.stop()
        GPIO.cleanup()
