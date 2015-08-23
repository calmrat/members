#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: "Chris Ward" <cward@redhat.com>

'''
Invoke Project Tasks
'''

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

import logging

from invoke import run, task

logging.basicConfig()
logr = logging.getLogger()
logr.setLevel(logging.INFO)


@task
def clean(docs=False, bytecode=True, extra=''):
    logr.info('>> CLEAN')
    patterns = ['build']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
        patterns.append('*.pyc')
    if extra:
        patterns.append(extra)
    logr.info(' ... [{}]'.format(', '.join(patterns)))
    for pattern in patterns:
        run("rm -rf %s" % pattern)


@task
def build(docs=False):
    run("python setup.py build")
    if docs:
        run("sphinx-build docs docs/_build")


@task
def deploy():
        run("python setup.py sdist upload")
