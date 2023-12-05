import time

from cansatapi.nineaxissensor import *

if __name__ == "__main__":
    print('CanSat02-Nine Axis Sensor Test Program')
    print('9軸センサの検証を開始します。')
    print('実行前に次の各項目についてチェックしてください。')
    print('RaspberryPi-CanSat02拡張ボードがGPIOに適切に接続されているか')
    print('RaspberryPi-CanSat02拡張ボード上に9軸センサが正しい向きで接続されているか')
    print('9軸センサのモジュール上のジャンパの状態が次の状態であること')
    print('加速度計のアドレス・・・' + str(ACCL_ADDR))
    print('ジャイロセンサーのアドレス・・・' + str(GYRO_ADDR))
    print('磁気コンパスのアドレス・・・' + str(MAG_ADDR))
    keyInput = input('以上について確認の上、実行を続行しますか？？[Y/N]')
    if (keyInput == 'N') or (keyInput == 'n'):
        print('実行を中断しました。')
        exit(-1)

    print('検証を開始します・・・')

    print('9軸センサのインスタンスを生成しています・・・')

    Obj = NineAxisSensor()

    # print('get_accelaration関数を実行します・・・')
    # for i in range(60):
    #     data = Obj.get_acceleration()
    #     first = "{:.4f}".format(data[0])
    #     second = "{:.4f}".format(data[1])
    #     third = "{:.4f}".format(data[2])
    #     print("\r" + str(first) + "," + str(second) + "," + str(third), end="")
    #     time.sleep(1)
    #
    # print('get_angular_rate関数を実行します・・・')
    # for i in range(60):
    #     print("\r" + str(Obj.get_angular_rate()), end="")
    #     time.sleep(1)

    print('get_magnetic_heading関数を実行します・・・')
    for i in range(60):
        print("\r" + str(i) + "回目：" + str(Obj.get_magnetic_heading()), end="")
        time.sleep(1)
    print("\n")

    print('すべての関数の実行が完了しました。')


