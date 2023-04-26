# 地上局から値を受信する事と、機体から値を送信する事を行う。

import json
import time
import serial
from serial import SerialException

# ポート設定
PORT = '/dev/ttyUSB0'
# 通信レート設定
BAUD_RATE = 9600

# シリアルポート使用判定フラグ(使用中はTrue)
serial_port_flg = False


# ===値送信用関数　引数：json形式で書かれたデータ　戻り値：なし===
def send(filename, json_data):
    # ログ用ファイルをオープン
    f = open(filename, 'a')
    # jsonとして書き込み
    json.dump(json_data, f, indent=4, ensure_ascii=False)
    f.close()

    while True:
        if serial_port_flg == False:  # シリアルポートは使用中ではないか
            # シリアルポート使用判定フラグを使用中にする
            global serial_port_flg
            serial_port_flg = True

            try:
                ser = serial.Serial(PORT, BAUD_RATE)
                # シリアルにjsonを書き込む
                ser.write(json_data.encode('utf-8'))
                ser.close()

                serial_port_flg = False
                break

            except SerialException:  # デバイスが見つからない、または構成できない場合
                serial_port_flg = False
                break  # ここの処理について要件等

        else:
            time.sleep(0.5)

    return


# ===値受信用関数　引数：なし　戻り値：受信値 (例外発生時の戻り値:None ポート使用時の戻り値:port)===
def receive():
    if serial_port_flg == False:
        # シリアルポート使用判定フラグを使用中にする
        global serial_port_flg
        serial_port_flg = True

        try:
            ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
            utf8_string = ser.read_all()  # 機体から値を受け取る
            ser.close()

            serial_port_flg = False
            return utf8_string

        except SerialException:  # デバイスが見つからない、または構成できない場合
            serial_port_flg = False
            return None

    else:
        return "port"
