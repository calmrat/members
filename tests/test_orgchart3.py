#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

from __future__ import unicode_literals


def test_global_import():
    from members import orgchart3 as oc3  # NOQA: W0611; only import


def test_GET_ARGS_DEFAULTS():
    # IMPORT FROM FIXTURE
    from members import orgchart3 as oc3

    _GET_ARGS = {
        'direct': 'true',
        'indirect': 'true',
        'kerberos': 'true',
        'location': 'true',
        'realname': 'false',
        'product_role': 'true',  # Product / Role
        'manager': 'false',
        'functional': 'false',
        'group': 'true',  # Group
        'email': 'true',  # Email
        'start': 'true',  # Hire Date
        'type': 'true',   # Empoyee Type
        'costcenter': 'true',  # Cost Center
        'organization': 'true',  # Organization
        'title': 'false',
        'tag': 'false',
    }

    if oc3.GET_ARGS != _GET_ARGS:
        raise SystemError('SYNC GET_ARGS in test_orgchart3.py')
