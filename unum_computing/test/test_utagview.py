__author__ = 'charles'
import unittest
import unum

class Test_utagview(unittest.TestCase):

    def setUp(self):
        self.old_e = unum.esizesize
        self.old_f = unum.fsizesize

    def tearDown(self):
        unum.setenv ((self.old_e, self.old_f))

    def test_10_utagview_0_0(self):
        unum.setenv ((0, 0))

        self.assertEqual(unum.utagview(unum.x2u(0)), '|0|| || |\n .  1  1 ')

