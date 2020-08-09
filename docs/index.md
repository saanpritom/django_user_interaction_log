Django Event Logger
===================

[![Build Status](https://travis-ci.org/saanpritom/django_event_logger.svg?branch=master)](https://travis-ci.org/saanpritom/django_event_logger)

[![Coverage](https://coveralls.io/repos/github/saanpritom/django_event_logger/badge.svg?branch=dev)](https://coveralls.io/github/saanpritom/django_event_logger?branch=dev)


Description
-----------

Django Event Logger keeps the log record of any operation on a Django
based application. Such as an user views a page on a Django application
then it may keeps record of the event. Like 'ExampleUser has performed
read operation on ExampleCar at /example/path/ 10 minutes ago'. This is
a dummy log record.

Requirements
------------

This package only needs Django to run.

Version
-------

Current stable version is 1.0

Compatibility
-------------

This package is Tox tested with Python version 3.6, 3.7 and 3.8 with
Django version 2.0, 2.1, 2.2, 3.0, 3.1. However, this package is
compatible with Python version &gt; 3.0 and Django version &gt; 2.0 but
not compatible with Python 2.7 and Django version &lt; 2.0

Package Creator
---------------

This package is created by Pritom Borogoria. The package is inspired by
[Django Activity Stream]: https://github.com/justquick/django-activity-stream
  
