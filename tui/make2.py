#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script parse Ninja or Make output to extract the compiler warnings
# and print a pretty progressbar

# It either write to a file to be consumed later or upload to an artifact
# manager service

import sys
import os
import re
import json
import multiprocessing
import provider
from subprocess import PIPE, Popen
from threading  import Thread

ON_POSIX = 'posix' in sys.builtin_module_names

rows_, columns_ = os.popen('stty size', 'r').read().split()
rows, columns = int(rows_), int(columns_)

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

# file:line[:column]:error/warning:error message
def parse_message(line):
    mess = re.compile('([^:]+):([0-9]+):([0-9]+):[ ]*([a-zA-Z ]+):(.+)$')
    parsed = mess.match(line)
    warning = {}

    if parsed:
        warning["fullname"  ] = parsed.group(1)
        warning["filename"  ] = os.path.basename(warning["fullname"])
        warning["line"      ] = parsed.group(2)
        warning["columns"   ] = parsed.group(3)
        warning["type"      ] = parsed.group(4)
        warning["message"   ] = parsed.group(5).strip()
        warning["warning"   ] = ""

        errre = re.compile('^[^\[]*\[-[A-Z]([a-z]+)')
        err = errre.match(warning["message"])

        if err:
            warning["warn"] = err.group(1)

        warning["iserror"] = warning["type"].find("rror") != -1

        if len(sys.argv) >= 3 and sys.argv[2] != "--no-print":
            sys.stdout.write(warning["filename"]+"("+warning["line"]+"): "+warning["message"]+"\n")

        sys.stdout.flush()

    return warning

def get_progress(line, fallback):
    mess = re.compile('\[[ ]*([0-9]+)%\]')
    parsed = mess.match(line)

    if not parsed:
        return fallback

    return int(parsed.group(1))

def print_progress(percent):
    width = int(((columns-7)/100.0)*percent)
    sys.stdout.write(' \r\033[32;1m[ '+str(percent)+"%]"+'>\033[32;0m\r'.rjust(width,'='))
    sys.stdout.flush()
    provider.setProgress(percent)

def enqueue_output(out, queue, is_complete):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
    is_complete.append(True)

def print_completed(code):
    padding = int((columns)/2+3)
    sys.stdout.write(code > 0 and "\033[41m" or "\033[32m")
    sys.stdout.write("\r"+"COMPLETE".rjust(padding,'=')+('\033[39;0m').rjust(padding,'='))
    sys.stdout.flush()

def parse_output(p, q1, q2):
    is_complete = []
    t  = Thread(target=enqueue_output, args=(p.stdout, q1, is_complete))
    t2 = Thread(target=enqueue_output, args=(p.stderr, q2, is_complete))

    t.daemon, t2.daemon = True, True
    t.start()

    t2.start()

    last_progress = 0

    warnings = []

    while True:
        while not q2.empty():
            try:
                line = q2.get_nowait().decode('utf-8')
            except Empty:
                pass
            else:
                ret = parse_message(line)
                if len(ret) > 0:
                    provider.appendData(ret)
                    warnings.append(ret)

        if len(is_complete) == 2:
            print_completed(p.wait())
            is_complete = []
            break

        try:
            line = q1.get(timeout=0.1).decode('utf-8')
            last_progress = get_progress(line, last_progress)
        except Empty:
            pass

        print_progress(last_progress)
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'w') as f:
            f.write(json.dumps(warnings, indent=4))
            f.write('\n')
            f.close()

def run_ninja(args):
    p = Popen(['ninja '+args], stdout=PIPE, stderr=PIPE, bufsize=64, shell=True, close_fds=ON_POSIX,env=os.environ)
    q1, q2 = Queue(), Queue()
    parse_output(p, q1, q2)

def run_make(args):
    provider.beginListening()
    count = str(multiprocessing.cpu_count())
    p = Popen(['make -j'+count+' '+args], stdout=PIPE, stderr=PIPE, bufsize=64, shell=True, close_fds=ON_POSIX,env=os.environ)
    q1, q2 = Queue(), Queue()
    parse_output(p, q1, q2)
    provider.endListening()

run_make("")
#run_ninja("")

