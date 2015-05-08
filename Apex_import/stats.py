"""Contains class singleton stats which counts import actions and prints a summary.
"""

from support.local_logging import Logger, LineLogger, FunctionLogger
from support.string_utils import su

class _Stats():
	__COUNT_ATTRS=(
			"subsystemsProcessed",
			"viewsProcessed",
			"dirsProcessed",
			"filesCopied",
			"filesDeletedFirst",
			"itemsSkipped")
	
	def __init__(self):
		self._effortOnly=False
		self._counts=dict()
		for countAttr in self.__COUNT_ATTRS:
			self._counts[countAttr]=0
		self._dirsDeleted=""
		self._ssWithoutView=set()
		# self._startTime = time.clock()
		
	def setEffortOnly(self, effortOnly):
		self._effortOnly=effortOnly
		
	def increment(self, attrName, inc=1):
		self._counts[attrName] += inc

	def addDeletedDir(self, dir):
		self._dirsDeleted = su.concatWString(self._dirsDeleted, ", ", dir)
		
	def addSs(self, ss):
		self._ssWithoutView.add(ss)
		
	def noteSsHasView(self, ss):
		if ss in self._ssWithoutView:
			self._ssWithoutView.remove(ss)
		
	def printStats(self):
		ssWithoutView = list(self._ssWithoutView)
		ssWithoutView.sort()
		print ("There were " + str(len(ssWithoutView)) + " subsystems with no views processed: ")
		for ss in ssWithoutView:
			print (ss)
		print
		for countAttr in self.__COUNT_ATTRS:
			print (str(countAttr) + ": " + str(self._counts[countAttr]))
		if self._effortOnly:
			print ("Would first have deleted: " + self._dirsDeleted)
		else:
			print ("First deleted: " + self._dirsDeleted)
		# inaccurate?  (too short compared to log):
		#print("Took " + str(time.clock() - self._startTime) + " seconds")
		
stats=_Stats()


class _Test ():
	def __init__(self):
		self._logger=Logger(name='test_stats', level=Logger.DEBUG, 
						showDate = True, 
						showTime = True, 
						showName = False,
						showFunc = False)
		self._debug = self._logger.logger.debug
		self.log = self._logger.log
	
	def setup (self):
		test.log("BEGIN test")
	
	def run (self):
		stats.increment("subsystemsProcessed", 1)
		stats.increment("viewsProcessed", 2)
		stats.increment("dirsProcessed", 3)
		stats.increment("filesCopied", 4)
		stats.increment("filesDeletedFirst", 5)
		stats.increment("itemsSkipped", 6)
		stats.addDeletedDir("foo")
		stats.addDeletedDir("foobar")
		stats.addSs("/nif/code/Support/Utilities.ss")
		stats.addSs("/nif/code/Support/IDL.ss")
		stats.noteSsHasView("/nif/code/Support/IDL.ss")
		stats.noteSsHasView("/nif/code/Support/IDL.ss")
		stats.printStats()
		
	def finish (self):
		self.log("END test")
		
if __name__ == '__main__':
	test = _Test()
	test.setup()
	test.run()
	test.finish()
	