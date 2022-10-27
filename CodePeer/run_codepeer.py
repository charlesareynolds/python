#!/usr/bin/env python
"""Runs AdaCore CodePeer on a GNAT Ada project.
"""

# Standard library imports
from argparse import ArgumentParser
import inspect
import os
import sys

# Add parent dir to path, so we can import from sibling directories:
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# Local imports
from codepeer_api import CodePeer_API
from support.local_logging import Logger


class CodePeerRunner:

    def __init__(self):
        # Will be a Namespace (e.g. can refer to self._args.command_args):
        self._args = None
        self._codepeer_api = None
        self._current_dir = ""
        self._logger = Logger('run_codepeer.CodePeerRunner')
        self._parser = None
        self._script_dir = ""
        self._secondary_command = ""
        self._define_args()

    def _define_args(self):
        parser = ArgumentParser(
            # usage='Usage: %prog [options] <GNAT project file>',
                                description = __doc__)
        parser.add_argument('-d', '--debug',
                            action='store_true', default=False,
                            help='Turn on debugging [default: %(default)s]')
        parser.add_argument('-e', '--effort_only',
                            action='store_true', default=False,
                            help='Log what would be done without actually doing it [default: %(default)s]')
        parser.add_argument('-p', '--project',
                            action='store', type=ascii, default="",
                            help='Full path to a GNAT project file with suffix .gpr',
                            metavar = '<path>', required=True)
        self._parser = parser

    def _process_args(self):
        """Parse the command-line args, store them, and finish initializing
        """
        self._args = self._parser.parse_args()
        if self._args.debug:
            self._logger.set_debug_on()
        self._current_dir = os.getcwd()
        # Robustly get this script's directory, even when started by exec or execfiles:
        script_rel_path = inspect.getframeinfo(inspect.currentframe()).filename
        self._script_dir = os.path.dirname(os.path.abspath(script_rel_path))
        self._primary_command = r"C:\CODEPEER\22.2\bin\codepeer.exe"

        self._logger.debug('self._args: ' + str(self._args))
        self._logger.debug('self._current_dir: ' + str(self._current_dir))
        self._logger.debug('self._script_dir: ' + str(self._script_dir))
        self._logger.debug('self._primary_command: ' + str(self._primary_command))

    def run(self):
        self._process_args()
        self._codepeer_api = CodePeer_API (
            debugOn = self._args.debug,
            effortOnly = self._args.effort_only,
            project = self._args.project)
        self._codepeer_api.analyze()
        self._codepeer_api.generate_csv()

def main():
    CodePeerRunner().run()

if __name__ == '__main__':
    main()
