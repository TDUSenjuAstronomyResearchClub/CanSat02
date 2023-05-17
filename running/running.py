# gps.pyからサンプル取得地点の緯度経度値を取得する関数
def get_sample():
    # gps.pyの関数を呼び出してサンプル取得地点の緯度経度値を取得する処理を記述する
    # ここでは、仮の値として示すだけする
    #要追記
    sample_latitude = 35.6789
    sample_longitude = 139.0123
    return sample_latitude, sample_longitude

# SeeValueに渡す緯度経度値を含む関数
def SeeValue():
    # gps.pyからサンプル取得地点の緯度経度値を取得
    sample_latitude, sample_longitude = get_sample()

    # ゴールの緯度経度値を"x,y"形式で設定
    goal_latitude = x
    goal_longitude = y

    # ゴール地点とサンプル取得地点の値を表示
    print("ゴール地点の緯度経度値:", goal_latitude, goal_longitude)
    print("サンプル取得地点の緯度経度値:", sample_latitude, sample_longitude)

    # ゴール地点とサンプル取得地点の値を返す
    #関数を呼び出せば求める値が返ってくる予定
    #ゴールの緯度経度、サンプル取得地点の緯度経度の順で返す
    return goal_latitude, goal_longitude, sample_latitude, sample_longitude

# 関数を呼び出して緯度経度値を表示
result = SeeValue()

# 結果の仮想処理 要削除
print("結果の仮想処理:")
goal_latitude, goal_longitude, sample_latitude, sample_longitude = result
# ここで結果を使った処理を行う
print("ゴール地点の緯度経度値:", goal_latitude, goal_longitude)
print("サンプル取得地点の緯度経度値:", sample_latitude, sample_longitude)