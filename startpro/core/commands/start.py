# encoding: utf-8

'''
Created on 2014.05.26

@author: ZoeAllen
'''
import sys
from core.topcmd import TopCommand
from core.utils.opts import get_script

class Command(TopCommand):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def run(self, **kwargvs):
        scripts = get_script()
        script_name = str(sys.argv[2])
        if not scripts.has_key(script_name):
            print('[INFO]:Unsupported script.')
            sys.exit(1)
        func = scripts.get(script_name)
        func(**kwargvs)
        
        
        