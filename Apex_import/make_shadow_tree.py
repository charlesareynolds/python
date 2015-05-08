#!/usr/bin/env python
"""Utility to make a shadow code tree without view names from NIF Apex views.

Given a view name, makes a shadow code tree in the form:

/nif/code/shadow/[view]/[layer]/[subsystem]/[subdirs]/[hard links to Ada files]

Deletes /nif/code/shadow/[view] first if it exists.
There is no view name after the subsystem name.
The subsystem name is witout the ".ss".
Each link points to the corresponding Ada file.  Two hard links are created for
each original *.[12].ada file - one with Apex naming, and one with Gnat naming.

This is to support tools that don't work well with Apex's strategy of changeable
view names to indicate branches and releases.

Hard links to *.gpr files are created, too, so that everything can be CMed in 
Apex, for now.
"""

# 2007/06/22 CAR SCR20738 Took out CORBA shadowing, since the gnat CORBA project 
# 		files now refer to the distribution views directly.
# 2007/07/12 CAR SCR 20738 changing back to hard links for Windows.
# 2007/09/17 CAR turning off Apex view processing to save time and allow parallel runs.
# 2007/10/01 CAR making links symbolic AND relative ("../../target")for Windows and Linux
# 2007/10/25 CAR PolyORB generates gnat file names.  Linking them too.
# 2007/12/19 CAR adding switch processing and support for migration to AccuRev workspaces
# 2007/12/20 CAR No longer copying/linking IDL into the Ada tree.
# 2008/02/05 CAR No longer processing IDL at all.  This is now done in the 
# 		 corresponding AccuRev version of this script.
# 2008/03/26 CAR Taking out GNAT project links
# 2008/03/26 CAR Adding IDL only option.


__author__ = "Charles Reynolds"
__version__ = "$Revision: 1.39 $"
__date__ = "$Date: 05/05/2008 11:23:35 $"
__copyright__ = "Copyright 2006 LLNL"

import array
from optparse import OptionParser
import os
import shutil
import sys

Apex_Ada_Suffix = ".ada"
Apex_Body_Suffix = ".2.ada"
Apex_Current_View = "sun4_solaris2.ada95.4.2.0.rel"
Apex_Internal_Dirs = (
    ".Rational_Location", 
    ".Rational", 
    "Policy", 
    "Imports", 
    "Exports")
Apex_Root_Path = "/nif/rational/base/ada"
Apex_Spec_Suffix = ".1.ada"
Apex_Subsystems = (
#   Leaving out the Rational-specific subsystems:
    "lrm.ss",
    "numerics.ss",
#    "posix.ss",
    "predefined.ss",
#    "rational.ss",
    "real_time_systems.ss",
#    "rts_vads_exec.ss",
    "systems_programming.ss")
#    "testmate.ss")
Gnat_Body_Suffix = ".adb"
Gnat_Spec_Suffix = ".ads"
IDL_Suffix = ".idl"
Log_Prefix = "UNDEFINED"
NIF_Root_Path = "/nif/code"  
NIF_Shadow_Root_Path = NIF_Root_Path + "/shadow" 
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
Old_Dirs_Deleted = ""
Subsystem_Suffix = ".ss"
Target_IDL_Root_Path = ""
Target_IDL_Links_Path = ""

Views_Processed = 0
Files_Processed = 0
Files_Copied_Or_Linked = 0
Target_Count = 0

#################################################################################
# BEGIN Procedures designed to be called by Process_View_Dirs
#################################################################################

def Debug_Print (Message):
    if options.Debug:
        print "$$$ " + Message
                
def Log (Message):
    print Log_Prefix + Message        
        
def Run_Or_Log (Command):
    Log (Command)
    if not options.Effort_Only:
        exec Command

def Print_Source_And_Target_Dirs (Source_Path, Target_Path):
    print Source_Path
    print Target_Path

def Print_Ada_Files_In_Source_Dir (Source_Path, Target_Path):
    """Prints the Ada files in View_Path.  Target_Path is unused.
    """
    Debug_Print ("Print_Ada_Files_In_Source_Dir (" + Source_Path + ", " + Target_Path + ")")
    for Entry in os.listdir (Source_Path):
    	# Hopefully there are no directories ending in .ada:
        if Entry [-4:] == Apex_Ada_Suffix:
            print os.path.join (Source_Path, Entry)                
               
