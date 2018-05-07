#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
import curses.wrapper
import os
import sys
import re
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

    def swap_up(self):
        if self.cursor == 0:
            return

        tmp = self.all_options[self.cursor-1]
        self.all_options[self.cursor-1] = self.all_options[self.cursor]
        self.all_options[self.cursor] = tmp
        self.cursor -= 1

    def swap_down(self):
        if self.cursor == len(self.all_options):
            return

        tmp = self.all_options[self.cursor+1]
        self.all_options[self.cursor+1] = self.all_options[self.cursor]
        self.all_options[self.cursor] = tmp
        self.cursor += 1

    def getSelected(self):
        if self.aborted == True:
            return( False )

        ret = ""

        mapper = {
            " ": "pick ",
            "E": "edit ",
            "S": "squash ",
            "F": "fixup ",
            "O": "#omit "
        }

        for o in self.all_options:
            ret += mapper[o["mode"]]+o["right"]+o["label"]+"\n"

        return( ret )

    def draw_word(self, key, name, color, offset, attr):
        line = 0
        roffset = offset
        if offset + 6 + len(name) > self.window_width:
            line = 1
            roffset = 1 + max(0, offset - self.window_width + 4)

        self.help_win.addstr(line, roffset, " "+key+" ", curses.A_REVERSE|curses.A_BOLD)
        self.help_win.addstr(line, roffset+3, " "+name+" ", curses.color_pair(color)|attr)
        return offset + 6 + len(name)

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

    def redraw(self):
        self.win.clear()
        self.win.box()

        position = 0
        range = self.all_options[self.offset:self.offset+self.window_height+1]
        for option in range:
            line_label = "["+ option["mode"] + "] "

            force_bold = curses.A_BOLD if option["mode"] != ' ' else 0

            # Highlight the current line
            if position == self.cursor:
                # Draw the background
                self.win.addstr(
                    position + 2, 1, option["right"].rjust(self.window_width - 2, ' '),
                    curses.color_pair(self.mode_color2[ option["mode"] ]['bg'])|curses.A_BOLD
                )

                self.win.addstr(
                    position + 2, 2, line_label + option["label"],
                    curses.color_pair(self.mode_color2[ option["mode"] ]['bg'])|curses.A_BOLD
                )
            else:
                # Draw the background
                self.win.addstr(
                    position + 2, 1, option["right"].rjust(self.window_width - 2, ' '),
                    curses.color_pair(27)
                )

                self.win.addstr(
                    position + 2, 2, line_label + option["label"],
                    curses.color_pair(self.mode_color2[ option["mode"] ]['fg'])|force_bold
                )

            position = position + 1

        # hint for more content above
        if self.offset > 0:
            self.win.addstr(1, 5, self.more, curses.color_pair(1))

        # hint for more content below
        if self.offset + self.window_height <= self.length - 2:
            self.win.addstr(self.window_height + 3, 5, self.more)

        self.win.addstr(0, 5, "[ " + self.title + " ]", curses.A_REVERSE)
        self.win.addstr(
            0, self.window_width - 11,
            "[ " + str(self.selcount) + "/" + str(self.length) + " ]"
        )

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

            temp = self.getSelected()
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

if len(sys.argv) == 1:
    print "This program requires an imput file"
    quit()
elif sys.argv[1].find("rebase") == -1:
    # This app only support rebase
    # TODO split into a dispatcher script
    call([ "nvim", sys.argv[1], '+0' ])
    quit()

content = []

with open(sys.argv[1]) as f:
    content = f.readlines()
    f.close()

options = []

line_parser = re.compile('([a-z]+) ([a-f0-9]+) (.*)')

for line in content:
    line = line.strip()
    if len(line) > 0:
        if line[0] == "#" or line == "noop":
            break;
        else:
            fields = line_parser.match(line)
            options.append([fields.groups(0)[2], fields.groups(0)[1]])

opts = Picker(
    title = 'COMMITS',
    options = options
).getSelected()

if opts == False:
    print "Aborted!"
    with open(sys.argv[1], 'w') as f:
        content = f.write('')
        f.close()
else:
    #print opts
    with open(sys.argv[1], 'w') as f:
        content = f.write(opts)
        f.close()
