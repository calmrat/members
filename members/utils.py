#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

import logging
import os
import subprocess
import sys

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
        args = args or {}
        config = config or {}
        assert isinstance(args, dict)
        assert isinstance(config, dict)
        self._args, self._config = args, config

    def get(self, key, default=None, **kwargs):
        user_value = self._args.get(key) or self._config.get(key)
        if hasattr(default, '__call__'):
            value = user_value or default(**kwargs)
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


def run(cmd):
    cmd = cmd if isinstance(cmd, list) else cmd.split()
    try:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as error:
        logr.error("'{0}' failed: {1}".format(cmd, error))
        raise
    output, errors = process.communicate()
    if process.returncode != 0 or errors:
        if output:
            logr.error(output)
        if errors:
            logr.error(errors)
        sys.exit(process.returncode)
    return output, errors
