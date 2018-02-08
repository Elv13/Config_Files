#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses
from page import Page
import pygments
import string
import re
from theme import theme
from pygments import highlight
from pygments import lexers
from pygments import formatters

lex = pygments.lexers.get_lexer_by_name("c++")
form = pygments.formatters.get_formatter_by_name("256")

# ^[[38;5;241m
def get_color(win, seq):
    fields = []
    cur = ""
    idx = 0

    for char in seq:
        if char == "[":
            pass
        elif char == ";":
            fields.append(cur)
            cur = ""
        else:
            assert(int(char) < 10)
            cur += char

    fields.append(cur)

    if len(fields) < 1:
        return

    # 256 color mode
    if fields[0] == "38":
        fields[0] = "-1"

    # reset
    if fields[0] == "39" or fields[0] == "49" :
        return

    colors = []
    for f in fields:
        c = int(f)
        assert(c >= -1 and c < 256)
        colors.append(c)

    if len(fields) == 3:
        col = theme.getPair(colors[2], colors[0])

        if colors[1] == 5:
            col |= curses.A_BOLD

        return col
    elif len(fields) == 4:
        col = theme.getPair(colors[2], colors[0])

        if colors[1] == 5:
            col |= curses.A_BOLD

        return col
    elif len(fields) == 2:
        col = theme.getPair(colors[1], colors[0])
        return col
    elif len(fields) == 1:
        col = theme.getPair(-1, colors[0])
        return col

    return

def print_ansi(win, x, y, line):
    rel_pos = 0
    cur_escape = None
    cur_attr = None

    for i in range(0, len(line)):
        char = line[i]
        if cur_escape == None and char == "\033":
            cur_escape = ""
        elif cur_escape != None and char == "m":
            if cur_attr != None:
                win.attroff(cur_attr)
            cur_attr = get_color(win, cur_escape)

            if cur_attr != None:
                win.attron(cur_attr)

            cur_escape = None
        elif cur_escape != None:
            cur_escape += char
        else:
            win.addch(y, x+rel_pos, char)
            rel_pos += 1


def get_code_lines(lines, number, context):

    # Remove excess spaces
    linelen = []

    counter = 0
    for l in lines:

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

    for i in range(0, len(lines)):
        col = "\033[100m"

        if number - context + i == number:
            col = "\033[41m"

        ln = col+("{:"+str(maxnumlen)+"}").format(number - context + i)+"\033[49m "

        lines[i] = ln + lines[i]

    return lines

class CodeView(Page):
    def __init__(self):
        Page.__init__(self)
        self._current_line = 0
        self._code = [
            "NumberWrapper* wrap3 = nullptr;",
            "",
            "//Check if the URI is complete or short",
            "const bool hasAtSign = uri.hasHostname();",
            "",
            "// Append the account hostname, this should always reach the same destination",
            "// as long as the server implementation isn't buggy.",
            "const auto extendedUri = (hasAtSign || !account) ? uri : URI(QStringLiteral(\"%1@%2\")",
            "    .arg(uri)",
            "    .arg(account->hostname()));",
            "",
            "//Try to see if there is a better candidate with a suffix (LAN only)",
            "if ( !hasAtSign && account ) {",
            "",
            "    // Attempt an early candidate using the extended URI. The later",
            "    // `confirmedCandidate2` will attempt a similar, but less likely case.",
            "    if ((wrap2 = d_ptr->m_hDirectory.value(extendedUri))) {",
            "        if (auto cm = d_ptr->fillDetails(wrap2, extendedUri, account, contact, type))",
            "        return cm;",
            "    }",
            "}",
            "",
            "//Check",
            "ContactMethod* confirmedCandidate = d_ptr->fillDetails(wrap,uri,account,contact,type);",
            "",
            "//URIs can be represented in multiple way, check if a more verbose version",
            "//already exist",
            "ContactMethod* confirmedCandidate2 = nullptr;",
            "",
            "//Try to use a ContactMethod with a contact when possible, work only after the",
            "//contact are loaded",
            "if (confirmedCandidate && confirmedCandidate->contact())",
            "    confirmedCandidate2 = d_ptr->fillDetails(wrap2,uri,account,contact,type);",
            "",
            "ContactMethod* confirmedCandidate3 = nullptr;",
            "",
            "//Else, try to see if the hostname correspond to the account and flush it",
            "//This have to be done after the parent if as the above give \"better\"",
            "//results. It cannot be merged with wrap2 as this check only work if the",
            "//candidate has an account.",
            "if (hasAtSign && account && uri.hostname() == account->hostname()) {",
            "    if ((wrap3 = d_ptr->m_hDirectory.value(uri.userinfo()))) {",
            "        foreach(ContactMethod* number, wrap3->numbers) {",
            "        if (number->account() == account) {",
            "            if (contact && ((!number->contact()) || (contact->uid() == number->contact()->uid())))",
            "                number->setPerson(contact); //TODO Check all cases from fillDetails()",
            "            //TODO add alternate URI",
            "            confirmedCandidate3 = number;",
            "            break;",
            "        }",
            "        }",
            "    }",
            "}",
        ]

    def page_up(self):
        self._current_line -= self.height-2
        self._current_line = max(0, self._current_line)
        self.repaint()

    def page_down(self):
        self._current_line += self.height-2
        if self._current_line + self.height-2 > len(self._code):
            self._current_line = len(self._code) -  self.height - 2
        self.repaint()

    def repaint(self, clear = False):
        if self.win == None:
            return

        self.win.erase()

        sliced_lines = self._code[self._current_line:self._current_line+self.height-2]

        lines = get_code_lines(sliced_lines, self._current_line+1, 3)

        for i in range(0, len(lines)):
            print_ansi(self.win, 1, 1+i, lines[i])
            #self.win.addstr(1+i, 2, lines[i])

        self.win.box()

        self.win.refresh()

