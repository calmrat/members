#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

from getpass import getuser
import logging
import os

# EXTERNALLY INSTALLED
import yaml

# Load logging before anything else
logging.basicConfig(format='>> %(message)s')
logr = logging.getLogger('members')

''' Load the config file so modules can import and reuse '''
CONFIG_FILE = os.path.expanduser('~/.members')
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as _:
        config = yaml.load(_)
else:
    config = {}


class StandardArgs(object):
    '''
    FIXME: DOCS...
    '''
    uid = None
    password = None
    base_url = None

    def __init__(self, args=None, config=None):
        '''
        FIXME: DOCS...
        '''
        self._args, self._config = args or {}, config or {}
        logr.debug('CREATING STANDARD ARGS')
        logr.debug(' ... args: {}'.format(args))
        logr.debug(' ... config: {}'.format(config))
        self.user = self.get('user', getuser())
        self.password = self.get('password')
        self.base_url = self.get('base_url')
        self.kind = self.get('kind')

    def get(self, key, default=None):
        user_value = self._args.get(key) or self._config.get(key)
        if hasattr(default, '__call__'):
            value = user_value or default()
        else:
            value = user_value or default
        return value


def request_password(user=None):
    user = user or ''
    # http://stackoverflow.com/a/27293138/1289080
    try:
        input = raw_input
    except NameError:  # Python 3
        pass
    #############################################

    password = input('[{}] password: '.format(user))
    return password
