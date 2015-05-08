'''
Created on May 14, 2010

@author: reynolds12
'''
import unittest

from parser import Parser
from testing_support import TS

class TestParser(unittest.TestCase):

    badXMLFileName = "bogus_XML_file_name.xml"
    expectedDeliverable= "sample_fep_main"
    expectedPlatform= "ppc-vxworks"
    expectedProjectPath = "Main_Programs/Sample_FEP/Sample_FEP.gpr"
    
    def getExpectedProject(self):
        for project in self.parser.getProjects():
            if self.parser.getPath (project) == self.expectedProjectPath:
                return project
        return None

    def getExpectedDeliverable(self):
        project = self.getExpectedProject()
        if project != None:
            for deliverable in self.parser.getDeliverables (project):
                if self.parser.getName (deliverable) == self.expectedDeliverable:
                    return deliverable
        return None

    def getExpectedPlatform(self):
        deliverable = self.getExpectedDeliverable()
        if deliverable != None:
            for platform in self.parser.getPlatforms (deliverable):
                if self.parser.getName (platform) == self.expectedPlatform:
                    return platform
        return None

    def setUp(self):
        self.parser = Parser()
        self.parser.parse(file(TS.XMLFileName))

    def tearDown(self):
        self.parser = None

    def test01_parseFile(self):
        pass

    def test011_parseFileName(self):
        self.parser.parse(TS.XMLFileName)

    def test012_parseBadFileName(self):
        self.assertRaises(Parser.UsageError, self.parser.parse, self.badXMLFileName)

    def test02_getRelease(self):
        self.assertNotEqual(self.parser._getRelease(), None)

    def test03_getProjects(self):
        self.assertNotEqual(self.parser.getProjects(), None)
        self.assertEquals (self.parser.getProjects()._get_length(), 2)

    def test04_expectedProjectPath(self):
        self.assertNotEqual (self.getExpectedProject(), None)
                
    def test05_expectedDeliverableName(self):
        self.assertNotEqual (self.getExpectedDeliverable(), None)
                
    def test06_expectedPlatformName(self):
        self.assertNotEqual (self.getExpectedPlatform(), None)
        
    def test07_getBeforeParse(self):
        self.parser = Parser()
        self.assertRaises(Parser.UsageError, self.parser._getRelease)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()