#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
import math
from theme import theme
from page import Page

class WarningPage(Page):
    def __init__(self):
        Page.__init__(self)
        self.full_width = True
        self._entry = None

    def set_entry(self, entry):
        self._entry = entry
        self.repaint()

    def repaint(self, clear = False):
        if self.win == None:
            return

        self.win.erase()

        # Draw the sides
        self.win.vline(0, 0, curses.ACS_VLINE, self.height)
        self.win.vline(0, self.width-1, curses.ACS_VLINE, self.height)

        if not self._entry:
            self.win.refresh()
            return

        # Draw the static box
        self.win.hline(1, 1, curses.ACS_HLINE, self.width-2)
        self.win.hline(3, 1, curses.ACS_HLINE, self.width-2)
        self.win.addch(1, 0, curses.ACS_LTEE)
        self.win.addch(3, 0, curses.ACS_LTEE)
        self.win.addch(1, self.width-1, curses.ACS_RTEE)
        self.win.addch(3, self.width-1, curses.ACS_RTEE)

        # Draw the dynamic parts of the box
        line_len = len(str(self._entry["line"]))+9
        self.win.addch(1, line_len, curses.ACS_TTEE )
        self.win.addch(2, line_len, curses.ACS_VLINE)
        self.win.addch(3, line_len, curses.ACS_BTEE )

        col_len = len(str(self._entry["columns"]))+8
        self.win.addch(1, line_len+col_len, curses.ACS_TTEE )
        self.win.addch(2, line_len+col_len, curses.ACS_VLINE)
        self.win.addch(3, line_len+col_len, curses.ACS_BTEE )

        warn_len = len(str(self._entry["warn"]))+4
        self.win.addch(1, self.width-warn_len, curses.ACS_TTEE )
        self.win.addch(2, self.width-warn_len, curses.ACS_VLINE)
        self.win.addch(3, self.width-warn_len, curses.ACS_BTEE )

        message_len = len(self._entry["message"]) + 12
        message_lines = int(math.ceil(float(message_len)/float(self.width-12)))
        yoffset = 4 + message_lines

        if self.height > yoffset:
            self.win.hline(yoffset, 1, curses.ACS_HLINE, self.width-2)
            self.win.addch(yoffset, 0, curses.ACS_LTEE)
            self.win.addch(yoffset, self.width-1, curses.ACS_RTEE)

        # Draw the text
        self.win.attron(curses.A_BOLD)
        self.win.addstr(0, 2, "FILE:")
        self.win.addstr(2, 2, "LINE:")
        self.win.addstr(2, line_len+2 , "COL:")
        self.win.addstr(4, 2, "MESSAGE:")
        self.win.attroff(curses.A_BOLD)

        self.win.addstr(2, 8, self._entry["line"])
        self.win.addstr(2, line_len + 7, self._entry["columns"])

        filecol = theme.getPair(curses.COLOR_BLUE, -1)
        self.win.addstr(0, 8, self._entry["filename"], filecol)

        warncol = theme.getPair(curses.COLOR_RED, -1)
        self.win.addstr(2, self.width-warn_len+2, self._entry["warn"].upper(), warncol|curses.A_BOLD)

        mess = theme.getPair(208, -1)

        for l in range(0, message_lines):
            start = l*(self.width-12)
            end   = start + self.width-12
            self.win.addstr(4+l, 11, self._entry["message"][start:end], mess)

        self.win.refresh()

