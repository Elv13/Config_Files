#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This module consume data exposed by the provider

import urllib.request, json, time

# Fetch all comments
def consume(*args):
    (server, port, job_uuid) = args
    retry = 0

    while True:
        comments = []
        try:
            with urllib.request.urlopen("http://127.0.0.1:"+port) as data:
                data = json.loads(data.read().decode())
                print("got data", len(data))
                #for comment in data:
                    #comments.append(comment)
        except:
            if retry >= 5:
                print("End job: ", job_uuid)
                break
            else:
                time.sleep(1)
                retry += 1
