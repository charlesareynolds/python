"""Specifies the files, directories, etc. to be explicitly included and 
excluded when importing into AccuRev. 
"""
import os
import re
from support.local_logging import Logger, LineLogger, FunctionLogger

_logger=Logger(name=__name__, level=Logger.NONDEBUG, 
				showDate=True, 
				showTime=True, 
				showName=False,
				showFunc=True)
_debug = _logger.logger.debug
		
class DirEntryBase (object):
	"""Base class for various directory entry kind specification classes. 
	"""
	pass		
		
class Exclude (DirEntryBase):
	"""A directory entry of this class was explicitly excluded by a filter. 
	"""
	pass		

class NonExcludedEntry (DirEntryBase):
	"""Directory entries of this class were not excluded by a filter. 
	If explicitlyIncluded=True, they were explicitly included by a filter.
	"""
	def __init__(self, explicitlyIncluded=True):
		self.explicitlyIncluded = explicitlyIncluded

class File (NonExcludedEntry):
	def isA(self, path):
		return os.path.isfile(path)
_file=File()

class Directory (NonExcludedEntry):
	def __init__(self, explicitlyIncluded=True, removeTargetTreeFirst=False):
		NonExcludedEntry.__init__(self, explicitlyIncluded)
		self.removeTargetTreeFirst=removeTargetTreeFirst
		
	def isA(self, path):
		return os.path.isdir(path)
	
	def isDirMatchesPattern (self,  path, pattern):
		return (
			# Self is a subclass of Directory.  Prevent infinite recursion by calling Directory.IsA directly:
			Directory.isA(self, path) and 
			re.compile("^.*" + pattern + "$").match(path) > -1)
_directory = Directory()
			
class Subsystem (Directory):
	PATTERN=r"[^/]*\.ss"
	def isA(self, path):
		return self.isDirMatchesPattern (path, self.PATTERN)
_subsystem= Subsystem()
			
class View (Directory):
	PATTERN=r"[^/]*(\.wrk|\.rel)"
	def isA(self, path):
		return self.isDirMatchesPattern (path, self.PATTERN)
_view=View()
			
class Link (NonExcludedEntry):
	"""Conceptually, a link consists of itself and its target, two different paths, thus this
	Link class, instead of having "isLink" in DirEntryBase.
	"""
	def __init__(self, target, copyTarget=False, explicitlyIncluded=True):
		assert isinstance(target, NonExcludedEntry), "link target's class " + str(target.__class__) + " is not in NonExcludedEntry"
		NonExcludedEntry.__init__(self, explicitlyIncluded)
		self.target = target
		self.copyTarget = copyTarget
		
	def isA(self, path):
		return os.path.islink(path)
_link=Link(_file)

class FileFilters():
	""" This class specifies the desired files/directories/subsystems/etc at each level.
	It uses a combination of include/exclude logic to make a list of desired file entries.
	Usage:
	
		nonExcludedEntries = self.filter.allNonExcludedEntriesIn (dir)
		for sourceEntry in nonExcludedEntries.keys():
			if nonExcludedEntries [sourceEntry].explicitlyIncluded:
				# Filtered, included entry behavior:
				self.copy (sourceEntry, targetDir)
			else:
				# Unfiltered, not excluded entry behavior:
				self._logger.warning("Skipping '" + localSourcePath + "'" )
	"""
		
	def __init__(self):
		_debug ('')
		self.__class__._filters = dict()
		
	def addFilter (self, filterName, filterEntries):
		"""Adds a filter to the class wide state.  
		- filterName may be a directory path or an re pattern.
		- filterEntries is a dictionary.  
		-- Each key is a  file name or an re pattern.
		-- Each value is a DirEntryBase object.
		An re pattern is a string starting with "^" or ending with "$".
		"""
		_debug ('"' + filterName + '"')
		assert not self.__class__._filters.has_key(filterName)
		self.__class__._filters [filterName]=filterEntries
		
	def getFilter (self, filterName):
		return self.__class__._filters[filterName]

	def explicitFilterNames (self):
		return self._explicitsOrPatternsOf(self.__class__._filters.keys(), returnPatterns=False)
		
	def patternFilterNames (self):
		return self._explicitsOrPatternsOf(self.__class__._filters.keys(), returnPatterns=True)
	
	def explicitEntriesOf(self, filterName):
		return self._explicitsOrPatternsOf(self.__class__._filters[filterName].keys(), returnPatterns=False)
		
	def patternEntriesOf(self, filterName):
		return self._explicitsOrPatternsOf(self.__class__._filters[filterName].keys(), returnPatterns=True)
		
	def _explicitsOrPatternsOf (self, entries, returnPatterns):
		names = []
		for entry in entries:
			if self._isPattern(entry) == returnPatterns:
				names.append(entry)
		# Sorting helps debugging:
		names.sort()
		return names		
		
	def _isPattern (self, aString):
		if len (aString) == 0:
			return False
		else: 
			return  (aString[0] == "^" or aString[-1] == "$")
	
