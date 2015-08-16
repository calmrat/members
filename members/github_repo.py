#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: "Chris Ward" <cward@redhat.com>

'''
Github API repo membership
'''

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

from getpass import getuser
import logging

from github import Github

logr = logging.getLogger(__name__)


# FIXME: move to (auth) utils
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


# FIXME: Add to utils
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


def _logins(users, attr=None):
    '''
    FIXME: DOCS...
    '''
    ATTRS = {
        'login': lambda x: x.login,
        'email': lambda x: x.email,
    }

    attr = attr or 'login'
    attr_fun = ATTRS[attr]
    users = [attr_fun(u) for u in users]
    return users


def extract(args=None, config=None):
    '''
    FIXME: DOCS...
    '''
    args, config = args or {}, config or {}
    sargs = StandardArgs(args, config)
    user = sargs.user

    # eg, login, email; user.ATTR to return as ['member', 'member', ... ']
    user_attr = args.get('user_attr')

    # use token if available, otherwise, password
    if 'token' in config:
        logr.debug(" ... FOUND AUTH TOKEN")
        password = config.get('token')
    else:
        password = sargs.password

    if user and password:
        logr.debug("AUTHENTICATING USER: {}".format(user))
        g = Github(user, password)
    else:
        if user:
            logr.debug("NOT AUTHENTICATING USER: {}".format(user))
        else:
            logr.debug("NO USER / PASSWORD set")
        g = Github()

    uri = args.get('uri')
    if not uri:
        raise RuntimeError("URI must be specified")
    repo = g.get_repo(uri)

    members = ''

    # DEFAULT to contributors if who isn't set to avoid an error
    # contributors shouldn't require authentication
    who = args.get('who', 'contributors')

    # List of Github API calls available
    WHO = {
        'collaborators': lambda x: x.get_collaborators(),
        'assignees': lambda x: x.get_assignees(),
        'contributors': lambda x: x.get_contributors(),
        'stargazers': lambda x: x.get_stargazers(),
        'teams': lambda x: x.get_teams(),
        'watchers': lambda x: x.get_watchers(),
    }

    if not who in WHO.keys():
        raise RuntimeError("Unknown members target [{}]".format(who))

    caller = WHO[who]
    members = _logins(users=caller(repo), attr=user_attr)

    return members
