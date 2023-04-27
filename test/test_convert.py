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
        per_s = 1000
        absss = 1000
        self.assertAlmostEqual(raw_ang_rate_to_ang_per_s(per_s, absss), 401)
    def ut_to_azimuth(self):
        azim = 1.5
        muth = 0.5
        self.assertAlmostEqual(ut_to_azimuth(azim, muth), 18.43)
    def acceleration_to_roll(self):
        accel = 0.5
        roll = 1.5
        self.assertAlmostEqual(acceleration_to_roll(accel, roll), 18.43)

    def acceleration_to_pitch(self):
        rec = -0.5
        tec = 1.5
        xec = 2.5
        self.assertAlmostEqual(acceleration_to_pitch(rec, tec, xec), -31.93)

    def conv_range(self):
        xcc = 10
        xdd = 8
        xee = 12
        xff = 10
        xgg = 15
        self.assertAlmostEqual(conv_range(xcc, xdd, xee, xff, xgg), 25)

