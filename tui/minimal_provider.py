#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file provides a minimal example to create an artifact provider. It is
# also useful for integration testing

import flaskthread
from threading import Thread
import time

flaskthread.beginListening()

def appendThings():
    data = {}
    data["foo"] = "bar"
    flaskthread.appendData(data)

while True:
    appendThings()
    time.sleep(2)

flaskthread.endListening()
