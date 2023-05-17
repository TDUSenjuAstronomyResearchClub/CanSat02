"""DCモーター行動制御用モジュール
"""
import time
from cansatapi.dcmotor import DCMotor

# TODO: ピン番号は書き換えること
FIN = 0
RIN = 0

def StraightLine():
    """3秒間前進させるための関数
    """
    def forward(self, duty: int = 80):
        """duty比を80と0にする
        """
        self.fin.ChangeDutyCycle(duty)
        self.rin.ChangeDutyCycle(0)

    time.sleep(3)
    
    def forward(self, duty: int = 0):
        """duty比を0と0にする
        """
        self.fin.ChangeDutyCycle(duty)
        self.rin.ChangeDutyCycle(0)

    time.sleep(1)

    return