def Make_Target_Dir (Source_Path, Target_Path):
    """Creates directory Target_Path and any non-existent parent directories.
    Source_Path is unused.
    """
    Debug_Print ("Make_Target_Dir (" + Source_Path + ", " + Target_Path + ")")
    if os.path.exists (Target_Path):
        print "+-- Exists: " + Target_Path
    else:
        Run_Or_Log ('os.makedirs ("' + Target_Path + '")')
        
def Prepare_Target_Location (Target_Path):
    """Prepares to link or copy a file.  Deletes the target, 
    and creates any needed target directories.
    """
    Target_Parent_Path = os.path.dirname(Target_Path)
    if os.path.exists (Target_Path):
        Run_Or_Log ('os.remove ("' + Target_Path + '")')
    if not os.path.exists (Target_Parent_Path):
        Run_Or_Log ('os.makedirs ("' + Target_Parent_Path + '")')    
    
def Link_A_File (Source_Path, Target_Path):
    """Creates a link named Target_Path that points at Source_Path.
    Replaces old Target_Path.  Never copies.
    """
    global Target_Count
    Prepare_Target_Location (Target_Path)
    Target_Path = os.path.normpath (Target_Path)
    Target_Parent_Path = os.path.dirname(Target_Path)
    # Gnat Ada programs and some others don't know about drive letters, 
    # so must use relative symbolic links.
    Slash_Count = Target_Path.count ("/")
    # Depth from root, or "/":
    Slash_Depth = Slash_Count - 1
    Debug_Print ("Target_Path depth is: " + str(Slash_Depth))
    Relative_Source_Path = Source_Path
    while Slash_Depth > 1:
        Relative_Source_Path = "../" + Relative_Source_Path
        Slash_Depth = Slash_Depth - 1
    Relative_Source_Path = os.path.normpath (Relative_Source_Path)
    Debug_Print ("Relative source path is: " + Relative_Source_Path)
    if os.path.exists (Target_Path):
        Run_Or_Log ('os.remove ("' + Target_Path + '")')
    if not os.path.exists (Target_Parent_Path):
        Run_Or_Log ('os.makedirs ("' + Target_Parent_Path + '")')    

    # Windows explorer with CIFS sees symbolic link as file.
    if options.Make_Hard_Links:
        Run_Or_Log ('os.link ("' + Relative_Source_Path + '", "' + Target_Path + '")')
    else:
        Run_Or_Log ('os.symlink ("' + Relative_Source_Path + '", "' + Target_Path + '")')
    Target_Count = Target_Count + 1
                     
def Copy_Or_Link_A_File (Source_Path, Target_Path):
    """Creates a link named Target_Path that points at Source_Path,
    OR copies Source_Path to Target_Path.  Replaces old Target_Path.
    """
    global Target_Count
    if options.Copy_Files:
        Prepare_Target_Location (Target_Path)
        Run_Or_Log ('shutil.copy2 ("' + Source_Path + '", "' + Target_Path + '")')
        Target_Count = Target_Count + 1
    else:
        Link_A_File (Source_Path, Target_Path)
        
def Apex_To_Gnat (File_Name):
    """Converts an Apex file name (without "/"s) to a Gnat file name. If the
    file does not have an Apex file name extension, returns File_Name.
    """        
    Name_Root = File_Name[:-6]
    # Turn the dots into dashes:
    Name_Root = Name_Root.replace(".", "-")
    if File_Name [-6:] == Apex_Spec_Suffix:
        Result = Name_Root + Gnat_Spec_Suffix
    elif File_Name [-6:] == Apex_Body_Suffix:
        Result = Name_Root + Gnat_Body_Suffix
    else:
        Result = File_Name
    return Result
                     
