# encoding: utf-8

'''
Created on 2014年.05.26

@author: Allen
'''
from startpro.core.topcmd import TopCommand

options = {'-name': "project name"}

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
            
        except Exception, e:
            print("[ERROR]:%s" % e)
        
        
    def help(self, **kwargvs):
        print('')
        print("Available options:")
        for name, desc in sorted(options.iteritems()):
            print("  %-13s %s" % (name, desc))
        