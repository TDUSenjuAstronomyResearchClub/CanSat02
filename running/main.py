import multiprocessing
import time
import RPi.GPIO as GPIO
from multiprocessing import Process

# from cansatapi import *
from cansatapi.point_declination import SAMPLE_LON, SAMPLE_LAT, GOAL_LON, GOAL_LAT, DECLINATION
from cansatapi.servo import Servo
from cansatapi import dcmotor
from cansatapi import xbee
from cansatapi import gps
from cansatapi import nineaxissensor
from cansatapi import servo
from cansatapi.soil_moisture import soilmoisture


def fall_judgement() -> bool:
    """落下判定を返す関数
    """


def landing_judgement() -> bool:
    """着地判定を返す関数
    """


def detach_parachute():
    """パラシュートの切り離しを行います
    """

    # 機体を前進させる
    dcmotor.Wheels.stop()
    # print("機体を11秒前進させる")
    dcmotor.Wheels.forward()
    # パラシュートを切り離す
    para_servo = Servo(servo.PARA_PIN)
    para_servo.rotate_cw()
    time.sleep(11)
    para_servo.rotate_stop()
    dcmotor.Wheels.stop()


def manual_mode():
    """手動制御を行う関数
    """
    dcmotor.Wheels.stop()
    xbee.send_msg("Manual operation mode: Please send command")
    while True:
        cmd = xbee.get_received_str()
        # print(f"cmd={cmd}")

        if cmd == "forward":
            print("forward mode")
            xbee.send_msg("forward mode")
            print(cmd)
            dcmotor.Wheels.forward()
            time.sleep(6)
            dcmotor.Wheels.stop()
            xbee.send_msg("Manual operation mode: Please send command")

        elif cmd == "reverse":
            print("reverse mode")
            xbee.send_msg("reverse mode")
            dcmotor.Wheels.reverse()
            time.sleep(4)
            dcmotor.Wheels.stop()
            xbee.send_msg("Manual operation mode: Please send command")

        elif cmd == "right":
            print("right mode")
            xbee.send_msg("right mode")
            dcmotor.Wheels.r_pivot_fwd()
            time.sleep(1)
            dcmotor.Wheels.stop()
            xbee.send_msg("Manual operation mode: Please send command")

        elif cmd == "left":
            print("left mode")
            xbee.send_msg("left mode")
            dcmotor.Wheels.l_pivot_fwd()
            time.sleep(1)
            dcmotor.Wheels.stop()
            xbee.send_msg("Manual operation mode: Please send command")

        elif cmd == "soil":
            print("soil mode")
            xbee.send_msg("soil mode")
            soil_moisture()
            xbee.send_msg("Manual operation mode: Please send command")


        # elif cmd == "picture"
        #    TODO:カメラの画像を取得し，地上局に送信するコードを書く（camera.py動確すんでないため未記入．動確担当者りくお）
        #    xbee.send_msg("Manual operation mode: Please send command")

        elif cmd == "end":  # elseにすると文字列がPCから送られてこなかったらcmdがNoneになり，条件が整ってしまうためelse ifにした
            print("end")
            xbee.send_msg("end")
            return

        time.sleep(0.1)



def is_straight(lat: float, lon: float) -> bool:
    """指定された地点と機体が一定の範囲内に収まってたらTrueを返す関数

    Args:
        lat (float): 地点の緯度
        lon (float): 地点の経度
    """
    return gps.calculate_distance_bearing(lat, lon, DECLINATION)[1] - nineaxissensor \
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

    # print(servo.SOIL_PIN)
    soil_servo = Servo(servo.SOIL_PIN)
    soil_servo.rotate_cw()  # センサの差し込み
    time.sleep(0.7)
    soil_servo.rotate_stop()

    for n in range(5):
        time.sleep(2)
        xbee.send_soilmois_data(soilmoisture.get_soil_moisture())  # 土壌水分の測定と送信

    time.sleep(1)
    soil_servo.rotate_ccw()  # センサの収納
    time.sleep(0.6)
    soil_servo.finish()

    return


def sample_collection():
    """サンプルを採取する関数
    """


def main():
    """メインアルゴリズム
    """
    # 受信を開始
    parse_proc = Process(target=xbee.start)
    parse_proc.start()

    global isAuto
    xbee.send_msg("system start")

    # while not fall_judgement():
    #    time.sleep(0.1)
    # xbee.send_msg("落下検知")

    # while not landing_judgement():
    #    time.sleep(0.1)
    # xbee.send_msg("着地")

    while True:
        print("sleep mode")
        received_start = xbee.get_received_str()
        if received_start == "start":
            print("parachute start")
            xbee.send_msg("parachute start")
            detach_parachute()  # パラシュート分離
            break
        else:
            time.sleep(0.1)

    # detach_parachute()  # パラシュート分離

    go_to_sample = True

    while True:
        print("manual or auto")
        # 1行動ごとにループを回す
        received_str = xbee.get_received_str()  # モード指定orマニュアルモードのコマンドが入る

        if received_str == "manual":
            isAuto = False
        elif received_str == "auto":
            isAuto = True
        print("mode select")

        if isAuto:
            print("自立制御開始")
            lat = SAMPLE_LAT if go_to_sample else GOAL_LAT
            lon = SAMPLE_LON if go_to_sample else GOAL_LON

            if is_straight(lat, lon):
                dcmotor.Wheels.forward()  # 方位角が範囲に収まっていれば10秒直進
                time.sleep(10)
                dcmotor.Wheels.stop()
            else:
                angle_adjustment(lat, lon)  # 収まっていなければ調整

            if is_goal() and go_to_sample:
                xbee.send_msg("サンプル地点到達")
                # sample_collection()
                soil_moisture()
                go_to_sample = False
            elif is_goal() and not go_to_sample:
                xbee.send_msg("ゴール到達")
                xbee.send_msg("動作終了")
                break

        elif not isAuto:  # isAutoがFalseの場合動く．手動運転動作確認のため初期値をFalseにしたので設けた．本番で入らない？
            manual_mode()
        else:
            manual_mode()

        break
    parse_proc.terminate()
    GPIO.cleanup()
    return



if __name__ == "__main__":
    isAuto = False  # TODO:手動運転の動作確認のためFalseにしている．本番はTrueにする
    print("プログラムスタート")
    main()
    print("プログラムエンド")
