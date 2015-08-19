#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

from instructions import commands, datatypes
import pytest

TEST_REPO = 'kejbaly2/members'


# MAKE THIS SO IT ONLY EVER GETS RUN ONCE PER "SESSION"
def test_global_import():
    from members import github_repo  # NOQA: W0611; only import


def repo_no_auth(args=None):
    '''
    'anonymous' user; no user/pass set
    '''
    args = args or {}
    args["user"] = None
    args["password"] = None
    args["uri"] = TEST_REPO
    return args

@pytest.mark.xfail(reason="GithubException")
def test_default_auth_good():
    from members import github_repo as repo

    # DEFAULT AUTH should be 'anonymous'; no user/pass required
    args = repo_no_auth()
    # assignees should not require authenticated user to call
    args['who'] = 'assignees'
    users = repo.extract(args=args, config=None)

    # see: https://github.com/maxtepkeev/instructions
    # see: http://bit.ly/maxtepkeev_instructions_eupy15
    result = commands.count(datatypes.string).inside(users)
    if not result >= 1:
        raise RuntimeError(
            "Expeted more than one assignee, got {}".format(result))

    # contributors should not require authenticated user to call
    args['who'] = 'contributors'
    users = repo.extract(args=args, config=None)


def test_default_auth_bad():
    from members import github_repo as repo

    # DEFAULT AUTH should be 'anonymous'; no user/pass required
    args = repo_no_auth()
    # collaborators SHOULD require auth
    args['who'] = 'collaborators'
    try:
        repo.extract(args=args)
    # FIXME: check for specific github exception too.
    except Exception as e:
        print('EXPECTED GITHUB EXCEPTION, got {}. IGNORING!'.format(e))
    else:
        raise RuntimeError("EXPECTED EXCEPTION, didn't get one though... oops")
