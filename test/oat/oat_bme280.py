from cansatapi.temperature import Temperature

if __name__ == "__main__":
    temp = Temperature()
    result = temp.temperature_result()
    print(f"温度: {result[0]}")
    print(f"湿度: {result[1]}")
    print(f"気圧: {result[2]}")
