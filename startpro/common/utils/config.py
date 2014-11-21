#-*- encoding: utf-8 -*-
'''
Created on 2014年.05.26

@author: Allen
'''
import ConfigParser
import os


class Config():

    def __init__(self, config_file):
        self.config = ConfigParser.ConfigParser()
        self.config_file = config_file
        self.__init_config()

    def __init_config(self):
        try:
            if not os.path.exists(self.config_file):
                f = file(self.config_file, "w")
                f.close()
            self.config.read(self.config_file)
        except Exception, e:
            print e

    def set_config(self, section, option, value):
        try:
            value = str(value).replace(r'\n', '')
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, option, value)
            self.config.write(open(self.config_file, "w"))
            return True
        except Exception, e:
            print ("Warn:set_config error.%s" % e)
            return False

    def get_config(self, section, option):
        configVal = ""
        try:
            if not self.config.has_section(section):
                return configVal
            if not self.config.has_option(section, option):
                return configVal
            configVal = self.config.get(section, option)
        except Exception, e:
            print ("Warn:get_config error.%s" % e)
            return ''
        return str(configVal).strip()

    def get_config_list(self, section):
        configs = []
        try:
            if self.config.has_section(section):
                configs = self.config.items(section)
        except Exception, e:
            print ("Warn:get_configs error.%s" % e)
        return configs

    def remove_option(self, section, option):
        try:
            self.config.remove_option(section, option)
            self.config.write(open(self.config_file, "w"))
            return True
        except:
            return False
