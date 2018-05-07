#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses
import curses.wrapper
import os

rows_, columns_ = os.popen('stty size', 'r').read().split()
rows, columns = int(rows_), int(columns_)

class Picker:
    """Allows you to select from a list with curses"""
    stdscr = None
    win = None
    help_win = None
    title = ""
    more = ""
    c_selected = ""
    c_empty = ""
    
    cursor = 0
    offset = 0
    selected = 0
    selcount = 0
    aborted = False
    
    window_height = rows -8
    window_width = columns -2
    all_options = []
    length = 0

    mode_color = {
        'E': 7,
        'S': 10,
        'O': 8,
        'F': 9,
        ' ': 0
    }
    
    def curses_start(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()

        # Highlight color
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED) # O
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE) # E
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW) # F
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_CYAN) # S
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

        # Text color
        curses.init_pair(7 , curses.COLOR_BLUE  , -1)
        curses.init_pair(8 , curses.COLOR_RED   , -1)
        curses.init_pair(9 , curses.COLOR_YELLOW, -1)
        curses.init_pair(10, curses.COLOR_CYAN  , -1)

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

    def move_up(self):
        if self.cursor == 0:
            return

        tmp = self.all_options[self.cursor-1]
        self.all_options[self.cursor-1] = self.all_options[self.cursor]
        self.all_options[self.cursor] = tmp
        self.cursor -= 1

    def move_down(self):
        if self.cursor == len(self.all_options):
            return

        tmp = self.all_options[self.cursor+1]
        self.all_options[self.cursor+1] = self.all_options[self.cursor]
        self.all_options[self.cursor] = tmp
        self.cursor += 1


    def getSelected(self):
        if self.aborted == True:
            return( False )

        ret_s = filter(lambda x: x["selected"], self.all_options)
        ret = map(lambda x: x["label"], ret_s)
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
        offset = self.draw_word("E", "Edit", 3, 1, 0)
        offset = self.draw_word("F", "Fixup", 4, offset, 0)
        offset = self.draw_word("O", "Omit", 1, offset, 0)
        offset = self.draw_word("S", "Squash", 5, offset, 0)
        offset = self.draw_word("/", "Search", 6, offset, 0)
        offset = self.draw_word("K", "Move Up", 2, offset, curses.A_BOLD)
        offset = self.draw_word("J", "Move Down", 2, offset, curses.A_BOLD)
        offset = self.draw_word("Q", "Quit", 2, offset, curses.A_BOLD)
        self.help_win.refresh()
        
    def redraw(self):
        self.win.clear()
        self.win.box()
        
        position = 0
        range = self.all_options[self.offset:self.offset+self.window_height+1]
        for option in range:
            if option["selected"] != "":
                line_label = "["+ option["selected"] + "] "
            else:
                line_label = self.c_empty + " "
      
            # Highlight the current line
            if position == self.cursor:
                # Draw the background
                self.win.addstr(
                    position + 2, 1, ('').rjust(self.window_width - 2, ' '),
                    curses.color_pair(2)|curses.A_BOLD
                )

                self.win.addstr(
                    position + 2, 2, line_label + option["label"],
                    curses.color_pair(2)|curses.A_BOLD
                )
            else:
                self.win.addstr(
                    position + 2, 2, line_label + option["label"],
                    curses.color_pair(self.mode_color[ option["selected"] ])
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
                self.all_options[self.selected]["selected"] = "E"
            elif c == ord('s'):
                self.all_options[self.selected]["selected"] = "S"
            elif c == ord('o'):
                self.all_options[self.selected]["selected"] = "O"
            elif c == ord('f'):
                self.all_options[self.selected]["selected"] = "F"
            elif c == ord('k'):
                self.move_up()
            elif c == ord('j'):
                self.move_down()
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
        more="...",
        c_selected="[X]",
        c_empty="[ ]"
    ):
        self.title = title
        self.more = more
        self.c_selected = c_selected
        self.c_empty = c_empty
        
        self.all_options = []
        
        for option in options:
            self.all_options.append({
                "label": option,
                "selected": " "
            })
            self.length = len(self.all_options)
        
        self.curses_start()
        curses.wrapper( self.curses_loop )
        self.curses_stop()
