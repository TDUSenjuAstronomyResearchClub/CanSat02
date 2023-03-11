"""
Module Name: <br>
緯度経度・海抜取得プログラム<br><br>
Description:<br>
 gps.pyから緯度経度を受け取り、ゴールと機体との緒戦距離と方位角を求めるプログラム<br><br>
Notes:<br>
ソースにあるgoal_latitudeとgoal_longitudeの関数にゴールの緯度経度を入力する必要あり<br><br>
Library:<br>
gps.py 同じディレクトリにプログラムを入れる<br><br>


"""

import gps
import math

# 極半径
pole_radius = 6356752.314245  
# 赤道半径                
equator_radius = 6378137.0  

#目標地点の緯度（要設定）
goal_latitude = 0.0
#目標地点の経度（要設定）
goal_longitude = 0.0 

latitude = gps.gps_latitude()
longitude = gps.gps_longitude()

# gpsの緯度経度をラジアンに変換して距離を求める関数　距離(m)を返す
def get_gpsdistance():
    """
    gps.pyから緯度経度を受け取りゴールと機体との直線距離を返すプログラム。

    Returns
    -------
    float
            ゴールと機体との直線距離(m)を返す関数
    """
    # 緯度経度をラジアンに変換
    lat_goal_latitude= math.radians(goal_latitude)
    lon_goal_longitude = math.radians(goal_longitude)
    lon_gps_longitude = math.radians(longitude)
    lat_gps_latitude = math.radians(latitude)

    lat_difference = lat_goal_latitude - lat_gps_latitude       # 緯度差
    lon_difference = lon_goal_longitude - lon_gps_longitude       # 経度差
    lat_average = (lat_goal_latitude + lat_gps_latitude) / 2    # 平均緯度

    e2 = (math.pow(equator_radius, 2) - math.pow(pole_radius, 2)) \
            / math.pow(equator_radius, 2)  # 第一離心率^2
    w = math.sqrt(1- e2 * math.pow(math.sin(lat_average), 2))
    m = equator_radius * (1 - e2) / math.pow(w, 3) # 子午線曲率半径
    n = equator_radius / w                         # 卯酉線曲半径
    distance = math.sqrt(math.pow(m * lat_difference, 2) \
                   + math.pow(n * lon_difference * math.cos(lat_average), 2)) # 距離計測
    return distance/1000000

def get_gpsazimuth():
    """
    gps.pyから緯度経度を受け取り方位角(0から360の間の角度で真北から時計回りに測定される)を求める関数

    Returns
    -------
    float
            ゴールと機体との直線距離(m)を返す関数
    """
    lat1 = math.radians(latitude)
    lat2 = math.radians(goal_latitude)
    diff_lon = math.radians(goal_longitude - longitude)

    y = math.sin(diff_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diff_lon))

    initial_bearing = math.atan2(y, x)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
