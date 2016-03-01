""" This module tests:
Abs
BitAnd
BitOr
BitShiftLeft
BitShiftRight
BitXor
Boole
Ceiling
Denominator
Floor
Grid
integerQ
Log
Max
Row
Style
IntegerString
"""
import unittest
import unum

class MyTestCase(unittest.TestCase):

    def test_Abs(self):
        self.assertEqual(unum.Abs(0), 0)
        self.assertEqual(unum.Abs(0.0), 0.0)
        self.assertEqual(unum.Abs(1), 1)
        self.assertEqual(unum.Abs(1.1), 1.1)
        self.assertEqual(unum.Abs(10), 10)
        self.assertEqual(unum.Abs(1000000.1), 1000000.1)
        self.assertEqual(unum.Abs(12345678901234567890), 12345678901234567890)
        self.assertEqual(unum.Abs(1234567890.1234567890), 1234567890.1234567890)
        self.assertEqual(unum.Abs(-0), 0)
        self.assertEqual(unum.Abs(-0.0), 0.0)
        self.assertEqual(unum.Abs(-1), 1)
        self.assertEqual(unum.Abs(-1.1), 1.1)
        self.assertEqual(unum.Abs(-10), 10)
        self.assertEqual(unum.Abs(-1000000.1), 1000000.1)
        self.assertEqual(unum.Abs(-12345678901234567890), 12345678901234567890)
        self.assertEqual(unum.Abs(-1234567890.1234567890), 1234567890.1234567890)

    def test_BitAnd(self):
        self.assertEqual(unum.BitAnd(1, 1), 1)
        self.assertEqual(unum.BitAnd(0, 1), 0)
        self.assertEqual(unum.BitAnd(1, 0), 0)
        self.assertEqual(unum.BitAnd(0, 0), 0)
        self.assertEqual(unum.BitAnd(0b0, 0b0), 0b0)
        self.assertEqual(unum.BitAnd(0b11111, 0b11111), 0b11111)
        self.assertEqual(unum.BitAnd(0b11111, 0b00000), 0b00000)
        self.assertEqual(unum.BitAnd(0b11111, 0b10101), 0b10101)
        self.assertEqual(unum.BitAnd(0b11111, 0b0), 0b0)
        self.assertEqual(unum.BitAnd(0b11111111111111111111, 0b10000000000000000000), 0b10000000000000000000)
        self.assertEqual(unum.BitAnd(0b111110000, 0b000011111), 0b000010000)

    def test_BitOr(self):
        self.assertEqual(unum.BitOr(1, 1), 1)
        self.assertEqual(unum.BitOr(0, 1), 1)
        self.assertEqual(unum.BitOr(1, 0), 1)
        self.assertEqual(unum.BitOr(0, 0), 0)
        self.assertEqual(unum.BitOr(0b0, 0b0), 0b0)
        self.assertEqual(unum.BitOr(0b11111, 0b11111), 0b11111)
        self.assertEqual(unum.BitOr(0b11111, 0b00000), 0b11111)
        self.assertEqual(unum.BitOr(0b00000, 0b10101), 0b10101)
        self.assertEqual(unum.BitOr(0b11111, 0b0), 0b11111)
        self.assertEqual(unum.BitOr(0b11111111111111111111, 0b10000000000000000000), 0b11111111111111111111)
        self.assertEqual(unum.BitOr(0b111110000, 0b000011111), 0b111111111)

    def test_BitShiftLeft(self):
        self.assertEqual(unum.BitShiftLeft(0b0, 0), 0b0)
        self.assertEqual(unum.BitShiftLeft(0b1, 0), 0b1)
        self.assertEqual(unum.BitShiftLeft(0b101, 0), 0b101)
        self.assertEqual(unum.BitShiftLeft(0b11111111111111111111, 0), 0b11111111111111111111)
        self.assertEqual(unum.BitShiftLeft(0b0, 1), 0b0)
        self.assertEqual(unum.BitShiftLeft(0b1, 1), 0b10)
        self.assertEqual(unum.BitShiftLeft(0b101, 1), 0b1010)
        self.assertEqual(unum.BitShiftLeft(0b11111111111111111111, 1), 0b111111111111111111110)
        self.assertEqual(unum.BitShiftLeft(0b0, 2), 0b0)
        self.assertEqual(unum.BitShiftLeft(0b1, 2), 0b100)
        self.assertEqual(unum.BitShiftLeft(0b101, 2), 0b10100)
        self.assertEqual(unum.BitShiftLeft(0b11111111111111111111, 2), 0b1111111111111111111100)
        self.assertEqual(unum.BitShiftLeft(0b0, 4), 0b0)
        self.assertEqual(unum.BitShiftLeft(0b1, 4), 0b10000)
        self.assertEqual(unum.BitShiftLeft(0b101, 4), 0b1010000)
        self.assertEqual(unum.BitShiftLeft(0b11111111111111111111, 4), 0b111111111111111111110000)
        self.assertEqual(unum.BitShiftLeft(0b0, 20), 0b0)
        self.assertEqual(unum.BitShiftLeft(0b1, 20), 0b100000000000000000000)
        self.assertEqual(unum.BitShiftLeft(0b101, 20), 0b10100000000000000000000)
        self.assertEqual(unum.BitShiftLeft(0b11111111111111111111, 20), 0b1111111111111111111100000000000000000000)

    def test_BitShiftRight(self):
        self.assertEqual(0b0 >> 0, 0b0)
        self.assertEqual(0b1 >> 0, 0b1)
        self.assertEqual(0b101 >> 0, 0b101)
        self.assertEqual(0b11111111111111111111 >> 0, 0b11111111111111111111)
        self.assertEqual(0b0 >> 1, 0b0)
        self.assertEqual(0b1 >> 1, 0b0)
        self.assertEqual(0b101 >> 1, 0b10)
        self.assertEqual(0b11111111111111111111 >> 1, 0b1111111111111111111)
        self.assertEqual(0b0 >> 2, 0b0)
        self.assertEqual(0b1 >> 2, 0b0)
        self.assertEqual(0b101 >> 2, 0b1)
        self.assertEqual(0b11111111111111111111 >> 2, 0b111111111111111111)
        self.assertEqual(0b0 >> 4, 0b0)
        self.assertEqual(0b1 >> 4, 0b0)
        self.assertEqual(0b101 >> 4, 0b0)
        self.assertEqual(0b11111111111111111111 >> 4, 0b1111111111111111)
        self.assertEqual(0b0 >> 20, 0b0)
        self.assertEqual(0b1 >> 20, 0b0)
        self.assertEqual(0b101 >> 20, 0b0)
        self.assertEqual(0b1111111111111111111100000000000000000000>> 20, 0b11111111111111111111)

    def test_BitXor(self):
        self.assertEqual(1 ^ 1, 0)
        self.assertEqual(0 ^ 1, 1)
        self.assertEqual(1 ^ 0, 1)
        self.assertEqual(0 ^ 0, 0)
        self.assertEqual(0b0 ^ 0b0, 0b0)
        self.assertEqual(0b11111 ^ 0b11111, 0b00000)
        self.assertEqual(0b11111 ^ 0b00000, 0b11111)
        self.assertEqual(0b00000 ^ 0b10101, 0b10101)
        self.assertEqual(0b11111 ^ 0b0, 0b11111)
        self.assertEqual(0b11111111111111111111 ^ 0b10000000000000000000, 0b01111111111111111111)
        self.assertEqual(0b111110000 ^ 0b000011111, 0b111101111)

    def test_Boole(self):
        self.assertEqual(unum.Boole(True), 1)
        self.assertEqual(unum.Boole(False), 0)

    def test_Ceiling(self):
        self.assertEqual(unum.Ceiling(0.0), 0)
        self.assertEqual(unum.Ceiling(1.0), 1)
        self.assertEqual(unum.Ceiling(1.5), 2)
        self.assertEqual(unum.Ceiling(9.999), 10)
        self.assertEqual(unum.Ceiling(1.001), 2)
        self.assertEqual(unum.Ceiling(1.0001), 2)
        self.assertEqual(unum.Ceiling(1.000001), 2)
        self.assertEqual(unum.Ceiling(1.00000001), 2)
        self.assertEqual(unum.Ceiling(1.0000000001), 2)
        self.assertEqual(unum.Ceiling(1.0000000000001), 2)
        self.assertEqual(unum.Ceiling(1.000000000000001), 2)
        self.assertEqual(unum.Ceiling(1.00000000000000001), 1)
        # self.assertEqual(unum.Ceiling(1.00000000000000001), 2)
        self.assertEqual(unum.Ceiling(1.0000000000000000001), 1)
        # self.assertEqual(unum.Ceiling(1.0000000000000000001), 2)
        self.assertEqual(unum.Ceiling(1.000000000000000000001), 1)
        # self.assertEqual(unum.Ceiling(1.000000000000000000001), 2)
        self.assertEqual(unum.Ceiling(100000000000000000000.1), 100000000000000000000)
        # self.assertEqual(unum.Ceiling(100000000000000000000.1), 100000000000000000001)
        self.assertEqual(unum.Ceiling(-1.0), -1)
        self.assertEqual(unum.Ceiling(-1.5), -1)
        self.assertEqual(unum.Ceiling(-9.999),-9)
        self.assertEqual(unum.Ceiling(-1.999), -1)
        self.assertEqual(unum.Ceiling(-1.9999), -1)
        self.assertEqual(unum.Ceiling(-1.999999), -1)
        self.assertEqual(unum.Ceiling(-1.99999999), -1)
        self.assertEqual(unum.Ceiling(-1.9999999999), -1)
        self.assertEqual(unum.Ceiling(-1.9999999999999), -1)
        self.assertEqual(unum.Ceiling(-1.999999999999999), -1)
        self.assertEqual(unum.Ceiling(-1.99999999999999999), -2)
        # self.assertEqual(unum.Ceiling(-1.99999999999999999), -1)
        self.assertEqual(unum.Ceiling(-1.9999999999999999999), -2)
        # self.assertEqual(unum.Ceiling(-1.9999999999999999999), -1)
        self.assertEqual(unum.Ceiling(-1.999999999999999999999), -2)
        # self.assertEqual(unum.Ceiling(-1.999999999999999999999), -1)
        self.assertEqual(unum.Ceiling(-99999999999999999999.9), -100000000000000000000)
      # self.assertEqual(unum.Ceiling(-99999999999999999999.9),  -99999999999999999999)

    def test_Denominator(self):
        self.assertEqual(unum.Denominator(0.0), 1)
        self.assertEqual(unum.Denominator(1.0), 1)
        self.assertEqual(unum.Denominator(2.0), 1)
        self.assertEqual(unum.Denominator(0.5), 2)
        self.assertEqual(unum.Denominator(1/2), 1)
        self.assertEqual(unum.Denominator(1.0/2.0), 2)
        self.assertEqual(unum.Denominator(3.0/4.0), 4)
        self.assertEqual(unum.Denominator(1.625), 8)

    def test_Floor(self):
        self.assertEqual(unum.Floor(0.0), 0)
        self.assertEqual(unum.Floor(1.0), 1)
        self.assertEqual(unum.Floor(1.5), 1)
        self.assertEqual(unum.Floor(9.999),9)
        self.assertEqual(unum.Floor(1.999), 1)
        self.assertEqual(unum.Floor(1.9999), 1)
        self.assertEqual(unum.Floor(1.999999), 1)
        self.assertEqual(unum.Floor(1.99999999), 1)
        self.assertEqual(unum.Floor(1.9999999999), 1)
        self.assertEqual(unum.Floor(1.9999999999999), 1)
        self.assertEqual(unum.Floor(1.999999999999999), 1)
        self.assertEqual(unum.Floor(1.99999999999999999), 2)
        # self.assertEqual(unum.Floor(1.99999999999999999), 1)
        self.assertEqual(unum.Floor(1.9999999999999999999), 2)
        # self.assertEqual(unum.Floor(1.9999999999999999999), 1)
        self.assertEqual(unum.Floor(1.999999999999999999999), 2)
        # self.assertEqual(unum.Floor(1.999999999999999999999), 1)
        self.assertEqual(unum.Floor(99999999999999999999.9), 100000000000000000000)
      # self.assertEqual(unum.Floor(99999999999999999999.9),  99999999999999999999)
        self.assertEqual(unum.Floor(-1.0), -1)
        self.assertEqual(unum.Floor(-1.5), -2)
        self.assertEqual(unum.Floor(-9.999), -10)
        self.assertEqual(unum.Floor(-1.001), -2)
        self.assertEqual(unum.Floor(-1.0001), -2)
        self.assertEqual(unum.Floor(-1.000001), -2)
        self.assertEqual(unum.Floor(-1.00000001), -2)
        self.assertEqual(unum.Floor(-1.0000000001), -2)
        self.assertEqual(unum.Floor(-1.0000000000001), -2)
        self.assertEqual(unum.Floor(-1.000000000000001), -2)
        self.assertEqual(unum.Floor(-1.00000000000000001), -1)
        # self.assertEqual(unum.Floor(-1.00000000000000001), -2)
        self.assertEqual(unum.Floor(-1.0000000000000000001), -1)
        # self.assertEqual(unum.Floor(-1.0000000000000000001), -2)
        self.assertEqual(unum.Floor(-1.000000000000000000001), -1)
        # self.assertEqual(unum.Floor(-1.000000000000000000001), -2)
        self.assertEqual(unum.Floor(-100000000000000000000.1), -100000000000000000000)
        # self.assertEqual(unum.Floor(-100000000000000000000.1), -100000000000000000001)

    def test_Grid(self):
        self.assertEquals(unum.Grid(((1,2), (3,4))), ' 1  2 \n 3  4 ')
        self.assertEquals(unum.Grid(((1,2),)), ' 1  2 ')
        self.assertEquals(unum.Grid(((1,), (3,))), ' 1 \n 3 ')
        with self.assertRaises(RuntimeError):
            x = self.assertEquals(unum.Grid((1, 3)), ' 1 \n 3 ')
        with self.assertRaises(RuntimeError):
            x = self.assertEquals(unum.Grid('foo'), 'foo')
        with self.assertRaises(RuntimeError):
            x = self.assertEquals(unum.Grid(('foo', 'bar')), ' foo \n bar ')
        self.assertEquals(unum.Grid(((1,2), (3,4)),
                                    Frame=(None, None, {(1,1): True})), '|1| 2 \n 3  4 ')

    def test_integerQ(self):
        self.assertTrue(unum.IntegerQ(0))
        self.assertTrue(unum.IntegerQ(1))
        self.assertTrue(unum.IntegerQ(-1))
        self.assertFalse(unum.IntegerQ(0.0))
        self.assertFalse(unum.IntegerQ(1.0))
        self.assertFalse(unum.IntegerQ(1.5))
        self.assertFalse(unum.IntegerQ(unum.NaN))
        self.assertFalse(unum.IntegerQ(unum.Infinity))
        self.assertFalse(unum.IntegerQ(unum.NegInfinity))

    def test_Log(self):
        self.assertEquals(unum.Log(2, 1), 0)
        self.assertEquals(unum.Log(2, 2), 1)
        self.assertEquals(unum.Log(2, 4), 2)
        self.assertEquals(unum.Log(2, 8), 3)
        self.assertEquals(unum.Log(2, 1.0/2.0), -1)
        self.assertEquals(unum.Log(2, 1.0/4.0), -2)
        self.assertEquals(unum.Log(2, 1.0/8.0), -3)
        self.assertAlmostEquals(unum.Log(2, 2**0.5), 0.5)
        self.assertEquals(unum.Log(10, 100), 2)
        self.assertEquals(unum.Log(3, 27), 3)
        self.assertEquals(unum.Log(2, 0), unum.NegInfinity)
        self.assertEquals(unum.Log(10, 0), unum.NegInfinity)
        with self.assertRaises(ValueError):
            x = unum.Log(2, -1)

    def test_Max(self):
        self.assertEquals(unum.Max(1, 2), 2)
        self.assertEquals(unum.Max(1, 1), 1)
        self.assertEquals(unum.Max(0, 0), 0)
        self.assertEquals(unum.Max(1, 1.1), 1.1)
        self.assertEquals(unum.Max(1, 1.01), 1.01)
        self.assertEquals(unum.Max(1, 1.001), 1.001)
        self.assertEquals(unum.Max(1, 1.000000000000000000001), 1)
        # self.assertEquals(unum.Max(1, 1.000000000000000000001), 1.000000000000000000001)
        self.assertEquals(unum.Max(-1, 0), 0)
        self.assertEquals(unum.Max(-1, -1.1), -1)
        self.assertEquals(unum.Max(-1, -1.01), -1)
        self.assertEquals(unum.Max(-1, -1.001), -1)
        self.assertEquals(unum.Max(-2, -1.999999999999999999999), -2)
        # self.assertEquals(unum.Max(-2, -1.999999999999999999999), -1.999999999999999999999)

    def test_Row(self):
        self.assertEquals(unum.Row((1,2,3)), '123')
        self.assertEquals(unum.Row((1,2,3), ' '), '1 2 3')
        self.assertEquals(unum.Row('a'), 'a')
        self.assertEquals(unum.Row('abc', ' '), 'abc')

    def test_Style(self):
        self.assertEquals(unum.Style(1), '1')
        self.assertEquals(unum.Style(1, 'bold'), '1')
        self.assertEquals(unum.Style('1'), '1')

    def test_IntegerString(self):
        self.assertEquals(unum.IntegerString(1), '1')
        self.assertEquals(unum.IntegerString(-100), '-100')
        self.assertEquals(unum.IntegerString(4, 10), '4')
        self.assertEquals(unum.IntegerString(4, 2), '100')
        self.assertEquals(unum.IntegerString(4, 10, 3), '004')
        self.assertEquals(unum.IntegerString(-4, 10, 4), '-004')
        self.assertEquals(unum.IntegerString(-4, 10, 3), '-04')

        self.assertEquals(unum.IntegerString(123, 10, 3), '123')
        self.assertEquals(unum.IntegerString(123, 10, 2), '23')
        self.assertEquals(unum.IntegerString(123, 10, 0), ' ')
        # self.assertEquals(unum.IntegerString(123, 10, 0), '')

if __name__ == '__main__':
    unittest.main()
