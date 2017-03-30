# -*- encoding: utf-8 -*-
"""
Created on 2014年.05.26

@author: Allen
"""
import os
import sys

if sys.version_info[0] < 3:
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser


class Config(object):
    """
    parse config file
    """

    def __init__(self, config_file):
        """

        :param config_file: config file path
        :return:
        """
        self.config = ConfigParser()
        self.config_file = config_file
        self.__init_config()

    def __init_config(self):
        try:
            if not os.path.exists(self.config_file):
                # new config file
                f = file(self.config_file, "w")
                f.close()
            self.config.read(self.config_file)
        except Exception as e:
            print(e)

    def set_config(self, section, option, value):
        """
        set config
        :param section: section name
        :param option: under section option name
        :param value: string val
        :return:
        """
        try:
            value = str(value).replace(r'\n', '')
            if not self.config.has_section(section):
                # check
                self.config.add_section(section)
            self.config.set(section, option, value)
            self.config.write(open(self.config_file, "w"))
            return True
        except Exception as e:
            print(e)
            return False

    def get_config(self, section, option):
        """

        :param section: section name
        :param option: under section option name
        :return:
        """
        config_val = ""
        try:
            if not self.config.has_section(section):
                return config_val
            if not self.config.has_option(section, option):
                return config_val
            config_val = self.config.get(section, option)
        except Exception as e:
            print(e)
            return ''
        return str(config_val).strip()

    def get_config_list(self, section):
        """
        get all configs under section
        :param section: section name
        :return:
        """
        configs = []
        try:
            if self.config.has_section(section):
                configs = self.config.items(section)
        except Exception as e:
            print(e)
        return configs

    def remove_option(self, section, option):
        """
        remove config option
        :param section: section name
        :param option:
        :return:
        """
        try:
            self.config.remove_option(section, option)
            self.config.write(open(self.config_file, "w"))
            return True
        except:
            return False
