"""単位などの変換をする関数をまとめたモジュールです
"""
import math


def g_to_m_per_s2(data: list[float]) -> list[float]:
    """単位を[g]から[m/s^2]に変換する関数

    Args:
        data (list[float]): 加速度(x, y, z)[g]

    Returns:
        list[float]: 加速度(x, y, z)[m/s^2]
    """
    return list(map(lambda x: x * 9.80665, data))


def raw_ang_rate_to_ang_per_s(data: list[float], range_abs: int) -> list[float]:
    """生の角速度データを[°/s]に変換する関数

    生データの範囲はrange_absで変更できます

    Args:
        data (list[float]): 生の角速度データ
        range_abs (int): 角速度センサの測定範囲[°]

    Returns:
        list[float]: 角速度(x, y, z)[°/s]
    """
    # 範囲変換式で±32767を±range_absの中に収めるように変換
    return list(map(lambda x: (x + 32767) / 65534 * 2 * range_abs - range_abs, data))


def ut_to_azimuth(x: float, y: float) -> float:
    """3軸の地磁気[μT]から方位角[°]を計算する

    Args:
        x: X軸の地磁気[μT]
        y: Y軸の地磁気[μT]

    Returns:
        float: 方位角[°]
    """
    # todo: センサーの傾きを考慮した式にする
    # todo: キャリブレーションを追加する
    return math.atan(x/y)


def acceleration_to_roll(x: float, y: float) -> float:
    """X, Y軸の加速度[m/s^2]からロール角[rad]を計算する

    Args:
        x (float): X軸の加速度[m/s^2]
        y (float): Y軸の加速度[m/s^2]

    Returns:
        float: ロール角[rad]
    """
    return math.atan(y / x)


def acceleration_to_pitch(x: float, y: float, z: float) -> float:
    """X, Y, Z軸の加速度[m/s^2]からピッチ角[rad]を計算する

    Args:
        x (float): X軸の加速度[m/s^2]
        y (float): Y軸の加速度[m/s^2]
        z (float): Z軸の加速度[m/s^2]

    Returns:
        float: ピッチ角[rad]
    """
    roll = acceleration_to_roll(x, y)
    denominator = y * math.sin(roll) + z * math.cos(roll)
    return math.atan(-x / denominator)