# encoding: utf-8

"""
Created on 2014.04.21

@author: Allen
"""


class TopCommand(object):

    def __init__(self):
        """
        Constructor
        """
        pass

    def run(self, **kwargs):
        raise NotImplementedError

    def help(self, **kwargs):
        """
        print help info.
        """
        pass
