"""Provides access to AccuRev.
"""
# import inspect
from optparse import OptionParser
import string
from support.local_logging import Logger
from support.runner import Runner
from xml.dom.minidom import parseString

class AccuRevCommand:
	"""Provides AccuRev commands"""
    
	# Client-caused exceptions:
	class Usage_Error (Exception): pass
	
	# Internal constants:
	_ClientProg = "accurev"
	
	class _ObjectTypes:
		"""Holds constants that name AccuRev Object types
		"""
		Streams = "streams"

	class _Commands:
		"""Holds constants that name commands.
		"""
		Add = "add"
		Defunct = "defunct"
		Exclude = "excl"
		Info = "info"
		Keep = "keep"
		ListRules = "lsrules"
		Promote = "promote"
		Show = "show"
		Stat = "stat"
		Update = "update"
		
	class Elements:
		"""Holds lists of elements that were added or defuncted.
		"""
		AddedElements = []
		DefunctedElements = []
            	
	class _Options:
		"""Holds constants that name options for commands
		"""
		AllFiles = "-a"
		AllExternalElements = "-x"
		AllMissingElements = "-M"
		AllModifiedElements = "-m"
		Comment = "-c"
		DefaultGroup = "-d"
		Depot = "-p"
		IgnoreIgnore = "-fi"
		NoTimestampOptimization = "-O"
		WorkspaceRulesOnly = "-d"
		XMLFormat = "-fx"

	class _ErrorStrings:
		"""Holds strings that indicate an error condition when found in AccuRev 
		output.
		"""
		NotAuthenticated = "Not authenticated"
		NotInWorkspace = "You are not in a directory associated with a workspace"
		NotLoggedIn = "(not logged in)"
		
	class _Keys:
		"""Holds strings used in parsing a dictionary created from non-XML output
		"""
		Depot = "Depot"
		# This value is only seen on the "Principal:" line output from the "info" command:
		Parent = "Basis"
		User = "Principal"
		Workspace = "Workspace/ref"

	class _XMLTags:
		"""Holds constants useful for processing XML output. 
		"""
		Basis = "basis"
		Basis_Number = "basisStreamNumber"
		Element = "element"
		Kind = "kind"
		Location = "location"
		Name = "name"
		Root_Basis = "root"
		Stream = "stream"
		Stream_Number = "streamNumber"
		
	class _XMLValues:
		"""Holds constants useful for processing XML output. 
		"""
		Excluded = "excl"
		
	#
	# Common command args
	#
	# accurev stat -a -fx
	_XMLStatArgs = [
			_ClientProg, 
			_Commands.Stat, 
			_Options.AllFiles, 
			_Options.XMLFormat]
    
	def __init__(self, debugOn, effortOnly):
		"""Initializes the instance variables associated with the class
		"""
		self._debugOn = debugOn
		self._effortOnly = effortOnly
		self._logger=Logger(name="AccuRevCommand")
		self._logger.set_debug (self._debugOn)
		self._debug = self._logger.logger.debug
		self._log = self._logger.logger.info
		self._runner=Runner()
    
	def issueCommandReturnXML (self, popenArgsList, wsDir=None):
		"""Issues the command and provides the results as XML.
		"""
		output = self.issueCommand(popenArgsList, wsDir)
		XML_Result = parseString (output)
		self._debug (`XML_Result`)
		return XML_Result

	def issueCommand (self, popenArgsList, wsDir=None):
		"""Issue the command associated with the given Popen arguments list.
		    Returns the results of the command in a (output, errors) tuple and does
		    some AccuRev-specific error checking. 
		"""
		self.dumpPopenArgs(popenArgsList[1], popenArgsList)
		(output, errors) = self._runner.popenOrLog (popenArgsList, wsDir)
		self._debug ("output: " + str (output))
		self._debug ("errors: " + str (errors))
		if (self._ErrorStrings.NotAuthenticated in errors or self._ErrorStrings.NotLoggedIn in output):
			raise self.Usage_Error ("Not logged in to AccuRev.")
		if self._ErrorStrings.NotInWorkspace in errors:
			raise self.Usage_Error (`wsDir` + " is not in a workspace.")
		return output

	def dumpPopenArgs(self, commandName, popenArgsList):
		"""Dumps the contents of the given Popen arguments list.
		"""
		self._debug('Arg list for command "' + commandName + '"')
		self._debug("-----------------------------------------------------------")
		for popenArg in popenArgsList:
			for arg in popenArg.split(","):
				self._debug(arg)
		self._debug("-----------------------------------------------------------")

	def getInfo (self, wsDir):
		"""Runs the AccuRev 'info' command on wsDir and returns a dictionary 
		containing the results.
		"""
		self._debug ("getInfo (wsDir = " + `wsDir`)
		Popen_Args = [self._ClientProg, self._Commands.Info]		
		info = self.parseInfo (self.issueCommand(Popen_Args, wsDir))
		self.assertLoggedInInfo(info)
		return info
	    
	def parseInfo(self, Info):
		"""Take the "Field_Name:\t\tfield" lines in the info command output and
		change them into a dictionary.  The info command is one of the few that 
		doesn't have an xml output option.   
		"""
		Info_Lines = Info.splitlines()
		Info_Dict = dict()
		for Line in Info_Lines:
			#self._debug(`string.split(Line, "\t")`)
			Key, Dummy1, Dummy2 = Line.partition(":")
			Key = Key.strip ()
			Dummy1, Dummy2 ,Value = Line.rpartition("\t")
			self._debug("Key=" + `Key`)
			self._debug("Value=" + `Value`)
			Info_Dict[Key] = Value
		return Info_Dict        

	def update (self, wsDir):
		"""Runs the AccuRev 'update' command on the workspace containing wsDir.  
		Returns the output from the command.  Raises Usage_Error if not in a 
		Workspace.
		"""
		self._debug ("update (wsDir = " + `wsDir`)
		# "accurev info:
		Popen_Args = [self._ClientProg, self._Commands.Update]
		return  self.issueCommand(Popen_Args, wsDir)
    
	def assertLoggedInInfo (self, info):
		if info[self._Keys.User] == self._ErrorStrings.NotLoggedIn:
			raise self.Usage_Error ("Not logged in to AccuRev.")

	def getDepot (self, wsDir):
		"""Returns the depot containing the workspace/stream of directory wsDir.
		"""
		info = self.getInfo (wsDir)
		self.assertLoggedInInfo (info)
		return info [self._Keys.Depot]
	
	def getWorkspace (self, wsDir):
		"""Returns the workspace/stream of directory wsDir.
		"""
		info = self.getInfo (wsDir)
		self.assertLoggedInInfo (info)
		return info [self._Keys.Workspace]
        
	def getStreams (self, Depot):
		"""Get the info for all streams in Depot and return it as an XML object.
		"""
		self._debug ("getStreams (Depot = " + `Depot`)
		# "accurev show -fx -p <depot> streams":
		Popen_Args = [
					self._ClientProg, 
					self._Commands.Show, 
					self._Options.XMLFormat,
					self._Options.Depot, Depot,
					self._ObjectTypes.Streams]
		return self.issueCommandReturnXML(Popen_Args)   

	def getAncestors (self, Depot, Stream_In):
		"""Returns a list of the ancestors of Stream_In, with Stream_In 
		first on the list.  
		"""
		self._debug ("getParent (Depot = " + Depot + ", Stream_In = " + Stream_In)
		Stream_XML_Doc = self.getStreams (Depot)
		Streams = Stream_XML_Doc.getElementsByTagName (self._XMLTags.Stream)
		# Get the basis and number for every stream:
            # Snapshot views are frozen forever.  A snapshot's basis stream
            # name may have changed since the snapshot was taken, but not 
            # the basis stream number.  Therefore, we track ancestors by 
            # number, not name.
		Stream_Basis_Map = dict ()
		Number_Stream_Map = dict ()
		Stream_In_Found = False
		for Stream in Streams:
			self._debug ("----")
			Name = Stream.attributes.get (self._XMLTags.Name).value
			Number = Stream.attributes.get (self._XMLTags.Stream_Number).value
			self._debug ("Stream: " + Name + "(" +  Number + ")")
			Number_Stream_Map [Number] = Name
			# The root stream has no basis:
			if Stream.attributes.has_key (self._XMLTags.Basis):
				Basis_Name = Stream.attributes.get (self._XMLTags.Basis).value
				Basis_Number = Stream.attributes.get (self._XMLTags.Basis_Number).value
				self._debug ("Basis: " + Basis_Name + "(" +  Basis_Number + ")")
				Stream_Basis_Map [Number] = Basis_Number
			if Name == Stream_In:
				Stream_In_Found = True
				Stream_In_Number = Number
		if not Stream_In_Found:
			raise self.Usage_Error ("Stream '" + Stream_In + "' not found.")
		# Make an ancestor name map:
		Ancestors = []
		Ancestor_Number = Stream_In_Number
		while Stream_Basis_Map.has_key (Ancestor_Number):
			Ancestor_Number = Stream_Basis_Map [Ancestor_Number]
			Ancestor = Number_Stream_Map [Ancestor_Number]
			self._debug (Ancestor)
			Ancestors.append (Ancestor)
		return (Ancestors)
	
	def getExternalElements(self, wsDir):
		"""Returns all the external elements  in the workspace.  Does not honor 
		ACCUREV_IGNORE_ELEMS.
		"""
		# accurev stat -a -fx -x
		return self.issueCommandReturnXML(
								self._XMLStatArgs + [self._Options.AllExternalElements], 
								wsDir)   
	
	def getMissingElements(self, wsDir):
		"""Returns all the missing elements in the workspace.
		"""
		# accurev stat -a -fx -M
		return self.issueCommandReturnXML(
								self._XMLStatArgs + [self._Options.AllMissingElements], 
								wsDir)   
	
	def getModifiedElements(self, wsDir):
		"""Returns all the modified elements in the workspace.
		"""
		# accurev stat -a -fx -m -O
		return self.issueCommandReturnXML(
								self._XMLStatArgs + [self._Options.AllModifiedElements, 
												self._Options.NoTimestampOptimization], 
								wsDir)
	def getExcludes(self, wsDir):
		"""Returns a list of all the excludes explicitly set on this workspace.
		"""
		# accurev lsrules -d -fx
		rulesXML = self.issueCommandReturnXML(
										[self._ClientProg, 
										self._Commands.ListRules,
										self._Options.WorkspaceRulesOnly,
										self._Options.XMLFormat],
										wsDir)
		rules = rulesXML.getElementsByTagName (self._XMLTags.Element)
		excludes = []
		for rule in rules:
			if rule.attributes.get (self._XMLTags.Kind).value == self._XMLValues.Excluded:
				excludes = excludes + [rule.attributes.get (self._XMLTags.Location).value]
		return excludes
		
	################################################
	# State changing operations
	################################################
	
	def addAllExternalElements(self, wsDir, comment, honorIgnore):
		"""Adds all the external elements in the workspace.  honorIgnore (boolean)
		controls whether this command honors ACCUREV_IGNORE_ELEMS.
		"""
		externalElementsXML=self.getExternalElements(wsDir)
		externalElements=self._extractElements(externalElementsXML)
		newElements=self._removeDirChildren(externalElements)		
		# accurev add -c <comment> -x
 		popenArgs=[self._ClientProg,
							self._Commands.Add,
							self._Options.Comment,
							comment,
							self._Options.AllExternalElements]
		if not honorIgnore:
			# accurev add -c <comment> -x -fi
 			popenArgs=popenArgs + [self._Options.IgnoreIgnore]
 		self.Elements.AddedElements.extend(newElements)
		return self.issueCommand(popenArgs, wsDir)
	
	def keepAllModifiedElements(self, wsDir, comment, ignoreTimestampOptimization):
		"""Keeps all modified elements in the workspace.  When 
		IgnoreTimestampOptimization is True, does not check files older than the 
		last update time for changes.
		"""
		# accurev keep -c <comment> -m
 		popenArgs=[self._ClientProg,
							self._Commands.Keep,
							self._Options.Comment,
							comment,
							self._Options.AllModifiedElements]
 		if  ignoreTimestampOptimization:
 			# accurev keep -c <comment> -m -O
 			popenArgs=popenArgs + [self._Options.NoTimestampOptimization]
		return self.issueCommand(popenArgs, wsDir)
	
	def defunctAllMissingElements(self, wsDir, comment):
		"""Defuncts all missing elements in the workspace.
		"""
		missingElementsXML=self.getMissingElements(wsDir)
		missingElements=self._extractElements(missingElementsXML)
		defunctableElements=self._removeDirChildren(missingElements)
		#accurev defunct -c <comment> <element list>
 		popenArgs=[self._ClientProg,
							self._Commands.Defunct,
							self._Options.Comment,
							comment] + defunctableElements
		# Save the list of defuncted elements
		self.Elements.DefunctedElements.extend(defunctableElements)
		return self.issueCommand(popenArgs, wsDir)
	
	def _extractElements (self, XMLElements):
		"""Given an XML doc of elements, returns the "/./" named element names.
		"""
		elements = XMLElements.getElementsByTagName (self._XMLTags.Element)
		elementNames = []
		for element in elements:
			elementNames = elementNames + [element.attributes.get (self._XMLTags.Location).value]
		return elementNames
	
	def _removeDirChildren(self, elements):
		"""Given a list of elements, returns that list minus children of directories.
		If you defunct a directory AND a child of that directory, the child becomes
		a stranded defunct member of the workspace. 
		"""
		withoutDirChildren = []
		for possibleChild in elements:
			isChild = False
			for possibleDir in elements:
				if self._isInDir(possibleChild, possibleDir):
					isChild = True
			if not isChild:
				withoutDirChildren = withoutDirChildren + [possibleChild]
		return withoutDirChildren
	
	def _isInDir (self, possibleChild, possibleDir):
		"""Returns True if possibleChild is in the directory PossibleDir
		"""
		# "in" is safe to use here because all element names begin with "./":		
		return (possibleDir + "/") in possibleChild
			
	def promoteAllActiveElements(self,wsDir, comment):
		"""Promotes all elements in the Default Group to the parent stream.
		"""
		#accurev promote -c <comment> -d
 		popenArgs=[self._ClientProg,
							self._Commands.Promote,
							self._Options.Comment,
							comment,
							self._Options.DefaultGroup]
		return self.issueCommand(popenArgs, wsDir)

	def excludeElement(self, wsDir, element):
		"""Excludes element from the workspace at wsDir
		"""
		excludes = self.getExcludes (wsDir)
		if element in excludes:
			return 'Element "' + element + '" already excluded.  No excluded needed.'
		else:
			#accurev excl <element>
			return self.issueCommand(
									[self._ClientProg,
									self._Commands.Exclude,
									element], 
									wsDir)
		