from cansatapi.servo import Servo
import sys

if __name__ == "__main__":
    servo = Servo(18)
    while True:
        try:
            servo.rotate_to_angle(90)
            servo.rotate_to_angle(0)
            servo.rotate_to_angle(-90)
            servo.rotate_to_angle(0)
        except KeyboardInterrupt:
            servo.stop()
            sys.exit(0)