#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This module detect Q_ASSERT and print a summary

import gdb
import os

rows_, columns_ = os.popen('stty size', 'r').read().split()
rows, columns = int(rows_), int(columns_)

def print_scary_message(message):
    size    = len(message) + 12
    padding = ('').rjust(int(round((columns - size)/2)))
    print("")
    print(padding + "\033[40;5;1m"+('').rjust(size)+"\033[39;0m")
    print(padding + "\033[40;5;1m   == ASSERT ==   \033[39;0m")
    print(padding + "\033[40;5;1m"+('').rjust(size)+"\033[39;0m")
    print("")


def detect_asserts():
    frame_count =  0

    # If there is a cycle, then assume the newest frame is part of it
    newest = gdb.newest_frame()

    # Get the oldest frame
    f = newest

    if newest.name() != "raise":
        return

    f = f.older().older().older().older()
    sal = gdb.Frame.find_sal(f)

    print_scary_message("ASSERT")

    print_box(4, f, sal, 4, True)

    block = f.block()

    names = set()

    print("Variables:")

    thisVar = None

    while block:
        for symbol in block:
            if symbol.is_variable:
                name = symbol.name

                # Noisy metadata for unsupported Qt types are useless
                if name.find("qt_meta_") != -1:
                    continue

                # Relevant info from this are in pretty printed already
                if name.find("staticMetaObject") != -1:
                    continue

                if not name in names:
                    print('{} = {}'.format(name, symbol.value(f)))
                    names.add(name)
            elif symbol.is_argument and symbol.name == "this":
                thisVar = symbol
        block = block.superblock

    f.select()

    print("\nAttributes:")
    if thisVar != None:
        t = thisVar.type.unqualified().target()
        fields = t.fields()
        for field in fields:
            try:
                val = gdb.execute("print "+str(field.name), to_string=True)
                print(field.name," = ", val)
            except:
                print("FAILED TO READ",field.name)

    print("")


def stop_handler (event):
    if isinstance(event,gdb.SignalEvent):
        if event.stop_signal == "SIGABRT":
            detect_asserts()

gdb.events.stop.connect (stop_handler)
