import BatteryTemp

BT=BatteryTemp.BatteryTemp_result()

if BT == True:
    print("OS errer")

else:
    print("Temperature: %d C" % BT[0])
    print("Humidity: %d %%" % BT[1])
        
