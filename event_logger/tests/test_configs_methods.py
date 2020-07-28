from django.test import TestCase
from django.core.exceptions import ValidationError
from ..configs import ModuleConfigurations


class ModuleConfigurationsTestCases(TestCase):
    """Testing various methods of the ModuleConfigurations class"""
    test_class_name = ModuleConfigurations()

    def setUp(self):
        """Constructing a fake settings object for testing"""
        fake_settings_object_list = []
        fake_settings_object = type('test', (object,), {})()
        fake_settings_object_list.append(fake_settings_object)
        #  Setting EVENT_LOGGER_SETTINGS keyword to the fake_settings_object
        fake_settings_object = type('test', (object,), {})()
        fake_settings_object.EVENT_LOGGER_SETTINGS = lambda: None
        setattr(fake_settings_object.EVENT_LOGGER_SETTINGS, 'EVENT_LOGGER_SETTINGS', {})
        fake_settings_object_list.append(fake_settings_object)
        fake_settings_object = type('test', (object,), {})()
        fake_settings_object.EVENT_LOGGER_SETTINGS = lambda: None
        setattr(fake_settings_object.EVENT_LOGGER_SETTINGS, 'EVENT_LOGGER_SETTINGS', {})
        fake_settings_object.EVENT_LOGGER_SETTINGS.EVENT_LOGGER_SETTINGS['sensitive_test_cases'] = False
        fake_settings_object.EVENT_LOGGER_SETTINGS.EVENT_LOGGER_SETTINGS['user_representer_field'] = 'email'
        fake_settings_object.EVENT_LOGGER_SETTINGS.EVENT_LOGGER_SETTINGS['list_paginated_by'] = 500
        fake_settings_object_list.append(fake_settings_object)
        fake_settings_object = type('test', (object,), {})()
        fake_settings_object.EVENT_LOGGER_SETTINGS = lambda: None
        setattr(fake_settings_object.EVENT_LOGGER_SETTINGS, 'EVENT_LOGGER_SETTINGS', {})
        fake_settings_object.EVENT_LOGGER_SETTINGS.EVENT_LOGGER_SETTINGS['sensitive_test_cases'] = True
        fake_settings_object.EVENT_LOGGER_SETTINGS.EVENT_LOGGER_SETTINGS['user_representer_field'] = True
        fake_settings_object.EVENT_LOGGER_SETTINGS.EVENT_LOGGER_SETTINGS['list_paginated_by'] = 'string data'
        fake_settings_object_list.append(fake_settings_object)
        fake_settings_object = type('test', (object,), {})()
        fake_settings_object.EVENT_LOGGER_SETTINGS = lambda: None
        setattr(fake_settings_object.EVENT_LOGGER_SETTINGS, 'EVENT_LOGGER_SETTINGS', {})
        fake_settings_object.EVENT_LOGGER_SETTINGS.EVENT_LOGGER_SETTINGS['sensitive_test_cases'] = 'Some Value'
        fake_settings_object_list.append(fake_settings_object)
        return fake_settings_object_list

    def test_allow_sensitive_test_cases_method(self):
        test_settings_object_list = self.setUp()
        self.assertEqual(self.test_class_name.default_allow_sensitive_test_case, False)
        self.assertEqual(self.test_class_name.allow_sensitive_test_cases(True, test_settings_object_list[0]), False)
        self.assertEqual(self.test_class_name.allow_sensitive_test_cases(True, test_settings_object_list[1].EVENT_LOGGER_SETTINGS), False)
        self.assertEqual(self.test_class_name.allow_sensitive_test_cases(True, test_settings_object_list[2].EVENT_LOGGER_SETTINGS), False)
        self.assertEqual(self.test_class_name.allow_sensitive_test_cases(True, test_settings_object_list[3].EVENT_LOGGER_SETTINGS), True)
        self.assertRaises(ValidationError, self.test_class_name.allow_sensitive_test_cases, on_test=True,
                          test_settings_object=test_settings_object_list[4].EVENT_LOGGER_SETTINGS)
        self.assertRaisesMessage(ValidationError, 'sensitive_test_cases value is expected a Boolean value',
                                 self.test_class_name.allow_sensitive_test_cases, on_test=True,
                                 test_settings_object=test_settings_object_list[4].EVENT_LOGGER_SETTINGS)

    def test_get_default_user_representer_field(self):
        test_settings_object_list = self.setUp()
        self.assertEqual(self.test_class_name.default_user_representer_field, '__str__')
        self.assertEqual(self.test_class_name.get_default_user_representer_field(True, test_settings_object_list[0]), '__str__')
        self.assertEqual(self.test_class_name.get_default_user_representer_field(True, test_settings_object_list[1].EVENT_LOGGER_SETTINGS), '__str__')
        self.assertEqual(self.test_class_name.get_default_user_representer_field(True, test_settings_object_list[2].EVENT_LOGGER_SETTINGS), 'email')
        self.assertRaises(ValidationError, self.test_class_name.get_default_user_representer_field, on_test=True,
                          test_settings_object=test_settings_object_list[3].EVENT_LOGGER_SETTINGS)
        self.assertRaisesMessage(ValidationError, 'user_representer_field value must be a string',
                                 self.test_class_name.get_default_user_representer_field,
                                 on_test=True, test_settings_object=test_settings_object_list[3].EVENT_LOGGER_SETTINGS)

    def test_get_log_records_list_pagination(self):
        test_settings_object_list = self.setUp()
        self.assertEqual(self.test_class_name.default_log_list_paginated_by, 100)
        self.assertEqual(self.test_class_name.get_log_records_list_pagination(True, test_settings_object_list[0]), 100)
        self.assertEqual(self.test_class_name.get_log_records_list_pagination(True, test_settings_object_list[1].EVENT_LOGGER_SETTINGS), 100)
        self.assertEqual(self.test_class_name.get_log_records_list_pagination(True, test_settings_object_list[2].EVENT_LOGGER_SETTINGS), 500)
        self.assertRaises(ValidationError, self.test_class_name.get_log_records_list_pagination, on_test=True, test_settings_object=test_settings_object_list[3].EVENT_LOGGER_SETTINGS)
        self.assertRaisesMessage(ValidationError, 'list_paginated_by value must be an Integer',
                                 self.test_class_name.get_log_records_list_pagination, on_test=True,
                                 test_settings_object=test_settings_object_list[3].EVENT_LOGGER_SETTINGS)
