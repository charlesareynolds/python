# $Source: /nif/code/Research/C2Ada.ss/.Rational/Version_History/Common/c2ada/UnitDict.py,v $
# $Revision: 1.1 $  $Date: 03/09/2006 16:23:57 $

# A UnitDict is a dictionary that maps unit numbers to lists.
# This module is used in aux_decls to keep track of various interesting
# types associated with a module.

class UnitDict:
    def __init__(self):
	self.dict = {}
    def entry(self, key):
	try:
	    return self.dict[key]
	except:
	    result = []
	    self.dict[key] = result
	    return result

# The lists use_type record the types for which the Ada module
# requires a "use type" declaration.
#
use_type = UnitDict()

# The lists in stdarg_concat record the types for which the
# Ada module requires an instantation of Stdarg.Concat.
#
stdarg_concat = UnitDict()
