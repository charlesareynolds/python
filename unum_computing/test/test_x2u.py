import unittest
import unum

class TestX2u(unittest.TestCase):
    def setUp(self):
        self.old_e = unum.esizesize
        self.old_f = unum.fsizesize

    def tearDown(self):
        unum.setenv ((self.old_e, self.old_f))

    def test_1_x2u(self):
        def test_list(xu_list):
            for x, u in xu_list:
                print ('Calling x2u(%s)' % x)
                xu = unum.x2u(x)
                self.assertEqual(xu, u,
                    'In environment (%s, %s), unum.x2u(%s) should = %s, not %s' % (unum.esizesize,unum.fsizesize,x,u, xu))

        unum.setenv((0, 0))
        test_list ([
            [0.0, 0],
            [1.0, 2],
            [1.5, 3],
            [2.0, 4],
            [3.0, 5],
            [10.0, 5],
            [100.0, 5]
        ])

        unum.setenv((0, 1))
        test_list ([
            [0.0, 0],
            [1.0, 2],
            [1.5, 3],
            [2.0, 4],
            [3.0, 5],
            [10.0, 5],
            [100.0, 5]
        ])


    def test_2_autoN(self):
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

    def test_3_inf_nan(self):
        self.assertEqual(unum.Infinity, unum.Infinity)
        self.assertNotEqual(unum.Infinity, unum.NegInfinity)
        self.assertNotEqual(unum.Infinity, 1.0)

        self.assertNotEqual(unum.NaN, 1.0)
        self.assertNotEqual(unum.NaN, 0.0)

        self.assertEqual(0.0, -0.0)

        self.assertNotEqual(unum.NaN, unum.NaN)
        self.assertTrue(unum.NaN is unum.NaN)
        self.assertFalse(unum.NaN is not unum.NaN)

        self.assertNotEqual(unum.NaN, unum.Infinity)
        self.assertTrue(unum.NaN is not unum.Infinity)
        self.assertFalse(unum.NaN is unum.Infinity)

    def test_4_unumQ(self):
        unum.setenv((2, 3))
        self.assertTrue(unum.unumQ(0))
        self.assertTrue(unum.unumQ(1))
        self.assertTrue(unum.unumQ(unum.sNaNu))
        self.assertFalse(unum.unumQ(-1))
        self.assertFalse(unum.unumQ(unum.sNaNu + 1))
        self.assertFalse(unum.unumQ(1.5))
        self.assertFalse(unum.unumQ(unum.NaN))
        self.assertFalse(unum.unumQ(unum.Infinity))
        self.assertFalse(unum.unumQ(unum.NegInfinity))
        self.assertFalse(unum.unumQ('foo'))

    def test_5_fsizeminus1(self):
        unum.setenv((3, 4))
        self.assertEqual (unum.fsizeminus1(unum.x2u(30.0)),1)
        self.assertEqual (unum.fsizeminus1(unum.x2u(31.0)),1)


suite = unittest.TestLoader().loadTestsFromTestCase(TestX2u)

if __name__ == '__main__':
    unittest.main()
