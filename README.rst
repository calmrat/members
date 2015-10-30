.. image:: https://travis-ci.org/kejbaly2/members.png
   :target: https://travis-ci.org/kejbaly2/members

.. image:: https://coveralls.io/repos/kejbaly2/members/badge.svg
   :target: https://coveralls.io/r/kejbaly2/members


INSTALLATION
============
Example install, using VirtualEnv::

    # install/use python virtual environment
    virtualenv ~/virtenv_scratch --no-site-packages

    # activate the virtual environment
    source ~/virtenv_scratch/bin/activate

    # upgrade pip in the new virtenv
    pip install -U pip setuptools

    # install this package in DEVELOPMENT mode
    python setup.py develop

    # or simply install
    # python setup.py install

CONFIGURATION
=============

Example configuration, eg at `~/.members`::

    mailman2: 
        base_url: http://some.domain.com/mailman2
        lists:
            announce-list: 
                user: bla@bla.com
                password: asdfvi5f211
            memo-list: 
                user: bla@bla.com
                password: dasdf458@1j
            dept-list:

    github:
        user: kejbaly2
        token: FGIOUSODIUGSDGJ
        # password: ********
        user_attrs: [email, bio, url]

    orgchart:
        base_url: http://some.domain.com/orgchart3


USAGE
=====

Mailman2
--------

Example usage, for Mailman2::

    members mailman2 dept-list

Overriding username and password::

    members mailman2 dept-list -u other -p SoM3P@Ss!


OrgChart 3
----------

Example usage, for OrgChart 3::

    members orgchart3 teamlead cward


BUILD DOCS
==========

Example scenario for building docs with sphinx::

    cd docs
    make html


TESTING
=======
Testing is py.test based. Run with::

    py.test tests/ -v


DEVELOPMENT
===========
Install the supplied githooks; eg, ::

    ln -s ~/repos/members/_githooks/commit-msg ~/repos/members/.git/hooks/commit-msg
    ln -s ~/repos/members/_githooks/pre-commit ~/repos/members/.git/hooks/pre-commit
