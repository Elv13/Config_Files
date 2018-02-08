#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses

max_current_color_index = 2

def create_color(fg, bg):
    global max_current_color_index

    max_current_color_index +=1
    curses.init_pair(max_current_color_index, fg, bg)
    return curses.color_pair(max_current_color_index)

class Theme:
    def init(self):
        self.cache    = {}
        self.selected = create_color(curses.COLOR_GREEN, -1)|curses.A_REVERSE|curses.A_BOLD
        self.normal   = create_color(-1, -1)

    def getPair(self, foreground, background):
        background = background if background else -1
        foreground = foreground if foreground else -1

        if not background in self.cache:
            self.cache[background] = {}

        if not foreground in self.cache[background]:
            self.cache[background][foreground] = create_color(foreground, background)

        return self.cache[background][foreground]

theme = Theme()
