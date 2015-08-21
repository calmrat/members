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


@pytest.mark.xfail(reason="URLError")
def test_extract():
    import urllib2
    import re

    from members import mailman2 as mm2

    args = {}
    args['user'] = "username"
    args['password'] = "password"

    config = {}
    config['lists'] = {}
    config['lists']['qe-dept-list'] = {}

    with pytest.raises(RuntimeError):
        mm2.extract(args, config)

    args['base_url'] = "http://post-office.corp.redhat.com/mailman"
    args['list_name'] = "qe-dept-list"

    list_url = "{}/roster/{}".format(args['base_url'], args['list_name'])
    content = urllib2.urlopen(list_url).read()

    users = re.findall(r'(?<=--at--redhat\.com">)(?<=>).*(?=<\/a>)', content)
    users = ['@'.join(user.split(' at ')) for user in users]

    assert mm2.extract(args, config) == users
