""" This module tests:
u2f
x2u
"""

import unittest
import unum

class TestX2u(unittest.TestCase):
    def setUp(self):
        self.old_e = unum.esizesize
        self.old_f = unum.fsizesize

    def tearDown(self):
        unum.setenv ((self.old_e, self.old_f))

    def do_u2f_equal(self, uf_list):
        """ Support routine
        """
        for u, f in uf_list:
            self.assertEqual(unum.u2f(u), f)

    def do_u2f_raises(self, u_list):
        """ Support routine
        """
        for u in u_list:
            with self.assertRaises(AssertionError):
                _x = unum.u2f(u)

    def do_x2u_list(self, xu_list):
        for x, u in xu_list:
           # print ('Calling x2u(%s)' % x)
            xu = unum.x2u(x)
            # print ('x2u returned:\n%s\n' % unum.utagview(xu))
            self.assertEqual(xu, u,
                'In environment (%s, %s), unum.x2u(%s) should return:\n%s\n(%s), not:\n%s\n(%s)' %
                             (unum.esizesize,unum.fsizesize, x,
                              unum.utagview(u),u, unum.utagview(xu), xu))

    def test_05_u2f_0_0(self):
        unum.setenv ((0, 0))
        self.do_u2f_equal([
            [0, 0.0],
            [2, 1.0],
            [4, 2.0],
            [6, unum.Infinity],
            [8, 0.0],
            [10, -1.0],
            [12, -2.0],
            [14, unum.NegInfinity],
        ])
        self.do_u2f_raises((1,3,5,7,9,11,13,15))


    def test_05_u2f_0_1(self):
        unum.setenv ((0, 1))
        self.do_u2f_equal([
            [0, 0.0],
            [1, 0.0],
            [4, 1.0],
            [5, 0.5],
            [8, 2.0],
            [9, 1.0],
            [12, 3.0],
            [13, 1.5],
            [16, 0.0],
            [17, 2.0],
            [20, -1.0],
            [21, 2.5],
            [24, -2.0],
            [25, 3],
            [28, -3.0],
            [29, unum.Infinity],
        ])
        self.do_u2f_raises((2,3,6,7,10,11,14,15,18,19,22,23,26,27,30,31))

    def test_05_u2f_1_0(self):
        unum.setenv ((1,0))
        self.do_u2f_equal([
            [0, 0.0],
            [1, 0.0],
            [4, 1.0],
            [5, 0.5],
            [8, 2.0],
            [9, 1.0],
            [12, 3.0],
            [13, 1.5],
            [16, 0.0],
            [17, 2.0],
            [20, -1.0],
            [21, 3.0],
            [24, -2.0],
            [25, 4.0],
            [28, -3.0],
            [29, unum.Infinity],
        ])
        self.do_u2f_raises((2,3,6,7,10,11,14,15,18,19,22,23,26,27,30,31))

    def test_05_u2f_1_1(self):
        unum.setenv ((1,1))
        self.do_u2f_equal([
            [0, 0.0],
            [1, 0.0],
            [2, 0.0],
            [3, 0.0],
            [8, 1.0],
            [9, 0.5],
            [10, 0.5],
            [11, 0.25],
            [16, 2.0],
            [17, 1.0],
            [18, 1.0],
            [19, 0.5],
            [24, 3.0],
            [25, 1.5],
            [26, 1.5],
            [27, 0.75],
        ])
        self.do_u2f_raises((4,4,6,7,12,13,14,15,20,21,22,23,28,29,30,31))


    def test_10_x2u(self):

        unum.setenv((0, 0))
        self.do_x2u_list ([
            [0.0, 0],
            [0.5, 1],
            [1.0, 2],
            [1.5, 3],
            [2.0, 4],
            [3.0, 5],
            [10.0, 5],
        ])

        unum.setenv((0, 1))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 4],
            [1.5, 13],
            [2.0, 8],
            [3.0, 12],
            [10.0, 27],
            [100.0, 27],
        ])

        unum.setenv((0, 2))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 8],
            [1.5, 25],
            [2.0, 16],
            [3.0, 24],
            [10.0, 247],
            [100.0, 247],
        ])

        unum.setenv((0, 3))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 16],
            [1.5, 49],
            [2.0, 32],
            [3.0, 48],
            [10.0, 8175],
            [100.0, 8175],
        ])

        unum.setenv((1, 0))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 9],
            [1.5, 13],
            [2.0, 8],
            [3.0, 12],
            [10.0, 27],
            [100.0, 27],
        ])

        unum.setenv((1, 1))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 18],
            [1.5, 26],
            [2.0, 16],
            [3.0, 24],
            [10.0, 119],
            [100.0, 119],
        ])

        unum.setenv((1, 2))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 36],
            [1.5, 52],
            [2.0, 32],
            [3.0, 48],
            [10.0, 1007],
            [100.0, 1007],
        ])

        unum.setenv((1, 3))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 72],
            [1.5, 104],
            [2.0, 64],
            [3.0, 96],
            [10.0, 32735],
            [100.0, 32735],
        ])

        unum.setenv((2, 0))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 17],
            [1.5, 25],
            [2.0, 16],
            [3.0, 24],
            [10.0, 102],
            [100.0, 223],
            [1000.0, 247],
            [10000.0, 247]
        ])
        self.do_x2u_list ([
            [3, 24],
            [4, 49],
            [5, 53],
            [6, 57],
            [7, 94],
            [8, 98],
            [9, 102],
            [10.0, 102],
            [11.0, 102],
            [12.0, 106],
        ])

        unum.setenv((2, 1))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 34],
            [1.5, 50],
            [2.0, 32],
            [3.0, 48],
            [10.0, 405],
            # [100.0, 879],
            [1000.0, 1007],
            [10000.0, 1007]
        ])

        unum.setenv((2, 2))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 68],
            [1.5, 100],
            [2.0, 64],
            [3.0, 96],
            [10.0, 809],
            [100.0, 6959],
            [1000.0, 8159],
            [10000.0, 8159]
        ])

        unum.setenv((2, 3))
        self.do_x2u_list ([
            [0.0, 0],
            [1.0, 136],
            [1.5, 200],
            [2.0, 128],
            [3.0, 192],
            [10.0, 1617],
            [100.0, 13915],
            [1000.0, 262079],
            [10000.0, 262079]
        ])

    def test_13_setenv_0_loop(self):
        for fsize in range(0, 9):
        # for fsize in range(0, 11):
            for esize in range(0, 4):
                unum.setenv ((esize, fsize))
                for x in (0.0, 1.0, 1.5, 2.0, 3.0, 10.0, 100.0, 1000.0, 10000.0):
                    # The test is that none of these raise an exception:
                    # print ('esize: %s, fsize: %s, x: %s' % (esize, fsize, x))
                    u = unum.x2u(x)

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


suite = unittest.TestLoader().loadTestsFromTestCase(TestX2u)

if __name__ == '__main__':
    unittest.main()
