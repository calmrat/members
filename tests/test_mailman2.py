#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

from __future__ import unicode_literals
import pytest


def test_raise_exception():
    from members import mailman2 as mm2

    content = ("<h2>Error</h2>"
        "<strong>An example of an Error message.</strong>")

    with pytest.raises(RuntimeError):
        mm2.check_h2(content, 'Error')

def test_download_no_auth():
    from members import mailman2 as mm2

    import urllib2

    user = 'username'
    password = 'password'
    uri = "http://example.com/"

    assert mm2.download(uri, user, None) == urllib2.urlopen(uri).read()
    assert mm2.download(uri, None, password) == urllib2.urlopen(uri).read()
    assert mm2.download(uri, None, None) == urllib2.urlopen(uri).read()

def test_download_auth():
    from members import mailman2 as mm2

    import urllib2
    # which username and password shoud i use in testor should i use it at all?
    user = 'username'
    password = 'password'
    uri = "http://example.com/"

    assert mm2.download(uri, user, password) == urllib2.urlopen(uri).read()

def test_download_auth():
    import urllib2

    from members import mailman2 as mm2
    # which username and password shoud i use in testor should i use it at all?
    user = 'username'
    password = 'password'
    uri = "http://example.com/"

    assert mm2.download(uri, user, password) == urllib2.urlopen(uri).read()

def test_extract():
    from members import mailman2 as mm2
    # should i create here args obj and test extractions with it?
    # or we need to refactor parse_cli() func in the way that 
    # it will take sys.argv as input
    # http://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module
    
    # assert mm2.extract(None)