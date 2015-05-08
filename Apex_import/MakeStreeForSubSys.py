#!/usr/bin/env python
"""Class definition derived from the MakeStree base class.
This class defines the method that will process directories and files
for a given Subsystem directory.
"""

__author__    = "Randy Sanchez"
__version__   = "$Revision: 1.19 $"
__date__      = "$Date: 08/01/2008 08:03:38 $"
__copyright__ = "Copyright 2008 LLNL"

import os
import shutil
import string
import sys
from MakeStreeBaseClass import *
from make_stree_utilities import *
from IccsApexCommand import *
from optparse import OptionParser
from subprocess import *

class MakeStreeForSubSys(MakeStree):
    "Make a shadow tree by a given [tower], [layer] and [subsystem]"
    
    def performLink(self, sourceFilePath, targetFilePath):
        """Perform the actual linking of the source file to the target file.
            Softlinks or hardlinks will be used based on how the user wants it.
            Also, the target file will be massaged to be a relative path
            back to the source file.
        """
        self.prepareTargetFile(targetFilePath)
        Target_Path = os.path.normpath(targetFilePath)
        # Gnat Ada programs and some others don't know about drive letters, 
        # so must use relative symbolic links.
        Slash_Count = Target_Path.count ("/")
        # Depth from root, or "/":
        Slash_Depth = Slash_Count - 1
        self.debugPrint("Target_Path depth is: " + str(Slash_Depth))
        Relative_Source_Path = sourceFilePath
        # Changed 'Slash_Depth' check from '> 0' to '> 1'
        # to make sure that the PC users can see the files also!
        while Slash_Depth > 1:
            Relative_Source_Path = "../" + Relative_Source_Path
            Slash_Depth = Slash_Depth - 1
        Relative_Source_Path = os.path.normpath (Relative_Source_Path)
        self.debugPrint ("Relative source path is: " + Relative_Source_Path)

        # Windows explorer with CIFS sees symbolic link as file.
        if self.makeHardLink:
            self.runOrLog ('os.link ("' + Relative_Source_Path + '", "' + Target_Path + '")')
        else:
            self.runOrLog ('os.symlink ("' + Relative_Source_Path + '", "' + Target_Path + '")')
        
        self.targetCount = self.targetCount + 1

    def performCopy(self, sourceFilePath, targetFilePath):
        """Perform the actual copying of the source file to the target file.
        """
        self.prepareTargetFile(targetFilePath)
        self.runOrLog('shutil.copy2 ("' + sourceFilePath + '", "' + targetFilePath + '")')
        self.targetCount = self.targetCount + 1

    def makeTheFile(self, sourceFilePath, targetFilePath, alwaysLink=False):
        """Setup to perform the actual link, copy or move.
        """
        if self.makeSoftLink:
            self.debugPrint("making a softlink from " + sourceFilePath)
            self.debugPrint("                    to " + targetFilePath)
            self.performLink(sourceFilePath, targetFilePath)
        elif self.makeHardLink:
            self.debugPrint("making a hardlink from " + sourceFilePath)
            self.debugPrint("                    to " + targetFilePath)
            self.performLink(sourceFilePath, targetFilePath)
        elif self.makeCopy:
            if (alwaysLink):
                self.debugPrint("making a softlink from " + sourceFilePath)
                self.debugPrint("                    to " + targetFilePath)
                self.performLink(sourceFilePath, targetFilePath)
                return
            self.debugPrint("     copying file from " + sourceFilePath)
            self.debugPrint("                    to " + targetFilePath)
            self.performCopy(sourceFilePath, targetFilePath)
        else:
            self.debugPrint("NO WORK TO BE PERFORMED ON " + sourceFilePath)
        
    def aaaOsSpecificFile(self, sourceFilePath):
        """Determine if the given file resides under an 'AAA_os_specific' directory.
        """
        if (sourceFilePath.find("/AAA_os_specific/") > 0):
            return True
        else:
            return False

    def processAaaOsSpecificFile(self, sourceFilePath, targetFilePath, alwaysLink=False):
        """Change the path of an OS specific file.
            Change the path from:
                    <target>/<layer>/<subsys>/.../AAA_os_specific/<platform>/<file>
                            to:
                    <target>/AAA_os_specific/<platform>/<layer>/<subsys>/.../<file>
        """
        Name_List = targetFilePath.split("/")
        Layer_Just_Found = False
        Layer_Found = False
        Layer_Dirname = ""
        Subsys_Found = False
        Subsys_Dirname = ""
        Os_Specific_Dir_Found = False
        Os_Specific_Dirname = "AAA_os_specific"
        Platform_Found = False
        Platform_Dirname = Name_List[len(Name_List)-2]
        New_List = []
        for dirname in Name_List:
            if (dirname == ""):
                continue
            if (not Layer_Found):
                for Layer in apex.NIF_Layers:
                    if (dirname == Layer):
                        Layer_Found = True
                        Layer_Just_Found = True
                        Layer_Dirname = dirname
                        New_List = New_List + [Os_Specific_Dirname]
                        break # for Layer loop
                if (not Layer_Found):
                    New_List = New_List + [dirname]
            elif (not Subsys_Found):
                if (Layer_Just_Found):
                    Subsys_Found = True
                    Subsys_Dirname = dirname
                    New_List = New_List + [Platform_Dirname]
                    New_List = New_List + [Layer_Dirname]
                    New_List = New_List + [Subsys_Dirname]
                    Layer_Just_Found = False
                if (not Subsys_Found):
                    New_List = New_List + [dirname]
            elif (not Os_Specific_Dir_Found):
                if (dirname == Os_Specific_Dirname):
                    Os_Specific_Dir_Found = True
                if (not Os_Specific_Dir_Found):
                    New_List = New_List + [dirname]
            elif (not Platform_Found):
                if (dirname == Platform_Dirname):
                    Platform_Found = True
                if (not Platform_Found):
                    New_List = New_List + [dirname]
            else:
                New_List = New_List + [dirname]
        New_Target_Filename_Path = "/" + "/".join(New_List)
        self.debugPrint("OS specific file: " + os.path.basename(sourceFilePath))
        self.debugPrint("          sourceFilePath = " + sourceFilePath)
        self.debugPrint("          targetFilePath = " + targetFilePath)
        self.debugPrint("New_Target_Filename_Path = " + New_Target_Filename_Path)
        self.makeTheFile(sourceFilePath, New_Target_Filename_Path, alwaysLink)

    def processApexFile(self, sourcePath, targetPath, filename):
        """Process the link or copy of the given Apex Ada file.
            Only if the given file is a valid Ada file.
        """
        if not isAdaFile(filename):
