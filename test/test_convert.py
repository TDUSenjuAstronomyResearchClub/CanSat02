import unittest
from cansatapi.util.convert import g_to_m_per_s2
from cansatapi.util.convert import raw_ang_rate_to_ang_per_s
from cansatapi.util.convert import ut_to_azimuth
from cansatapi.util.convert import acceleration_to_roll
from cansatapi.util.convert import acceleration_to_pitch
from cansatapi.util.convert import conv_range


class TestConvert(unittest.TestCase):

    def test_g_to_m_s2(self):
        g = [1, 1, 1]
        m_s2 = 9.80665
        self.assertAlmostEqual(g_to_m_per_s2(g)[0], m_s2)

    def raw_ang_rate_to_ang_per_s(self):
        per_s = 1
        absss = 2000
        self.assertAlmostEqual(raw_ang_rate_to_ang_per_s(per_s, absss), -250)

    def ut_to_azimuth(self):
        x = 100
        y = 100
        self.assertAlmostEqual(ut_to_azimuth(x, y), 45)

    def acceleration_to_roll(self):
        x = 1
        y = 1
        self.assertAlmostEqual(acceleration_to_roll(x, y), 0.78)

    def acceleration_to_pitch(self):
        x = 1
        y = 1
        z = 1
        self.assertAlmostEqual(acceleration_to_pitch(x, y, z), 0.61)

    def conv_range(self):
        a_min = 50
        a_max = 0
        b_min = 100
        b_max = 0
        target = 1
        self.assertAlmostEqual(conv_range(a_min, a_max, b_min, b_max, target), 0.5)

