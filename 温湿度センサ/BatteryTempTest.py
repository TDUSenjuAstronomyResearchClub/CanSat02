import BatteryTemp

BT=BatteryTemp.BatteryTemp_result()
print("Temperature: %d C" % BT[0])
print("Humidity: %d %%" % BT[1])

"""
---想定使用用途---
2
バッテリー周辺の温度・湿度の測定値をとる
3
​
4
---主な機能---
5
温度と湿度を測定することができる
6
​
7
---使用方法---
8
BatteryTemp.pyは温湿度気圧センサの値を得て、その値をreturnで返すプログラムになっている
9
＊OSerrorが発生した場合はTrueを返す
10
​
11
動作確認をする際は、BatteryTempTest.pyを実行する
12
BatteryTemp.BatteryTemp_result()で温湿度気圧センサの値を呼び出せる
16
​
18
---ピン番号---
19
センサ側  ：　ラズパイ側
20
5V  :  5Vpin
GPIO  :  （初期設定　14pin)
3pin is not conect : not conect
GND​  :  GNDpin
21
​
22
---必須ライブラリ---
23
​import dht11
githubからライブラリをクローンする。
git clone https://github.com/szazo/DHT11_Python.gitを実行する。
環境ができていない場合インストールできないのでsudo apt-get install gitでgitclientをインストールすること。
24
​
25
---参考にしたサイト---
26
​https://qiita.com/mininobu/items/1ba0223af84be153b850
27
​
28
​
29
---温湿度センサ　DHT11---
30
データシート
31
chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://akizukidenshi.com/download/ds/aosong/DHT11_20180119.pdf
32
秋月のリンク
33
https://akizukidenshi.com/catalog/g/gM-07003/
"""
        