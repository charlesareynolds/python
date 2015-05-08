#!/usr/bin/env python

''' PyMenu.py
General curses-based menu system. 
'''

import curses
import os
import sys
import time
from xml.dom import minidom

class MenuSystem (object):
    
    class UsageError (Exception): pass

    def __init__(self, display):   
        self.display = display
        self.XMLFileName = sys.argv[1]
        try:
            self.XMLDoc = minidom.parse(self.XMLFileName)
        except Exception, x:
            print (x)
            print ("Usage: %s [XML menu file]" % sys.argv[0])
            sys.exit(1)
            
    def run(self):
        try:
            self._runMenu()
        except Exception, x:
            self.display = None
            # Without this, the error message soesn't seem to come out at all:
            time.sleep (1)
            print (x)
     
    def _runMenu(self):
        ''' _runMenu
        Puts up menu and gets a selection. Then executes a command, goes to a 
        child or parent menu, or exits.  
        '''
        menuStack = self._initMenuStack ()
        done = False        
        while not done:
            # For a clean screen, a new MenuItems is needed even after _doExecute:
            menuItems = MenuItems(menuStack, self.display.Window)            
            item = menuItems.getSelection()                
            if item.action == MenuItem.SUBMENU:
                menuStack.append(item.menuElement)
            if item.action == MenuItem.PARENT_MENU:
                if len(menuStack)==1:
                    #This is the top menu.  Exit:
                    done=True
                else:
                    menuStack.pop()
            elif item.action == MenuItem.EXECUTE:
                menuItems.stopForCommand()
                self._doExecute(item.command)
                menuItems.restartAfterCommand()
                
    def _initMenuStack (self):
        ''' _initMenuStack
        Creates a menuStack and adds the root menu as the first menu.
        ''' 
        menuStack = []
        for node in self.XMLDoc.documentElement.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.tagName == "menu":
                    menuStack = [node]
        if menuStack == []:
            usageError = self.UsageError ("No root menu found in XML file " + self.XMLFileName)
            raise usageError
        return menuStack
                    
    def _doExecute(self, command):
        ''' _doExecute
        Turns off the menu display, runs a system command, and turns the menu display back on.
        '''
        self.display.stop()
        os.system(command)
        raw_input("\nPress Enter to return to menu\n")
        self.display.start()

