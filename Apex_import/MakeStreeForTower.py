#!/usr/bin/env python
"""Class definition derived from the MakeStree base class.
This class defines the main method that processes the NIF Layer directories
defined for a given Tower.
"""

__author__    = "Randy Sanchez"
__version__   = "$Revision: 1.6 $"
__date__      = "$Date: 05/07/2008 14:18:51 $"
__copyright__ = "Copyright 2008 LLNL"

import os
from MakeStreeBaseClass import *
from MakeStreeForLayer import *
from make_stree_utilities import *
from optparse import OptionParser

class MakeStreeForTower(MakeStree):
    "Make a shadow tree by a given [tower]"
    
    def processDir(self, sourcePath, targetAdaPath, targetIdlPath):
        """For each layer in the given source directory,
            create a MakeStreeForLayer object and use that object
            to create the appropriate files.
        """
        self.logName()
        for Layer in apex.NIF_Layers:
            Layer_Path = os.path.join(sourcePath, Layer)
            if os.path.isdir(Layer_Path):
                layerInstance = MakeStreeForLayer(self.towerName, Layer, self.subsysName, Layer)
                #
                # setup the flags within the Layer instance based on the
                #   flags setup for this Tower instance.
                #
                layerInstance.setInstanceVars((self.createApex, self.createGnat, self.createIdl,
                                                self.makeSoftLink, self.makeHardLink, self.makeCopy,
                                                self.moveIdlAda, self.removeIdlAdaDir, self.checkIdlAdaDir,
                                                self.effortOnly, self.debugOn, self.underApexSession,
                                                self.workspace))
                #
                # make the Source and Target path names for our given instance
                #
                layerInstance.makeSourcePathNames()
                layerInstance.makeTargetPathNames()
                if not (self.moveIdlAda or self.removeIdlAdaDir or self.checkIdlAdaDir):
                    layerInstance.prepareTargetDirectory(layerInstance.targetAdaLayerPath)
                #
                # process the given Layer directory making the appropriate
                #   files based on the command line options that the user chose.
                #
                layerInstance.processDir(layerInstance.sourceLayerPath, 
                                          layerInstance.targetAdaLayerPath, 
                                          layerInstance.targetIdlLayerPath)
                #
                # get the counts of the processed files and directories and other counts
                #
                (viewsProcessed, dirsProcessed, filesProcessed, targetCount,
                    moveCount, statusCount, latestCount, duplicateCount) = \
                                        layerInstance.getProcessCounts()
                # have the Subsystem instance log his counts
                layerInstance.logProcessCounts()
                # update my instances counts
                self.viewsProcessed = self.viewsProcessed + viewsProcessed
                self.dirsProcessed  = self.dirsProcessed + dirsProcessed
                self.filesProcessed = self.filesProcessed + filesProcessed
                self.targetCount    = self.targetCount + targetCount
                self.moveCount      = self.moveCount + moveCount
                self.statusCount    = self.statusCount + statusCount
                self.latestCount    = self.latestCount + latestCount
                self.duplicateCount = self.duplicateCount + duplicateCount
