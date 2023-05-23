"""機体の向きをゴールと一直線にする走行試験用のテストモジュール
"""
import datetime

from cansatapi.util.logging import Logger

def manual_mode():
    """機体をゴールと一直線にする
    """

def angle_adjustment():
    """機体をゴールと一直線にする
    """

def go_to_goal():
    """機体をゴールに向かわせる
    """
    # ログ用ファイルの作成
    dt_start = datetime.datetime.now()  # 現在日時を取得する
    filename = 'angle_adjustment' + dt_start.strftime('%Y年%m月%d日_%H時%M分%S秒') + '.csv'  # ファイル名を現在時刻にする
    Logger.log(filename)

            

if __name__ == "__main__":
    go_to_goal()
