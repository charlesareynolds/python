#!/usr/bin/env python
"""Module to hold utility routines used by the
make_shadow_tree and make_shadow_tree_accurev
utilities.
"""

__author__    = "Randy Sanchez"
__version__   = "$Revision: 1.8 $"
__date__      = "$Date: 08/15/2008 08:30:11 $"
__copyright__ = "Copyright 2008 LLNL"

import apex
import gnat
import os

def addParserOptions(parser):
    """Add options to the given parser for the make shadow tree utilities.
    """
    parser.add_option("-a", "--apex",
                      action="store_false", 
                      dest="Make_Gnat_Format_Targets", 
                      default=True,
                      help="Make only Apex formatted Ada file names " +
                            "(may not be used with -g) [default: FALSE].")
    parser.add_option("-b", "--both",
                      action="store_true", 
                      dest="Make_Both_Format_Targets", 
                      default=False,
                      help="Make both Apex and Gnat formatted Ada file names " +
                            "(overrides -a and -g) [default: %default].")
    parser.add_option("-c", "--copy",
                      action="store_true", 
                      dest="Copy_Files", 
                      default=False,
                      help="Make copies, not symbolic links " +
                            "(may not be used with --hard_links) [default: %default].")
    parser.add_option("-d", "--debug",
                      action="store_true", 
                      dest="Debug", 
                      default=False,
                      help="Turn on debugging [default: %default].")
    parser.add_option("-e", "--effort_only",
                      action="store_true", 
                      dest="Effort_Only", 
                      default=False,
                      help="Log what would be done without actually doing it [default: %default].")
    parser.add_option("-g", "--gnat",
                      action="store_true", 
                      dest="Make_Gnat_Format_Targets", 
                      default=True,
                      help="Make only Gnat formatted Ada file names " +
                            "(may not be used with -a) [default: %default].")
    parser.add_option("--hard_links",           # NOTE: no quick way to make hardlinks
                      action="store_true", 
                      dest="Make_Hard_Links", 
                      default=False,
                      help="Make hard links, not symbolic links " +
                            "(may not be used with -c) [default: %default].")
    parser.add_option("-i", "--idl_only",
                      action="store_true", 
                      dest="IDL_Only", 
                      default=False,
                      help="Only process IDL files [default: %default].")
#    parser.add_option("--move_idl_ada",         # NOTE: no quick way to move IDL_Ada files
#                      action="store_true", 
#                      dest="Move_Idl_Ada", 
#                      default=False,
#                      help="Move controlled files in IDL_Ada directories " +
#                            "to the parent directory.  " + 
#                            "This option overrides all file options (-a, -b, -g, -i) " +
#                            "and all work options (-c, --hard_links, -remove_idl_ada_dirs) " +
#                            "[default: %default].")
#    parser.add_option("--remove_idl_ada_dirs",  # NOTE: no quick way to remove IDL_Ada directories
#                      action="store_true",
#                      dest="Remove_Idl_Ada_Dirs", 
#                      default=False,
#                      help="Remove IDL_Ada directories.  " +
#                            "This option overrides all file options (-a, -b, -g, -i) " +
#                            "and all work options (-c, --hard_links, -move_idl_ada) " +
#                            "[default: %default].")
#    parser.add_option("--check_idl_ada_dirs",  # NOTE: no quick way to check IDL_Ada directories
#                      action="store_true", 
#                      dest="Check_Idl_Ada_Dirs", 
#                      default=False,
#                      help="Check IDL_Ada directories for possible problems before issuing " +
#                            "the --move_idl_ada or --remove_idl_ada_dirs options.  " +
#                            "This option overrides all file options (-a, -b, -g, -i) " +
#                            "and all work options (-c, --hard_links, -move_idl_ada) " +
#                            "[default: %default].")
    parser.add_option("-w", "--workspace", 
                      action="store", 
                      type="string", 
                      dest="Workspace", 
                      default="",
                      metavar="<path>", 
                      help="Use <path>/src/ada for the Ada and <path>/src/idl for the IDL.")

