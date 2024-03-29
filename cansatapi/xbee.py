"""機体と地上局の通信を行うモジュール
"""
import multiprocessing
import queue

from serial import PortNotOpenError
from serial import SerialException

from .message import jsonGenerator, type
from .point_declination import get_lon_lat_decl
from .util.logging import LoggerJSON

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
        マルチスレッドを使用する際、新しいプロセスとして動作させる
    """
    c = 0
    while True:
        while _send_queue.empty():
            c += 1
            if c >= 5:
                # print("jsonファイル送信作業開始")
                get_send_sensor_data()  # 約5秒に1度各センサー値の入ったjsonファイルを送信する
                c = 0
                # print("jsonファイル送信作業終了")
            else:
                # print("jsonファイル受信開始")
                _receive(1)  # 1秒間待機する
                # print("jsonファイル送信作業終了")
        _send()


def _send():
    """キューからメッセージを送信する関数
    """
    msg = _send_queue.get_nowait()
    eol = '\n'  # end of line
    if msg is None:
        return

    ser = None
    try:
        ser = serial.Serial(PORT, BAUD_RATE)
    except SerialException:
        pass  # ここでSerialExceptionが発生した場合、serはNoneのままになる

    retry_c = 0
    while True:
        try:
            if ser is not None:
                ser.write(msg.encode('utf-8'))
                ser.write(eol.encode('utf-8'))  # EOLを末尾に書き込む
                return
            else:
                raise SerialException  # ここでSerialExceptionを発生させる

        except (SerialException, OSError) as e:
            # エラーが発生した場合のリトライ処理
            retry_c += 1
            if retry_c > 5:
                print(f"Error: {e}")
                break  # リトライ回数を超えたらループを抜ける
            else:
                time.sleep(0.5)
                try:
                    ser = serial.Serial(PORT, BAUD_RATE)  # 再試行
                except SerialException:
                    pass
        finally:
            if ser is not None:
                ser.close()


def send(msg: str):
    """データをローカルにJSONファイルを保存し、送信用キューに格納する

    Args:
        msg (str): 送信するメッセージ
    """
    log_json = LoggerJSON()
    log_json.log_json(msg)  # ローカルにJSONを保存
    _send_queue.put_nowait(msg)


def send_msg(msg: str):
    """メッセージをjson形式に変換し、送信用キューに格納する関数を呼び出す

    Args:
        msg: 任意のメッセージ
    """
    send(jsonGenerator.generate_json(data_type="only_message_data", time=time.time(), message=msg))
    print(msg)


def send_pic(pic_hex: str):
    """写真データをjson形式に変換し、送信用キューに格納する関数を呼び出す

    Args:
        pic_hex: 写真データ(16進数)
    """
    print("debug comment:action send_pic")
    send(jsonGenerator.generate_json(data_type="only_picture_data", time=time.time(), camera=pic_hex))


def send_soilmois_data(moisture: float):
    """土壌水分量データをjson形式に変換し、送信用キューに格納する関数を呼び出す

    Args:
        moisture: 土壌水分量
    """
    send(jsonGenerator.generate_json(data_type="only_soil_data", time=time.time(), soil_moisture=moisture))


def get_send_sensor_data():
    """ラズパイから各種センサの値を一定時間ごとに取得し、json形式に変換・送信用キューに格納する関数を呼び出す

        土壌水分・カメラ・気圧センサ(機体に載せていない）・バッテリー残量計（機体に載せていない）以外を取得する
    """
    # ここで初期化することで、例外処理が起きた時に初期値でjson形式で書き込みができる
    latitude_longitude_altitude = (0.0, 0.0, 0.0)
    sample_distance_and_azimuth = (0.0, 0.0)
    goal_distance_and_azimuth = (0.0, 0.0)
    acceleration_tmp = (0.0, 0.0, 0.0)
    angular_rate_tmp = (0.0, 0.0, 0.0)
    azimuth_tmp = 0.0
    temperature_tmp = 0.0
    humidity_tmp = 0.0
    pressure_tmp = 0.0

    time_now = time.time()
    point = get_lon_lat_decl()  # サンプル採取地点とゴール地点の緯度経度・磁気偏角値を取得

    try:
        # gps関係のデータを読み込み
        latitude_longitude_altitude = get_gps_data()
        sample_distance_and_azimuth = calculate_distance_bearing(point[0], point[1], point[4])
        goal_distance_and_azimuth = calculate_distance_bearing(point[2], point[3], point[4])
    except SerialException:
        pass

    try:
        # 9軸センサー関係のデータを読み込み
        acceleration_tmp = nine_axis_sensor.get_acceleration()
        angular_rate_tmp = nine_axis_sensor.get_angular_rate()
        azimuth_tmp = nine_axis_sensor.get_magnetic_heading()

        # 温湿度気圧センサー関係のデータを読み込み
        temperature_tmp = bme280_instance.get_temperature()
        humidity_tmp = bme280_instance.get_humidity()
        pressure_tmp = bme280_instance.get_pressure()
    except OSError:
        pass

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

    acceleration_data: type.Acceleration = {
        'x': acceleration_tmp[0],
        'y': acceleration_tmp[1],
        'z': acceleration_tmp[2]
    }

    angular_rate_data: type.AngularVelocity = {
        'x': angular_rate_tmp[0],
        'y': angular_rate_tmp[1],
        'z': angular_rate_tmp[2]
    }

    nine_axis_data: type.NineAxis = {
        'acceleration': acceleration_data,
        'angular_velocity': angular_rate_data,
        'azimuth': azimuth_tmp
    }

    bme280_data: type.Bme280 = {
        'temperature': temperature_tmp,
        'humidity': humidity_tmp,
        'pressure': pressure_tmp
    }

    send(jsonGenerator.generate_json(data_type="only_sensor_data", time=time_now, gps=gps_data,
                                     nine_axis=nine_axis_data, bme280=bme280_data))


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
    ser = None
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
    except SerialException:
        pass  # ここでSerialExceptionが発生した場合、serはNoneのままになる

    while time.time() - st < sec:
        try:
            if ser is not None:
                receive_data = ser.readline().removesuffix(b'\n')
                if len(receive_data) != 0:
                    data_utf8 = receive_data.decode("utf-8")
                    _receive_queue.put_nowait(data_utf8)  # キューに受信したデータを追加
                    return True
            else:
                raise SerialException  # ここでSerialExceptionを発生させる

        except (SerialException, OSError) as e:
            # エラーが発生した場合のリトライ処理
            if ret >= retry:
                print(f"Error: {e}")
                break  # リトライ回数を超えたらループを抜ける
            else:
                time.sleep(retry_wait)
                try:
                    ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)  # 再試行
                except SerialException:
                    pass
        finally:
            if ser is not None:
                ser.close()
    return False


def get_received_str() -> str:
    """受信した文字列を返す関数
        受信した値が入っているキューから値を取り出す

    Returns:
        str: 受信した文字列
    """
    try:
        # print("debug comment:action get_received_str")
        return _receive_queue.get_nowait()
    except queue.Empty:  # 何も受信していない場合はNoneを返す
        # print("debug comment:return None")
        return None
