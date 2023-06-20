"""加速度・角速度・方位角を求めるモジュール

使用しているライブラリ:
    smbus2
"""

import smbus2

from .util import convert

# アドレスはデータシートのp.145に記載
# 回路によってアドレスが変わるのでコメントアウトしておきます
# 詳しくは説明書 https://akizukidenshi.com/download/ds/akizuki/AE-BMX055_20220804.pdf を参照
# データシートp.145のTable 64にも記載あり

# 加速度計のアドレス
# ACCL_ADDR = 0x18
ACCL_ADDR = 0x19

# ジャイロのアドレス
# GYRO_ADDR = 0x68
GYRO_ADDR = 0x69

# 磁気コンパスのアドレス
# MAG_ADDR = 0x10
# MAG_ADDR = 0x11
# MAG_ADDR = 0x12
MAG_ADDR = 0x13


class NineAxisSensor:
    """BMX055センサを制御し、加速度・角速度・方位角を求めるクラス

    データシート: https://akizukidenshi.com/download/ds/bosch/BST-BMX055-DS000.pdf
    """

    def __init__(self):
        """BMX055センサを初期化する
        """
        self.bus = smbus2.SMBus(1)

        # 加速度計の設定
        # PMU_RANGEレジスタに加速度の測定範囲を設定
        # 0b0101 = ±4g
        self.bus.write_byte_data(ACCL_ADDR, 0x0F, 0b0101)

        # PMU_BWレジスタにローパスフィルターのカットオフ周波数を設定
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

        # BWレジスタにアウトプットのレートとローパスフィルターのカットオフ周波数を設定
        # 0b0111 = レート 100Hz, カットオフ周波数 32Hz
        self.bus.write_byte_data(GYRO_ADDR, 0x10, 0b0111)

        # LPM1レジスタに主電源モードと低電力時スリープ時間を設定
        self.bus.write_byte_data(GYRO_ADDR, 0x11, 0x00)

        # 磁気コンパスの設定
        # MAGレジスタに実行モードとアウトプットのレートを設定
        # 0x00 = Normal mode, レート 10Hz
        self.bus.write_byte_data(MAG_ADDR, 0x4C, 0x00)

        # MAGレジスタに割り込みとどの軸を有効にするかの設定をする
        # 0x84 = DRDY pinをhighにする(読みだし準備が完了したことを通知する)
        self.bus.write_byte_data(MAG_ADDR, 0x4E, 0x84)

        # MAGレジスタにx, y軸に対する反復の回数を設定する
        # 0x04 = 9回
        self.bus.write_byte_data(MAG_ADDR, 0x51, 0x04)

        # MAGレジスタにz軸に対する反復の回数を設定する
        # 0x0F = 15回
        self.bus.write_byte_data(MAG_ADDR, 0x52, 0x0F)

    def get_acceleration(self) -> tuple[float, float, float]:
        """加速度[m/s^2]を取得する

        Returns:
            tuple[float, float, float]: 加速度（x, y, z）（単位:m/s^2）

        Raises:
            OSError: I2C通信が正常に行えなかった際に発生
        """
        return convert.g_to_m_per_s2(self.__get_acceleration())

    def __get_acceleration(self) -> tuple[float, float, float]:
        """加速度[g]を取得する

        Returns:
            tuple[float, float, float]: 加速度(x, y, z)[g]

        Raises:
            OSError: I2C通信が正常に行えなかった際に発生
        """
        # レジスタから値を読む
        raw_accl_x = self.bus.read_i2c_block_data(ACCL_ADDR, 0x02, 2)
        raw_accl_y = self.bus.read_i2c_block_data(ACCL_ADDR, 0x04, 2)
        raw_accl_z = self.bus.read_i2c_block_data(ACCL_ADDR, 0x06, 2)

        # データを12bitsに変換
        accl_x = ((raw_accl_x[1] * 256) + (raw_accl_x[0] & 0xF0)) / 16
        # 符号付整数なので、0ビット目が1ならば負の数に変換する
        if accl_x > 2047:
            accl_x -= 4096
        accl_y = ((raw_accl_y[1] * 256) + (raw_accl_y[0] & 0xF0)) / 16
        if accl_y > 2047:
            accl_y -= 4096
        accl_z = ((raw_accl_z[1] * 256) + (raw_accl_z[0] & 0xF0)) / 16
        if accl_z > 2047:
            accl_z -= 4096

        # ±4gモードでは出力される値の単位は1.95mgなのでgに変換する
        accl_x *= 0.00195
        accl_y *= 0.00195
        accl_z *= 0.00195
        return accl_x, accl_y, accl_z

    def get_angular_rate(self) -> tuple[float, float, float]:
        """角速度[°/s]を取得する

        Returns:
            tuple[float, float, float]: 角速度（x, y, z）（単位:[°/s]）
        
        Raises:
            OSError: I2C通信が正常に行えなかった際に発生
        """
        # 測定範囲は±500°を指定
        return convert.raw_ang_rate_to_ang_per_s(self.__get_angular_rate(), 500)

    def __get_angular_rate(self) -> tuple[float, float, float]:
        """生の角速度を取得する

        Returns:
            tuple[float, float, float]: 生の角速度データ (x, y, z)
        """
        # レジスタから値を読む
        raw_ang_rate = self.bus.read_i2c_block_data(GYRO_ADDR, 0x02, 6)

        # ビット範囲の変換
        ang_rate_x = raw_ang_rate[1] * 256 + raw_ang_rate[0]
        # 符号付整数なので、0ビット目が1ならば負の数に変換する
        if ang_rate_x > 32767:
            ang_rate_x -= 65536
        ang_rate_y = raw_ang_rate[3] * 256 + raw_ang_rate[2]
        if ang_rate_y > 32767:
            ang_rate_y -= 65536
        ang_rate_z = raw_ang_rate[5] * 256 + raw_ang_rate[4]
        if ang_rate_z > 32767:
            ang_rate_z -= 65536
        return ang_rate_x, ang_rate_y, ang_rate_z

    def get_magnetic_heading(self) -> float:
        """地磁気センサから方位角を計算する

        Returns:
            float: 方位角（単位：度）

        Raises:
            OSError: I2C通信が正常に行えなかった際に発生
        """
        mag_field = self.__get_magnetic_field_data()
        return convert.ut_to_azimuth(mag_field[0], mag_field[1])

    def __get_magnetic_field_data(self) -> tuple[float, float, float]:
        """3軸地磁気センサから3軸の地磁気[μT]を取得する

        Returns:
            tuple[float, float, float]: 地磁気[μT] (x, y, z)
        """
        # レジスタから値を読む
        raw_mag_x_y = self.bus.read_i2c_block_data(MAG_ADDR, 0x42, 4)
        raw_mag_z = self.bus.read_i2c_block_data(MAG_ADDR, 0x46, 2)

        # 13ビットに変換
        mag_x = ((raw_mag_x_y[1] * 256) + (raw_mag_x_y[0] & 0xF8)) / 8
        # 符号付整数なので、0ビット目が1ならば負の数に変換する
        if mag_x > 4095:
            mag_x -= 8192
        mag_y = ((raw_mag_x_y[3] * 256) + (raw_mag_x_y[2] & 0xF8)) / 8
        if mag_y > 4095:
            mag_y -= 8192

        # 15ビットに変換
        mag_z = ((raw_mag_z[1] * 256) + (raw_mag_z[0] & 0xFE)) / 2
        if mag_z > 16383:
            mag_z -= 32768

        return mag_x, mag_y, mag_z


nine_axis_sensor = NineAxisSensor()
