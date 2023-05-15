
#3秒間前進
def StraightLine():

    #duty比を80と0にする
    set_motor_duty(80, 0)

    time.sleep(3)

    #duty比を0と0にする
    set_motor_duty(0, 0)

    time.sleep(1)

    return

