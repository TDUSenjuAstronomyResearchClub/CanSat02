"""単位などの変換をする関数をまとめたモジュールです
"""
import math


def g_to_m_per_s2(data: tuple[float, float, float]) -> tuple[float, float, float]:
    """単位を[g]から[m/s^2]に変換する関数

    Z軸に関しては重力加速度の影響を排除した値を計算し返します。

    Args:
        data (tuple[float, float, float]): 加速度(x, y, z)[g]

    Returns:
        tuple[float, float, float]: 加速度(x, y, z)[m/s^2]
    """
    x = data[0] * 9.80665
    y = data[1] * 9.80665
    z = (data[2] - 1) * 9.80665
    return x, y, z


def raw_ang_rate_to_ang_per_s(data: tuple[float, float, float], range_abs: int) -> tuple[float, ...]:
    """生の角速度データを[°/s]に変換する関数

    生データの範囲はrange_absで変更できます

    Args:
        data (tuple[float, float, float]): 生の角速度データ
        range_abs (int): 角速度センサの測定範囲[°]

    Returns:
        tuple[float, float, float]: 角速度(x, y, z)[°/s]
    """
    # 範囲変換式で±32767を±range_absの中に収めるように変換
    return tuple((x + 32767) / 65534 * 2 * range_abs - range_abs for x in data)


def ut_to_azimuth(x: float, y: float) -> float:
    """3軸の地磁気から方位角[°]を計算する

    地磁気の比から方位角を算出するので地磁気の単位は問いません

    Args:
        x: X軸の地磁気
        y: Y軸の地磁気

    Returns:
        float: 方位角[°]
    """
    # todo: センサーの傾きを考慮した式にする
    # todo: キャリブレーションを追加する
    return math.degrees(math.atan2(y, x))


def acceleration_to_roll(x: float, y: float) -> float:
    """X, Y軸の加速度からロール角[rad]を計算する

    加速度の比からロール角を算出するので加速度の単位は問いません

    Args:
        x (float): X軸の加速度
        y (float): Y軸の加速度

    Returns:
        float: ロール角[rad]
    """
    return math.atan2(y, x)


def acceleration_to_pitch(x: float, y: float, z: float) -> float:
    """X, Y, Z軸の加速度からピッチ角[rad]を計算する

    加速度の比からピッチ角を算出するので加速度の単位は問いません

    Args:
        x (float): X軸の加速度
        y (float): Y軸の加速度
        z (float): Z軸の加速度

    Returns:
        float: ピッチ角[rad]
    """
    roll = acceleration_to_roll(x, y)
    denominator = y * math.sin(roll) + z * math.cos(roll)
    return math.atan2(denominator, -x)


def conv_range(x: float, a: float, b: float, c: float, d: float) -> float:
    """数値xを範囲[a, b]から範囲[c, d]へ変換する関数

    Args:
        x: 変換する数値
        a: 変換元の範囲の最小値
        b: 変換元の範囲の最大値
        c: 変換先の範囲の最小値
        d: 変換先の範囲の最大値

    Returns:
        float: 範囲変換後のx
    """
    return ((x - a) / (b - a)) * (d - c) + c