#            self.debugPrint("not an Ada file!")
            return
        if isApexFile(filename):
            fromFilename = filename
            toFilename   = filename
        elif isGnatFile(filename):
            fromFilename = filename
            toFilename   = fromGnatToApex(filename)
        else:
            self.debugPrint("invalid filename got thru: " + filename)
            return
        
        sourceFilePath = os.path.join(sourcePath, fromFilename)
        targetFilePath = os.path.join(targetPath, toFilename)
        if (self.aaaOsSpecificFile(sourceFilePath)):
            self.processAaaOsSpecificFile(sourceFilePath, targetFilePath)
        else:
            self.makeTheFile(sourceFilePath, targetFilePath)
            
    def processGnatFile(self, sourcePath, targetPath, filename):
        """Process the link or copy of the given Gnat Ada file.
            Only if the given file is a valid Ada file.
        """
        if not isAdaFile(filename):
#            self.debugPrint("not an Ada file!")
            return
        if isApexFile(filename):
            fromFilename = filename
            toFilename   = fromApexToGnat(filename)
        elif isGnatFile(filename):
            fromFilename = filename
            toFilename   = filename
        else:
            self.debugPrint("invalid filename got thru: " + filename)
            return
        
        sourceFilePath = os.path.join(sourcePath, fromFilename)
        targetFilePath = os.path.join(targetPath, toFilename)
        if (self.aaaOsSpecificFile(sourceFilePath)):
            self.processAaaOsSpecificFile(sourceFilePath, targetFilePath)
        else:
            self.makeTheFile(sourceFilePath, targetFilePath)

    def processIdlFile(self, sourcePath, targetPath, filename):
        """Process the link or copy of the given Idl file.
            Only if the given file is a valid Idl file.
            NOTE: The Idl file is linked or copied to two places.
                  That is why there are two calls to 'makeTheFile()'.
        """
        if not isIdlFile(filename):
