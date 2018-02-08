#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
import curses.textpad
from page import Page

class Editor(Page):
    def __init__(self):
        Page.__init__(self)
        self._lines = [""]
        self._cursor_y = 0
        self._cursor_x = 0
        self._textbox = None

    def display(self, sess):
        Page.display(self, sess)
        if self._textbox == None:
            self._textbox = curses.textpad.Textbox(self.win)
            curses.beep()

    def key_event(self, key):
        #self._lines[0] += "d"
        #self._cursor_x += 1
        #self.repaint()
        #self._textbox.do_command(key)
        self._textbox.edit()
        return False

    def repaint(self, clear = False):
        if self.win == None or self._textbox == None:
            return

        self.win.erase()

        #for i in range(0, len(self._lines)):
            #self.win.addstr(i+1, 1, self._lines[i][0:self.width-2])

        self.win.refresh()

