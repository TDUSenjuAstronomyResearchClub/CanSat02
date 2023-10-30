"""dcモーターが止まらなくなった際に動かすプログラム
"""

from cansatapi import *

dcmotor.Wheels.stop()
dcmotor.Wheels.cleanup()