class MenuItems (object):
#    _DEFAULT_COLORS = ["yellow", "red"]
#    _DEFAULT_COLORS = ["yellow", "blue"] 
    
    def __init__(self, menuStack, WindowClass):
        self.menuStack = menuStack
        self.lastItemNum = 0
        self.window = WindowClass(self._getColors())
        self._addHeader ()
        self._addUpItem ()
        self._addBody()
        self.running = True
        
    def _getColors (self):
        defaultColors = ["white", "black"]
        colors = defaultColors
        gotFG = False
        gotBG = False
        for menuElement in reversed(self.menuStack):
            if not gotFG:
                if menuElement.hasAttribute ("foreground"):
                    colors[0] = menuElement.getAttribute ("foreground")
                    gotFG = True
            if not gotBG:
                if menuElement.hasAttribute ("background"):
                    colors[1] = menuElement.getAttribute ("background")
                    gotBG = True
        return colors
    
    def _addHeader (self):
        self.window.addLineHeader(self._getBreadCrumbs())
        
    def _getBreadCrumbs (self):
        breadCrumbs = ""
        for menuElement in self.menuStack:
            breadCrumbs += menuElement.getAttribute("name") + " > "
        return breadCrumbs
    
    def _addUpItem (self):
        # Is this the top menu?
        if len(self.menuStack) == 1:
            upName = 'Quit'
        else:
            upName = 'Up to Previous level'
        self.items = [MenuItem().createParent
                      (selNum = self.lastItemNum, 
                       name   = upName)]
        self._addLine(self.lastItemNum, upName)
        
    def _addBody(self):
        for node in self.menuStack[-1].childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.tagName == "menu":
                    self._appendSubMenu(node.getAttribute("name") + " >", node)
                elif node.tagName == "shellCommand":
                    self._appendCommand(node.getAttribute("name"), 
                                        node.getAttribute("command"))
                    
    def _appendCommand (self, name, command):    
        self.lastItemNum += 1
        self.items.append(MenuItem().createCommand
                          (selNum  = self.lastItemNum, 
                           name    = name,
                           command = command))
        self._addLine(self.lastItemNum, name)

    def _appendSubMenu (self, name, menuElement):    
        self.lastItemNum += 1
        self.items.append(MenuItem().createSubMenu
                          (selNum      = self.lastItemNum, 
                           name        = name,
                           menuElement = menuElement))
        self._addLine(self.lastItemNum, name)
        
    def _addLine(self, selNum, name):
        line="%s : %s" %(selNum, name)
        self.window.addLineNormal(line)
        
    def getSelection(self):
        ''' getSelection
        Returns the menu item the user selects.  Saves the selection number 
        unless it's zero ("go up") and then uses that selection number as the 
        starting point next time this menu is used in this run.
        '''
        currentMenuElement = self.menuStack[-1]
        if currentMenuElement.hasAttribute("lastSelNo"):
            startingSelNum = currentMenuElement.getAttribute("lastSelNo")
        else:
            startingSelNum = 0
        selNum=self.window.getSelNum(startingSelNum)
        if selNum > 0:
            currentMenuElement.setAttribute("lastSelNo", selNum)
        return self.items[selNum]

    def stopForCommand(self):
        ''' stopForCommand 
        Stop the window before executing a commend.
        '''
        if self.running:
            self.running = False    
            self.window.stop()
        
    def restartAfterCommand(self):
        ''' restartAfterCommand 
        Restart the window after executing a commend.
        '''
        if not self.running:
            self.window.start()
            self.running = True    
        
class MenuItem (object):
    PARENT_MENU = 'p'
    EXECUTE = 'c'
    SUBMENU = 's'
    
    def createParent (self, selNum, name):
        self.selNum=selNum
        self.name=name
        self.action=self.PARENT_MENU
        return self
    
    def createSubMenu (self, selNum, name, menuElement):
        self.selNum=selNum
        self.name=name
        self.menuElement=menuElement 
        self.action=self.SUBMENU 
        return self
    
    def createCommand (self, selNum, name, command):
        self.selNum=selNum
        self.name=name
        self.command=command 
        self.action=self.EXECUTE 
        return self
    
class CursesDisplay (object):
    '''This Display class is implemented using curses.
    '''
    def __init__(self):
        curses.initscr()
        self.running = False
        self.start()
        
    def __del__(self):
        self.stop()
        # Moved endWin from __del__() to stop() to clean up screen after executing a command
#        curses.endwin()
        
    def start(self):
        '''Sets up curses settings at the beginning of the program and after 
        running a command in _doExecute().  raw_input() in _doExecute() gets an 
        EOFerror on main-frame-dev1 after the second call to curses.initscr, 
        so initscr is not called here.   
        '''
        if not self.running:
            curses.start_color()
            curses.noecho()
            curses.cbreak()
            try:
                # gets ERR on nif-controls-b490:
                curses.curs_set(0)
            except:
                pass
            self.running = True

    def stop(self):
        if self.running:
            self.running = False
            try:
                # gets ERR on nif-controls-b490:
                curses.curs_set(1)
            except:
                pass
            curses.nocbreak()
            curses.echo()
            # Moved endWin from __del__() to stop() to clean up screen after executing a command
            curses.endwin()

    class Window (object):
        ''' Window
        Displays menu selections in a window.
        Caches lines to determine window size before creating the window.  
        Interacts with the user to return a selection number. 0 is lowest.
        Curses-specific implementation
        '''
        _BORDER_B_SIZE = 1
        _BORDER_L_SIZE = 1
        _BORDER_R_SIZE = 1
        _BORDER_T_SIZE = 1
        _COLOR_MAP = {"black" : curses.COLOR_BLACK,
                      "blue" : curses.COLOR_BLUE,
                      "cyan" : curses.COLOR_CYAN,
                      "green" : curses.COLOR_GREEN,
                      "magenta" : curses.COLOR_MAGENTA,
                      "red" : curses.COLOR_RED,
                      "white" : curses.COLOR_WHITE,
                      "yellow" : curses.COLOR_YELLOW}
        _DEFAULT_STYLE = curses.A_BOLD
