#!/usr/bin/env python
################################################################################
#
#	FILENAME:	pseudo.py
#
#	PURPOSE:	This utility will allocate a master/slave pseudo tty
#			pair of devices.  This utility will fork a child process
#			and that child will continually monitor the STDIN and
#			STDOUT file descriptors fo the master side of the pseudo
#			tty for a given string pattern.  If the given string
#			pattern (if any) is found then a response pattern
#			(if any) will be sent to the STDIN of the master side
#			of the pseudo tty.
#			The slave side of the pseudo tty will be connected to
#			the STDIN of the command to be issued.
#			The STDOUT and STDERR file descriptors of the command
#			will be directed to the STDOUT and STDERR of the 
#			parent (this may be a login shell's pty or it may be
#			a log file).
#			If the users command relies on something coming from
#			STDIN then the child process is supplying a dummy
#			newline, hopefully responding to any question that the
#			users command may be asking.
#			The child process is terminated once the users command
#			terminates.
#
#	ARGUMENTS:	pseudo.py [<options>] -- arg0 arg1 ... argN
#
#				where <options> can be:
#
#					[-debug]
#					[-dumpProgOutput]
#					[-if_you_see_this <seeThis>]
#					[-send_this <sendThis>]
#					[-terminateIt]
#
#				and where arg0 is the name of the users program
#							to be executed
#				      and arg1 ... argN are the command line
#						arguments that are to be 
#						provided to the users program
#
#			NOTE: The double dash '--' is REQUIRED!
#
#	HISTORY:
#
# 2011/01/06	RJS	IC-32676 Need platform-independent utilities for SysMgr
#
################################################################################

import getopt
import os
import pty
import signal
import sys
import time

########################################
#
#	GLOBAL VARIABLES
#
debug = False
dumpProgOutput = False
ifYouSeeThis = ""
sendThis = ""
terminateIt = False

########################################
#
#	ROUTINE:	displayMsg()
#
def displayMsg(msg):
    if (debug == True):
	print("pseudo: %s" % msg)

########################################
#
#	ROUTINE:	displayMsg1()
#
def displayMsg1(msg):
    if (debug == True):
	print("    pty monitor: %s" % msg)

########################################
#
#	ROUTINE:	displayMsg2()
#
def displayMsg2(msg):
    if (debug == True):
	print("        user application: %s" % msg)

#
########################################

########################################
#
#	ROUTINE:	firstChild()
#
def firstChild(masterFd, slaveFd, ifYouSeeThis, sendThis, terminateIt):

    global dumpProgOutput
    displayMsg1("Inside firstChild()!")

    # close slave side of pseudo tty
    # it is not needed by the first child process
    #
    displayMsg1("closing Slave side of PTY (%d)" % slaveFd)
    os.close(slaveFd)

    displayMsg1("reading from masterFd [%d] waiting for data ..." % masterFd)
    while 1:
	buffer = os.read(masterFd, 1024)
	displayMsg1("buffer = [%s]" % buffer)
	if (dumpProgOutput):
	    sys.stdout.write(buffer)
	if (ifYouSeeThis != ""):
	    if (buffer.find(ifYouSeeThis) != -1):
		displayMsg1("found string [%s] in buffer [%s]" % (ifYouSeeThis, buffer))
		if (terminateIt == True):
		    displayMsg1("terminating because you said so")
		    os._exit(0)
		if (sendThis != ""):
		    displayMsg1("should send this [%s]" % (sendThis))

    os._exit(6)

#
########################################

########################################
#
#	ROUTINE:	closeAndDup()
#
def closeAndDup(fd1, fd2):

    # close fd1
    # dup fd2 to fd1
    #
    os.close(fd1)
    os.dup(fd2)

#
########################################

########################################
#
#	ROUTINE:	secondChild()
#
def secondChild(masterFd, slaveFd, clArgs):

    displayMsg2("Inside secondChild()!")

    # close master side of pseudo tty
    # it is not needed by the second child process
    #
    displayMsg2("closing Master side of PTY (%d)" % masterFd)
    os.close(masterFd)

    # close STDIN, STDOUT and STDERR
    # dup the Slave Fd to these Fds
    #
    closeAndDup(0, slaveFd)
    closeAndDup(1, slaveFd)
    closeAndDup(2, slaveFd)

    displayMsg2("starting users application [%s] now ..." % clArgs[0])
    os.execvp(clArgs[0], clArgs[0:])
    displayMsg2("successfully execed!")
    os._exit(5)

#
########################################

