# encoding: utf-8

'''
Created on 2014.05.26

@author: Allen
'''
import sys
import re
from startpro.core.topcmd import TopCommand
from startpro.core.utils.opts import get_script

options = {"-full": "if need full path name of script"}

class Command(TopCommand):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def run(self, **kwargvs):
        if len(sys.argv) < 3:
            print('[INFO]:need start script name.')
            return
        scripts = get_script(kwargvs.get('paths', []), bool(kwargvs.get('full', False)))
        script_name = str(sys.argv[2])
        if not scripts.has_key(script_name):
            try:
                n = int(script_name)
                script_name = sorted(scripts.keys())[n]
            except:
                print('[INFO]:Unsupported script.')
                return
        func = scripts.get(script_name)
        func(**kwargvs)
        
    def help(self, **kwargvs):
        print('Start a program.')
        print('')
        print("Available options:")
        for name, desc in sorted(options.iteritems()):
            print("  %-13s %s" % (name, desc))
        
        
        