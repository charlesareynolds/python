'''
Contains the XtermRunner class, which extends support.runner.Runner to run a 
command in an xterm.
'''
from support.runner import Runner

import os
import subprocess

class XtermRunner(Runner):
    ''' Extends Runner to run a command in an xterm.
    '''

    def __init__(self, effortOnly=False):
        Runner.__init__ (self, effortOnly)
        
    def xtermOrLog(self, xtermArgs, popenArgs, run_dir=None):
#        xtermArgs = ["-geometry", "90x40"]
#        popenArgs = ["xterm", "-badxarg"]
#        popenArgs = ["xterm",] + ["-e",] + popenArgs
        popenArgs = ["xterm", "-hold"] + xtermArgs + ["-e",] + popenArgs
        if self._effortOnly:
            self._logger.info("Would do " + self._commandMessage(popenArgs, run_dir))
            return ("", "")
        else:
            self._logger.info(self._commandMessage(popenArgs, run_dir))
            return self.tryXterm(popenArgs, run_dir)

    def tryXterm(self, popenArgs, run_dir=None):
        """Issue the command associated with the given Popen arguments list.
        Does not return the results of the command.
        """
        try:   
            p1 = subprocess.Popen(args = popenArgs, 
                                  env = os.environ, 
                                  #stdout = subprocess.PIPE, 
                                  #stderr = subprocess.PIPE,
                                  #shell = True,
                                  cwd = run_dir)
            (output, errors) = p1.communicate()
        except OSError:
            self._logger.logger.exception('EXCEPTION raised while running "' + self._commandMessage(popenArgs, run_dir) + '"')
            self._logger.error("Raising Runner.Failed")
            raise self.Failed ()
        return (output, errors)

        