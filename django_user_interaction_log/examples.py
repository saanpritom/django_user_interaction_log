from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from .apps import DjangoUserInteractionLogConfig
from .mixins import DjangoUserInteractionLogMixin
from .registrars import create_log_record


class ExampleViewWithMixin(DjangoUserInteractionLogMixin, TemplateView):
    """This example is for the class based view users"""
    template_name = str(DjangoUserInteractionLogConfig.name) + '/example_template.html'
    django_user_interaction_log_detail_message = str(DjangoUserInteractionLogConfig.name) + ' example class view test operation'

    def get_log_target_object(self, request, *args, **kwargs):
        if get_user_model().objects.filter().exists():
            return get_user_model().objects.first()
        return None


def example_function_based_view(request):
    """This example is for the function based view users"""
    target_object = None
    if get_user_model().objects.filter().exists():
        target_object = get_user_model().objects.first()
    create_log_record(request=request, log_detail=str(DjangoUserInteractionLogConfig.name) + ' example function view test operation',
                      log_target=target_object)
    return render(request, str(DjangoUserInteractionLogConfig.name) + '/example_template.html')
