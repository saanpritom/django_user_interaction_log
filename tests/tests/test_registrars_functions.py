from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_event_logger.registrars import create_log_record


class RegistrarsTestCase(TestCase):
    """This class tests the functions on registrars.py file"""

    def setUp(self):
        self.test_create_log_record_dict = {}
        request = HttpRequest()
        request.path = '/test/request/path/'
        test_user_one = get_user_model().objects.create(username='test_user_one', email='test_user_one@example.com', password='superacces123one')
        test_user_two = get_user_model().objects.create(username='test_user_two', email='test_user_two@example.com', password='superacces123two')
        setattr(request, 'user', test_user_one)
        self.test_create_log_record_dict['empty_log_record'] = create_log_record()
        self.test_create_log_record_dict['full_log_record'] = create_log_record(request, 'read operation', test_user_two)

    def test_create_log_record_empty(self):
        test_object = self.test_create_log_record_dict['empty_log_record']
        self.assertEqual(test_object.id, 1)
        self.assertEqual(test_object.user_content_type, None)
        self.assertEqual(test_object.user_object_id, '0')
        self.assertEqual(test_object.log_user, None)
        self.assertEqual(test_object.log_detail, 'no specified operation')
        self.assertEqual(test_object.target_content_type, None)
        self.assertEqual(test_object.target_object_id, None)
        self.assertEqual(test_object.log_target, None)
        self.assertEqual(test_object.event_path, 'n/a')
        self.assertEqual(str(test_object), '1. Anonymous performed no specified operation at n/a ' + str(test_object.get_timesince()) + ' ago')
        self.assertEqual(test_object.is_user_anonymous(), True)
        self.assertEqual(test_object.get_user_representer(), 'Anonymous')
        self.assertEqual(test_object.get_user_object_absolute_url(), '#')
        self.assertEqual(test_object.get_target_object_absolute_url(), '#')

    def test_create_log_record_full(self):
        test_object = self.test_create_log_record_dict['full_log_record']
        self.assertEqual(test_object.id, 2)
        self.assertEqual(test_object.user_object_id, get_user_model().objects.get(username='test_user_one').id)
        self.assertEqual(test_object.log_user, get_user_model().objects.get(username='test_user_one'))
        self.assertEqual(test_object.log_detail, 'read operation')
        self.assertNotEqual(test_object.target_content_type, None)
        self.assertEqual(test_object.target_object_id, get_user_model().objects.get(username='test_user_two').id)
        self.assertEqual(test_object.log_target, get_user_model().objects.get(username='test_user_two'))
        self.assertEqual(test_object.event_path, '/test/request/path/')
        self.assertEqual(str(test_object), '2. test_user_one performed read operation on test_user_two at /test/request/path/ ' + str(test_object.get_timesince()) + ' ago')
        self.assertEqual(test_object.is_user_anonymous(), False)
        self.assertEqual(test_object.get_user_representer(), 'test_user_one')
        self.assertEqual(test_object.get_user_object_absolute_url(), '#')
        self.assertEqual(test_object.get_target_object_absolute_url(), '#')

    def test_create_log_record_error(self):
        fake_request_object = type('test', (object,), {})()
        fake_user_object = type('test', (object,), {})()
        request = HttpRequest()
        setattr(request, 'user', fake_user_object)
        invalid_log_target = 'invalid_one'
        self.assertRaisesMessage(ValidationError, 'request must be a Django HttpRequest object', create_log_record, fake_request_object)
        self.assertRaisesMessage(ValidationError, 'The request.user object seems to be tempered', create_log_record, request)
        self.assertRaisesMessage(ValidationError, 'log_target must be an instance of an object or none', create_log_record, log_target=invalid_log_target)
