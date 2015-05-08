#!/usr/bin/env python
""" Base class definition for the Make Shadow Tree utilities.
"""

__author__    = "Randy Sanchez"
__version__   = "$Revision: 1.10 $"
__date__      = "$Date: 07/02/2008 15:07:25 $"
__copyright__ = "Copyright 2008 LLNL"

# 2008/10/14

import os
import shutil
import sys

class MakeStree:
    "Make shadow tree base class"
    
    def __init__(self, tower, layer, subsystem, instanceName):
        """Initializes the instance variables associated with the class.
        """
        self.towerName        = tower
        self.layerName       = layer
        self.subsysName      = subsystem
        self.instanceName    = instanceName
        self.createApex      = False
        self.createGnat      = True
        self.createIdl       = True
        self.makeSoftLink    = True
        self.makeHardLink    = False
        self.makeCopy        = False
        self.moveIdlAda      = False
        self.removeIdlAdaDir = False
        self.checkIdlAdaDir  = False
        self.effortOnly      = False
        self.debugOn         = False
        self.workspace       = ""
        self.underApexSession = False
        self.verificationMode = False    # set to True to verify against the 'make_shadow_tree.py' utility
        self.viewsProcessed  = 0        # views are considered directories with a ".ss" suffix
        self.dirsProcessed   = 0        # views are directories also
        self.filesProcessed  = 0        # processing means that it has been looked at
        self.targetCount     = 0        # this counts the number of targets created
        self.moveCount       = 0        # this counts the number of moves performed
        self.statusCount     = 0        # this counts the number of files 
                                        # that were issued the 'show_status' APEX command
        self.latestCount     = 0        # this counts the number of files updated to the 'latest' version
        self.duplicateCount  = 0        # this counts the number of files that needed to be 'duplicated'
                                        # being 'duplicated' is APEX's way of copying the file
                                        # to a different view under the same sub-system.
        
        self.maxApexShowCommands = 7    # this is the maximum number of 'popen' calls
                                        # that will be used when issuing the APEX 'show_status' commands.
                                        # This will be tunable using the '-maxApexShowCommands'
                                        # command line option.
        self.maxApexMoveCommands = 1    # this is the maximum number of 'popen' calls
                                        # that will be used when issuing the APEX 'move' commands.
                                        # This will not be tunable at this time.  
                                        # The maxFilesPerApexMove will be a tunable parameter.
        self.maxFilesPerApexMove = 7    # this is the maximum number of files that can be placed
                                        # on the APEX 'move' command.  This is so that you can issue
                                        # less APEX 'move' commands since you are moving the files to
                                        # the same place, as a group.
                                        # This will be tunable using the 'maxFilesPerApexMove'
                                        # command line option.
        self.maxFilesPerApexStatus = 7
        self.maxFilesPerApexUpdate = 7

    def getProcessCounts(self):
        """Returns the base class instance variables associated with counts.
        """
        return (self.viewsProcessed, self.dirsProcessed, self.filesProcessed, self.targetCount,
                self.moveCount, self.statusCount, self.latestCount, self.duplicateCount)
    
    def logProcessCounts(self):
        """Logs the count information.
        """
        self.log("")
        self.log("        Views Processed: " + str(self.viewsProcessed))
        self.log("  Directories Processed: " + str(self.dirsProcessed))
        self.log("        Files Processed: " + str(self.filesProcessed))
        self.log("        Targets Created: " + str(self.targetCount))
        if (self.moveIdlAda):
            self.log("         Files Statused: " + str(self.statusCount))
            self.log("            Files Moved: " + str(self.moveCount))
            self.log("Files Updated to Latest: " + str(self.latestCount))
            self.log("       Files Duplicated: " + str(self.duplicateCount))
        self.log("")
    
    def setInstanceVars(self, param):
        """Sets the instance variables associated with the class based on the incoming info.
        """
        (self.createApex, 
         self.createGnat, 
         self.createIdl,
         self.makeSoftLink, 
         self.makeHardLink, 
         self.makeCopy,
         self.moveIdlAda, 
         self.removeIdlAdaDir, 
         self.checkIdlAdaDir,
         self.effortOnly, 
         self.debugOn, 
         self.underApexSession,
         self.workspace) = param
            
    def dumpInstanceVars(self):
        """Dumps the contents of the instance variables associated with the class.
        """
        self.debugPrint( "      towerName = " + self.towerName)
        self.debugPrint( "      layerName = " + self.layerName)
        self.debugPrint( "     subsysName = " + self.subsysName)
        self.debugPrint( "     createApex = " + str(self.createApex))
        self.debugPrint( "     createGnat = " + str(self.createGnat))
        self.debugPrint( "      createIdl = " + str(self.createIdl))
        self.debugPrint( "   makeSoftLink = " + str(self.makeSoftLink))
        self.debugPrint( "   makeHardLink = " + str(self.makeHardLink))
        self.debugPrint( "       makeCopy = " + str(self.makeCopy))
        self.debugPrint( "     moveIdlAda = " + str(self.moveIdlAda))
        self.debugPrint( "removeIdlAdaDir = " + str(self.removeIdlAdaDir))
        self.debugPrint( " checkIdlAdaDir = " + str(self.checkIdlAdaDir))
        self.debugPrint( "     effortOnly = " + str(self.effortOnly))
        self.debugPrint( "        debugOn = " + str(self.debugOn))
        self.debugPrint( "      workspace = " + self.workspace)
        self.debugPrint( "underApexSession = " + str(self.underApexSession))
        self.debugPrint("")
        
    def makeSourcePathNames(self):
        """Sets up the Source path names based on the Tower, Layer and Subsystem
            provided by the user or the calling class.
        """
        self.sourceRootPath   = "/nif/code"
        self.sourceLayerPath  = os.path.join (self.sourceRootPath, self.layerName)
        self.sourceSubsysPath = os.path.join (self.sourceLayerPath, self.subsysName)
        self.sourceViewPath   = os.path.join (self.sourceSubsysPath, self.towerName)
        self.debugPrint( "sourceLayerPath  = " + self.sourceLayerPath)
        self.debugPrint( "sourceSubsysPath = " + self.sourceSubsysPath)
        self.debugPrint( "sourceViewPath   = " + self.sourceViewPath)
        self.debugPrint("")
        
    def makeTargetPathNames(self):
        """Sets up the Target path names based on the Tower, Layer, Subsystem and
            Workspace provided by the user or the calling class.
        """
        if self.workspace == "":
            self.targetAdaRootPath  = "/nif/code/shadow"
            self.targetIdlRootPath  = os.path.join(self.targetAdaRootPath, self.towerName + "_IDL")
            self.targetIdlLinksPath = os.path.join(self.targetIdlRootPath, "links")
            self.targetAdaTowerPath  = os.path.join (self.targetAdaRootPath, self.towerName)
        else:
            self.targetAdaRootPath  = os.path.join(self.workspace, "src/ada")
            self.targetIdlRootPath  = os.path.join(self.workspace, "src/idl")
            self.targetIdlLinksPath = os.path.join(self.targetIdlRootPath, "links")
            self.targetAdaTowerPath  = self.targetAdaRootPath
        self.targetAdaLayerPath  = os.path.join(self.targetAdaTowerPath, self.layerName)
        self.targetAdaSubsysPath = os.path.join(self.targetAdaLayerPath, self.subsysName[:-3])
        self.debugPrint( "targetAdaTowerPath  = " + self.targetAdaTowerPath)
        self.debugPrint( "targetAdaLayerPath  = " + self.targetAdaLayerPath)
        self.debugPrint( "targetAdaSubsysPath = " + self.targetAdaSubsysPath)
        self.targetIdlTowerPath = self.targetIdlRootPath
        self.targetIdlLayerPath  = os.path.join(self.targetIdlTowerPath, self.layerName)
        self.targetIdlSubsysPath = os.path.join(self.targetIdlLayerPath, self.subsysName[:-3])
        self.debugPrint( "targetIdlTowerPath  = " + self.targetIdlTowerPath)
        self.debugPrint( "targetIdlLayerPath  = " + self.targetIdlLayerPath)
        self.debugPrint( "targetIdlSubsysPath = " + self.targetIdlSubsysPath)
        self.debugPrint( "targetIdlLinksPath  = " + self.targetIdlLinksPath)
        self.debugPrint("")

    def prepareTargetDirectory (self, targetDirPath):
        """Prepares target directory by removing the entire tree of the given directory.
        This is in preparation of creating a new tree with new files.
        """
        if os.path.exists(targetDirPath):
            self.runOrLog('shutil.rmtree ("' + targetDirPath + '")')
        if not os.path.exists (targetDirPath):
            self.runOrLog ('os.makedirs ("' + targetDirPath + '")')    
    
    def prepareTargetFile (self, targetFilePath):
        """Prepares to link or copy a file.  Deletes the target, 
        and creates any needed target directories.
        """
        Target_Parent_Path = os.path.dirname(targetFilePath)
        if os.path.exists (targetFilePath):
            self.runOrLog ('os.remove ("' + targetFilePath + '")')
        if not os.path.exists (Target_Parent_Path):
            self.runOrLog ('os.makedirs ("' + Target_Parent_Path + '")')    
    
    def debugPrint(self, message):
        """Display the given debug message onto the terminal
            if and only if debugging mode has been turned on.
        """
        if self.debugOn:
            print "$$$ " + self.instanceName + ": " + message
            
    def logName(self):
        """Logs the name of the instance of the Make Stree class.
        """
        self.log("")
        self.log("    Instance Name = " + self.instanceName)
        self.log("")
        
    def log(self, message):
        """Display the given message onto the terminal.
        """
        if self.verificationMode:
            if self.effortOnly:
                print "--- Would do: " + message
            else:
                print "--- Doing: " + message
        else:
            if self.effortOnly:
                print "EFFORT_ONLY " + self.instanceName + ": " + message
            else:
                print self.instanceName + ": " + message

    def runOrLog(self, command):
        """Display the command and execute the command only if the user wanted to.
        """
        self.log(command)
        if not self.effortOnly:
            exec command

    def lookForPositiveResponse(self, responseStr):
        """Analyze the given response string.
            Return True for a positive response (such as 'y', 'yes', 'Y' or 'YES')
                   False for a negative response (anything other that the positive response)
        """
        if ((responseStr == "y") or (responseStr == "yes") or
            (responseStr == "Y") or (responseStr == "YES")):
            return True
        else:
            return False
                
    def lookForNegativeResponse(self, responseStr):
        """Analyze the given response string.
            Return True for a negative response (such as 'n', 'no', 'N' or 'NO')
                   False for a positive response (anything other that the negative response)
        """
        if ((responseStr == "n") or (responseStr == "no") or
            (responseStr == "N") or (responseStr == "NO")):
            return True
        else:
            return False
                
    def askQuestion(self, questionStr):
        """Display the question to the terminal and return the response.
            Returns the response to the question.
        """
        sys.stdout.write(questionStr)
        sys.stdout.flush()
        resp = sys.stdin.readline()
        return resp.strip() # returns the response string with the '\n' striped

