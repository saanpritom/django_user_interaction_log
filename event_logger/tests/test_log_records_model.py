from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from ..models import LogRecordsModel


class LogRecordsModelTestCase(TestCase):
    """LogRecordsModelTestCase holds and perform the initial test cases for the model of LogRecordsModel.
       It initialize and create some test values and run various tests depends on the value. If you want
       to run your own tests then you may extend this class and run your testcase here"""
    model = LogRecordsModel

    def setUp(self):
        """Setting up some fake datas depends on various scenarios"""
        test_user_one = get_user_model().objects.create(username='test_user_one', email='test_user_one@example.com', password='superacces123one')
        test_user_two = get_user_model().objects.create(username='test_user_two', email='test_user_two@example.com', password='superacces123two')
        self.model.objects.create()
        self.model.objects.create(log_user=test_user_one, log_detail='read operation', log_target=test_user_two, event_path='/test/user/path/')

    def get_test_object(self, id):
        return get_object_or_404(self.model, pk=id)

    def test_log_records_default_data(self):
        """Testing if database default data are working properly"""
        test_object = self.get_test_object(1)
        self.assertEqual(test_object.id, 1)
        self.assertEqual(test_object.user_content_type, None)
        self.assertEqual(test_object.user_object_id, '0')
        self.assertEqual(test_object.log_user, None)
        self.assertEqual(test_object.log_detail, 'no specified operation')
        self.assertEqual(test_object.target_content_type, None)
        self.assertEqual(test_object.target_object_id, None)
        self.assertEqual(test_object.log_target, None)
        self.assertEqual(test_object.event_path, 'n/a')
        self.assertEqual(str(test_object), '1. Anonymous performed no specified operation on None at n/a ' + str(test_object.get_timesince()) + ' ago')
        self.assertEqual(test_object.is_user_anonymous(), True)
        self.assertEqual(test_object.get_user_representer(), 'Anonymous')
        self.assertEqual(test_object.get_user_object_absolute_url(), '#')
        self.assertEqual(test_object.get_target_object_absolute_url(), '#')
        #  performing the clean() method tests
        test_object.user_object_id = None
        test_object.log_detail = None
        test_object.event_path = None
        test_object.clean()
        self.assertEqual(test_object.user_object_id, '0')
        self.assertEqual(test_object.log_detail, 'no specified operation')
        self.assertEqual(test_object.event_path, 'n/a')
        test_object.log_user = self.get_test_object(2)
        self.assertRaises(ValidationError, test_object.clean)
        self.assertRaisesMessage(ValidationError, 'The log user argument must be an User instance', test_object.clean)

    def test_log_records_dummy_data_one(self):
        """Testing if database inserted data are working properly"""
        test_object = self.get_test_object(2)
        test_object.clean()
        self.assertEqual(test_object.id, 2)
        self.assertNotEqual(test_object.user_content_type, None)
        self.assertEqual(test_object.user_object_id, str(get_user_model().objects.get(username='test_user_one').id))
        self.assertEqual(test_object.log_user, get_user_model().objects.get(username='test_user_one'))
        self.assertEqual(test_object.log_detail, 'read operation')
        self.assertNotEqual(test_object.target_content_type, None)
        self.assertEqual(test_object.target_object_id, str(get_user_model().objects.get(username='test_user_two').id))
        self.assertEqual(test_object.log_target, get_user_model().objects.get(username='test_user_two'))
        self.assertEqual(test_object.event_path, '/test/user/path/')
        self.assertEqual(str(test_object), '2. test_user_one performed read operation on test_user_two at /test/user/path/ ' + str(test_object.get_timesince()) + ' ago')
        self.assertEqual(test_object.is_user_anonymous(), False)
        self.assertEqual(test_object.get_user_representer(), 'test_user_one')
        self.assertEqual(test_object.get_user_object_absolute_url(), '#')
        self.assertEqual(test_object.get_target_object_absolute_url(), '#')
