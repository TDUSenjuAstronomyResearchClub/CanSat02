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

import queue #追加

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


def manual_mode():
    """手動制御を行う関数

    """

    dcmotor.Wheels.stop()
    xbee.send_msg("Manual operation mode: Please send command")
    while True:
        cmd = xbee.get_received_str()
        # print(f"cmd={cmd}")

        if cmd == "forward":
            # print("forward")
            print(cmd)
            dcmotor.Wheels.forward()
            time.sleep(10)
            dcmotor.Wheels.stop()
            xbee.send_msg("Manual operation mode: Please send command")

        elif cmd == "reverse":
            print("reverse")
            dcmotor.Wheels.reverse()
            time.sleep(10)
            dcmotor.Wheels.stop()
            xbee.send_msg("Manual operation mode: Please send command")

        elif cmd == "right":
            print("right")
            dcmotor.Wheels.r_pivot_fwd()
            time.sleep(10)
            dcmotor.Wheels.stop()
            xbee.send_msg("Manual operation mode: Please send command")

        elif cmd == "left":
            print("left")
            dcmotor.Wheels.l_pivot_fwd()
            time.sleep(10)
            dcmotor.Wheels.stop()
            xbee.send_msg("Manual operation mode: Please send command")

        # elif cmd == "picture"
        #    TODO:カメラの画像を取得し，地上局に送信するコードを書く（camera.py動確すんでないため未記入．動確担当者りくお）
        #    xbee.send_msg("Manual operation mode: Please send command")

        elif cmd == "end":  # elseにすると文字列がPCから送られてこなかったらcmdがNoneになり，条件が整ってしまうためelse ifにした
            print("end")
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


def sample_collection():
    """サンプルを採取する関数
    """
def serial_data(input_queue, mode_pipe):
    while True:
        try:
            received_str = None
            print("manual or auto")
            # 1行動ごとにループを回す
            time.sleep(5)
            # received_str = xbee.get_received_str()  # モード指定orマニュアルモードのコマンドが入る
            # キューから文字列を非ブロッキングで受け取る
            try:
                received_str = input_queue.get(block=False)
            except queue.Empty:
                received_str = None

            print(received_str)
            if received_str == "manual":
                isauto = False
                mode_pipe.send(isauto)
            elif received_str == "auto":
                isauto = True
                mode_pipe.send(isauto)
            else:
                print(f"Unknown command: {received_str}")
            print("mode select")
        except EOFError:
            print("error")
            time.sleep(1)
            pass

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

    detach_parachute()  # パラシュート分離

    go_to_sample = True
    # 受信後の判定開始
    #input_pipe, serial_mode_pipe = multiprocessing.Pipe()
    input_queue = multiprocessing.Queue()
    mode_pipe, main_mode_pipe = multiprocessing.Pipe()
    serial_proc = Process(target=serial_data, args=(input_queue, mode_pipe))
    serial_proc.start()

    try:
        while True:

            """
            print("manual or auto")
            # 1行動ごとにループを回す
            #received_str = xbee.get_received_str()  # モード指定orマニュアルモードのコマンドが入る
            received_str = input()
            print(received_str)
    
            if received_str == "manual":
                isAuto = False
            elif received_str == "auto":
                isAuto = True
            print("mode select")
            """
            isAuto = main_mode_pipe.recv()
            if isAuto:
                print("自立制御開始")
                lat = SAMPLE_LAT if go_to_sample else GOAL_LAT
                lon = SAMPLE_LON if go_to_sample else GOAL_LON
                # lat = float(input("lat = "))
                # lon = float(input("lon = "))

                if is_straight(lat, lon):
                    dcmotor.Wheels.forward()  # 方位角が範囲に収まっていれば10秒直進
                    time.sleep(10)
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

            elif not isAuto:  # isAutoがFalseの場合動く．手動運転動作確認のため初期値をFalseにしたので設けた．本番で入らない？
                manual_mode()
            else:
                manual_mode()

        parse_proc.terminate()
        serial_proc.terminate()
        GPIO.cleanup()

    except KeyboardInterrupt:
        # Ctrl+Cが押された場合の処理
        # プログラムを終了する際の処理
        parse_proc.terminate()
        serial_proc.terminate()
        serial_proc.join()
        parse_proc.join()
        GPIO.cleanup()
        print("プログラムを終了しました.")


if __name__ == "__main__":
    isAuto = False  # TODO:手動運転の動作確認のためFalseにしている．本番はTrueにする
    print("プログラムスタート")
    main()
