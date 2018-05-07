#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file wait for data, gather it and dump it into a socket
# The socket consumer must wait on the socket for data to be available then
# read it (aka: server push).

import flask
import os
import time
from threading import Thread, Lock, Condition
import json
import urllib

# Disable stdout noise
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class Provider:
    """An application page"""

    def __init__(self):
        self.slices = []
        self.xpos   = []
        self.wins   = []
        self.height = 0
        self.width  = 0
        self.stdscr = None
        self.keys   = {}
        self._keygrabber = None


app = flask.Flask(__name__)

queue = []

datamtx = Condition()

readyToQuit = False
last_progress = 0

# Prtect the queue
qmtx = Lock()

token = ""
port = 5000

def register_job():
    global port, token

    data = {}

    # Get a new job token from the central manager
    with urllib.request.urlopen("http://127.0.0.1:5001/gen_token/") as server:
        data = json.loads(server.read().decode())
        token = data["job_uuid"]
        port  = data["suggested_port"]

    with urllib.request.urlopen("http://127.0.0.1:5001/register_provider/?job="+token+"&port="+str(port)+"&ip=http://127.0.0.1/") as server:
        data = json.loads(server.read().decode())

def begin_app():
    register_job()
    global port, token
    app.run(port=port)

t = Thread(target = begin_app, args = ())

# **MUST** be called from the main thread before adding data
def beginListening():
    global datamtx
    global t
    datamtx.acquire()
    t.start()

def endServer():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# Quit cleanly
def endListening():
    global readyToQuit
    global datamtx
    readyToQuit = True
    datamtx.release()
    time.sleep(1)
    datamtx.acquire()
    global t
    t.join()

# Called from the "main" thread
def appendData(dt):
    global datamtx
    global qmtx
    global queue

    # Add the data to the queue
    qmtx.acquire()
    queue.append(dt)
    qmtx.release()

    # Unlock the waiting request
    datamtx.notify()
    datamtx.release()
    time.sleep(0.05)

    # Lock new requests again
    datamtx.acquire()

# Notify the manager of this job progress
def setProgress(progress):
    global last_progress, token
    if int(progress) > last_progress:
        last_progress = int(progress)
        ret = {}
        ret["job_uuid"] = token
        ret["progress"] = last_progress
        appendData(ret)

# If there is data, then return it, otherwise wait for data
def getData():
    global queue
    global datamtxt2
    global datamtxt
    global readyToQuit

    # Only quit when all the data is consumed
    if readyToQuit and len(queue) == 0:
        endServer()
        return ''

    if len(queue) > 0:
        # Consume the cached data
        qmtx.acquire()
        data = queue
        queue = []
        qmtx.release()
        return data
    else:
        # Wait for new data
        datamtx.acquire()
        qmtx.acquire()

        # Until some kind of message passing socket replace the mutex, the
        # sleep may cause a race condition where the queue is empty
        while len(queue) == 0 and not readyToQuit:
            qmtx.release()
            datamtx.release()
            time.sleep(0.05)
            datamtx.acquire()
            qmtx.acquire()

        # Bye
        if readyToQuit:
            endServer()

        # Reset the queue
        data = queue
        queue = []
        qmtx.release()
        datamtx.release()

        return data

@app.route('/')
def interface_help():
    data = getData()
    return json.dumps(data, indent=4)

@app.route('/version/')
def interface_hello():
    return '1'

@app.route('/reset/')
def interface_rebuild():
    global qmtx
    global queue
    qmtx.acquire()
    queue = []
    qmtx.release()
    return 'Cleared'

