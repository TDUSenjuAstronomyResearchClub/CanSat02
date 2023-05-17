import unittest
from unittest.mock import MagicMock
from cansatapi.batteryfuelgauge import BatteryFuelGauge


class TestBatteryFuelGauge(unittest.TestCase):
    # テストクラス

    def test_get_level(self):
        # get_level()メソッドをテストするためのテストメソッド

        # smbus2ライブラリのモックを作成
        smbus2 = MagicMock()
        # モックのread_byte_data()メソッドに返す値を設定
        smbus2.SMBus.return_value.read_byte_data.return_value = 50
        # BatteryFuelGaugeクラスのインスタンスを作成し、モックをセット
        battery = BatteryFuelGauge()
        battery.bus = smbus2

        # get_level()メソッドを呼び出し、取得した値が想定通りか確認
        level = battery.get_level()
        self.assertEqual(level, 50)


if __name__ == '__main__':
    unittest.main()