def Gnat_To_Apex (File_Name):
    """Converts a Gnat file name (without "/"s) to an Apex file name. If the
    file does not have a Gnat file name extension, returns File_Name.
    """        
    Name_Root = File_Name[:-4]
    # Turn the dashes into dots:
    Name_Root = Name_Root.replace("-", ".")
    if File_Name [-4:] == Gnat_Spec_Suffix:
        Result = Name_Root + Apex_Spec_Suffix
    elif File_Name [-4:] == Gnat_Body_Suffix:
        Result = Name_Root + Apex_Body_Suffix
    else:
        Result = File_Name
    return Result

def Is_Ada_File (File_Name):
    """Returns True if the file name has an Ada Suffix
    """
    if (File_Name [-4:] == Gnat_Spec_Suffix or
        File_Name [-4:] == Gnat_Body_Suffix or
        File_Name [-6:] == Apex_Spec_Suffix or
        File_Name [-6:] == Apex_Body_Suffix):
        return True
    else:
        return False
                      
def Link_Ada_Files (Source_Path, Target_Path):
    """Creates Target_Path and any non-existent parent directories, then
    creates a link to each Ada file in Source_Path from Target_Path.
    May make Gnat, Apex, or both format links.  
    Also makes links to Gnat Project (.gpr) files and IDL files. 
    """
    global Files_Copied_Or_Linked
    global Files_Processed
    Log ("Link_Ada_Files (" + Source_Path + ", " + Target_Path + ")")
    Debug_Print ("Link_Ada_Files (" + Source_Path + ", " + Target_Path + ")")
    
    for Entry in os.listdir (Source_Path):
        Debug_Print ("Processing '" + Entry + "' - Entry [-4:] is '" + Entry [-4:] + "'")
        Source_Entry_Path = os.path.join (Source_Path, Entry)
        # Don't process any directories:
        if not os.path.isdir(Source_Entry_Path):
            if Is_Ada_File (Entry):
                if options.Make_Both_Format_Targets or options.Make_Gnat_Format_Targets:
                    Shadow_Entry_Path = os.path.join (Target_Path, Apex_To_Gnat(Entry))
                    Copy_Or_Link_A_File (Source_Entry_Path, Shadow_Entry_Path)
                if options.Make_Both_Format_Targets or (not options.Make_Gnat_Format_Targets):
                    Shadow_Entry_Path = os.path.join (Target_Path, Gnat_To_Apex(Entry))
                    Copy_Or_Link_A_File (Source_Entry_Path, Shadow_Entry_Path)
                Files_Copied_Or_Linked = Files_Copied_Or_Linked + 1 
            Files_Processed = Files_Processed + 1 
                    
def Link_IDL_Files (Source_Path, Target_Path):
    """Creates Target_Path and any non-existent parent directories, then
    creates a link to each IDL file in Source_Path from Target_Path.
    """
    global Files_Copied_Or_Linked
    global Files_Processed
    Debug_Print ("Link_IDL_Files (" + Source_Path + ", " + Target_Path + ")")
    
    for Entry in os.listdir (Source_Path):
        Debug_Print ("Processing '" + Entry + "' - Entry [-4:] is '" + Entry [-4:] + "'")
        Source_Entry_Path = os.path.join (Source_Path, Entry)
        # Don't process any directories:
        if not os.path.isdir(Source_Entry_Path):
            if Entry [-4:] == IDL_Suffix:
                Shadow_Entry_Path = os.path.join (Target_Path, Entry)
                Copy_Or_Link_A_File (Source_Entry_Path, Shadow_Entry_Path)
                Link_A_File (Shadow_Entry_Path, Target_IDL_Links_Path + "/" + Entry)
                Files_Copied_Or_Linked = Files_Copied_Or_Linked + 1
            Files_Processed = Files_Processed + 1 
            
#################################################################################
# END Procedures designed to be called by Process_View_Dirs
#################################################################################

