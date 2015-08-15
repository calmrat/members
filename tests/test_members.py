#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

from __future__ import unicode_literals


def test_version_check():
    from members import _version

    ######################################################
    # THIS NEEDS TO BE UPDATED EVERY TIME THE MAIN PACKAGE
    # VERSION IS UPDATED!!!
    ######################################################
    # expected
    # version_info = ('0', '0', '2')
    # __version__ = '.'.join(version_info[0:3])
    _v = '0.0.2'

    if _version.__version__ != _v:
        raise SystemError('SYNC VERSION in tests/test_members.py')


# MAKE THIS SO IT ONLY EVER GETS RUN ONCE PER "SESSION"
def test_global_import():
    import members  # NOQA: W0611; only import
