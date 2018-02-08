#!/usr/bin/python2
# -*- coding: utf-8 -*-

import base
import json
import session
from pager import Pager
from codeview import CodeView
from basicpage import BasicPage
from tabs import Tabs
from help import Help

s = session.Session()
content = []


#pipeline = Pager()
#pipeline.expand = True
#s.addPage(pipeline)

pipeline = CodeView()
pipeline.expand = True
s.addPage(pipeline)

def go_up():
    pipeline.page_up()

def go_down():
    pipeline.page_down()

s.add_key(key = 'k', callback = go_up)
s.add_key(key = 'j', callback = go_down)
#s.add_key(key = '\t', callback = next_page)

helpPage = Help()
s.addPage(helpPage)

s.display()
s.close()
