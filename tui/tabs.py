#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
from page import Page

class Tabs(Page):
    def __init__(self):
        Page.__init__(self)
        self.expand = True
        self.tabs = [] #["Simple", "Complex", "Extreme"]
        self.selected = 0

    def move(self, x,y):
        self.x = x
        self.y = y
        for tab in self.tabs:
            if "page" in tab and tab["page"] != None:
                xoff, yoff = 0 if tab["page"].full_width else 1, 2

                tab["page"].move(x+xoff, y+yoff)

    def resize(self, h, w):
        self.height = h
        self.width = w
        for tab in self.tabs:
            if "page" in tab and tab["page"] != None:
                woff = 0 if tab["page"].full_width else 2

                tab["page"].resize(h - 3, w-woff)

    def view_next(self):
        self.selected += 1
        if self.selected >= len(self.tabs):
            self.selected = 0

        self.win.erase()
        self.repaint()

    def add_tab(self, name, page):
        self.tabs.append({
            "name" : name,
            "page" : page,
        })

    def repaint(self, clear = False):
        if self.win == None:
            return

        if len(self.tabs) == 0:
            return

        if clear:
            self.win.clear()

        # Draw the tabs
        offset = 3
        selected_page = None if not "page" in self.tabs[self.selected] else self.tabs[self.selected]["page"]

        self.win.hline(1, 1, curses.ACS_HLINE, 2)

        for i in range(0, len(self.tabs)):
            info = self.tabs[i]
            tab = info["name"]
            self.win.addch(0, offset, curses.ACS_ULCORNER)
            self.win.addch(0, offset+3+len(tab), curses.ACS_URCORNER)
            self.win.hline(0, offset+1, curses.ACS_HLINE, 1)
            self.win.addstr(0, offset+2, tab.upper())
            self.win.hline(0, offset+2+len(tab), curses.ACS_HLINE, 1)
            self.win.hline(1, offset+4+len(tab), curses.ACS_HLINE, 1)

            if i == self.selected:
                self.win.addstr(0, offset+2, tab.upper(), curses.A_BOLD)
                self.win.addch(1, offset, curses.ACS_LRCORNER)
                self.win.addch(1, offset+3+len(tab), curses.ACS_LLCORNER)
                self.win.hline(1, offset+1, ' ', len(tab)+2)
            else:
                self.win.addstr(0, offset+2, tab.upper())
                self.win.addch(1, offset, curses.ACS_BTEE)
                self.win.addch(1, offset+3+len(tab), curses.ACS_BTEE)
                self.win.hline(1, offset+1, curses.ACS_HLINE, len(tab)+2)

            offset += 5+len(tab)

        self.win.hline(1, offset, curses.ACS_HLINE, self.width-offset-1)

        # Draw the box

        if selected_page and not selected_page.full_width:
            self.win.vline(2, 0, curses.ACS_VLINE, self.height-2)
            self.win.vline(2, self.width-1, curses.ACS_VLINE, self.height-2)

        self.win.hline(self.height - 1, 1, curses.ACS_HLINE, self.width-2)
        self.win.addch(1, 0, curses.ACS_ULCORNER)
        self.win.addch(1, self.width-1, curses.ACS_URCORNER)
        self.win.addch(self.height-1, 0, curses.ACS_LLCORNER)
        #self.win.addch(self.height-1, self.width-1, curses.ACS_LRCORNER) #WTF!

        self.win.refresh()

        # Draw the selected tab
        selected = self.tabs[self.selected]

        if "page" in selected and selected["page"] != None:
            page = selected["page"]

            if page.win == None:
                page.display(None)

            page.repaint(clear)

