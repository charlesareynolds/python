import unittest
import unum

class TestX2u(unittest.TestCase):
    def setUp(self):
        self.old_e = unum.esizesize
        self.old_f = unum.fsizesize

    def tearDown(self):
        unum.setenv ((self.old_e, self.old_f))

    def test_x2u(self):
        unum.setenv((0, 0))
        u = unum.x2u(1.0)
        self.assertEqual(u, 2)

    def test_autoN(self):
        self.assertEqual(str(unum.autoN(unum.NaN)), 'nan')
        self.assertEqual(str(unum.autoN(unum.Infinity)), 'inf')
        self.assertEqual(str(unum.autoN(0.0)), '0.0')
        self.assertEqual(str(unum.autoN(1.0)), '1.0')
        self.assertEqual(str(unum.autoN(1.)), '1.0')
        self.assertEqual(str(unum.autoN(2.0)), '2.0')
        self.assertEqual(str(unum.autoN(1.5)), '1.5')
        self.assertEqual(str(unum.autoN(1.0/16.0)), '0.0625')

        self.assertEqual(str(unum.autoN(0)), '0')
        self.assertEqual(str(unum.autoN(1)), '1')

        self.assertEqual(str(unum.autoN(-1.0)), '-1.0')
        self.assertEqual(str(unum.autoN(unum.NegInfinity)), '-inf')

    def test_inf_nan(self):
        self.assertEqual(unum.Infinity, unum.Infinity)
        self.assertNotEqual(unum.NaN, 1.0)
        self.assertNotEqual(unum.NaN, unum.NaN)
        self.assertNotEqual(unum.NaN, unum.Infinity)
        self.assertTrue(unum.NaN is unum.NaN)
        self.assertFalse(unum.NaN is not unum.NaN)
        self.assertFalse(unum.NaN is unum.Infinity)



suite = unittest.TestLoader().loadTestsFromTestCase(TestX2u)

if __name__ == '__main__':
    unittest.main()
