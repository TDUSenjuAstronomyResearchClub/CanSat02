import Temperature
import time

while True:
    temp = Temperature.Temperature_result()
    
    if temp == True:
        print('OSerrer')

    else:
        print(temp[0])#気温　℃
        print(temp[1])#気圧　hpa 
        print(temp[2])# 湿度 %
        print("---------------------")
    


    time.sleep(1)
