'''
Created on May 14, 2010

@author: reynolds12
'''
from xml.dom.minidom import parse

class Parser(object):
    """This class manages parsing the deliverables XML.  The XML is assumed to
    be valid (match its DTD or XSD).  A non-validating XML parser is used.
    """

    class UsageError(Exception):
        """The user did something wrong.
        """
        pass

    class _XMLTags:
        """Holds constants useful for processing XML output.
        """
        DELIVERABLE = "Deliverable"
        NAME = "Name"
        PATH = "Path"
        PLATFORM = "Platform"
        PROJECT = "Project"
        RELEASE = "Release"
        
    def __init__(self):
        self.parsed = False
            
    def parse(self, input):
        try:
            self.XMLDoc = parse (input)
        except IOError:
            raise self.UsageError ("gen_Makefile_Ada.parser.Parser could not open file " 
                              + '"' + str(input) + '"')
        self.parsed = True
        self.projects = self.getProjects()

    def _getRelease(self):
        if not self.parsed:
            raise self.UsageError ("getRelease was called before calling parse")
        else:
            return self.XMLDoc.getElementsByTagName (self._XMLTags.RELEASE).item(0)

    def getProjects(self):
        release = self._getRelease()
        return release.getElementsByTagName (self._XMLTags.PROJECT)

    def getDeliverables(self, project):
        return project.getElementsByTagName (self._XMLTags.DELIVERABLE)

    def getPlatforms(self, deliverable):
        return deliverable.getElementsByTagName (self._XMLTags.PLATFORM)
        
    def getName(self, element):
        """ Gets a platform or deliverable name.
        """
        return element.attributes.get (self._XMLTags.NAME).value

    def getPath(self, project):
        return project.attributes.get (self._XMLTags.PATH).value

        