def Process_View_Dirs (View_Path, Shadow_Path, The_Process):
    global Apex_Internal_Dirs
    """Recursively processes the directories starting at View_Path, leaving out the internal 
    Rational dirs.  Sends each along with its corresponding shadow directory to The_Process.
    """
    Debug_Print ("Process_View_Dirs (" + View_Path + ", " + Shadow_Path + ")")
    # Actual processing: 
    The_Process (View_Path, Shadow_Path)
    # Don't recurse through any links:
    if os.path.islink (View_Path):
        return
    Entries = os.listdir (View_Path)
    # This is only needed for the first (view) level directory, 
    # but it won't hurt to do it every time:
    # Skip the Rational internal directories:
    for Skip_Dir in Apex_Internal_Dirs:
        if Skip_Dir in Entries:
            Entries.remove (Skip_Dir)
    for Entry in Entries:
        Entry_Path = os.path.join (View_Path, Entry)
        if os.path.isdir (Entry_Path):
            #
            # Recurse:
            #
            Process_View_Dirs (Entry_Path, os.path.join (Shadow_Path, Entry), The_Process)
                       
def Get_Subsystems_At (Root_Path):
    """Returns a list of the subsystem dirs at Root_Path.
    """
    Debug_Print ("Get_Subsystems_At (" + Root_Path + ")")
    Result = []
    for Entry in os.listdir (Root_Path):
        Path = os.path.join (Root_Path, Entry)
        if os.path.isdir (Path) and  Path [-3:] == Subsystem_Suffix:
            Result = Result + [Entry]
    return Result
                       
def Process_Subsystems (View, The_Process, Layer_Path, Target_Layer_Path, Subsystems):
    """Process View in Subsystems at Layer_Path with The_Process
    """
    global Views_Processed
    Debug_Print ("Process_Subsystems (" + View + ", " + `The_Process` + ", " + Layer_Path + ", " + Target_Layer_Path + ", " + `Subsystems` + ")")
    for Subsystem in Subsystems:
        Subsystem_Path = os.path.join (Layer_Path, Subsystem)
        View_Path = os.path.join (Subsystem_Path, View)
        # Trim ".ss" off the end of the target "shadow" subsystem name:
        Shadow_Path = os.path.join (Target_Layer_Path, Subsystem [:-3])
        # Debug_Print ("Process_Subsystems: View_Path   => " + View_Path)
        # Debug_Print ("Process_Subsystems: Shadow_Path => " + Shadow_Path)
        # If this is an existing view, process it:
        if os.path.isdir (View_Path):
            Process_View_Dirs (View_Path, Shadow_Path, The_Process)
            Views_Processed = Views_Processed + 1           

def Process_NIF_Views (Tower_Name, Target_Root_Path, The_Process):
    """Processes the "Tower_Name" view and all directories in it for all NIF subsystems.
    Deletes all links first.
    """
    global Old_Dirs_Deleted
    Debug_Print ("Process_NIF_Views (" + Tower_Name + ", " + Target_Root_Path + ", " + `The_Process` + ")")
    if os.path.exists (Target_Root_Path):
        Run_Or_Log ('shutil.rmtree ("' + Target_Root_Path + '")')
        Old_Dirs_Deleted =  Old_Dirs_Deleted + Target_Root_Path + ", "
        
    for Layer in NIF_Layers:
        Layer_Path = os.path.join (NIF_Root_Path, Layer)
        Target_Layer_Path = os.path.join (Target_Root_Path, Layer)
        Process_Subsystems (
          Tower_Name, 
          The_Process, 
          Layer_Path, 
          Target_Layer_Path, 
          Get_Subsystems_At (Layer_Path)) 
               

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] <simple view name>", 
                          version="%prog 1.2")
    parser.add_option("-a", "--apex",
                      action="store_false", dest="Make_Gnat_Format_Targets", default=True,
                      help="Make only Apex formatted Ada file names (overrides -g if last) [default: %default].")
    parser.add_option("-b", "--both",
                      action="store_true", dest="Make_Both_Format_Targets", default=False,
                      help="Make both Apex and Gnat formatted Ada file names (overrides -a and -g regardless of order) [default: %default].")
    parser.add_option("-c", "--copy",
                      action="store_true", dest="Copy_Files", default=False,
                      help="Make copies, not symbolic links (may not be used with --hard_links) [default: %default].")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="Debug", default=False,
                      help="Turn on debugging [default: %default].")
    parser.add_option("-e", "--effort_only",
                      action="store_true", dest="Effort_Only", default=False,
                      help="Log what would be done without actually doing it [default: %default].")
    parser.add_option("-g", "--gnat",
                      action="store_true", dest="Make_Gnat_Format_Targets", default=True,
                      help="Make only Gnat formatted Ada file names (overrides -a if last) [default: %default].")
    parser.add_option("--hard_links",
                      action="store_true", dest="Make_Hard_Links", default=False,
                      help="Make hard, not symbolic links (may not be used with -c) [default: %default].")
    parser.add_option("-i", "--idl_only",
                      action="store_true", dest="IDL_Only", default=False,
                      help="Only process IDL files [default: %default].")
    parser.add_option("-t", "--test", 
                      action="store_true", dest="Test", default=False,
                      help="Turns on temporary test code - not for general use")
    parser.add_option("-w", "--workspace", 
                      action="store", type="string", dest="Workspace", default="",
                      metavar="<path>", help="Use <path>/src/ada for the Ada and <path>/src/idl for the IDL.")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("expected 1 argument, got " + str (len(args)))
    if options.Copy_Files and options.Make_Hard_Links:
        parser.error("options -c and -h are mutually exclusive")
    Tower_Name = args[0]
    	    
    print "[" + sys.argv [0] + " " + Tower_Name + "]"    
            
    if options.Effort_Only:
        Log_Prefix = "--- Would do: "
    else:
        Log_Prefix = "--- Doing: "
        
    Views_Processed = 0
    Files_Processed = 0
    Files_Copied_Or_Linked = 0
    Target_Count = 0
            
