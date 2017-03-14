# encoding: utf-8

"""
Created on 2014.04.21

@author: Allen
"""


class TopCommand():

    def __init__(self):
        """
        Constructor
        """
        pass

    def run(self, **kwargvs):
        raise NotImplementedError

    def help(self, **kwargvs):
        """
        print help info.
        """
        pass
