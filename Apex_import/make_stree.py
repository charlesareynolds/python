#!/usr/bin/env python
"""Utility to make a shadow code tree, for a given APEX Tower,
without tower names from NIF Apex towers.

Given a tower name, or a tower name and a layer or
a tower name and a layer name and a subsystem name, 
makes a shadow code tree in the form:

/nif/code/shadow/[tower]/[layer]/[subsystem]/[subdirs]/[hard links to Ada files]

All layers below the given tower will be created.
All subsystems below the given layer will be created.
Deletes /nif/code/shadow/[tower]/[layer]/[subsystem] first if it exists.
There is no tower name after the subsystem name.
The subsystem name is without the ".ss".
Each link points to the corresponding Ada file.  
Two links are created for each original *.[12].ada file (if requested)- 
one with Apex naming, and one with Gnat naming.

This is to support tool that doesn't work well with Apex's strategy of changeable
tower names to indicate branches and releases.

"""

__author__    = "Randy Sanchez"
__version__   = "$Revision: 1.9 $"
__date__      = "$Date: 08/15/2008 08:30:09 $"
__copyright__ = "Copyright 2008 LLNL"

import sys
#
# NOTE: before installing this utility, make sure that the 
#   Library_Path is set to the location where the 'make_stree'
#   Python modules are being store.
#   This should be in the following directory:
#
#   /nif/tools/lib/make_stree
#
Library_Path = '/nif/tools/lib/make_stree'
#
#Library_Path = '/nif/tools/bin/scripts.ss/sanchez23.wrk'
#print sys.path
sys.path.append(Library_Path);
#print sys.path

from MakeStreeForSubSys import *
from MakeStreeForLayer import *
from MakeStreeForTower import *
from make_stree_utilities import *
from optparse import OptionParser

if __name__ == "__main__":
    
    # parse command line options
    parser = OptionParser(usage="Usage: %prog [options] <tower name> [<layer name> [<subsys name>]]", 
                          version="%prog 1.0")
    addParserOptions(parser)
    (options, args) = parser.parse_args()
    if len(args) == 0 or len(args) > 3:
        print
        parser.print_help()
        print
        parser.error("expected 1, 2 or 3 arguments, got " + str (len(args)))
        print
    if options.Copy_Files and options.Make_Hard_Links:
        parser.error("options -c and -h are mutually exclusive")
#    if options.Move_Idl_Ada and options.Remove_Idl_Ada_Dirs:
#        parser.error("options --move_idl_ada and --remove_idl_ada_dirs are mutually exclusive")
#    if options.Check_Idl_Ada_Dirs and \
#        (options.Move_Idl_Ada or options.Remove_Idl_Ada_Dirs):
#        parser.error("options --check_idl_ada_dirs and " +
#                        "(--move_idl_ada and --remove_idl_ada_dirs) are mutually exclusive")
        
    if len(args) == 1:
        Tower_Name  = args[0]
        Layer_Name  = "TBD"
        Subsys_Name = "TBD.ss"
        # create an instance of the MakeStreeForTower class
        #   initializing it with the Tower name
        #
        makeStree = MakeStreeForTower(Tower_Name, Layer_Name, Subsys_Name, Tower_Name)
    elif len(args) == 2:
        Tower_Name  = args[0]
        Layer_Name  = args[1]
        Subsys_Name = "TBD.ss"
        # create an instance of the MakeStreeForLayer class
        #   initializing it with the Layer name
        #
        makeStree = MakeStreeForLayer(Tower_Name, Layer_Name, Subsys_Name, Layer_Name)
    else:
        Tower_Name  = args[0]
        Layer_Name  = args[1]
        Subsys_Name = args[2]
        # create an instance of the MakeStreeForSubsys class
        #   initializing it with the Subsys name
        #
        makeStree = MakeStreeForSubSys(Tower_Name, Layer_Name, Subsys_Name, Subsys_Name)
    
    #
    # setup the flags within the makeStree instance based on the
    #   command line options that the user chose.
    #
    setupFlags(options, makeStree)

    makeStree.log("")
    if len(args) >= 1:
        makeStree.log("     Tower Name = " + Tower_Name)
    if len(args) >= 2:
        makeStree.log("     Layer Name = " + Layer_Name)
    if len(args) == 3:
        makeStree.log("Sub-System Name = " + Subsys_Name)
    makeStree.log("")
    #
    # make the Source and Target path names for our given instance
    #
    makeStree.makeSourcePathNames()
    makeStree.makeTargetPathNames()
    #
    # based on the number of arguments, initialize the Source and Target
    # paths for each possible type of request.
    #
    if len(args) == 1:
        Source_Path     = makeStree.sourceRootPath
        Target_Ada_Path = makeStree.targetAdaTowerPath
        Target_Idl_Path = makeStree.targetIdlTowerPath
    elif len(args) == 2:
        Source_Path     = makeStree.sourceLayerPath
        Target_Ada_Path = makeStree.targetAdaLayerPath
        Target_Idl_Path = makeStree.targetIdlLayerPath
    else:
        Source_Path     = makeStree.sourceViewPath
        Target_Ada_Path = makeStree.targetAdaSubsysPath
        Target_Idl_Path = makeStree.targetIdlSubsysPath
    #
    # if the user wants to move controlled files out of the IDL_Ada
    #       directory, then the tower name provided MUST be a working
    #       tower and not a release tower.
    if (makeStree.moveIdlAda and Tower_Name[-4:] != ".wrk"):
        parser.error("You must provide a 'working' tower when using the option --move_idl_ada!")
    #
    # as per Charles Reynolds request on 05/05/08
    #       the 'removeIdlAdaDir' option will not be available.
    #
    if (makeStree.removeIdlAdaDir):
        parser.error("As of 05/05/08 the '--remove_idl_ada_dirs' option is NOT available!")
    #
    # prepare the target Ada/Idl directory paths before processing the directories
    #
    if not (makeStree.moveIdlAda or makeStree.removeIdlAdaDir or makeStree.checkIdlAdaDir):
        makeStree.prepareTargetDirectory(Target_Ada_Path)
        if len(args) == 1:
            makeStree.prepareTargetDirectory(Target_Idl_Path)
    
    #
    # process the given Tower making the appropriate
    #   files based on the command line options that the user chose.
    #
    makeStree.processDir(Source_Path, 
                         Target_Ada_Path, 
                         Target_Idl_Path)
    
    # have my instance log its Process Counts
    makeStree.logProcessCounts()