#        _DEFAULT_STYLE = curses.A_NORMAL
        _HEADER_OFFSET = 2
        _LEFT_MARGIN = 1
        _RIGHT_MARGIN = 1
        _HEADER_STYLE = _DEFAULT_STYLE
        _INITIAL_TOP_OFFSET = _BORDER_T_SIZE
        _INITIAL_LEFT_OFFSET = _BORDER_L_SIZE + _LEFT_MARGIN
        _NORMAL_STYLE = _DEFAULT_STYLE
        _SELECTION_STYLE = curses.A_REVERSE
        
        def __init__(self, colors):
            FGColor, BGColor = colors
#            curses.init_pair (1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
            curses.init_pair (1, self._COLOR_MAP[FGColor], self._COLOR_MAP[BGColor])
            self._HEADER_STYLE |= curses.color_pair(1)
            self._NORMAL_STYLE |= curses.color_pair(1)
            self._SELECTION_STYLE |= curses.color_pair(1)
            self.maxSelNum = -1
            self.height = 0
            self.width = 0
            self.lines = []
            self.running = False
                
        def __del__(self):
            self.stop()
            
        def start(self):
            ''' start
            Call this after the last line has been added, and after running a 
            command.
            '''
            if not self.running:
#                self.scr = curses.newwin(12, 50, 0, 0)
                self.scr = curses.newwin(self.height + self._BORDER_T_SIZE + self._BORDER_B_SIZE, 
                                         self.width + self._BORDER_L_SIZE + self._BORDER_R_SIZE 
                                         + self._LEFT_MARGIN + self._RIGHT_MARGIN, 
                                         0, 0)
                self.scr.keypad(1)
                self.scr.bkgd(" ", self._NORMAL_STYLE)
                self.scr.touchwin()
                self.running = True
            
        def stop(self):
            ''' stop
            Call this when shutting down the window, and before running a 
            command.
            '''
            if self.running:
                self.running = False
                self.scr.keypad(0)
                self.scr.bkgd(" ", self._DEFAULT_STYLE)
                self.scr.clear()
                self.scr.refresh()

        def _getChar (self):
            return self.scr.getch()
              
        def addLineNormal(self, line):
            self._addLine(line)
            self.maxSelNum += 1
    
        def addLineHeader(self, line):
