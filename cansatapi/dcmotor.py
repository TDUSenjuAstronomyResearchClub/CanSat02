"""DCモーター制御用モジュール
"""
import RPi.GPIO as GPIO


class DCMotor:
    """DCモーターをドライバを通してPWM制御するクラス
    """

    def __init__(self, fin: int, rin: int, freq: int = 50_000):
        """DCモーターを初期化するメソッド

        Args:
            fin (int): 正転制御用ピン
            rin (int): 逆転制御用ピン
            freq (int): PWMの周波数[Hz]
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(fin, GPIO.OUT)
        GPIO.setup(rin, GPIO.OUT)
        self.fin = GPIO.PWM(fin, freq)
        self.rin = GPIO.PWM(rin, freq)

        self.fin = GPIO.start(0)
        self.rin = GPIO.start(0)

    def forward(self, duty: int = 50):
        """モーターを正転させます

        Args:
            duty (int): デューティ比[%]
        """
        self.fin.ChangeDutyCycle(duty)
        self.rin.ChangeDutyCycle(0)

    def reverse(self, duty: int = 50):
        """モーターを逆転させます

        Args:
            duty (int): デューティ比[%]
        """
        self.fin.ChangeDutyCycle(0)
        self.rin.ChangeDutyCycle(duty)

    def stop(self):
        """モーターを停止させるメソッド
        """
        # 両方がLOWになる
        self.fin.ChangeDutyCycle(0)
        self.rin.ChangeDutyCycle(0)

    def cleanup(self):
        """モーターの使用後に呼び出すメソッド

        GPIOのクリーンアップを行います。
        DCモーター使用後は必ず呼び出して下さい。
        """
        self.stop()
        self.fin.stop()
        self.rin.stop()
        GPIO.cleanup()


class DCMotorController:
    """左右の2個のモーターを同時にコントロールするクラス

    前進するために左右のモーターを同じデューティ比にするときなどに使います。
    初期化する際にそれぞれのモーターのインスタンスを渡してください。
    """

    def __init__(self, r_motor: DCMotor, l_motor: DCMotor):
        self.r_motor = r_motor
        self.l_motor = l_motor

    def cleanup(self):
        """GPIOのクリーンアップを行うメソッド

        インスタンスの使用が終わったら必ず呼び出して下さい。
        """
        self.r_motor.cleanup()
        self.l_motor.cleanup()

    def stop(self):
        """左右のモーターを停止させるメソッド
        """
        self.r_motor.stop()
        self.l_motor.stop()

    def forward(self, duty: int = 50):
        """左右のモーターを正転させるメソッド

        Args:
            duty (int): デューティ比[%]
        """

        self.r_motor.forward(duty)
        self.l_motor.forward(duty)

    def reverse(self, duty: int = 50):
        """左右のモーターを逆転させるメソッド

        Args:
            duty (int): デューティ比[%]
        """

        self.r_motor.reverse(duty)
        self.l_motor.reverse(duty)

    def r_pivot_fwd(self, duty: int = 50):
        """時計回りに右車輪を軸に信地旋回を行うメソッド

        Args:
            duty (int): デューティ比[%]
        """

        self.r_motor.stop()
        self.l_motor.forward(duty)

    def r_pivot_rev(self, duty: int = 50):
        """反時計回りに右車輪を軸に信地旋回を行うメソッド

        Args:
            duty (int): デューティ比[%]
        """

        self.r_motor.stop()
        self.l_motor.reverse(duty)

    def l_pivot_fwd(self, duty: int = 50):
        """反時計回りに左車輪を軸に信地旋回を行うメソッド

        Args:
            duty (int): デューティ比[%]
        """

        self.r_motor.forward(duty)
        self.l_motor.stop()

    def l_pivot_rev(self, duty: int = 50):
        """時計回りに左車輪を軸に信地旋回を行うメソッド

        Args:
            duty (int): デューティ比[%]
        """

        self.r_motor.reverse(duty)
        self.l_motor.stop()

    def r_spin(self, duty: int = 50):
        """時計回りに超信地回転を行うメソッド

        Args:
            duty (int): デューティ比[%]
        """

        self.r_motor.reverse(duty)
        self.l_motor.forward(duty)

    def l_spin(self, duty: int = 50):
        """反時計回りに超信地回転を行うメソッド

        Args:
            duty (int): デューティ比[%]
        """

        self.r_motor.reverse(duty)
        self.l_motor.forward(duty)
