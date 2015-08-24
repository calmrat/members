===========
STYLE GUIDE
===========

Python
======
Read and understand `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_.  
WARNING: Your code might be rejected if any of the following report back errors!

 * `flake8 <https://pypi.python.org/pypi/flake8>`_

Use vim? Install `python-mode <https://github.com/klen/python-mode>`_


Highlights
----------
Wrap margins at 79. No lines in any `*.py` (or other text file) file 
should ever be longer than 79c, even long strings! There are techniques 
for shortening lines so they are readable at 79c; learn them and be creative.

Capitalize Classes. Lowercase everything else and separate words by 
underscore `_`.

Use leading underscore to indicate 'private' or 'local scope only'.


GIT REPO
========

Commit Message
--------------
See: `How to write a GIT Commit <http://chris.beams.io/posts/git-commit/>`_

Commit message *subject* line length should be no more than 50c! Anything 
longer means you are trying to make to many changes in a single commit.

A properly formed git commit subject line should always be able to 
complete the following sentence::

    If applied, this commit will [your subject line here]

Details go into the commit *body*. Here are some more hints::

    **Separate subject from body with a blank line**
    Capitalize the subject line
    Do not end the subject line with a period
    Use the imperative mood in the subject line
    Wrap the body at 72 characters
    Use the body to explain what and why vs. how

For example::

    Summarize changes in around 50 characters or less

    More detailed explanatory text, if necessary. Wrap it to about 72
    characters or so. In some contexts, the first line is treated as the
    subject of the commit and the rest of the text as the body. The
    blank line separating the summary from the body is critical (unless
    you omit the body entirely); various tools like `log`, `shortlog`
    and `rebase` can get confused if you run the two together.

    Explain the problem that this commit is solving. Focus on why you
    are making this change as opposed to how (the code explains that).
    Are there side effects or other unintuitive consequenses of this
    change? Here's the place to explain them.

    Further paragraphs come after blank lines.

     - Bullet points are okay, too

     - Typically a hyphen or asterisk is used for the bullet, preceded
       by a single space, with blank lines in between, but conventions
       vary here

     If you use an issue tracker, put references to them at the bottom,
     like this:

     Resolves: #123
     See also: #456, #789

Versioning
----------
A simple X.Y.Z[a] schema will be used. With 'Z' being equivalent to 'release'.

Branching
---------
By default branch from and rebase/merge your branches with master unless
the code is a backport, fix or feature for a previously release version.

Prepend "grouping" tokens in front of your branch names. For example::

    feat: feature
    bug:  bug or defect
    wip:  experiment, work in progress
    junk: tmp, safe to throw-away **anytime**

Do not use bare numbers (or hex numbers) as part of your branch naming scheme.
GIT might interpret the numbers as part of a sha-1 instead of a branch name
dring TAB-expansion.

Avoid long descriptive names for long-lived branches.

Use **dashes** to separate parts of your branch names.

New 'version' branches will be created once a release has been deployed. In
the case you are developing something for a specific (released) version,
prepend the version to the branch name, eg: 0.0.1-new-feature; 0.1.5-bug-fix.

Otherwise, by default, just use a short, descriptive name.

More, see: 
`GIT branch naming best practices <http://stackoverflow.com/a/6065944>`_
Even more, see: 
`A successful GIT branching model <http://nvie.com/posts/a-successful-git-branching-model/>`_
