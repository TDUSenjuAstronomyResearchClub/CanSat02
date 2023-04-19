"""加速度・角速度・方位角を求めるモジュール

使用しているライブラリ:
    smbus2
"""

import math

import smbus2

from . import gps

# アドレスはデータシートのp.145に記載
# 回路によってアドレスが変わるのでコメントアウトしておきます
# 詳しくは説明書 https://akizukidenshi.com/download/ds/akizuki/AE-BMX055_20220804.pdf を参照
# データシートp.145のTable 64にも記載あり

# 加速度計のアドレス
ACCL_ADDR = 0x18
# ACCL_ADDR = 0x19

# ジャイロのアドレス
GYRO_ADDR = 0x68
# GYRO_ADDR = 0x69

# 磁気コンパスのアドレス
MAG_ADDR = 0x10


# MAG_ADDR = 0x11
# MAG_ADDR = 0x12
# MAG_ADDR = 0x13

def conv_g_to_m_per_s2(data: list[float]) -> list[float]:
    """単位を[g]から[m/s^2]に変換する関数

    Args:
        data (list[float]): 加速度(x, y, z)[g]

    Returns:
        list[float]: 加速度(x, y, z)[m/s^2]
    """
    return list(map(lambda x: x * 9.80665, data))


def conv_raw_ang_rate_to_ang_per_s(data: list[float], range_abs: int) -> list[float]:
    """生の角速度データを[°/s]に変換する関数

    生データの範囲はrange_absで変更できます

    Args:
        data: 生の角速度データ
        range_abs: 角速度センサの測定範囲[°]

    Returns:
        list[float]: 角速度(x, y, z)[°/s]
    """
    # 範囲変換式で±32767を±range_absの中に収めるように変換
    return list(map(lambda x: (x + 32767) / 65534 * 2 * range_abs - range_abs, data))


