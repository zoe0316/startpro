# encoding: utf-8

'''
Created on 2014年.05.26

@author: Allen
'''
from startpro.core.topcmd import TopCommand
from startpro.core.utils.opts import get_script

class Command(TopCommand):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def run(self, **kwargvs):
        print('[INFO]:script list:')
        for k in sorted(get_script(kwargvs.get('paths', []), bool(kwargvs.get('full', False))).keys()):
            print('----> %s' % k)
        