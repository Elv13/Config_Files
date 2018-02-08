#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
import os
from theme import theme

class Session:
    """An application page"""

    def __init__(self):
        self.slices = []
        self.xpos   = []
        self.wins   = []
        self.height = 0
        self.width  = 0
        self.stdscr = None
        self.keys   = {}
        self._keygrabber = None

    def repaint(self):
        if self.stdscr == None:
            return

        for slice in self.slices:
            slice.repaint()

    def reflow(self):
        if self.stdscr == None:
            return

        rows_, columns_ = os.popen('stty size', 'r').read().split()
        self.height, self.width = int(rows_), int(columns_)
        self.repaint()

    def resize_pages(self):
        assert(self.height > 0)
        assert(self.width > 0)

        minimal_size = 0
        expand_count = 0

        for page in self.slices:
            if page.expand:
                expand_count += 1
            else:
                minimal_size += page.height

        offset = 0
        for page in self.slices:
            size = page.height

            if page.expand:
                size = (self.height-minimal_size)/expand_count

            page.resize(size , self.width)
            page.move(0, offset)
            offset += size

    def addPage(self, page):
        self.slices.append(page)

        if self.stdscr == None:
            return

        self.resize_pages()

    def display(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()
        global theme
        theme.init()

        self.reflow()

        self.resize_pages()

        for page in self.slices:
            page.display(self)

        self.evenLoop()

    def add_key(self, key, callback, name = None, color = None):
        self.keys[ord(key)] = {
            "key"     : key,
            "callback": callback,
            "name"    : name,
            "color"   : color,
        }

    def close(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def set_key_grabber(self, page):
        self._keygrabber = page
        assert(self._keygrabber)

    def evenLoop(self):
        self.stdscr.refresh()
        self.repaint()

        #while 1:
            #self.stdscr.move(self.height-1,self.width-1)
            #c = self.stdscr.getch()

            #if c == ord('q') or c == ord('Q'):
                #break
            #elif c == curses.KEY_UP or c == ord('k'):
                #self.slices[0].selectPrevious()
            #elif c == curses.KEY_DOWN or c == ord('j'):
                #self.slices[0].selectNext()

        while 1:
            self.stdscr.move(self.height-1,self.width-1)
            c = self.stdscr.getch()

            if self._keygrabber:
                if self._keygrabber.key_event(c):
                    continue

            if c == ord('q') or c == ord('Q'):
                break
            elif c in self.keys:
                self.keys[c]["callback"]()

