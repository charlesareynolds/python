#!/usr/bin/env python
"""Runs unit tests on support.runner.
"""
import unittest
from support.local_logging import Logger
import support.runner


class TestCase1(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = Logger("support.runner_tests.TestCase")
        self.runner = support.runner.Runner()
        self.command = "print('foo')"

    def tearDown(self):
        self.runner = None
        unittest.TestCase.tearDown(self)

    def test01_EffortOnly(self):
        self.logger.log("Exercising effortOnly=True.  Command should not execute.")
        self.runner.setEffortOnly(True)
        self.runner.runOrLog(self.command)

    def test02_DoIt(self):
        self.logger.log("Exercising effortOnly=False.  Command should execute.")
        self.runner.setEffortOnly(False)
        self.runner.runOrLog(self.command)

    def test03_HandleExcep(self):
        self.logger.log("Exercising runAndHandle.  Exception should be logged and not reraised.")
        self.runner.runOrLog("print(nonExistentVar)")

    def test04_ReraiseExcep(self):
        self.logger.log("Exercising runAndHandle.  Exception should be logged and reraised.")
        self.assertRaises(
            support.runner.Runner.Failed,
            self.runner.runOrLog, "print(nonExistentVar)", doReraise=True)


class TestCase2NameSpace(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = Logger("support.runner_tests.TestCaseNameSpace")
        self.runner = support.runner.Runner()
        self.command = "atexit.register(abs, 0)"

    def tearDown(self):
        self.runner = None
        unittest.TestCase.tearDown(self)

    def test01_EffortOnly(self):
        self.logger.log("Exercising effortOnly=True.  Command should not execute.")
        self.runner.setEffortOnly(True)
        self.runner.runOrLog(self.command, globals(), locals())

    def test02_DoIt(self):
        self.logger.log("Exercising effortOnly=False.  Command should execute.")
        self.runner.setEffortOnly(False)
        self.runner.runOrLog(self.command, globals(), locals())

    def test03_HandleExcep(self):
        self.logger.log("Exercising operation not in namespace.  Exception should be raised.")
        self.runner.runOrLog(self.command)


def square(parm_in):
    print ("parm_in is " + str(parm_in))
    return parm_in * parm_in


class TestCase3Eval(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = Logger("support.runner_tests.TestCase3Eval")
        self.runner = support.runner.Runner()
        self.command = "square(parm)"

    def tearDown(self):
        self.runner = None
        unittest.TestCase.tearDown(self)

    def test01_EffortOnly(self):
        self.logger.log("Exercising effortOnly=True.  Command should not execute.")
        self.runner.setEffortOnly(True)
        result = self.runner.evalOrLog(self.command, globals(), locals())

    def test02_DoIt(self):
        self.logger.log("Exercising effortOnly=False.  Command should execute.")
        self.runner.setEffortOnly(False)
        parm = 3
        result = self.runner.evalOrLog(self.command, globals(), locals())
        self.assertEquals(result, 9)

    def test04_ReraiseExcep(self):
        self.logger.log("Exercising evalAndHandle.  Exception should be logged and reraised.")
        self.assertRaises(
            support.runner.Runner.Failed,
            self.runner.evalOrLog, "print(nonExistentVar)")


class TestCase4Popen(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = Logger("support.runner_tests.TestCase4Popen")
        self.runner = support.runner.Runner()
        self.dir = "/"
        self.badDir = "/nosuchdir"
        self.popenArgs = ["uname", "-a"]
        self.badPopenArgs = ["nosuchprog", ]

    def tearDown(self):
        self.runner = None
        unittest.TestCase.tearDown(self)

    def test01_EffortOnly(self):
        self.logger.log("Exercising effortOnly=True.  Command should not execute.")
        self.runner.setEffortOnly(True)
        (output, errors) = self.runner.popenOrLog(self.popenArgs, self.dir)
        self.assertTrue(output == "")
        self.assertTrue(errors == "")

    def test02_DoIt(self):
        self.logger.log("Exercising effortOnly=False.  Command should execute.")
        self.runner.setEffortOnly(False)
        (output, errors) = self.runner.popenOrLog(self.popenArgs, self.dir)
        self.assertTrue(errors == "")
        self.assertTrue("SunOS" in output or "Linux" in output)

    def test04_ReraiseExcep(self):
        self.logger.log("Exercising popenAndHandle.  Exception should be logged and reraised.")
        self.assertRaises(
            support.runner.Runner.Failed,
            self.runner.popenOrLog, self.badPopenArgs, self.dir)

    def test05_ReraiseExcep(self):
        self.logger.log("Exercising popenAndHandle.  Exception should be logged and reraised.")
        self.assertRaises(
            support.runner.Runner.Failed,
            self.runner.popenOrLog, self.popenArgs, self.badDir)


if __name__ == "__main__":
    unittest.main()