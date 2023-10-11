import time

from cansatapi import dcmotor
# import RPi.GPIO as GPIO

if __name__ == "__main__":
    print("デバック:モーターストップ")
    dcmotor.Wheels.stop()
    print("デバック:モーター前進")
    dcmotor.Wheels.forward()
    time.sleep(2)

    print("デバック:モーター後退")
    dcmotor.Wheels.reverse()
    time.sleep(2)

    dcmotor.Wheels.cleanup()
    # GPIO.cleanup()
