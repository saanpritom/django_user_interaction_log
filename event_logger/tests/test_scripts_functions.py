from django.test import TestCase
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from ..scripts import get_request_event_path


class ScriptsFunctionsTestCase(TestCase):
    """This class run TestCases for the functions of scripts.py file"""

    def setUp(self):
        get_request_event_path_dict = {}
        get_request_event_path_dict['fake_request_object'] = type('test', (object,), {})()
        get_request_event_path_dict['empty_request_object'] = HttpRequest()
        request = HttpRequest()
        request = delattr(request, 'path')
        get_request_event_path_dict['deleted_path_request_object'] = request
        request = HttpRequest()
        request.path = '/demo/path/23/'
        get_request_event_path_dict['request_object_with_path'] = request
        self.get_request_event_path_dict = get_request_event_path_dict

    def test_get_request_event_path(self):
        self.assertEqual(get_request_event_path(None), None)
        self.assertEqual(get_request_event_path(self.get_request_event_path_dict['empty_request_object']), None)
        self.assertEqual(get_request_event_path(self.get_request_event_path_dict['deleted_path_request_object']), None)
        self.assertEqual(get_request_event_path(self.get_request_event_path_dict['request_object_with_path']), '/demo/path/23/')
        self.assertRaisesMessage(ValidationError, 'request must be a Django HttpRequest object', get_request_event_path, self.get_request_event_path_dict['fake_request_object'])
