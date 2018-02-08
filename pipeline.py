#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
#import curses.wrapper
import os
import sys
import re
import math
from subprocess import call

rows_, columns_ = os.popen('stty size', 'r').read().split()
rows, columns = int(rows_), int(columns_)

max_current_color_index = 2

def create_color(fg, bg):
    global max_current_color_index

    max_current_color_index +=1
    curses.init_pair(max_current_color_index, fg, bg)
    return max_current_color_index

class Picker:
    """Allows you to select from a list with curses"""
    stdscr = None
    win = None
    help_win = None
    title = ""
    more = ""

    cursor = 0
    offset = 0
    selected = 0
    selcount = 0
    aborted = False

    window_height = rows -8
    window_width = columns -2
    all_options = []
    length = 0

    # Create a color pair for each mode
    mode_color2 = {}

    def curses_start(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()

        self.mode_color2 = {
            'E': {
                'fg': create_color(curses.COLOR_BLUE, -1),
                'bg': create_color(curses.COLOR_BLACK, curses.COLOR_BLUE),
                },
            'S': {
                'fg': create_color(curses.COLOR_CYAN, -1),
                'bg': create_color(curses.COLOR_WHITE, curses.COLOR_CYAN),
                },
            'O': {
                'fg': create_color(curses.COLOR_RED, -1),
                'bg': create_color(curses.COLOR_BLACK, curses.COLOR_RED),
                },
            'F': {
                'fg': create_color(curses.COLOR_YELLOW, -1),
                'bg': create_color(curses.COLOR_BLACK, curses.COLOR_YELLOW),
                },
            ' ': {
                'fg': create_color(-1, -1),
                'bg': create_color(curses.COLOR_WHITE, curses.COLOR_GREEN),
                }
        }

        curses.init_pair(26, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

        # Commit hash
        curses.init_pair(27, 125  , -1)

        curses.noecho()
        curses.cbreak()
        self.win = curses.newwin(
            self.window_height + 5,
            self.window_width,
            1,
            1
        )
        self.help_win =  curses.newwin(
            4,
            self.window_width,
            self.window_height +6,
            1
        )
        self.draw_help()

    def curses_stop(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def draw_word(self, key, name, color, offset, attr):
        line = 0
        roffset = offset
        if offset + 6 + len(name) > self.window_width:
            line = 1
            roffset = 1 + max(0, offset - self.window_width + 4)

        self.help_win.addstr(line, roffset, " "+key+" ", curses.A_REVERSE|curses.A_BOLD)
        self.help_win.addstr(line, roffset+3, " "+name+" ", curses.color_pair(color)|attr)
        return offset + 6 + len(name)

    def draw_box(self, win, x, y, w, h):
        self.win.hline(curses.ACS_HLINE, w)

        self.win.vline(curses.ACS_VLINE, h)
        self.win.move(y, w-1)
        self.win.vline(curses.ACS_VLINE, h)

        self.win.move(y+h,x)
        self.win.hline( curses.ACS_HLINE, w)

        self.win.addch(y, x, curses.ACS_ULCORNER)
        self.win.addch(y+h, x, curses.ACS_LLCORNER)
        self.win.addch(y , w-1, curses.ACS_URCORNER)
        self.win.addch(h, w-1, curses.ACS_LRCORNER)

    def draw_stages(self, win, height):
        text_color = create_color(238, -1)
        line_color = create_color(234, -1)

        stages = [" Setup ", " Compile ", " Lint ", " Test ", " Package ", " Deploy "]

        stage_width = int(self.window_width-2)/(len(stages)+1)

        for i, t in enumerate(stages):
            win.attron(curses.color_pair(line_color))
            win.vline(2, int(stage_width + stage_width*i), curses.ACS_VLINE, height)
            win.attroff(curses.color_pair(line_color))
            win.attron(curses.color_pair(text_color))

            win.hline(2, int(stage_width + stage_width*i - len(t)/2), curses.ACS_HLINE, len(t))
            win.addch(2, int(stage_width + i*stage_width), curses.ACS_TTEE)

            win.attron(curses.A_REVERSE|curses.A_BOLD)
            win.addstr(1, int(stage_width + stage_width*i - len(t)/2), t)

            win.attroff(curses.color_pair(text_color))
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
        done_color    = curses.color_pair(create_color( 28, -1))
        fail_color    = curses.color_pair(create_color(160, -1))
        current_color = curses.color_pair(create_color(226, -1))
        self.draw_step_block(win, 10, 5 , done_color)
        self.draw_step_block(win, 20, 9 , fail_color)
        self.draw_step_block(win, 10, 13, current_color)
        self.draw_dependency(win, 11, 7, 20, 10)

    def draw_help(self):
        self.help_win.clear()
        offset = self.draw_word("E", "Edit"     , self.mode_color2['E']['bg'] , 1     , 0            )
        offset = self.draw_word("F", "Fixup"    , self.mode_color2['F']['bg'] , offset, 0            )
        offset = self.draw_word("O", "Omit"     , self.mode_color2['O']['bg'] , offset, 0            )
        offset = self.draw_word("S", "Squash"   , self.mode_color2['S']['bg'] , offset, 0            )
        offset = self.draw_word("/", "Search"   , 26                          , offset, 0            )
        offset = self.draw_word("K", "Move Up"  , 2 , offset, curses.A_BOLD)
        offset = self.draw_word("J", "Move Down", 2 , offset, curses.A_BOLD)
        offset = self.draw_word("Q", "Quit"     , 2 , offset, curses.A_BOLD)
        self.help_win.refresh()

    def draw_partial_box(self, height):
        self.draw_box(self.win, 0, 0, self.window_width, 17)
        self.draw_stages(self.win, 14)
        self.draw_steps(self.win)

    def redraw(self):
        self.win.clear()

        # Draw the box around the pipeline
        self.draw_partial_box(12)

        self.win.refresh()
        self.draw_help() #TODO remove

    def check_cursor_up(self):
        if self.cursor < 0:
            self.cursor = 0
            if self.offset > 0:
                self.offset = self.offset - 1

    def check_cursor_down(self):
        if self.cursor >= self.length:
            self.cursor = self.cursor - 1

        if self.cursor > self.window_height:
            self.cursor = self.window_height
            self.offset = self.offset + 1

            if self.offset + self.cursor >= self.length:
                self.offset = self.offset - 1

    def curses_loop(self, stdscr):
        while 1:
            self.redraw()
            c = stdscr.getch()

            if c == ord('q') or c == ord('Q'):
                self.aborted = True
                break
            elif c == curses.KEY_UP:
                self.cursor = self.cursor - 1
            elif c == curses.KEY_DOWN:
                self.cursor = self.cursor + 1
            #elif c == curses.KEY_PPAGE:
            #elif c == curses.KEY_NPAGE:
            elif c == ord('e'):
                self.all_options[self.selected]["mode"] = "E"
            elif c == ord('s'):
                self.all_options[self.selected]["mode"] = "S"
            elif c == ord('o'):
                self.all_options[self.selected]["mode"] = "O"
            elif c == ord('f'):
                self.all_options[self.selected]["mode"] = "F"
            elif c == ord('k'):
                self.swap_up()
            elif c == ord('j'):
                self.swap_down()
            elif c == 10:
                break

            # deal with interaction limits
            self.check_cursor_up()
            self.check_cursor_down()

            # compute selected position only after dealing with limits
            self.selected = self.cursor + self.offset

            self.selcount = len(temp)

    def __init__(
        self,
        options,
        title='Select',
        more="..."
    ):
        self.title       = title
        self.more        = more
        self.all_options = []

        for option in options:
            self.all_options.append({
                "label": option[0],
                "right": option[1]+" ",
                "mode" : " "
            })
            self.length = len(self.all_options)

        self.curses_start()
        curses.wrapper( self.curses_loop )
        self.curses_stop()

opts = Picker(
    title = 'COMMITS',
    options = []
)
