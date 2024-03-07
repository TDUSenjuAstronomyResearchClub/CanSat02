"""ローテーションサーボモーターを制御するモジュール
データシート
https://akizukidenshi.com/download/ds/feetech/fs90r_20201214.pdf
参考資料
https://mickey-happygolucky.hatenablog.com/entry/2019/10/23/114711
"""

import RPi.GPIO as GPIO

PARA_PIN = 23
SOIL_PIN = 24



class Servo:
    def __init__(self, pin_number: int):
        """サーボを初期化するメソッド

        Args:
            pin_number: サーボのピン番号
        """
        self.servo_pin = pin_number
        # GPIOの番号指定モードをBCMに設定
        GPIO.setmode(GPIO.BCM)

        # SERVO_PINを出力モードに設定
        GPIO.setup(self.servo_pin, GPIO.OUT)

        # PWMの設定
        self.servo = GPIO.PWM(self.servo_pin, 50)

        # サーボの制御を開始する
        # PWM周波数:50Hz→周期:20ms　サーボモーター停止のパルス幅1500us
        # 停止時のduty比 = 1500us/(20ms*1000)*100 = 7.5%
        self.servo.start(7.5)

    def rotate_cw_or_ccw(self, duty: float):
        """ローテーションサーボモーターを時計回りか反時計回りに任意の速さで回すメソッド

        Args:
            duty: 3.5~11.5を入力する．7.5以下が時計回り，7.5以上が反時計回り
        """
        self.servo.ChangeDutyCycle(duty)

    def rotate_cw(self):
        """ローテーションサーボモーターを時計回りに最速で回すメソッド
        """
        self.servo.ChangeDutyCycle(3.5)

    def rotate_ccw(self):
        """ローテーションサーボモーターを反時計回りに最速で回すメソッド
        """
        self.servo.ChangeDutyCycle(11.5)

    def rotate_stop(self):
        """ローテーションサーボモーターを止めるメソッド
        """
        self.servo.ChangeDutyCycle(7.1)

    def finish(self):
        """サーボモーターを停止させるメソッド

        サーボモーター使用後は必ず呼び出すこと
        """
        self.servo.stop()
        GPIO.cleanup()
