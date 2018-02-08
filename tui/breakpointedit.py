#!/usr/bin/python2
# -*- coding: utf-8 -*-

import base
import json
import session
from pager import Pager
from editor import Editor
from basicpage import BasicPage
from tabs import Tabs
from help import Help

s = session.Session()
content = []

toptabs = Tabs()
toptabs.height = 10
toptabs.expand = False
s.addPage(toptabs)


elems = base.ElementList()


elems.add(base.Element( ["locat"] ))
elems.add(base.Element( ["bobcat"] ))
elems.add(base.Element( ["locat"] ))


bplist = base.ElementViewSlice(elems)
toptabs.add_tab(name = "Commands" , page= bplist )


tabs = Tabs()
s.addPage(tabs)

pipeline = Editor()
pipeline.expand = True
s.set_key_grabber(pipeline)
tabs.add_tab(name = "Commands" , page= pipeline )
tabs.add_tab(name = "Python"   , page= None     )

def go_up():
    pipeline.page_up()

def go_down():
    pipeline.page_down()

s.add_key(key = 'k', callback = go_up)
#s.add_key(key = 'j', callback = go_down)
#s.add_key(key = '\t', callback = next_page)

helpPage = Help()
s.addPage(helpPage)

s.display()
s.close()
