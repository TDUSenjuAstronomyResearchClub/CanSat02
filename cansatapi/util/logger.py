"""ロギングモジュール
"""
from __future__ import annotations

import csv
import sys
import time
import json
from datetime import datetime

LOG_DIR = "./log/"

DATETIME_F = "%Y-%m-%d_%H-%M-%S"


def json_log(json_data: str):
    """JSONファイルとしてログを残す

    Args:
        json_data (str): JSONデータ
    """
    f = open(LOG_DIR + 'send_data_' + datetime.now().strftime(DATETIME_F) + '.json', 'a')
    # jsonとして書き込み
    json.dump(json_data, f, indent=4, ensure_ascii=False)
    f.close()


class Logger:
    """ロガークラス

    CSV形式でロギングを行います。
    """

    def __init__(self, file_name: str):
        """ロガーのコンストラクタ

        CSV形式でロギングを行います。

        Args:
            file_name: ログファイルの名前
        """
        self.log_path = LOG_DIR + datetime.now().strftime(DATETIME_F) + file_name
        file = open(file_name, 'a')
        writer = csv.writer(file, lineterminator='\n')

        # CSVにインデックスをつける
        writer.writerow(['現在日時', '説明', '内容'])
        file.close()

    def log(self, category: str, content: str | float):
        """ロギング用のメソッド

        Args:
            category (str): ログのカテゴリ
            content (str): ログメッセージ
        """
        file = open(self.log_path, 'a')
        writer = csv.writer(file, lineterminator='\n')
        dt_now = datetime.now().strftime(DATETIME_F)  # 現在日時を取得する
        log_list = [dt_now, category, content]  # リストに各値を挿入

        writer.writerow(log_list)
        file.close()
        time.sleep(0.1)

    def msg(self, msg: str):
        """メッセージロギング用メソッド

        Args:
            msg (str): メッセージ
        """
        self.log("message", msg)
        print("[Msg]" + msg, file=sys.stdout)

    def error(self, msg: str):
        """エラーロギング用のメソッド

        Args:
            msg (str): エラーメッセージ
        """
        self.log("ERROR", msg)
        print("[Error]" + msg, file=sys.stderr)
