import unittest

from py.util.types import RGB8, Size2D


class TestRGB8(unittest.TestCase):
    def test_parse_syntax_error(self):
        with self.assertRaises(ValueError):
            RGB8.parse("rgb(1,2)")
        with self.assertRaises(ValueError):
            RGB8.parse("#abcd")
        with self.assertRaises(ValueError):
            RGB8.parse("#12345678")

    def test_parse_rgb_func(self):
        self.assertEqual(RGB8.parse("rgb(1,2,3)"), RGB8(1, 2, 3))
        self.assertEqual(RGB8.parse("rgb(0xff, 0xff, 0xff)"), RGB8(255, 255, 255))

    def test_parse_six_hex(self):
        self.assertEqual(RGB8.parse("#345abc"), RGB8(0x34, 0x5A, 0xBC))

    def test_parse_three_hex(self):
        self.assertEqual(RGB8.parse("#abc"), RGB8(0xAA, 0xBB, 0xCC))

    def test_parse_str_isomorphic(self):
        x = RGB8.parse("rgb(5, 10, 15)")
        self.assertEqual(x, RGB8(5, 10, 15))
        self.assertEqual(RGB8.parse(str(x)), x)


class TestSize2D(unittest.TestCase):
    def test_parse_syntax_error(self):
        with self.assertRaises(ValueError):
            Size2D.parse("1")
        with self.assertRaises(ValueError):
            Size2D.parse("1x")
        with self.assertRaises(ValueError):
            Size2D.parse("1x1a")
        with self.assertRaises(ValueError):
            Size2D.parse("1ax1")

    def test_parse(self):
        self.assertEqual(Size2D.parse("30x40"), Size2D(30, 40))