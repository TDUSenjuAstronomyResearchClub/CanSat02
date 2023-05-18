from cansatapi.gps import get_gps_data
# gps.pyからサンプル取得地点の緯度経度値を取得する関数


def get_sample():
    # gps.pyの関数を呼び出してサンプル取得地点の緯度経度値を取得する処理を記述する
    # 取得地点の緯度経度値
    sample_let = []
    sample_let = get_gps_data()
    sample_latitude = sample_let[0]
    sample_longitude = sample_let[1]
    return sample_latitude, sample_longitude

# SeeValueに渡す緯度経度値を含む関数


def SeeValue():
    # gps.pyからサンプル取得地点の緯度経度値を取得
    sample_latitude, sample_longitude = get_sample()
    # ゴール地点の緯度経度を手入力必須
    goal_latitude = 35.6789
    goal_longitude = 139.0123

    # ゴール地点とサンプル取得地点の値を表示
    print("ゴール地点の緯度経度値:", goal_latitude, goal_longitude)
    print("サンプル取得地点の緯度経度値:", sample_latitude, sample_longitude)

    # ゴール地点とサンプル取得地点の値を返す
    # 関数を呼び出せば求める値が返ってくる予定
    # ゴールの緯度経度、サンプル取得地点の緯度経度の順で返す
    return goal_latitude, goal_longitude, sample_latitude, sample_longitude

# 関数を呼び出して緯度経度値を表示


result = SeeValue()

# 結果の仮想処理 要削除
print("結果の仮想処理:")
goal_latitude, goal_longitude, sample_latitude, sample_longitude = result
# ここで結果を使った処理を行う
print("ゴール地点の緯度経度値:", goal_latitude, goal_longitude)
print("サンプル取得地点の緯度経度値:", sample_latitude, sample_longitude)
