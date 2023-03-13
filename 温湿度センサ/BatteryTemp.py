#coding: utf-8
"""
Module Name:<br> 
バッテリー用温湿度センサ<br><br>
Description:<br> 
バッテリー周辺の温度・湿度の測定値をとるプログラム<br><br>
Library:<br>
dht11<br>
githubからライブラリをクローンする。<br>
git clone https://github.com/szazo/DHT11_Python.git を実行する。<br>
環境ができていない場合インストールできないのでsudo apt-get install gitでgitclientをインストールすること。<br>

"""
import RPi.GPIO as GPIO
import dht11

#使用するピン番号に変更すること
pin=14

#GPIOのセットアップ
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(pin)

def BatteryTemp_result():
    """
    温湿度気圧センサ(DHT11)を使って温度、湿度の値を返却するプログラム。

    Returns
    -------
    list
            リスト形式で、[温度(℃)、湿度(%)]を返す。
    bool
            OSErrorが発生した場合はTrueを返す。
    """
    result = instance.read()
    try:
        temp=result.temperature
        hum=result.humidity
        #動作確認用
        #print("Temperature: %d C" % temp)
        #print("Humidity: %d %%" % hum)
        re=[temp,hum]
        return re
    
    except OSError:
        return True
