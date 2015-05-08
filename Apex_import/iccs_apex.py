#!/usr/bin/env python
"""Module to hold ICCS'isms associated with APEX
"""

__author__    = "Randy Sanchez"
__version__   = "$Revision: 1.2 $"
__date__      = "$Date: 07/03/2008 08:25:01 $"
__copyright__ = "Copyright 2008 LLNL"

import string

INFIX_VX_ADA_CLIENT   = "vx.ada.client"
INFIX_VX_ADA          = "vx.ada"
INFIX_SOL_ADA_EMUL    = "sol.ada.emul"
INFIX_SOL_ADA_CLIENT  = "sol.ada.client"
INFIX_SOL_ADA         = "sol.ada"
INFIX_GNAT_ADA_CLIENT = "gnat.ada.client"
INFIX_GNAT_ADA        = "gnat.ada"

NO_VALID_INFIX = "NONE"

def getInfixList():
    Infix_List = []
    Infix_List = Infix_List + [INFIX_VX_ADA_CLIENT]
    Infix_List = Infix_List + [INFIX_VX_ADA]
    Infix_List = Infix_List + [INFIX_SOL_ADA_EMUL]
    Infix_List = Infix_List + [INFIX_SOL_ADA_CLIENT]
    Infix_List = Infix_List + [INFIX_SOL_ADA]
    Infix_List = Infix_List + [INFIX_GNAT_ADA_CLIENT]
    Infix_List = Infix_List + [INFIX_GNAT_ADA]
    return Infix_List

def isValidInfixStream(aString):
    """Validates wether the given string has a valid <infix> string located within it.
            Returns True if it does.
            False if it does not.
    """
    Infix_List = getInfixList()
    for infix in Infix_List:
        if (string.find(aString, infix) > 0):
            return True
    return False
    
def whatInfixIsStream(aString):
    """Determines the <infix> string that the given string is associated with.
        Returns '<infix>' string if a valid one is found.
                'NONE' if no valid <infix> string is found.
    """
    Infix_List = getInfixList()
    for infix in Infix_List:
        if (string.find(aString, infix) > 0):
            return infix
    return NO_VALID_INFIX
    
def findPrefixInfixPostFix(self, aString):
    """Finds the <prefix>, <infix> and <postfix> strings associated with the given string.
        The <infix> is one of the valid Infix strings define in getInfixList().
        Returns a tuple as follows:
            (<prefix>, <infix>, <postfix>) or
            ('NONE', 'NONE', 'NONE') if a valid <infix> string could not be found.
    """
    Infix_Stream = self.whatInfixIsStream(aString)
    if (Infix_Stream == NO_VALID_INFIX):
        return (NO_VALID_INFIX, NO_VALID_INFIX, NO_VALID_INFIX)
        
    Prefix_Stream, Postfix_Stream = string.split(aString, Infix_Stream)
    return (Prefix_Stream, Infix_Stream, Postfix_Stream)
