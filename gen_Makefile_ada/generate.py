#!/usr/bin/env python
from xml.dom.minidom import parse
import sys
def add(items, key, item):            
    if key in items:
        items[key] = items[key] + [item]
    else:
        items[key] = [item]
if __name__ == "__main__":
    XMLDoc = parse(sys.argv[1])
    outputFile = file(sys.argv[2], mode='w')
    platformRules = dict()
    executableRules = dict()
    for project in XMLDoc.getElementsByTagName("Release").item(0)\
    .getElementsByTagName("Project"):
        for deliverable in project.getElementsByTagName("Deliverable"):
            add(executableRules, project.attributes.get("Path").value, 
                                 deliverable.attributes.get("Name").value)
            for platform in deliverable.getElementsByTagName("Platform"):
                add(platformRules, platform.attributes.get("Name").value, 
                                   deliverable.attributes.get("Name").value)
    outputFile.write("#!!!WARNING!!! THIS FILE IS AUTO-GENERATED!!!\n")
    outputFile.write("\n")
    outputFile.write("# Define the rules for each platform.\n")
    for platform, deliverables in sorted(platformRules.iteritems()):
        outputFile.write(".PHONY: " + platform + "_for_release\n")
        ruleLine = platform + "_for_release :"
        for deliverable in sorted(deliverables):
            ruleLine = ruleLine + " " + deliverable
        outputFile.write(ruleLine + "\n")
    outputFile.write("\n")
    outputFile.write("# Define the rules for each executable.\n")
    for project, deliverables in sorted(executableRules.iteritems()):
        executableString = ""
        for deliverable in sorted(deliverables):
            executableString =  executableString + deliverable + " "
        outputFile.write(executableString + ": " + project + "\n")
        outputFile.write("\t@${LOGRULE}\n")
        outputFile.write("\t${GNATMAKE} -P$< ${GPRFLAGS} ${notdir ${basename $@}}\n")
        