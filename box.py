#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Get a table horizontal line
def get_hline25(length):
    s = ''
    for x in range(0, length):
        s = s + '─'

    return s

# Get a line with the frame name
def box_first_line():
    return "┌"+get_hline(columns-2)+'┐\n'

def box_last_line():
    return "└"+get_hline(columns-2)+'┘\033[39;0m\n'

def box_second_line(offset, tag, color):
    framename = gdb.Frame.name(f)

    thisVar, thisSize = get_this(f)

    framename_len = len(framename)

    thislen = 0

    this = ""

    if thisSize > 0:
        this = '['+thisVar+']─'
        thislen = thisSize + 3

    firstCol = get_hline(offset)

    #             ┌    ────         ┬─[...]  ┐
    totalOffset = 1 + offset + 2      + 1 + 4

    middleLineWidth = columns-totalOffset-framename_len-thislen

    if middleLineWidth < 0:
        framename = "..."+framename[-middleLineWidth+3:]
        framename_len = len(framename)
        middleLineWidth = 0

    endcol = '\033[0m'

    # Crop the title to fix the current terminal
    title = '[ \033[39;1m'+framename.encode('utf-8')+endcol+color+' ]'

    return color+"┌"+firstCol+"┬─"+title+get_hline(middleLineWidth)+this+'┐\n'
