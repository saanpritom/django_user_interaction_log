from django.test import TestCase
from django.contrib.auth import get_user_model
from django_user_interaction_log.models import LogRecordsModel
from django_user_interaction_log.templatetags.model_objects_info import (model_object_meta_data, model_object_fields_list, is_field_printable,
                                                                         model_field_value_object)


class TemplateTagsTestCase(TestCase):
    """Running tests on templatetags"""

    def setUp(self):
        self.test_model_object = type('test', (object,), {})()
        test_meta_object = type('test', (object,), {})()
        setattr(self.test_model_object, '_meta', test_meta_object)
        setattr(self.test_model_object._meta, 'email', 'test_email')
        test_user_one = get_user_model().objects.create(username='test_user_one', email='test_user_one@example.com', password='superacces123one')
        test_user_two = get_user_model().objects.create(username='test_user_two', email='test_user_two@example.com', password='superacces123two')
        self.test_real_model_object = LogRecordsModel.objects.create(log_user=test_user_one, log_detail='read operation', log_target=test_user_two, event_path='/test/user/path/')
        self.test_field_object_without_verbose = type('test', (object,), {})()
        self.test_field_object_with_verbose = type('test', (object,), {})()
        setattr(self.test_field_object_with_verbose, 'verbose_name', 'test verbose')
        self.first_field = self.test_real_model_object._meta.get_fields()[0]

    def test_model_object_meta_data(self):
        self.assertEqual(model_object_meta_data(self.test_model_object, 'email'), 'test_email')
        self.assertEqual(model_object_meta_data(self.test_model_object, 'not_exists_attribute'), None)

    def test_model_object_fields_list(self):
        self.assertGreater(len((model_object_fields_list(self.test_real_model_object))), 0)

    def test_is_field_printable(self):
        self.assertEqual(is_field_printable(self.test_field_object_without_verbose), False)
        self.assertEqual(is_field_printable(self.test_field_object_with_verbose), True)

    def test_model_field_value_object(self):
        self.assertEqual(model_field_value_object(self.first_field, self.test_real_model_object), 1)
        self.assertEqual(model_field_value_object(self.test_model_object, self.test_real_model_object), None)
