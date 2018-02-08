#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gdb
import os
import pygments
import string
import re
from pygments import highlight
from pygments import lexers
from pygments import formatters

rows_, columns_ = os.popen('stty size', 'r').read().split()
rows, columns = int(rows_), int(columns_)

lex = pygments.lexers.get_lexer_by_name("c++")
form = pygments.formatters.get_formatter_by_name("256")

def get_base_dir(): #TODO
    return "/home/lepagee/dev/commentFromSyntax/"

def get_trimmed_filename(filename):
    if filename.find(get_base_dir()) != -1:
        return os.path.normpath(filename).replace(get_base_dir(), "$SRC/")
    return filename

# Get a formatted `this` pointer
def get_this(f):
    thisVar = ""
    try:
        thisVar = str(gdb.Frame.read_var(f,"this"))
    except ValueError:
        return ["", 0]

    size = len(thisVar)

    if thisVar == "0x0":
        thisVar = "\033[31;1mNULL\033[39;0m"
        size = 4
    else:
        thisVar = "\033[32;1m"+thisVar+"\033[39;0m"

    return [thisVar, size]

# Get a table horizontal line
def get_hline(length):
    s = ''
    for x in range(0, length):
        s = s + '─'

    return s

def get_endline(length, color):
    return color+('│\n').rjust(length-1, ' ')

def get_first_col(offset):
    return "│ "+('').rjust(offset-1, ' ')+"│"

def get_indentation(line):
    line2 = line.lstrip()
    return len(line) - len(line2)

# Get a new table row
def get_new_row(offset):
    if offset > 0:
        return "│" + ('').rjust(offset, ' ') + "├" + get_hline(columns-offset-3) + "┤\n"
    else:
        return "├" + get_hline(columns-2) + "┤\n"

def get_code_lines(offset, path, number, context, color):
    lines = []
    minindent = 999999

    try:
        line = gdb.execute("list "+path+":"+str(number-context)+","+str(number+context-1), to_string=True)

        # Those provide no value
        if line[0:5] == "file:":
            return ""

        lines = line.split('\n')

        counter = 0

        for l in lines:

            # GDB adds a warning when the file changed, nothing can be done, skip
            if l.find("Source file is more") != -1:
                continue

            stripped = l[len(str(number+context)):].rstrip()

            mini = minindent

            if len(stripped.lstrip()) > 0:
                mini = get_indentation(stripped)

            if mini < minindent:
                minindent = mini

            lines[counter] = stripped
            counter += 1

        line = lines[0].encode('utf-8')

    except:
        pass

    # Remove excess spaces
    linelen = []

    counter = 0
    for l in lines:
        l = l[mini:].rstrip()

        if l == "":
            l = "~"

        lines[counter] = l
        counter += 1
        linelen.append(len(l))

    concat = string.join(lines, "\n")

    # Highlight
    concat = highlight(concat.encode('utf-8'), lex, form).encode('utf-8').rstrip()

    lines = concat.split("\n")

    ret = ""
    counter = 0
    maxnumlen = len(str(number+context))
    for l in lines:
        col = "\033[100m"

        if number - context + counter == number:
            col = "\033[41m"

        ln = col+("{:"+str(maxnumlen)+"}").format(number - context + counter)+"\033[49m "

        if offset > 0:
            ret += get_first_col(offset)
        else:
            ret += "│ "

        ret += ln + l.rstrip() + get_endline(columns-offset-linelen[counter]-maxnumlen+1, color)
        counter += 1

    return ret

# Get a frame file information line
def get_fileinfo(filename, line):
    # Hide Qt garbage and noisy paths
    if filename.find("/moc_") != -1:
        filename = "Qt MOC FILE"

    filename = get_trimmed_filename(filename)

    buf = " PATH: \033[34m" + filename + "\033[39;0m"

    buf += " LINE \033[30;44;1m: " + str(line) + " :\033[39;0m"

    return buf, len(filename) + len(str(line)) + 11

# Get a line with the frame name
def get_frame_header(offset, f, sal, color):
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

def get_function_block(block):
    while block.function == None:
        block = block.superblock

    return block

def get_frame_arguments(f):
    args = []

    #TODO it should be possible to get the function block for missing obj too
    try:
        block = f.block()
    except:
        return args

    # Get the function
    block = get_function_block(block)

    for symbol in block:
        if symbol.is_argument:
            val = {}
            val["name"] = symbol.name
            val["type"] = str(symbol.type)

            try:
                val["value"] = str(f.read_var(symbol))
            except:
                val["value"] = "N/A"

            args.append(val)

    return args

