# encoding: utf-8

'''
Created on 2014年.05.26

@author: Allen
'''
from startpro.core.topcmd import TopCommand
from importlib import import_module
from startpro.core.settings import MAIN_PATH, MAIN_CONFIG
import os
import shutil

options = {'-name': "project name"}

DEFAULT_CFG  = '''
# Automatically created by: startpro
#
# For more information about the section see:
# https://github.com/zoe0316/startpro

[settings]
# Base settings

# execute module match pattern name
# default = script
# default = rest,db,web
# default = script*
default = script

[package]
name = %s
'''

class Command(TopCommand):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
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
            cfg_text = DEFAULT_CFG %kwargvs.get('name', '')
            cfg_path = os.path.join(dst, MAIN_CONFIG)
            with open(cfg_path, 'w+') as f:
                f.write(cfg_text)
        except Exception, e:
            print("[ERROR]:%s" % e)
        
    def help(self, **kwargvs):
        print('Create a project.')
        print('')
        print("Available options:")
        for name, desc in sorted(options.iteritems()):
            print("  %-13s %s" % (name, desc))
        