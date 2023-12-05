import time
from multiprocessing import Process

from cansatapi import *
from cansatapi.point_declination import SAMPLE_LON, SAMPLE_LAT, GOAL_LON, GOAL_LAT, DECLINATION
from cansatapi.servo import Servo


def manual_mode(cmd: str):
    """手動制御を行う関数

    Args:
        cmd(str): コマンド文字列
    """
    if cmd == "forward":
        dcmotor.Wheels.forward()
    elif cmd == "reverse":
        dcmotor.Wheels.reverse()
    elif cmd == "right":
        dcmotor.Wheels.r_pivot_fwd()
    elif cmd == "left":
        dcmotor.Wheels.l_pivot_fwd()

    time.sleep(3)
    dcmotor.Wheels.stop()


def fall_judgement() -> bool:
    """落下判定を返す関数
    """


def landing_judgement() -> bool:
    """着地判定を返す関数
    """


def detach_parachute():
    """パラシュートの切り離しを行います
    """
    print(servo.PARA_PIN)
    para_servo = Servo(servo.PARA_PIN)
    para_servo.rotate_cw()
    time.sleep(10)
    para_servo.rotate_stop()

    # 機体を前進させる
    dcmotor.Wheels.stop()
    print("機体を20秒前進させる")
    dcmotor.Wheels.forward()
    time.sleep(20)
    dcmotor.Wheels.stop()
    dcmotor.Wheels.cleanup()


def is_straight(lat: float, lon: float) -> bool:
    """指定された地点と機体が一定の範囲内に収まってたらTrueを返す関数

    Args:
        lat (float): 地点の緯度
        lon (float): 地点の経度
    """
    return gps.calculate_distance_bearing(lat, lon, DECLINATION)[0] - nineaxissensor \
        .nine_axis_sensor.get_magnetic_heading() < 30  # todo: ここの値は要確認


def angle_adjustment(lat: float, lon: float):
    """目的地と機体を一直線にする関数

    Args:
        lat (float): 地点の緯度
        lon (float): 地点の経度
    """
    gps_temp = gps.calculate_distance_bearing(lat, lon, DECLINATION)
    difference = gps_temp[1] - nineaxissensor.nine_axis_sensor.get_magnetic_heading()
    if difference >= 0:
        dcmotor.Wheels.r_pivot_fwd()
    else:
        dcmotor.Wheels.l_pivot_fwd()

    return


def is_goal() -> bool:
    """gps.calculate_distance_bearingの距離をもとにゴールについたか判定する関数
    """


def soil_moisture():
    """土壌水分量を測定する関数
    """


def sample_collection():
    """サンプルを採取する関数
    """


def main():
    """メインアルゴリズム
    """
    global isAuto

    # 受信を開始
    # parse_proc = Process(target=xbee.start)
    # parse_proc.start()

    xbee.send_msg("走行開始")

    # while not fall_judgement():
    #    time.sleep(0.1)

    #xbee.send_msg("落下検知")

    #while not landing_judgement():
    #    time.sleep(0.1)

    #xbee.send_msg("着地")
    detach_parachute()


"""
    go_to_sample = True
    while True:
        # 1行動ごとにループを回す
        received_str = xbee.get_received_str()  # モード指定orマニュアルモードのコマンドが入る
        if received_str == "manual":
            isAuto = False
        elif received_str == "auto":
            isAuto = True

        if isAuto:
            lat = SAMPLE_LAT if go_to_sample else GOAL_LAT
            lon = SAMPLE_LON if go_to_sample else GOAL_LON

            if is_straight(lat, lon):
                dcmotor.Wheels.forward()  # 方位角が範囲に収まっていれば3秒直進
                time.sleep(3)
                dcmotor.Wheels.stop()
            else:
                angle_adjustment(lat, lon)  # 収まっていなければ調整

            if is_goal() and go_to_sample:
                xbee.send_msg("サンプル地点到達")
                sample_collection()
                soil_moisture()
                go_to_sample = False
            elif is_goal() and not go_to_sample:
                xbee.send_msg("ゴール到達")
                xbee.send_msg("動作終了")
                break
        else:
            manual_mode(received_str)

    parse_proc.terminate()
"""

if __name__ == "__main__":
    isAuto = True
    main()  # 実行
