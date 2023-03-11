import serial
#from time import strftime
import datetime
import time

# シリアルポートの設定
ser = serial.Serial('COM8', 9600)



def camera():
    now =datetime.datetime.now()
    d = now.strftime('%Y-%m-%d_%H-%M-%S')
    # 受信データを保存するファイル名
    file_name = d + '.jpg'

    # シリアルポートを開く
    #ser.open()

    # バッファと画像の終端文字列（EOF）を定義
    buffer = b""
    eof = b"\xff\xd9" # JPEG形式の場合

    # データ受信開始時刻と現在時刻を取得
    start_time = time.time()
    current_time = start_time

    # データ受信ループ
    while True:
        # シリアルポートから1バイト読み込む
        data = ser.read(1)

        # 読み込んだデータがあればバッファに追加する
        if data:
            buffer += data

            # バッファの末尾がEOFと一致すれば画像受信完了と判断する
            if buffer[-len(eof):] == eof:
                print("Image received.")
                break

    # バッファにデータがあればファイルに書き込む
    if buffer:
        with open(file_name, "wb") as f: # ファイル名とモード（書き込み・バイナリ）
            f.write(buffer)
            print("Image saved.")
    else:
        print("No data.")

    return file_name


    # # シリアルポートから1バイト読み込む
    # img_data = b""
    # while True:
    #     byte = ser.read()
    #     if byte == b"\xff\xd9":
    #         break
    #     img_data += byte

    # with open(file_name, 'wb') as f:
    #     f.write(img_data)
    
    


"""     with open(file_name, "wb") as f:
        data = b''
        while True:
            data = ser.read()
            if data == b'\n':
                break
            file.write(data)

        # 受信したデータを閉じる
        file.close()
        return file_name """


name = camera()
print('file name is ' + name)
exit
    

    


