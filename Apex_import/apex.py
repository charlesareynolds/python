#!/usr/bin/env python
"""Module to hold APEX'isms
"""

__author__    = "Randy Sanchez"
__version__   = "$Revision: 1.4 $"
__date__      = "$Date: 08/07/2008 07:49:57 $"
__copyright__ = "Copyright 2008 LLNL"

Ada_Suffix = ".ada"
Body_Suffix = ".2.ada"
IDL_Ada_Dir = "IDL_Ada"
Internal_Dirs = (
    ".Rational_Location", 
    ".Rational", 
    "Policy", 
    "Imports", 
    "Exports")
Spec_Suffix = ".1.ada"
Subsystem_Suffix = ".ss"

Full_Command_Path = "/nif/rational/releases/apex.4.2.0b/bin/apexinit"
Command                   = "apex"
Compare_Views_Command     = "compare"
Copy_Command              = "copy"
Create_Working_Command    = "create_working"
Create_Release_Command    = "create_release"
Move_Object_Command       = "move"
Remove_Object_Command     = "discard"
Set_Switch_Command        = "set_switch"
Show_Status_Command       = "show_status"
Show_Switches_Command     = "show_switches"
Update_Command            = "accept_changes"
Update_To_Latest_Command  = "update_to_latest_version"
Duplicate_Version_Command = "duplicate_version"

Executable_Inclusions_Attribute = "VC_EXECUTABLE_INCLUSIONS"

NIF_Root_Path = "/nif/code"  
NIF_Layers = (
        "Application_Behavior",
        "Application_Scripts",
        "Application_Support",
        "Controllers",
        "Devices",
        "Framework_Services",
        "Framework_Templates",
        "Main_Programs",
        "Support",
        "Research")
