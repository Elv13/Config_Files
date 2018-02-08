#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
import os
import sys
import re
from subprocess import call
from theme import theme
from page import Page

import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

# Yet another homebrew widget toolkit. I now have 11 of them!
# Seriously. This UX either have basic tables or fully custom views, so existing
# toolkits for ncurses would not really be helpful.


class Align:
    LEFT   = 0
    CENTER = 1
    RIGHT  = 2

class Element:
    """A single element in a list"""

    def __init__(self, columns, background = None, foreground = None):
        self.content = columns
        self.background = background
        self.foreground = foreground

    def getColumn(self, col):
        return self.content[col]

    def getColumnCount(self):
        return len(self.content)

    def getAttributes(self, selected):
        attr = theme.normal

        if self.background or self.foreground:
            attr = theme.getPair(self.foreground, self.background)

        if selected:
            attr = theme.selected

        return attr

    def applyAttributes(self, win, selected):
        win.attron(self.getAttributes(selected))

    def resetAttributes(self, win, selected):
        win.attroff(self.getAttributes(selected))


class ElementList:
    def __init__(self):
        self.elements     = []
        self.alignments   = {}
        self.columnWidth  = []
        self.sectionWidth = [0,0,0]

    def add(self, elem):
        self.elements.append(elem)

        # Update the cached column width
        for fieldIdx in range(0, elem.getColumnCount()):
            if not fieldIdx in self.alignments:
                self.alignments[fieldIdx] = Align.LEFT

            if len(self.columnWidth) < fieldIdx+1:
                self.columnWidth.append(0)

            align = self.alignments[fieldIdx]
            self.columnWidth [fieldIdx] = max( self.columnWidth [fieldIdx], len(elem.getColumn(fieldIdx)))
            self.sectionWidth[align   ] = max( self.sectionWidth[align   ], len(elem.getColumn(fieldIdx)))

    def count(self):
        return len(self.elements)

    def getElements(self):
        return self.elements

    def getSlice(self, start, count):
        return self.elements[start:start+count]

    def alignColumn(self, idx, alignment):
        self.alignments[idx] = alignment

class ElementViewSlice(Page):
    """An actual widget on the page"""

    def getOffset(self, column):
        return 0, 0

    def __init__(self, elems):
        Page.__init__(self)
        self.elem_list = elems
        self.selected = 5

    def printScrollbar(self, y, index):
        char = (u'▓' if index > 10 else u'░').encode('utf-8')
        self.win.addstr(y, self.width -1, char, theme.normal)

    def printLine(self, elem, y, index):
        y2, x2 = self.getOffset(0)
        loff, roff = 0, 0

        elem.applyAttributes(self.win, index == self.selected)

        # Make sure the whole line is always painted
        self.win.addstr(y, x2, ('').rjust(self.width-1))

        for i in range(0, elem.getColumnCount()):
            field = elem.getColumn(i)
            align = self.elem_list.alignments[i]
            colw  = self.elem_list.columnWidth[i]

            # Prevent fatal errors when the data isn't sanitized
            if x2+loff+len(field) >= self.width-1:
                field = field[0:self.width-x2+loff-1]

            if align == Align.LEFT or align == None:
                self.win.addstr(y, x2+loff, field)
                loff += colw + 1
            elif align == Align.CENTER:
                self.win.addstr(y, x2+self.elem_list.sectionWidth[0], field)
            elif align == Align.RIGHT:
                self.win.addstr(y, x2 + self.width - 1 - roff - colw, field)
                roff += colw + 1

        elem.resetAttributes(self.win, index == self.selected)

        self.printScrollbar(y, index)

    def repaint(self, clear = False):
        if self.win == None:
            return

        # Draw the header
        #header = "["+str(self.selected)+"/"+str(self.elem_list.count())+"]"
        #self.win.addstr(0, self.width - len(header) - 2, header)

        # Draw the columns
        #loff, roff = 0, 0
        #for i in range(0, len(self.elem_list.columnWidth)):
            #width = self.elem_list.columnWidth[i]
            #align = self.elem_list.alignments[i]

            #if align == Align.LEFT or align == None:
                #self.win.vline(1, int(loff + width*i), curses.ACS_VLINE, self.height-2)
                #loff += width
            #elif align == Align.RIGHT:
                #self.win.vline(1, self.width - int(roff + width*i), curses.ACS_VLINE, self.height-2)
                #roff += width

        count = 0
        y2, x2 = self.getOffset(0)
        for elem in self.elem_list.getSlice(self.position, self.height-1):
            self.printLine(elem, count+y2, self.position+count)
            count += 1

        self.win.refresh()

    def selectPrevious(self):
        if self.selected == 0:
            return

        self.selected -= 1

        if self.selected < self.position:
            self.position -= 1
            self.repaint(True)
        else:
            self.repaint()

    def selectNext(self):
        if self.selected == self.elem_list.count() - 1:
            return

        self.selected += 1

        if self.selected > self.position+self.height - 3:
            self.position += 1
            self.repaint(True)
        else:
            self.repaint()
