from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import LogRecordsModel
from .configs import ModuleConfigurations


# Create your views here.
class LogRecordsListView(ListView):
    paginate_by = ModuleConfigurations().get_log_records_list_pagination()
    model = LogRecordsModel


class LogRecordsDetailView(DetailView):
    model = LogRecordsModel
