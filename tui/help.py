#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
from page import Page
from theme import theme

class Help(Page):
    def __init__(self):
        Page.__init__(self)
        self.height = 2

    def draw_word(self, key, name, color, offset, attr):
        line = 0
        roffset = offset
        if offset + 6 + len(name) > self.width:
            line = 1
            roffset = 1 + max(0, offset - self.width + 4)

        self.win.addstr(line, roffset, " "+key+" ", curses.A_REVERSE|curses.A_BOLD)
        self.win.addstr(line, roffset+3, " "+name+" ", curses.color_pair(color)|attr)
        return offset + 6 + len(name)

    def repaint(self, clear = False):
        if self.win == None:
            return

        if clear:
            self.win.clear()


        #self.mode_color2 = {
        #'E': {
            #'fg': create_color(curses.COLOR_BLUE, -1),
            #'bg': create_color(curses.COLOR_BLACK, curses.COLOR_BLUE),
            #},
        #'S': {
            #'fg': create_color(curses.COLOR_CYAN, -1),
            #'bg': create_color(curses.COLOR_WHITE, curses.COLOR_CYAN),
            #},
        #'O': {
            #'fg': create_color(curses.COLOR_RED, -1),
            #'bg': create_color(curses.COLOR_BLACK, curses.COLOR_RED),
            #},
        #'F': {
            #'fg': create_color(curses.COLOR_YELLOW, -1),
            #'bg': create_color(curses.COLOR_BLACK, curses.COLOR_YELLOW),
            #},
        #' ': {
            #'fg': create_color(-1, -1),
            #'bg': create_color(curses.COLOR_WHITE, curses.COLOR_GREEN),
            #}
        #}

        offset = self.draw_word("E", "Edit"     , theme.getPair(122, -1) , 1     , 0            )
        offset = self.draw_word("F", "Fixup"    , theme.getPair(curses.COLOR_BLACK, curses.COLOR_YELLOW) , offset, 0            )
        offset = self.draw_word("O", "Omit"     , theme.getPair(curses.COLOR_BLACK, curses.COLOR_RED) , offset, 0            )
        offset = self.draw_word("S", "Squash"   , theme.getPair(curses.COLOR_WHITE, curses.COLOR_CYAN) , offset, 0            )
        #offset = self.draw_word("/", "Search"   , 26                          , offset, 0            )
        offset = self.draw_word("K", "Move Up"  , 2 , offset, curses.A_BOLD)
        offset = self.draw_word("J", "Move Down", 2 , offset, curses.A_BOLD)
        offset = self.draw_word("Q", "Quit"     , 2 , offset, curses.A_BOLD)
        self.win.refresh()