#            colorNumber = 1
#            line += "Number: " + str(colorNumber) + " "
#            colorPair = curses.pair_content(colorNumber)
#            line += "Pair: " + str(colorPair) + " "
#            for color in colorPair:
#                line += "Color : " + str(curses.color_content(color)) + " "
            self._addLine(line)
            self._addLine(" ")

        def _addLine(self, line):
            ''' addLine
            Adds line to the window buffer and updates width and height.
            '''
            self.lines.append(line)
            self.height += 1
            if len(line) > self.width:
                self.width = len(line)
            
        def getSelNum(self, startingselNum):
            ''' getSelNum
            Interacts with the user to return a selection number between 0 and 
            maxSelNum (but not more than 9).  
            
            The following keys are enabled:
            
            Up         - moves the selection up one (wraps)
            Down       - moves the selection down one (wraps)
            PgUp, Home - moves the selection to the top
            PgDn, End  - moves the selection to the bottom
            Enter      - returns the current selection immediately
            0-9        - returns that selection immediately
            backspace  - goes to parent menu (returns selection 0) immediately
            
            Any other key just beeps.
            
            ''' 
            selNum = startingselNum
            self.start()
            self._writeLines()
            gotIt = False
            while not gotIt:
                self._highlightSelection(selNum)
                self.scr.refresh()
                ch = self._getChar()
                # Can't go before getChar because that seems to do a redraw and
                # unhighlight happens before the user can make a selection:
                self._unHighlightSelection(selNum)
                if ord('0') <= ch <= ord('9'):
                    # shortcut to numbered item
                    if int(chr(ch)) <= self.maxSelNum:
                        selNum = int(chr(ch))
                        gotIt = True
                    else:
                        curses.beep()
                # Curses documentation says curses.KEY_BACKSPACE is unreliable:
                elif ch == 8:
                    selNum = 0
                    gotIt = True
                # Curses documentation says curses.KEY_ENTER is unreliable.
                elif ch == ord('\n'): #enter key pressed
                    # Perform the currently selected action:
                    gotIt = True
                elif ch == curses.KEY_UP:
                    # Go up, wrap:
                    selNum -= 1
                    if selNum < 0: 
                        selNum = self.maxSelNum
                elif ch == curses.KEY_DOWN:
                    # Go down, wrap:
                    selNum += 1
                    if selNum > self.maxSelNum: 
                        selNum = 0
                elif ch == curses.KEY_HOME or ch == curses.KEY_PPAGE:
                    # Go to top:
                    selNum = 0
                elif ch == curses.KEY_END or ch == curses.KEY_NPAGE:
                    # Go to bottom:
                    selNum = self.maxSelNum            
                else:
                    # Illegal key.
                    curses.beep()                
            return selNum

        def _writeLines(self):
            ''' writeLines
            Writes all the lines to the curses window buffer and redraws the window.
            '''
            nextTopOffset = self._INITIAL_TOP_OFFSET
            nextLeftOffset = self._INITIAL_LEFT_OFFSET
            for line in self.lines:
                self.scr.addstr(nextTopOffset, nextLeftOffset, line)
                nextTopOffset += 1
            self._emphasizeHeader()
            self.scr.border()
#            self.scr.border("|", "|", "-", "-", "+", "+", "+", "+")
            self.scr.refresh()
            
        def _highlightSelection(self, selNum):
            self._setSelectionLineStyle(selNum, self._SELECTION_STYLE)
            
        def _unHighlightSelection(self, selNum):
            self._setSelectionLineStyle(selNum, self._NORMAL_STYLE)
            
        def _emphasizeHeader(self):
            self._setLineStyle(self._INITIAL_TOP_OFFSET, 
                              self._INITIAL_LEFT_OFFSET, 
                              self._HEADER_STYLE)
            
        def _setSelectionLineStyle(self, selNum, style):
            self._setLineStyle(selNum + self._INITIAL_TOP_OFFSET + self._HEADER_OFFSET, 
                              self._INITIAL_LEFT_OFFSET, 
                              style)
            
        def _setLineStyle(self, topOffset, leftOffset, style):
            self.scr.chgat(topOffset, leftOffset, self.width, style)
            
def announce(classs, method, instance):
    ''' announce
    Debug support method for printing what operation was called by what kind of object
    '''
    print ("Called " + classs.__name__ + "." + method.__name__ + 
           " with a " + instance.__class__.__name__)
        
def beep(count=1, interval=.25, delay=.5):
    ''' beep
    Debug support method for emitting different beeps when it isn't convenient 
    to print a "you are here" text message.
    '''
    for index in range (count):
        curses.beep()
        if index < count - 1:
            time.sleep(interval)
    time.sleep(delay)

if __name__ == '__main__':
    MenuSystem(CursesDisplay()).run()