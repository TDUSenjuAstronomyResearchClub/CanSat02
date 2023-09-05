import time

from cansatapi import dcmotor

if __name__ == "__main__":
    dcmotor.Wheels.stop()
    print("wheels stop")
    dcmotor.Wheels.forward()
    print("wheels forward")
    time.sleep(2)

    dcmotor.Wheels.reverse()
    print("wheels reverse")
    time.sleep(2)

    para = dcmotor.DCMotor(dcmotor.PARACHUTE_FIN, dcmotor.PARACHUTE_RIN)
    para.forward()
    print("para motor forward")
    time.sleep(2)
    para.reverse()
    print("para motor reverse")
    time.sleep(2)
    para.stop()
    print("para motor stop")
    para.cleanup()

    dcmotor.Wheels.cleanup()
