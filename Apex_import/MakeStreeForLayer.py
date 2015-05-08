#!/usr/bin/env python
"""Class definition derived from the MakeStree base class.
This class defines the main method that processes 
all of the Subsystem directories for a given NIF Layer directory.
"""

__author__    = "Randy Sanchez"
__version__   = "$Revision: 1.6 $"
__date__      = "$Date: 05/07/2008 14:18:50 $"
__copyright__ = "Copyright 2008 LLNL"

import os
from MakeStreeBaseClass import *
from MakeStreeForSubSys import *
from make_stree_utilities import *
from optparse import OptionParser

class MakeStreeForLayer(MakeStree):
    "Make a shadow tree by a given [tower] and [layer]"
    
    def processDir(self, sourcePath, targetAdaPath, targetIdlPath):
        """For each subsystem in the given source directory,
            create a MakeStreeForSubsys object and use that object
            to create the appropriate files.
        """
        self.logName()
        subsysList = []
        for Entry in os.listdir(sourcePath):
            Entry_Path = os.path.join(sourcePath, Entry)
            # only add entries to the 'subsysList' if they are directories
            # with the appropriate SubSystem suffix
            if os.path.isdir(Entry_Path) and Entry_Path[-3:] == apex.Subsystem_Suffix:
                subsysList = subsysList + [Entry]
                
        for subsys in subsysList:
            Subsys_Path = os.path.join(sourcePath, subsys)
            Tower_Path  = os.path.join(Subsys_Path, self.towerName)
            Shadow_Path = os.path.join(targetAdaPath, subsys[:-3])
            if os.path.isdir(Tower_Path):
                subsysInstance = MakeStreeForSubSys(self.towerName, self.layerName, subsys, subsys)
                #
                # setup the flags within the SubSys instance based on the
                #   flags setup for this Layer instance.
                #
                subsysInstance.setInstanceVars((self.createApex, self.createGnat, self.createIdl,
                                                self.makeSoftLink, self.makeHardLink, self.makeCopy,
                                                self.moveIdlAda, self.removeIdlAdaDir, self.checkIdlAdaDir,
                                                self.effortOnly, self.debugOn, self.underApexSession,
                                                self.workspace))
                #
                # make the Source and Target path names for new instance
                #
                subsysInstance.makeSourcePathNames()
                subsysInstance.makeTargetPathNames()
                if not (self.moveIdlAda or self.removeIdlAdaDir or self.checkIdlAdaDir):
                    subsysInstance.prepareTargetDirectory(subsysInstance.targetAdaSubsysPath)
                #
                # process the given Subsystem directory making the appropriate
                #   files based on the command line options that the user chose.
                #
                subsysInstance.logName()
                subsysInstance.processDir(subsysInstance.sourceViewPath, 
                                          subsysInstance.targetAdaSubsysPath, 
                                          subsysInstance.targetIdlSubsysPath)
                #
                # get the counts of the processed files and directories and other counts
                #
                (viewsProcessed, dirsProcessed, filesProcessed, targetCount,
                    moveCount, statusCount, latestCount, duplicateCount) = \
                                        subsysInstance.getProcessCounts()
                # have the Subsystem instance log his counts
                subsysInstance.logProcessCounts()
                # update my instances counts
                self.viewsProcessed = self.viewsProcessed + 1
                self.dirsProcessed  = self.dirsProcessed + dirsProcessed
                self.filesProcessed = self.filesProcessed + filesProcessed
                self.targetCount    = self.targetCount + targetCount
                self.moveCount      = self.moveCount + moveCount
                self.statusCount    = self.statusCount + statusCount
                self.latestCount    = self.latestCount + latestCount
                self.duplicateCount = self.duplicateCount + duplicateCount
    
