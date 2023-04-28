import sys
import time

from cansatapi.temperature import Temperature

if __name__ == "__main__":
    temp = Temperature()
    while True:
        try:
            result = temp.temperature_result()
            print(f"温度: {result[0]}")
            print(f"湿度: {result[1]}")
            print(f"気圧: {result[2]}")
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)

