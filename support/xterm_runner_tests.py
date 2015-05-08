#!/usr/bin/env python
"""Runs unit tests on support.xterm_runner.
"""
import unittest
from support.local_logging import Logger
from support.xterm_runner import XtermRunner

class TestCase1(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = Logger("support.xterm_runner_tests.TestCase1")
        self.runner = XtermRunner()
        self.dir = "/"
        self.badDir = "/nosuchdir"
        self.popenArgs = ["uname", "-a"]
        self.badPopenArgs=["nosuchprog",]
        self.xtermArgs1 = ["-geometry", "90x40"]
        self.xtermArgs2 = ["-geometry", "90x40-10-10"]
        self.badXtermArgs = ["-badxtermarg",]


    def tearDown(self):
        self._xtermRunner = None
        unittest.TestCase.tearDown(self)

    def test01_EffortOnly(self):
        self.logger.log("Exercising effortOnly=True.  Command should not execute.")
        self.runner.setEffortOnly(True)
        self.runner.xtermOrLog(xtermArgs=self.xtermArgs1, 
                               popenArgs=self.popenArgs, 
                               dir=self.dir)
#        (output, errors)=self.runner.xtermOrLog(self.popenArgs, self.dir)
#        self.assertTrue(output=="")
#        self.assertTrue(errors=="")
        
    def test02_DoIt(self):
        self.logger.log("Exercising effortOnly=False.  Command should execute.")
        self.runner.setEffortOnly(False)
#        self.runner.xtermOrLog(self.xtermArgs2, self.popenArgs, self.dir)
        (output, errors)=self.runner.xtermOrLog(self.xtermArgs1, self.popenArgs, self.dir)
        print ("output:")
        print (output)
        print ("errors:")
        print (errors)
        self.assertTrue(errors==None)
#        self.assertTrue("SunOS" in output or "Linux" in output)

    def test04_ReraiseExcep(self):
        self.logger.log("Exercising popenAndHandle. errors should not be None")
        (output, errors)=self.runner.xtermOrLog(self.badXtermArgs, self.popenArgs, self.dir)
        print ("output:")
        print (output)
        print ("errors:")
        print (errors)
        self.assertTrue(errors != None)
        
    def test05_ReraiseExcep(self):
        self.logger.log("Exercising popenAndHandle.  Exception should be logged and reraised.")
        self.assertRaises(
                        XtermRunner.Failed, 
                        self.runner.xtermOrLog, self.xtermArgs1, self.popenArgs, self.badDir)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()