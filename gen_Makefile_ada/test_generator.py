'''
Created on May 17, 2010

@author: reynolds12
'''
import unittest

from generator import Generator
from testing_support import TS
from pythonmock.mock import Mock
import os

class TestGenerator(unittest.TestCase):

    _EXPECTED_OUTPUT = open("test_Makefile_ada.for_release").readlines()
    
    def setUp(self):
        pass

    def tearDown(self):
        self.generator = None

    def test01_genRules(self):
        """test01 Check that each write line call is correct.
        """
        self.outputFile = Mock()
        self.generator = Generator(inputFile = TS.XMLFileName,
                                   outputFile = self.outputFile)
        self.generator.genRules()
        for callNo in range(14):
            self.outputFile.mockCheckCall(callNo, 'write', 
                                              self._EXPECTED_OUTPUT [callNo])

    def test02_genRealFile(self):
        """test02 Given a string, check that the corresponding file is created.
        """
        outputFileName = "TestGeneratorOutput"
        if os.path.exists(outputFileName):
            os.remove(outputFileName)
        self.generator = Generator(inputFile = TS.XMLFileName,
                                   outputFile = outputFileName)
        self.generator.genRules()
        self.assertTrue(os.path.exists(outputFileName))
        if os.path.exists(outputFileName):
            os.remove(outputFileName)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()