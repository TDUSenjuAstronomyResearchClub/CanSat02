"""機体と地上局の通信を行うモジュール
"""
import multiprocessing

from serial import PortNotOpenError
from serial import SerialException

from .message import jsonGenerator, type
from .point_declination import get_lon_lat_decl
from .util.logging import json_log

from cansatapi.gps import *
from cansatapi.nineaxissensor import *
from cansatapi.bme280 import *
from cansatapi.distance import *

# ポート設定
PORT = '/dev/ttyUSB0'
# 通信レート設定
BAUD_RATE = 9600

_send_queue = multiprocessing.Queue()
_receive_queue = multiprocessing.Queue()


def start():
    """XBeeモジュールの待機動作を開始する関数
    """
    c = 0
    while True:
        try:
            while not _send_queue.empty():
                _send()

        except:
            c += 1
            if c >= 5:
                send_sensor_data()  # 約5秒に1度各センサー値の入ったjsonファイルを送信する
                c = 0
            else:
                _receive(1)  # 1秒間待機する


def _send():
    """キューからメッセージを送信する関数
    """
    msg = _send_queue.get_nowait()
    if msg is None:
        return

    retry_c = 0
    while True:
        try:
            ser = serial.Serial(PORT, BAUD_RATE)
            # シリアルにjsonを書き込む
            ser.write(msg.encode('utf-8'))
            ser.write(0x04)  # EOTを末尾に書き込む
            ser.close()
            return

        except PortNotOpenError:
            # 5回リトライに失敗したらエラーを吐く
            retry_c += 1
            if retry_c > 5:
                raise PortNotOpenError
            else:
                time.sleep(0.5)
                continue
        except SerialException:
            raise SerialException  # ここの処理について要件等


def send(msg: str):
    """データ送信用関数

    Args:
        msg (str): 送信するメッセージ
    """
    json_log(msg)  # ローカルにJSONを保存
    _send_queue.put_nowait(msg)


def send_msg(msg: str):
    """任意のメッセージを地上に送信する関数

    Args:
        msg: 任意のメッセージ
    """
    send(jsonGenerator.generate_json(time=time.time(), message=msg))


def send_pic(pic_hex: str):
    """写真データを地上に送信する関数

    Args:
        pic_hex: 写真データ(16進数)
    """
    send(jsonGenerator.generate_json(time=time.time(), camera=pic_hex))


def send_sensor_data():
    """センサーデータをjsonファイルに書き込んで地上に送信する関数（写真・土壌水分・メッセージ以外）
        lps25hb（気圧センサー）、batteryは使用しないため、常時Noneを返すようにしている
    """
    time_now = time.time()

    # gps関係のデータを読み込み
    latitude_longitude_altitude = get_gps_data()

    point = get_lon_lat_decl()
    sample_distance_and_azimuth = calculate_distance_bearing(point[0], point[1], point[4])
    goal_distance_and_azimuth = calculate_distance_bearing(point[2], point[3], point[4])

    # 警告出てるけど、無視して大丈夫な気がする
    distance_data: type.Distance = {
        'sample': sample_distance_and_azimuth[0],
        'goal': goal_distance_and_azimuth[0]
    }

    azimuth_data: type.Azimuth = {
        'sample': sample_distance_and_azimuth[1],
        'goal': goal_distance_and_azimuth[1]
    }

    gps_data: type.Gps = {
        'latitude': latitude_longitude_altitude[0],
        'longitude': latitude_longitude_altitude[1],
        'altitude': latitude_longitude_altitude[2],
        'distance': distance_data,
        'azimuth': azimuth_data
    }

    # 9軸センサー関係のデータを読み込み
    acceleration_tmp = nine_axis_sensor.get_acceleration()
    acceleration_data: type.Acceleration = {
        'x': acceleration_tmp[0],
        'y': acceleration_tmp[1],
        'z': acceleration_tmp[2]
    }

    angular_rate_tmp = nine_axis_sensor.get_angular_rate()
    angular_rate_data: type.AngularVelocity = {
        'x': angular_rate_tmp[0],
        'y': angular_rate_tmp[1],
        'z': angular_rate_tmp[2]
    }

    nine_axis_data: type.NineAxis = {
        'acceleration': acceleration_data,
        'angular_velocity': angular_rate_data,
        'azimuth': nine_axis_sensor.nineget_magnetic_heading()
    }

    bme280_data: type.Bme280 = {
        'temperature': bme280_instance.get_temperature(),
        'humidity': bme280_instance.get_humidity(),
        'pressure': bme280_instance.get_pressure()
    }

    # 超音波距離センサーの距離データを読み込み
    ultrasound_distance = distance_result()

    # lps25hb（気圧センサー）、batteryは使用しないため、常時Noneを返すようにしている
    send(jsonGenerator.generate_json(time=time_now, gps=gps_data, nine_axis=nine_axis_data, bme280=bme280_data,
                                     lps25hb=None, battery=None, distance=ultrasound_distance))


def _receive(sec: float, retry: int = 5, retry_wait: float = 0.5) -> bool:
    """データを地上から受信する関数

    データを受信するとキューにデータを格納します。

    Args:
        retry_wait (float): リトライ時に待機する秒数
        sec (float): 待機する時間
        retry (int): ポートが使用中だった際のリトライ回数

    Returns:
        bool: データを受信したかどうか
    """
    st = time.time()
    ret = 0
    while time.time() - st < sec:
        try:
            ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
            receive_data = ser.readline().removesuffix(bytes(0x04))
            ser.close()
            if len(receive_data) != 0:
                data_utf8 = receive_data.decode("utf-8")
                json_log(data_utf8)  # ロギング
                _receive_queue.put_nowait(data_utf8)  # キューに受信したデータを追加

            return len(receive_data) != 0

        except PortNotOpenError:
            # 5回リトライに失敗したらエラーを吐く
            if ret >= retry:
                raise PortNotOpenError
            else:
                time.sleep(retry_wait)
                continue
        except SerialException:  # デバイスが見つからない、または構成できない場合
            raise SerialException


def get_received_str() -> str:
    """受信した文字列を返す関数

    Returns:
        str: 受信した文字列
    """
    return _receive_queue.get_nowait()