SUBSYSTEM_PATTERN=Subsystem.PATTERN
VIEW_PATTERN=View.PATTERN
SUBSYSTEM_VIEW_PATTERN=SUBSYSTEM_PATTERN + "/"+ VIEW_PATTERN
NIF_CODE_LAYER_PATTERN="/nif/code/[^/]*"
NIF_CODE_LAYER_SS_PATTERN=NIF_CODE_LAYER_PATTERN + "/" + SUBSYSTEM_PATTERN
					

def _makeClassOrLink(path, theClass, explicitlyIncluded):
	"""	If an entry is a link, it is also whatever it's pointing at.
	"""
	if _link.isA(path):
		targetPath = os.path.realpath(path)
		if path == targetPath:
			raise Exception, "Factory can't find target for recursive link '" + path + "'"
		else:
			target = theClass(explicitlyIncluded=explicitlyIncluded)
			return Link(target, explicitlyIncluded=explicitlyIncluded)
	else:
		return theClass(explicitlyIncluded=explicitlyIncluded)

def createFilterEntry(path, explicitlyIncluded=False):
	"""Returns a subclass of DirEntryBase that matches path.
	"""
	if os.path.exists(path):
		if _view.isA(path):
			return _makeClassOrLink (path, View, explicitlyIncluded)
		elif _subsystem.isA(path):
			return _makeClassOrLink (path, Subsystem, explicitlyIncluded)
		# Check for dir after subsys and view since it is their superclass:
		elif _directory.isA(path):
			return _makeClassOrLink (path, Directory, explicitlyIncluded)
		elif _file.isA(path):
			return _makeClassOrLink (path, File, explicitlyIncluded)
		else:
			raise Exception, "Factory doesn't know how to create entry for path '" + path + "' (not a view, subsystem, directory, or file)"
	else:
		raise Exception, "Factory doesn't know what kind of object to create for non-existent path '" + path + "'"

def sortedKeysOf (sequence):
		"""Returns a copy of sequence's list of keys, sorted.  Sorting things helps debugging.
		"""
		if isinstance (sequence, dict):
			keys = sequence.keys()
		elif isinstance (sequence, set):
			keys = list (sequence)
		keys.sort()
		return keys
				
