import unittest
import unum

class TestX2u(unittest.TestCase):
    def setUp(self):
        self.old_e = unum.esizesize
        self.old_f = unum.fsizesize

    def tearDown(self):
        unum.setenv ((self.old_e, self.old_f))

    def test_10_x2u(self):
        def test_list(xu_list):
            for x, u in xu_list:
                print ('Calling x2u(%s)' % x)
                xu = unum.x2u(x)
                self.assertEqual(xu, u,
                    'In environment (%s, %s), unum.x2u(%s) should return %s, not %s' % (unum.esizesize,unum.fsizesize,x,u, xu))

        unum.setenv((0, 0))
        test_list ([
            [0.0, 0],
            [1.0, 2],
            [1.5, 3],
            # [2.0, 4],
            # [3.0, 5],
            # [10.0, 5],
            # [100.0, 5]
        ])

        unum.setenv((0, 1))
        test_list ([
            [0.0, 0],
            [1.0, 4],
            [1.5, 13],
            [2.0, 8],
            [3.0, 12],
            [10.0, 27],
            [100.0, 27]
        ])

        unum.setenv((0, 2))
        test_list ([
            [0.0, 0],
            [1.0, 8],
            [1.5, 25],
            [2.0, 16],
            [3.0, 24],
            [10.0, 247],
            [100.0, 247]
        ])

        unum.setenv((0, 3))
        test_list ([
            [0.0, 0],
            [1.0, 16],
            [1.5, 49],
            [2.0, 32],
            [3.0, 48],
            [10.0, 8175],
            [100.0, 8175]
        ])

        unum.setenv((1, 0))
        test_list ([
            [0.0, 0],
            [1.0, 9],
            [1.5, 13],
            [2.0, 8],
            [3.0, 12],
            [10.0, 27],
            [100.0, 27]
        ])

        unum.setenv((1, 1))
        test_list ([
            [0.0, 0],
            [1.0, 18],
            [1.5, 26],
            [2.0, 16],
            [3.0, 24],
            [10.0, 119],
            [100.0, 119]
        ])

        unum.setenv((1, 2))
        test_list ([
            [0.0, 0],
            [1.0, 36],
            [1.5, 52],
            [2.0, 32],
            [3.0, 48],
            [10.0, 1007],
            [100.0, 1007]
        ])

        unum.setenv((1, 3))
        test_list ([
            [0.0, 0],
            [1.0, 72],
            [1.5, 104],
            [2.0, 64],
            [3.0, 96],
            [10.0, 32735],
            [100.0, 32735]
        ])

        unum.setenv((2, 0))
        test_list ([
            [0.0, 0],
            [1.0, 17],
            [1.5, 25],
            [2.0, 16],
            [3.0, 24],
            [10.0, 102],
            [100.0, 223]
        ])

        unum.setenv((2, 1))
        test_list ([
            [0.0, 0],
            [1.0, 34],
            [1.5, 50],
            [2.0, 32],
            [3.0, 48],
            [10.0, 405],
            [100.0, 879]
        ])

        unum.setenv((2, 2))
        test_list ([
            [0.0, 0],
            [1.0, 68],
            [1.5, 100],
            [2.0, 64],
            [3.0, 96],
            [10.0, 809],
            [100.0, 6959]
        ])

        unum.setenv((2, 3))
        test_list ([
            [0.0, 0],
            [1.0, 136],
            [1.5, 200],
            [2.0, 128],
            [3.0, 192],
            [10.0, 1617],
            [100.0, 13915]
        ])

    def test_11_setenv_0_excep_1_0(self):
        # Gets an exception in the call to Log:
        unum.setenv ((1, 0))
        u = unum.x2u(1)

    def test_12_setenv_0_excep_0_5(self):
        # Gets an exception in the call to Log:
        unum.setenv ((0, 5))
        u = unum.x2u(1)

    def test_13_setenv_0_loop(self):
        for fsize in range(0, 11):
            for esize in range(0, 4):
                unum.setenv ((esize, fsize))
                for x in range(0, 9):
                    # The test is that none of these raise an exception:
                    print ('esize: %s, fsize: %s, x: %s' % (esize, fsize, x))
                    u = unum.x2u(x)

    def test_14_setenv_3_4(self):
        unum.setenv((3, 4))
        for x in range(31):
            u= unum.x2u(x)
        self.assertEqual(unum.fsizeminus1(unum.x2u(30.0)),1)
        self.assertEqual(unum.fsizeminus1(unum.x2u(31.0)),1)

    def test_20_autoN(self):
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

    def test_30_inf_nan(self):
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

    def test_40_unumQ(self):
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

    def test_50_fsizeminus1(self):
        unum.setenv((3, 4))
        for x in range(31):
            u= unum.x2u(x)
        self.assertEqual (unum.fsizeminus1(unum.x2u(30.0)),1)
        self.assertEqual (unum.fsizeminus1(unum.x2u(31.0)),1)


suite = unittest.TestLoader().loadTestsFromTestCase(TestX2u)

if __name__ == '__main__':
    unittest.main()