def setupFlags(parsedOptions, streeInstance):
        """Setup flags within the given Object Instance
            based on the given parsed command line options.
        """
        # Setup defaults for instance flag variables
        createApex, createGnat, createIdl = False, True, True
        makeSoftLink, makeHardLink, makeCopy = True, False, False
        moveIdlAda, removeIdlAdaDir, checkIdlAdaDir = False, False, False
        effortOnly = False # as of 03/25/08 TRUE is for testing only
        debugOn, underApexSession = False, False
        workspace = ""

        # check out what options the user provided
        if not parsedOptions.Make_Gnat_Format_Targets:
            createApex, createGnat = True, False
        if parsedOptions.Make_Gnat_Format_Targets:
            createApex, createGnat = False, True
        if parsedOptions.Make_Both_Format_Targets:
            createApex, createGnat = True, True
        if parsedOptions.IDL_Only:
            createApex, createGnat, createIdl = False, False, True
        if parsedOptions.Copy_Files:
            makeSoftLink, makeHardLink, makeCopy = False, False, True
        if parsedOptions.Make_Hard_Links:
            makeSoftLink, makeHardLink, makeCopy = False, True, True
#        if parsedOptions.Move_Idl_Ada or parsedOptions.Remove_Idl_Ada_Dirs or parsedOptions.Check_Idl_Ada_Dirs:
#            createApex, createGnat, createIdl = False, False, False
#            makeSoftLink, makeHardLink, makeCopy = False, False, False
#            if parsedOptions.Move_Idl_Ada:
#                moveIdlAda, removeIdlAdaDir, checkIdlAdaDir = True, False, False
#            elif parsedOptions.Remove_Idl_Ada_Dirs:
#                moveIdlAda, removeIdlAdaDir, checkIdlAdaDir = False, True, False
#            else:
#                moveIdlAda, removeIdlAdaDir, checkIdlAdaDir = False, False, True
#            try:
#                if os.environ["APEX_HOME"] != "":
#                    underApexSession = True
#            except KeyError, e:
#                print
#                print "***** WARNING: Not under an APEX session!"
#                print "*****          Issuing APEX commands WILL take too long to run!"
#                print "*****          Not allowing user to run this utility under these conditions!"
#                print "*****          Stopping utility NOW!"
#                print
#                os._exit(13)
        if parsedOptions.Workspace != "":
            workspace = parsedOptions.Workspace
        if parsedOptions.Debug:
            debugOn = True
        if parsedOptions.Effort_Only:
            effortOnly = True
        # Set the instance variables based on the options provided by the user
        streeInstance.setInstanceVars((createApex, createGnat, createIdl,
                                      makeSoftLink, makeHardLink, makeCopy,
                                      moveIdlAda, removeIdlAdaDir, checkIdlAdaDir,
                                      effortOnly, debugOn, underApexSession,
                                      workspace))
        # print a copy of what was set, only printed if debugging is turned on
        streeInstance.dumpInstanceVars()
        
def isAdaFile(filename):
    """Returns True if the file name has an Ada Suffix,
            either Apex or Gnat
    """
    if (isApexFile(filename) or isGnatFile(filename)):
        return True
    else:
        return False
        
def isApexFile(filename):
    """Returns True if the file name has an Apex Ada Suffix
    """
    if (filename[-6:] == apex.Spec_Suffix or
        filename[-6:] == apex.Body_Suffix):
        return True
    else:
        return False
        
def isGnatFile(filename):
    """Returns True if the file name has a Gnat Ada Suffix
    """
    if (filename[-4:] == gnat.Spec_Suffix or
        filename[-4:] == gnat.Body_Suffix):
        return True
    else:
        return False
        
def isIdlFile(filename):
    """Returns True if the file name has an IDL Suffix
    """
    if (filename[-4:] == ".idl"):
        return True
    else:
        return False
        
def fromApexToGnat(filename):
    """Convert the given filename from an Apex Ada file format to a Gnat Ada file format.
            Returns the file unchanged if the given file is not
            of a valid format.
    """
    Name_Root = filename[:-6]
    # Turn the dots into dashes
    Name_Root = Name_Root.replace(".", "-")
    if filename[-6:] == apex.Spec_Suffix:
        Result = Name_Root + gnat.Spec_Suffix
    elif filename[-6:] == apex.Body_Suffix:
        Result = Name_Root + gnat.Body_Suffix
    else:
        Result = filename
            
    return Result
        
def fromGnatToApex(filename):
    """Convert the given filename from a Gnat Ada file format to an Apex Ada file format.
            Returns the file unchanged if the given file is not
            of a valid format.
    """
    Name_Root = filename[:-4]
    # Turn the dashes into dots
    Name_Root = Name_Root.replace("-", ".")
    if filename[-4:] == gnat.Spec_Suffix:
        Result = Name_Root + apex.Spec_Suffix
    elif filename[-4:] == gnat.Body_Suffix:
        Result = Name_Root + apex.Body_Suffix
    else:
        Result = filename
            
    return Result
    
