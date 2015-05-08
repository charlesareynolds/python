"""Contains classes to identify and handle directories, links, views, subsystems, and files.
Basically, those classes just add copy behavior to file_filters.py.
class Utils supplies all the path name modification operations to the directory etc. 
classes copy operations.
"""
import file_filters
import os
import re
import shutil
from stats import stats
import support.runner
from support.string_utils import su
from support.local_logging import Logger, LineLogger, FunctionLogger
# import time

lineLogger=LineLogger()
runner = support.runner.runner
_logger = Logger(name='dir_entries.py', level=Logger.DEBUG, 
				showDate=True, 
				showTime=True, 
				showName=False,
				showFunc=True)
_debug = _logger.logger.debug
_log = _logger.logger.info

class Utils (object):
	"""Place to collect various utilities
	TODO: refactor later
	"""
	NEW_NIF_CODE = "/src/code"
	NEW_NIF_IDL = "/src/idl"
	
	skipClean = False
	def setTargetRoot (self, targetRoot):
		self.targetRoot = targetRoot
	
	def constructTargetPath(self, targetPath):
		"""Modify targetPath as needed.
		constructTargetPath is used both by Directory.copy on the directory path, and by 
		adjustLinkTarget on the link target path.  Targets that would not be copied 
		(e.g. /etc/hosts) must be treated differently that those that would be (e.g. 
		/nif/code/Framework_Templates/System_Manager.ss/accurev.7.2.0.rel).
		Successive processing of the same target will not wipe out any previous changes.
		"""
		localTargetPath = targetPath
		localTargetPath = self._changeNifToTargetRoot(localTargetPath)
		localTargetPath = self._changeCodeToSrcCode(localTargetPath)
		localTargetPath = self._extractTargetTree (localTargetPath)
		localTargetPath = self._extractIDLTree (localTargetPath)
		localTargetPath = self._extractShadowTree (localTargetPath)
		localTargetPath = self._trimView (localTargetPath)
		localTargetPath = self._trimSS (localTargetPath)
		return localTargetPath
	
	def _changeNifToTargetRoot (self,  targetPath):
		"""change  
		"/nif"
		to 
		"self.targetRoot"
		but only for 
		/nif/code
		/nif/environment
		/nif/rational
		/nif/tools
		"""
		if re.compile("^/nif/(code|environment|rational|tools).*").match(targetPath):
			return re.sub("^/nif",  self.targetRoot, targetPath, 1)
		else:
			return targetPath
			
	def _changeCodeToSrcCode (self,  targetPath):
		"""change  
		<workspace>/code
		to 
		<workspace><NEW_NIF_CODE>
		"""
		return re.sub("^" + self.targetRoot + "/code",  self.targetRoot + self.NEW_NIF_CODE, targetPath, 1)
			
	def _extractTargetTree (self, targetPath):
		"""change  
		<workspace><NEW_NIF_CODE>/.../AAA_os_specific/<platform>/...
		to 
		<workspace><NEW_NIF_CODE>/Target/<platform>/.../...
		"""
		result =self._changeCodeToSrcCode(targetPath)
		for platform in (
			    "ppc-vxworks",
			    "sparc-solaris",
			    "x86-linux",
			    "x86-windows"):
			AAASegment = "/AAA_os_specific/" + platform
			if result.find(AAASegment) > -1:
				# _debug('FOUND (AAASegment = "' + AAASegment + '")')
				newSrcRoot = self.targetRoot + self.NEW_NIF_CODE + "/Target/" + platform
				result = result.replace(AAASegment, "").replace(self.targetRoot + self.NEW_NIF_CODE, newSrcRoot)
				#_debug('(targetPath = "' + targetPath + '", result = "' + result + '")')
		return result
	
	def _trimSS (self, targetPath):
		"""Change .../<subsystem>.ss/... to .../<subsystem>/...
		"""
		result = re.sub(r"\.ss$", "", targetPath, 1)
		result = re.sub(r"\.ss/", "/", result, 1)
		return result

	def _trimView (self, targetPath):
		"""Change .../<view> to ...
		TODO: leave /nif/rational/base/ada views in.  We have multiple source views from the same subsystem.
		"""
		return re.sub("/" + file_filters.View.PATTERN, "", targetPath, 1)

	def _extractIDLTree (self, targetPath):
		"""change  
		<workspace><NEW_NIF_CODE>/.../IDL
		or
		<workspace>/src/.../IDL
		to 
		<workspace>/src/idl/...
		but not for <workspace>/src/Support/IDL  or .../Support/IDL.ss
		but not for <workspace>/src/Framework_Templates/IDL_CORBA
		but not for <workspace>/src/Target/ppc-vxworks/Support/IDL
		but not for <workspace>/src/code/Support/IDL
		"""
		srcRoot = "(?P<srcRoot>" + self.targetRoot + "/src)"
		notTargetPlatform = r"(?!/Target/[^/]+)"
		layer = r"(?P<layer>/[^/]+)"
		subsystem = r"(?P<subsystem>/[^/]+(\.ss)?)"
		subdirs1 = r"(?P<subdirs1>(/.*)*)"
		subdirs2 = r"(?P<subdirs2>($)|(/.*))"
		result = re.sub(
					pattern = srcRoot + "(/code)" + notTargetPlatform + layer + subsystem + subdirs1 + "(/IDL)" + subdirs2, 
					repl = r"\g<srcRoot>/idl\g<layer>\g<subsystem>\g<subdirs1>\g<subdirs2>", 
					string = targetPath)
		#_debug('(targetPath = "' + targetPath + '", result = "' + result + '")')
		return result
	
	def _extractShadowTree (self, targetPath):
		"""change  
		<workspace><NEW_NIF_CODE>/Slices/Shadow_Deployment.ss/<.view>/foo...
		to 
		<workspace>/foo...
		"""
		root = r"(?P<root>" + self.targetRoot + r")"
		subdirs = r"(?P<subdirs>($)|(/.*))"
		result = re.sub(
					pattern = root + self.NEW_NIF_CODE + r"/Slices/Shadow_Deployment(\.ss)?" + subdirs, 
					repl = r"\g<root>/product\g<subdirs>", 
					string = targetPath)
		return result
	
	def prepareTargetLocation (self, targetPath):
		"""Prepares to link or copy a file.  Deletes the target, 
		and creates any needed target directories.
		"""
		if not self.__class__.skipClean and os.path.exists (targetPath):
			runner.runOrLog ('os.remove ("' + targetPath + '")', globals(), locals())
			stats.increment("filesDeletedFirst")
		targetParentPath = os.path.dirname(targetPath)
		if not os.path.exists (targetParentPath):
			runner.runOrLog ('os.makedirs ("' + targetParentPath + '")', globals(), locals())
			
	def join (self, dir, entry):
		"""Returns "<dir>/<entry>" unless entry is "".  Then, returns "<dir>" 
		"""
		if entry == "":
			return dir
		else:
			return os.path.join (dir, entry)
		
	def adjustLinkTarget (self, sourcePath, targetPath):
		"""Returns a relative path from sourcePath to targetPath.
		If targetPath is not in /nif/(code|environment|rational|tools), returns targetPath.
		"""
		def toAbsPath (sourcePath, targetPath):
			if targetPath[0] != '/': 
				return os.path.realpath(os.path.join(sourcePath, targetPath))
			else:
				return  os.path.normpath (targetPath)
						
		def dotDotCount (string):
			searchResult = re.findall (r"\.\./", string)
			return len(searchResult)
		
		def partsOf (path):
			return re.findall (r"[^/]+", path)
						
		def segmentCount (path):
			pathParts = partsOf (path)
			return len(pathParts)
		
		def inWorkspace (path):
			"""For /nif/code, return true, for /oracle return false, etc.
			"""
			return re.compile (r"^/nif/(code|src|environment|rational|tools)").match(path)
		
		absTargetPath = toAbsPath (sourcePath, targetPath)
		if not inWorkspace (absTargetPath):
			result = absTargetPath
		else:
			localSourcePath = self.constructTargetPath (sourcePath)
			localTargetPath = self.constructTargetPath (absTargetPath)
			result = "."
			targetPathParts = partsOf (localTargetPath)
			sourcePathParts = partsOf (localSourcePath)
			targetPathLength = len (targetPathParts)
			sourcePathLength = len (sourcePathParts)
			minLength = min(sourcePathLength, targetPathLength)
			pathsDiverged = False
			for index in range (minLength):
				if targetPathParts [index] != sourcePathParts [index]:
					pathsDiverged = True
				if pathsDiverged:
					result = os.path.join ("..", result, targetPathParts [index])
			for index in range (sourcePathLength - minLength):
				result = os.path.join ("..", result)
			for index in range (targetPathLength - minLength):
				result = os.path.join (result, targetPathParts [index + minLength])
			
			result = self.constructTargetPath (os.path.normpath (result))
		return result
		

	def test (self):
		def assertEq (l,r):
			"""Call this instead of assert, when you want to see what values made the assert fail.
			"""
			try:
				assert l == r
			except AssertionError:
				print (str(l) + " != " + str(r))
				raise
		
		def assert_extractIDLTreeEqWOrWoFile (targetPath, resultPath):
			assertEq (self._extractIDLTree(self.targetRoot + "/" + targetPath),
												self.targetRoot + "/" + resultPath)
			assertEq (self._extractIDLTree(self.targetRoot + "/" + targetPath + "/file"),
												self.targetRoot + "/" + resultPath + "/file")
			
		def assertIDLTreeEqSsViewVariations (targetPrefix, targetSuxffix, resultPrefix, resultSuffix):
			view = "accurev.7.2.0.rel"
			assert_extractIDLTreeEqWOrWoFile (targetPrefix + ".ss/" + view + targetSuxffix,
												resultPrefix + ".ss/" + view + resultSuffix)
			assert_extractIDLTreeEqWOrWoFile (targetPrefix + "/" + view + targetSuxffix,
												resultPrefix + "/" + view + resultSuffix)
			assert_extractIDLTreeEqWOrWoFile (targetPrefix + ".ss" + targetSuxffix,
												resultPrefix + ".ss" + resultSuffix)
			assert_extractIDLTreeEqWOrWoFile (targetPrefix + "" + targetSuxffix,
												resultPrefix + ""  + resultSuffix)		
			
		def assertProperIDLTreeChanges (layerSsWithoutss):
			assertIDLTreeEqSsViewVariations(
										targetPrefix = "src/code/" + layerSsWithoutss, targetSuxffix = "/IDL", 
										resultPrefix = "src/idl/" + layerSsWithoutss, resultSuffix = "")
			
		def assertNo_extractIDLTreeChanges (layerSsWithoutss):
			assertIDLTreeEqSsViewVariations(
										targetPrefix = "src/code/" + layerSsWithoutss, targetSuxffix = "", 
										resultPrefix = "src/code/" + layerSsWithoutss, resultSuffix = "")
			
		assert (self.targetRoot != None)
		assert (self.targetRoot != "")
		
		assert (self._changeNifToTargetRoot ("/nif/code") == self.targetRoot + "/code")
		assert (self._changeNifToTargetRoot ("/nif/code/foo") == self.targetRoot + "/code/foo")
		assert (self._changeNifToTargetRoot ("/nif/environment") == self.targetRoot + "/environment")
		assert (self._changeNifToTargetRoot ("/nif/rational") == self.targetRoot + "/rational")
		assert (self._changeNifToTargetRoot ("/nif/tools") == self.targetRoot +"/tools")

		assert (self._changeCodeToSrcCode (self.targetRoot + "/code") == self.targetRoot + self.NEW_NIF_CODE)
		assert (self._changeCodeToSrcCode (self.targetRoot + "/src") == self.targetRoot + "/src")
		assert (self._changeCodeToSrcCode (self.targetRoot + "/code/Controllers.ss") == self.targetRoot + self.NEW_NIF_CODE + "/Controllers.ss")
		assert (self._changeCodeToSrcCode (self.targetRoot + self.NEW_NIF_CODE + "/Controllers.ss") == self.targetRoot + self.NEW_NIF_CODE + "/Controllers.ss")
		assert (self._changeCodeToSrcCode ("/tmp/code") == "/tmp/code")

		assertEq (self._extractTargetTree  (self.targetRoot + self.NEW_NIF_CODE + "/Controllers/Motor_Controllers.ss/accurev.7.2.0.rel/AAA_os_specific/x86-linux"), 
			self.targetRoot + self.NEW_NIF_CODE + "/Target/x86-linux/Controllers/Motor_Controllers.ss/accurev.7.2.0.rel")
		assert (self._extractTargetTree  (self.targetRoot + self.NEW_NIF_CODE + "/Controllers/Motor_Controllers.ss/accurev.7.2.0.rel/AAA_os_specific/x86-linux/file") == 
			self.targetRoot + self.NEW_NIF_CODE + "/Target/x86-linux/Controllers/Motor_Controllers.ss/accurev.7.2.0.rel/file")
		assert (self._extractTargetTree  (self.targetRoot + self.NEW_NIF_CODE + "/Target/x86-linux/Controllers/Motor_Controllers.ss/accurev.7.2.0.rel") == 
			self.targetRoot + self.NEW_NIF_CODE + "/Target/x86-linux/Controllers/Motor_Controllers.ss/accurev.7.2.0.rel")
		
		assert (self._trimSS ("/fred.ss") == "/fred")
		assert (self._trimSS ("/fred.ss/foo") == "/fred/foo")
		assert (self._trimSS ("/fred") == "/fred")

		assert (self._trimView ("/view.wrk") == "")
		assert (self._trimView ("/view.rel") == "")
		assert (self._trimView ("subsystem.ss/view.rel") == "subsystem.ss")
		assert (self._trimView ("subsystem.ss/view.rel/foo") == "subsystem.ss/foo")
		assert (self._trimView ("") == "")
		
		assertProperIDLTreeChanges("Support/Utilities")
		assertNo_extractIDLTreeChanges("Support/IDL")
		assertNo_extractIDLTreeChanges("Framework_Templates/IDL_CORBA")
		assertProperIDLTreeChanges("Framework_Templates/IDL_CORBA")
		assertNo_extractIDLTreeChanges("Framework_Services/IDL_Services")
		assertNo_extractIDLTreeChanges("Main_Programs/IDL_Client_Examples")
		assertNo_extractIDLTreeChanges("Main_Programs/IDL_Server")
		
		assert (self.constructTargetPath ("/arbitrary") == "/arbitrary")
		assert (self.constructTargetPath ("/nif") == "/nif")
		assert (self.constructTargetPath ("/nif/arbitrary") == "/nif/arbitrary")
		
		assert (self.constructTargetPath ("/nif/code") == self.targetRoot + self.NEW_NIF_CODE)
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE) == self.targetRoot + self.NEW_NIF_CODE)
		
		assert (self.constructTargetPath ("/nif/code/Support.ss") == self.targetRoot + self.NEW_NIF_CODE + "/Support")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support.ss") == self.targetRoot + self.NEW_NIF_CODE + "/Support")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support") == self.targetRoot + self.NEW_NIF_CODE + "/Support")
		
		assert (self.constructTargetPath ("/nif/code/Support/Utilities.ss/accurev.7.2.0.rel") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities.ss/accurev.7.2.0.rel") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/accurev.7.2.0.rel") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities")
		
		assert (self.constructTargetPath ("/nif/code/Support/Utilities.ss/accurev.7.2.0.rel/subdir") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/subdir")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities.ss/accurev.7.2.0.rel/subdir") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/subdir")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/accurev.7.2.0.rel/subdir") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/subdir")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/subdir") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/subdir")
		
		assertEq (self.constructTargetPath ("/nif/code/Support/Utilities.ss/accurev.7.2.0.rel/IDL"),
											self.targetRoot + self.NEW_NIF_IDL + "/Support/Utilities")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities.ss/accurev.7.2.0.rel/IDL") == 
											self.targetRoot + self.NEW_NIF_IDL + "/Support/Utilities")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/accurev.7.2.0.rel/IDL") == 
											self.targetRoot + self.NEW_NIF_IDL + "/Support/Utilities")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/IDL") == 
											self.targetRoot + self.NEW_NIF_IDL + "/Support/Utilities")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_IDL + "/Support/Utilities") == 
											self.targetRoot + self.NEW_NIF_IDL + "/Support/Utilities")

		assert (self.constructTargetPath ("/nif/code/Support/IDL.ss") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/IDL")
		assert (self.constructTargetPath (	self.targetRoot + self.NEW_NIF_CODE + "/Support/IDL.ss") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/IDL")
		assert (self.constructTargetPath (	self.targetRoot + self.NEW_NIF_CODE + "/Support/IDL") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/IDL")
		
		assert (self.constructTargetPath ("/nif/code/Support/Utilities.ss/accurev.7.2.0.rel/AAA_os_specific") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/AAA_os_specific")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/AAA_os_specific") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/AAA_os_specific")
		assert (self.constructTargetPath ("/nif/code/Support/Utilities.ss/accurev.7.2.0.rel/AAA_os_specific/ppc-vxworks") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Target/ppc-vxworks/Support/Utilities")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/Utilities/AAA_os_specific/ppc-vxworks") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Target/ppc-vxworks/Support/Utilities")
		
		assert (self.constructTargetPath ("/nif/code/Support/IDL.ss/accurev.7.2.0.rel/AAA_os_specific") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/IDL/AAA_os_specific")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/IDL/AAA_os_specific") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Support/IDL/AAA_os_specific")
		assert (self.constructTargetPath ("/nif/code/Support/IDL.ss/accurev.7.2.0.rel/AAA_os_specific/ppc-vxworks") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Target/ppc-vxworks/Support/IDL")
		assert (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Support/IDL/AAA_os_specific/ppc-vxworks") == 
											self.targetRoot + self.NEW_NIF_CODE + "/Target/ppc-vxworks/Support/IDL")
		
		assertEq (self.constructTargetPath ("/nif/code/Slices/Shadow_Deployment.ss/accurev.7.2.0.rel"), 
											self.targetRoot + "/product")
		assertEq (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Slices/Shadow_Deployment.ss/accurev.7.2.0.rel"), 
											self.targetRoot + "/product")
		assertEq (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Slices/Shadow_Deployment/accurev.7.2.0.rel"), 
											self.targetRoot + "/product")
		assertEq (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Slices/Shadow_Deployment"),
											self.targetRoot + "/product")
		
		assertEq (self.constructTargetPath ("/nif/code/Slices/Shadow_Deployment.ss/accurev.7.2.0.rel/foo"),
											self.targetRoot + "/product/foo")
		assertEq (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Slices/Shadow_Deployment.ss/accurev.7.2.0.rel/foo"), 
											self.targetRoot + "/product/foo")
		assertEq (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Slices/Shadow_Deployment/accurev.7.2.0.rel/foo"), 
											self.targetRoot + "/product/foo")
		assertEq (self.constructTargetPath (self.targetRoot + self.NEW_NIF_CODE + "/Slices/Shadow_Deployment/foo"), 
											self.targetRoot + "/product/foo")
		

		# Test paths within the same workspace:
		assertEq (self.adjustLinkTarget (
											"/nif/code/a/b/c/d/e", 
											"/nif/code/a/b/c/d/e"), ".")
		assert (self.adjustLinkTarget (
											"/nif/environment/a/b/c/d/e", 
											"/nif/environment/a/b/c/d/e") == ".")
		assert (self.adjustLinkTarget (
											"/nif/rational/a/b/c/d/e", 
											"/nif/rational/a/b/c/d/e") == ".")
		assert (self.adjustLinkTarget (
											"/nif/tools/a/b/c/d/e", 
											"/nif/tools/a/b/c/d/e") == ".")
		assertEq (self.adjustLinkTarget (
											"/nif/code/a/b/c/d/e", 
											"/nif/code/a/b/c/d"), "..")
		assert (self.adjustLinkTarget (
											"/nif/code/a/b/c/d", 
											"/nif/code/a/b/c/d/e") == "e")
		assert (self.adjustLinkTarget (
											"/nif/code/a/b/c/d", 
											"/nif/code/a/b/c/e") == "../e")
		assert (self.adjustLinkTarget (
											"/nif/code/a/b/c/d", 
											"/nif/code/a/b/c/e/f") == "../e/f")
		assert (self.adjustLinkTarget (
											"/nif/code/a/b/c", 
											"/nif/code/d/e/f") == "../../../d/e/f")
		assert (self.adjustLinkTarget (
											"/nif/code/a/b/c/d/e", 
											"c/d/e") == "c/d/e")
		assert (self.adjustLinkTarget (
											"/nif/code/a/b/e", 
											"/nif/code/a/b/c/d/e") == "../c/d/e")
		# test paths outside the workspace:
		assert (self.adjustLinkTarget (
											"/nif/data/a/b/c/d/e", 
											"/nif/data/a/b/c/d/e") == "/nif/data/a/b/c/d/e")
		assert (self.adjustLinkTarget (
											"/nif/data/a/b/c/d/e", 
											"/oracle/program") == "/oracle/program")
		
		# test that link target gets adjusted like other targets:
		assertEq (self.adjustLinkTarget (
											"/nif/environment/oracle/coraenv",
											"/nif/code/Support/Database_Admin.ss/sol.db.7.2.0.rel/Environment/coraenv"),  
											"../../.." + self.NEW_NIF_CODE + "/Support/Database_Admin/Environment/coraenv")
						
_utils = Utils()

class File (file_filters.File):
	def copy (self, sourcePath, targetPath, fileFilters):
		"""Copies sourcePath to targetPath.  Replaces old targetPath.  
		Preserves the source file's attributes.  
		Creates any missing intermediate directories.
		If the source file is a link, copies the file it is pointing at.
		See class Link.
		"""
		_utils.prepareTargetLocation (targetPath)
		runner.runOrLog ('shutil.copy2 ("' + sourcePath + '", "' + targetPath + '")', globals(), locals())
		stats.increment("filesCopied")
		
file = File()
	
class Directory (file_filters.Directory):
	# Keep state between calls:
	_skipDirs = ()
	
	def setSkipDirs(self, skipDirs):
		self.__class__._skipDirs = skipDirs
		
	def copy (self, sourcePath, targetPath, fileFilters):
		""" Copy all the entries in a directory, recursively.
		"""		
		_debug(str(self.__class__) + '(sourcePath = "' + sourcePath + '", targetPath = "' + targetPath + '")')
		if sourcePath in self._skipDirs:
			_log('SKIPPING "' + sourcePath + '" per command line option')
			stats.increment("itemsSkipped")
		else:	
			localTargetPath = _utils.constructTargetPath(targetPath) 
			if self.removeTargetTreeFirst:
				self._removeTargetTree (localTargetPath)
				if localTargetPath.find (_utils.targetRoot + "/src/code") > -1:
 					self._removeTargetTree (_utils.targetRoot + "/src/idl")
					
			nonExcludedEntries = file_filters.DirEntryFiltering().allNonExcludedEntriesIn(sourcePath, fileFilters)
			for sourceEntry in file_filters.sortedKeysOf(nonExcludedEntries):
				_createDirEntryFromFilterEntry(
											nonExcludedEntries [sourceEntry]).copy(
																				_utils.join (sourcePath, sourceEntry), 
																				_utils.join(localTargetPath, sourceEntry),
																				fileFilters)
			stats.increment("dirsProcessed")
			
	def _removeTargetTree (self, targetPath):
		_debug('(targetPath = "' + targetPath + '")')
    	# TODO: fix to handle read-only permission error
		if  os.path.exists (targetPath):
			runner.runOrLog ('shutil.rmtree ("' + targetPath + '")', globals(), locals())
			stats.addDeletedDir (targetPath)			
				
directory = Directory()
		
class Subsystem (file_filters.Subsystem):
	def copy(self, sourcePath, targetPath, fileFilters):
		""" Copy the one wanted (usually the "tower") view in a subsystem.
		"""		
		_debug(str(self.__class__) + '(sourcePath = "' + sourcePath + '", targetPath = "' + targetPath + '")')
		stats.addSs(sourcePath)
		Directory().copy (sourcePath, targetPath, fileFilters)
		stats.increment("subsystemsProcessed")
			
class View (file_filters.View):
	def copy(self, sourcePath, targetPath, fileFilters):
		""" Copy the files and directories in a view.
		"""		
		_debug(str(self.__class__) + '(sourcePath = "' + sourcePath + '", targetPath = "' + targetPath + '")')
		stats.noteSsHasView(os.path.dirname(sourcePath))
		Directory().copy (sourcePath, targetPath, fileFilters)
		stats.increment("viewsProcessed")
			
class Link (file_filters.Link):
	def __init__(self, target, copyTarget=True, explicitlyIncluded=True):
		file_filters.Link.__init__(self, target, copyTarget=copyTarget, explicitlyIncluded=explicitlyIncluded)
		
	def copy(self, sourcePath, targetPath, fileFilters):
		"""If copyTarget is true, copies the linked-to Entry to the target, using the 
		real (pointed-to) path as the sourcePath.  Otherwise, copies the link 
		itself, modified for where the linked-to Entry is now.
		"""
		_debug(str(self.__class__) + '(sourcePath = "' + sourcePath + '", targetPath = "' + targetPath+ '", self.copyTarget = "' + str (self.copyTarget) + '")')
		sourceLinkTarget=os.path.realpath(sourcePath)
		if self.copyTarget:
			self.target.copy(sourceLinkTarget, targetPath, fileFilters)
		else:
			self._copyLink(sourcePath, sourceLinkTarget, targetPath)
			
	def _copyLink(self, sourcePath, sourceLinkTarget, targetPath):
		"""Create a link in the new location with the same relative target as the link in the old location.
		"""
		relativeLinkTarget = _utils.adjustLinkTarget(os.path.dirname(sourcePath), sourceLinkTarget)
		_utils.prepareTargetLocation (targetPath)
		runner.runOrLog ('os.symlink ("' + relativeLinkTarget + '", "' + targetPath + '")', globals(), locals())

def _createDirEntryFromFilterEntry(entry, explicitlyIncluded=False):
	# Checks using __class__= instead of isinstance to avoid finding membership in parent classes
	if entry.__class__ == file_filters.File:
		result = File (explicitlyIncluded=explicitlyIncluded)
	elif entry.__class__ ==  file_filters.Directory:
		result = Directory (explicitlyIncluded=explicitlyIncluded, removeTargetTreeFirst=entry.removeTargetTreeFirst)
	elif entry.__class__ ==  file_filters.Subsystem:
		result = Subsystem (explicitlyIncluded=explicitlyIncluded)
	elif entry.__class__ ==  file_filters.View:
		result = View (explicitlyIncluded=explicitlyIncluded)
	elif entry.__class__ ==  file_filters.Link:
		result = Link (target=_createDirEntryFromFilterEntry (entry.target),  copyTarget=entry.copyTarget, explicitlyIncluded=explicitlyIncluded)
	else:
		raise Exception, "don't know how to create " + str (entry)
	return result

def createDirEntry(path, explicitlyIncluded=False):
	"""Returns a subclass of DirEntry that matches path.
	"""
	fileFilterEntry = file_filters.createFilterEntry (path, explicitlyIncluded)
	return _createDirEntryFromFilterEntry (fileFilterEntry, explicitlyIncluded)	
			
class _Test ():
	def __init__(self):
		self._logger=Logger(name='test_file_filtering', level=Logger.DEBUG, 
						showDate = True, 
						showTime = True, 
						showName = False,
						showFunc = False)
		self._debug = self._logger.logger.debug
		self.log = self._logger.log
	
	def setup (self):
		self.log("BEGIN test")
		self.utils = Utils()
		self.utils.setTargetRoot ("/tmp/foo")
	
	def run (self):
		self.utils.test()
		self.testDirEntryClasses()
		
	def finish (self):
		self.log("END test (no errors)")
		
	def testDirEntryClasses (self): 
		file = File(explicitlyIncluded = True)
		directory = Directory(explicitlyIncluded = True)
		subsystem = Subsystem(explicitlyIncluded = True)
		view = View(explicitlyIncluded = True)
		fileLink = Link(target = File(), explicitlyIncluded = True, copyTarget = True)
		directoryLink = Link(target = Directory(), explicitlyIncluded = True, copyTarget = True)
		subsystemLink = Link(target = Subsystem(), explicitlyIncluded = True, copyTarget = True)
		viewLink = Link(target = View(), explicitlyIncluded = True, copyTarget = True)
		assert createDirEntry("/nif").__class__ ==  Directory
		assert createDirEntry("/nif/.cvspass").__class__ ==  File
		assert createDirEntry("/nif/nif").__class__ ==  Link
		assert createDirEntry("/nif/nif").target.__class__ ==  Directory
		assert createDirEntry("/nif/environment/setup.ss").__class__ ==  Subsystem
		assert createDirEntry("/nif/environment/setup.ss/latest.wrk").__class__ ==  View
		
if __name__ == '__main__':
	test=_Test()
	test.setup()	
	test.run()
	test.finish()
