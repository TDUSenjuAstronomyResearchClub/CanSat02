# -- coding: utf-8 --
"""
Module Name:<br> 
電流値取得プログラム<br><br>
Description:<br> 
電流センサを使って電圧、電流、電力、シャント電圧の値を取得できるプログラム。動作確認用実行ファイルはSoilMoistureTest.py<br><br>
Library:<br>
from ina219 import INA219とfrom ina219 import DeviceRangeError<br>
「sudo pip3 install pi-ina219」でダウンロードする<br><br>
"""
from ina219 import INA219
from ina219 import DeviceRangeError
import logging

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2
INA219_ADDRESS = 0x40

#値の取得
def SoilMois_result():
    """
    電流センサ(INA219)を使って電圧、電流、電力、シャント電圧の値を返却するプログラム。

    Returns
    -------
    list
            リスト形式で、[電圧（V）、電流（mA）、電力（mW）、シャント電圧（V）]を返す。
    bool
            OSErrorが発生した場合はTrueを返す。
    """
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

