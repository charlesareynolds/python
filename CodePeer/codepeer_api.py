"""Provides an API to AdaCore CodePeer
"""

#Local imports
from support.local_logging import Logger, GeneralAutoLog
from support.runner import Runner

class CodePeer_API:
    """Provides CodePeer commands"""

    def __init__(self, debugOn, effortOnly, project):
        self._command = r'C:\CODEPEER\22.2\bin\codepeer.exe'
        self._debugOn = debugOn
        self._effortOnly = effortOnly
        self._logger = Logger(name='codepeer_api.CodePeer_API')
        self._project = project
        self._runner = Runner()

        self._logger.set_debug(self._debugOn)
        self._runner.setEffortOnly(self._effortOnly)

    class AutoLog (GeneralAutoLog):
        def __init__(self, func_name=None):
          super(GeneralAutoLog, self).__init__(
              logger_name='CodePeer_API',
              func_name=func_name)

    # @GeneralAutoLog()
    def analyze(self):
        self._logger.debug('BEGIN analyze')
        args = [self._command,
                # '-P%s' % self._project]
                r'-PC:\Users\ch030982\Documents\Restore-L\git_PPE_code_analysis\Restore-L-GSP\restore_l_gsp.gpr']
        dir = "."
        try:
            self._runner.callOrLog(args, dir)
        except Runner.Failed as e:
            self._logger.exception('%s args:%s' % (type(e), str(e)))

    @GeneralAutoLog()
    def generate_csv(self):
        pass
#
#
# # my_project = 'C:\Users\ch030982\Documents\Restore-L\git_PPE_code_analysis\Restore-L-GSP\restore_l_gsp.gpr'
# my_codepeer = CodePeer_API(my_project)
# my_codepeer.analyze()
# my_codepeer.generate_csv()
