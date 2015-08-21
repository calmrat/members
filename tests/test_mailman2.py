#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Eduard Trott" <etrott@redhat.com>

from __future__ import unicode_literals
import pytest


def test_global_import():
    from members import mailman2 as mm2  # NOQA: W0611 'imported but unused'


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

    assert mm2._download(uri, user, None) == urllib2.urlopen(uri).read()
    assert mm2._download(uri, None, password) == urllib2.urlopen(uri).read()
    assert mm2._download(uri, None, None) == urllib2.urlopen(uri).read()


def test_download_auth():
    from members import mailman2 as mm2

    import urllib2
    # which username and password shoud i use in testor should i use it at all?
    user = 'username'
    password = 'password'
    uri = "http://example.com/"

    assert mm2._download(uri, user, password) == urllib2.urlopen(uri).read()


def test_extract():
    import urllib2
    import re

    from members import mailman2 as mm2

    base_url = "http://mailman.ijs.si/mailman"
    list_name = 'mailman'

    # null value for either base_url or list_name raises RuntimeError
    not_a_url = None
    with pytest.raises(RuntimeError):
        mm2.extract(list_name=list_name, base_url=not_a_url)

    # null value for either base_url or list_name raises RuntimeError
    not_a_name = None
    with pytest.raises(RuntimeError):
        mm2.extract(list_name=not_a_name, base_url=base_url)

    # Check that an invalid url raises ValueError
    not_a_url = 'NOT A URL'
    with pytest.raises(ValueError):
        mm2.extract(list_name=list_name, base_url=not_a_url)

    list_url = "{}/roster/{}".format(base_url, list_name)
    content = urllib2.urlopen(list_url).read()

    users = re.findall(r'(?<=>)(\S* at \S*|\S*@\S*)(?=<\/a>)', content)
    users = ['@'.join(u.split(' at ')) if ' at ' in u else u
             for u in users]

    assert mm2.extract(list_name=list_name, base_url=base_url) == users
