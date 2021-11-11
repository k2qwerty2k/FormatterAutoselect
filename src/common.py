#!/usr/bin/env python3

import os
from os.path import (abspath, basename, expanduser, expandvars, isdir,
                     isfile, join, normpath, pathsep, split, splitext)
import sys
from imp import reload
import logging
import sublime

log = logging.getLogger('root')
IS_WINDOWS = sublime.platform() == 'windows'
PLUGIN_NAME = 'FormatterAutoselect'

def settings():
    base_name = PLUGIN_NAME + '.sublime-settings'
    prefs = sublime.load_settings(base_name)
    if prefs:
        return prefs
    log.error('Could not load settings file: %s', base_name)
    return None

def setup_logger(name):
    formatter = logging.Formatter(fmt='▋[' + PLUGIN_NAME + '](%(threadName)s:%(filename)s#L%(lineno)s): [%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    return logger

