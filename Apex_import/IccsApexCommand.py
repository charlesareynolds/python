#!/usr/bin/env python
"""Class definition that implements the APEX commands associated with the
Integrated Computer Control System (ICCS).
This class defines methods that will process APEX commands.
"""

__author__    = "Randy Sanchez"
__version__   = "$Revision: 1.2 $"
__date__      = "$Date: 05/09/2008 13:09:26 $"
__copyright__ = "Copyright 2008 LLNL"

import iccs_apex
import os
import string
from ApexCommand import *

class IccsApexCommand(ApexCommand):
    "APEX commands associated with the ICCS application"
    
    def getReleaseVersion(self, workingTowerName, infixStream):
        """This method takes the working tower name and returns a release version
            of the name.  Both the working tower name and release version are returned
            from this method.
        """
        towerInfix = iccs_apex.whatInfixIsStream(workingTowerName)
        prefixStream, postfixStream = string.split(workingTowerName, towerInfix)
        releaseVersion, postVersion = string.split(postfixStream, "wrk")
        releaseTowerName = infixStream + releaseVersion + "rel"
        
        return releaseTowerName

    def findDuplicateWorkingFiles(self, initialList, curInfix, newInfix):
        """Finds files from the given list from a working tower that are duplicated in 
            other working directories.
            The other directories searched will be based on the <curInfix> name of the
            directory that the existing files reside in.  The <newInfix> name will be used
            as the new directory to search for the duplicate files.
            Returns a list of files from the 'initialList' that reside in the 'newInfix'
                    directory.
                    If no duplicate files exist then an empty list is returned.
        """
        Duplicate_List = []
        for fname in initialList:
            infixStream = iccs_apex.whatInfixIsStream(fname)
            if (infixStream == curInfix):
                prefixStream, postfixStream = string.split(fname, infixStream)
                A_File_Name = prefixStream + newInfix + postfixStream
                if (os.path.exists(A_File_Name)):
                    Duplicate_List = Duplicate_List + [A_File_Name]
                    
        return Duplicate_List
    
    def findDuplicateReleaseFiles(self, initialList, workingTowerName, newInfix):
        """Finds files from the given list from a working tower that are duplicated in 
            any release directories.
            The other directories searched will be based on the release version of the
            directory that the existing files reside in.  The <newInfix> name will be used
            as the new directory to search for the duplicate files.
            Returns a list of files from the 'initialList' that reside in the 'newInfix'
                    directory.
                    If no duplicate files exist then an empty list is returned.
        """
        Release_Tower_Name = self.getReleaseVersion(workingTowerName, newInfix)
        Duplicate_List = []
        for fname in initialList:
            prefixStream, postfixStream = string.split(fname, workingTowerName)
            A_File_Name = prefixStream + Release_Tower_Name + postfixStream
            if (os.path.exists(A_File_Name)):
                Duplicate_List = Duplicate_List + [A_File_Name]
                    
        return Duplicate_List
    
    def newDuplicateFiles(self, duplicateList, curInfixStream, newInfixStream):
        """This method returns a new list of files that have the IDL_Ada directory removed from its path.
            Returns a new list containing path names to files that do not exist yet.
        """
        Return_List = []
        for fname in duplicateList:
            File_Name_Part = os.path.basename(fname)
            Directory_Name_Part = os.path.dirname(fname)
            Parent_Directory_Name = os.path.dirname(Directory_Name_Part)
            File_Name = os.path.join(Parent_Directory_Name, File_Name_Part)
            prefixStream, postfixStream = string.split(File_Name, curInfixStream)
            New_File_Name = prefixStream + newInfixStream + postfixStream
            Return_List = Return_List + [New_File_Name]
        return Return_List
    
    def newDestinationStream(self, destination, curInfixStream, newInfixStream):
        """This method takes apart the destination, based on the current <infix> stream,
            and returns a new destination stream based on the new <infix> stream.
        """
        prefixStream, postfixStream = string.split(destination, curInfixStream)
        return prefixStream + newInfixStream + postfixStream

