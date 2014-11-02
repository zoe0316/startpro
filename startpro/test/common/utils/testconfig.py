'''
Created on 2014.10.31

@author: ZoeAllen
'''
import unittest
from startpro.common.utils.config import Config

class Test(unittest.TestCase):


    def setUp(self):
        self.config = Config("./config.ini")


    def tearDown(self):
        pass
    
    def test_config(self):
        assert self.config
        
    def test_set_config(self):
        assert self.config.set_config("common", "host", "127.0.0.1")
        
    def test_get_config(self):
        print self.config.get_config('common', 'host')
        
    def test_get_config_list(self):
        print self.config.get_config_list('common')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()