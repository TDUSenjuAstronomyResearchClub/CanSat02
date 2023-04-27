import math
import unittest
from cansatapi.gps import *


class TestGPSMethods(unittest.TestCase):

    def test_lat_conv_deg_min_to_decimal(self):
        lat_deg_min = "3544.92"
        direction = "N"

        expect = 35.74866667
        decimal = lat_conv_deg_min_to_decimal(lat_deg_min, direction)

        # 浮動小数点のチェックなので、近似しているかどうかを検証する
        self.assertTrue(math.isclose(expect, decimal))

    def test_lan_conv_deg_min_to_decimal(self):
        lon_deg_min = "13948.38"
        direction = "E"

        expect = 139.80633333
        decimal = lon_conv_deg_min_to_decimal(lon_deg_min, direction)

        self.assertTrue(math.isclose(expect, decimal))
