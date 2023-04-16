from CanSatAPI import temperature
import time


if __name__ == "__main__":
    while True:
        temp = temperature.temperature_result()

        if temp:
            print('OSError')
        else:
            print(temp[0])  # 気温 ℃
            print(temp[1])  # 気圧 hpa
            print(temp[2])  # 湿度 %
            print("---------------------")

        time.sleep(1)
