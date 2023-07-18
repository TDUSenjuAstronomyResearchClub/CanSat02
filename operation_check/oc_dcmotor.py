import time

from cansatapi import dcmotor

if __name__ == "__main__":
    dcmotor.Wheels.stop()
    dcmotor.Wheels.forward()
    time.sleep(2)

    dcmotor.Wheels.reverse()
    time.sleep(2)

    para = dcmotor.DCMotor(dcmotor.PARACHUTE_FIN, dcmotor.PARACHUTE_RIN)
    para.forward()
    time.sleep(2)
    para.reverse()
    time.sleep(2)
    para.stop()
    para.cleanup()

    dcmotor.Wheels.cleanup()
