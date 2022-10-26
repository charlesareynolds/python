#!/usr/bin/env python
"""Runs unit tests on support.runner.
"""
import unittest
from local_logging import Logger
from runner import Runner


class TestCase1ExecOrLog(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = Logger("support.runner_tests.TestCase1ExecOrLog")
        self.runner = Runner()
        self.command = "print('foo')"
        self.bad_command = "print(nonExistentVar)"
        self.logger.info("")

    def tearDown(self):
        self.runner = None
        unittest.TestCase.tearDown(self)

    def test01_EffortOnly(self):
        self.logger.info("test01_EffortOnly: Exercising execOrLog with effortOnly=True.")
        self.logger.info("Command should not execute.")
        self.runner.setEffortOnly(True)
        self.runner.execOrLog(self.command)

    def test02_DoIt(self):
        self.logger.info("test02_DoIt: Exercising execOrLog with effortOnly=False.")
        self.logger.info("Command should execute.")
        self.runner.setEffortOnly(False)
        self.runner.execOrLog(self.command)

    def test03_HandleExcep(self):
        self.logger.info("test03_HandleExcep: Exercising execOrLog with a bad command.")
        self.logger.info("Exception should be logged but not Runner.Failed should be raised.")
        self.logger.info("Last log should be: '--- (support.runner.Runner) Continuing...'")
        self.runner.execOrLog(self.bad_command)

    def test04_ReraiseExcep(self):
        self.logger.info("test04_ReraiseExcep: Exercising execOrLog with a non-existent variable and doReraise=True.")
        self.logger.info("Exception should be logged and Runner.Failed should be raised.")
        self.logger.info("Last log should be: '*** (support.runner.Runner) Raising Runner.Failed'")
        self.assertRaises(
            Runner.Failed,
            self.runner.execOrLog, self.bad_command, doReraise=True)


class TestCase2NameSpace(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = Logger("support.runner_tests.TestCase2NameSpace")
        self.runner = Runner()
        self.bad_command = "atexit.register(abs, 0)"
        self.logger.info("")

    def tearDown(self):
        self.runner = None
        unittest.TestCase.tearDown(self)

    def test03_ReraiseExcep(self):
        self.logger.info("test03_ReraiseExcep: Exercising execOrLog with operation not in namespace.")
        self.logger.info("Exception should be logged and Runner.Failed should be raised.")
        self.logger.info("Last log should be: '*** (support.runner.Runner) Raising Runner.Failed'")
        self.assertRaises(
            Runner.Failed,
            self.runner.execOrLog, self.bad_command, doReraise=True)


def square(parm_in):
    print("parm_in is " + str(parm_in))
    return parm_in * parm_in


class TestCase3Eval(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = Logger("support.runner_tests.TestCase3Eval")
        self.runner = Runner()
        self.expression = "square(parm)"
        self.bad_expression = "nonExistentVar"
        self.logger.info("")

    def tearDown(self):
        self.runner = None
        unittest.TestCase.tearDown(self)

    def test01_EffortOnly(self):
        self.logger.info("test01_EffortOnly: Exercising evalOrLog with effortOnly=True.")
        self.logger.info("Command should not execute.")
        self.runner.setEffortOnly(True)
        result = self.runner.evalOrLog(self.expression, globals(), locals())

    def test02_DoIt(self):
        self.logger.info("test02_DoIt: Exercising evalOrLog with effortOnly=False.  Command should execute.")
        self.runner.setEffortOnly(False)
        parm = 3
        result = self.runner.evalOrLog(self.expression, globals(), locals())
        self.assertEqual(result, 9)

    # No no_reraise test here because there is no no_reraise option in evalOrLog.

    def test04_ReraiseExcep(self):
        self.logger.info("test04_ReraiseExcep: Exercising evalOrLog on bad expression.")
        self.logger.info("Exception should be logged and Runner.Failed should be raised.")
        self.logger.info("Last log should be: '*** (support.runner.Runner) Raising Runner.Failed'")
        self.assertRaises(
            Runner.Failed,
            self.runner.evalOrLog, self.bad_expression, globals(), locals())


class TestCase4Popen(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = Logger("support.runner_tests.TestCase4Popen")
        self.runner = Runner()
        self.dir = "/"
        self.badDir = "/nosuchdir"
        # Unix:
        # self.args = ["uname", "-a"]
        # Windows:
        self.args = ["SYSTEMINFO", ]
        self.badArgs = ["nosuchprog", ]
        self.logger.info("")

    def tearDown(self):
        self.runner = None
        unittest.TestCase.tearDown(self)

    def test01_EffortOnly(self):
        self.logger.info("test01_EffortOnly: Exercising popenOrLog with effortOnly=True.")
        self.logger.info("Command should not execute.")
        self.runner.setEffortOnly(True)
        (output, errors) = self.runner.popenOrLog(self.args, self.dir)
        self.assertTrue(output == "")
        self.assertTrue(errors == "")

    def test02_DoIt(self):
        self.logger.info("test02_DoIt: Exercising popenOrLog with effortOnly=False.")
        self.logger.info("Command should execute.")
        self.runner.setEffortOnly(False)
        (output, errors) = self.runner.popenOrLog(self.args, self.dir)
        self.logger.info("output:")
        for line in output.strip().decode().splitlines():
            print(line)
        # print (output)
        self.logger.info("errors:")
        print(errors)
        self.assertEqual(errors, b'')
        str_output = str(output)
        self.assertTrue(("SunOS" in str_output) or ("Linux" in str_output) or ("Windows" in str_output))

    # No no_reraise test here because there is no no_reraise option in popenOrLog.

    def test04_ReraiseExcep(self):
        self.logger.info("test04_ReraiseExcep: Exercising popenOrLog with bad args.")
        self.logger.info("Exception should be logged and Runner.Failed should be raised.")
        self.logger.info("Last log should be: '*** (support.runner.Runner) Raising Runner.Failed'")
        self.assertRaises(
            Runner.Failed,
            self.runner.popenOrLog, self.badArgs, self.dir)

    def test05_ReraiseExcep(self):
        self.logger.info("test05_ReraiseExcep: Exercising popenOrLog with bad dir.")
        self.logger.info("Exception should be logged and Runner.Failed should be raised.")
        self.logger.info("Last log should be: '*** (support.runner.Runner) Raising Runner.Failed'")
        self.assertRaises(
            Runner.Failed,
            self.runner.popenOrLog, self.args, self.badDir)


class TestCase5Call(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = Logger("support.runner_tests.TestCase5Call")
        self.runner = Runner()
        self.dir = "/"
        self.badDir = "/nosuchdir"
        # Unix:
        # self.args = ["uname", "-a"]
        # Windows:
        self.args = ["SYSTEMINFO", ]
        self.badArgs = ["nosuchprog", ]
        self.logger.info("")

    def tearDown(self):
        self.runner = None
        unittest.TestCase.tearDown(self)

    def test01_EffortOnly(self):
        self.logger.info("test01_EffortOnly: Exercising callOrLog with effortOnly=True.")
        self.logger.info("Command should not execute.")
        self.runner.setEffortOnly(True)
        self.runner.callOrLog(self.args, self.dir)

    def test02_DoIt(self):
        self.logger.info("test02_DoIt: Exercising callOrLog with effortOnly=False.")
        self.logger.info("Command should execute.")
        self.runner.setEffortOnly(False)
        self.runner.callOrLog(self.args, self.dir)

    # No no_reraise test here because there is no no_reraise option in callOrLog.

    def test04_ReraiseExcep(self):
        self.logger.info("test04_ReraiseExcep: Exercising callOrLog with bad args.")
        self.logger.info("Exception should be logged and Runner.Failed should be raised.")
        self.logger.info("Last log should be: '*** (support.runner.Runner) Raising Runner.Failed'")
        self.assertRaises(
            Runner.Failed,
            self.runner.callOrLog, self.badArgs, self.dir)

    def test05_ReraiseExcep(self):
        self.logger.info("test05_ReraiseExcep: Exercising callOrLog with bad dir.")
        self.logger.info("Exception should be logged and Runner.Failed should be raised.")
        self.logger.info("Last log should be: '*** (support.runner.Runner) Raising Runner.Failed'")
        self.assertRaises(
            Runner.Failed,
            self.runner.callOrLog, self.args, self.badDir)


if __name__ == "__main__":
    unittest.main()
