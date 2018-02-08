#!/usr/bin/python2
# -*- coding: utf-8 -*-

import base
import json
import session
import os
from warningpage import WarningPage
from tabs import Tabs
from help import Help

rows_, columns_ = os.popen('stty size', 'r').read().split()
rows, columns = int(rows_), int(columns_)

s = session.Session()
content = []

# Setup the table
elems = base.ElementList()
elems.alignColumn(0, base.Align.LEFT )
elems.alignColumn(1, base.Align.RIGHT)
elems.alignColumn(2, base.Align.RIGHT)
warninglist = base.ElementViewSlice(elems)

source = Tabs()
source.expand = False
source.height = 10
s.addPage(source)

source.add_tab(name = "Clazy"     , page= warninglist )
source.add_tab(name = "GCC"       , page= None        )
source.add_tab(name = "Krazy2"    , page= None        )
source.add_tab(name = "Coverity"  , page= None        )
source.add_tab(name = "MemCheck"  , page= None        )
source.add_tab(name = "HeapTrack" , page= None        )
#source.add_tab(name = "Static"    , page= None        )

# Create a waning list
with open("/tmp/clazy.json", 'r') as f:
    content = json.load(f)
    f.close()

    if len(content) == 0:
        exit(1)

    for entry in content:
        entry["warn"] = entry["warn"] if "warn" in entry else "foo"

        elem = base.Element(
            [entry["filename"],entry["line"], entry["warn"]],
            background = 196 if entry["iserror"] else None,
            foreground = 16 if entry["iserror"] else None
        )

        elems.add(elem)

# Display the selected warning data
warningpage = WarningPage()
warningpage.set_entry(content[0])

# Add some additional info
tabs = Tabs()
s.addPage(tabs)

tabs.add_tab(name = "Details"  , page= warningpage )
tabs.add_tab(name = "Code"     , page= None        )
tabs.add_tab(name = "Backtrace", page= None        )
tabs.add_tab(name = "Settings" , page= None        )

# Navigation
def go_up():
    warninglist.selectPrevious()
    warningpage.set_entry(content[warninglist.selected])

def go_down():
    warninglist.selectNext()
    warningpage.set_entry(content[warninglist.selected])

def next_page():
    tabs.view_next()

s.add_key(key = 'k', callback = go_up)
s.add_key(key = 'j', callback = go_down)
s.add_key(key = '\t', callback = next_page)

if rows > 21:
    helpPage = Help()
    s.addPage(helpPage)

s.display()
s.close()
