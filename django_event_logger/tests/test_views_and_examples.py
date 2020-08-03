from django.test import RequestFactory, TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..views import LogRecordsListView
from ..registrars import create_log_record
from ..examples import ExampleViewWithMixin, example_function_based_view


class ViewTestCases(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create(username='view_tester', email='view_tester@example.com', password='superacces123')
        self.target_user = get_user_model().objects.create(username='target_tester', email='target_tester@example.com', password='superacces123')
        request = HttpRequest()
        setattr(request, 'user', self.user)
        self.log_record = create_log_record(request=request, log_detail='test log view', log_target=self.target_user)

    def test_list_view_response(self):
        request = self.factory.get(reverse('event_logger_list_view'))
        response = LogRecordsListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_example_mixin_view_response(self):
        request = self.factory.get(reverse('event_logger_mixin_example_view'))
        response = ExampleViewWithMixin.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_example_function_view_response(self):
        request = self.factory.get(reverse('event_logger_function_example_view'))
        response = example_function_based_view(request)
        self.assertEqual(response.status_code, 200)
