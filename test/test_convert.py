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
        azim = 100
        muth = 100
        self.assertAlmostEqual(ut_to_azimuth(azim, muth), 45)

    def acceleration_to_roll(self):
        accel = 1
        roll = 1
        self.assertAlmostEqual(acceleration_to_roll(accel, roll), 0.78)

    def acceleration_to_pitch(self):
        rec = 1
        tec = 1
        xec = 1
        self.assertAlmostEqual(acceleration_to_pitch(rec, tec, xec), 0.61)

    def conv_range(self):
        xcc = 50
        xdd = 0
        xee = 100
        xff = 0
        xgg = 1
        self.assertAlmostEqual(conv_range(xcc, xdd, xee, xff, xgg), 0.5)

