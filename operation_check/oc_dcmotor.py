import time

from cansatapi import dcmotor
# import RPi.GPIO as GPIO

if __name__ == "__main__":
    print("デバック:モーターストップ")
    dcmotor.Wheels.stop()
    print("デバック:モーター前進")
    dcmotor.Wheels.forward()
    time.sleep(900)

    print("デバック:モーター後退")
    dcmotor.Wheels.reverse()
    time.sleep(2)

    dcmotor.Wheels.cleanup()
    # GPIO.cleanup()

    print("デバック:右モーターだけ動かす")
    right_motor = dcmotor.DCMotor(dcmotor.R_WHEEL_FIN, dcmotor.R_WHEEL_RIN)
    right_motor.forward()
    time.sleep(2)
    right_motor.reverse()
    time.sleep(2)
    right_motor.stop()
    right_motor.cleanup()

    print("デバック:左モーターだけ動かす")
    left_motor = dcmotor.DCMotor(dcmotor.L_WHEEL_FIN, dcmotor.L_WHEEL_RIN)
    left_motor.forward()
    time.sleep(2)
    left_motor.reverse()
    time.sleep(2)
    left_motor.stop()
    left_motor.cleanup()
