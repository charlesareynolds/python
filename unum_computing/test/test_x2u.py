import unittest
import unum

class TestX2u(unittest.TestCase):
    def test_x2u(self):
        old_e = unum.esizesize
        old_f = unum.fsizesize

        unum.setenv(0, 0)
        u = unum.x2u(1.0)
        self.assertEqual(u, 2)

        unum.setenv (old_e, old_f)

if __name__ == '__main__':
    unittest.main()
