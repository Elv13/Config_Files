#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
import json
from page import Page

class Pager(Page):
    def __init__(self):
        Page.__init__(self)
        self._current_line = 0
        self._tail = False
        self._content = ""
        with open("/tmp/clazy.json", 'r') as f:
            self._parse_lines(f.read())
            f.close()

    def _parse_lines(self, s):
        self._content = s.split("\n")

    def page_up(self):
        self._current_line -= self.height-2
        self._current_line = max(0, self._current_line)
        self.repaint()

    def page_down(self):
        self._current_line += self.height-2
        if self._current_line + self.height-2 > len(self._content):
            self._current_line = len(self._content) -  self.height - 2
        self.repaint()

    def repaint(self, clear = False):
        if self.win == None:
            return

        self.win.erase()

        self.win.box()

        for i in range(1, self.height - 2):
            self.win.addstr(i, 1, self._content[self._current_line+i][0:self.width-2])

        self.win.refresh()

