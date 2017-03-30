# encoding: utf-8

"""
Created on 2014年.05.26

@author: Allen
"""
from importlib import import_module
import os
import shutil

from startpro.core.topcmd import TopCommand
from startpro.core.settings import MAIN_PATH, MAIN_CONFIG

options = {'-name': "project name"}


class Command(TopCommand):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """

    def run(self, **kwargvs):
        try:
            if not kwargvs.get('name', None):
                print("[WARN]:create a project by argument '-name [value]'.")
                return None
            mod = import_module(MAIN_PATH)
            src = mod.__path__[0]
            dst = os.path.join(os.getcwd(), kwargvs['name'])
            if not os.path.exists(dst):
                os.mkdir(dst)
            else:
                print("[INFO]:directory exists.")
            cfg = os.path.join(src, MAIN_CONFIG)
            shutil.copy(cfg, dst)
        except Exception as e:
            print("[ERROR]:%s" % e)

    def help(self, **kwargvs):
        print('Create a project.')
        print('')
        print("Available options:")
        for name, desc in sorted(options.items()):
            print("  %-13s %s" % (name, desc))