#    Process_NIF_Views (View_Name, Print_Path_And_Shadow)
#    Process_NIF_Views (View_Name, Print_Code_Files)
 
    # # First, process Apex Compiler views with modified contents in 
    # # them for Artisan (these links will not be overwritten) and
    # # put the resulting llinks in the regular shadow tree:
    # Process_Subsystems (
    #   "artisan." + Apex_Current_View, 
    #   Link_Ada_Files, 
    #   Apex_Root_Path, 
    #   os.path.join (NIF_Shadow_Root_Path, Apex_Current_View), 
    #   Apex_Subsystems)

    # # Apex Compiler subsystems:
    # Process_Subsystems (
    #   Apex_Current_View, 
    #   Link_Ada_Files, 
    #   Apex_Root_Path, 
    #   os.path.join (NIF_Shadow_Root_Path, Apex_Current_View), 
    #   Apex_Subsystems)

    if options.Workspace == "":
        Target_Ada_Root_Path = os.path.join (NIF_Shadow_Root_Path, Tower_Name)
        Target_IDL_Root_Path = os.path.join (NIF_Shadow_Root_Path, Tower_Name + "_IDL")
        Target_IDL_Links_Path = os.path.join (Target_IDL_Root_Path, "IDL_Links")
    else:
        Target_Ada_Root_Path = os.path.join (options.Workspace, "src/ada")
        Target_IDL_Root_Path = os.path.join (options.Workspace, "src/idl")
        Target_IDL_Links_Path = os.path.join (options.Workspace, "src/idl_links")
        
    if not options.IDL_Only:
        Process_NIF_Views (Tower_Name, Target_Ada_Root_Path, Link_Ada_Files)
    
    # It's not necessary to delete this at the moment, since the tree is brand new,
    # but this "rmtree" increases this code segment's independence:
    if os.path.exists (Target_IDL_Links_Path):
            Run_Or_Log ('shutil.rmtree ("' + Target_IDL_Links_Path + '")')
    Run_Or_Log ('os.makedirs ("' + Target_IDL_Links_Path + '")') 
    Process_NIF_Views (Tower_Name, Target_IDL_Root_Path, Link_IDL_Files)
    
    print "Views_Processed:        " + `Views_Processed`
    print "Files_Processed:        " + `Files_Processed`
    if options.Workspace != "":
      print "(Above includes once for Ada, once for IDL)"
    print "Files_Copied_Or_Linked: " + `Files_Copied_Or_Linked`
    print "Target_Count:           " + `Target_Count`

    if options.Effort_Only:
        print "Would first have deleted: " + Old_Dirs_Deleted
    else:
        print "First deleted: " + Old_Dirs_Deleted
        
    
