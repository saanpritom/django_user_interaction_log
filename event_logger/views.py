from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from .models import LogRecordsModel
from .configs import ModuleConfigurations
from .mixins import EventLoggerMixin
from django.contrib.auth import get_user_model


# Create your views here.
class LogRecordsListView(ListView):
    paginate_by = ModuleConfigurations().get_log_records_list_pagination()
    model = LogRecordsModel


class LogRecordsDetailView(DetailView):
    model = LogRecordsModel


class TestTemplateView(EventLoggerMixin, TemplateView):
    template_name = 'testview.html'
    event_logger_log_detail_message = 'template test operation'

    def get_log_target_object(self, request, *args, **kwargs):
        return get_user_model().objects.first()
