.. image:: https://travis-ci.org/kejbaly2/members.png
   :target: https://travis-ci.org/kejbaly2/members

.. image:: https://coveralls.io/repos/kejbaly2/members.png 
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

Example configuration::

    mailman2: 
        base_url: http://some.domain.com/mailman2
        lists:
            announce-list: 
                user: cward@redhat.com
                password: asdfvi5f211
            memo-list: 
                user: cward@redhat.com
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

    members mailman2 memo-list -u other -p SoM3P@Ss!


OrgChart 3
----------

Example usage, for OrgChart 3::

    members orgchart3 teamlead cward



TESTING
=======
Testing is py.test based. Run with::

    py.test tests/ -v
