#!/usr/bin/env python
"""Base class definition that implements the basic APEX commands.
This class defines methods that will process APEX commands.
"""

__author__    = "Randy Sanchez"
__version__   = "$Revision: 1.10 $"
__date__      = "$Date: 08/07/2008 07:49:56 $"
__copyright__ = "Copyright 2008 LLNL"

import apex
import os
import string
from StringIO import *
from subprocess import *

class ApexCommand:
    "Apex command implementation base class"
    
    def __init__(self, debugOn, effortOnly):
        """Initializes the instance variables associated with the class
        """
        self.__debugOn    = debugOn
        self.__effortOnly = effortOnly
    
    def log(self, message):
	    """Display the given message onto the terminal.
	    """
	    if self.__effortOnly:
		   print "EFFORT_ONLY " + message
	    else:
		   print message

    def debugPrint(self, message):
        """Display the given debug message onto the terminal
            if and only if debugging mode has been turned on.
        """
        if self.__debugOn:
            print "$$$ " + message

    def setDebugOn(self, debugOn):
        """Set the class variable to what was passed
        """
        if (debugOn == True):
            self.__debugOn = True
        else:
            self.__debugOn = False

    def setEffortOnly(self, effortOnly):
        """Set the class variable to what was passed
        """
        if (effortOnly == True):
            self.__effortOnly = True
        else:
            self.__effortOnly = False

    def isFileControlled(self, filename):
        """Performs the APEX 'show_status' command to determine if the given file
            is an APEX controlled file.
            Returns True if the filename is an APEX Controlled file.
            Returns False if the filename is an APEX Uncontrolled file.
            The APEX command performed is as follows:
                apex show_status -all <filename>
        """
        resultList = self.isFileListControlled([filename])
        (fname, results) = resultList[0]
        return results

    def isFileListControlled(self, filenameList):
        """Performs the APEX 'show_status' command to determine if the given
            list of files are APEX controlled files.
            Returns a tuple list containing a filename and a boolean.
                The filename is the name of the file from the list and the
                boolean is True if the filename is an APEX Controlled file
                and False if the filename is an APEX Uncontrolled file.
            The APEX command performed is as follows:
                apex show_status -all <filenameList>
        """
        Popen_Args_List = self.buildShowStatusCommand(filenameList)
        self.dumpPopenArgs(apex.Show_Status_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        return self.analyzeShowStatusResults(filenameList, Results_Stream)

    def isFileReadyToMove(self, filename):
        """Performs the APEX 'show_status' command to determine if the given file
            is an APEX controlled file and is 'ready to be moved'.
            Being 'ready to move' means the following:
                The file is checked-in.
                The file is at the latest version.
            Returns True if the filename is an APEX Controlled file and is ready to be moved or
                            the filename is an APEX Uncontrolled file
                            (in this case the Uncontrolled file will not affect a move).
            Returns False if the filename is an APEX Controlled file that is NOT ready to be moved.
            The APEX command performed is as follows:
                apex show_status -all <filename>
        """
        resultList = self.isFileListReadyToMove([filename])
        (fname, results) = resultList[0]
        return results

    def isFileListReadyToMove(self, filenameList):
        """Performs the APEX 'show_status' command to determine if the given
            list of files are APEX controlled files and are 'ready to be moved'.
            Being 'ready to move' means the following:
                The file is checked-in.
                The file is at the latest version.
            Returns a tuple list containing a filename and a boolean.
                The filename is the name of the file from the list and the
                boolean is True if the filename is an APEX Controlled file that is ready to be moved
                                        or an Uncontrolled APEX file which would not affect a move
                and False if the filename is an APEX Controlled file that is NOT ready to be moved.
            The APEX command performed is as follows:
                apex show_status -all <filenameList>
        """
        Popen_Args_List = self.buildShowStatusVerboseCommand(filenameList)
        self.dumpPopenArgs(apex.Show_Status_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        return self.analyzeShowStatusResultsForReadiness(filenameList, Results_Stream)

    def moveFileToDir(self, filename, dirname):
        """Performs an APEX move of the given file to the given directory.
            Returns True if the filename has been moved.
            Returns False otherwise.
            The APEX command performed is as follows:
                apex move -set all <filename> <dirname>
        """
        resultList = self.moveFileListToDir([filename], dirname)
        (fname, results) = resultList[0]
        return results

    def makeNewWorkingView(self, viewName):
        """Performs an APEX create_working command to create the new viewName in the current directory.
            Returns True if the view has been created.
            Returns False otherwise.
            The APEX command performed is as follows:
                apex create_working -group inherit -access_category group_public
                        -model "" <viewName>
        """
        Popen_Args_List = self.buildCreateWorkingCommand(viewName)
        self.dumpPopenArgs(apex.Create_Working_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        return self.analyzeCreateResults(apex.Create_Working_Command, Results_Stream)

    def makeNewReleaseView(self, viewName):
        """Performs an APEX create_working command to create the new viewName in the current directory.
            Returns True if the view has been created.
            Returns False otherwise.
            The APEX command performed is as follows:
                apex create_release -group inherit -access_category group_public
                        -model "" <viewName>
        """
        Popen_Args_List = self.buildCreateReleaseCommand(viewName)
        self.dumpPopenArgs(apex.Create_Release_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        return self.analyzeCreateResults(apex.Create_Release_Command, Results_Stream)

    def moveFileListToDir(self, filenameList, dirname):
        """Performs an APEX move on the given list of files to the given directory.
            Returns a tuple list containing a filename and a boolean.
                The filename is the name of the file from the list and the
                boolean is True if the filename was moved and False if it wasn't.
            The APEX command performed is as follows:
                apex move -set all <filenameList> <dirname>
        """
        Popen_Args_List = self.buildMoveCommand(filenameList, dirname)
        self.dumpPopenArgs(apex.Move_Object_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        return self.analyzeResults(apex.Move_Object_Command, filenameList, Results_Stream)

    def updateFileToLatest(self, filename):
        """Performs the APEX 'accept_changes' command to update the given file
            to its latest version.
            Returns True if the filename has been updated to the latest version.
            Returns False otherwise.
            The APEX command performed is as follows:
                apex accept_changes +no_artifacts -expand_configurations -latest +control <filename>
        """
        resultList = self.updateFileListToLatest([filename])
        (fname, results) = resultList[0]
        return results

    def updateFileListToLatest(self, filenameList):
        """Performs the APEX 'accept_changes' command to update the given
            list of files to their latest versions.
            Returns a tuple list containing a filename and a boolean.
                The filename is the name of the file from the list and the
                boolean is True if the filename was updated and False if it wasn't.
            The APEX command performed is as follows:
                apex accept_changes +no_artifacts -expand_configurations -latest +control <filenameList>
        """
        Popen_Args_List = self.buildUpdateToLatestCommand(filenameList)
        self.dumpPopenArgs(apex.Update_To_Latest_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        return self.analyzeResults(apex.Update_To_Latest_Command, filenameList, Results_Stream)

    def copyDirectory(self, sourcePath, destinationName): 
        """Performs the APEX 'accept_changes' command to duplicate the contents of the
            'sourcePath' directory into the 'destinationName' directory name.
            It is assumed that the caller has changed directories to the parent directory
            of the 'destinationName' location.
            Returns True if the 'source' directory has been copied to the destination location.
            Returns False otherwise.
            The APEX command performed is as follows:
                apex accept_changes +no_artifacts -expand_configurations -source <sourcePath>
                    -new_history acceptable_history +control <destinationName>
        """
        Popen_Args_List = self.buildDuplicateVersionCommand([sourcePath], destinationName, False)
        self.dumpPopenArgs(apex.Duplicate_Version_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        return self.analyzeCopyResults(apex.Duplicate_Version_Command, Results_Stream)

    def copyFileAsIs(self, sourcePath, destinationName): 
        """Performs the APEX 'accept_changes' command to duplicate the contents of the
            'sourcePath' file into the 'destinationName' directory name or file name.
            Returns True if the 'source' file has been copied to the destination location.
            Returns False otherwise.
            The APEX command performed is as follows:
                apex accept_changes +no_artifacts -expand_configurations -source <sourcePath>
                    -new_history all +control <destinationName>
        """
        Current_Working_Dir = os.getcwd()
        if (os.path.isfile(destinationName)):
            Destination_Dir = os.path.dirname(destinationName)
        else:
            Destination_Dir = destinationName
        os.chdir(Destination_Dir)
        Popen_Args_List = self.buildDuplicateVersionCommand([sourcePath], destinationName, True)
        self.dumpPopenArgs(apex.Duplicate_Version_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        os.chdir(Current_Working_Dir)
        resultList = self.analyzeCopyResults(apex.Duplicate_Version_Command, Results_Stream)
        (fname, results) = resultList[0]
        return results

    def buildCopyCommand(self, fromFile, toFileOrDir):
        """Build a list that contains the APEX 'copy' command to copy the given file
            to the given directory or filename.
            Format for APEX 'copy' command:
                apex copy fromFile toFileOrDir
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command]
        Popen_Args = Popen_Args + [apex.Copy_Command]
        Popen_Args = Popen_Args + [fromFile]
        Popen_Args = Popen_Args + [toFileOrDir]
        return Popen_Args

    def copyFile(self, sourcePath, destinationName): 
        """Performs the APEX 'copy' command to copy the contents of the 'sourcePath' file
            into the 'destinationName' directory name or file name.
            Returns True if the 'source' file has been copied to the destination location.
            Returns False otherwise.
            The APEX command performed is as follows:
                apex copy <sourcePath> <destinationName>
        """
        Current_Working_Dir = os.getcwd()
        if (os.path.isfile(destinationName)):
            Destination_Dir = os.path.dirname(destinationName)
        else:
            Destination_Dir = destinationName
        os.chdir(Destination_Dir)
        Popen_Args_List = self.buildCopyCommand(sourcePath, destinationName)
        self.dumpPopenArgs(apex.Copy_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        os.chdir(Current_Working_Dir)
        resultList = self.analyzeCopyResults(apex.Copy_Command, Results_Stream)
        (fname, results) = resultList[0]
        return results

    def forceCopyOfFile(self, sourcePath, destinationName): 
        """Performs the APEX 'accept_changes' command to make an identical duplicate of the contents of the
            'sourcePath' file into the 'destinationName' directory name or file name.
            Returns True if the 'source' file has been copied to the destination location.
            Returns False otherwise.
            The APEX command performed is as follows:
                apex accept_changes +no_artifacts -expand_configurations -identical
                    -source <sourcePath> -save -control <destinationName>
        """
        Current_Working_Dir = os.getcwd()
        if (os.path.isfile(destinationName)):
            Destination_Dir = os.path.dirname(destinationName)
        else:
            Destination_Dir = destinationName
        os.chdir(Destination_Dir)
        Popen_Args_List = self.buildIdenticalVersionCommand([sourcePath], destinationName)
        self.dumpPopenArgs(apex.Duplicate_Version_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        os.chdir(Current_Working_Dir)
        resultList = self.analyzeCopyResults(apex.Duplicate_Version_Command, Results_Stream)
        (fname, results) = resultList[0]
        return results

    def compareViews(self, baselineView, currentView): 
        """Performs the APEX 'compare' command to compare the contents of the
            'baselineView' directory against the 'currentView' directory name.
            Returns a list of tuples (that contain the difference token and the name of the file)
                    if the baselineView and currentView are not exactly the same.
            Returns an empty list of tuples otherwise.
            The APEX command performed is as follows:
                apex compare -controlled <baselineView> <currentView>
        """
        Popen_Args_List = self.buildCompareViewsCommand(baselineView, currentView)
        self.dumpPopenArgs(apex.Compare_Views_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        return self.analyzeCompareResults(apex.Compare_Views_Command, Results_Stream)

    def duplicateFileVersion(self, filename, destination): 
        """Performs the APEX 'accept_changes' command to create a duplicate version of the
            file in the given directory.
            Returns True if the filename has been duplicated in the destination location.
            Returns False otherwise.
            The APEX command performed is as follows:
                apex accept_changes +no_artifacts -expand_configurations -source <filename>
                    -new_history acceptable_history +control <destination>
        """
        resultList = self.duplicateFileListVersion([filename], destination)
        (fname, results) = resultList[0]
        return results

    def duplicateFileListVersion(self, filenameList, destination):
        """Performs the APEX 'accept_changes' command to create a duplicate version of the
            list of files in the given directory.
            Returns a tuple list containing a filename and a boolean.
                The filename is the name of the file from the list and the
                boolean is True if the filename was duplicated and False if it wasn't.
            The APEX command performed is as follows:
                apex accept_changes +no_artifacts -expand_configurations -source <filenameList>
                    -new_history acceptable_history +control <destination>
        """
        Popen_Args_List = self.buildDuplicateVersionCommand(filenameList, destination, False)
        self.dumpPopenArgs(apex.Duplicate_Version_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        return self.analyzeResults(apex.Duplicate_Version_Command, filenameList, Results_Stream)

    def getSwitchInfo(self, viewName, switchName):
        """Performs the APEX 'show_switches' command to show the switch information for a given APEX switch.
            This method returns the information contained in the given APEX switch upon successful execution.
            Upon failure it will return 'NoSwItChInFo'
            The APEX command performed is as follows:
                apex show_switches <viewName> -switch <switchName>
        """
        Popen_Args_List = self.buildShowSwitchesCommand(viewName, switchName)
        self.dumpPopenArgs(apex.Show_Switches_Command, Popen_Args_List)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        return self.analyzeShowSwitchesResults(apex.Show_Switches_Command, switchName, Results_Stream)

    def buildShowSwitchesCommand(self, viewName, switchName):
        """Build a list that contains the APEX 'show_switches' command to display the switch information
            for the given view name.
            Format for APEX show_switches command:
                apex show_switches <viewName> -switch <switchName>
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command]
        Popen_Args = Popen_Args + [apex.Show_Switches_Command]
        Popen_Args = Popen_Args + [viewName]
        Popen_Args = Popen_Args + ["-switch"] + [switchName]
        return Popen_Args

    def analyzeShowSwitchesResults(self, commandName, switchName, resultsStream):
        """Analyze the results found within the resultsStream from the 'show_switches' APEX command.
            The results stream will either have the name of the switch at the beginning of the line
            with its contents following the colon(:) or
            an error indicator string '***' stating the problem.
        """
        Dump_Output_Upon_Error = False
        self.debugPrint(resultsStream)
        Command_Failed = False
        Switches = "NoSwItChInFo"
        Sptr  = StringIO(resultsStream)
        try:
            for line in Sptr:
#               self.debugPrint("line = [" + line + "]")
                if (string.find(line, " *** ") >= 0):
                    self.debugPrint("    'show_switches' failed!")
                    Idx = string.find(line, " *** ");
                    self.log("'show_switches' command failed: " + line[Idx+5:])
                    Command_Failed = True
                    Dump_Output_Upon_Error = True
                    break # for loop
                if (string.find(line, switchName) == 0):
                    self.debugPrint("    Switch Name: [" + switchName + "] found!")
                    if (string.find(line, ": ") >= 0):
                        Idx = string.find(line, ": ")
                        Switches = line[Idx+2:]
                        break # for loop
        finally:
            Sptr.close()

        if (Dump_Output_Upon_Error):
            if (not self.__debugOn):
                self.log(resultsStream)
        
        if (Switches == "NoSwItChInFo"):
            Command_Failed = True
        self.debugPrint("Switches = [" + Switches + "]")
        return (Command_Failed, Switches)

    def setSwitchInfo(self, viewName, switchName, switchInfo):
        """Performs the APEX 'set_switch' command to set the switch information for a given APEX switch.
            This method returns True for successfully setting the switch information
            or False for failure to set the switch information.
            The 'set_switch' command must be in the appropriate directory/viewName to set the switch.
            The APEX command performed is as follows:
                apex set_switch <switchName> <switchInfo>
        """
        Popen_Args_List = self.buildSetSwitchCommand(switchName, switchInfo)
        self.dumpPopenArgs(apex.Set_Switch_Command, Popen_Args_List)
        Current_Working_Dir = os.getcwd()
        os.chdir(viewName)
        Results_Stream = self.issueApexCommand(Popen_Args_List)
        os.chdir(Current_Working_Dir)
        return self.analyzeSetSwitchResults(apex.Set_Switch_Command, switchName, Results_Stream)

    def buildSetSwitchCommand(self, switchName, switchInfo):
        """Build a list that contains the APEX 'set_switch' command to set the switch information
            for the given switch name.
            Format for APEX set_switch command:
                apex set_switch <switchName> "<switchInfo>"
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command]
        Popen_Args = Popen_Args + [apex.Set_Switch_Command]
        Popen_Args = Popen_Args + [switchName] + ["\"" + switchInfo + "\""]
        return Popen_Args

    def analyzeSetSwitchResults(self, commandName, switchName, resultsStream):
        """Analyze the results found within the resultsStream from the 'show_switches' APEX command.
            The results stream will either have the name of the switch at the beginning of the line
            with its contents following the colon(:) or
            an error indicator string '***' stating the problem.
        """
        Dump_Output_Upon_Error = False
        self.debugPrint(resultsStream)
        Command_Succeeded = True
        Sptr  = StringIO(resultsStream)
        try:
            for line in Sptr:
#               self.debugPrint("line = [" + line + "]")
                if (string.find(line, " *** ") >= 0):
                    self.debugPrint("    'set_switch' failed!")
                    Idx = string.find(line, " *** ");
                    self.log("'set_switch' command failed: " + line[Idx+5:])
                    Command_Succeeded = False
                    Dump_Output_Upon_Error = True
                    break # for loop
                if (string.find(line, " +++ ") >= 0):
                    Idx = string.find(line, " +++ ");
                    self.debugPrint("'show_switches' command succeeded: " + line[Idx+5:])
                    Command_Succeeded = True
                    break # for loop
        finally:
            Sptr.close()
        
        if (Dump_Output_Upon_Error):
            if (not self.__debugOn):
                self.log(resultsStream)
        
        return Command_Succeeded

    def dumpPopenArgs(self, commandName, popenArgsList):
        """Dump the contents of the given Popen arguments list, for the given APEX command,
            to the display.
        """
        self.debugPrint("    dump of APEX command <" + commandName + "> ...")
        self.log("-----------------------------------------------------------")
        Arg_String = ""
        for popenArg in popenArgsList:
            for arg in string.split(popenArg, ","):
                self.log(Arg_String + arg)
                Arg_String = Arg_String + "  "
        self.log("-----------------------------------------------------------")

    def dumpResultsList(self, commandName, resultsList):
        """Dump the contents of the given results list, for the given APEX command,
            to the display.  The results list is a list of tuples containing the following:
                the name of the file the command was issued on
                a boolean result of the outcome, True for success, False for failure
        """
        self.debugPrint("    dump of results for APEX command <" + commandName + "> ...")
        for (fname, results) in resultsList:
            Results_Str = "' Failed   "
            if (results):
                Results_Str = "' Succeeded"
            self.debugPrint("        '" + commandName + Results_Str + " on file: " + fname)

    def buildBogusOutputStream(self):
        return "Output Stream will not be parsed on EffortOnly commands!"
    
    def issueApexCommand(self, popenArgsList):
        """Issue the APEX command associated with the given Popen arguments list.
            This method will return the results of the command.  
            It will up to another method to parse the results for what they expect to see.
        """
        if (self.__effortOnly and (popenArgsList[1] != apex.Show_Status_Command)):
            return self.buildBogusOutputStream()
        
        try:   
            p1 = Popen(popenArgsList, env = os.environ, stdout = PIPE, stderr = PIPE)
            Output_Stream = p1.communicate()[0]
        except OSError, e:
            print "Execution failed:", e
            raise
        # return the output stream results
        return Output_Stream

    def buildCreateWorkingCommand(self, viewName):
        """Build a list that contains the APEX 'create_working' command and the options and arguments
            needed to create a working view for the given viewName.
            Format for APEX create_working command:
                apex create_working -group inherit -access_category group_public
                        -model "" <viewName>
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command] + [apex.Create_Working_Command]
        Popen_Args = Popen_Args + ["-group"] + ["inherit"]
        Popen_Args = Popen_Args + ["-access_category"] + ["group_public"]
        Popen_Args = Popen_Args + ["-model"] + ["\"\""]
        Popen_Args = Popen_Args + [viewName]
        return Popen_Args

    def buildCreateReleaseCommand(self, viewName):
        """Build a list that contains the APEX 'create_release' command and the options and arguments
            needed to create a release view for the given viewName.
            Format for APEX create_release command:
                apex create_release -group inherit -access_category group_public
                        -model "" <viewName>
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command] + [apex.Create_Release_Command]
        Popen_Args = Popen_Args + ["-group"] + ["inherit"]
        Popen_Args = Popen_Args + ["-access_category"] + ["group_public"]
        Popen_Args = Popen_Args + ["-model"] + ["\"\""]
        Popen_Args = Popen_Args + [viewName]
        return Popen_Args

    def buildShowStatusCommand(self, filenameList):
        """Build a list that contains the APEX 'show_status' command and the options and arguments
            needed to show the status of the given files.
            Format for APEX show_status command:
                apex show_status -all <list of files>
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command] + [apex.Show_Status_Command] + ["-all"]
        for fname in filenameList:
            Popen_Args = Popen_Args + [fname]
        return Popen_Args

    def buildShowStatusVerboseCommand(self, filenameList):
        """Build a list that contains the APEX 'show_status' command and the options and arguments
            needed to show the status of the given files.
            Format for APEX show_status command:
                apex show_status -all -verbose <list of files>
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command] + [apex.Show_Status_Command] + ["-all"] + ["-verbose"]
        for fname in filenameList:
            Popen_Args = Popen_Args + [fname]
        return Popen_Args

    def buildMoveCommand(self, filenameList, targetDirectory):
        """Build a list the contains the APEX 'move' command and the options and arguments
            needed to move a list of files to a given directory.
            Format for APEX move command:
                apex move -set all <list of files> <target directory>
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command] + [apex.Move_Object_Command] + ["-set"] + ["all"]
        for fname in filenameList:
            Popen_Args = Popen_Args + [fname]
        Popen_Args = Popen_Args + [targetDirectory]
        return Popen_Args

    def buildUpdateToLatestCommand(self, filenameList):
        """Build a list the contains the APEX 'accept_changes' command and the options and arguments
            needed to update the given list of files to their latest versions.
            Format for APEX update latest command:
                apex accept_changes +no_artifacts -expand_configurations -latest +control <filenameList>
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command] + [apex.Update_Command] + ["+no_artifacts"]
        Popen_Args = Popen_Args + ["-expand_configurations"] + ["-latest"] + ["+control"]
        for fname in filenameList:
            Popen_Args = Popen_Args + [fname]
        return Popen_Args

    def buildDuplicateVersionCommand(self, filenameList, destination, copyAsIs):
        """Build a list the contains the APEX 'accept_changes' command and the options and arguments
            needed to update the given list of files to their latest versions.
            Format for APEX update latest command:
                apex accept_changes +no_artifacts -expand_configurations -source <filenameList>
                    -new_history acceptable_history +control <destination>
            NOTE: the <filenameList> has the following format:
                if there is only 1 filename in the list then it is just the filename otherwise
                the format is:
                    {<fn1>,<fn2>,...,<fnN>}
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command] + [apex.Update_Command] + ["+no_artifacts"]
        Popen_Args = Popen_Args + ["-expand_configurations"] + ["-source"]
	    
        if (len(filenameList) == 1):
            Source_Stream = filenameList[0]
        else:
            Source_Stream = "{"
            for fname in filenameList:
                Source_Stream = Source_Stream + fname
                if (fname != filenameList[-1]):
                    Source_Stream = Source_Stream + ","
            Source_Stream = Source_Stream + "}"
		
        Popen_Args = Popen_Args + [Source_Stream] + ["-new_history"]
        if (copyAsIs):
            Popen_Args = Popen_Args + ["all"]
        else:
            Popen_Args = Popen_Args + ["acceptable_history"]
        Popen_Args = Popen_Args + ["+control"] + [destination]
        return Popen_Args

    def buildIdenticalVersionCommand(self, filenameList, destination):
        """Build a list the contains the APEX 'accept_changes' command and the options and arguments
            needed to make an identical copy of the given list of files to the given destination.
            Format for APEX identical copy command:
                apex accept_changes +no_artifacts -expand_configurations -identical
                    -source <filenameList> -save -control <destination>
            NOTE: the <filenameList> has the following format:
                if there is only 1 filename in the list then it is just the filename otherwise
                the format is:
                    {<fn1>,<fn2>,...,<fnN>}
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command] + [apex.Update_Command] + ["+no_artifacts"]
        Popen_Args = Popen_Args + ["-expand_configurations"] + ["-identical"] + ["-source"]
        
        if (len(filenameList) == 1):
            Source_Stream = filenameList[0]
        else:
            Source_Stream = "{"
            for fname in filenameList:
                Source_Stream = Source_Stream + fname
                if (fname != filenameList[-1]):
                    Source_Stream = Source_Stream + ","
            Source_Stream = Source_Stream + "}"
        Popen_Args = Popen_Args + [Source_Stream] + ["-save"]
        Popen_Args = Popen_Args + ["-control"] + [destination]
        return Popen_Args

    def buildCompareViewsCommand(self, baselineView, currentView):
        """Build a list the contains the APEX 'compare' command and the options and arguments
            needed to compare the baselineView against the currentView.
            Format for APEX compare command:
                apex compare -controlled <baselineView> <currentView>
        """
        Popen_Args = []
        Popen_Args = Popen_Args + [apex.Command] + [apex.Compare_Views_Command] + ["-controlled"]
        Popen_Args = Popen_Args + [baselineView] + [currentView]
        return Popen_Args

    def analyzeShowStatusResults(self, filenameList, resultsStream):
        """Analyze the results found within the resultsStream from the APEX 'show_status' command
            associated with the list of files given.
        """
        self.debugPrint(resultsStream)
        File_Name_Hdr_Found = False
        Results_List        = []
        FnIdx = 0
        Sptr  = StringIO(resultsStream)
        try:
            for line in Sptr:
                self.debugPrint("line = [" + line + "]")
                if File_Name_Hdr_Found:
                    if (FnIdx >= len(filenameList)):
                        continue # for line in Sptr loop
                    if (string.find(line, os.path.basename(filenameList[FnIdx])) >= 0):
                        self.debugPrint("    Filename found: " + filenameList[FnIdx])
                        if (string.find(line, "Uncontrolled") >= 0):
                            # file is NOT controlled
                            self.debugPrint("        File is UNCONTROLLED!")
                            Results_List = Results_List + [(filenameList[FnIdx], False)]
                        else:
                            # file IS controlled
                            self.debugPrint("        File is CONTROLLED!")
                            Results_List = Results_List + [(filenameList[FnIdx], True)]
                        FnIdx = FnIdx + 1
                        self.debugPrint("    FnIdx = " + str(FnIdx))
                else:
                    if (string.find(line, "File Name") >= 0):
                        self.debugPrint("    File Name header found!")
                        File_Name_Hdr_Found = True
        finally:
            Sptr.close()
	    
        if (FnIdx < len(filenameList)):
            self.log("***** WARNING: Reached end of results before processing all filenames in list!")
            self.log("*****          Filling in list with failures for this command!")
            while (FnIdx < len(filenameList)):
                Results_List = Results_List + [(filenameList[FnIdx], False)]
                FnIdx = FnIdx + 1
        
        self.dumpResultsList(apex.Show_Status_Command, Results_List)
        return Results_List

    def analyzeShowStatusResultsForReadiness(self, filenameList, resultsStream):
        """Analyze the results found within the resultsStream from the APEX 'show_status' command
            associated with the list of files given.
        """
        self.debugPrint(resultsStream)
        File_Name_Hdr_Found = False
        Results_List        = []
        FnIdx = 0
        Sptr  = StringIO(resultsStream)
        try:
            for line in Sptr:
                self.debugPrint("line = [" + line + "]")
                if File_Name_Hdr_Found:
                    if (FnIdx >= len(filenameList)):
                        continue # for line in Sptr loop
                    if (string.find(line, os.path.basename(filenameList[FnIdx])) >= 0):
                        self.debugPrint("    Filename found: " + filenameList[FnIdx])
                        if (string.find(line, "Uncontrolled") >= 0):
                            # file is NOT controlled
                            self.debugPrint("        File is UNCONTROLLED!")
                            Results_List = Results_List + [(filenameList[FnIdx], True)]
                        else:
                            # file IS controlled
                            self.debugPrint("        File is CONTROLLED!")
                            # need to check that the file is check-in and is the latest version.
                            # Look for the following patterns to determine if a file is ready to be moved:
                            #
                            #       ' In/' shows up in ' In/In' pattern that shows it is not at the latest version
                            #       ' In/' shows up in ' In/Out' pattern that shows it has been check out somewhere else
                            #       ' Private/' shows up in 'Private/In' pattern that shows it has been checked-out privately
                            #       ' Private/' shows up in 'Private/Out' pattern that shows it has been checked-out privately
                            #       ' Del' shows up in ' Del' pattern that shows that the file is not at the latest version
                            if ((string.find(line, " In/") >= 0) or
                                (string.find(line, "Out") >= 0) or
                                (string.find(line, "Private") >= 0) or
                                (string.find(line, "Del") >= 0)):
                                self.debugPrint("            but file is NOT ready to be moved!")
                                Results_List = Results_List + [(filenameList[FnIdx], False)]
                                # show the line that failed!
                                self.log(line)
                            else:
                                self.debugPrint("            and file IS ready to be moved!")
                                Results_List = Results_List + [(filenameList[FnIdx], True)]
                        FnIdx = FnIdx + 1
                        self.debugPrint("    FnIdx = " + str(FnIdx))
                else:
                    if (string.find(line, "File Name") >= 0):
                        self.debugPrint("    File Name header found!")
                        File_Name_Hdr_Found = True
        finally:
            Sptr.close()
        
        if (FnIdx < len(filenameList)):
            self.log("***** WARNING: Reached end of results before processing all filenames in list!")
            self.log("*****          Filling in list with failures for this command!")
            while (FnIdx < len(filenameList)):
                Results_List = Results_List + [(filenameList[FnIdx], False)]
                FnIdx = FnIdx + 1
        
        self.dumpResultsList(apex.Show_Status_Command, Results_List)
        return Results_List

    def analyzeResults(self, commandName, filenameList, resultsStream):
        """Analyze the results found within the resultsStream from an APEX command
            associated with the list of files given.
            The resultsStream will contain data associated with one of the filenames in the list
            and a status stream, defined as follows:
                '---' request associated with a file
                '***' failure processing request for the file
                '++*' finished processing file but had a failure
                '++-' finished processing file and no affects were made
                '+++' finished processing file successfully
                ':::' finished processing of the command
        """
        Dump_Output_Upon_Error = False
        self.debugPrint(resultsStream)
        Results_List = []
        FnIdx = 0
        Sptr  = StringIO(resultsStream)
        try:
            for line in Sptr:
#               self.debugPrint("line = [" + line + "]")
                if (FnIdx >= len(filenameList)):
                    continue # for line in Sptr loop
                if (string.find(line, os.path.basename(filenameList[FnIdx])) >= 0):
                    self.debugPrint("    File found: [" + filenameList[FnIdx] + "]")
                    if (string.find(line, " ++") >= 0):
#                       self.debugPrint("        operation completed!")
                        # processing of file completed
                        if (string.find(line, " ++* ") >= 0):
                            # operation failed on this file
                            self.debugPrint("            operation FAILED!")
                            Results_List = Results_List + [(filenameList[FnIdx], False)]
                            Dump_Output_Upon_Error = True
                        else:
                            # operation completed on this file (either successfully or no change)
                            self.debugPrint("            operation SUCCEEDED!")
                            Results_List = Results_List + [(filenameList[FnIdx], True)]
                        FnIdx = FnIdx + 1
#                       self.debugPrint("    FnIdx = " + str(FnIdx))
        finally:
            Sptr.close()
		
        if (FnIdx < len(filenameList)):
            if (not self.__effortOnly):
                self.log("***** WARNING: Reached end of results before processing all filenames in list!")
                self.log("*****          Filling in list with failures for this command!")
        while (FnIdx < len(filenameList)):
            Valid_Response = False
            if (self.__effortOnly):
                Valid_Response = True
            Results_List = Results_List + [(filenameList[FnIdx], Valid_Response)]
            FnIdx = FnIdx + 1
		
        if (Dump_Output_Upon_Error):
            if (not self.__debugOn):
                self.log(resultsStream)
        
        self.dumpResultsList(commandName, Results_List)
        return Results_List

    def extractFilename(self, line):
        """Extract the name of the file from an APEX command result output stream.
            The name of the file should be surrounded by double quotes.
        """
        Filename = "uNkNoWn"
        Beg_Quote_Idx = line.find("\"")
        if (Beg_Quote_Idx >= 0):
            End_Quote_Idx = line.find("\"", Beg_Quote_Idx + 1)
            if (End_Quote_Idx >= 0):
                Filename = line[Beg_Quote_Idx+1:End_Quote_Idx]
        return Filename
        
    def analyzeCopyResults(self, commandName, resultsStream):
        """Analyze the results found within the resultsStream from an APEX copy command.
            The resultsStream will contain data associated with files from a given source directory
            and a status stream, defined as follows:
                '---' request associated with a file
                '***' failure processing request for the file
                '++*' finished processing file but had a failure
                '++-' finished processing file and no affects were made
                '+++' finished processing file successfully
                ':::' finished processing of the command
        """
        Dump_Output_Upon_Error = False
        self.debugPrint(resultsStream)
        Results_List = []
        if (self.__effortOnly):
            Results_List = Results_List + [("BogusFile", True)]
            self.dumpResultsList(commandName, Results_List)
            return Results_List
        Sptr  = StringIO(resultsStream)
        try:
            for line in Sptr:
#               self.debugPrint("line = [" + line + "]")
                if (string.find(line, " ++") >= 0):
#                   self.debugPrint("        operation completed!")
                    Filename = self.extractFilename(line)
                    self.debugPrint("    File found: [" + Filename + "]")
                    if (string.find(line, " ++* ") >= 0):
                        # operation failed on this file
                        self.debugPrint("            operation FAILED!")
                        Results_List = Results_List + [(Filename, False)]
                        Dump_Output_Upon_Error = True
                    else:
                        # operation completed on this file (either successfully or no change)
                        if ((string.find(line, "was successful") >= 0) or
                            (string.find(line, "not necessary") >= 0)):
                            # processing of file completed
                            self.debugPrint("            operation SUCCEEDED!")
                            Results_List = Results_List + [(Filename, True)]
        finally:
            Sptr.close()
            
        if (Dump_Output_Upon_Error):
            if (not self.__debugOn):
                self.log(resultsStream)
        
        self.dumpResultsList(commandName, Results_List)
        return Results_List

    def analyzeCreateResults(self, commandName, resultsStream):
        """Analyze the results found within the resultsStream from an APEX create_working command.
            The resultsStream will contain data associated with files from a given source directory
            and a status stream, defined as follows:
                '---' request associated with commandName
                '***' failure processing request
                '++*' finished processing but had a failure
                '++-' finished processing and no affects were made
                '+++' finished processing successfully
                ':::' finished processing of the command
        """
        Dump_Output_Upon_Error = False
        self.debugPrint(resultsStream)
        Results_List = []
        if (self.__effortOnly):
            Results_List = Results_List + [("BogusView", True)]
            self.dumpResultsList(commandName, Results_List)
            return Results_List[0]
        Sptr  = StringIO(resultsStream)
        try:
            for line in Sptr:
#               self.debugPrint("line = [" + line + "]")
                if (string.find(line, " ++") >= 0):
#                   self.debugPrint("        operation completed!")
                    # processing of file completed
                    Viewname = self.extractFilename(line)
                    self.debugPrint("    APEX " + commandName + " for view name: " + Viewname)
                    if (string.find(line, " ++* ") >= 0):
                        # operation failed on this file
                        self.debugPrint("            operation FAILED!")
                        Results_List = Results_List + [(Viewname, False)]
                        Dump_Output_Upon_Error = True
                    else:
                        # operation completed on this file (either successfully or no change)
                        self.debugPrint("            operation SUCCEEDED!")
                        Results_List = Results_List + [(Viewname, True)]
        finally:
            Sptr.close()
        
        if (Dump_Output_Upon_Error):
            if (not self.__debugOn):
                self.log(resultsStream)
        
        self.dumpResultsList(commandName, Results_List)
        return Results_List[0]
    
    def extractFieldMinMax(self, line):
        """Extract the min and max of the fields based on the '-' divider.
        """
        FilenameMin        = line.find("-")
        FilenameMax        = line.find(" ", FilenameMin)
        BaselineHistoryMin = line.find("-", FilenameMax)
        BaselineHistoryMax = line.find(" ", BaselineHistoryMin)
        BaselineVersionMin = line.find("-", BaselineHistoryMax)
        BaselineVersionMax = line.find(" ", BaselineVersionMin)
        BaselineStateMin   = line.find("-", BaselineVersionMax)
        BaselineStateMax   = line.find(" ", BaselineStateMin)
        CurrentHistoryMin  = line.find("-", BaselineStateMax)
        CurrentHistoryMax  = line.find(" ", CurrentHistoryMin)
        CurrentVersionMin  = line.find("-", CurrentHistoryMax)
        CurrentVersionMax  = line.find(" ", CurrentVersionMin)
        CurrentStateMin    = line.find("-", CurrentVersionMax)
        CurrentStateMax    = len(line)
        MinMaxFieldList = []
        MinMaxFieldList = MinMaxFieldList + [("Filename", FilenameMin, FilenameMax)]
        MinMaxFieldList = MinMaxFieldList + [("BaselineHistory", BaselineHistoryMin, BaselineHistoryMax)]
        MinMaxFieldList = MinMaxFieldList + [("BaselineVersion", BaselineVersionMin, BaselineVersionMax)]
        MinMaxFieldList = MinMaxFieldList + [("BaselineState", BaselineStateMin, BaselineStateMax)]
        MinMaxFieldList = MinMaxFieldList + [("CurrentHistory", CurrentHistoryMin, CurrentHistoryMax)]
        MinMaxFieldList = MinMaxFieldList + [("CurrentVersion", CurrentVersionMin, CurrentVersionMax)]
        MinMaxFieldList = MinMaxFieldList + [("CurrentState", CurrentStateMin, CurrentStateMax)]
        return MinMaxFieldList

    def dumpFieldInfoList(self, fieldInfoList):
        """Display the contents of the given 'fieldInfoList'.
            This list should contain the following tuple:
                (fieldName, fieldData)
        """
        for (fieldName, fieldData) in fieldInfoList:
            self.debugPrint(fieldName + " = [" + fieldData + "]")
         
    def getFieldFromFieldInfoList(self, fieldname, fieldInfoList):
        """Get the given field from the fieldInfoList.
        """
        Field_Data = "UnKnOwN"
        for (fieldName, fieldData) in fieldInfoList:
            if (fieldName == fieldname):
                Field_Data = fieldData
        return Field_Data
           
    def fileNeedsMoreWork(self, fieldInfoList, annotation):
        """Determine if the file contained in the fieldInfoList needs more work done!
        """
        if (annotation == "-"):
            if ((self.getFieldFromFieldInfoList("BaselineState", fieldInfoList) == "Del") or
                (self.getFieldFromFieldInfoList("CurrentState", fieldInfoList) == "Del")):
                return (False, "needs NO work, don't care (anno-)")
            elif ((self.getFieldFromFieldInfoList("BaselineHistory", fieldInfoList) == "Common") and
                (self.getFieldFromFieldInfoList("CurrentHistory", fieldInfoList) == "Common")):
                return (True, "needs to be updated1 (anno-)")
            elif (self.getFieldFromFieldInfoList("BaselineHistory", fieldInfoList) == 
                  self.getFieldFromFieldInfoList("CurrentHistory", fieldInfoList)):
                return (True, "needs to be updated2 (anno-)")
            else:
                return (True, "needs more work (anno-)")
        elif (annotation == "*"):
            if ((self.getFieldFromFieldInfoList("BaselineState", fieldInfoList) == "Del") or
                (self.getFieldFromFieldInfoList("CurrentState", fieldInfoList) == "Del")):
                if (self.getFieldFromFieldInfoList("BaselineState", fieldInfoList) == "Del"):
                    return (False, "needs NO work, don't care (anno*)")
                else:
                    return (True, "needs more work1 (anno*)")
            else:
                return (True, "needs more work2 (anno*)")
        else:
            return (True, "needs more work (annoo)")
                
    def extractFileInfoFromCompare(self, line, relativePathList, minMaxFieldList):
        """Extract the name of the file (and other info) from an APEX compare command result output stream.
            The minMaxFieldList should contain the min/max indexes from the line for the field info.
        """
        Field_Info_List = []
        for (fieldName, fieldMin, fieldMax) in minMaxFieldList:
            if (fieldName == "Filename"):
                Field_Data = line[fieldMin:fieldMax]
                Field_Data = str.rstrip(Field_Data)
                Directory_Depth = Field_Data.count("  ")
#               print "Directory_Depth = ", Directory_Depth
                Field_Data = str.strip(line[fieldMin:fieldMax])
#                print "Field_Data after strip = ", Field_Data
                if (len(relativePathList) > 0):
                    if (Directory_Depth > 0):
                        Rel_Path_Name = relativePathList[0]
                        Depth = 0
                        for relDir in relativePathList:
#                            print "relDir = ", relDir
                            Depth = Depth + 1
                            if (Depth > Directory_Depth):
                                break
                            if (Depth == 1):
                                continue
                            Rel_Path_Name = Rel_Path_Name + relDir
#                            print "Rel_Path_Name = ", Rel_Path_Name
                        Field_Data = Rel_Path_Name + str(Field_Data)
#                        print "Field_Data = ", Field_Data
            else:
                Field_Data = str.strip(line[fieldMin:fieldMax])
            Field_Info_List = Field_Info_List + [(fieldName, Field_Data)]
#            print "Field_Info_List = ", Field_Info_List
        return Field_Info_List

    def extractFilenameFromCompare(self, line, relativePathList, annotation):
        """Extract the name of the file from an APEX compare command result output stream.
            The name of the file should be surrounded by spaces just after the annotation.
        """
        Filename = "uNkNoWn"
        Stripped_Line = string.lstrip(line[2:])
        White_Space_Idx = Stripped_Line.find(" ")
        if (White_Space_Idx > 0):
            Filename = Stripped_Line[:White_Space_Idx]
        if (line[2:3] == " "):
            Truncated_Len = len(line) - len(Stripped_Line)
            Directory_Depth = str.count(line[2:Truncated_Len], "  ")
        else:
            Directory_Depth = 0
        if (len(relativePathList) > 0):
            if (Directory_Depth > 0):
                Rel_Path_Name = relativePathList[0]
                Depth = 0
                for relDir in relativePathList:
                    Depth = Depth + 1
                    if (Depth >= Directory_Depth):
                        break
                    if (Depth == 1):
                        continue
                    Rel_Path_Name = Rel_Path_Name + relDir
                Filename = Rel_Path_Name + Filename
        return Filename
        
    def analyzeCompareResults(self, commandName, resultsStream):
        """Analyze the results found within the resultsStream from an APEX compare command.
            The resultsStream will contain data associated with the baseline view and the current view.
            This data contains the file name, the baseline history, version and state
            and the current history, version and state.
            The first column of an element entry will contain an annotation summarizing the
            differences between the baseline view and the current view.  The character in the
            first column can be one of the following:
                ' ' history and version are the same for baseline and current views (ok)
                '+' history is the same but current view has a later version (ok)
                '-' history is the same but current view has an older version (may need work)
                '*' baseline view and current view have different histories (may need work)
                'o' the file is checked out in one of the views (needs work)
        """
        self.debugPrint(resultsStream)
        Results_List = []
        File_Name_Hdr_Found = False
        if (self.__effortOnly):
            self.dumpResultsList(commandName, Results_List)
            return Results_List
        Sptr  = StringIO(resultsStream)
        try:
            Relative_Path = []
            for line in Sptr:
                self.debugPrint("line = [" + line + "]")
                if (File_Name_Hdr_Found):
                    if (line.count("-") > 10):
                        MinMaxFieldList = self.extractFieldMinMax(line)
                    if (line[-2:-1] == "/"): # end-of-line = "/"
                        Idx = line.count("  ") # each double-space denotes a directory depth
                        if (Idx == 1):
                            # reset list
                            Relative_Path = [str.lstrip(line[:-1])]
                        elif (Idx <= len(Relative_Path)):
                            # replace entry
                            Relative_Path[Idx-1] = str.lstrip(line[:-1])
                        else:
                            # add new entry
                            Relative_Path = Relative_Path + [str.lstrip(line[:-1])]
#                        print "Relative_Path = ", Relative_Path
                    if ((line[:1] == "-") or (line[:1] == "*") or (line[:1] == "o")):
                        Field_Info_List = self.extractFileInfoFromCompare(line, Relative_Path, 
                                                                          MinMaxFieldList)
                        self.dumpFieldInfoList(Field_Info_List)
                        (File_Needs_More_Work, Reason) = self.fileNeedsMoreWork(Field_Info_List, line[:1])
                        Filename = self.getFieldFromFieldInfoList("Filename", Field_Info_List)
                        self.debugPrint("This file: <" + Filename + "> reason: " + Reason)
                        if (File_Needs_More_Work):
                            Results_List = Results_List + [((Filename, Reason), False)]
                else:
                    if (string.find(line, "File Name") >= 0):
                        self.debugPrint("    File Name header found!")
                        File_Name_Hdr_Found = True
        finally:
            Sptr.close()
        
        return Results_List