########################################
#
#	ROUTINE:	waitForChildren()
#
def waitForChildren(cpid1, cpid2):

    displayMsg("Inside waitForChildren()!")

    cpid1Terminated = 0
    cpid2Terminated = 0

    while (cpid1Terminated == 0) or (cpid2Terminated == 0):
	displayMsg("Waiting for [%d] or [%d] to terminate ..." % (cpid1, cpid2))

	(pid, status) = os.wait()

	if (pid == cpid1):
	    displayMsg("First Child Process [%d] terminated with status [%d]" %
					    (pid, status/256))
	    if (cpid2Terminated == 0):
		displayMsg("Terminating Second Child Process [%d] now ..." % cpid2)
		os.kill(cpid2, signal.SIGTERM)
	    else:
		displayMsg("Second Child process [%d] already terminated!" % cpid2)
	    cpid1Terminated = 1
	elif (pid == cpid2):
	    displayMsg("Second Child Process [%d] terminated with status [%d]" %
					    (pid, status/256))
	    if (cpid1Terminated == 0):
		displayMsg("Terminating First Child Process [%d] now ..." % cpid1)
		os.kill(cpid1, signal.SIGTERM)
	    else:
		displayMsg("First Child process [%d] already terminated!" % cpid1)
	    cpid2Terminated = 1
    displayMsg("Both child processes terminated!")
    os._exit(4)

#
########################################

########################################
#
#	ROUTINE:	usage()
#
def usage():

    print("")
    print("Usage: %s [<options>] -- arg0 arg1 ... argN" % sys.argv[0])
    print("")
    print("       where: <options> can be:")
    print("              [-debug]")
    print("              [-dumpProgOutput]")
    print("              [-if_you_see_this <seeThis>]")
    print("              [-send_this <sendThis>]")
    print("              [-terminateIt]")
    print("")
    print("       and where arg0 is the name of the program to be executed")
    print("             and arg1 ... argN are the command line arguments")
    print("                          that are to be provided to the program!")
    print("")
    print("       NOTE:  The double dash '--' is REQUIRED!")
    print("")
    os._exit(0)

#
########################################

########################################
#
#	ROUTINE:	createArgList()
#
def createArgList(argv):

    global debug, dumpProgOutput, ifYouSeeThis, sendThis, terminateIt

    argList = []
    storeIt = False

    for i in range(1, len(sys.argv[1:])+1):
	if (storeIt == True):
	    argList.append(sys.argv[i])
	else:
	    if (sys.argv[i] == '-debug'):
		debug = True
	    elif (sys.argv[i] == '-dumpProgOutput'):
		dumpProgOutput = True
	    elif (sys.argv[i] == '-if_you_see_this'):
		ifYouSeeThis = sys.argv[i+1]
	    elif (sys.argv[i] == '-send_this'):
		sendThis = sys.argv[i+1]
	    elif (sys.argv[i] == '-terminateIt'):
		terminateIt = True
	    elif (sys.argv[i] == '-?'):
		usage()
	    elif (sys.argv[i] == '--'):
		storeIt = True

    if (debug == True and dumpProgOutput == True):
	dumpProgOutput = False

    return argList

#
########################################

########################################
#
#	ROUTINE:	main
#
def main(argv):

    argList = createArgList(argv)
    displayMsg("if you see this [%s] send this [%s] or terminateIt [%s]" % 
    				(ifYouSeeThis, sendThis, terminateIt))
    if (len(argList) <= 0):
	print("You must supply a command and options!")
	os._exit(9)

    displayMsg("my pid = [%d]" % os.getpid())

    (masterFd, slaveFd) = pty.openpty()
    displayMsg("masterFD = [%d] slaveFd = [%d]" % (masterFd, slaveFd))

    displayMsg("Starting First Child ...")
    cpid1 = os.fork()
    if (cpid1 == 0):
	displayMsg1("First Child process, my pid = [%d]" % os.getpid())
	firstChild(masterFd, slaveFd, ifYouSeeThis, sendThis, terminateIt)
	os._exit(1)
    elif (cpid1 < 0):
	displayMsg("failed to fork, pid = [%d]" % cpid1)
	os._exit(2)

    displayMsg("Starting Second Child ...")
    cpid2 = os.fork()
    if (cpid2 == 0):
	displayMsg2("Second Child process, my pid = [%d]" % os.getpid())
	secondChild(masterFd, slaveFd, argList)
	os._exit(3)
    elif (cpid2 < 0):
	displayMsg("failed to fork, pid = [%d]" % cpid2)
	os._exit(4)

    displayMsg("Waiting for children to terminate ...")
    waitForChildren(cpid1, cpid2)

#
########################################

########################################
#
#	ROUTINE:	main
#
if __name__ == '__main__':
    main(sys.argv[1:])

