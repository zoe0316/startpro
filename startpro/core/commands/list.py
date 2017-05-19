# encoding: utf-8

"""
Created on 2014.05.26

@author: Allen
"""
from startpro.core.topcmd import TopCommand
from startpro.core.utils.opts import get_script

options = {"-full": "if need full path name of script",
           "-choose":'if need to display the scripts you want. e.g. Like script "first.second.third" which start with "first" Use [script list -choose first] to show all qualified scripts'}

class Command(TopCommand):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """

    def run(self, **kwargvs):
        scripts = enumerate(sorted(get_script(kwargvs.get('paths', []), bool(kwargvs.get('full', False)), kwargvs.get('choose', None)).keys()))
        print('[INFO]:script list:')
        for i, k in scripts:
            print('----> %d: %s' % (i, k))

    def help(self, **kwargvs):
        print('Lists all program.')
        print('')
        print("Available options:")
        for name, desc in sorted(options.items()):
            print("  %-13s %s" % (name, desc))
