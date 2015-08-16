#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

import logging
import os
import re

# INTERNAL PYTHON MODULES
import argparse

# EXTERNALLY INSTALLED
import yaml

# Load logging before anything else
logging.basicConfig(format='>> %(message)s')
logr = logging.getLogger('members')

''' Load the config file so modules can import and reuse '''
CONFIG_FILE = os.path.expanduser('~/.members')
with open(CONFIG_FILE) as _:
    config = yaml.load(_)


def exclude(users, exclude):
    users = users or []
    exclude = exclude or []

    if not exclude:
        return users

    # expecting 1+ patterns to match against
    ex_res = [re.compile(x) for x in exclude]

    excluded = set()
    for u in users:
        for pattern in ex_res:
            if pattern.search(u):
                excluded.add(u)

    users = set(users) - excluded
    logr.debug("{} members EXCLUDED".format(len(excluded)))
    return list(users)


def parse_cli():
    '''
    members "public" CLI API
    '''
    # Setup the argparser
    parser = argparse.ArgumentParser(
        description='Get list of members from various data sources')
    subparsers = parser.add_subparsers(help='Datasources', dest='src')

    parser.add_argument('-o', metavar='o', nargs='?',
                        dest='output', help='Output file')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="turn verbose logging ON")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="turn debug logging ON")
    # FIXME SUPPORT excluding users from the final list before printing
    parser.add_argument('-x', '--exclude', metavar='USER', nargs='+',
                        help="exclude results users by pattern")

    # Mailman 2
    mm2 = subparsers.add_parser('mailman2')
    mm2.add_argument('list_name', metavar='S',
                     help='Mailman 2 list name')
    mm2.add_argument('-B', '--base-url', metavar='URL',
                     help='URL to Mailman2 list-serve')
    mm2.add_argument('-u', '--user', metavar='USER',
                     help='Username to login with')
    mm2.add_argument('-p', '--password', metavar='PASS',
                     help='Password to login with')

    # Orgchart 3
    # SUPPORTS KERBEROS LOGIN ONLY FOR NOW
    oc3 = subparsers.add_parser('orgchart3')
    # FIXME: support by group
    oc3.add_argument('type', metavar='TYPE', choices=['teamlead'],
                     help='Orgchart3 grouping type')
    oc3.add_argument('name', metavar='NAME',
                     help='Orgchart3 type name (eg, team x)')
    # oc3.add_argument('-f', '--filter', metavar='FILTER', choices=['location']
    #                 help='Orgchart3 member filters')
    oc3.add_argument('-B', '--base-url', metavar='URL',
                     help='URL to Mailman2 list-serve')
    oc3.add_argument('-NDED', '--no-default-email-domain', action='store_true',
                     help="don't append default email to usernames")
    oc3.add_argument('-DED', '--default-email-domain',
                     help="default email domain (eg: @example.com)")

    # Github API - Github repo members
    g = subparsers.add_parser('github_repo')
    g.add_argument('uri',
                   help='Github "[user|group]/repo" resource uri')
    g.add_argument('who',
                   choices=['collaborators', 'assignees', 'contributors',
                            'stargazers', 'teams', 'watchers'],
                   help='Github repository name')
    g.add_argument('user_attr',
                   nargs='?',
                   choices=['email', 'login'],
                   default='email',
                   help='Github User attribute (default: email)')

    args = vars(parser.parse_args())  # parse and load args as a dict
    return args
