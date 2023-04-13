import temperature
import time


def print_data():
    """
    温度センサの動作を確認する関数
    Returns
    -------

    """
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
