from django.test import TestCase
from ..configs import ModuleConfigurations


class ModuleConfigurationsTestCases(TestCase):
    """Testing various methods of the ModuleConfigurations class"""
    test_class_name = ModuleConfigurations()

    def setUp(self):
        pass

    def test_allow_sensitive_test_cases_method(self):
        self.assertEqual(self.test_class_name.default_allow_sensitive_test_case, False)