#            self.debugPrint("not an IDL file!")
            return
        
        sourceFilePath = os.path.join(sourcePath, filename)

        targetDirName = os.path.basename(targetPath)
        if (targetDirName == "IDL"):
            targetPathLessIdlDir = os.path.dirname(targetPath)
            targetFilePath = os.path.join(targetPathLessIdlDir, filename)
        else:
            targetFilePath = os.path.join(targetPath, filename)
            
        targetFileIdlPath = os.path.join(self.targetIdlLinksPath, filename)
        if (self.aaaOsSpecificFile(sourceFilePath)):
            self.processAaaOsSpecificFile(sourceFilePath, targetFilePath)
            self.processAaaOsSpecificFile(sourceFilePath, targetFilePath, True)
        else:
            self.makeTheFile(sourceFilePath, targetFilePath)
            self.makeTheFile(targetFilePath, targetFileIdlPath, True)

    def removeIdlAdaDirectory(self, sourcePath, controlledFileList):
        """Process the removal of the IDL Ada directory 'IDL_Ada'.
        """
        if (len(controlledFileList) > 0):
            self.log("*****")
            self.log("***** Directory: " + sourcePath)
            self.log("*****")
            self.log("***** WARNING: There are one or more files in this directory")
            self.log("*****          that are still Controlled by APEX!")
            self.log("*****")
            for fname in controlledFileList:
                self.log("*****          " + fname)
            self.log("*****")
            self.log("*****          This directory will NOT be removed!")
            self.log("*****")
        else:
            self.runOrLog('shutil.rmtree ("' + sourcePath + '")')
               
    def listNotReadyToBeMovedFiles(self, sourcePath, controlledFileList):
        """Process the list of files that are NOT ready to be moved.
        """
        if (len(controlledFileList) > 0):
            self.log("*****")
            self.log("***** Directory: " + sourcePath)
            self.log("*****")
            self.log("***** WARNING: There are one or more files in this directory")
            self.log("*****          that are NOT ready to be moved!")
            self.log("*****")
            for fname in controlledFileList:
                self.log("*****          " + fname)
            self.log("*****")
            self.log("*****          These files CANNOT be moved at this time!")
            self.log("*****          Fix the problems then run this command again!")
            self.log("*****          Once all files are ready to be moved then run the move command!")
            self.log("*****")
               
    def processApexResultsList(self, apexCommandName, resultsTupleList):
        """Process the results of the given APEX command.
            The tuple found within the list is as follows:
                (filename, results)
            where filename is the name of the file the command was issued on
              and results  is the result of the command True for success
                                                    and False for failure
            Returns a tuple of lists as follows:
                (Success_List, Failed_List)
        """
        Succeeded_List = []
        Failed_List    = []
        for (filename, results) in resultsTupleList:
            if (results):
                if (self.effortOnly):
                    Result_Stream = "Would have SUCCEEDED"
                else:
                    Result_Stream = "SUCCEEDED"
                self.debugPrint("    APEX [" + apexCommandName + 
                                "] command " + Result_Stream + " on file: " + filename)
                Succeeded_List = Succeeded_List + [filename]
            else:
                Failed_List = Failed_List + [filename]
                self.log("    APEX [" + apexCommandName + "] command FAILED on file: " + filename)
        
        return (Succeeded_List, Failed_List)
    
    def logFailuresAndAsk(self, actionThatFailed, failedList):
        self.log("*****")
        self.log("***** ERROR: One or more files failed to be " + actionThatFailed + "!")
        for fname in failedList:
            self.log("*****            " + fname)
        self.log("*****")
        Question_Stream = "Do you want to continue processing? (y/n) "
        if (self.lookForPositiveResponse(self.askQuestion(Question_Stream))):
            self.log("*****")
            self.log("***** WARNING: The user requested to continue processing!")
            self.log("*****          The files that failed to be " +
                                            actionThatFailed + " should be handled!")
        else:
            self.log("*****")
            self.log("***** ERROR: The user requested to stop processing at this time!")
            sys.stdout.flush()
            os._exit(19)

    def duplicateIdlAdaFiles(self, updatedFileList, nonExistingInfix, existingInfix, generalTargetDestination):
        """Duplicate the files, based on the given list of files, that are contained
            in a given set of <infix> duplicate directories to the general target directory.
            The general target directory is where the given files were moved.
            Now these moved files need to be duplicated in the 
        """
        if (not iccs_apex.isValidInfixStream(self.towerName)):
            return
        if (len(updatedFileList) == 0):
            return

        New_Duplicate_List = self.apex_command.newDuplicateFiles(updatedFileList, 
                                                                 nonExistingInfix, existingInfix)
        New_Destination = self.apex_command.newDestinationStream(generalTargetDestination,
                                                                 existingInfix, nonExistingInfix)
        Success_List = []
        Failure_List = []
        File_List = []
        for Entry in New_Duplicate_List:
            File_List = File_List + [Entry]
            if (len(File_List) >= self.maxFilesPerApexUpdate):
                Results_List = self.apex_command.duplicateFileListVersion(File_List, New_Destination)
                File_List = []
                Succeeded_List, Failed_List = self.processApexResultsList(apex.Update_Command,
                                                                          Results_List)
                Success_List = Success_List + Succeeded_List
                Failure_List = Failure_List + Failed_List
                
        if (len(File_List) > 0):
            Results_List = self.apex_command.duplicateFileListVersion(File_List, New_Destination)
            File_List = []
            Succeeded_List, Failed_List = self.processApexResultsList(apex.Update_Command,
                                                                      Results_List)
            Success_List = Success_List + Succeeded_List
            Failure_List = Failure_List + Failed_List
        
        self.duplicateCount = self.duplicateCount + len(Success_List)
                        
        if (len(Failure_List) > 0):
            self.logFailuresAndAsk("duplicated", Failure_List)
            

    def updateDuplicateIdlAdaFiles(self, controlledFileList, targetDirectory):
        """Update the files, based on the given list of files, that are contained
            in a given set of <infix> duplicate directories.  If the original file
            has been moved, then the duplicate file will now have a 'Deleted' entry.
            Updating the duplicate file to its latest version will remove the duplicate
            file from the directory.
        """
        if (not iccs_apex.isValidInfixStream(self.towerName)):
            return
        if (len(controlledFileList) == 0):
            return

        My_Infix_Stream = iccs_apex.whatInfixIsStream(self.towerName)
        View_Type_List = []
        View_Type_List = View_Type_List + ["working"]
        View_Type_List = View_Type_List + ["release"]
        for vtype in View_Type_List:
            for infixStream in iccs_apex.getInfixList():
                if ((infixStream == My_Infix_Stream) and (vtype == "working")):
                    continue    # for loop
                if (vtype == "working"):
                    Duplicate_List = self.apex_command.findDuplicateWorkingFiles(controlledFileList, 
                                                                  My_Infix_Stream, infixStream)
                else:
                    Duplicate_List = self.apex_command.findDuplicateReleaseFiles(controlledFileList, 
                                                                  self.towerName, infixStream)
                if (len(Duplicate_List) <= 0):
                    self.debugPrint("    No duplicate entries for '" + vtype + "' <infix>: " + infixStream)
                    continue
                self.debugPrint("Duplicate '" + vtype + "' List:")
                for fname in Duplicate_List:
                    self.debugPrint("    fname = " + fname)
            
                Success_List = []
                Failure_List = []
                File_List = []
                for Entry in Duplicate_List:
                    File_List = File_List + [Entry]
                    if (len(File_List) >= self.maxFilesPerApexUpdate):
                        Results_List = self.apex_command.updateFileListToLatest(File_List)
                        File_List = []
                        Succeeded_List, Failed_List = self.processApexResultsList(apex.Update_Command, 
                                                                                Results_List)
                        Success_List = Success_List + Succeeded_List
                        Failure_List = Failure_List + Failed_List
            
                if (len(File_List) > 0):
                    Results_List = self.apex_command.updateFileListToLatest(File_List)
                    File_List = []
                    Succeeded_List, Failed_List = self.processApexResultsList(apex.Move_Object_Command, 
                                                                                Results_List)
                    Success_List = Success_List + Succeeded_List
                    Failure_List = Failure_List + Failed_List
                
                if (len(Success_List) > 0):
                    self.latestCount = self.latestCount + len(Success_List)
                    if (vtype == "working"):
                        self.duplicateIdlAdaFiles(Success_List, infixStream, 
                                                  My_Infix_Stream, targetDirectory)
                    else:
                        Release_Tower = self.apex_command.getReleaseVersion(self.towerName, infixStream)
                        self.duplicateIdlAdaFiles(Success_List, Release_Tower, 
                                                  self.towerName, targetDirectory)
                
                if (len(Failure_List) > 0):
                    self.logFailuresAndAsk("updated to their latest version", Failure_List)

    def moveIdlAdaFiles(self, controlledFileList, targetDirectory):
        """Move all of the files in the given list to the target directory.
        """
        
        Succeeded_List = []
        Failed_List    = []
        Success_List = []
        Failure_List = []
        File_List    = []
        for Entry in controlledFileList:
            File_List = File_List + [Entry]
            if (len(File_List) >= self.maxFilesPerApexMove):
                Results_List = self.apex_command.moveFileListToDir(File_List, targetDirectory)
                File_List = []
                Succeeded_List, Failed_List = self.processApexResultsList(apex.Move_Object_Command, 
                                                                          Results_List)
                Success_List = Success_List + Succeeded_List
                Failure_List = Failure_List + Failed_List
        
        # if the File List is not empty then you have files left over to be moved
        if (len(File_List) > 0): 
            Results_List = self.apex_command.moveFileListToDir(File_List, targetDirectory)
            File_List = []
            Succeeded_List, Failed_List = self.processApexResultsList(apex.Move_Object_Command, 
                                                                      Results_List)
            Success_List = Success_List + Succeeded_List
            Failure_List = Failure_List + Failed_List

        self.moveCount = self.moveCount + len(Success_List)
        self.updateDuplicateIdlAdaFiles(Success_List, targetDirectory)
        
        if (len(Failure_List) > 0):
            self.logFailuresAndAsk("moved", Failure_List)

    def processIdlAdaDirectory(self, sourcePath):
        """Process the IDL_Ada directory
           based on the command line options the user has chosen.
        """
        if not (self.removeIdlAdaDir or self.moveIdlAda or self.checkIdlAdaDir):
            self.log("User does not want to process the IDL_Ada directory!")
            return
        
        self.debugPrint("#####    DebugOn => " + str(self.debugOn))
        self.debugPrint("##### EffortOnly => " + str(self.effortOnly))
        self.apex_command = IccsApexCommand(self.debugOn, self.effortOnly)
        Controlled_File_List = []
        Pipe_Tuple_List = []
        Entries = os.listdir (sourcePath)
        File_List = []
        for Entry in Entries:
            Entry_Source = os.path.join(sourcePath, Entry)
            if os.path.isdir(Entry_Source):
                if os.path.islink (Entry_Source):
                    continue # continue processing entries, don't follow a directory link
                self.debugPrint("")
                self.debugPrint(" Directory = " + Entry)
                self.log("***** ERROR: The following directory entry was found:")
                self.log("*****            " + Entry_Source)
                self.log("*****        This utility will not process directories under the IDL_Ada directory.")
                self.log("*****        This utility has halted processing pending an answer to a question.")
                self.log("*****")
                sys.stdout.flush()
                Question_Stream = "Do you want to continue processing? (y/n) "
                if (self.lookForPositiveResponse(self.askQuestion(Question_Stream))):
                    self.log("*****")
                    self.log("***** WARNING: The user requested to ignore the directory found ")
                    self.log("*****          under the IDL_Ada directory and continue processing!")
                else:
                    self.log("*****")
                    self.log("***** ERROR: The user requested to stop processing at this time!")
                    sys.stdout.flush()
                    os._exit(59)
            else:
                self.debugPrint("      File = " + Entry)
                self.filesProcessed = self.filesProcessed + 1
                self.statusCount    = self.statusCount + 1
                File_List = File_List + [Entry_Source]
                if (len(File_List) >= self.maxFilesPerApexStatus):
                    if self.checkIdlAdaDir:
                        Results_List = self.apex_command.isFileListReadyToMove(File_List)
                    else:
                        Results_List = self.apex_command.isFileListControlled(File_List)
                    File_List = []
                    for (fname, results) in Results_List:
                        if self.checkIdlAdaDir:
                            if results == False:
                                # load the controlled files that are NOT ready to be moved!
                                Controlled_File_List = Controlled_File_List + [fname]
                        else:                   
                            if results:
                                # load the controlled files that are ready to be moved!
                                Controlled_File_List = Controlled_File_List + [fname]
        
        # if there are any files left over in the File_List that have not been processed
        if (len(File_List) > 0):
            if self.checkIdlAdaDir:
                Results_List = self.apex_command.isFileListReadyToMove(File_List)
            else:
                Results_List = self.apex_command.isFileListControlled(File_List)
            File_List = []
            for (fname, results) in Results_List:
                if self.checkIdlAdaDir:
                    if results == False:
                        # load the controlled files that are NOT ready to be moved!
                        Controlled_File_List = Controlled_File_List + [fname]
                else:                   
                    if results:
                        # load the controlled files that are ready to be moved!
                        Controlled_File_List = Controlled_File_List + [fname]
                
        if self.removeIdlAdaDir == True:
            self.removeIdlAdaDirectory(sourcePath, Controlled_File_List)
        if self.moveIdlAda == True:
            Target_Dir = os.path.dirname(sourcePath)
            self.moveIdlAdaFiles(Controlled_File_List, Target_Dir)    
        if self.checkIdlAdaDir == True:
            self.listNotReadyToBeMovedFiles(sourcePath, Controlled_File_List)        

    def processFile(self, sourcePath, targetAdaPath, targetIdlPath, filename):
        """Process the given file.  Calling the appropriate method to create
            the appropriate type of file (Apex file, Gnat file, Idl file, ...)
        """
        if self.createApex:
            self.processApexFile(sourcePath, targetAdaPath, filename)
        if self.createGnat:
            self.processGnatFile(sourcePath, targetAdaPath, filename)
        if self.createIdl:
            self.processIdlFile(sourcePath, targetIdlPath, filename)
    
    def processDir(self, sourcePath, targetAdaPath, targetIdlPath):
        """Recursively process a given directory path.
            When a file is found it will be processed as a file.
        """
        self.debugPrint( "   sourcePath = " + sourcePath)
        self.debugPrint( "targetAdaPath = " + targetAdaPath)
        self.debugPrint( "targetIdlPath = " + targetIdlPath)
        Entries = os.listdir (sourcePath)
        for Skip_Dir in apex.Internal_Dirs:
            if Skip_Dir in Entries:
                Entries.remove (Skip_Dir)
        for Entry in Entries:
            Entry_Source = os.path.join(sourcePath, Entry)
            if os.path.isdir(Entry_Source):
                if os.path.islink (Entry_Source):
                    continue # continue processing entries, don't follow a directory link
                self.debugPrint("")
                self.debugPrint(" Directory = " + Entry)
                self.dirsProcessed = self.dirsProcessed + 1
                if Entry == apex.IDL_Ada_Dir:
                    self.processIdlAdaDirectory(Entry_Source)
                else:
                    Entry_Ada_Target = os.path.join(targetAdaPath, Entry)
                    Entry_Idl_Target = os.path.join(targetIdlPath, Entry)
                    self.processDir(Entry_Source, Entry_Ada_Target, Entry_Idl_Target)
            else:
                self.debugPrint("      File = " + Entry)
                if isAdaFile(Entry) or isIdlFile(Entry):
                    self.filesProcessed = self.filesProcessed + 1
                    self.processFile(sourcePath, targetAdaPath, targetIdlPath, Entry)
#                else:
#                    self.debugPrint("         this file is NOT an ADA file!")
    
