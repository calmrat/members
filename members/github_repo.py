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

logr = logging.getLogger(__name__)

# List of Github API calls available
TARGETS = {
    'collaborators': lambda x: x.get_collaborators(),
    'assignees': lambda x: x.get_assignees(),
    'contributors': lambda x: x.get_contributors(),
    'stargazers': lambda x: x.get_stargazers(),
    'teams': lambda x: x.get_teams(),
    'watchers': lambda x: x.get_watchers(),
}


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

    # 'login' will be the dict index key; remove it from user_attr columns
    if 'login' in user_attrs:
        if user_attrs.index('login') >= 0:
            # get this out of the remaining attrs to parse
            del user_attrs[user_attrs.index('login')]

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


def extract(repo_url=None, target=None, user=None, password=None, token=None,
            user_attrs=None):
    '''
    FIXME: DOCS...
    '''
    if not repo_url:
        raise RuntimeError("URI must be specified")

    if target not in TARGETS.keys():
        raise RuntimeError("Unknown members target [{}]".format(target))

    # eg, login, email; user.ATTR to return as ['member', 'member', ... ']
    user_attrs = user_attrs or []
    # user_attrs can be a list (of strings) or a string
    assert isinstance(user_attrs, (unicode, str, list))
    # if we get a string, put convert it to a single item list
    if isinstance(user_attrs, (unicode, str)):
        user_attrs = [user_attrs]
    # Should only have a list at this point... empty or with strings
    assert isinstance(user_attrs, list)
    logr.debug("user_attrs: {}".format(user_attrs))

    # use token if available, otherwise, password
    if token:
        logr.debug(" ... USING AUTH TOKEN")
        password = token
    else:
        assert password != ''  # is not null

    if user and password:
        logr.debug("AUTHENTICATING USER (WITH PASSOWRD): {}".format(user))
        g = Github(user, password)
    else:
        if user:
            logr.debug("NOT AUTHENTICATING USER: {}".format(user))
        else:
            logr.debug("NO USER / PASSWORD set")
        g = Github()

    repo = g.get_repo(repo_url)

    # run the github api call for members depending on requested target
    users = TARGETS[target](repo)

    members = _logins(users=users, user_attrs=user_attrs)

    return members
