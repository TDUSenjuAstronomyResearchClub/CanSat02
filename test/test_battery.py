from cansatapi.batteryfuelgauge import BatteryFuelGauge

if __name__ == "__main__":
    battery = BatteryFuelGauge()
    print(battery.get_level())
