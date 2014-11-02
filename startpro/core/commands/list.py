# encoding: utf-8

'''
Created on 2014年.05.26

@author: ZoeAllen
'''
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
        print('[INFO]:script list:')
        for k in sorted(get_script().keys()):
            print('----> %s' % k)
        