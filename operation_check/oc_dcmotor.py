import time

from cansatapi import dcmotor

if __name__ == "__main__":
    dcmotor.Wheels.stop()
    dcmotor.Wheels.forward()
    time.sleep(2)

    dcmotor.Wheels.reverse()
    time.sleep(2)

    dcmotor.Wheels.cleanup()
