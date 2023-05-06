"""ロギングモジュール
"""
import csv
import sys
import time
import datetime


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
        self.file_name = file_name
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
        file = open(self.file_name, 'a')
        writer = csv.writer(file, lineterminator='\n')
        dt_now = datetime.datetime.now()  # 現在日時を取得する
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