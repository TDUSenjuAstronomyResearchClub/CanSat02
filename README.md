# CanSat機体プログラム

能代宇宙イベントで使用する機体のプログラムです

## micropyGPSの導入(sdカードを変えたら実行する)
cansatapiディレクトリに移動して，以下のコマンドを実行する．
```shell
git clone https://github.com/inmcm/micropyGPS
cd micropyGPS
python setup.py install
cd ..
cp micropyGPS/micropyGPS.py .
```

## APIのインストール方法

まず、`git clone`でこのリポジトリをラズパイにクローンします。

次にクローンしたリポジトリのルートディレクトリ内に移動して

```shell
pip install -r requirements.txt

pip install .
```
を実行します。

このとき、Pythonのバージョンが`3.9`以上でないとエラーとなります。  

## 機体作成に当たって使用している他のサイト

### SharePoint

<https://tdumedia.sharepoint.com/sites/astronomy>

### API仕様書

<https://tdusenjuastronomyresearchclub.github.io/CanSat02/>

