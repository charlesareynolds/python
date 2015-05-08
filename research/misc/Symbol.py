# $Source: /nif/code/Research/C2Ada.ss/.Rational/Version_History/Common/c2ada/Symbol.py,v $
# $Revision: 1.1 $  $Date: 03/09/2006 16:23:56 $

class Symbol:
    def __init__(self,addr):
	self.addr = addr
	#self.requisites = None  # will be assigned when calculated
    def __repr__(self):
	return "oSymbol(0x%x)" % self.addr

    
symboldict = {}

def oSymbol(addr):
    try: 
	return symboldict[addr]
    except:
	result = Symbol(addr)
	symboldict[addr] = result
	return result

def symFilter(syms,test):
    for sym in syms.keys():
	if not test(sym):
	    del syms[sym]
	
