#!/usr/bin/python2
# -*- coding: utf-8 -*-

import base
import json
import session
from pipeline import Pipeline
from basicpage import BasicPage
from tabs import Tabs
from help import Help

s = session.Session()
content = []

#s.add_key(key = 'k', callback = go_up)
#s.add_key(key = 'j', callback = go_down)
#s.add_key(key = '\t', callback = next_page)

pipeline = Pipeline()
s.addPage(pipeline)

fill = BasicPage()
fill.expand = True
s.addPage(fill)

helpPage = Help()
s.addPage(helpPage)

s.display()
s.close()
