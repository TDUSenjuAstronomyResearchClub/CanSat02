"""サーボモーターの動作確認用モジュール
"""
from cansatapi.servo import Servo
import sys
import time

if __name__ == "__main__":
    servo1 = Servo(23)
    servo2 = Servo(24)
    servo3 = Servo(25)

    while True:
        try:
            print("servo1")
            servo1.rotate_to_angle(90)
            servo1.rotate_to_angle(0)
            servo1.rotate_to_angle(-90)
            servo1.rotate_to_angle(0)
            time.sleep(1)

            print("servo2")
            servo2.rotate_to_angle(90)
            servo2.rotate_to_angle(0)
            servo2.rotate_to_angle(-90)
            servo2.rotate_to_angle(0)
            time.sleep(1)

            print("servo3")
            servo3.rotate_to_angle(90)
            servo3.rotate_to_angle(0)
            servo3.rotate_to_angle(-90)
            servo3.rotate_to_angle(0)
            time.sleep(1)

        except KeyboardInterrupt:
            servo1.stop()
            servo2.stop()
            servo3.stop()
            sys.exit(0)
