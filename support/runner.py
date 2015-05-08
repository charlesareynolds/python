"""Contains the Runner class, which supports effort-only behavior by logging a 
command instead of running it.
"""
import os
import subprocess
from support.local_logging import Logger, LineLogger, FunctionLogger


class Runner():
    class Failed(Exception):
        pass

    def __init__(self, effortOnly=False):
        self._effortOnly = effortOnly
        self._logger = Logger(
            name='support.runner.Runner',
            level=Logger.DEBUG)

    def setEffortOnly(self, effortOnly):
        self._effortOnly = effortOnly

    def runOrLog(self, command, globals=None, locals=None, doReraise=False):
        if self._effortOnly:
            self._logger.info("Would do: " + command)
        else:
            self._logger.info(command)
            self.tryExec(command, globals, locals, doReraise)

    def tryExec(self, command, globals=None, locals=None, doReraise=False):
        try:
            exec command in globals, locals
        except Exception:
            self._logger.logger.exception('EXCEPTION raised while running "' + command + '"')
            if doReraise:
                self._logger.error("Raising Runner.Failed")
                raise self.Failed()
            else:
                self._logger.info("Continuing...")

    def evalOrLog(self, command, globals=None, locals=None):
        if self._effortOnly:
            self._logger.info("Would do: " + command)
        else:
            self._logger.info(command)
            return self.tryEval(command, globals, locals)

    def tryEval(self, command, globals=None, locals=None):
        """Evaluates the expression in command and returns the result.  Always
        reraises any exceptions.
        """
        try:
            return eval(command, globals, locals)
        except Exception:
            self._logger.logger.exception('EXCEPTION raised while evaluating "' + command + '"')
            self._logger.error("Raising Runner.Failed")
            raise self.Failed()

    def _commandMessage(self, popenArgs, dir):
        return "Popen(args=" + str(popenArgs) + ", dir=" + str(dir)

    def popenOrLog(self, popenArgs, dir=None):
        if self._effortOnly:
            self._logger.info("Would do " + self._commandMessage(popenArgs, dir))
            return ("", "")
        else:
            self._logger.info(self._commandMessage(popenArgs, dir))
            return self.tryPopen(popenArgs, dir)

    def tryPopen(self, popenArgs, dir=None):
        """Issue the command associated with the given Popen arguments list.
        Returns the results of the command in a (output, errors) tuple.
        """
        try:
            p1 = subprocess.Popen(
                args=popenArgs,
                env=os.environ,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=dir)
            (output, errors) = p1.communicate()
        except OSError, e:
            self._logger.logger.exception(
                'EXCEPTION raised while running "' + self._commandMessage(popenArgs, dir) + '"')
            self._logger.error("Raising Runner.Failed")
            raise self.Failed()
        return output, errors

    # Synonyms
    execOrLog = runOrLog


runner = Runner()
