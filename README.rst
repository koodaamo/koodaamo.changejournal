.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

======================
koodaamo.changejournal
======================

Manage access timestamps and a journal of changes.

Features
--------

- Provides access timestamps
- Provides a journal of changes


Usage
--------

Prepare your content for timestamped access:

- assign IPortalAccessTimestamped for the content

Prepare your content for tracking:

- assign IPortalChangeJournaled to the content to be tracked
- implement a IJournaledRecordGenerator adapter that adapts the
  content to prodvidee a data records iterator


Installation
------------

Install koodaamo.changejournal by adding it to your buildout::

    [buildout]

    ...

    eggs =
        koodaamo.changejournal


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/koodaamo.changejournal/issues
- Source Code: https://github.com/collective/koodaamo.changejournal
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
