Django User Interaction Log
===========================


Installation
------------

This package can be installed in two ways. One is via the pypi package
manager and other is directly from the Github.

For pypi installation please use the following command

```
    pip install django_user_interaction_log
```

And for directly downloading from the Github repository use the
following commands

```
    git clone https://github.com/saanpritom/django_user_interaction_log.git
```

After successful installation open Django's settings.py file and add
'django\_event\_logger', on your INSTALLED\_APPS list.

```
    INSTALLED_APPS = [
        ...
        'django_user_interaction_log',
    ]
```

Include the event loggers URLconf in your project urls.py like this

```
    path('django_user_interaction_log/', include('django_user_interaction_log.urls')),
```

Here you can put whatever you like on the path. Now run the app
migration for creating the database migrations

```
    python manage.py makemigrations
    python manage.py migrate
```

For Customizing settings there is a directory available for settings.py
file. However, if you do not put the dictionary on the settings.py file
then it will use the default values for the keys.

```
    DJANGO_USER_INTERACTION_LOG_SETTINGS = {
        'sensitive_test_cases': True,
        'user_representer_field': '__str__',
        'list_paginated_by': 100,
    }
```

These are the default values for the keywords.

1.  'sensitive\_test\_cases' means the package will run some test cases
    that are dependent on a specific environment. Most of the cases
    these tests will not create any error However, if it does then just
    make it False to avoid those test cases running
2.  'user\_representer\_field' means the default field that will be used
    to construct the full log message for the actor. '**str**' means it
    is pointing to the get\_user\_model default **str** method. If you
    want to change it then please write the valid name of a user field.
    Example: 'user\_representer\_field': 'email' This will print email
    as the default field for the actor
3.  'list\_paginated\_by' means the pagination number for the log\_list
    page. It is an integer number. Default is 100 but you can put any
    valid integer value

Basic Usage
------------

This package ships with one Django Mixin for class based views and one
function for function based views. The full example can be found on
examples.py file. However, the examples are explained below:

Function Based Views
--------------------

on your views.py file import the following module

```
    from django_user_interaction_log.registrars import create_log_record
```

and on your function based view just add this method as below

```
    def example_function_based_view(request):
        """This example is for the function based view users"""
        target_object = None
        if get_user_model().objects.filter().exists():
            target_object = get_user_model().objects.first()
        create_log_record(request=request, log_detail='django_user_interaction_log example function view test operation',
                          log_target=target_object)
        return render(request, 'example_templates/example_template.html')
```

Here the create\_log\_record() function is taking 3 optional arguments.

1.  request (Which is a Django HttpRequest object. If not provide then
    it's default value is None)
2.  log\_detail (A text describing the action performed on that view by
    the user. If not provided then it's default value is None)
3.  log\_target (The instance of the page object. Suppose the page is
    showing a Detail view of Books. so the log\_target will be the
    single book object. If the page is a list page and there are
    multiple objects or no particular object then just do not use the
    log\_target argument. On that case it will use None as the default
    value. If any string, integer or float number has passed to this
    argument then it will raise a ValidationError)

Class Based Views
-----------------

on the views.py file import the following Mixin

```
    from django_user_interaction_log.mixins import DjangoUserInteractionLogMixin
```

and on any class based views use this mixin as follow:

```
    class ExampleViewWithMixin(DjangoUserInteractionLogMixin, TemplateView):
        """This example is for the class based view users"""
        template_name = 'example_templates/example_template.html'
        django_user_interaction_log_log_detail_message = 'django_user_interaction_log example class view test operation'

        def get_log_target_object(self, request, *args, **kwargs):
            if get_user_model().objects.filter().exists():
                return get_user_model().objects.first()
            return None
```

Here two things to notice that the 'event\_logger\_log\_detail\_message'
and 'get\_log\_target\_object()'

1.  'event\_logger\_log\_detail\_message' holds the action message
    performed by the user on this view. If not assign then it will use
    the default None
2.  'get\_log\_target\_object()' this method returns the instance of the
    target object. Same as the log\_target on the function based view.
    Just pass this view specific object here. If the page is a list view
    or there are no specific target\_object then do not override this
    method. If not overridden the this will use the default value which
    is None

Log Records List
----------------

There are two views for the stored log records of this application. But
one cannot add, update or delete anything on these records through these
views. To add, delete or update a log record the user must have to use
the Django default Admin Panel. Where this app will be found on the name
of 'Event Logger'

1.  The default list view can be checked from this URL

    ```
     https://your-ip-or-domain/django_user_interaction_log/
    ```

    with ```?format=table``` or ```?format=file``` will show table and file formatted
    lists of the logs. For a detail table format view the URL will be
    <https://your-ip-or-domain/django_user_interaction_log/?format=table> and for a file
    format view the URL will be
    <https://your-ip-or-domain/django_user_interaction_log/?format=file>

2.  The default detail view can be checked from this URL
    ```
      https://your-ip-or-domain/django_user_interaction_log/3/
    ```
    Here 3 is the primary key for that particular log record
