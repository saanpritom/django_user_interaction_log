from django.test import TestCase
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from ..scripts import (get_clean_request_object, get_request_event_path, get_request_user)


class ScriptsFunctionsTestCase(TestCase):
    """This class run TestCases for the functions of scripts.py file"""

    def setUp(self):
        get_request_dict = {}
        get_request_dict['fake_request_object'] = type('test', (object,), {})()
        get_request_dict['empty_request_object'] = HttpRequest()
        request = HttpRequest()
        request = delattr(request, 'path')
        get_request_dict['deleted_path_request_object'] = request
        request = HttpRequest()
        request.path = '/demo/path/23/'
        get_request_dict['request_object_with_path'] = request
        request = HttpRequest()
        test_user_object = get_user_model().objects.create(username='test_user_one', email='test_user_one@example.com', password='superacces123one')
        setattr(request, 'user', test_user_object)
        get_request_dict['request_object_with_valid_user_object'] = request
        request = HttpRequest()
        anon_user = AnonymousUser()
        setattr(request, 'user', anon_user)
        get_request_dict['request_object_with_anon_user_object'] = request
        request = HttpRequest()
        fake_user_object = type('test', (object,), {})()
        setattr(request, 'user', fake_user_object)
        get_request_dict['request_object_with_fake_user_object'] = request
        self.get_request_dict = get_request_dict

    def test_get_clean_request_object(self):
        self.assertEqual(get_clean_request_object(self.get_request_dict['empty_request_object']), self.get_request_dict['empty_request_object'])
        self.assertRaisesMessage(ValidationError, 'request must be a Django HttpRequest object', get_clean_request_object, self.get_request_dict['fake_request_object'])

    def test_get_request_event_path(self):
        self.assertEqual(get_request_event_path(None), None)
        self.assertEqual(get_request_event_path(self.get_request_dict['empty_request_object']), None)
        self.assertEqual(get_request_event_path(self.get_request_dict['deleted_path_request_object']), None)
        self.assertEqual(get_request_event_path(self.get_request_dict['request_object_with_path']), '/demo/path/23/')
        self.assertRaisesMessage(ValidationError, 'request must be a Django HttpRequest object', get_request_event_path, self.get_request_dict['fake_request_object'])

    def test_get_request_user(self):
        self.assertEqual(get_request_user(None), None)
        self.assertEqual(get_request_user(self.get_request_dict['empty_request_object']), None)
        self.assertRaisesMessage(ValidationError, 'request must be a Django HttpRequest object', get_request_user, self.get_request_dict['fake_request_object'])
        self.assertEqual(get_request_user(self.get_request_dict['request_object_with_anon_user_object']), None)
        self.assertEqual(get_request_user(self.get_request_dict['request_object_with_valid_user_object']), get_user_model().objects.first())
        self.assertRaisesMessage(ValidationError, 'The request.user object seems to be tempered', get_request_user, self.get_request_dict['request_object_with_fake_user_object'])
