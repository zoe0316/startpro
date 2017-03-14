# encoding: utf-8

"""
Created on 2014.04.21

@author: Allen
"""
import os

COMMAND_MODEULE = 'startpro.core.commands'

SCRIPT_MODULE = ''

# PROGRAM BASE INFO
VERSION = ''
NAME = 'Unknown'
DESCRIPTION = ''

# RUNNING CONFIGURE
CONFIG = None
ROOT_PATH = ''
CLIENT_FILE = 'client_file'
RESULT_FILE = 'result_file'
CONFIG_FILE = 'config.ini'

# MAIN PATH CONFIGURE
MAIN_PATH = "startpro"
MAIN_PY = 'startpro.py'
MAIN_SETTING = os.path.join('core', 'settings.py')
MAIN_CONFIG = "startpro.cfg"

# TEMPLATE FILE
TEMPLATE = "template"
TEMPLATE_PACKAGE = os.path.join(TEMPLATE, "package.py")

# LOAD PATHS
LOAD_PATHS = '#LOAD_PATHS#'

# TAMP FILE
SCRIPT_TEMP = '.scripts.tmp'
