#!/usr/bin/python2
# -*- coding: utf-8 -*-

import curses

class Page:
    def __init__(self):
        self.position = 0
        self.height = 10
        self.width = 10
        self.x = 0
        self.y = 0
        self.expand = False
        self.full_width = False
        self.win = None

    def resize(self, h, w):
        self.height = h
        self.width = w

    def move(self, x,y):
        self.x = x
        self.y = y

    def key_event(key):
        return False

    def display(self, sess):
        self.win = curses.newwin(
            self.height,
            self.width,
            self.y,
            self.x
        )
        self.repaint()


    def repaint(self, clear = False):
        raise NotImplementedError('subclasses must override foo()!')
