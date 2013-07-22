Referee - keeping track of contest data
============

Models to help with managing contests in Django

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    $ pip install django-referee

To get the latest commit from GitHub

.. code-block:: bash

    $ pip install -e git+git://github.com/gaqzi/django-referee.git#egg=referee

TODO: Describe further installation steps (edit / remove the examples below):

Add ``referee`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'referee',
    )

Add the ``referee`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^referee/', include('referee.urls')),
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate referee


Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-referee
    $ python setup.py install
    $ pip install -r dev_requirements.txt

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send us a pull request for your feature branch
