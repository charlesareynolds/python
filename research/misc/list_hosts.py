#!/usr/bin/env python
"""Utility to make a list of UINIX hosts and identify their OS and machine kinds
"""


# 2007/06/22 CAR SCR20738 Took out CORBA shadowing, since the gnat CORBA project 
# 		files now refer to the distribution views directly.
# 2007/07/12 CAR SCR 20738 changing back to hard links for Windows.

__author__ = "Charles Reynolds"
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 02/27/2008 07:32:56 $"
__copyright__ = "Copyright 2007 LLNL"

import nis
#import os
#import shutil
from subprocess import *
import sys
import time
#import thread
#import threading

Log_Prefix = "UNDEFINED"

Debug = True
Effort_Only = False

#################################################################################
# BEGIN Procedures designed to be called by Process_View_Dirs
#################################################################################
    
def Debug_Print (Message):
    if Debug:
        print "$$$ " + Message

The_Errors = open ("list_hosts.err", "w")      
The_Output = open ("list_hosts.out", "w")      
The_Thread_List = []  

def Process_Host (Host):
    """Process one host in the background.
    """
    Debug_Print ("Process_Host (" + Host + ")")
    global Popen
    global The_Output
    global The_Thread_List
    Command = ("rsh", Host, "uname", "-a")
    The_Thread_List.append(Popen (Command, shell=False, stdout=The_Output, stderr=The_Errors))      
    
        
def Process_Hosts ():
    """Process all the hosts in ypcat
    """
    Index = 0
    for Host in nis.cat ("hosts"):
        """Only run a certain number of subprocesses at a time.  
        Clear out the completed ones and check if under 100 every second:
        500 results in "rcmd: socket: Cannot assign requested address"
        """ 
        while len(The_Thread_List) > 100:
            for Thread in The_Thread_List:
                if Thread.poll() != None:
                    Debug_Print ("Removing" + str (Thread))        
                    The_Thread_List.remove(Thread)
            Debug_Print ("Sleeping")        
            time.sleep (1)      
              
        Process_Host (Host)
        Index = Index + 1
#        """Don't try doing them all yet:
#        """
#        if (Index >= 200):
#            break
            
    Process_Host ("calaveras")  
    Process_Host ("superglide")  
        
if __name__ == "__main__":
    if not (len (sys.argv) == 1):
        print "Usage: " + sys.argv [0]
        sys.exit (-1)
            
    print ("::: Running " + sys.argv [0])
    Process_Hosts ()
    print ("::: " + sys.argv [0] + " complete.")
