#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is the "central" component of the distributed CI. It creates and
# manage session tokens and job tokens. It listen to jobs data and broadcast
# all data back to all listeners
#
# Nothing is stored or parser, this is only multiplexing multiple input to
# multiple outputs.
#
# When used on multiple systems at, it makes a nice little proxy. This what
# enabled it to be a truly distributed system. While some module don't like
# having multiple instances (such as the artifact manager), they don't care
# if there is only one multiplexer of a dozen. The most dangerous trap here is
# having messages bouncing in circle between three or more multiplexer.

import flask
import json
import uuid
import consumer
from threading import Thread
import provider

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

# Disable stdout noise
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = flask.Flask(__name__)

session = str(uuid.uuid4())

def get_session():
    global session
    return session

@app.route('/version/')
def version():
    return '1'

@app.route('/gen_token/')
def gen_token():
    ret = {}
    ret[ "session_uuid"  ] = get_session()
    ret[ "job_uuid"      ] = str(uuid.uuid4())
    ret[ "suggested_port"] = 5003
    return json.dumps(ret)

@app.route('/register_provider/', methods=['GET'])
def register_provider():
    job_uuid = flask.request.args.get("job")
    ip_address = flask.request.args.get("ip")
    port = flask.request.args.get("port")
    args = str(ip_address), str(port), str(job_uuid),

    print("Begin job: ", job_uuid)

    t = Thread(target = consumer.consume, args = args)
    t.start()
    return json.dumps("Ok")

@app.route('/register_listener/', methods=['GET'])
def register_listener():
    job_uuid = flask.request.args.get("job")
    print("Add listener: ", job_uuid)
    t = Thread(target = consumer.consume, args = args)
    t.start()
    return json.dumps("Ok")


app.run(port=5001)
