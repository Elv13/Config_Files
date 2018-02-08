#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
from page import Page

class Box(Page):
    def __init__(self):
        Page.__init__(self)

    def repaint(self, clear = False):
        if self.win == None:
            return

        #self.win.erase()

        self.win.box()

        self.win.refresh()

