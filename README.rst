Django Event Logger
===================

.. image:: https://travis-ci.org/saanpritom/django_event_logger.svg?branch=dev
    :target: https://travis-ci.org/saanpritom/django_event_logger

Description
-----------

Django Event Logger keeps the log record of any operation on a Django
based application. Such as an user views a page on a Django application
then it may keeps record of the event. Like 'ExampleUser has performed
read operation on ExampleCar at /example/path/ 10 minutes ago'. This is
a dummy log record.

Compatibility
-------------

This package is Tox tested with Python version 3.6, 3.7 and 3.8 with Django
version 2.0, 2.1, 2.2, 3.0, 3.1. However, this package is compatible with
Python version > 3.0 and Django version > 2.0 but not compatible with
Python 2.7 and Django version < 2.0

Installation
------------

Please initialize git at an empty directory. Then add the repository
address to your git remote origin (The master branch as it is the most
tested version).

After downloading create a python virtual environment using virtualenv
or anything you like. This package is tested using only Python3.
However, Python2.7 testing is on the way. After creating the virtualenv
activate it.

Then run

.. code:: python

   pip install -r requirements.txt

to download and install all the required packages.

After successful pip installation open your settings.py file and add
'event_logger', on your INSTALLED_APPS list.

.. code:: python

   INSTALLED_APPS = [
       ...
       'django_event_logger',
   ]

Include the event loggers URLconf in your project urls.py like this::

.. code:: python

   path('django_event_logger/', include('django_event_logger.urls')),

Now run the app migration for creating the databases

.. code:: python

   python manage.py makemigrations
   python manage.py migrate

For Customizing settings there is a directory available for settings.py
file. However, if you do not put the dictionary on the settings.py file
then it will use the default values for the keys.

.. code:: python

   EVENT_LOGGER_SETTINGS = {
       'sensitive_test_cases': True,
       'user_representer_field': '__str__',
       'list_paginated_by': 100,
   }

These are the default values for the keywords.

1. 'sensitive_test_cases' means the package will run some test cases
   that are dependent on a specific environment. Most of the cases these
   tests will not create any error However, if it does then just make it
   False to avoid those test cases running

2. 'user_representer_field' means the default field that will be used to
   construct the full log message for the actor. '**str**' means it is
   pointing to the get_user_model default **str** method. If you want to
   change it then please write the valid name of a user field. Example:
   'user_representer_field': 'email' This will print email as the
   default field for the actor

3. 'list_paginated_by' means the pagination number for the log_list
   page. It is an integer number. Default is 100 but you can put any
   valid integer value

Basic Usage
-----------

This package ships with one Django Mixin for class based views and one
function for function based views. The full example can be found on
examples.py file. However, the examples are explained below:

Function Based Views:
'''''''''''''''''''''

on your views.py file import the following module

.. code:: python

   from event_logger.registrars import create_log_record

and on your function based view just add this method as below

.. code:: python

   def example_function_based_view(request):
       """This example is for the function based view users"""
       target_object = None
       if get_user_model().objects.filter().exists():
           target_object = get_user_model().objects.first()
       create_log_record(request=request, log_detail='event_logger example function view test operation',
                         log_target=target_object)
       return render(request, 'example_templates/example_template.html')

Here the create_log_record() function is taking 3 optional arguments.

1. request (Which is a Django HttpRequest object. If not provide then
   it's default value is None)

2. log_detail (A text describing the action performed on that view by
   the user. If not provided then it's default value is None)

3. log_target (The instance of the page object. Suppose the page is
   showing a Detail view of Books. so the log_target will be the single
   book object. If the page is a list page and there are multiple
   objects or no particular object then just do not use the log_target
   argument. On that case it will use None as the default value. If any
   string, integer or float number has passed to this argument then it
   will raise a ValidationError)

Class Based Views:
''''''''''''''''''

on the views.py file import the following Mixin

.. code:: python

   from event_logger.mixins import EventLoggerMixin

and on any class based views use this mixin as follow:

.. code:: python

   class ExampleViewWithMixin(EventLoggerMixin, TemplateView):
       """This example is for the class based view users"""
       template_name = 'example_templates/example_template.html'
       event_logger_log_detail_message = 'event_logger example class view test operation'

       def get_log_target_object(self, request, *args, **kwargs):
           if get_user_model().objects.filter().exists():
               return get_user_model().objects.first()
           return None

Here two things to notice that the 'event_logger_log_detail_message' and
'get_log_target_object()'

1. 'event_logger_log_detail_message' holds the action message performed
   by the user on this view. If not assign then it will use the default
   None
2. 'get_log_target_object()' this method returns the instance of the
   target object. Same as the log_target on the function based view.
   Just pass this view specific object here. If the page is a list view
   or there are no specific target_object then do not override this
   method. If not overridden the this will use the default value which
   is None


Log Records List
----------------

There are two views for the stored log records of this application. But
one cannot add, update or delete anything on these records through these
views. To add, delete or update a log record the user must have to use
the Django default Admin Panel. Where this app will be found on the name
of 'Event Logger'

1. The default list view can be checked from this URL

  .. code:: python

     https://your-ip-or-domain/event_logger/

  with ?format=table or ?format=file will show table and file formatted
  lists of the logs. For a detail table format view the URL will be
  https://your-ip-or-domain/event_logger/?format=table and for a file
  format view the URL will be
  https://your-ip-or-domain/event_logger/?format=file

2. The default detail view can be checked from this URL

  .. code:: python

     https://your-ip-or-domain/event_logger/3/

  Here 3 is the primary key for that particular log record

Package Creator
---------------

This package is created by Pritom Borogoria. The package is inspired by
`Django Activity Stream`_

.. _Django Activity Stream: https://github.com/justquick/django-activity-stream
