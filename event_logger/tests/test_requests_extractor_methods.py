from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model, authenticate
from ..requests import RequestExtractor
from ..configs import ModuleConfigurations


class RequestExtractorTestCases(TestCase):
    """This class is testing various methods of RequestExtractor class with different kinds of data.
       You can write your own test case here or can extract this class to add more and more test cases."""
    test_class_name = RequestExtractor()
    config_class = ModuleConfigurations()

    def get_test_user_object(self):
        """We are also creating an user object for running TestCases"""
        if self.config_class.allow_sensitive_test_cases():
            if hasattr(get_user_model(), 'username') and hasattr(get_user_model(), 'password'):
                if get_user_model().objects.exists():
                    return get_user_model().objects.first()
                else:
                    return get_user_model().objects.create_user(username='test_user', email='test@example.com', password='testpass123$#')
            else:
                return None
        else:
            return None

    def setUp(self):
        """This setUp class is creating a HttpRequest object with various type of data. As an example
           at first it creates an empty HttpRequest object and add it to the request_object_list.
           On the second it add GET as the method value and set a new attribute called user and add an user
           object to the attribute and add it to the second element to the request_object_list. At third
           we are setting POST as the method value and sending an authenticated user instance and add it to
           the request_object_list 3rd value"""
        request_object_list = []
        request_object_list.append(HttpRequest())
        request = HttpRequest()
        request.method = 'GET'
        request.user = lambda: None
        setattr(request.user, 'user', self.get_test_user_object())
        request_object_list.append(request)
        request = HttpRequest()
        request.method = 'POST'
        user_object = self.get_test_user_object()
        authenticated_user = authenticate(username=user_object.username, password='testpass123$#')
        request.user = lambda: None
        setattr(request.user, 'user', authenticated_user)
        request_object_list.append(request)
        request = HttpRequest()
        request.method = 'PUT'
        request_object_list.append(request)
        request = HttpRequest()
        request.method = 'PATCH'
        request_object_list.append(request)
        return request_object_list

    def test_extract_actor_id_method(self):
        """Testing the extract_actor_id method of the test_class_name. At first checking with an empty request object"""
        test_objects_list = self.setUp()
        self.assertEqual(self.test_class_name.extract_actor_id(test_objects_list[0]), '0')
        self.assertEqual(self.test_class_name.extract_actor_id(test_objects_list[1].user), '1')
        self.assertEqual(self.test_class_name.extract_actor_id(test_objects_list[2].user), '1')

    def test_construct_log_detail_method(self):
        """Testing the constract_log_detail method of the test_class_name. At first checking with an empty request object"""
        test_objects_list = self.setUp()
        self.assertEqual(self.test_class_name.constract_log_detail(test_objects_list[0]), 'unknown operation')
        self.assertEqual(self.test_class_name.constract_log_detail(delattr(test_objects_list[0], 'method')), 'suspicious operation')
        self.assertEqual(self.test_class_name.constract_log_detail(test_objects_list[1]), 'read operation')
        self.assertEqual(self.test_class_name.constract_log_detail(test_objects_list[2]), 'write operation')
        self.assertEqual(self.test_class_name.constract_log_detail(test_objects_list[3]), 'update operation')
        self.assertEqual(self.test_class_name.constract_log_detail(test_objects_list[4]), 'patch operation')
