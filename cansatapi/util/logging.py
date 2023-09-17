"""ロギングモジュール
"""
from __future__ import annotations

import csv
import sys
import time
import json
import datetime

LOG_DIR = "./log/"

FILE_NAME_FMT = '%Y年%m月%d日_%H時%M分%S秒'


class LoggerJSON:
    """ロガーJSONクラス

    JSON形式で地上局に送信するデータのロギングを行います。
    """
    _instance = None
    _is_initialized = False  # 初期化がすでに行われたかどうかを確認するためのフラグ

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # オブジェクトクラスの__new__メソッドを呼び出して、新しいインスタンスを作成

    def __init__(self):
        # シングルトンの初期化は一度のみ行う
        if LoggerJSON._is_initialized:
            return

        # ローカル保存用jsonファイル名を決定
        dt_start = datetime.datetime.now()  # 現在日時を取得する
        file_name = 'send_test' + dt_start.strftime(FILE_NAME_FMT)  # ファイル名を現在時刻にする
        self.log_path = LOG_DIR + file_name + ".json"  # ファイル名を入れる
        LoggerJSON._is_initialized = True

    def log_json(self, json_data: dict):
        """JSONファイルとしてログを残す

        Args:
            json_data (str): JSONデータ
        """
        file = open(self.log_path, 'a')
        # jsonとして書き込み
        json.dump(json_data, file, indent=4, ensure_ascii=False)
        file.close()


# グローバルなインスタンスを作成し、他のモジュールからアクセスできるようにする
log_json_singleton = LoggerJSON()


class LoggerCSV:
    """ロガーCSVクラス

    CSV形式でロギングを行います。
    """

    def __init__(self, file_name: str):
        """ロガーのコンストラクタ

        CSV形式でロギングを行います。

        Args:
            file_name: ログファイルの名前
        """
        self.log_path = LOG_DIR + file_name + ".csv"
        file = open(file_name, 'a')
        writer = csv.writer(file, lineterminator='\n')

        # CSVにインデックスをつける
        writer.writerow(['現在日時', '説明', '内容'])
        file.close()

    def log_csv(self, category: str, content: str | float):
        """ロギング用のメソッド

        Args:
            category (str): ログのカテゴリ
            content (str): ログメッセージ
        """
        file = open(self.log_path, 'a')
        writer = csv.writer(file, lineterminator='\n')
        dt_now = time.time()  # UNIX形式で現在日時を取得する
        log_list = [dt_now, category, content]  # リストに各値を挿入

        writer.writerow(log_list)
        file.close()
        time.sleep(0.1)

    def msg_csv(self, msg: str):
        """メッセージロギング用メソッド

        Args:
            msg (str): メッセージ
        """
        self.log_csv("message", msg)
        print("[Msg]" + msg, file=sys.stdout)

    def error_csv(self, msg: str):
        """エラーロギング用のメソッド

        Args:
            msg (str): エラーメッセージ
        """
        self.log_csv("ERROR", msg)
        print("[Error]" + msg, file=sys.stderr)
