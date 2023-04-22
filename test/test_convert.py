import unittest
from cansatapi.util.convert import g_to_m_per_s2


class TestConvert(unittest.TestCase):

    def test_g_to_m_s2(self):
        g = [1, 1, 1]
        m_s2 = 9.80665
        self.assertAlmostEqual(g_to_m_per_s2(g)[0], m_s2)
