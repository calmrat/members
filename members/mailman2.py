#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Eduard Trott" <etrott@redhat.com>

from __future__ import unicode_literals

import logging
import re
import sys
import urllib2
import cookielib

import ClientForm


# load the root logger if it exists; or use the default if not already created
logging.basicConfig()
logr = logging.getLogger(__name__)


def check_h2(content, search_str):
    if re.search(r'<h2>{}<\/h2>'.format(search_str), content):
        err = re.findall(r'(?<=<strong>).*(?=<\/strong>)', content)[0]
        logr.error(err)
        raise RuntimeError


def auth(list_link, user, password):
    logr.debug('AUTH {}:{}'.format(user, list_link))
    cookieJar = cookielib.CookieJar()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible)")]
    urllib2.install_opener(opener)
    forms = ClientForm.ParseResponse(
        urllib2.urlopen(list_link), backwards_compat=False)
    form = forms[2]
    form['roster-email'] = user
    form['roster-pw'] = password
    try:
        fp = urllib2.urlopen(form.click())
        content = fp.read()
        check_h2(content, 'Error')
    finally:
        fp.close()


def extract(args, config=None):

    base_url = args.get('base_url') or config.get('base_url')
    list_name = args.get('list_name')

    lists = config.get('lists') or {}
    list_config = lists.get(list_name) or {}
    list_user = args.get('user') or list_config.get('user')
    list_password = args.get('password') or list_config.get('password')

    logr.debug(
        '[{}] {}: {}'.format(base_url, list_name, list_user))

    if not base_url and list_name:
        raise RuntimeError(
            "base_url [{}] and list_name [{}] can not be NULL".format(
                base_url, list_name))

    list_link = "{}/listinfo/{}".format(base_url, list_name)
    list_members_link = "{}/roster/{}".format(base_url, list_name)

    if list_user and list_password:
        # auth is specified, use it
        auth(list_link, list_user, list_password)
        content = urllib2.urlopen(list_members_link).read()
    else:
        # if anyone can access to the list of members
        content = urllib2.urlopen(list_members_link).read()

    check_h2(content, 'Error')

    # source contain list members page content
    list_members = re.findall(r'(?<=--at--redhat\.com">)(?<=>).*(?=<\/a>)', content)

    users = ['@'.join(mail.split(' at ')) for mail in list_members]

    return users