def get_flat_frame_arguments(offset, f, color):
    ret = get_new_row(offset) + get_first_col(offset)

    args = get_frame_arguments(f)

    if len(args) == 0:
        return ""

    pos = offset + 1

    for arg in args:
        nulloffset = arg["value"] == "0x0" and 1 or 0
        linelen = len(arg["name"]) + len(arg["type"]) + len(arg["value"])+6+nulloffset

        # Don't show multiline or long values
        if len(arg["value"]) > columns-offset or arg["value"].find("\n") != -1:
            linelen -= len(arg["value"]) - 6
            arg["value"] = "\033[35;1mHIDDEN\033[39;0m"
        elif arg["value"] == "<optimized out>":
            linelen -= len(arg["value"]) - 9
            arg["value"] = "\033[33;1mOPTIMIZED\033[39;0m"

        if linelen > columns-offset-3:
            linelen -= len(arg["type"]) - 3
            arg["type"] = "###"

        if pos + linelen + 3 > columns:
            ret += get_endline(columns-pos+3, color)+get_first_col(offset)
            pos = offset + 1

        ret += " \033[38;5;240m(" + arg["type"] \
            +") \033[38;5;202m"+ arg["name"] +"\033[39m="

        if nulloffset > 0:
            ret += "\033[41;30;1mNULL\033[39;0m,"
        else:
            ret += arg["value"]+","

        pos += linelen

    ret += get_endline(columns-pos+3, color)

    return ret

def print_box(number, f, sal, context, arguments):
    filename = "N/A"

    color = ""

    if sal.symtab != None:
        filename = sal.symtab.filename
    else:
        color = "\033[90m"

    line = sal.line

    firstColLen = len(str(number))+2

    # The header
    buf = get_frame_header(firstColLen, f, sal, color)

    # Info line
    fileinfo, fileinfo_len = get_fileinfo(filename, line)
    buf += "│ "+str(number)+" │\033[39;0m" + fileinfo + get_endline(columns-fileinfo_len-firstColLen-4,color)

    # Display the frame arguments
    if arguments == True:
        buf += get_flat_frame_arguments(firstColLen, f, color)

    # Display some code
    if context > 0 and sal.symtab != None:
        srcline = get_code_lines(firstColLen, filename , line, context-1, color)
        buf += get_new_row(firstColLen) + srcline

    # Footer
    buf += "└"+ get_hline(firstColLen) +'┴'+ get_hline(int(columns)-3-firstColLen)+'┘\033[39;0m\n'

    gdb.write(buf)


def print_pretty_frame(number, context, arguments, variable, attributes):
    cur = 0

    f = None

    # Select the current frame
    if number == -1:
        f = gdb.selected_frame ()
        cur = -1
    else:
        f = gdb.newest_frame()

    while f is not None:
        if cur == number:
            f.select()
            sal = gdb.Frame.find_sal(f)
            print_box(number, f, sal, context, arguments)
            return

        f = gdb.Frame.older(f)
        cur +=1

def print_thread(number):
    name = "[THREAD: "+str(number)+"]"
    padding = (columns - len(name))
    name = "\033[107;30;1m"+name+"\033[39;0m"
    gdb.write(''.rjust(padding/2+padding%2, '=')+name+''.rjust(padding/2, '='))

def print_pretty_backtrace(allfrm, context, arguments, variable, attributes, ran):
    #for thread in gdb.selected_inferior().threads():
        #thread.switch()
        #print_thread(thread.num)

    thread = gdb.selected_thread()

    f = gdb.newest_frame()

    number = 0

    while f is not None:
        if number >= ran[0]:
            sal = gdb.Frame.find_sal(f)

            if (ran[0] != -1 or allfrm == True) or sal.symtab != None:
                print_box(number, f, sal, context, arguments)

        if number >= ran[1] and ran[1] != -1:
            return

        f = gdb.Frame.older(f)
        number +=1

class PrettyBt (gdb.Command):
    """Print a more useful backtrace"""

    def __init__ (self):
        super (PrettyBt, self).__init__ ("bt", gdb.COMMAND_USER)
        self.rang = re.compile('[ ]*([0-9]+),([0-9]+)')

    def invoke (self, arg, from_tty):
        args = arg.split(' ')

        first, last = -1, -1

        limit = self.rang.match(arg)

        if limit:
            first = int(limit.group(1))
            last = int(limit.group(2))

        print_pretty_backtrace(
            arg.find("all") != -1,
            arg.find("context") != -1 and 2 or 0,
            arg.find("args") != -1,
            False, False, (first, last)
        )

PrettyBt ()

class PagedBt (gdb.Command):
    """Print a more useful backtrace"""

    def __init__ (self):
        super (PagedBt, self).__init__ ("btf", gdb.COMMAND_USER)
        self.rang = re.compile('[ ]*([0-9]+),([0-9]+)')

    def invoke (self, arg, from_tty):
        args = arg.split(' ')

        first, last = -1, -1

        limit = self.rang.match(arg)

        if limit:
            first = int(limit.group(1))
            last = int(limit.group(2))

        print_pretty_backtrace(
            arg.find("all") != -1,
            3,
            True,
            True, True, (first, last)
        )

PagedBt ()

class PrettyFrame (gdb.Command):
    """Print a more useful backtrace"""

    def __init__ (self):
        super (PrettyFrame, self).__init__ ("frame", gdb.COMMAND_USER)

    def invoke (self, arg, from_tty):
        if arg == None or arg == "":
            print_pretty_frame(-1, 5, True, False, False)
            return

        args = arg.split(' ')

        index = 0

        try:
            index = int(args[0])
        except:
            gdb.write("The argument isn't a number")
            return
        print_pretty_frame(index, 5, True, False, False)

PrettyFrame ()
