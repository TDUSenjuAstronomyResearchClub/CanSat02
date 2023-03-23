# -- coding: utf-8 --
import SoilMoisture

#呼び出し表示
result= SoilMoisture.SoilMois_result()
print("Bus Voltage: %.3f V" % result[0])    #電圧
print("Bus Current: %.3f mA" % result[1])   #電流
print("Power: %.3f mW" % result[2])         #電力
print("Shunt voltage: %.3f mV" % result[3]) #シャント電圧