class DirEntryFiltering (object):
	
	def allNonExcludedEntriesIn (self, sourceDir, fileFilters):
		"""Returns a dictionary of some or all of the directory entries in sourceDir.  
		Leaves out those that should be excluded. 
		Returns the rest. The not explicitly included ones have "explicitlyIncluded = False".
		Does this for all the explicit and pattern filter names that match sourceDir.
		"""
		_debug(sourceDir)
		# 	These instance attribute assignments are for carrying parameters to and from function calls. 
		self.localSourceDir = os.path.normpath(sourceDir)
		self.fileFilters = fileFilters
		self.dirEntrySet = set(os.listdir (self.localSourceDir))
		self.nonExcludedEntries = dict()
		self.entryMatchedEntryPattern = dict()
		# Explicitly-named filters take precedence over pattern-named filters, so they come first:
		self._applyExplicitlyNamedFilters()
		self._applyPatternNamedFilters()
		self._addNotFoundEntries()
		return self.nonExcludedEntries
	
	def _applyExplicitlyNamedFilters (self):
		for filterName in self.fileFilters.explicitFilterNames():
			if self.localSourceDir == filterName:
				self._getIncludedEntries(filterName)
				
	def _applyPatternNamedFilters (self):
		for filterName in self.fileFilters.patternFilterNames():
			if re.compile(filterName).match(self.localSourceDir):
				self._getIncludedEntries(filterName)
				
	def _addNotFoundEntries (self):
		for dirEntry in self.dirEntrySet:
			self.nonExcludedEntries [dirEntry] = createFilterEntry (os.path.join(self.localSourceDir, dirEntry),
														explicitlyIncluded = False)

	def _getIncludedEntries (self, filterName):
		"""Constructs self.nonExcludedEntries from the entries in self.dirEntrySet that should be 
		included according to filterName.  Deletes each found Entry from self.dirEntrySet.
		"""		
		explicitFilterEntries = self.fileFilters.explicitEntriesOf(filterName)
		for dirEntry in sortedKeysOf(self.dirEntrySet):
			# Explicits take precedence over patterns:
			if dirEntry in explicitFilterEntries:
				self._handleFoundDirEntry (dirEntry, filterName, dirEntry)
			else:
				self._checkIfDirMatchesPattern (dirEntry, filterName)
				
	def _checkIfDirMatchesPattern (self, dirEntry, filterName):				
		for pattern in self.fileFilters.patternEntriesOf(filterName):
			if re.compile(pattern).match(dirEntry):
				if self.entryMatchedEntryPattern.has_key(dirEntry):
					raise Exception ("Multiple rules found for dirEntry '" + dirEntry + "'" +
									" prev: '" +  self.entryMatchedEntryPattern[dirEntry] + "', current: '" + pattern + "'")
				else:
					self._handleFoundDirEntry (dirEntry, filterName, pattern)
					self.entryMatchedEntryPattern[dirEntry] = pattern
						
	def _handleFoundDirEntry (self,  dirEntry, filterName, filterEntryName):
		filterEntry=self.fileFilters.getFilter (filterName)[filterEntryName]
		if  isinstance(filterEntry , Exclude):
			action = "EXCLUDED"
		else:
			action = "included"
			if filterEntry.isA (os.path.join(self.localSourceDir, dirEntry)):
				self.nonExcludedEntries [dirEntry] = filterEntry
			else:
				action = "EXCLUDED (dir entry kind mismatch)"
		self.dirEntrySet.remove (dirEntry)
		_debug ("'" + self.localSourceDir + "':'"+ dirEntry + "' is " + action + " by filter '" + filterName + "': '" + filterEntryName + "'")
	
class _Test ():
	def __init__(self):
		self._logger=Logger(name='test_file_filtering', level=Logger.DEBUG, 
						showDate=True, 
						showTime=True, 
						showName=False,
						showFunc=False)
		self._debug = self._logger.logger.debug
		self.log = self._logger.log
	
	def setup (self):	
		self.log("BEGIN test")
		
	def run (self):
		self.testConstructors ()
		self.testCreateFilterEntry ()

	def finish (self):
		#sourcePath="/nif/code/Framework_Services/Generic_Client.ss/reynolds.SCR21941.sol.ada.7.2.0.wrk"
		#self._debug("'" + sourcePath + "'" + str (re.match(re.compile("^" + _view.PATTERN + "$"), sourcePath)))
		#self._debug("'" + sourcePath + "'" + str (re.search(re.compile(_view.PATTERN), sourcePath)))
		self.log("END test (no errors)")
				
	def testConstructors (self): 
		# Be sure these succeed:
		self.filtering = DirEntryFiltering()
		dirEntry = DirEntryBase()
		exclude = Exclude()
		explicitNonExcludedEntry = NonExcludedEntry(explicitlyIncluded = True)
		implicitExcludedEntry = NonExcludedEntry(explicitlyIncluded = False)
		file = File(explicitlyIncluded = True)
		directory = Directory(explicitlyIncluded = True)
		subsystem = Subsystem(explicitlyIncluded = True)
		view = View(explicitlyIncluded = True)
		fileLink = Link(target = File(), copyTarget= False, explicitlyIncluded = True)
		directoryLink = Link(target = Directory(), explicitlyIncluded = True)
		subsystemLink = Link(target = Subsystem(), explicitlyIncluded = True)
		viewLink = Link(target = View(), explicitlyIncluded = True)
		
	def testCreateFilterEntry(self):
		assert createFilterEntry("/nif").__class__ == Directory
		assert createFilterEntry("/nif/.cvspass").__class__ == File
		assert createFilterEntry("/nif/nif").__class__ == Link
		assert createFilterEntry("/nif/nif").target.__class__ == Directory
		assert createFilterEntry("/nif/environment/setup.ss").__class__ == Subsystem
		assert createFilterEntry("/nif/environment/setup.ss/latest.wrk").__class__ == View
		
if __name__ == '__main__':
	test = _Test()
	test.setup()
	test.run()
	test.finish()
