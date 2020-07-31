Django Event Logger
=======

Description
-----------

Django Event Logger keeps the log record of any operation on a Django based application. Such as an user views a
page on a Django application then it may keeps record of the event. Like 'ExampleUser has performed read operation
on ExampleCar at /example/path/ 10 minutes ago'. This is a dummy log record.

Installation
------------

Please initialize git at an empty directory. Then add the repository address to your git remote origin (The master branch as it is the most tested version).

After downloading create a python virtual environment using virtualenv or anything you like. This package is tested
using only Python3. However, Python2.7 testing is on the way. After creating the virtualenv activate it.

Then run pip install -r requirements.txt to download and install all the required packages.

After successful pip installation open your settings.py file and 'event_logger', on your INSTALLED_APPS list.

For Customizing settings there is a directory available for settings.py file. However, if you do not put the dictionary
on the settings.py file then it will use the default values for the keys.

EVENT_LOGGER_SETTINGS = {
    'sensitive_test_cases': True,
    'user_representer_field': '__str__',
    'list_paginated_by': 100,
}

These are the default values for the keywords.

'sensitive_test_cases' means the package will run some test cases that are dependent on a specific environment. Most of the cases these tests will not create any error However, if
it does then just make it False to avoid those test cases running

'user_representer_field' means the default field that will be used to construct the full log message for the actor.
'__str__' means it is pointing to the get_user_model default __str__ method. If you want to change it then please
write the valid name of a user field.
Example: 'user_representer_field': 'email' This will print email as the default field for the actor

'list_paginated_by' means the pagination number for the log_list page. It is an integer number. Default is 100 but
you can put any valid integer value


Basic Usage
-----------

This package ships with
