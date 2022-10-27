#!/usr/bin/env python
"""Tests string_utilis.py
"""

# Standard library imports
import os
import sys
import unittest

# Add parent dir to path, so we can import from sibling directories:
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import unittest

#Local imports
from support.string_utils import su


class TestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_stripSuffixes(self):
        self.assertEqual(su.stripSuffixes(["foo.bar", "all.out"]), ["foo", "all"])

    def test_stripSuffix(self):
        self.assertEqual(su.stripSuffix("foo.bar"), "foo")

    def test_countIsOrAre(self):
        self.assertEqual(su.countIsOrAre(0), "0 are")
        self.assertEqual(su.countIsOrAre(1), "1 is")
        self.assertEqual(su.countIsOrAre(2), "2 are")

    def test_countWasOrWere(self):
        self.assertEqual(su.countWasOrWere(0), "0 were")
        self.assertEqual(su.countWasOrWere(1), "1 was")
        self.assertEqual(su.countWasOrWere(2), "2 were")

    def test_countSingularOrPlural(self):
        self.assertEqual(su.countSingularOrPlural(0, "is singular", "is plural"), "0 is plural")
        self.assertEqual(su.countSingularOrPlural(1, "is singular", "is plural"), "1 is singular")
        self.assertEqual(su.countSingularOrPlural(2, "is singular", "is plural"), "2 is plural")

    def test_noneToEmpty(self):
        self.assertEqual(su.noneToEmpty(None), "")
        self.assertEqual(su.noneToEmpty("foo"), "foo")

    def test_concatWSpace(self):
        self.assertEqual(su.concatWSpace('one', 'two'), 'one two')
        self.assertEqual(su.concatWSpace('one', ''), 'one')
        self.assertEqual(su.concatWSpace('one', None), 'one')
        self.assertEqual(su.concatWSpace('', 'two'), 'two')
        self.assertEqual(su.concatWSpace(None, 'two'), 'two')
        self.assertEqual(su.concatWSpace('', ''), '')
        self.assertEqual(su.concatWSpace('', None), '')
        self.assertEqual(su.concatWSpace(None, ''), '')
        self.assertEqual(su.concatWSpace(None, None), '')

    def test_concatWString(self):
        self.assertEqual(su.concatWString('one', "-", "two"), "one-two")
        self.assertEqual(su.concatWString('one', "...", "two"), "one...two")
        self.assertEqual(su.concatWString('one', "", "two"), "onetwo")
        self.assertEqual(su.concatWString('one', "...", ''), 'one')
        self.assertEqual(su.concatWString('one', "...", None), 'one')
        self.assertEqual(su.concatWString('', "...", 'two'), 'two')
        self.assertEqual(su.concatWString(None, "...", 'two'), 'two')
        self.assertEqual(su.concatWString('', "...", ''), '')
        self.assertEqual(su.concatWString('', "...", None), '')
        self.assertEqual(su.concatWString(None, "...", ''), '')
        self.assertEqual(su.concatWString(None, "...", None), '')


if __name__ == '__main__':
    unittest.main()
