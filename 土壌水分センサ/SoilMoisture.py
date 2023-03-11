# -- coding: utf-8 --
from ina219 import INA219
from ina219 import DeviceRangeError
import logging

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2
INA219_ADDRESS = 0x40

#値の取得
def SoilMois_result():
    try:
        ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=INA219_ADDRESS, log_level=logging.INFO)
        ina.configure()

        volt = ina.voltage()
        cur = ina.current()
        pow = ina.power()
        svolt = ina.shunt_voltage()
        result = [volt,cur,pow,svolt]
        return result
    
    except OSError:
        return True  #OSerrerが発生したか否かを判断する（Trueが出たらエラーが発生した判定）

