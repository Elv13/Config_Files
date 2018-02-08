#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
import math
import sys
from theme import theme
from page import Page

class Pipeline(Page):
    def __init__(self):
        Page.__init__(self)
        self.full_width = True
        self.height = 18
        self._entry = None

    def set_entry(self, entry):
        self._entry = entry
        self.repaint()

    def draw_word(self, key, name, color, offset, attr):
        line = 0
        roffset = offset
        if offset + 6 + len(name) > self.width:
            line = 1
            roffset = 1 + max(0, offset - self.width + 4)

        self.help_win.addstr(line, roffset, " "+key+" ", curses.A_REVERSE|curses.A_BOLD)
        self.help_win.addstr(line, roffset+3, " "+name+" ", color|attr)
        return offset + 6 + len(name)

    def draw_stages(self, win, height):
        text_color = theme.getPair(238, -1)
        line_color = theme.getPair(234, -1)

        stages = [" Setup ", " Compile ", " Lint ", " Test ", " Package ", " Deploy "]

        stage_width = int(self.width-2)/(len(stages)+1)

        for i, t in enumerate(stages):
            win.attron(line_color)
            win.vline(2, int(stage_width + stage_width*i), curses.ACS_VLINE, height)
            win.attroff(line_color)
            win.attron(text_color)

            win.hline(2, int(stage_width + stage_width*i - len(t)/2), curses.ACS_HLINE, len(t))
            win.addch(2, int(stage_width + i*stage_width), curses.ACS_TTEE)

            win.attron(curses.A_REVERSE|curses.A_BOLD)
            win.addstr(1, int(stage_width + stage_width*i - len(t)/2), t)

            win.attroff(text_color)
            win.attroff(curses.A_REVERSE|curses.A_BOLD)

    def draw_step_block(self, win, x,y, color):
        win.attron(color)

        # Require python3.3
        #if (sys.version_info > (3, 3)):
            #win.addch(y  , x, "⣾"); win.addch(y  , x+1, "⣿");win.addch(y  , x+2, "⣷");
            #win.addch(y+1, x, "⢿"); win.addch(y+1, x+1, "⣿");win.addch(y+1, x+2, "⡿");
        #else:
            #win.hline(y  , x, curses.ACS_CKBOARD, 3)
            #win.hline(y+1, x, curses.ACS_CKBOARD, 3)
        win.hline(y  , x, curses.ACS_CKBOARD, 3)
        win.hline(y+1, x, curses.ACS_CKBOARD, 3)

        win.attroff(color)

    def draw_dependency(self, win, from_x, from_y, to_x, to_y):
        #win.addch(from_y, from_x, "┃") #┃┣┗━
        if (sys.version_info > (3, 3)):
            for i in range(from_y, to_y):
                win.addch(i, from_x, "┃")
            win.addch(to_y, from_x, "┗")
            for i in range(from_x+1, to_x):
                win.addch(to_y, i, "━")
        else:
            win.vline(from_y, from_x, curses.ACS_VLINE, to_y-from_y)
            win.hline(to_y, from_x, curses.ACS_HLINE, to_x-from_x)


    def draw_steps(self, win):
        done_color    = theme.getPair( 28, -1)
        fail_color    = theme.getPair(160, -1)
        current_color = theme.getPair(226, -1)
        self.draw_step_block(win, 10, 5 , done_color)
        self.draw_step_block(win, 20, 9 , fail_color)
        self.draw_step_block(win, 10, 13, current_color)
        self.draw_dependency(win, 11, 7, 20, 10)

    def draw_partial_box(self, height):
        self.draw_stages(self.win, 14)
        self.draw_steps(self.win)

    def repaint(self, clear = False):
        if self.win == None:
            return

        self.win.erase()

        # Draw the sides
        self.win.box()

        # Draw the box around the pipeline
        self.draw_partial_box(12)

        self.win.refresh()

