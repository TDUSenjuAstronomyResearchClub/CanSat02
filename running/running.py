import datetime
import time
import threading

from cansatapi import *
from cansatapi.util import logging
from cansatapi.util.logging import Logger


# 本番前に記入
SAMPLE_LON: float = 0.0
SAMPLE_LAT: float = 0.0

GOAL_LON: float = 0.0
GOAL_LAT: float = 0.0

# 共有変数
receive_command = ''

def manual_mode():
    """手動制御を行う関数
    """

def FallJudgement():
    """落下判定をするまで待つ関数
    """
    global receive_command
    while True:
        if receive_command == 'manual':
            #TODO: マニュアルモードの関数を呼び出す
            receive_command = '' #コマンドを初期化

        elif receive_command == 'distination':
            #TODO: 目的地の緯度経度を変更する関数を呼び出す
            receive_command = '' #コマンドを初期化

        else:
            #TODO: 落下開始判定をするプログラムを書く（drop_test.pyを参考に）
            return
        
        time.sleep(1)   #1秒待つ


def LandingJudgement():
    """着地判定をするまで待つ関数
    """
    global receive_command
    while True:
        if receive_command == 'manual':
            #TODO: マニュアルモードの関数を呼び出す
            receive_command = '' #コマンドを初期化

        elif receive_command == 'destination':
            #TODO: 目的地の緯度経度を変更する関数を呼び出す
            receive_command = '' #コマンドを初期化
        
        elif receive_command == 'landing':   #着地判定を手動で行う
            return
            
        else:
            #TODO: 着地判定をするプログラムを書く（drop_test.pyを参考に）
            return
        
        time.sleep(1)   #1秒待つ


def detach_parachute(logger: Logger):
    """パラシュートの切り離しを行います
    """
    para_motor = dcmotor.DCMotor(9, 10)
    logger.msg("パラシュート切り離し開始")
    para_motor.forward()

    time.sleep(10)  # 10秒間巻取り

    para_motor.stop()
    para_motor.cleanup()
    logger.msg("パラシュート切り離し終了")

def angle_adjustment():
    """目的地と機体を一直線にする関数
    """


def go_to_goal():
    """ゴールまで直進する関数
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
    # Xbeeからのデータ受信用スレッド作成
    receive_data = threading.Thread(target=XBee.receive)
    # Xbeeからのデータ受信用スレッドをスタート
    receive_data.start()

    main_logger = Logger("Running" + datetime.datetime.now().strftime(logging.DATETIME_F))
    XBee.send_msg("Start running")

    FallJudgement()
    XBee.send_msg("Detect falling")

    LandingJudgement()
    XBee.send_msg("Landed")

    detach_parachute(main_logger)


if __name__ == "__main__":
    main()  # 実行
