#!/usr/bin/env python
"""Runs unit tests on accurev_api.  Only works if you are logged into AccuRev.
"""
import os
import unittest

from  support.accurev_api import AccuRevCommand

class BaseTestCase(unittest.TestCase):
	
	def setUp(self):
		unittest.TestCase.setUp(self)
		self.arc=AccuRevCommand(
							debugOn=False, 
							effortOnly=False)
		self.wsDir="/nif/working/reynolds/nif-cm1/ICCS/ICCS_API_testing"
		self.badWsDir="/"
	
	def tearDown(self):
		self.arc=None
		unittest.TestCase.tearDown(self)
		
	def issueCommand(self, wsDir):
		Popen_Args = [self.arc._ClientProg, 	self.arc._Commands.Info]
		Results_Stream = self.arc.issueCommand(Popen_Args, wsDir)
		self.assertEquals (Results_Stream[0:6], "Shell:")
		# print (str (Results_Stream))
				
	def getInfo(self, wsDir):
		Info = self.arc.getInfo (wsDir)
		self.assert_ ("Shell" in Info)
		self.assert_ (self.arc._Keys.User in Info)
		self.assert_ ("Host" in Info)
		self.assert_ ("Domain" in Info)
		self.assert_ ("TZ" in Info)
		self.assert_ ("Server name" in Info)
		self.assert_ ("Port" in Info)
		self.assert_ ("ACCUREV_BIN" in Info)
		self.assert_ ("Client time" in Info)
		self.assert_ ("Server time" in Info)
		return Info

class TestCase1InWorkspace(BaseTestCase):
	
	def test01_issueCommand(self):
		"""Note: If this fails unexpectedly, confirm that self.wsDir is a Linux WS if this 
		is running on Linux, and a Solaris WS if running on Solaris.
		""" 
		self.issueCommand(self.wsDir)
	
	def test02_getInfo(self):
		Info = self.getInfo(self.wsDir)
		self.assert_ (self.arc._Keys.Depot in Info)
		self.assert_ (self.arc._Keys.Workspace in Info)
		self.assert_ (self.arc._Keys.Parent in Info)
		self.assert_ ("Top" in Info)
		
	def test03_getDepot(self):
		depot = self.arc.getDepot (self.wsDir)
		print ("Depot: " + depot)
		
	def test04_getWorkspace(self):
		workspace = self.arc.getWorkspace (self.wsDir)
		print ("Workspace: " + workspace)
		
	def test05_getStreams(self):
		depot = self.arc.getDepot (self.wsDir)
		streams = self.arc.getStreams (depot)
		print ("Streams: " + str(streams))
		# Puts out too much:
		#	print ("Streams: " + Streams.toxml())
		
	def test06_getAncestors(self):
		depot = self.arc.getDepot (self.wsDir)
		workspace = self.arc.getWorkspace (self.wsDir)
		Ancestors = self.arc.getAncestors (
										Depot=depot, 
										Stream_In=workspace)
		print ("Ancestors: " + str(Ancestors))
		
	def test07_getExcludes(self):
		excludes = self.arc.getExcludes (self.wsDir)
		print ("Excludes: " + str(excludes))
		
class TestCase2NotInWorkspace (BaseTestCase):
	
	def test1_issueCommand(self):
		self.failUnlessRaises(AccuRevCommand.Usage_Error, self.issueCommand, self.badWsDir)
	
	def test2_getInfo(self):
		self.failUnlessRaises(AccuRevCommand.Usage_Error, self.getInfo, self.badWsDir)
		
	def test3_getDepot(self):
		self.failUnlessRaises(AccuRevCommand.Usage_Error, self.arc.getDepot, self.badWsDir)
		
	def test4_getWorkspace(self):
		self.failUnlessRaises(AccuRevCommand.Usage_Error, self.arc.getWorkspace, self.badWsDir)
		
class TestCase3LongTests(BaseTestCase):
	"""These tests each take a while.
	"""
	def setUp(self):
		BaseTestCase.setUp(self)
	
	def test08_getExternalElements(self):
		externalFiles=self.arc.getExternalElements(self.wsDir)
		print ("externalFiles: " + externalFiles.toprettyxml())
		
	def test09_getMissingElements(self):
		missingFiles=self.arc.getMissingElements(self.wsDir)
		print ("missingFiles: " + missingFiles.toprettyxml())
		
	def test10_getModifiedElements(self):
		#This one takes a long while - like 5 min on a fully populated workspace.
		modifiedFiles=self.arc.getModifiedElements(self.wsDir)
		print ("modifiedFiles: " + modifiedFiles.toprettyxml())
		
class TestCase4StateChangers(BaseTestCase):
	"""These test cases can actually change the state of a workspace or stream.
	""" 
	
	def test05_excludeElement(self):
		print ("Exclude results: " + str(self.arc.excludeElement(
														wsDir=self.wsDir,
														element="/./src/idl/include")))
	
	def test10_update(self):		
		print ("Update results: " + str(self.arc.update(self.wsDir)))

	def test20_addAllExternalElements(self):		
		print ("Add results: " + str(self.arc.addAllExternalElements(
															wsDir=self.wsDir, 
															comment="Testing Python AccuRev API",
															honorIgnore=True)))

	def test30_keepAllModifiedElements(self):		
		#This can be very slow - 5 min plus - with timestamp optimization off		
		print ("Keep results: " + str(self.arc.keepAllModifiedElements(
															wsDir=self.wsDir, 
															comment="Testing Python AccuRev API",
															ignoreTimestampOptimization=True)))

	def test40_defunctAllMissingElements(self):		
		print ("Defunct results: " + str(self.arc.defunctAllMissingElements(
															wsDir=self.wsDir, 
															comment="Testing Python AccuRev API")))

	def test50_promoteAllActiveElements(self):		
		print ("Promote results: " + str(self.arc.promoteAllActiveElements(
															wsDir=self.wsDir, 
															comment="Testing Python AccuRev API")))
		
class TestCase5Utilities(BaseTestCase):
			
	def testCase10_removeDirChildren(self):
		self.assert_(self.arc._removeDirChildren(["./rational/config/flexlm.dat","./rational"]) == 
					["./rational"])
		
if __name__ == '__main__':
	unittest.main()
	