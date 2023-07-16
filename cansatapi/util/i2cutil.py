"""I2C用ユーティリティモジュール"""

import busio
from adafruit_blinka.board.raspberrypi.raspi_40pin import *


def write8(addr: int, reg: int, value):
    """8bitのデータを指定のアドレスに書き込む
    Args:
        addr (int): アドレス
        reg (int): レジスタ
        value (int): 書き込む値
    """
    i2c_bus = busio.I2C(SCL, SDA)
    wait_lock(i2c_bus)
    try:
        i2c_bus.writeto(addr, bytes([reg, value]))
    finally:
        i2c_bus.unlock()


def read8(addr: int, reg: int) -> int:
    """8bitのデータを指定のアドレスから読み込む
    Args:
        addr (int): アドレス
        reg (int): レジスタ
    """
    return read_multiple(addr, reg, 1)[0]


def read_multiple(addr: int, reg: int, length: int) -> bytearray:
    """複数バイトのデータを指定のアドレスから読み込む
    Args:
        addr (int): アドレス
        reg (int): レジスタ
        length (int): 読み込むバイト長
    """
    i2c_bus = busio.I2C(SCL, SDA)
    value = bytearray(length)
    wait_lock(i2c_bus)
    try:
        i2c_bus.writeto_then_readfrom(addr, bytes([reg]), value)
    finally:
        i2c_bus.unlock()

    return value


def wait_lock(i2c_bus: busio.I2C):
    """I2Cバスが解放されるまで待つ関数

    Args:
        i2c_bus (busio.I2c): I2Cバス
    """
    while not i2c_bus.try_lock():
        pass
