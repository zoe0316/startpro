# encoding: utf8

"""
Created on 2014.06.23

@author: Allen
"""


class Process(object):
    def __init__(self):
        pass

    def start(self):
        raise NotImplementedError

    def run(self, **kwargvs):
        raise NotImplementedError
