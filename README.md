# CanSat用のプログラム

能代宇宙イベントで使用する機体のプログラムです

## APIのインストール方法

まず、`git clone`でこのリポジトリをラズパイにクローンします。

次にクローンしたリポジトリのルートディレクトリ内に移動して

```shell
pip install -r requirements.txt

pip install .
```
を実行します。

このとき、Pythonのバージョンが`3.10`以上でないとエラーとなります。  
Raspbianに標準でインストールされているPythonは3.9.xなので注意してください。  
また、pipのバージョンも最新に上げるのを忘れないでください。

## 機体作成に当たって使用している他のサイト

### SharePoint

<https://tdumedia.sharepoint.com/sites/astronomy>

### API仕様書

<https://tdusenjuastronomyresearchclub.github.io/CanSat02/>

## 使用パーツ

### サーボモーター

MG92B

- データシート(情報少)
  - <https://akizukidenshi.com/download/ds/towerpro/mg92b.pdf>
- Adafruitのページ(詳しく書いてある)
  - <https://www.adafruit.com/product/2307>
- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gM-13228/>

### GPSモジュール

AE-GYSFDMAXB

- 取扱説明書  
  - <https://akizukidenshi.com/download/ds/akizuki/AE-GPS_manual_r1.06_s.pdf>
- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gK-09991/>

### 温湿度・気圧センサー

AE-BME280

- 取扱説明書
  - <https://akizukidenshi.com/download/ds/akizuki/AE-BME280_manu_v1.1.pdf>
- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gK-09421/>

### 電池残量計用IC

MCP3008 

- データシート
  - <https://akizukidenshi.com/download/ds/microchip/mcp3008.pdf>
- スイッチサイエンスのリンク
  - <https://akizukidenshi.com/catalog/g/gI-09485/>

### 9軸センサー

BMX055

- 取扱説明書
  - <https://akizukidenshi.com/download/ds/akizuki/AE-BMX055_20220804.pdf>
- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gK-13010/>

### 土壌水分センサ

Adafruit STEMMA Soil Sensor - I2C CapacitiveMoisture Sensor

- データシート類
  - <https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/downloads>
- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gM-16357/>

### 超音波センサー

HC-SR04

- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gM-11009/>
- 参考にしたサイト
  - <https://s-design-tokyo.com/use-hcsr04/>

### 気圧センサー

AE-LPS25HB

- 取扱説明書
  - <https://akizukidenshi.com/download/ds/akizuki/ae-lps25hb.pdf>
- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gK-13460/>

### 無線機 (XBee)

XB24CZ7WIT-004

- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gM-10072/>

### Xbee USBエクスプローラー

AE-XBEE-USB

- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gK-06188/>

### カメラ

913-2664

- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gM-10518/>

### USB向け降圧型DC-DCコンバータモジュール

- リンク
  - <https://strawberry-linux.com/catalog/items?code=18697>

### バッテリー

Kypom リポバッテリー　1300mA、7.4 V

- リンク
  - <https://www.amazon.co.jp/dp/B017VOKS4U>

### ギアードモーター

RA250060-58Y91

-千石電商のリンク
  ‐<https://www.sengoku.co.jp/mod/sgk_cart/detail.php?code=EEHD-0SE4>

### モータードライバ

BD6231F-E2

- データシート
  - <https://akizukidenshi.com/download/ds/rohm/bd623x-j.pdf>
- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gI-05088/>

### 超小型モータ

F-M2-12133-0

- 千石電商のリンク
  - <https://www.sengoku.co.jp/mod/sgk_cart/detail.php?code=EEHD-04YJ>

### マイクロスイッチ
SS-5GL2

- モノタロウのリンク
  - <https://www.monotaro.com/p/3257/7106/>


### Raspberry Pi 3 Model A+

- 秋月のリンク
  - <https://akizukidenshi.com/catalog/g/gM-14878/>