class NineAxisSensor:
    """BMX055センサを制御し、加速度・角速度・方位角を求めるクラス

    データシート: https://akizukidenshi.com/download/ds/bosch/BST-BMX055-DS000.pdf
    """

    def __init__(self, declination: float = 0):
        """BMX055センサを初期化する

        Args:
            declination (float): 地磁気偏角（単位：度）。省略時はゼロを指定する。
        """
        self.bus = smbus2.SMBus(1)

        # 加速度計の設定
        # PMU_RANGEレジスタに加速度の測定範囲を設定
        # 0b0101 = ±4g
        self.bus.write_byte_data(ACCL_ADDR, 0x0F, 0b0101)

        # PMU_BWレジスタにデータフィルターの帯域幅を設定
        # 恐らくノイズ除去用
        # 0b1000 = 7.81Hz
        self.bus.write_byte_data(ACCL_ADDR, 0x10, 0b1000)

        # PMU_LPWレジスタに主電源モードと低電力時スリープ時間を設定
        # 0x00 = NORMAL mode, sleep duration = 0.5ms
        self.bus.write_byte_data(ACCL_ADDR, 0x11, 0x00)

        # ジャイロの設定
        # RANGEレジスタに角速度の測定範囲設定
        # 測定範囲を変更したらget_angular_rateの測定範囲も変更すること
        # 0b0010 = ±500°/s
        self.bus.write_byte_data(GYRO_ADDR, 0x0F, 0b0010)

        # BWレジスタにアウトプットのレートとフィルター帯域幅を設定
        # 0b0111 = レート 100Hz, フィルタ帯域幅 32Hz
        self.bus.write_byte_data(GYRO_ADDR, 0x10, 0b0111)

        # LPM1レジスタに主電源モードと低電力時スリープ時間を設定
        self.bus.write_byte_data(GYRO_ADDR, 0x11, 0x00)

        # 磁気コンパスの設定
        # MAGレジスタに電源管理・ソフトリセット・SPIインターフェースモードを設定
        # 0x83 = 0b1000_0011 = Soft Reset
        self.bus.write_byte_data(MAG_ADDR, 0x4B, 0x83)

        # MAGレジスタに実行モードとアウトプットのレートを設定
        # 0x00 = Normal mode, レート 10Hz
        self.bus.write_byte_data(MAG_ADDR, 0x4C, 0x00)

        # MAGレジスタに割り込みとどの軸を有効にするかの設定をする
        # 0x84 = DRDY pinをhighにする(読みだし準備が完了したことを通知する)
        self.bus.write_byte_data(MAG_ADDR, 0x4E, 0x84)

        # MAGレジスタにx, y軸に対する反復の回数を設定する
        # 0x04 = 9回
        self.bus.write_byte_data(0x10, 0x51, 0x04)

        # MAGレジスタにz軸に対する反復の回数を設定する
        # 0x0F = 15回
        self.bus.write_byte_data(0x10, 0x52, 0x0F)

        self.declination = declination

    def get_acceleration(self) -> list[float]:
        """加速度[m/s^2]を取得する

        Returns:
            list[float]: 加速度（x, y, z）（単位:m/s^2）

        Raises:
            OSError: I2C通信が正常に行えなかった際に発生
        """
        return conv_g_to_m_per_s2(self.get_acceleration())

    def __get_acceleration(self) -> list[float]:
        """加速度[g]を取得する

        Returns:
            list[float]: 加速度(x, y, z)[g]

        Raises:
            OSError: I2C通信が正常に行えなかった際に発生
        """
        # レジスタから値を読む
        raw_accl_x = self.bus.read_i2c_block_data(ACCL_ADDR, 0x02, 6)
        raw_accl_y = self.bus.read_i2c_block_data(ACCL_ADDR, 0x04, 2)
        raw_accl_z = self.bus.read_i2c_block_data(ACCL_ADDR, 0x06, 2)

        # データを12bitsに変換
        accl_x = ((raw_accl_x[1] * 256) + (raw_accl_x[0] & 0xF0)) / 16
        if accl_x > 2047:
            accl_x -= 4096
        accl_y = ((raw_accl_y[1] * 256) + (raw_accl_y[0] & 0xF0)) / 16
        if accl_y > 2047:
            accl_y -= 4096
        accl_z = ((raw_accl_z[1] * 256) + (raw_accl_z[0] & 0xF0)) / 16
        if accl_z > 2047:
            accl_z -= 4096

        return [accl_x, accl_y, accl_z]

    def get_angular_rate(self) -> list[float]:
        """角速度を取得する

        Returns:
            list[float]: 角速度（x, y, z）（単位:rad/s）
        
        Raises:
            OSError: I2C通信が正常に行えなかった際に発生
        """
        # 測定範囲は±500°を指定
        return conv_raw_ang_rate_to_ang_per_s(self.__get_angular_rate(), 500)

    def __get_angular_rate(self) -> list[float]:
        """生の角速度を取得する

        Returns:
            list[float]: 生の角速度データ (x, y, z)
        """
        # レジスタから値を読む
        raw_ang_rate = self.bus.read_i2c_block_data(GYRO_ADDR, 0x02, 6)
        # ±32767の範囲内に収まるように値を加工
        return list(map(lambda x: x - 65536 if x > 32767 else x, raw_ang_rate))

    def get_magnetic_heading(self) -> float:
        """地磁気センサから方位角を計算する

        Returns:
            float: 方位角（単位：度）

        Raises:
            OSError: I2C通信が正常に行えなかった際に発生
        """
        raw_mag = self.bmx055.get_mag_data()
        gps_date = gps.get_gps_data()

        # 地磁気偏角を適用する
        declination = self.calculate_declination(gps_date[0], gps_date[1])
        heading = math.atan2(raw_mag[1], raw_mag[0]) + math.radians(declination)

        # 方位角を0から360度の範囲にする
        heading = math.degrees(heading)
        if heading < 0:
            heading += 360.0

        return heading
