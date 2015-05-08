#!/usr/bin/env python
'''
Created on May 19, 2010

@author: reynolds12
'''
from parser import Parser

class Rules(object):
    """ Assembles a collection of one-to-many relationships and returns it as an
    iterable.
    """
    def __init__(self):
        self.items = dict()
        
    def add(self, key, item):
        if key in self.items:
            self.items[key] = self.items[key] + [item]
        else:
            self.items[key] = [item]
        
    def getRules(self):
        """Returns an iterable."""
        return self.items.iteritems()

class Generator(object):
    '''
    Generates Makefile_ada.for_release.  See test_Makefile_ada.for_release
    to see what one of those should look like:
    '''
    
    def __init__(self, inputFile, outputFile):
        """inputFile is passed on to parser uninspected.
        If outputFile is a string, a corresponding file is opened.  Otherwise,
        it is assumed to be an open real or mock file. 
        """
        self.inputFile = inputFile
        if outputFile.__class__ is str:
            self.outputFile = file(outputFile, mode='w')
        else:
            self.outputFile = outputFile
        self.parser = Parser()
        
    def genRules(self):
        self.parser.parse(self.inputFile)
        platformRules, executableRules = self._assembleRules(self.parser.getProjects())
        self._output ("#!!!WARNING!!! THIS FILE IS AUTO-GENERATED!!!")
        self._output ("")
        self._ouptutPlatformRules(platformRules)
        self._output ("")
        self._outputExecutableRules(executableRules)
        
    def _assembleRules(self, projects):
        platformRules = Rules()
        executableRules = Rules()
        for project in projects:
            for deliverable in self.parser.getDeliverables (project):
                executableRules.add (self.parser.getPath(project), 
                                     self.parser.getName(deliverable))
                for platform in self.parser.getPlatforms(deliverable):
                    platformRules.add (self.parser.getName(platform), 
                                       self.parser.getName(deliverable))
        return platformRules, executableRules
        
    def _ouptutPlatformRules(self, platformRules):    
        self._output ("# Define the rules for each platform.")
        for platform, deliverables in sorted(platformRules.getRules()):
            platformString = platform + "_for_release"
            self._output (".PHONY: " + platformString)
            ruleLine = platformString + " :"
            for deliverable in sorted(deliverables):
                ruleLine = ruleLine + " " + deliverable
            self._output (ruleLine)

    def _outputExecutableRules(self, executableRules):
        self._output ("# Define the rules for each executable.")
        for project, deliverables in sorted(executableRules.getRules()):
            executableString = ""
            for deliverable in sorted(deliverables):
                executableString =  executableString + deliverable + " "
            executableString = executableString + ": " + project
            self._output (executableString)
            self._output ("\t@${LOGRULE}")
            self._output ("\t${GNATMAKE} -P$< ${GPRFLAGS} ${notdir ${basename $@}}")
            
    def _output(self, line):
        """ Outputs one line to the output file.  Separate method  to control 
        output behavior in one place."""
        self.outputFile.write (line + "\n")

if __name__ == "__main__":
    Generator(inputFile = "Makefile_ada.in.xml",
              outputFile = "Makefile_ada.for_release").genRules()
     
