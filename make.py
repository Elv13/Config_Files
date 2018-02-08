#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import gdb
from subprocess import PIPE, Popen
from threading  import Thread

ON_POSIX = 'posix' in sys.builtin_module_names

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

def highlighttxt(text, new, current):
    return "\033["+new+"m"+text+"\033["+current+"m"

# file:line[:column]:error/warning:error message
def parse_message(line):
    mess = re.compile('([^:]+):([0-9]+):([0-9]+):[ ]*([a-zA-Z ]+):(.+)$')
    parsed = mess.match(line)

    if parsed:

        fullname   = parsed.group(1)
        filename   = get_trimmed_filename(fullname)
        linenumber = parsed.group(2)
        colnumber  = parsed.group(3)
        mtype      = parsed.group(4)
        message    = parsed.group(5).strip()
        warn       = ""

        errre = re.compile('^[^\[]*\[-[A-Z]([a-z]+)')
        err = errre.match(message)

        if err:
            warn = err.group(1)

        col1, col2 = len(linenumber) +8, len(colnumber) + 7
        col4 = len(warn)+2
        col3 = columns - col1 - col2 - col4 - 5
        lfm = len(filename)

        col = "0"

        if mtype.find("rror") != -1:
            col = "0;38;5;124"

        code = ""

        try:
            code = get_code_lines(0, fullname, int(linenumber), 1, "\033["+col+"m")
        except:
            pass

        filename   = highlighttxt(" FILE: ", "39;1", col)+highlighttxt(filename, "34", col)
        linenumber = highlighttxt(" LINE: ", "39;1", col)+linenumber
        colnumber  = highlighttxt(" COL: ", "39;1", col)+colnumber
        message    = highlighttxt(" MESSAGE: ", "39;1", col)+highlighttxt(message, "0;38;5;208", col)
        warn       = highlighttxt(warn.upper(), "31;1", col)

        print("\r\033["+col+"m┌" + get_hline(columns-2) + "┐")
        print("│"+filename+'│'.rjust(columns-lfm-6, ' '))
        print("├"+get_hline(col1)+"┬"+get_hline(col2)+"┬"+get_hline(col3)+"┬"+get_hline(col4)+"┤")
        print("│"+linenumber + " │" +colnumber+' │'+'│ '.rjust(col3+4, ' ')+warn+" │")
        print("├"+get_hline(col1)+"┴"+get_hline(col2)+"┴"+get_hline(col3)+"┴"+get_hline(col4)+"┤")

        print("│"+message+' │')

        if len(code) > 0:
            sys.stdout.write(get_new_row(0))
            sys.stdout.write(code)

        sys.stdout.write("└" + get_hline(columns-2) + "┘\n\n")
        sys.stdout.flush()

def get_progress(line, fallback):
    mess = re.compile('\[[ ]*([0-9]+)%\]')
    parsed = mess.match(line)

    if not parsed:
        return fallback

    return int(parsed.group(1))

def print_progress(percent):
    width = int(((columns-7)/100.0)*percent)
    sys.stdout.write(' \r\033[32;1m[ '+str(percent)+"%]"+'>\033[32;0m'.rjust(width,'='))
    sys.stdout.flush()

def enqueue_output(out, queue, is_complete):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
    is_complete.append(True)

def run_make(args):
    p = Popen(['make -j8 '+args], stdout=PIPE, stderr=PIPE, bufsize=64, shell=True, close_fds=ON_POSIX,env=os.environ)
    q1, q2 = Queue(), Queue()

    is_complete = []

    t  = Thread(target=enqueue_output, args=(p.stdout, q1, is_complete))
    t2 = Thread(target=enqueue_output, args=(p.stderr, q2, is_complete))

    t.daemon, t2.daemon = True, True
    t.start()

    t2.start()

    last_progress = 0

    while True:
        while not q2.empty():
            try:
                line = q2.get_nowait()
            except Empty:
                pass
            else:
                parse_message(line)

        if len(is_complete) == 2:
            padding = (columns)/2+3
            sys.stdout.write(p.wait() > 0 and "\033[41m" or "\033[32m")
            sys.stdout.write("\r"+"COMPLETE".rjust(padding,'=')+('\033[39;0m').rjust(padding,'='))
            sys.stdout.flush()
            is_complete = []
            return

        try:
            line = q1.get(timeout=0.1)
            last_progress = get_progress(line, last_progress)
        except Empty:
            pass

        print_progress(last_progress)


class PrettyMake (gdb.Command):
    """Integrate compilation warnings with GDB"""

    def __init__ (self):
        super (PrettyMake, self).__init__ ("make", gdb.COMMAND_USER)

    def invoke (self, args, from_tty):
        run_make(args)

PrettyMake ()
