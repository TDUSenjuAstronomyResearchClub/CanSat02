# -- coding: utf-8 --
"""
Module Name:<br> 
緯度経度・海抜取得プログラム<br><br>
Description:<br> 
gpsモジュールを使って緯度と経度、海抜を取得できるプログラム。動作確認用実行ファイルはgpsTest.py<br><br>
Library:<br>
micropyGPS<br>
サイト(https://github.com/inmcm/micropyGPS)からファイルをダウンロードし、gps.pyが入っているディレクトリに移す<br><br>
serial<br>
「sudo raspi-config」を打ち込み、シリアルを有効にする<br>
「ls /dev/se*」を打ち込み、「/dev/serial0 /dev/serial1」と出力されることを確認<br>
「cat /boot/cmdline.txt」を入力し、エディターで「console=serial0,115200」を削除しリブートすることでcmdline.txtを修正し、serial0をコンソールとして使わないように設定する。<br>
「sudo apt-get install python-serial」を入力し、シリアルモジュールをインストールする<br><br>

"""
import serial
import micropyGPS
import threading
import time


gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                    # 引数はタイムゾーンの時差と出力フォーマット



def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
    try:
        s = serial.Serial('/dev/serial0', 9600, timeout=10)
        s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
        while True:
            sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
            if sentence[0] != '$': # 先頭が'$'でなければ捨てる
                continue
            for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
                gps.update(x)
    except IndexError:
        return True
    except TypeError:
        return True
    

gpsthread = threading.Thread(target=rungps, args=()) # 上の関数を実行するスレッドを生成
gpsthread.daemon = True
gpsthread.start() # スレッドを起動

def gps_latitude(): #緯度
    """
    gpsモジュール（AE-GYSFDMAXB）から緯度を求める関数。

    Returns
    -------
    list
            リスト形式で、[緯度]を返す。
    """
    i=1
    while i<=20:
        if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
            h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
            i=0
            return gps.latitude[0]
        
        i+=1
        time.sleep(1)

def gps_longitude(): #経度
    """
    gpsモジュール（AE-GYSFDMAXB）から経度を求める関数。

    Returns
    -------
    list
            リスト形式で、[経度]を返す。
    """
    i=1
    while i<=20:
        if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
            h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
            i=0
            return gps.longitude[0]
        i+=1
        time.sleep(1)
    
def gps_altitude(): #海抜
    """
    gpsモジュール（AE-GYSFDMAXB）から海抜を求める関数。

    Returns
    -------
    list
            リスト形式で、[海抜(m)]を返す。
    """
    i=1
    while i<=20:
        if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
            h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
            i=0
            return gps.altitude
        i+=1
        time.sleep(1)
        

