#!/usr/bin/python2
# -*- coding: utf-8 -*-

import base
import json
import os
import sys
import time
import curses
import session
from subprocess import PIPE, Popen
from threading  import Thread
from page import Page
from tabs import Tabs
from basicpage import BasicPage
from help import Help

ON_POSIX = 'posix' in sys.builtin_module_names

elems = None

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

os.environ["QT_MESSAGE_PATTERN"] = '|//|%{type}|//|%{appname}|//|%{file}|//|%{line}|//|%{qthreadptr}|//|%{time}|//|%{message}'

messages = []

def parse_qdebug(line, is_error = False):
    mess = {}
    if line[0:4] == "|//|":
        parsed = line.split("|//|")
        mess = {
            "type"      : parsed[1],
            "appname"   : parsed[2],
            "file"      : parsed[3],
            "line"      : parsed[4],
            "qthreadptr": parsed[5],
            "time"      : parsed[6],
            "message"   : parsed[7],
            "is_error"  : parsed[1] == "error"
        }
    else:
        mess = {
            "type"      : "",
            "appname"   : "",
            "line"      : "",
            "file"      : "",
            "qthreadptr": "",
            "time"      : "",
            "message"   : line,
            "is_error"  : is_error
        }

    col = -1

    if mess["type"] == "warning":
        col = 227
    elif mess["type"] == "error":
        col = 169,
    elif mess["type"] == "info":
        col = 99

    messages.append(mess)
    elems.add(base.Element(
        [mess["message"]],
        background = -1,
        foreground = col
    ))


def enqueue_output(out, queue, is_complete):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
    is_complete.append(True)

def run_make(args, q1, q2):
    args = ""
    p = Popen(['~/dev/ring-kde/build/src/ring-kde'+args], stdout=PIPE, stderr=PIPE, bufsize=64, shell=True, close_fds=ON_POSIX,env=os.environ)

    is_complete = []

    t  = Thread(target=enqueue_output, args=(p.stdout, q1, is_complete))
    t2 = Thread(target=enqueue_output, args=(p.stderr, q2, is_complete))

    t.daemon, t2.daemon = True, True
    t.start()

    t2.start()

    last_progress = 0

    while True:
        if len(is_complete) == 2:
            return

        while not q2.empty():
            try:
                line = q2.get_nowait()
                parse_qdebug(line, True)
            except Empty:
                pass

        try:
            line = q1.get(timeout=0.1)
            parse_qdebug(line)
        except Empty:
            pass


s = session.Session()
content = []

tabs = Tabs()
s.addPage(tabs)

elems = base.ElementList()
warninglist = base.ElementViewSlice(elems)

tabs.add_tab(name = "Ring-KDE" , page= warninglist )
tabs.add_tab(name = "Daemon"   , page= None )
tabs.add_tab(name = "System"   , page= None )

# Display info
class InfoPage(Page):
    def __init__(self):
        Page.__init__(self)
        self.height = 8
        self._entry = None

    def set_entry(self, entry):
        self._entry = entry
        self.repaint()

    def repaint(self, clear = False):
        if self.win == None:
            return

        self.win.erase()

        self.win.box()

        self.win.attron(curses.A_BOLD)
        self.win.addstr(1, 2, "FILE:"     )
        self.win.addstr(2, 2, "TIME:"     )
        self.win.addstr(3, 2, "COMPONENT:")
        self.win.addstr(4, 2, "THREAD:"   )
        self.win.addstr(5, 2, "TYPE:"     )
        self.win.addstr(6, 2, "COUNT:"    )
        self.win.attroff(curses.A_BOLD)

        if not self._entry:
            self.win.refresh()
            return

        self.win.addstr(1, 13, self._entry["file"]+":"+self._entry["line"])
        self.win.addstr(2, 13, self._entry["time"      ])
        self.win.addstr(3, 13, self._entry["appname"   ])
        self.win.addstr(4, 13, self._entry["qthreadptr"])
        self.win.addstr(5, 13, self._entry["type"      ])

        self.win.refresh()


basicPage = InfoPage()
s.addPage(basicPage)

# Navigation
def go_up():
    warninglist.selectPrevious()
    basicPage.set_entry(messages[warninglist.selected])

def go_down():
    warninglist.selectNext()
    basicPage.set_entry(messages[warninglist.selected])

def next_page():
    tabs.view_next()


s.add_key(key = 'k', callback = go_up)
s.add_key(key = 'j', callback = go_down)
s.add_key(key = '\t', callback = next_page)

q1, q2 = Queue(), Queue()
t3 = Thread(target=run_make, args=("", q1, q2))
t3.start()

s.display()
s.close()
