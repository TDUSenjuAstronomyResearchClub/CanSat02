from cansatapi.nineaxissensor import NineAxisSensor

if __name__ == "__main__":
    nineaxis = NineAxisSensor()
    while True:
        acc = nineaxis.get_acceleration()
        print(f'加速度 X: {acc[0]}, Y: {acc[1]}, Z: {acc[2]}')

        ang_rate = nineaxis.get_acceleration()
        print(f'角速度 X: {ang_rate[0]}, Y: {ang_rate[1]}, Z: {ang_rate[2]}')

        heading = nineaxis.get_magnetic_heading()
        print(f'方位角: {heading}')
