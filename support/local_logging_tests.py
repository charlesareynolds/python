#!/usr/bin/env python
"""Runs unit tests on local_logging.
"""
import unittest
from local_logging import Logger, FunctionLogger, LineLogger, FunctionLineLogger


def test_a_logger(logger):
    print ("Testing levels: error, problem, warning, success, progress, log, info, and more")
    logger.error("error")
    logger.problem("problem")
    logger.warning("warning")
    logger.success("success")
    logger.progress("progress")
    logger.log("log")
    logger.info("info")
    logger.more("more")


def test_raw_logger(logger):
    print ("Testing raw logging levels: critical, error, warn, info, and debug")
    logger.logger.critical("critical")
    logger.logger.error("error")
    logger.logger.warn("warn")
    logger.logger.info("info")
    logger.logger.debug("debug")


class TestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test01_Default(self):
        print("Exercising default logging:")
        logger = Logger()
        test_a_logger(logger)
        print

    def test02_Debug(self):
        print("Exercising debug and level changing behavior:")
        logger = Logger()
        print("Debug is off.  calling debug (should print nothing)")
        logger.debug("debug while off")
        print("Debug is on.  calling debug")
        logger.set_debug_on()
        logger.debug("debug while on")
        print

    def test03_ParentChild(self):
        print("Exercising parent and child behavior:")
        parent = Logger("parent")
        child = Logger("parent.child")
        print("Logging to parent.  Should print once.")
        parent.log("Logging to parent.")
        print("Logging to child.  Should print twice.")
        child.log("Logging to child.")
        parent.disable()
        print("Only child is enabled. Logging to child.  Should print once.")
        child.log("Logging to child.")
        parent.enable()
        child.disable()
        print("Only parent is enabled. Logging to child.  Should print once.")
        child.log("Logging to child.")
        print

    def test04_NoPrefixes(self):
        print("Exercising no prefix logging:")
        logger = Logger(
            name='shortLogger',
            level=Logger.DEBUG,
            show_date=False,
            show_time=False,
            show_name=False)
        test_a_logger(logger)
        print

    def test05_LineNumberLogging(self):
        print("Exercising line number logging:")
        logger = LineLogger()
        test_raw_logger(logger)
        print

    def test06_FunctionNameLogging(self):
        print("Exercising function name logging:")
        logger = FunctionLogger()
        test_raw_logger(logger)
        print

    def test07_FunctionNameLineNumberLogging(self):
        print("Exercising function name line number logging:")
        logger = FunctionLineLogger()
        test_raw_logger(logger)
        print

    def test08_MultipleInits(self):
        print("Exercising mutiple initializes on same logger:")
        logger = Logger("multi")
        print("Initialized once.  Logging.  Should print once.")
        logger.log("log messge")
        logger = Logger("multi", show_date=False)
        print("Initialized again, w/o date output).  Logging.  Should print once.")
        logger.log("log messge")
        print


if __name__ == '__main__':
    unittest.main()