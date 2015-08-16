#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: "Chris Ward" <cward@redhat.com>

'''
Github API repo membership
'''

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

import logging

from github import Github

from members.utils import StandardArgs

logr = logging.getLogger(__name__)


def _logins(users, user_attrs=None):
    '''
    FIXME: DOCS...
    '''
    # FIXME: check for support attrs
    # Supported attrs:
    # login  # DEFAULT, no auth required
    # email
    # bio
    # company
    # created_at
    # hireable
    # location
    # updated_at
    # url

    _users = {}
    for u in users:
        l = u.login
        logr.debug('LOGIN: {}'.format(l))
        _users[l] = {}
        for a in user_attrs:
            logr.debug('user: {}'.format(u))
            logr.debug('attr: {}'.format(a))
            _users[l][a] = getattr(u, a)
    return _users


def extract(args=None, config=None):
    '''
    FIXME: DOCS...
    '''
    args, config = args or {}, config or {}
    sargs = StandardArgs(args, config)
    user = sargs.user

    # eg, login, email; user.ATTR to return as ['member', 'member', ... ']
    user_attrs = args.get('user_attrs') or []
    if not isinstance(user_attrs, list):
        user_attrs = [user_attrs]

    # SPECIAL CASE - Always get logins
    if 'login' in user_attrs:
        if user_attrs.index('login') >= 0:
            # get this out of the remaining attrs to parse
            del user_attrs[user_attrs.index('login')]

    if not user_attrs:
        user_attrs = config.get('user_attrs') or []

    logr.debug("user_attrs: {}".format(user_attrs))

    # use token if available, otherwise, password
    if 'token' in config:
        logr.debug(" ... FOUND AUTH TOKEN")
        password = config.get('token')
    else:
        password = sargs.password

    if user and password:
        logr.debug("AUTHENTICATING USER (WITH PASSOWRD): {}".format(user))
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
    who = args.get('who', 'assignees')

    # List of Github API calls available
    WHO = {
        'collaborators': lambda x: x.get_collaborators(),
        'assignees': lambda x: x.get_assignees(),
        'contributors': lambda x: x.get_contributors(),
        'stargazers': lambda x: x.get_stargazers(),
        'teams': lambda x: x.get_teams(),
        'watchers': lambda x: x.get_watchers(),
    }

    if who not in WHO.keys():
        raise RuntimeError("Unknown members target [{}]".format(who))

    users = WHO[who](repo)
    members = _logins(users=users, user_attrs=user_attrs)

    return members
