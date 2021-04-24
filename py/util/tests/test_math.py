import unittest

import py.util.math as M


class TestLerps(unittest.TestCase):
    def test_lerp(self):
        self.assertAlmostEqual(M.lerp(0.2, 10.0, 20.0), 12.0)
        self.assertAlmostEqual(M.lerp(-0.2, 10.0, 20.0), 8.0)
        self.assertAlmostEqual(M.lerp(1.2, 20.0, 10.0), 8.0)

    def test_lerp2(self):
        self.assertAlmostEqual(M.lerp2(3, 30, 4, 40, 5), 50)


class TestClamp(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(M.clamp(5, 50, 0), 5)
        self.assertEqual(M.clamp(5, 50, 30), 30)
        self.assertEqual(M.clamp(5, 50, 60), 50)