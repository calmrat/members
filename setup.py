#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: "Chris Ward" <cward@redhat.com>

# PY3 COMPAT
# BUG unicode_literals breaks disutils
# python-2.7 setup.py build
# "'package' must be a string (dot-separated), list, or tuple")
# python3 works
from __future__ import absolute_import  # , unicode_literals

from setuptools import setup

VERSION_FILE = "members/_version.py"
VERSION_EXEC = ''.join(open(VERSION_FILE).readlines())
__version__ = ''
exec(VERSION_EXEC)  # update __version__
if not __version__:
    raise RuntimeError("Unable to find version string in %s." % VERSION_FILE)

# acceptable version schema: major.minor[.patch][-sub[ab]]
__pkg__ = 'members'
__pkgdir__ = {'members': 'members'}
__pkgs__ = ['members', ]
__provides__ = ['members']
__desc__ = 'Get membership details from various data sources.'
__scripts__ = ['bin/members']
__irequires__ = [
    # CORE DEPENDENCIES
    'functioncache==0.92',
    'argparse==1.3.0',
    'pyyaml==3.11',
    'requests==2.7.0',
    'requests-kerberos==0.7.0',  # FIXME: no hard dep; orgchart3 only
    'pandas==0.16.2',  # FIXME: shouldn't be a hard dep; orgchart3 only
]
__xrequires__ = {
    'tests': [
        'pytest==2.7.2',
        'instructions',
        'pytest-pep8==1.0.6',  # run with `py.test --pep8 ...`
    ],
    'docs': ['sphinx==1.3.1', ],
    'github': ['PyGithub==1.25.2', ],
    'invoke': ['invoke==0.10.1', ],

}

pip_src = 'https://pypi.python.org/packages/src'
__deplinks__ = []

# README is in the parent directory
readme_pth = 'README.rst'
with open(readme_pth) as _file:
    readme = _file.read()

github = 'https://github.com/kejbaly2/members'
download_url = '%s/archive/master.zip' % github

default_setup = dict(
    url=github,
    license='GPLv3',
    author='Eduard Trott',
    author_email='etrott@redhat.com',
    maintainer='Chris Ward',
    maintainer_email='cward@redhat.com',
    download_url=download_url,
    long_description=readme,
    data_files=[],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
        'Topic :: Utilities',
    ],
    keywords=['information'],
    dependency_links=__deplinks__,
    description=__desc__,
    install_requires=__irequires__,
    extras_require=__xrequires__,
    name=__pkg__,
    package_dir=__pkgdir__,
    packages=__pkgs__,
    provides=__provides__,
    scripts=__scripts__,
    version=__version__,
    zip_safe=False,  # we reference __file__; see [1]
)

setup(**default_setup)
