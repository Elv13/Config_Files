#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This module detect infinite recursion and gather statistics

import gdb
import os

rows_, columns_ = os.popen('stty size', 'r').read().split()
rows, columns = int(rows_), int(columns_)

# Get a table horizontal line
def get_hline2(length):
    s = ''
    for x in range(0, length):
        s = s + '─'

    return s

def get_new_row2(col1, col2):
    return "├" + get_hline2(col1) + "┼" + get_hline2(col2) + "┤\n"

def get_frame_count(autostop):
    frame_count =  0

    # If there is a cycle, then assume the newest frame is part of it
    newest = gdb.newest_frame()
    next_similar = []

    # Get the oldest frame
    f = newest

    while f != None:
        f = f.older()
        frame_count += 1

        if frame_count == 300:
            newest = f
            f = f.older()
            break

    distance = 0

    # Keep track of the same functions frame distance to extract the pattern
    while f != None and len(next_similar) < 10:
        if newest.name() == f.name():
            next_similar.append(distance)
            distance = 0
        else:
            distance += 1
        f = f.older()

    sequence_size = 0


    # Assume the sequence is present at least twice
    if next_similar[0] == next_similar[1] and next_similar[1] == next_similar[2]:
        sequence_size = next_similar[0]
    else:
        for i in range(1,8):
            if next_similar[0] == next_similar[i] and next_similar[i+1] == next_similar[1]:
                for j in range(0, i-1):
                    sequence_size += next_similar[j]

    largest = max(len("Cycle length: "), len("Start: "), len("Stop :"))+1

    gdb.execute("bt "+str(frame_count)+","+str(frame_count+sequence_size))

    gdb.write("===\033[41;5mINFINITE RECURSION DETECTED\033[39;0m===\n")

    gdb.write("┌" + get_hline2(largest+10) + "┐\n")
    gdb.write("│ \033[;1m   Cycle information\033[;0m"+('│\n'.rjust(largest+10-17, ' ')))
    gdb.write("├" + get_hline2(largest) + "┬" + get_hline2(9) + "┤\n")
    gdb.write("│ Cycle length: │ \033[32m"+'{:8}'.format(sequence_size) + "\033[39m│\n")
    gdb.write(get_new_row2(largest, 9))
    gdb.write("│ Start:        │ \033[32m"+'{:8}'.format(frame_count) + "\033[39m│\n")
    gdb.write(get_new_row2(largest, 9))
    gdb.write("│ Stop:         │ \033[32m"+'{:8}'.format(frame_count+sequence_size) + "\033[39m│\n")
    gdb.write("└" + get_hline2(largest) + "┴" + get_hline2(9) + "┘\n")

def handle_sigsegv():
    get_frame_count(False)


def stop_handler (event):
    if isinstance(event,gdb.SignalEvent):
        if event.stop_signal == "SIGSEGV":
            handle_sigsegv()

gdb.events.stop.connect (stop_handler)
